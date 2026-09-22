#!/usr/bin/env python3
"""Build the blinded expert package for the independent-yardstick test of oracle alignment.

Preregistered in PREREGISTRATION_4.md. What the expert judges is one question, its schema and ONE
returned SQL: does this query answer the question. No reference query is shown, because the point of
this round is a yardstick that neither oracle produced, and a reference query is what both oracles
are made of. No score, no cell, no AI label, no stratum.

The primary endpoint lives on the questions where the two cells return the same SQL. There the
answer is a single object, so one verdict serves both cells and the cells differ only in the score
they attach to it. Those items and the few changed-SQL items are pooled, shuffled under a fixed
seed and given opaque ids, so the sheet does not reveal which of the two a given item is.

The key mapping an id back to its checkpoint, question and cell is written under experiments/ and is
not part of what the expert receives. That separation is a convention, not a guarantee, and the
protocol says so.
"""
import argparse, hashlib, json, os, random, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c4_recompute import load, pool_files
from c10_blind_audit_build import schema_lines
from c11_dma_decomposition import top_reps

TAGS = ("xiyansql-32b", "kwai-autosql-32b")
GEN_SEED = 101
VERDICTS = ("answers", "does_not_answer", "question_underspecified", "cannot_judge")


def collect():
    """Distinct (question, SQL) items, each with every checkpoint-and-cell it serves.

    Deduplicating across checkpoints matters twice: an expert should not judge one query twice, and
    a repeat is the one thing in a shuffled sheet a reader could notice.
    """
    items, meta = {}, {}
    for tag in TAGS:
        qs = load(pool_files(tag, GEN_SEED, "question"))
        ra, rd = top_reps(qs, "single"), top_reps(qs, "multi")
        text = {q["qid"]: q for q in qs}
        for qid in sorted(set(ra) & set(rd)):
            same = ra[qid] == rd[qid]
            for cell, sql in (("A", ra[qid]), ("D", rd[qid])):
                k = (qid, sql)
                use = {"tag": tag, "cell": cell, "same_sql": same}
                if use not in items.setdefault(k, []):
                    items[k].append(use)
                meta[k] = {"qid": qid, "db": text[qid]["db"]}
    return items, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--suite-root", default="data/spider/test_suite_database")
    ap.add_argument("--out-dir", default="alignment-audit")
    ap.add_argument("--key", default="experiments/c15_alignment_audit_key.json")
    ap.add_argument("--seed", type=int, default=20260908)
    a = ap.parse_args()

    # The candidate archives carry the question text against the same qid the analyser used,
    # so they are the source that cannot drift out of alignment with the per-question files.
    qtext = {}
    for tag in TAGS:
        path = f"experiments/c4_{tag}_seed{GEN_SEED}_candidates.jsonl"
        with open(path) as f:
            for line in f:
                r = json.loads(line)
                qtext[r["qid"]] = r["question"]

    items, meta = collect()
    rows = []
    for k, uses in items.items():
        qid, sql = k
        rows.append({**meta[k], "sql": sql, "uses": uses, "question": qtext.get(qid, "")})
    rng = random.Random(a.seed)
    rng.shuffle(rows)
    for i, r in enumerate(rows):
        r["item_id"] = f"AL{i + 1:04d}"

    os.makedirs(a.out_dir, exist_ok=True)
    dbs = sorted({r["db"] for r in rows})
    lines = ["# Item sheet", "",
             f"{len(rows)} items. For each one: read the question, run the SQL on the named database,",
             "and record one verdict in RESPONSES.csv. Schemas are listed at the end.", ""]
    for r in rows:
        lines += [f"## {r['item_id']}", "",
                  f"Question: {r['question'] or '(see the database and the query)'}", "",
                  f"Database: `{r['db']}`", "", "```sql", r["sql"].strip(), "```", ""]
    lines += ["", "# Schemas", ""]
    for db in dbs:
        p = os.path.join(a.suite_root, db, f"{db}.sqlite")
        lines += [f"## {db}", ""]
        lines += schema_lines(p) if os.path.isfile(p) else ["  (database file not found)"]
        lines += [""]
    sheet = "\n".join(lines)
    open(os.path.join(a.out_dir, "ITEMS.md"), "w").write(sheet)

    with open(os.path.join(a.out_dir, "RESPONSES.csv"), "w") as f:
        f.write("item_id,verdict,note\n")
        for r in rows:
            f.write(f"{r['item_id']},,\n")

    digest = hashlib.sha256(sheet.encode()).hexdigest()
    key = {"built": time.strftime("%Y-%m-%d"), "seed": a.seed,
           "note": "key for PREREGISTRATION_4; not part of the expert package",
           "checkpoints": list(TAGS), "generation_seed": GEN_SEED,
           "verdict_vocabulary": list(VERDICTS),
           "items": len(rows),
           "checkpoint_cell_uses": sum(len(r["uses"]) for r in rows),
           "items_serving_only_same_sql": sum(1 for r in rows if all(u["same_sql"] for u in r["uses"])),
           "items_sha256": digest,
           "key": [{"item_id": r["item_id"], "qid": r["qid"], "db": r["db"], "uses": r["uses"]}
                   for r in rows]}
    json.dump(key, open(a.key, "w"), indent=1)

    print(f"items {len(rows)}  checkpoint-cell uses {key['checkpoint_cell_uses']}  "
          f"serving only same-SQL cells {key['items_serving_only_same_sql']}")
    print(f"databases {len(dbs)}   questions with text {sum(1 for r in rows if r['question'])}")
    print(f"items_sha256 {digest}")
    print(f"Saved: {a.out_dir}/ITEMS.md, {a.out_dir}/RESPONSES.csv, {a.key}")


if __name__ == "__main__":
    main()
