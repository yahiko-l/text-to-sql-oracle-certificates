#!/usr/bin/env python3
"""Counts of the suite-ACCEPTED side of the current-practice cell, which no census examined.

The full census (c7) labelled every answer the multi-instance suite oracle REJECTS. This script
records, deterministically from the archived per-question files, how many answers the suite
ACCEPTS in cell A, how many distinct (question, SQL) outputs that is, and how many of those sit on
a question that carries at least one gold_defect verdict (the set the reverse stress test flips).
Same tie rule as the census scripts: the first-listed class of the per-question file, i.e. the
archived file-order population.
"""
import argparse, collections, json

TAGS = ["kwai-autosql-32b", "kwai-autosql-14b", "xiyansql-32b", "omnisql-32b"]
SEEDS = [101, 202, 303]


def top_index(cls):
    best = max(c["count"] for c in cls)
    return next(i for i, c in enumerate(cls) if c["count"] == best)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", default="experiments/c7_semantic_audit.json")
    ap.add_argument("--out", default="experiments/c7_accepted_side.json")
    a = ap.parse_args()
    audit = json.load(open(a.audit))
    flagged = sorted({c["qid"] for c in audit["cases"] if c["label"] == "gold_defect"})
    fl = set(flagged)
    per_pool, accepted_pairs, flagged_pairs = {}, set(), set()
    tot = collections.Counter()
    for tag in TAGS:
        for seed in SEEDS:
            qs = json.load(open(f"experiments/c4_{tag}_seed{seed}_results_official_per_question.json"))["questions"]
            c = collections.Counter()
            for q in qs:
                cls = q["single"]
                if not cls:
                    c["no_usable_class"] += 1
                    continue
                top = cls[top_index(cls)]
                c["answers"] += 1
                if top["strong_ok"]:
                    c["accepted"] += 1
                    accepted_pairs.add((q["qid"], top["representative"]))
                    if q["qid"] in fl:
                        c["accepted_on_flagged_question"] += 1
                        flagged_pairs.add((q["qid"], top["representative"]))
                else:
                    c["rejected"] += 1
            per_pool[f"{tag}|seed{seed}"] = dict(c)
            tot.update(c)
    out = {
        "note": "cell A of every main pool under the archived file-order tie rule; 'accepted' means the "
                "top class of the original-database partition is correct under the multi-instance suite "
                "oracle. No census examined any accepted answer. 'flagged' questions carry at least one "
                "gold_defect verdict in the full census; the reverse stress test counts every accepted "
                "answer on them as wrong.",
        "flagged_questions": len(flagged),
        "answers": tot["answers"],
        "accepted": tot["accepted"],
        "accepted_share": round(tot["accepted"] / tot["answers"], 4),
        "rejected": tot["rejected"],
        "accepted_distinct_question_sql": len(accepted_pairs),
        "accepted_on_flagged_question": tot["accepted_on_flagged_question"],
        "accepted_on_flagged_question_share_of_answers": round(tot["accepted_on_flagged_question"] / tot["answers"], 4),
        "accepted_on_flagged_question_distinct": len(flagged_pairs),
        "per_pool": per_pool,
    }
    json.dump(out, open(a.out, "w"), indent=1)
    print({k: v for k, v in out.items() if k not in ("per_pool", "note")})


if __name__ == "__main__":
    main()
