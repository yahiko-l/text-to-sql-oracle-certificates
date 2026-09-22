#!/usr/bin/env python3
"""Aggregate the preregistration-2 model panel and apply the frozen rules (PREREGISTRATION_2.md §6, §7).

Reads, per model, the three seed pools' analyser outputs (official comparator, question
splits, usable denominator = primary; database-grouped splits, budget denominator and the
custom comparator = declared secondary analyses) and the false-schema control, computes the
per-model verdicts and the family-level outcome, and writes a JSON summary plus a Markdown
table. Every rule is a computation on named result keys; nothing here is a judgement.
"""
import argparse, json, os

GAP_KEY = ("oracle_gap_within_cell_A", "marginal_risk_strong_minus_fit", "mean")
REP_KEY = ("paired_contrasts_vs_cell_A", "score=multi|calib=multi", "marginal_risk_strong", "mean_change_vs_A")
ANS_KEY = ("paired_contrasts_vs_cell_A", "score=multi|calib=multi", "answer_rate", "mean_change_vs_A")
SEL_KEY = ("paired_contrasts_vs_cell_A", "score=multi|calib=multi", "selective_risk_strong", "mean_change_vs_A")
A_RISK_FIT = ("cells", "score=single|calib=single", "marginal_risk_fit", "mean")
A_RISK_STRONG = ("cells", "score=single|calib=single", "marginal_risk_strong", "mean")
D_RISK_STRONG = ("cells", "score=multi|calib=multi", "marginal_risk_strong", "mean")
A_ANS = ("cells", "score=single|calib=single", "answer_rate", "mean")

RULE = {"gap_each_seed_gt": 0.0, "gap_mean_min": 0.010, "repair_mean_max": -0.030,
        "repair_robust_each_seed_max": -0.030, "narrow_margin": 0.005,
        "control_top1_max": 0.10, "control_risk_slack": 0.02}


def get(d, keys):
    for k in keys:
        d = d[k]
    return d


def load(path):
    return json.load(open(path)) if os.path.isfile(path) else None


def per_model(tag, seed_files, control_file, alpha=0.1):
    seeds = []
    for label, stem in seed_files:
        main = load(stem + "_official.json")
        if main is None:
            seeds.append({"seed": label, "missing": stem + "_official.json"}); continue
        row = {"seed": label, "top1_strong": main["top1_accuracy_under_strong_oracle"],
               "questions_usable": main["questions_usable"],
               "A_risk_fit": get(main, A_RISK_FIT), "A_risk_strong": get(main, A_RISK_STRONG),
               "D_risk_strong": get(main, D_RISK_STRONG), "A_answer_rate": get(main, A_ANS),
               "gap": get(main, GAP_KEY), "repair": get(main, REP_KEY),
               "answer_rate_cost": get(main, ANS_KEY), "selective_risk_change": get(main, SEL_KEY),
               "gap_same_sign": main["oracle_gap_within_cell_A"]["marginal_risk_strong_minus_fit"]["splits_with_same_sign"],
               "repair_same_sign": main["paired_contrasts_vs_cell_A"]["score=multi|calib=multi"]["marginal_risk_strong"]["splits_with_same_sign"],
               "parse_rate": (main.get("provenance") or {}).get("candidates_meta", {}).get("instrument_checks", {}).get("parse_rate"),
               "truncation_rate": (main.get("provenance") or {}).get("candidates_meta", {}).get("instrument_checks", {}).get("truncation_rate")}
        for suffix, name in (("_official_dbsplit.json", "dbsplit"), ("_official_budget.json", "budget"),
                             ("_custom.json", "custom")):
            v = load(stem + suffix)
            if v is None and name == "custom":
                legacy = load(stem + ".json")      # the original C2 pool's custom result keeps its legacy name
                v = legacy if legacy and legacy.get("comparator") == "custom" else None
            if v is not None:
                row[f"gap_{name}"] = get(v, GAP_KEY)
                row[f"repair_{name}"] = get(v, REP_KEY)
        if "gap_dbsplit" in row:
            row["dbsplit_consistent"] = ((row["gap_dbsplit"] > 0) == (row["gap"] > 0)
                                         and (row["repair_dbsplit"] < 0) == (row["repair"] < 0))
        seeds.append(row)
    ok = [s for s in seeds if "missing" not in s]
    out = {"tag": tag, "seeds": seeds, "n_seeds": len(ok)}
    if ok:
        gaps = [s["gap"] for s in ok]; reps = [s["repair"] for s in ok]
        out["gap_mean"] = round(sum(gaps) / len(gaps), 4)
        out["repair_mean"] = round(sum(reps) / len(reps), 4)
        out["answer_rate_cost_mean"] = round(sum(s["answer_rate_cost"] for s in ok) / len(ok), 4)
        out["gap_positive"] = all(g > RULE["gap_each_seed_gt"] for g in gaps) and out["gap_mean"] >= RULE["gap_mean_min"]
        out["repair_pass"] = out["repair_mean"] <= RULE["repair_mean_max"] and all(r < 0 for r in reps)
        out["repair_robust"] = out["repair_pass"] and all(r <= RULE["repair_robust_each_seed_max"] for r in reps)
        out["repair_narrow"] = out["repair_pass"] and (abs(out["repair_mean"]) - abs(RULE["repair_mean_max"])) < RULE["narrow_margin"]
        if all("dbsplit_consistent" in s for s in ok):
            out["dbsplit_consistent_all_seeds"] = all(s["dbsplit_consistent"] for s in ok)
    ctl = load(control_file) if control_file else None
    if ctl is not None:
        out["control"] = {"file": control_file, "top1_strong": ctl["top1_accuracy_under_strong_oracle"],
                          "A_risk_strong": get(ctl, A_RISK_STRONG), "A_answer_rate": get(ctl, A_ANS)}
        out["control_ok"] = (ctl["top1_accuracy_under_strong_oracle"] <= RULE["control_top1_max"]
                             and get(ctl, A_RISK_STRONG) <= alpha + RULE["control_risk_slack"])
        out["instrument_suspect"] = ctl["top1_accuracy_under_strong_oracle"] > RULE["control_top1_max"]
    else:
        out["control"] = None
        out["control_ok"] = None
        out["instrument_suspect"] = None
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", default="experiments/panel_entry.json")
    ap.add_argument("--tags", nargs="*", default=None, help="override the panel tags")
    ap.add_argument("--out", default="experiments/c3_panel_summary.json")
    a = ap.parse_args()

    tags = a.tags
    if tags is None:
        tags = json.load(open(a.panel))["panel"] if os.path.isfile(a.panel) else []
    models = {}
    models["xiyansql-32b"] = per_model(
        "xiyansql-32b",
        [("20260903", "experiments/c2_results"), ("11", "experiments/c2_genseed11_results"),
         ("22", "experiments/c2_genseed22_results"), ("33", "experiments/c2_genseed33_results")],
        "experiments/c3_xiyansql-32b_falseschema_results_official.json")
    for t in tags:
        models[t] = per_model(t, [(str(s), f"experiments/c3_{t}_seed{s}_results") for s in (101, 202, 303)],
                              f"experiments/c3_{t}_falseschema_results_official.json")

    counted = {t: m for t, m in models.items() if m.get("n_seeds") and not m.get("instrument_suspect")}
    n_gap = sum(1 for m in counted.values() if m.get("gap_positive"))
    n_pass = sum(1 for m in counted.values() if m.get("repair_pass"))
    n_robust = sum(1 for m in counted.values() if m.get("repair_robust"))
    new_families = [t for t in counted if t != "xiyansql-32b"]
    if not tags:
        outcome = "O5"
    elif n_gap >= 2 and n_pass >= 2 and n_robust >= 1:
        outcome = "O1"
    elif n_gap >= 2:
        outcome = "O2"
    elif any(counted[t].get("gap_positive") for t in new_families):
        outcome = "O2-partial"  # gap positive in a new family but XiYanSQL not counted; should not happen
    elif models["xiyansql-32b"].get("gap_positive") and not any(counted[t].get("gap_positive") for t in new_families):
        outcome = "O4" if new_families else "O3"
    else:
        outcome = "O3"
    summary = {"rule": RULE, "panel": tags, "models": models,
               "counts": {"families_counted": list(counted), "gap_positive": n_gap, "repair_pass": n_pass,
                          "repair_robust": n_robust},
               "outcome": outcome}
    json.dump(summary, open(a.out, "w"), indent=1, ensure_ascii=False)

    print("| model | seed | top1 | A risk fit | A risk strong | GAP | D risk strong | REPAIR | ans cost | GAP dbsplit | REPAIR dbsplit | REPAIR budget | REPAIR custom |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for t, m in models.items():
        for s in m["seeds"]:
            if "missing" in s:
                print(f"| {t} | {s['seed']} | missing: {s['missing']} |"); continue
            print(f"| {t} | {s['seed']} | {s['top1_strong']} | {s['A_risk_fit']} | {s['A_risk_strong']} | {s['gap']} | "
                  f"{s['D_risk_strong']} | {s['repair']} | {s['answer_rate_cost']} | {s.get('gap_dbsplit')} | "
                  f"{s.get('repair_dbsplit')} | {s.get('repair_budget')} | {s.get('repair_custom')} |")
    print()
    for t, m in models.items():
        if not m.get("n_seeds"):
            print(f"{t}: no results"); continue
        print(f"{t}: GAP mean {m['gap_mean']} positive={m['gap_positive']} | REPAIR mean {m['repair_mean']} "
              f"pass={m['repair_pass']} robust={m['repair_robust']} narrow={m['repair_narrow']} | "
              f"answer-rate cost {m['answer_rate_cost_mean']} | dbsplit consistent={m.get('dbsplit_consistent_all_seeds')} | "
              f"control ok={m['control_ok']} suspect={m['instrument_suspect']} {m['control']}")
    print("outcome:", outcome, summary["counts"])


if __name__ == "__main__":
    main()
