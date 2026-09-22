#!/usr/bin/env python3
"""E0 step 1 (local, CPU): build the prompt file for the oracle-intervention experiment.

Takes a stratified sample of Spider-family questions (official Spider dev or Spider-Realistic,
chosen by --dev), serialises each database schema as DDL plus a few example values, and renders
one of the prompt templates below: the XiYanSQL native template (Chinese, ends with an opened
```sql fence), a generic English instruction for general chat models, the OmniSQL template
(also used for Kwai-AutoSQL, which publishes no recipe of its own), the SQLCoder-70B completion
prompt, and the llama-3-sqlcoder-8b chat prompt with its prescribed partial assistant turn. The
output is one JSON object per line, ready to be sampled on the GPU box; each row also carries the
schema block on its own so a negative control can swap it out verbatim, and an answer mode that
tells the sampler how the query arrives in the generation.

--exclude-overlap-with drops every question of --dev that shares (database, gold SQL) or
(database, question text) with another benchmark file, so that a pilot drawn from Spider dev is
disjoint from a Spider-Realistic main set (Preregistration 2, deviation 1).

The sampling policy is written into the output file. The package's interface contract requires
the caller to declare it, because sample frequency only represents class mass under a declared
repeated-sampling policy.
"""
import argparse, collections, json, os, random, re, sqlite3

TEMPLATES = {
    "xiyan_cn": """你是一名{dialect}专家，现在需要阅读并理解下面的【数据库schema】描述，以及可能用到的【参考信息】，并运用{dialect}知识生成sql语句回答【用户问题】。
【用户问题】
{question}

【数据库schema】
{db_schema}

【参考信息】
{evidence}

【用户问题】
{question}

```sql""",
    "generic_en": """You are an expert in {dialect}. Using the database schema below, write one {dialect} query that answers the question.
Return only the query, inside a ```sql code block, with no explanation.

Database schema:
{db_schema}

Question: {question}""",
    # OmniSQL model card, verbatim; Kwai-AutoSQL ships no prompt of its own and is a Qwen3 fine-tune
    # of the same task family, so it takes this template too.
    "omnisql": """Task Overview:
You are a data science expert. Below, you are provided with a database schema and a natural language question. Your task is to understand the schema and generate a valid SQL query to answer the question.

Database Engine:
SQLite

Database Schema:
{db_schema}
This schema describes the database's structure, including tables, columns, primary keys, foreign keys, and any relevant relationships or constraints.

Question:
{question}

Instructions:
- Make sure you only output the information that is asked in the question. If the question asks for a specific column, make sure to only include that column in the SELECT clause, nothing more.
- The generated query should return all of the information asked in the question without any missing or extra information.
- Before generating the final SQL query, please think through the steps of how to write the query.

Output Format:
In your answer, please enclose the generated SQL query in a code block:
```
-- Your SQL query
```

Take a deep breath and think step by step to find the correct SQL query.""",
    # defog-ai/sqlcoder prompt.md (the SQLCoder-70B-alpha / 7b-2 format). The repository's
    # instruction block tells the model to answer "I do not know" when the schema cannot answer
    # the question; it is replaced by a dialect line, because in this design abstention is the
    # certificate's job and every sample has to be a query attempt, as it is for every other model.
    "sqlcoder": """### Task
Generate a SQL query to answer [QUESTION]{question}[/QUESTION]

### Instructions
- The query will run on a SQLite database; use SQLite syntax.

### Database Schema
The query will run on a database with the following schema:
{db_schema}

### Answer
Given the database schema, here is the SQL query that answers [QUESTION]{question}[/QUESTION]
[SQL]""",
    # llama-3-sqlcoder-8b model card: user turn below, then the assistant turn is opened with the
    # prescribed prefix (ASSISTANT_PREFIX), which ends inside a ```sql fence.
    "llama3_sqlcoder": """Generate a SQL query to answer this question: `{question}`
- The query will run on a SQLite database; use SQLite syntax.

DDL statements:
{db_schema}""",
}

# How the query arrives in the generation; the sampler's extractor follows this.
#   continuation: the prompt or the assistant prefix ends inside an opened ```sql fence, the model
#                 continues inside it, and the answer is everything before the closing fence
#   fenced:       the model writes prose of its own and encloses the query in a fenced block; the
#                 last non-empty block is the answer (a chain of thought may draft earlier ones)
#   bare:         the answer is the raw continuation, ended by [/SQL], a new ### section or EOS
ANSWER_MODE = {"xiyan_cn": "continuation", "generic_en": "fenced", "omnisql": "fenced",
               "sqlcoder": "bare", "llama3_sqlcoder": "continuation"}

# Partial assistant turn appended after the chat template's generation prompt, where the model
# card prescribes one.
ASSISTANT_PREFIX = {"llama3_sqlcoder": "The following SQL query best answers the question `{question}`:\n```sql\n"}


def norm(s):
    return re.sub(r"\s+", " ", s.strip().rstrip(";").strip()).lower()


def schema_ddl(path, max_values=3):
    """CREATE TABLE statements plus a few example values per column."""
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    con.text_factory = lambda b: b.decode("utf-8", "replace")
    parts = []
    tables = [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    for t in tables:
        ddl = con.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (t,)).fetchone()
        if not ddl or not ddl[0]:
            continue
        parts.append(ddl[0].strip().rstrip(";") + ";")
        try:
            cols = [r[1] for r in con.execute(f'PRAGMA table_info("{t}")')]
            rows = con.execute(
                f'SELECT * FROM "{t}" LIMIT {max_values}').fetchall()
            if rows and cols:
                ex = []
                for i, c in enumerate(cols):
                    vals = [str(r[i]) for r in rows if r[i] is not None][:max_values]
                    if vals:
                        ex.append(f"{c}: " + ", ".join(v[:40] for v in vals))
                if ex:
                    parts.append(f"-- example values in {t}: " + " | ".join(ex))
        except Exception:
            pass
    con.close()
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev", default="data/spider/dev.json")
    ap.add_argument("--suite-root", default="data/spider/test_suite_database")
    ap.add_argument("--n", type=int, default=500)
    ap.add_argument("--seed", type=int, default=20260903)
    ap.add_argument("--template", choices=tuple(TEMPLATES), default="xiyan_cn")
    ap.add_argument("--exclude-overlap-with", default="",
                    help="benchmark file whose (database, gold SQL) and (database, question) pairs "
                         "are removed from --dev before sampling, so a pilot set is disjoint from "
                         "the main set")
    ap.add_argument("--out", default="experiments/e0_prompts.jsonl")
    a = ap.parse_args()

    dev = json.load(open(a.dev))
    for i, r in enumerate(dev):
        r["qid"] = i          # position in the source file; stable across exclusion

    excluded = 0
    if a.exclude_overlap_with:
        other = json.load(open(a.exclude_overlap_with))
        sql_keys = {(r["db_id"], norm(r["query"])) for r in other}
        q_keys = {(r["db_id"], norm(r["question"])) for r in other}
        pool = [r for r in dev if (r["db_id"], norm(r["query"])) not in sql_keys
                and (r["db_id"], norm(r["question"])) not in q_keys]
        excluded = len(dev) - len(pool)
    else:
        pool = dev

    # proportional stratified sample by database, deterministic under the seed
    by_db = collections.defaultdict(list)
    for r in pool:
        by_db[r["db_id"]].append(r)
    rng = random.Random(a.seed)
    picked = []
    dbs = sorted(by_db)
    quota = {d: max(1, round(a.n * len(by_db[d]) / len(pool))) for d in dbs}
    for d in dbs:
        p = sorted(by_db[d], key=lambda r: r["qid"])
        rng.shuffle(p)
        picked += p[: quota[d]]
    picked.sort(key=lambda r: r["qid"])
    if len(picked) > a.n:
        keep = set(rng.sample([r["qid"] for r in picked], a.n))
        picked = [r for r in picked if r["qid"] in keep]

    cache = {}
    n_written = 0
    with open(a.out, "w") as f:
        for r in picked:
            db = r["db_id"]
            if db not in cache:
                p = os.path.join(a.suite_root, db, f"{db}.sqlite")
                cache[db] = schema_ddl(p)
            prompt = TEMPLATES[a.template].format(dialect="SQLite", question=r["question"],
                                                  db_schema=cache[db], evidence="")
            row = {
                "qid": r["qid"], "db_id": db, "question": r["question"],
                "gold": r["query"], "prompt": prompt,
                "schema_block": cache[db], "template": a.template,
                "answer_mode": ANSWER_MODE[a.template],
            }
            if a.template in ASSISTANT_PREFIX:
                row["assistant_prefix"] = ASSISTANT_PREFIX[a.template].format(question=r["question"])
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            n_written += 1

    meta = {
        "experiment": "E0 oracle intervention 2x2",
        "split": ("matched original Spider dev wording, Spider-Realistic item set"
                  if "matched-original" in os.path.basename(a.dev)
                  else "Spider-Realistic (Spider dev schemas)" if "realistic" in a.dev.lower()
                  else "official Spider dev"),
        "source_file": a.dev,
        "source_questions": len(dev),
        "exclusion": ({"file": a.exclude_overlap_with,
                       "rule": "drop every source question sharing (database, normalised gold SQL) "
                               "or (database, normalised question) with the file",
                       "excluded": excluded, "pool_after_exclusion": len(pool)}
                      if a.exclude_overlap_with else None),
        "sampling_policy": {
            "kind": "independent temperature sampling, fixed budget",
            "n_samples_per_question": "declared by the sampling run, see *_candidates_meta.json",
            "temperature": 1.0,
            "top_p": 0.95,
            "seed": a.seed,
            "note": "declared because sample frequency only represents equivalence-class mass "
                    "under a declared repeated-sampling policy; it is not valid for deduplicated "
                    "beam or top-k candidate lists",
        },
        "questions": n_written,
        "databases": len({r["db_id"] for r in picked}),
        "question_selection": f"proportional stratified by database, seed {a.seed}",
        "prompt_template": a.template,
        "answer_mode": ANSWER_MODE[a.template],
        "assistant_prefix": ASSISTANT_PREFIX.get(a.template),
        "schema_serialisation": "sqlite_master DDL plus up to 3 example values per column",
    }
    json.dump(meta, open(a.out.replace(".jsonl", "_meta.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(meta, ensure_ascii=False, indent=1))
    lens = [len(json.loads(l)["prompt"]) for l in open(a.out)]
    print(f"prompt chars: min {min(lens)} median {sorted(lens)[len(lens)//2]} max {max(lens)}")


if __name__ == "__main__":
    main()
