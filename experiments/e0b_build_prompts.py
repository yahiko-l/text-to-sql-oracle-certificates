#!/usr/bin/env python3
"""E0b step 1 (local, CPU): build prompts for a text2sql-data benchmark with a distilled suite.

E0 needs a benchmark that supplies BOTH a weak oracle (one database) and a strong one (many).
Spider supplies both, and it is the only such public benchmark: the eight text2sql-data tasks
that the distilled-suite release covers ship a database with no rows in it, which the official
classical evaluator never executes against and its own cache key names the empty database path.

So the weak oracle here is the lexicographically first instance of the question's OWN official
test suite, and the strong oracle is that whole suite. That substitution is not a free choice.
It was measured on Spider first, where both definitions exist, and it moved every cell of the
2x2 by less than a point; only then was it carried over here.

Two further consequences of the per-question suite, both handled below: the example values in
the prompt come from the weak-oracle instance, exactly as Spider's come from the one database it
ships, so the prompt never shows the model a database the weak oracle does not score on; and the
instance list travels in the output so the analysis uses the official per-question suite rather
than the whole directory.
"""
import argparse, collections, json, os, pickle, random, sqlite3

TEMPLATE = """你是一名{dialect}专家，现在需要阅读并理解下面的【数据库schema】描述，以及可能用到的【参考信息】，并运用{dialect}知识生成sql语句回答【用户问题】。
【用户问题】
{question}

【数据库schema】
{db_schema}

【参考信息】
{evidence}

【用户问题】
{question}

```sql"""


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
            rows = con.execute(f'SELECT * FROM "{t}" LIMIT {max_values}').fetchall()
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
    ap.add_argument("--gold", default="data/classical/classical_test.pkl")
    ap.add_argument("--suite-root", default="data/spider/test_suite_database")
    ap.add_argument("--task", default="advising")
    ap.add_argument("--n", type=int, default=500)
    ap.add_argument("--seed", type=int, default=20260903)
    ap.add_argument("--out", default="experiments/e0b_prompts.jsonl")
    a = ap.parse_args()

    gold = pickle.load(open(a.gold, "rb"))
    items = [g for g in gold if g["db_id"] == a.task]
    if not items:
        raise SystemExit(f"no questions for task {a.task}; have "
                         f"{sorted({g['db_id'] for g in gold})}")
    for i, g in enumerate(items):
        g["qid"] = i

    empty_db = f"{a.task}.sqlite"
    usable = []
    for g in items:
        insts = sorted({os.path.basename(p) for p in g["testsuite"]} - {empty_db})
        if not insts:
            continue
        g["instances"] = insts
        usable.append(g)

    rng = random.Random(a.seed)
    picked = usable[:]
    rng.shuffle(picked)
    picked = picked[: a.n]
    picked.sort(key=lambda g: g["qid"])

    ddir = os.path.join(a.suite_root, a.task)
    cache, n_written, suite_sizes = {}, 0, []
    with open(a.out, "w") as f:
        for g in picked:
            weak = g["instances"][0]
            if weak not in cache:
                cache[weak] = schema_ddl(os.path.join(ddir, weak))
            prompt = TEMPLATE.format(dialect="SQLite", question=g["text"],
                                     db_schema=cache[weak], evidence="")
            f.write(json.dumps({
                "qid": g["qid"], "db_id": a.task, "question": g["text"],
                "gold": g["query"].strip().rstrip(";").strip(),
                "instances": g["instances"], "prompt": prompt,
            }, ensure_ascii=False) + "\n")
            suite_sizes.append(len(g["instances"]))
            n_written += 1

    suite_sizes.sort()
    meta = {
        "experiment": "E0b oracle intervention 2x2, second benchmark axis",
        "benchmark": f"text2sql-data {a.task}, distilled test suites (Zhong et al. 2020)",
        "weak_oracle": "first_suite_instance",
        "weak_oracle_note": "the shipped database of every text2sql-data task holds no rows, so "
                            "the populated single database Spider supplies does not exist here; "
                            "the substitution was validated on Spider before being used",
        "sampling_policy": {
            "kind": "independent temperature sampling, fixed budget",
            "n_samples_per_question": 20, "temperature": 1.0, "top_p": 0.95,
            "max_tokens": 512, "seed": a.seed,
        },
        "questions_available": len(items),
        "questions_with_a_suite": len(usable),
        "questions": n_written,
        "suite_instances_per_question": {
            "min": suite_sizes[0], "median": suite_sizes[len(suite_sizes) // 2],
            "max": suite_sizes[-1],
        },
        "distinct_weak_oracle_instances": len(cache),
        "question_selection": f"uniform without replacement, seed {a.seed}",
        "model": "XGenerationLab/XiYanSQL-QwenCoder-32B-2504",
        "prompt_template": "XiYanSQL nl2sqlite_template_cn, dialect=SQLite, evidence empty",
        "schema_serialisation": "DDL of the weak-oracle instance plus up to 3 example values",
    }
    json.dump(meta, open(a.out.replace(".jsonl", "_meta.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(meta, ensure_ascii=False, indent=1))
    lens = [len(json.loads(l)["prompt"]) for l in open(a.out)]
    print(f"prompt chars: min {min(lens)} median {sorted(lens)[len(lens)//2]} max {max(lens)}")


if __name__ == "__main__":
    main()
