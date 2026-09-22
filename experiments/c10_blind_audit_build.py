#!/usr/bin/env python3
"""C10 step 1: build the blinded human expert audit package for the benchmark gold queries.

Why this exists. One load-bearing assumption is otherwise unverified: that a same-model-family AI
audit correctly separates a genuine semantic error from a defective reference query. Cohen's kappa
and two independent passes establish that the labelling is REPEATABLE. They establish nothing about
whether it is RIGHT. The whole benchmark-validity headline rests on that difference, so it has to
be measured by people who are not the labeller and who cannot see what the labeller said.

What the expert judges, and why it is the gold alone. The task is: given the natural-language
question, the schema and the database, is this reference query a correct rendering of the question?
No model output is shown. That matters for three reasons. It removes the strongest anchor, because
a reader shown "the model said X and the gold said Y" is being invited to prefer X. It makes the
task well defined and fast. And it yields exactly the quantity the paper needs, an estimate of the
gold defect rate that was produced without reference to any model.

The defect families the AI audit reported are all visible from the question, the schema and the
gold's own execution behaviour: a case-sensitive literal that never matches, an ORDER BY over a
TEXT column holding numbers, MAX where the question asks for the youngest, a JOIN without its ON,
a negated filter, an incomplete projection, a set operation over names rather than keys. So the
protocol asks the expert to RUN the gold and read its result, not only to read the SQL.

Three strata, and mixing them would be the design error. The 508 questions split into:

  flagged      the 73 the AI audit gave at least one gold_defect label
  examined     the 130 the census looked at and did NOT flag. The AI saw a suite-rejected answer
               on these and judged the gold fine, so comparing flagged against these measures
               whether the AI's flag DISCRIMINATES
  unexamined   the 305 no case ever covered, because the suite rejected no answer of theirs. These
               estimate the BACKGROUND gold defect rate of the benchmark, which is the quantity a
               benchmark-validity claim ultimately needs, and it is not the same quantity

Blinding. The three strata are pooled, shuffled under a fixed seed and given opaque ids that encode
nothing. The expert receives only the blind-audit/ directory: the protocol, the item sheet and the
response template. The key that maps an id back to its stratum and question id is written under
experiments/ and is not part of what the expert is given. That separation is a convention, not a
cryptographic guarantee, and the protocol says so.

There is no contrast pass in this package, deliberately. Showing the expert the model answer beside
the gold would be informative, but it cannot be blinded: items from the unexamined stratum have no
model answer by construction, so showing one only where it exists tells the expert which items came
from the census. Whether to run an unblinded contrast pass afterwards is a separate decision, and
its result could not be substituted for this one.
"""
import argparse, collections, hashlib, json, os, random, sqlite3, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

VERDICTS = ("gold_correct", "gold_defective", "question_underspecified", "cannot_judge")
DEFECTS = ("case_sensitivity", "text_column_numeric_or_ordering", "wrong_extremum",
           "missing_join_condition", "wrong_or_negated_filter", "incomplete_projection",
           "wrong_set_operation_key", "wrong_grouping", "other")


def schema_lines(path):
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    out = []
    for (name,) in con.execute("SELECT name FROM sqlite_master WHERE type='table' "
                               "AND name NOT LIKE 'sqlite_%' ORDER BY name"):
        cols = [f"{r[1]} {r[2]}" for r in con.execute(f'PRAGMA table_info("{name}")')]
        out.append(f"  {name}({', '.join(cols)})")
    con.close()
    return out


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def strata(cases_path, audit_path, pool_path, per_question_path):
    """The three strata and the per-question metadata, straight from the frozen artifacts."""
    cases = {c["case_id"]: c for c in json.load(open(cases_path))["cases"]}
    rows = json.load(open(audit_path))["cases"]
    flagged, tier = set(), {}
    for r in rows:
        if r["label"] != "gold_defect":
            continue
        q = cases[r["case_id"]]["qid"]
        flagged.add(q)
        agreed = r.get("label_a") == "gold_defect" and r.get("label_b") == "gold_defect"
        firm = agreed and not (r.get("borderline_a") or r.get("borderline_b"))
        prev = tier.get(q, "adjudicated_only")
        tier[q] = ("two_pass_non_borderline" if firm or prev == "two_pass_non_borderline"
                   else "two_pass_agreed" if agreed or prev == "two_pass_agreed"
                   else prev)
    examined = {c["qid"] for c in cases.values()} - flagged
    meta = {}
    for line in open(pool_path):
        r = json.loads(line)
        meta[r["qid"]] = {"question": r["question"], "gold": r["gold"], "db": r["db_id"]}
    allq = {q["qid"] for q in json.load(open(per_question_path))["questions"]}
    unexamined = allq - flagged - examined
    return {"flagged": sorted(flagged), "examined": sorted(examined),
            "unexamined": sorted(unexamined)}, tier, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default="experiments/c7_repair_cases.json")
    ap.add_argument("--audit", default="experiments/c7_semantic_audit.json")
    ap.add_argument("--pool", default="experiments/c4_kwai-autosql-14b_seed101_candidates.jsonl")
    ap.add_argument("--per-question",
                    default="experiments/c4_kwai-autosql-14b_seed101_results_official_per_question.json")
    ap.add_argument("--suite-root", default="data/spider/test_suite_database")
    ap.add_argument("--n-examined", type=int, default=40,
                    help="control drawn from the questions the census examined and did not flag")
    ap.add_argument("--n-unexamined", type=int, default=40,
                    help="control drawn from the questions no case ever covered")
    ap.add_argument("--all", action="store_true",
                    help="take every question of all three strata, 508 items")
    ap.add_argument("--seed", type=int, default=20260906,
                    help="the draw and the shuffle are fixed by this seed and preregistered")
    ap.add_argument("--out-dir", default="blind-audit")
    ap.add_argument("--key", default="experiments/c10_blind_audit_key.json")
    a = ap.parse_args()

    S, tier, meta = strata(a.cases, a.audit, a.pool, a.per_question)
    rng = random.Random(a.seed)
    pick = {"flagged": list(S["flagged"])}
    for name, n in (("examined", a.n_examined), ("unexamined", a.n_unexamined)):
        pool = list(S[name])
        pick[name] = pool if a.all else sorted(rng.sample(pool, min(n, len(pool))))
    items = [(q, s) for s, qs in pick.items() for q in qs]
    rng.shuffle(items)

    key, lines = [], []
    for i, (qid, stratum) in enumerate(items, 1):
        iid = f"Q{i:03d}"
        key.append({"item_id": iid, "qid": qid, "stratum": stratum, "db": meta[qid]["db"],
                    "ai_gold_defect_tier": tier.get(qid)})
        m = meta[qid]
        lines.append(f"### {iid}\n")
        lines.append(f"Database: `{m['db']}`  (schema in the appendix)\n")
        lines.append(f"**Question.** {m['question']}\n")
        lines.append("**Reference query under review.**\n```sql\n" + m["gold"].strip() + "\n```\n")
        lines.append("Verdict: ______  Defect type: ______  Borderline: ______\n")
        lines.append("Note:\n\n")

    dbs = sorted({meta[q]["db"] for q, _ in items})
    head = [
        "# Blinded review of benchmark reference queries\n",
        f"{len(items)} items. Read `PROTOCOL.md` before starting, and record every verdict in "
        f"`RESPONSES.csv`.\n",
        "For each item you are given a natural-language question and the reference query the "
        "benchmark ships as its correct answer. Your task is to judge **the reference query**: "
        "does it correctly answer the question against this database? Run it. No model output is "
        "shown anywhere in this package, and the items are in a shuffled order that carries no "
        "information.\n",
        "\n## Items\n",
    ]
    tail = ["\n## Schema appendix\n"]
    for db in dbs:
        p = os.path.join(a.suite_root, db, f"{db}.sqlite")
        tail.append(f"### `{db}`\n\nRun queries against `{p}`.\n\n```")
        tail += schema_lines(p) if os.path.isfile(p) else ["  (database file not found)"]
        tail.append("```\n")

    os.makedirs(a.out_dir, exist_ok=True)
    items_path = os.path.join(a.out_dir, "ITEMS.md")
    open(items_path, "w").write("\n".join(head + lines + tail))

    resp = os.path.join(a.out_dir, "RESPONSES.csv")
    with open(resp, "w") as f:
        f.write("item_id,verdict,defect_type,borderline,note\n")
        for k in key:
            f.write(f"{k['item_id']},,,,\n")

    counts = collections.Counter(s for _, s in items)
    out = {
        "built": time.strftime("%Y-%m-%d"),
        "seed": a.seed,
        "note": "the key maps a blinded item id back to its question and stratum. It is NOT part "
                "of what the expert receives; the expert gets the blind-audit/ directory only.",
        "strata_sizes_in_the_benchmark": {k: len(v) for k, v in S.items()},
        "sampled": dict(counts),
        "items": len(items),
        "verdict_vocabulary": VERDICTS,
        "defect_vocabulary": DEFECTS,
        "items_sha256": sha256_file(items_path),
        "key": key,
    }
    json.dump(out, open(a.key, "w"), indent=1, ensure_ascii=False)

    print(f"strata in the benchmark: " + ", ".join(f"{k} {len(v)}" for k, v in S.items()))
    print(f"sampled: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    print(f"  flagged by AI-label strength: "
          + ", ".join(f"{k} {v}" for k, v in sorted(collections.Counter(
              tier[q] for q in pick['flagged']).items())))
    print(f"written {items_path} ({os.path.getsize(items_path) / 1024:.0f} KB), {resp}, {a.key}")
    print(f"item sheet sha256 {out['items_sha256'][:16]}...")


if __name__ == "__main__":
    main()
