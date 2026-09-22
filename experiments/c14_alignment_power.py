#!/usr/bin/env python3
"""Precision of the paired AUROC contrast the independent-yardstick audit will estimate.

On the questions where both cells return the same SQL the answer is one object, so a single human
verdict serves both cells and the two cells differ only in the score they attach to it. The endpoint
is then a paired comparison of two scores predicting one binary outcome, which is the most
favourable shape this comparison can have.

The human labels do not exist yet, so the effect size cannot be known. What can be computed now is
the sampling precision of the contrast at a given number of audited questions, using the suite
oracle's labels to supply a realistic correctness base rate and a realistic correlation between the
two scores. The standard error below is therefore a design quantity; the effect size measured
against suite labels is NOT a prediction of the effect against human labels, and is reported here
only to show what the audit is powered to separate.

Run before the item sheet is frozen. Reported in PREREGISTRATION_4.md.
"""
import json, os, random, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c4_recompute import load, pool_files
from c11_dma_decomposition import top_reps

TAGS = ("xiyansql-32b", "kwai-autosql-32b")
SEED = 101


def auroc(pairs):
    """Mann-Whitney AUROC for predicting CORRECTNESS from a confidence score, ties at half credit.

    Table A6's convention: the positive class is a correct answer, so a useful score scores above 0.5.
    """
    pos = [s for s, y in pairs if y]
    neg = [s for s, y in pairs if not y]
    if not pos or not neg:
        return None
    order = sorted(set(s for s, _ in pairs))
    rank = {s: i for i, s in enumerate(order)}
    tot = 0.0
    for p in pos:
        for n in neg:
            tot += 1.0 if rank[p] > rank[n] else 0.5 if rank[p] == rank[n] else 0.0
    return tot / (len(pos) * len(neg))


def items(tag):
    """Same-SQL questions with the two cells' scores and the shared suite-oracle verdict."""
    qs = load(pool_files(tag, SEED, "question"))
    ra, rd = top_reps(qs, "single"), top_reps(qs, "multi")
    out = []
    for q in qs:
        i = q["qid"]
        if i not in ra or i not in rd or ra[i] != rd[i]:
            continue
        best = {}
        for key, part in (("A", "single"), ("D", "multi")):
            cls = q[part]
            n = sum(c["count"] for c in cls)
            masses = [c["count"] / n for c in cls]
            top = cls[[j for j, m in enumerate(masses) if m == max(masses)][0]]
            best[key] = (max(masses), top["strong_ok"])
        assert best["A"][1] == best["D"][1], "same SQL judged differently by the same oracle"
        out.append({"qid": i, "score_a": best["A"][0], "score_d": best["D"][0], "ok": best["A"][1]})
    return out


def main():
    rng = random.Random(20260908)
    report = {"note": __doc__.strip().splitlines()[0], "checkpoints": {}}
    for tag in TAGS:
        it = items(tag)
        base = sum(1 for r in it if not r["ok"]) / len(it)
        a = auroc([(r["score_a"], r["ok"]) for r in it])
        d = auroc([(r["score_d"], r["ok"]) for r in it])
        row = {"same_sql_questions": len(it), "wrong_rate_suite": round(base, 4),
               "auroc_a_suite": round(a, 4), "auroc_d_suite": round(d, 4),
               "delta_suite": round(d - a, 4), "paired_se": {}}
        for n in (508, 400, 300, 200):
            n = min(n, len(it))
            deltas = []
            for _ in range(400):
                s = [it[rng.randrange(len(it))] for _ in range(n)]
                aa = auroc([(r["score_a"], r["ok"]) for r in s])
                dd = auroc([(r["score_d"], r["ok"]) for r in s])
                if aa is not None and dd is not None:
                    deltas.append(dd - aa)
            se = statistics.stdev(deltas)
            row["paired_se"][n] = {"se": round(se, 4), "mde_95": round(1.96 * se, 4)}
        report["checkpoints"][tag] = row
        print(f"{tag:<20} same-SQL questions {len(it)}  wrong under suite {base*100:.1f}%  "
              f"AUROC A {a:.3f}  D {d:.3f}  delta {d-a:+.3f}")
        for n, v in row["paired_se"].items():
            print(f"    n={n:<4} paired SE {v['se']:.4f}   smallest delta separable at 95% {v['mde_95']:.3f}")
    json.dump(report, open("experiments/c14_alignment_power.json", "w"), indent=1)
    print("\nSaved: experiments/c14_alignment_power.json")


if __name__ == "__main__":
    main()
