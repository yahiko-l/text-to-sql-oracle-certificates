#!/usr/bin/env python3
"""C10 step 4: the post-hoc quantities the paper quotes beside the preregistered result.

The preregistered analysis is frozen in c10_blind_audit_analyse.py and stays that way. Everything
here was worked out after the labels came back, in response to questions the preregistration did
not anticipate, and is reported as post hoc. It lives in its own file so that every number in the
paper comes out of a released script.

Five quantities:

  borderline_either      the preregistration fixed two borderline conventions and not how to merge
                         two experts' marks; the frozen analyser takes the first expert's. This is
                         the order-independent alternative: drop an item if either expert marked it.
  design_weighted        a benchmark-wide point estimate. The three strata partition the 508
                         questions, so weighting each stratum's rate by its size gives one. It has
                         no preregistered interval and is not the preregistered endpoint.
  extensional            the protocol asks what a reference query returns on the supplied database,
                         and six adjudications call a reference defective whose result on that
                         database is right and whose logic fails elsewhere. This scores those six
                         the other way.
  human_vs_ai_restricted the preregistered human-versus-AI figure codes every never-examined item
                         as an AI negative, though the AI never examined them. This restricts the
                         comparison to the questions the AI actually looked at.
  single_expert          each independent expert's own sheet, run through the rule on its own. The
                         third pass was performed by the project lead, so this is the reading that
                         owes nothing to an interested party.
  defect_types           the human defect-type distribution, a preregistered descriptive secondary
                         analysis the frozen analyser reports but the result file alone does not
                         break out by stratum.
"""
import argparse
import collections
import csv
import importlib.util
import json
import os

# The six adjudications whose own note records that the current result agrees and the logic does not.
LATENT = ("Q033", "Q070", "Q080", "Q108", "Q145", "Q146")


def load_frozen(path="experiments/c10_blind_audit_analyse.py"):
    spec = importlib.util.spec_from_file_location("frozen", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_raw(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return {r["item_id"].strip(): r for r in csv.DictReader(f) if (r.get("verdict") or "").strip()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", default="experiments/c10_blind_audit_key.json")
    ap.add_argument("--responses", nargs=2,
                    default=["experiments/blind_audit/RESPONSES_专家1.clean.csv",
                             "experiments/blind_audit/RESPONSES_专家2.clean.csv"])
    ap.add_argument("--adjudicated", default="experiments/blind_audit/ADJUDICATION_标注.clean.csv")
    ap.add_argument("--out", default="experiments/c10_blind_audit_sensitivity.json")
    a = ap.parse_args()

    fz = load_frozen()
    K = json.load(open(a.key))
    key, bench = K["key"], K["strata_sizes_in_the_benchmark"]
    stratum = {k["item_id"]: k["stratum"] for k in key}

    e1, e2 = (fz.read_responses(p) for p in a.responses)
    adj = fz.read_responses(a.adjudicated)
    raw1, raw2 = (read_raw(p) for p in a.responses)

    merged = dict(e1)
    for k, v in e2.items():
        merged.setdefault(k, v)
    merged.update(adj)

    out = {"note": "post-hoc quantities; the preregistered analysis is in c10_blind_audit_result.json",
           "generated_from": {"key": a.key, "responses": a.responses, "adjudicated": a.adjudicated}}

    # 1. borderline, order-independent
    either = {i: (raw1[i]["borderline"].strip().lower() in ("yes", "y", "true", "1")
                  or raw2[i]["borderline"].strip().lower() in ("yes", "y", "true", "1"))
              for i in raw1 if i in raw2}
    keep = {i: v for i, v in merged.items() if not either.get(i, False)}
    rates_either = fz.rates([k for k in key if k["item_id"] in keep], keep)
    out["borderline_either"] = {
        "rule": "drop an item if either expert marked it borderline",
        "conflicting_marks_on_agreed_verdicts":
            sum(1 for i in raw1 if i in raw2 and e1[i]["verdict"] == e2[i]["verdict"]
                and raw1[i]["borderline"].strip().lower() != raw2[i]["borderline"].strip().lower()),
        "rates": rates_either,
        "decision": fz.decide(rates_either)}

    # 2. design-weighted benchmark-wide point estimate
    r = fz.rates(key, merged)
    weighted = (r["flagged"]["defective"]
                + bench["examined"] * r["examined"]["D"]
                + bench["unexamined"] * r["unexamined"]["D"]) / sum(bench.values())
    out["design_weighted"] = {
        "rule": "every flagged question was sampled, so its confirmed count enters directly; the "
                "two controls enter at their sampled rates times their stratum sizes",
        "strata_sizes": bench, "questions": sum(bench.values()),
        "estimate": round(weighted, 4),
        "interval95": None,
        "caveat": "point estimate only; no preregistered interval, and the strata are defined by "
                  "what four checkpoints exposed"}

    # 3. strictly extensional scoring of the six latent-defect adjudications
    ext = dict(merged)
    for i in LATENT:
        ext[i] = dict(ext[i], verdict="gold_correct")
    rates_ext = fz.rates(key, ext)
    out["extensional"] = {
        "rule": "score a reference correct when its result on the supplied database is correct, "
                "even where its logic would fail on other data",
        "items": list(LATENT), "rates": rates_ext, "decision": fz.decide(rates_ext)}

    # 4. human versus AI on the questions the AI actually examined
    seen = [k["item_id"] for k in key if k["stratum"] in ("flagged", "examined")]
    h = [merged[i]["verdict"] == "gold_defective" for i in seen]
    m = [stratum[i] == "flagged" for i in seen]
    out["human_vs_ai_restricted"] = {
        "rule": "the preregistered figure codes the never-examined stratum as an AI negative, "
                "though the AI never examined it; this restricts to the flagged and examined strata",
        "n": len(seen),
        "agreement": round(sum(1 for x, y in zip(h, m) if x == y) / len(seen), 4),
        "kappa": fz.cohen_kappa(h, m)}

    # 5. each expert alone, owing nothing to the adjudication
    out["single_expert"] = {}
    for name, sheet in (("expert1", e1), ("expert2", e2)):
        rr = fz.rates(key, sheet)
        out["single_expert"][name] = {"rates": rr, "decision": fz.decide(rr)}

    # 6. human defect types, overall and by stratum
    by_stratum = collections.defaultdict(collections.Counter)
    for i, v in merged.items():
        if v["verdict"] == "gold_defective":
            by_stratum[stratum[i]][v["defect_type"] or "unspecified"] += 1
    out["defect_types"] = {
        "overall": dict(collections.Counter(
            v["defect_type"] or "unspecified" for v in merged.values()
            if v["verdict"] == "gold_defective")),
        "by_stratum": {s: dict(c) for s, c in sorted(by_stratum.items())}}

    # 7. both kappas, so the preregistered five-class and binary readings are both on the record
    ids = sorted(merged)
    out["expert_agreement"] = {
        "n": len(ids),
        "four_way_agreement": round(sum(1 for i in ids
                                        if e1[i]["verdict"] == e2[i]["verdict"]) / len(ids), 4),
        "four_way_kappa": fz.cohen_kappa([e1[i]["verdict"] for i in ids],
                                         [e2[i]["verdict"] for i in ids]),
        "binary_agreement": round(sum(1 for i in ids
                                      if (e1[i]["verdict"] == "gold_defective")
                                      == (e2[i]["verdict"] == "gold_defective")) / len(ids), 4),
        "binary_kappa": fz.cohen_kappa([e1[i]["verdict"] == "gold_defective" for i in ids],
                                       [e2[i]["verdict"] == "gold_defective" for i in ids])}

    json.dump(out, open(a.out, "w"), indent=1, ensure_ascii=False)
    d, e = out["extensional"]["decision"], out["borderline_either"]["decision"]
    print(f"borderline, either expert marks : margin {100 * e['margin']:.1f} points -> {e['verdict']}")
    print(f"strictly extensional            : margin {100 * d['margin']:.1f} points -> {d['verdict']}")
    print(f"design-weighted over {out['design_weighted']['questions']} questions : "
          f"{100 * out['design_weighted']['estimate']:.1f}%")
    for name, v in out["single_expert"].items():
        d2 = v["decision"]
        print(f"{name} alone                  : margin {100 * d2['margin']:.1f} points -> {d2['verdict']}")
    hr = out["human_vs_ai_restricted"]
    print(f"human vs AI on examined strata  : {100 * hr['agreement']:.1f}%, kappa {hr['kappa']}, n={hr['n']}")
    ea = out["expert_agreement"]
    print(f"expert agreement                : four-way {100 * ea['four_way_agreement']:.1f}% "
          f"kappa {ea['four_way_kappa']}, binary {100 * ea['binary_agreement']:.1f}% kappa {ea['binary_kappa']}")
    print(f"human defect types              : {out['defect_types']['overall']}")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
