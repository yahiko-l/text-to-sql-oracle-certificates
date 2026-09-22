#!/usr/bin/env python3
"""Rebuild the compact summary tables from the analyser outputs.

This is the generator for the matched-control, candidate-only and gold-free comparisons, so each
table can be regenerated from the result files it summarises. It writes:

  experiments/c5_matched_control_summary.json     matched original-Spider control against the
                                                  preregistered Spider-Realistic pools
  experiments/c4_candidates_only_summary.json     partition built from the candidates alone
  experiments/c4_gold_free_summary.json           candidates-only partition AND a pair-derived
                                                  row-order rule, so the gold is used only to label

All three are post hoc. `--check` compares against the stored files instead of overwriting them.
"""
import argparse, json, os, statistics

TAGS = ("kwai-autosql-32b", "kwai-autosql-14b", "xiyansql-32b", "omnisql-32b")
SEEDS = (101, 202, 303)
G = ("oracle_gap_within_cell_A", "marginal_risk_strong_minus_fit", "mean")
R = ("paired_contrasts_vs_cell_A", "score=multi|calib=multi", "marginal_risk_strong", "mean_change_vs_A")
AR = ("cells", "score=single|calib=single", "marginal_risk_strong", "mean")
AF = ("cells", "score=single|calib=single", "marginal_risk_fit", "mean")
AA = ("cells", "score=single|calib=single", "answer_rate", "mean")
DR = ("cells", "score=multi|calib=multi", "marginal_risk_strong", "mean")
AN = ("paired_contrasts_vs_cell_A", "score=multi|calib=multi", "answer_rate", "mean_change_vs_A")


def get(d, keys):
    for k in keys:
        d = d[k]
    return d


def matched_control():
    rows = []
    for label, pat in (("matched original Spider (one-to-one)", "experiments/c5_kwai-autosql-14b_seed{s}_results{suf}.json"),
                       ("Spider-Realistic (preregistered)", "experiments/c4_kwai-autosql-14b_seed{s}_results{suf}.json")):
        for suf, name in (("_official", "question"), ("_official_dbsplit", "database")):
            v = {k: [] for k in ("g", "r", "ar", "af", "aa", "dr", "an", "t1")}
            for s in SEEDS:
                d = json.load(open(pat.format(s=s, suf=suf)))
                v["g"].append(get(d, G)); v["r"].append(get(d, R)); v["ar"].append(get(d, AR))
                v["af"].append(get(d, AF)); v["aa"].append(get(d, AA)); v["dr"].append(get(d, DR))
                v["an"].append(get(d, AN)); v["t1"].append(d["top1_accuracy_under_strong_oracle"])
            m = lambda k: round(statistics.mean(v[k]), 4)
            rows.append({"set": label, "split": name, "top1": m("t1"), "A_fit": m("af"), "A_strong": m("ar"),
                         "GAP": m("g"), "D_strong": m("dr"), "REPAIR": m("r"), "A_ans": m("aa"),
                         "ans_change": m("an"),
                         "per_seed_GAP": [round(x, 4) for x in v["g"]],
                         "per_seed_REPAIR": [round(x, 4) for x in v["r"]]})
    return rows


def variant(suffix, note, with_intransitivity=False):
    out = {}
    for tag in TAGS:
        a, b, ar, br, nt = [], [], [], [], []
        for s in SEEDS:
            p = f"experiments/c4_{tag}_seed{s}_results_{suffix}.json"
            if not os.path.isfile(p):
                return None
            x = json.load(open(p)); y = json.load(open(f"experiments/c4_{tag}_seed{s}_results_official.json"))
            a.append(get(x, G)); b.append(get(y, G)); ar.append(get(x, R)); br.append(get(y, R))
            c = x.get("counters", {})
            nt.append({"seed": s, "intransitive_pairs_single": c.get("intransitive_pairs_single", 0),
                       "intransitive_pairs_multi": c.get("intransitive_pairs_multi", 0),
                       "questions_with_intransitivity": c.get("questions_with_intransitivity", 0)})
        key = "gold_free" if with_intransitivity else "candidates_only"
        out[tag] = {f"GAP_{key}": round(statistics.mean(a), 4), "GAP_preregistered": round(statistics.mean(b), 4),
                    f"REPAIR_{key}": round(statistics.mean(ar), 4), "REPAIR_preregistered": round(statistics.mean(br), 4),
                    "identical_to_preregistered": a == b and ar == br,
                    "max_abs_diff": round(max(max(abs(u - v) for u, v in zip(a, b)),
                                              max(abs(u - v) for u, v in zip(ar, br))), 5)}
        if with_intransitivity:
            out[tag]["per_seed_GAP_gold_free"] = [round(x, 4) for x in a]
            out[tag]["per_seed_REPAIR_gold_free"] = [round(x, 4) for x in ar]
            out[tag]["intransitivity"] = nt
    return {"note": note, "models": out}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    cand = variant("candonly",
                   "deployment-equivalence sensitivity: the execution-equivalence partition is built from the "
                   "sampled candidates alone, with the gold used only to label a class afterwards")
    gold = variant("goldfree",
                   "fully gold-free sensitivity: the partition is built from the sampled candidates alone AND the "
                   "row-order convention passed to result_eq comes from the pair being compared (order matters if "
                   "either query carries an ORDER BY) rather than from the gold query. The gold is then used only to "
                   "label a class after the partition exists. Deriving the order rule per pair makes the relation "
                   "non-transitive in a few questions; the counts are reported per model.", with_intransitivity=True)
    tables = {"experiments/c5_matched_control_summary.json": matched_control(),
              "experiments/c4_candidates_only_summary.json": cand,
              "experiments/c4_gold_free_summary.json": gold}
    ok = True
    for path, obj in tables.items():
        if obj is None:
            print(f"{path}: source results missing, skipped"); continue
        if a.check:
            stored = json.load(open(path))
            if isinstance(stored, dict):
                stored = {k: v for k, v in stored.items() if k not in ("intransitivity_under_the_pair_order_rule",)}
                obj_cmp = obj
            else:
                obj_cmp = obj
            same = json.dumps(stored, sort_keys=True, default=str) == json.dumps(obj_cmp, sort_keys=True, default=str)
            ok &= same
            print(f"{path}: {'MATCHES' if same else 'DIFFERS from'} the stored file")
        else:
            json.dump(obj, open(path, "w"), indent=1, ensure_ascii=False)
            print("wrote", path)
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
