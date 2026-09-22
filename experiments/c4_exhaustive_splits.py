#!/usr/bin/env python3
"""Every schema-disjoint database split, exactly, instead of 200 random draws.

The preregistered database-grouped analysis draws 200 random 9/10 splits of the 19 schemas. That
leaves a Monte Carlo error on top of the quantity of interest. There are only C(19,9) = 92,378
such splits, so the whole distribution can be enumerated and the split noise removed. This does
NOT add independent schemas: the spread below is the spread over ways of cutting the same 19
schemas, not a confidence statement about new ones.

The certificate is recomputed from the per-question sufficient statistics with the same rules as
the analyser: CRC on the top-class mass with the cell's own calibration labels, evaluated on the
held-out schemas under the multi-instance oracle. Vectorised over the grid so all 92,378 splits
per pool are affordable.
"""
import argparse, collections, itertools, json, statistics
import numpy as np

TAGS = ("kwai-autosql-32b", "kwai-autosql-14b", "xiyansql-32b", "omnisql-32b")
SEEDS = (101, 202, 303)
NG = 201                                   # grid 0.000, 0.005, ..., 1.000, ascending


def cell_arrays(questions, scoring, cal_label, tie="first"):
    """Per question: grid index of its top-class mass, and whether that class is wrong under the
    fitting oracle and under the evaluation oracle.

    The analyser breaks a tie between equally massive classes by the larger internal class key,
    which the per-question file does not carry. `tie` therefore exposes the choice: 'first' and
    'last' take the earliest and the latest of the tied classes as the file lists them (classes are
    written in descending count, ties by ascending string of the key), and 'last' is the closer
    proxy for the analyser's rule. Ties are rare; both are reported rather than one being presented
    as the analyser's own.
    """
    db, k, wrong_fit, wrong_strong = [], [], [], []
    ok_key = "weak_ok" if cal_label == "single" else "constr_ok"
    for q in questions:
        cls = q[scoring]
        n = sum(c["count"] for c in cls)
        if n == 0:
            continue
        masses = [c["count"] / n for c in cls]
        best = max(masses)
        tied = [i for i, m in enumerate(masses) if m == best]
        i = tied[0] if tie == "first" else tied[-1]
        top = cls[i]
        db.append(q["db"])
        k.append(min(int(best * (NG - 1) + 1e-9), NG - 1))
        wrong_fit.append(not top.get(ok_key, top["strong_ok"]))
        wrong_strong.append(not top["strong_ok"])
    return db, np.array(k), np.array(wrong_fit), np.array(wrong_strong)


def per_db_tables(db, k, wrong_fit, wrong_strong, dbs):
    """Suffix counts per database: rows are databases, columns are grid indices.
    tot[d, g] = number of questions of d whose top class is answered at grid index g."""
    D, G = len(dbs), NG
    tot = np.zeros((D, G)); wf = np.zeros((D, G)); ws = np.zeros((D, G))
    di = {d: i for i, d in enumerate(dbs)}
    for j, d in enumerate(db):
        r = di[d]
        tot[r, : k[j] + 1] += 1                      # answered for every grid index <= k
        if wrong_fit[j]:
            wf[r, : k[j] + 1] += 1
        if wrong_strong[j]:
            ws[r, : k[j] + 1] += 1
    n = np.array([sum(1 for d in db if d == x) for x in dbs], dtype=float)
    return tot, wf, ws, n


def run_cell(questions, scoring, cal, alpha, combos, dbs, tie="first"):
    db, k, wf_flag, ws_flag = cell_arrays(questions, scoring, cal, tie)
    tot, wf, ws, n = per_db_tables(db, k, wf_flag, ws_flag, dbs)
    idx = np.arange(len(dbs))
    risk_strong = np.empty(len(combos)); risk_fit = np.empty(len(combos)); ans = np.empty(len(combos))
    for c, combo in enumerate(combos):
        cal_rows = np.array(combo)
        tst_rows = np.setdiff1d(idx, cal_rows, assume_unique=True)
        ncal = n[cal_rows].sum(); ntst = n[tst_rows].sum()
        wf_cal = wf[cal_rows].sum(axis=0)
        # CRC: smallest grid index whose calibration risk bound is within alpha
        bound = (ncal / (ncal + 1)) * (wf_cal / ncal) + 1 / (ncal + 1)
        feasible = np.flatnonzero(bound <= alpha)
        g = feasible[0] if feasible.size else NG          # NG means abstain on everything
        if g >= NG:
            risk_strong[c] = risk_fit[c] = ans[c] = 0.0
            continue
        risk_strong[c] = ws[tst_rows].sum(axis=0)[g] / ntst
        risk_fit[c] = wf[tst_rows].sum(axis=0)[g] / ntst
        ans[c] = tot[tst_rows].sum(axis=0)[g] / ntst
    return {"risk_strong": risk_strong, "risk_fit": risk_fit, "answer_rate": ans}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tags", nargs="*", default=list(TAGS))
    ap.add_argument("--alpha", type=float, default=0.1)
    ap.add_argument("--tie-break", choices=("first", "last", "both"), default="both",
                    help="'both' runs the enumeration under each tie convention and reports both")
    ap.add_argument("--out", default="experiments/c4_exhaustive_db_splits.json")
    a = ap.parse_args()

    out = {"note": "every schema-disjoint 9/10 split of the 19 databases, enumerated; the spread is "
                   "over ways of cutting these 19 schemas and is not a confidence statement",
           "alpha": a.alpha, "tie_conventions": ["first", "last"] if a.tie_break == "both" else [a.tie_break],
           "models": {}}
    for tie in out["tie_conventions"]:
      for tag in a.tags:
        per_seed = {}
        for s in SEEDS:
            qs = json.load(open(f"experiments/c4_{tag}_seed{s}_results_official_dbsplit_per_question.json"))["questions"]
            dbs = sorted({q["db"] for q in qs})
            combos = list(itertools.combinations(range(len(dbs)), len(dbs) // 2))
            A = run_cell(qs, "single", "single", a.alpha, combos, dbs, tie)
            D = run_cell(qs, "multi", "multi", a.alpha, combos, dbs, tie)
            gap = A["risk_strong"] - A["risk_fit"]
            rep = D["risk_strong"] - A["risk_strong"]
            q = lambda v, p: float(np.quantile(v, p))
            per_seed[str(s)] = {
                "n_splits": len(combos),
                "GAP_mean": round(float(gap.mean()), 4), "GAP_p2.5": round(q(gap, 0.025), 4),
                "GAP_p97.5": round(q(gap, 0.975), 4),
                "GAP_positive_fraction": round(float((gap > 0).mean()), 4),
                "REPAIR_mean": round(float(rep.mean()), 4), "REPAIR_p2.5": round(q(rep, 0.025), 4),
                "REPAIR_p97.5": round(q(rep, 0.975), 4),
                "REPAIR_negative_fraction": round(float((rep < 0).mean()), 4),
                "A_risk_strong_mean": round(float(A["risk_strong"].mean()), 4),
                "D_risk_strong_mean": round(float(D["risk_strong"].mean()), 4),
                "A_answer_rate_mean": round(float(A["answer_rate"].mean()), 4),
                "D_answer_rate_mean": round(float(D["answer_rate"].mean()), 4)}
            r = per_seed[str(s)]
            print(f"{tag:>18} s{s} tie={tie:<5}: {r['n_splits']} splits  GAP {r['GAP_mean']:+.4f} "
                  f"[{r['GAP_p2.5']:+.4f},{r['GAP_p97.5']:+.4f}] positive {r['GAP_positive_fraction']:.4f}  "
                  f"REPAIR {r['REPAIR_mean']:+.4f} [{r['REPAIR_p2.5']:+.4f},{r['REPAIR_p97.5']:+.4f}] "
                  f"negative {r['REPAIR_negative_fraction']:.4f}")
        m = lambda key: round(statistics.mean(per_seed[str(s)][key] for s in SEEDS), 4)
        out["models"][f"{tag}|tie={tie}"] = {
            "per_seed": per_seed, "GAP_mean": m("GAP_mean"), "REPAIR_mean": m("REPAIR_mean"),
            "GAP_positive_fraction_mean": m("GAP_positive_fraction"),
            "REPAIR_negative_fraction_mean": m("REPAIR_negative_fraction"),
            "GAP_positive_fraction_range": [min(per_seed[str(s)]["GAP_positive_fraction"] for s in SEEDS),
                                            max(per_seed[str(s)]["GAP_positive_fraction"] for s in SEEDS)],
            "REPAIR_negative_fraction_range": [min(per_seed[str(s)]["REPAIR_negative_fraction"] for s in SEEDS),
                                               max(per_seed[str(s)]["REPAIR_negative_fraction"] for s in SEEDS)]}
    json.dump(out, open(a.out, "w"), indent=1, ensure_ascii=False)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
