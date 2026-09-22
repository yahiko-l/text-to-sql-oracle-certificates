#!/usr/bin/env python3
"""Summarise the instance cross-fit runs (post-hoc).

The preregistered analysis builds the multi-instance equivalence classes and calibrates the
certificate on every suite instance, then evaluates on the same instances. That measures fit to a
finite oracle. The cross-fit runs split each database's suite in half: classes and calibration
labels come from the construction fold plus the original database, correctness is judged on the
held-out fold plus the original. This script collects both fold directions and also reports how
much the held-out oracle disagrees with the full oracle, which bounds how strong a test this is.
"""
import collections, json, os, statistics, sys

TAGS = ("kwai-autosql-32b", "kwai-autosql-14b", "xiyansql-32b", "omnisql-32b")
SEEDS = (101, 202, 303)
GAP = ("oracle_gap_within_cell_A", "marginal_risk_strong_minus_fit", "mean")
REP = ("paired_contrasts_vs_cell_A", "score=multi|calib=multi", "marginal_risk_strong", "mean_change_vs_A")
D_RISK = ("cells", "score=multi|calib=multi", "marginal_risk_strong", "mean")
A_RISK = ("cells", "score=single|calib=single", "marginal_risk_strong", "mean")


def get(d, keys):
    for k in keys:
        d = d[k]
    return d


def label_disagreement(tag, seed, fold):
    """How often the construction oracle and the evaluation oracle disagree about a class.

    Read directly from the cross-fit run's own per-question file, comparing `constr_ok` (labels the
    construction instances give, which is what calibrates the threshold) with `strong_ok` (labels
    the held-out instances give, which is what scores the test set). An earlier version compared the
    held-out labels with the FULL-oracle labels instead; the full oracle contains the held-out half,
    so that systematically understated the disagreement.
    """
    p = f"experiments/c4_{tag}_seed{seed}_results_crossfit2_f{fold}_per_question.json"
    if not os.path.isfile(p):
        return None
    n_s = d_s = n_m = d_m = n_top = d_top = 0
    for q in json.load(open(p))["questions"]:
        for c in q["single"]:
            n_s += 1; d_s += int(c["constr_ok"] != c["strong_ok"])
        for c in q["multi"]:
            n_m += 1; d_m += int(c["constr_ok"] != c["strong_ok"])
        if q["multi"]:
            top = max(q["multi"], key=lambda c: (c["count"], c["representative"]))
            n_top += 1; d_top += int(top["constr_ok"] != top["strong_ok"])
    r = lambda a, b: round(a / b, 4) if b else None
    return {"single_classes": n_s, "single_disagreements": d_s, "single_rate": r(d_s, n_s),
            "multi_classes": n_m, "multi_disagreements": d_m, "multi_rate": r(d_m, n_m),
            "top_multi_class_rate": r(d_top, n_top)}


def main():
    out = {"note": "post-hoc instance cross-fit: classes and calibration from one half of each "
                   "database's suite plus the original database, correctness judged on the other "
                   "half plus the original. Preregistered analysis used every instance for both.",
           "models": {}}
    for tag in TAGS:
        rows, miss = [], []
        for seed in SEEDS:
            for fold in (0, 1):
                p = f"experiments/c4_{tag}_seed{seed}_results_crossfit2_f{fold}.json"
                if not os.path.isfile(p):
                    miss.append(p); continue
                r = json.load(open(p))
                base = json.load(open(f"experiments/c4_{tag}_seed{seed}_results_official.json"))
                rows.append({"seed": seed, "construction_fold": fold,
                             "GAP": get(r, GAP), "GAP_full_oracle": get(base, GAP),
                             "REPAIR": get(r, REP), "REPAIR_full_oracle": get(base, REP),
                             "A_risk_strong": get(r, A_RISK), "D_risk_strong": get(r, D_RISK),
                             "top1_strong": r["top1_accuracy_under_strong_oracle"],
                             "top1_strong_full_oracle": base["top1_accuracy_under_strong_oracle"],
                             "label_disagreement": label_disagreement(tag, seed, fold)})
        if not rows:
            out["models"][tag] = {"missing": miss}; continue
        m = lambda k: round(statistics.mean(r[k] for r in rows), 4)
        out["models"][tag] = {
            "runs": rows, "missing": miss,
            "GAP_crossfit_mean": m("GAP"), "GAP_full_oracle_mean": m("GAP_full_oracle"),
            "REPAIR_crossfit_mean": m("REPAIR"), "REPAIR_full_oracle_mean": m("REPAIR_full_oracle"),
            "A_risk_strong_mean": m("A_risk_strong"), "D_risk_strong_mean": m("D_risk_strong"),
            "GAP_positive_every_run": all(r["GAP"] > 0 for r in rows),
            "REPAIR_negative_every_run": all(r["REPAIR"] < 0 for r in rows),
            "max_single_class_disagreement": max((r["label_disagreement"]["single_rate"] for r in rows
                                                 if r["label_disagreement"]), default=None),
            "max_multi_class_disagreement": max((r["label_disagreement"]["multi_rate"] for r in rows
                                                if r["label_disagreement"]), default=None),
            "max_top_multi_class_disagreement": max((r["label_disagreement"]["top_multi_class_rate"] for r in rows
                                                    if r["label_disagreement"]), default=None)}
        o = out["models"][tag]
        print(f"{tag:>18}  GAP crossfit {o['GAP_crossfit_mean']:+.4f} (full oracle {o['GAP_full_oracle_mean']:+.4f})  "
              f"REPAIR {o['REPAIR_crossfit_mean']:+.4f} ({o['REPAIR_full_oracle_mean']:+.4f})  "
              f"A risk {o['A_risk_strong_mean']:.4f} -> D {o['D_risk_strong_mean']:.4f}  "
              f"construction-vs-evaluation disagreement: single {o['max_single_class_disagreement']} "
              f"multi {o['max_multi_class_disagreement']} top-multi {o['max_top_multi_class_disagreement']}")
    json.dump(out, open("experiments/c4_crossfit_summary.json", "w"), indent=1, ensure_ascii=False)
    print("wrote experiments/c4_crossfit_summary.json")


if __name__ == "__main__":
    main()
