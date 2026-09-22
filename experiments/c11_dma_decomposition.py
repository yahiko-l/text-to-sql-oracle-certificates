#!/usr/bin/env python3
"""Decompose the D minus A contrast into the events that can carry it.

Both cells are scored against the same oracle, so a test question contributes to D minus A only
through the answers the two cells actually return. Four disjoint events exhaust the test half:

  both answer, same SQL      the two cells return one query, judged once, contribution exactly 0
  both answer, changed SQL   the partition changed the returned query
  only D answers             the suite-partition cell answers where current practice abstains
  only A answers             current practice answers where the suite-partition cell abstains
  neither answers            contribution 0

The three non-zero terms sum to D minus A by construction, which is the check this script asserts
on every split. Section 6.3 reports that 97.1 percent of returned SQL is unchanged; that share is a
property of the pools, not of the contrast, and this script measures how much of the contrast the
unchanged answers can carry, which is none, and where the rest comes from.

Everything here is post hoc. The preregistered result stays experiments/c4_panel_summary.json.
"""
import argparse, collections, json, os, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c4_recompute import cell_records, crc_lambda, load, make_splits, pool_files, SEEDS, TAGS

CELLS = {"A": "single", "D": "multi"}
EVENTS = ("both_same_sql", "both_changed_sql", "only_d", "only_a")


def top_reps(questions, scoring):
    """Representative SQL of the class each cell answers with, under the file-order tie rule."""
    out = {}
    for q in questions:
        cls = q[scoring]
        n = sum(c["count"] for c in cls)
        if n == 0:
            continue
        masses = [c["count"] / n for c in cls]
        best = max(masses)
        out[q["qid"]] = cls[[i for i, m in enumerate(masses) if m == best][0]]["representative"]
    return out


def decompose(questions, splits, alpha):
    recs = {k: cell_records(questions, s, s) for k, s in CELLS.items()}
    reps = {k: top_reps(questions, s) for k, s in CELLS.items()}
    acc = collections.defaultdict(list)
    for calq, tstq in splits:
        if not calq or not tstq:
            continue
        lam = {k: crc_lambda([(recs[k][i]["top_mass"], not recs[k][i]["fit_ok"]) for i in calq], alpha)
               for k in CELLS}
        n = len(tstq)
        contrib = dict.fromkeys(EVENTS, 0.0)
        share = dict.fromkeys(EVENTS + ("neither",), 0)
        for i in tstq:
            a_ans = recs["A"][i]["top_mass"] >= lam["A"]
            d_ans = recs["D"][i]["top_mass"] >= lam["D"]
            a_wrong = a_ans and not recs["A"][i]["strong_ok"]
            d_wrong = d_ans and not recs["D"][i]["strong_ok"]
            if a_ans and d_ans:
                ev = "both_same_sql" if reps["A"][i] == reps["D"][i] else "both_changed_sql"
            elif d_ans:
                ev = "only_d"
            elif a_ans:
                ev = "only_a"
            else:
                share["neither"] += 1
                continue
            share[ev] += 1
            contrib[ev] += float(d_wrong) - float(a_wrong)
        risk_a = sum(1 for i in tstq if recs["A"][i]["top_mass"] >= lam["A"]
                     and not recs["A"][i]["strong_ok"]) / n
        risk_d = sum(1 for i in tstq if recs["D"][i]["top_mass"] >= lam["D"]
                     and not recs["D"][i]["strong_ok"]) / n
        total = sum(contrib.values()) / n
        assert abs(total - (risk_d - risk_a)) < 1e-12, "decomposition does not sum to D minus A"
        assert contrib["both_same_sql"] == 0.0, "an unchanged answer moved the contrast"
        for k, v in contrib.items():
            acc["contrib_" + k].append(v / n)
        for k, v in share.items():
            acc["share_" + k].append(v / n)
        acc["dma"].append(risk_d - risk_a)
    return {k: statistics.mean(v) for k, v in acc.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--alpha", type=float, default=0.1)
    ap.add_argument("--splits", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260903)
    ap.add_argument("--out", default="experiments/c11_dma_decomposition.json")
    a = ap.parse_args()

    per_seed, means = [], {}
    for tag in TAGS:
        for how in ("question", "database"):
            rows = []
            for seed in SEEDS:
                qs = load(pool_files(tag, seed, how))
                ids = [q["qid"] for q in qs]
                dbs = {q["qid"]: q["db"] for q in qs}
                r = decompose(qs, make_splits(ids, dbs, how, a.splits, a.seed), a.alpha)
                r.update({"tag": tag, "split": how, "seed": seed})
                rows.append(r); per_seed.append(r)
            keys = [k for k in rows[0] if k not in ("tag", "split", "seed")]
            m = {k: statistics.mean(r[k] for r in rows) for k in keys}
            means[f"{tag}|{how}"] = m
            print(f"{tag:>18} {how:<9} D-A {m['dma']*100:+6.2f}  =  changed-SQL {m['contrib_both_changed_sql']*100:+6.2f}"
                  f"  only-D {m['contrib_only_d']*100:+6.2f}  only-A {m['contrib_only_a']*100:+6.2f}"
                  f"   [same-SQL answers {m['share_both_same_sql']*100:5.1f}% of questions, carry 0.00]")

    json.dump({"note": "post-hoc decomposition of D minus A; preregistered result is "
                       "experiments/c4_panel_summary.json",
               "options": vars(a), "three_seed_means": means, "per_seed": per_seed},
              open(a.out, "w"), indent=1)
    print("\nSaved: " + a.out)


if __name__ == "__main__":
    main()
