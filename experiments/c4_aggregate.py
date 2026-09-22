#!/usr/bin/env python3
"""Aggregate the Preregistration 3 panel and apply its frozen rules (PREREGISTRATION_3.md §6, §7).

Reads, per model, the three seed pools' analyser outputs under the two co-primary analyses
(official comparator with question-level half-splits and with database-grouped half-splits, both
on the usable denominator), the declared secondary analyses (budget denominator, custom
comparator) and the false-schema control; computes the per-model, per-family and panel-level
verdicts and writes a JSON summary plus a Markdown table. Every rule is a computation on named
result keys; nothing here is a judgement.

Families are base-checkpoint lineages. A family's verdict is that of its highest-ranked entering
member (the order below); further members are within-family replications and are reported, not
counted. Model tags and the family map are frozen here.
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

RULE = {"gap_each_seed_gt": 0.0, "gap_mean_min": 0.010,
        "repair_each_seed_lt": 0.0, "repair_mean_max": -0.030, "repair_robust_each_seed_max": -0.030,
        "narrow_margin": 0.005, "control_top1_max": 0.10, "control_risk_slack": 0.02}
SEEDS = (101, 202, 303)
SPLITS = (("question", "_official.json"), ("database", "_official_dbsplit.json"))
SECONDARY = (("budget", "_official_budget.json"), ("custom", "_custom.json"))

# base-checkpoint lineage of every candidate, and the vendor of that lineage
FAMILY = {"kwai-autosql-32b": "qwen3", "kwai-autosql-14b": "qwen3",
          "xiyansql-32b": "qwen25coder", "omnisql-32b": "qwen25coder",
          "sqlcoder-70b": "codellama", "llama3-sqlcoder-8b": "llama3"}
VENDOR = {"qwen3": "qwen", "qwen25coder": "qwen", "codellama": "meta", "llama3": "meta"}
# within-family order (the SQL-model ranking as it stood at freeze time); decides the representative
RANK = ["kwai-autosql-32b", "kwai-autosql-14b", "xiyansql-32b", "omnisql-32b", "sqlcoder-70b", "llama3-sqlcoder-8b"]
ORIGINAL = "xiyansql-32b"       # the family whose earlier pools produced the finding under test


def get(d, keys):
    for k in keys:
        d = d[k]
    return d


def load(path):
    return json.load(open(path)) if os.path.isfile(path) else None


def split_verdict(gaps, reps):
    mean_gap = sum(gaps) / len(gaps)
    mean_rep = sum(reps) / len(reps)
    v = {"gap_mean": round(mean_gap, 4), "repair_mean": round(mean_rep, 4),
         "gap_positive": all(g > RULE["gap_each_seed_gt"] for g in gaps) and mean_gap >= RULE["gap_mean_min"],
         "repair_pass": mean_rep <= RULE["repair_mean_max"] and all(r < RULE["repair_each_seed_lt"] for r in reps)}
    v["repair_robust"] = v["repair_pass"] and all(r <= RULE["repair_robust_each_seed_max"] for r in reps)
    v["repair_narrow"] = v["repair_pass"] and (abs(mean_rep) - abs(RULE["repair_mean_max"])) < RULE["narrow_margin"]
    return v


def per_model(tag, stems, control_file, alpha=0.1):
    """stems: list of (seed label, path stem) so that stem + suffix names each analysis file."""
    seeds = []
    for label, stem in stems:
        row = {"seed": label}
        for split, suffix in SPLITS:
            r = load(stem + suffix)
            if r is None:
                row[f"missing_{split}"] = stem + suffix
                continue
            row[split] = {"top1_strong": r["top1_accuracy_under_strong_oracle"],
                          "questions_usable": r["questions_usable"],
                          "A_risk_fit": get(r, A_RISK_FIT), "A_risk_strong": get(r, A_RISK_STRONG),
                          "D_risk_strong": get(r, D_RISK_STRONG), "A_answer_rate": get(r, A_ANS),
                          "gap": get(r, GAP_KEY), "repair": get(r, REP_KEY),
                          "answer_rate_change": get(r, ANS_KEY), "selective_risk_change": get(r, SEL_KEY),
                          "gap_same_sign": r["oracle_gap_within_cell_A"]["marginal_risk_strong_minus_fit"]["splits_with_same_sign"],
                          "repair_same_sign": r["paired_contrasts_vs_cell_A"]["score=multi|calib=multi"]["marginal_risk_strong"]["splits_with_same_sign"]}
            if split == "question":
                ic = (r.get("provenance") or {}).get("candidates_meta", {}).get("instrument_checks", {})
                row["parse_rate"] = ic.get("parse_rate")
                row["truncation_rate"] = ic.get("truncation_rate")
        for name, suffix in SECONDARY:
            r = load(stem + suffix)
            if r is not None:
                row[name] = {"gap": get(r, GAP_KEY), "repair": get(r, REP_KEY)}
        seeds.append(row)
    ok = [s for s in seeds if all(sp in s for sp, _ in SPLITS)]
    out = {"tag": tag, "family": FAMILY.get(tag), "seeds": seeds, "n_seeds_complete": len(ok)}
    if ok:
        for split, _ in SPLITS:
            out[split] = split_verdict([s[split]["gap"] for s in ok], [s[split]["repair"] for s in ok])
            out[split]["answer_rate_change_mean"] = round(sum(s[split]["answer_rate_change"] for s in ok) / len(ok), 4)
        q, d = out["question"], out["database"]
        out["gap_positive"] = q["gap_positive"] and d["gap_positive"]
        out["repair_pass"] = q["repair_pass"] and d["repair_pass"]
        out["repair_robust"] = q["repair_robust"] and d["repair_robust"]
        out["repair_narrow"] = out["repair_pass"] and (q["repair_narrow"] or d["repair_narrow"])
        out["repair_pass_question_only"] = q["repair_pass"] and not d["repair_pass"]
        out["gap_positive_question_only"] = q["gap_positive"] and not d["gap_positive"]
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
        out["instrument_suspect"] = None    # no control yet: the model is not counted until it has one
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", default="experiments/panel_entry_3.json")
    ap.add_argument("--tags", nargs="*", default=None, help="override the panel tags")
    ap.add_argument("--out", default="experiments/c4_panel_summary.json")
    a = ap.parse_args()

    tags = a.tags
    if tags is None:
        tags = json.load(open(a.panel))["panel"] if os.path.isfile(a.panel) else []
    unknown = [t for t in tags if t not in FAMILY]
    if unknown:
        raise SystemExit(f"tags without a frozen family: {unknown}")

    models = {}
    for t in tags:
        models[t] = per_model(t, [(str(s), f"experiments/c4_{t}_seed{s}_results") for s in SEEDS],
                              f"experiments/c4_{t}_falseschema_results_official.json")
    # the earlier, non-blind XiYanSQL pools, reported for reference and never counted
    prior = per_model("xiyansql-32b (prior pools, Preregistration 1 and 2)",
                      [("20260903", "experiments/c2_results"), ("11", "experiments/c2_genseed11_results"),
                       ("22", "experiments/c2_genseed22_results"), ("33", "experiments/c2_genseed33_results")],
                      "experiments/c3_xiyansql-32b_falseschema_results_official.json")

    # family verdicts: the highest-ranked entering member with complete results and a passing
    # instrument represents its family; instrument-suspect members and members without a
    # control are reported but never counted
    complete = {t: m for t, m in models.items() if m.get("n_seeds_complete") == len(SEEDS)}
    countable = {t: m for t, m in complete.items() if m.get("instrument_suspect") is False}
    families = {}
    for t in RANK:
        if t in countable and FAMILY[t] not in families:
            families[FAMILY[t]] = {"representative": t, "vendor": VENDOR[FAMILY[t]],
                                   "gap_positive": countable[t]["gap_positive"],
                                   "repair_pass": countable[t]["repair_pass"],
                                   "repair_robust": countable[t]["repair_robust"],
                                   "repair_pass_question_only": countable[t]["repair_pass_question_only"],
                                   "members_entering": [u for u in RANK if u in models and FAMILY[u] == FAMILY[t]],
                                   "all_members_gap_positive": all(countable.get(u, {}).get("gap_positive") is True
                                                                   for u in models if FAMILY[u] == FAMILY[t])}
    orig_fam = FAMILY[ORIGINAL]
    new_fams = {f: v for f, v in families.items() if f != orig_fam}
    n_gap = sum(1 for v in families.values() if v["gap_positive"])
    n_pass = sum(1 for v in families.values() if v["repair_pass"])
    n_robust = sum(1 for v in families.values() if v["repair_robust"])
    new_entered = [t for t in models if FAMILY[t] != orig_fam]
    orig_ok = families.get(orig_fam, {}).get("gap_positive")

    if ORIGINAL in complete and families.get(orig_fam, {}).get("representative") == ORIGINAL and orig_ok is False:
        outcome = "O6"      # the original family did not reproduce on fresh seeds
    elif not new_entered:
        outcome = "O5"      # no new family entered the panel
    elif not all(t in complete for t in models):
        outcome = "INCOMPLETE"
    elif n_gap >= 2 and n_pass >= 2 and n_robust >= 1:
        outcome = "O1"
    elif n_gap >= 2:
        outcome = "O2"
    elif new_fams and not any(v["gap_positive"] for v in new_fams.values()):
        outcome = "O4"      # new families entered and none is GAP-positive
    else:
        outcome = "O4"      # new members entered but none is countable (instrument suspect); reported, no family counted
    cross_vendor = any(v["gap_positive"] and v["vendor"] != VENDOR[orig_fam] for v in new_fams.values())
    summary = {"rule": RULE, "seeds": SEEDS, "panel": tags, "family_map": {t: FAMILY[t] for t in tags},
               "models": models, "prior_xiyansql": prior, "families": families,
               "counts": {"families_counted": list(families), "gap_positive": n_gap, "repair_pass": n_pass,
                          "repair_robust": n_robust,
                          "gap_positive_question_only_models": [t for t, m in complete.items() if m.get("gap_positive_question_only")],
                          "repair_pass_question_only_models": [t for t, m in complete.items() if m.get("repair_pass_question_only")],
                          "cross_vendor_gap_positive": cross_vendor},
               "outcome": outcome}
    json.dump(summary, open(a.out, "w"), indent=1, ensure_ascii=False)

    print("| model | seed | split | top1 | A risk fit | A risk strong | GAP | D risk strong | REPAIR | ans change | GAP budget | REPAIR budget | GAP custom | REPAIR custom |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for t, m in list(models.items()) + [("prior xiyansql-32b", prior)]:
        for s in m["seeds"]:
            for split, _ in SPLITS:
                if split not in s:
                    print(f"| {t} | {s['seed']} | {split} | missing |"); continue
                v = s[split]
                b = s.get("budget", {}); c = s.get("custom", {})
                print(f"| {t} | {s['seed']} | {split} | {v['top1_strong']} | {v['A_risk_fit']} | {v['A_risk_strong']} | {v['gap']} | "
                      f"{v['D_risk_strong']} | {v['repair']} | {v['answer_rate_change']} | {b.get('gap')} | {b.get('repair')} | {c.get('gap')} | {c.get('repair')} |")
    print()
    for t, m in list(models.items()) + [("prior xiyansql-32b", prior)]:
        if not m.get("n_seeds_complete"):
            print(f"{t}: no complete results"); continue
        print(f"{t}: question GAP {m['question']['gap_mean']} REPAIR {m['question']['repair_mean']} | "
              f"database GAP {m['database']['gap_mean']} REPAIR {m['database']['repair_mean']} | "
              f"GAP+={m.get('gap_positive')} REPAIR pass={m.get('repair_pass')} robust={m.get('repair_robust')} "
              f"narrow={m.get('repair_narrow')} q-only={m.get('repair_pass_question_only')} | "
              f"control ok={m['control_ok']} suspect={m['instrument_suspect']} {m['control']}")
    print("families:", json.dumps(families, ensure_ascii=False))
    print("outcome:", outcome, summary["counts"])


if __name__ == "__main__":
    main()
