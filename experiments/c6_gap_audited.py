#!/usr/bin/env python3
"""C6 step 4: recompute GAP with the audited semantic labels in place of the strong oracle's.

GAP is the difference, inside the current-practice cell, between the risk the certificate actually
carries under the strong oracle and the risk it reports under the labels it was fitted on. Every
answer that contributes to it is an answer the shipped database accepts and the distilled suite
rejects, and the census in c6_semantic_cases.py shows that set is exactly the set of answers the two
oracles disagree about: across all 11351 classes of the twelve pools, no class is strong-correct and
weak-wrong, so the strong label refines the weak one and nothing else moves GAP.

The audit read all 240 of those answers and found most of the rejections are not semantic errors.
This script asks the obvious next question: how much of GAP survives if only a genuine semantic
error counts as a wrong answer. It substitutes an audited oracle for the strong one,

    semantic_ok = strong_ok  or  this convention does not call the answer an error,

and reruns the frozen certificate machinery imported from c4_recompute, on the same splits, at the
same alpha, with the same tie rule. Four nested conventions run, differing in how much reviewer
agreement an error has to carry and in whether instance_defect exculpates; see CONVENTIONS. The
preregistered number is recomputed alongside as a control, so a discrepancy in the harness shows up
as a discrepancy in the control rather than in the result.

Two things this cannot do, both worth saying before the numbers are read. GAP here is non-negative
by construction: the weak label is the coarsest of the lot, so an answer it rejects is rejected
under every convention, and the count of splits with GAP > 0 therefore measures only whether a test
half contained a disagreement at all. It is not a significance statement and the frozen analysis's
split-share figures should not be read as one either. And "not a semantic error" is not the same
proposition as "correct": the taxonomy forced one label per case, and `underspecified` says the
question left the disputed point open, not that the returned query answered it. Every number below
is therefore a convention with a stated rule, not an estimate of a true risk.

Scope, stated because it is easy to overread: this corrects GAP and NOT REPAIR. REPAIR contrasts two
cells whose partitions differ, so the answer cell D returns is the representative of a
multi-instance class, a different string from the one audited here. Correcting REPAIR needs its own
census over the wrong answers of the strong partition, which this audit did not collect.
"""
import argparse, collections, copy, json, os, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c4_recompute import cell_records, evaluate, make_splits, TAGS, SEEDS  # noqa: E402

VARIANTS = ("preregistered", "wide", "narrow", "agreed", "unanimous")

# Four nested conventions for "this answer was really wrong", weakest evidence last.
# They are conventions, not a confidence interval: "not a semantic error" is not the same
# statement as "correct", because the taxonomy forced one label per case and `underspecified`
# only says the question did not settle the point in dispute. So `unanimous` and `agreed` are
# lower bounds on the count of real errors, `narrow` is the audit's own reading, and `wide` is
# a schema-formal sensitivity analysis in which any instance the declared schema permits
# counts as a legitimate witness.
CONVENTIONS = {
    "unanimous": lambda r: (r["label_a"] == r["label_b"] == "semantic_error"
                            and not (r["borderline_a"] or r["borderline_b"])),
    "agreed": lambda r: r["label_a"] == r["label_b"] == "semantic_error",
    "narrow": lambda r: r["label"] == "semantic_error",
    "wide": lambda r: r["label"] in ("semantic_error", "instance_defect"),
}


def top_index(cls):
    """The class cell_records would answer with under the `first` tie rule."""
    best = max(c["count"] for c in cls)
    return next(i for i, c in enumerate(cls) if c["count"] == best)


def defective_gold_questions(audit, cases):
    """Questions carrying at least one gold_defect verdict.

    A strong-ACCEPTED answer to such a question matches, on every instance, a reference the audit
    judged a worse rendering of the question than some model answer. Matching it is therefore
    evidence of being wrong, not of being right. The audit never looked at those answers, so this
    set is what the one-sided design is exposed to.
    """
    q = {cases[cid]["qid"] for cid, r in audit.items() if r["label"] == "gold_defect"}
    return q


def relabel(questions, is_error, stress_questions=frozenset()):
    """Copy the pool with the audited oracle in place of the strong one on the answered class.

    Every strong-wrong answer the census covers is relabelled. Which answers that is depends on
    the census: the c6 census covers only the answers the two oracles disagree about, so an answer
    both oracles reject stays an error there; the c7 census covers every strong-wrong answer of
    the cell, so those are corrected too. Answers outside the census are left as they are and
    counted, because silently treating an unaudited answer as correct would read as a result.
    """
    out = copy.deepcopy(questions)
    touched = outside = 0
    for q in out:
        cls = q["single"]
        if not cls:
            continue
        top = cls[top_index(cls)]
        if not top["strong_ok"]:
            row = is_error.get((q["qid"], top["representative"]))
            if row is None:
                outside += 1
            elif not row:
                top["strong_ok"] = True
                touched += 1
        elif q["qid"] in stress_questions:
            # Stress direction: this answer matched a reference the audit called defective.
            top["strong_ok"] = False
            touched -= 1
    return out, touched, outside


def gap_of(questions, splits, alpha):
    recs = cell_records(questions, "single", "single")
    fit, strong = [], []
    for calq, tstq in splits:
        calq = [q for q in calq if q in recs]
        tstq = [q for q in tstq if q in recs]
        if not calq or not tstq:
            continue
        e = evaluate(recs, calq, tstq, alpha)
        fit.append(e["marginal_risk_fit"])
        strong.append(e["marginal_risk_strong"])
    gap = [s - f for f, s in zip(fit, strong)]
    return {"risk_reported": round(statistics.mean(fit), 4),
            "risk_audited": round(statistics.mean(strong), 4),
            "GAP": round(statistics.mean(gap), 4),
            "GAP_positive_splits": round(sum(1 for g in gap if g > 0) / len(gap), 4)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", default="experiments/c6_semantic_audit.json")
    ap.add_argument("--cases", default="experiments/c6_semantic_cases.json")
    ap.add_argument("--stress-defective-gold", action="store_true",
                    help="also count every strong-ACCEPTED answer on a question with a gold "
                         "defect as wrong. This is the opposite extreme to the audit's own "
                         "one-sidedness, not an estimate: it assumes every such answer inherits "
                         "the defect, which some of them will not.")
    ap.add_argument("--alpha", type=float, default=0.1)
    ap.add_argument("--splits", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260903)
    ap.add_argument("--out", default="experiments/c6_gap_audited.json")
    a = ap.parse_args()

    audit = json.load(open(a.audit))
    cases = json.load(open(a.cases))["cases"]
    by_id = {c["case_id"]: c for c in cases}
    stress = (defective_gold_questions({r["case_id"]: r for r in audit["cases"]},
                                       {c["case_id"]: c for c in cases})
              if a.stress_defective_gold else frozenset())
    err = {}
    for name, pred in CONVENTIONS.items():
        err[name] = {(by_id[r["case_id"]]["qid"], by_id[r["case_id"]]["rep"]): pred(r)
                     for r in audit["cases"]}

    result = {"date": audit.get("date"), "alpha": a.alpha, "splits": a.splits,
              "audit": {"cases": len(cases),
                        "answers": audit["headline"]["answers_total"],
                        "narrow_share_of_answers": audit["band"]["narrow"]["share_of_answers"],
                        "wide_share_of_answers": audit["band"]["wide"]["share_of_answers"]},
              "stress_defective_gold": a.stress_defective_gold,
              "note": "risk_reported is what the certificate claims, fitted on weak labels; "
                      "risk_audited is what it carries under the named convention; GAP is their "
                      "difference. The preregistered row uses the strong oracle unchanged. "
                      "GAP is non-negative by construction ONLY when the census covers just "
                      "the answers the two oracles disagree about, because then every convention "
                      "keeps the strong label a refinement of the weak one. THAT IS THE CENSUS "
                      "THIS FILE USES, so every value here is non-negative. A census that also "
                      "covers the answers both oracles reject breaks the property: exculpating "
                      "one of those lowers the truth side below the reported side and GAP can go "
                      "negative, which is what happens in experiments/c7_gap_audited_full.json, "
                      "not here. Where GAP is non-negative by construction the share of splits "
                      "with GAP > 0 is not a significance statement and must not be read as a "
                      "p-value; the magnitude is the result. Neither figure is an audited "
                      "semantic risk: every answer the strong oracle ACCEPTS is still presumed "
                      "correct, and none of them was audited. Read every number here as a "
                      "quantity relative to the multi-instance suite oracle, never as semantic "
                      "risk.",
              "conventions": {name: {"rule": rule, "cases": sum(1 for r in audit["cases"]
                                                                if CONVENTIONS[name](r))}
                              for name, rule in (
                                  ("unanimous", "both passes independently said semantic_error "
                                                "and neither called the case borderline"),
                                  ("agreed", "both passes independently said semantic_error"),
                                  ("narrow", "the audit's final label is semantic_error"),
                                  ("wide", "narrow plus instance_defect"))},
              "pools": {}, "summary": {}}

    agg = collections.defaultdict(lambda: collections.defaultdict(list))
    for tag in TAGS:
        for seed in SEEDS:
            for split in ("question", "database"):
                suffix = ("_official_per_question.json" if split == "question"
                          else "_official_dbsplit_per_question.json")
                path = f"experiments/c4_{tag}_seed{seed}_results{suffix}"
                qs = json.load(open(path))["questions"]
                qids = [q["qid"] for q in qs]
                dbs = {q["qid"]: q["db"] for q in qs}
                splits = make_splits(qids, dbs, split, a.splits, a.seed)
                row = {"preregistered": gap_of(qs, splits, a.alpha)}
                for variant in CONVENTIONS:
                    rel, n, out_ = relabel(qs, err[variant], stress)
                    row[variant] = {**gap_of(rel, splits, a.alpha), "answers_exculpated": n,
                                    "strong_wrong_answers_outside_the_census": out_}
                result["pools"][f"{tag}|seed{seed}|{split}"] = row
                for v in VARIANTS:
                    agg[(tag, split)][v].append(row[v]["GAP"])
                    agg[("ALL", split)][v].append(row[v]["GAP"])

    for (tag, split), d in sorted(agg.items()):
        result["summary"][f"{tag}|{split}"] = {v: round(statistics.mean(d[v]), 4)
                                               for v in VARIANTS}
        p = result["summary"][f"{tag}|{split}"]
        for v in ("unanimous", "agreed", "narrow", "wide"):
            p["retained_" + v] = (round(p[v] / p["preregistered"], 3)
                                  if p["preregistered"] else None)
    json.dump(result, open(a.out, "w"), indent=1, ensure_ascii=False)

    print(f"GAP at alpha = {a.alpha}, mean over {a.splits} splits and 3 seeds.")
    print("Conventions widen left to right; none of them is a confidence interval.\n")
    print(f"{'':26s}" + "".join(f"{v:>14s}" for v in VARIANTS))
    for split in ("question", "database"):
        print(f"  {split} splits")
        for tag in list(TAGS) + ["ALL"]:
            p = result["summary"][f"{tag}|{split}"]
            print(f"    {tag:22s}" + "".join(f"{p[v]:14.4f}" for v in VARIANTS))
    print(f"\nwritten {a.out}")


if __name__ == "__main__":
    main()
