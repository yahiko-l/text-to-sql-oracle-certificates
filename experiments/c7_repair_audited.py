#!/usr/bin/env python3
"""C7 step 3: recompute REPAIR with the audited semantic labels in place of the strong oracle's.

REPAIR is the paired change in strong-oracle risk from the current-practice cell A to the
strong-partition, strong-label cell D. The c6 audit could not touch it: it covered only the answers
the two oracles disagree about, and REPAIR counts every answer the strong oracle rejects, in two
cells whose returned SQL differs on the questions where the partitions disagree. The c7 census
closes that, covering all 742 distinct answers either cell returns and the suite rejects.

WHICH SIDE GETS RELABELLED, because it decides what the number means. The claim under test is that
calibrating with the strong oracle repairs the risk, so the strong oracle is the INTERVENTION and
has to stay exactly where it was: cell D still fits its threshold on strong labels, as it did when
the experiment ran. What the audit replaces is the YARDSTICK, the labels both cells are scored
against. That is the primary row, `evaluation_only`, and it answers: of the risk cell D appeared to
remove, how much was real?

A second row, `also_recalibrated`, additionally lets cell D fit on the audited labels. That is a
different and hypothetical system, one calibrated against a semantic oracle nobody has, and it is
reported only so a reader who wants it does not have to guess.

The splice that makes this exact: cell_records is called twice per cell, once on the untouched pool
and once on the relabelled copy, and the records are merged so the fitted threshold, the answered
set and fit_ok come from the run as it happened while the correctness used for risk comes from the
audit. Relabelling never changes a class count, so the two record sets agree question by question.
"""
import argparse, collections, copy, json, os, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c4_recompute import cell_records, evaluate, make_splits, TAGS, SEEDS  # noqa: E402
from c6_gap_audited import CONVENTIONS, top_index  # noqa: E402

ALL_VARIANTS = ("preregistered", "wide", "narrow", "agreed", "unanimous")
CELLS = {"A": ("single", "single"), "D": ("multi", "multi")}


def relabel(questions, is_error, scoring):
    """Copy the pool with the audited oracle on the class the named cell answers with."""
    out = copy.deepcopy(questions)
    touched = missing = 0
    for q in out:
        cls = q[scoring]
        if not cls:
            continue
        top = cls[top_index(cls)]
        if not top["strong_ok"]:
            row = is_error.get((q["qid"], top["representative"]))
            if row is None:
                missing += 1
                continue
            if not row:
                top["strong_ok"] = True
                touched += 1
    if missing:
        raise SystemExit(f"{missing} answers of cell {scoring} were never audited")
    return out, touched


def spliced(questions, relabelled, scoring, cal, recalibrate):
    """Records whose threshold comes from the run as it happened and whose risk from the audit."""
    base = cell_records(questions, scoring, cal)
    aud = cell_records(relabelled, scoring, cal)
    out = {}
    for qid, r in base.items():
        a = aud[qid]
        out[qid] = dict(r, strong_ok=a["strong_ok"], strong_mass=a["strong_mass"])
        if recalibrate:
            out[qid]["fit_ok"] = a["fit_ok"]
            out[qid]["fit_mass"] = a["fit_mass"]
    return out


def run_cells(questions, is_error, splits, alpha, recalibrate):
    per = {}
    for cell, (scoring, cal) in CELLS.items():
        rel, n = relabel(questions, is_error, scoring) if is_error else (questions, 0)
        recs = spliced(questions, rel, scoring, cal, recalibrate)
        risk, rate = [], []
        for calq, tstq in splits:
            calq = [q for q in calq if q in recs]
            tstq = [q for q in tstq if q in recs]
            if not calq or not tstq:
                continue
            e = evaluate(recs, calq, tstq, alpha)
            risk.append(e["marginal_risk_strong"])
            rate.append(e["answer_rate"])
        per[cell] = {"risk": risk, "rate": rate, "exculpated": n}
    d = [b - a for a, b in zip(per["A"]["risk"], per["D"]["risk"])]
    dr = [b - a for a, b in zip(per["A"]["rate"], per["D"]["rate"])]
    return {"risk_A": round(statistics.mean(per["A"]["risk"]), 4),
            "risk_D": round(statistics.mean(per["D"]["risk"]), 4),
            "REPAIR": round(statistics.mean(d), 4),
            "REPAIR_negative_splits": round(sum(1 for x in d if x < 0) / len(d), 4),
            "answer_rate_A": round(statistics.mean(per["A"]["rate"]), 4),
            "answer_rate_change": round(statistics.mean(dr), 4),
            "exculpated_A": per["A"]["exculpated"], "exculpated_D": per["D"]["exculpated"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default="experiments/c7_repair_cases.json")
    ap.add_argument("--audit", default="experiments/c7_semantic_audit.json",
                    help="the merged audit over all cases of both populations, carrying each "
                         "case's two passes and its adjudicated label")
    ap.add_argument("--alpha", type=float, default=0.1)
    ap.add_argument("--splits", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260903)
    ap.add_argument("--recalibrate", action="store_true",
                    help="also let cell D fit on the audited labels; a different, hypothetical "
                         "system, reported as a secondary row")
    ap.add_argument("--out", default="experiments/c7_repair_audited.json")
    a = ap.parse_args()

    cases = json.load(open(a.cases))["cases"]
    by_id = collections.defaultdict(list)
    for c in cases:
        by_id[c["case_id"]].append(c)

    rows = {r["case_id"]: r for r in json.load(open(a.audit))["cases"]}

    # The `agreed` and `unanimous` conventions ask whether TWO passes said semantic_error. A case
    # carrying only one pass silently fails that test and is scored as not-an-error, which would
    # read as a lower bound when it is really a missing measurement. Refuse rather than mislead.
    one_pass = [c["case_id"] for c in cases if rows.get(c["case_id"], {}).get("label_b") is None]
    err = {}
    for name, pred in CONVENTIONS.items():
        if name in ("agreed", "unanimous") and one_pass:
            continue
        m = {}
        for c in cases:
            r = rows.get(c["case_id"])
            if r is None:
                raise SystemExit(f"case {c['case_id']} has no label")
            m[(c["qid"], c["rep"])] = pred(r)
        err[name] = m
    if one_pass:
        print(f"WARNING: {len(one_pass)} of {len(cases)} cases have only one labelling pass, so "
              f"the two-pass conventions are NOT computed. Reporting preregistered, wide and "
              f"narrow only.\n")

    VARIANTS = tuple(v for v in ALL_VARIANTS if v == "preregistered" or v in err)
    result = {"date": None, "alpha": a.alpha, "splits": a.splits,
              "conventions_computed": list(VARIANTS),
              "cases_with_one_pass_only": len(one_pass),
              "mode": "also_recalibrated" if a.recalibrate else "evaluation_only",
              "population": json.load(open(a.cases))["population"],
              "note": "REPAIR is cell D's risk minus cell A's, both under the named yardstick; "
                      "negative means cell D carries less. In the primary mode the strong oracle "
                      "stays the intervention and only the yardstick is audited.",
              "pools": {}, "summary": {}}
    agg = collections.defaultdict(lambda: collections.defaultdict(list))
    for tag in TAGS:
        for seed in SEEDS:
            for split in ("question", "database"):
                suffix = ("_official_per_question.json" if split == "question"
                          else "_official_dbsplit_per_question.json")
                qs = json.load(open(f"experiments/c4_{tag}_seed{seed}_results{suffix}"))["questions"]
                splits = make_splits([q["qid"] for q in qs], {q["qid"]: q["db"] for q in qs},
                                     split, a.splits, a.seed)
                row = {"preregistered": run_cells(qs, None, splits, a.alpha, False)}
                for v in err:
                    row[v] = run_cells(qs, err[v], splits, a.alpha, a.recalibrate)
                result["pools"][f"{tag}|seed{seed}|{split}"] = row
                for v in VARIANTS:
                    agg[(tag, split)][v].append(row[v]["REPAIR"])
                    agg[(tag, split)][v + "_neg"].append(row[v]["REPAIR_negative_splits"])
                    agg[("ALL", split)][v].append(row[v]["REPAIR"])
    for (tag, split), d in sorted(agg.items()):
        result["summary"][f"{tag}|{split}"] = {v: round(statistics.mean(d[v]), 4) for v in VARIANTS}
        for v in VARIANTS:
            if d[v + "_neg"]:
                result["summary"][f"{tag}|{split}"][v + "_negative_splits"] = round(
                    statistics.mean(d[v + "_neg"]), 4)
    json.dump(result, open(a.out, "w"), indent=1, ensure_ascii=False)

    print(f"REPAIR at alpha = {a.alpha}, mode {result['mode']}. Negative means cell D is better.\n")
    print(f"{'':26s}" + "".join(f"{v:>14s}" for v in VARIANTS))
    for split in ("question", "database"):
        print(f"  {split} splits")
        for tag in list(TAGS) + ["ALL"]:
            s = result["summary"][f"{tag}|{split}"]
            print(f"    {tag:22s}" + "".join(f"{s[v]:14.4f}" for v in VARIANTS))
    print(f"\nwritten {a.out}")


if __name__ == "__main__":
    main()
