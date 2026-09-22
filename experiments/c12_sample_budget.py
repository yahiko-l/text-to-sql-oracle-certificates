#!/usr/bin/env python3
"""How the understatement and the score's resolution depend on the sample budget.

Appendix A makes score resolution the boundary at which the intervention stops doing anything: on
official Spider dev the score took eleven distinct values and the contrast vanished. That boundary
is load-bearing, so it is tested inside the main panel rather than only on another dataset.

GAP is a quantity of cell A alone, the risk its own weak labels report subtracted from the risk the
suite oracle assigns at the same threshold, so it depends only on the single-database partition.
Drawing m of a question's usable candidates without replacement and recounting that partition is
therefore an exact reduction of the budget for GAP, for the flip rate, and for every resolution
statistic below.

D minus A is NOT recomputed here. It needs both cells at once, and the archived per-question files
carry the two partitions marginally rather than their joint, so a budget drawn independently for
each would put the two cells on different candidate subsets and manufacture partition disagreement.
Reducing the budget for that contrast needs the analyser re-run over the suite instances.

Everything here is post hoc. The preregistered result stays experiments/c4_panel_summary.json.
"""
import argparse, collections, json, os, random, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c4_recompute import cell_records, crc_lambda, load, make_splits, pool_files, SEEDS, TAGS


def draw(questions, m, rng):
    """A budget-m pool: m of each question's usable candidates, single partition recounted."""
    out = []
    for q in questions:
        cls = q["single"]
        n = sum(c["count"] for c in cls)
        if n <= m:
            out.append({**q, "single": [dict(c) for c in cls]})
            continue
        pool = [i for i, c in enumerate(cls) for _ in range(c["count"])]
        rng.shuffle(pool)
        cnt = collections.Counter(pool[:m])
        # keep the file's descending-count order, original order among ties
        order = sorted(cnt.items(), key=lambda t: (-t[1], t[0]))
        out.append({**q, "single": [dict(cls[i], count=k) for i, k in order]})
    return out


def resolution(questions):
    """Score resolution of the single-database partition at this budget."""
    tops, sat = [], 0
    for q in questions:
        cls = q["single"]
        n = sum(c["count"] for c in cls)
        if n == 0:
            continue
        top = max(c["count"] for c in cls)
        tops.append(top / n)
        if top == n:
            sat += 1
    return {"distinct_top_masses": len(set(round(t, 6) for t in tops)),
            "unanimous_share": sat / len(tops),
            "flip_rate": None}


def flip_rate(questions):
    """Score-free ceiling: the answer cell A returns is weak-accepted and suite-rejected."""
    n = f = 0
    for q in questions:
        cls = q["single"]
        tot = sum(c["count"] for c in cls)
        if tot == 0:
            continue
        masses = [c["count"] / tot for c in cls]
        best = max(masses)
        top = cls[[i for i, m in enumerate(masses) if m == best][0]]
        n += 1
        f += bool(top["weak_ok"] and not top["strong_ok"])
    return f / n


def gap_of(questions, splits, alpha):
    recs = cell_records(questions, "single", "single")
    vals, ans = [], []
    for calq, tstq in splits:
        if not calq or not tstq:
            continue
        lam = crc_lambda([(recs[i]["top_mass"], not recs[i]["fit_ok"]) for i in calq], alpha)
        a = [i for i in tstq if recs[i]["top_mass"] >= lam]
        n = len(tstq)
        r_fit = sum(1 for i in a if not recs[i]["fit_ok"]) / n
        r_str = sum(1 for i in a if not recs[i]["strong_ok"]) / n
        vals.append(r_str - r_fit); ans.append(len(a) / n)
    return statistics.mean(vals), statistics.mean(ans)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budgets", nargs="*", type=int, default=[10, 20, 30, 50])
    ap.add_argument("--draws", type=int, default=3, help="subsample draws averaged per budget")
    ap.add_argument("--alpha", type=float, default=0.1)
    ap.add_argument("--splits", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260903)
    ap.add_argument("--out", default="experiments/c12_sample_budget.json")
    a = ap.parse_args()

    rows, means = [], {}
    for tag in TAGS:
        for how in ("question", "database"):
            for m in a.budgets:
                per = []
                for seed in SEEDS:
                    qs = load(pool_files(tag, seed, how))
                    ids = [q["qid"] for q in qs]; dbs = {q["qid"]: q["db"] for q in qs}
                    sp = make_splits(ids, dbs, how, a.splits, a.seed)
                    reps = 1 if m >= 50 else a.draws
                    for r in range(reps):
                        rng = random.Random((a.seed, tag, seed, how, m, r).__hash__())
                        pool = qs if m >= 50 else draw(qs, m, rng)
                        g, ar = gap_of(pool, sp, a.alpha)
                        res = resolution(pool)
                        per.append({"gap": g, "answer_rate": ar, "flip_rate": flip_rate(pool),
                                    "distinct_top_masses": res["distinct_top_masses"],
                                    "unanimous_share": res["unanimous_share"],
                                    "tag": tag, "split": how, "budget": m, "seed": seed, "draw": r})
                rows += per
                keys = ("gap", "answer_rate", "flip_rate", "distinct_top_masses", "unanimous_share")
                mm = {k: statistics.mean(p[k] for p in per) for k in keys}
                means[f"{tag}|{how}|{m}"] = mm
                print(f"{tag:>18} {how:<9} m={m:<3} GAP {mm['gap']*100:+6.2f}  flip {mm['flip_rate']*100:5.2f}"
                      f"  answer {mm['answer_rate']*100:5.1f}  distinct-top {mm['distinct_top_masses']:5.1f}"
                      f"  unanimous {mm['unanimous_share']*100:5.1f}%")

    json.dump({"note": "post-hoc budget sensitivity of GAP and of score resolution; D minus A is not "
                       "recomputable from the archived marginals, see the module docstring",
               "options": vars(a), "means": means, "rows": rows}, open(a.out, "w"), indent=1)
    print("\nSaved: " + a.out)


if __name__ == "__main__":
    main()
