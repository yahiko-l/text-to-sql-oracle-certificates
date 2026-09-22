#!/usr/bin/env python3
"""The suite-label contrast on exactly the questions the expert contrast is estimated on.

The design calculation of c14 reports the suite-label contrast over every same-SQL question, 507 on
XiYan-32B and 496 on Kwai-32B. The expert endpoint of PREREGISTRATION_4 drops the items the experts
disagree on and those whose verdict is not usable, so it is estimated on fewer questions. Comparing
the two as they stand changes the label and the population at once.

This recomputes the suite-label endpoint on the expert population, question for question, so the two
contrasts differ only in the label. It reads the same scores and the same DeLong test as the frozen
analysis, which it imports rather than edits. Post hoc.
"""
import argparse, csv, json, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c15_alignment_audit_analyse import cells_for, delong, two_sided_p

USABLE = ("answers", "does_not_answer")


def endpoint(tag, by, data, label):
    """Paired AUROC of the two cells' scores against `label(item_id, qid) -> bool | None`."""
    pos, neg = [], []
    for i, r in by.items():
        if not any(u["tag"] == tag and u["same_sql"] for u in r["uses"]):
            continue
        ok = label(i, r["qid"], tag)
        if ok is None:
            continue
        row = data[tag][r["qid"]]
        (pos if ok else neg).append([row["score_a"], row["score_d"]])
    auc, S = delong(pos, neg)
    var = S[0][0] + S[1][1] - 2 * S[0][1]
    d = auc[1] - auc[0]
    se = math.sqrt(var) if var > 0 else 0.0
    return {"auroc_a": round(auc[0], 4), "auroc_d": round(auc[1], 4), "delta": round(d, 4),
            "se": round(se, 4), "p": round(two_sided_p(d / se), 4) if se else 1.0,
            "n_correct": len(pos), "n_wrong": len(neg), "n": len(pos) + len(neg)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", default="experiments/c15_alignment_audit_key.json")
    ap.add_argument("--out", default="experiments/c20_matched_suite_contrast.json")
    a = ap.parse_args()

    key = json.load(open(a.key))
    by = {r["item_id"]: r for r in key["key"]}
    tags = key["checkpoints"]
    data = {t: cells_for(t) for t in tags}
    S = {e: {r["item_id"].strip(): (r.get("verdict") or "").strip()
             for r in csv.DictReader(open(f"experiments/alignment-audit/RESPONSES_{e}.csv",
                                          encoding="utf-8-sig"))} for e in ("E1", "E2")}
    agreed = {i: S["E1"][i] for i in by if S["E1"][i] == S["E2"][i]}

    def expert(i, qid, tag):
        v = agreed.get(i)
        return (v == "answers") if v in USABLE else None

    def suite_on_expert_population(i, qid, tag):
        return data[tag][qid]["suite_ok_a"] if agreed.get(i) in USABLE else None

    def suite_on_all_same_sql(i, qid, tag):
        return data[tag][qid]["suite_ok_a"]

    rep = {"note": __doc__.strip().splitlines()[0], "post_hoc": True, "checkpoints": {}}
    hdr = f"{'checkpoint':<20}{'labels / population':<34}{'n':>6}{'AUROC A':>10}{'AUROC D':>10}{'delta':>9}{'se':>8}{'p':>8}"
    print(hdr + "\n" + "-" * len(hdr))
    for tag in tags:
        row = {
            "expert_agreed": endpoint(tag, by, data, expert),
            "suite_matched": endpoint(tag, by, data, suite_on_expert_population),
            "suite_all_same_sql": endpoint(tag, by, data, suite_on_all_same_sql),
        }
        rep["checkpoints"][tag] = row
        for k, lab in (("expert_agreed", "expert, agreed items"),
                       ("suite_matched", "suite, same items as the experts"),
                       ("suite_all_same_sql", "suite, every same-SQL question")):
            v = row[k]
            print(f"{tag:<20}{lab:<34}{v['n']:>6}{v['auroc_a']:>10.4f}{v['auroc_d']:>10.4f}"
                  f"{v['delta']:>+9.4f}{v['se']:>8.4f}{v['p']:>8.4f}")
        row["population_shrinkage"] = row["suite_all_same_sql"]["n"] - row["suite_matched"]["n"]
        row["delta_shift_from_population"] = round(
            row["suite_matched"]["delta"] - row["suite_all_same_sql"]["delta"], 4)
    json.dump(rep, open(a.out, "w"), indent=1)
    print("\nSaved: " + a.out)


if __name__ == "__main__":
    main()
