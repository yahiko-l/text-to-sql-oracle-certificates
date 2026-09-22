#!/usr/bin/env python3
"""C6 step 3: stratify the audit cases mechanically and fold in the reviewer labels.

Two things happen here and they are kept apart on purpose.

The STRATUM of a case is a computation. It says what kind of difference the two result tables show
on the first instance that separates them, and how much of the suite separates them. It involves no
reading of the question and no judgement, so it is reproducible from the evidence file alone.

The LABEL of a case is a judgement, and it is not made here. It is read from the reviewer passes,
because the party whose headline claim this audit tests must not be the party that grades it. Two
independent passes are merged: agreement is reported, disagreements are carried as a band rather
than silently resolved, and an adjudication file (a third pass over the disagreements only) closes
them when present.

The output is the audit summary: what share of weak-correct, strong-wrong answers are genuine
semantic errors, what share are the strong oracle rejecting an answer the question never ruled out,
and how the error types distribute. Shares are reported over answers as well as over cases, because
one case can be the answer several pools returned, and the risk numbers count answers.
"""
import argparse, collections, json, os

# Priority-ordered, mutually exclusive. First matching rule wins.
MECHANISM_RULES = [
    ("row_order_only", "the same rows in a different order"),
    ("duplicate_multiplicity_only", "the same distinct rows with different multiplicity"),
    ("col_count_differs", "a different number of columns"),
    ("gold_empty", "the gold returns nothing here"),
    ("rep_empty", "the returned query returns nothing here"),
    ("gold_subset_of_rep", "the returned result strictly contains the gold's"),
    ("rep_subset_of_gold", "the returned result is strictly contained in the gold's"),
    ("disjoint", "no row in common"),
]
ARTIFACT_LABELS = ("underspecified", "gold_defect", "instance_defect", "comparator_artifact")
LABELS = ("semantic_error",) + ARTIFACT_LABELS


def mechanism(w):
    if w.get("execution_error"):
        return "execution_error"
    for k, _ in MECHANISM_RULES:
        if w.get(k):
            return k
    return "partial_overlap"


def breadth(c):
    f = c["disagree_fraction"]
    return "narrow (<=10% of instances)" if f <= 0.10 else \
           "middling (10-50%)" if f <= 0.50 else "broad (>50%)"


def load_labels(path, cases=None):
    """Read one reviewer pass, refusing anything outside the taxonomy.

    A label the taxonomy does not contain is a pass that graded something other than what this
    audit defines, and every share below would silently absorb it. Same for a case id the
    stratification never produced.
    """
    if not path or not os.path.isfile(path):
        return {}
    d = json.load(open(path))
    rows = d["labels"] if isinstance(d, dict) else d
    out = {}
    for r in rows:
        cid = r["case_id"]
        lab = r.get("label")
        if lab is not None and lab not in LABELS:
            raise SystemExit(f"{path}: case {cid} carries label {lab!r}, which is not one of "
                             f"{LABELS}")
        if cases is not None and cid not in cases:
            raise SystemExit(f"{path}: case {cid} is not one of the {len(cases)} cases this run "
                             f"stratified")
        if cid in out:
            raise SystemExit(f"{path}: case {cid} appears twice")
        out[cid] = r
    return out


def share(n, d):
    return round(n / d, 4) if d else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default="experiments/c6_semantic_cases.json")
    ap.add_argument("--pass-a", default="experiments/c6_labels_pass_a.json")
    ap.add_argument("--pass-b", default="experiments/c6_labels_pass_b.json")
    ap.add_argument("--adjudication", default="experiments/c6_labels_adjudicated.json")
    ap.add_argument("--carry-over", default="",
                    help="a completed audit summary whose cases were judged in an earlier round "
                         "under the same protocol; their two passes and final label are taken "
                         "from it rather than re-judged, so one audit covers both populations")
    ap.add_argument("--date", default="")
    ap.add_argument("--out", default="experiments/c6_semantic_audit.json")
    a = ap.parse_args()

    d = json.load(open(a.cases))
    C = {c["case_id"]: c for c in d["cases"]}
    A, B, ADJ = (load_labels(a.pass_a, C), load_labels(a.pass_b, C),
                 load_labels(a.adjudication, C))
    CARRY = {}
    if a.carry_over:
        for r in json.load(open(a.carry_over))["cases"]:
            CARRY[r["case_id"]] = r
        for cid, r in CARRY.items():
            A.setdefault(cid, {"label": r["label_a"], "error_type": r["error_type_a"],
                               "borderline": r["borderline_a"]})
            B.setdefault(cid, {"label": r["label_b"], "error_type": r["error_type_b"],
                               "borderline": r["borderline_b"]})
            if r["source"] == "adjudicated":
                ADJ.setdefault(cid, {"label": r["label"], "error_type": r["error_type"]})

    rows = []
    for cid, c in C.items():
        n_ans = len(c["answers"])
        r = {"case_id": cid, "qid": c["qid"], "db": c["db"], "answers": n_ans,
             "mechanism": mechanism(c["witness"]), "breadth": breadth(c),
             "disagree_fraction": c["disagree_fraction"],
             "label_a": A.get(cid, {}).get("label"), "label_b": B.get(cid, {}).get("label"),
             "error_type_a": A.get(cid, {}).get("error_type"),
             "error_type_b": B.get(cid, {}).get("error_type"),
             "borderline_a": A.get(cid, {}).get("borderline"),
             "borderline_b": B.get(cid, {}).get("borderline")}
        r["agree"] = (r["label_a"] is not None and r["label_a"] == r["label_b"])
        if cid in ADJ and r["agree"]:
            # The third pass exists to close disagreements. Letting it rewrite a label both
            # passes reached would make the two-pass agreement statistic meaningless and would
            # put the last word on a case in the hands of whoever ran the third pass.
            raise SystemExit(f"adjudication file resolves case {cid}, on which both passes "
                             f"already agree ({r['label_a']!r}). Agreed cases are fixed; the "
                             f"third pass covers disagreements only.")
        if cid in ADJ:
            r["label"] = ADJ[cid]["label"]
            r["error_type"] = ADJ[cid].get("error_type")
            r["source"] = "adjudicated"
        elif r["agree"]:
            r["label"] = r["label_a"]
            r["error_type"] = r["error_type_a"] or r["error_type_b"]
            r["source"] = "both passes agree"
        else:
            r["label"] = None
            r["error_type"] = None
            r["source"] = "unresolved" if r["label_a"] and r["label_b"] else "incomplete"
        rows.append(r)

    n_cases = len(rows)
    n_ans = sum(r["answers"] for r in rows)
    labelled = [r for r in rows if r["label"]]
    la = sum(r["answers"] for r in labelled)

    def tally(key, weight):
        t = collections.Counter()
        for r in labelled:
            t[r[key] or "n/a"] += (r["answers"] if weight else 1)
        return dict(t.most_common())

    both = [r for r in rows if r["label_a"] and r["label_b"]]
    agree = [r for r in both if r["agree"]]
    # Agreement on the question the audit is actually about: error against not-an-error.
    binar = lambda x: "semantic_error" if x == "semantic_error" else "artifact"
    bin_agree = [r for r in both if binar(r["label_a"]) == binar(r["label_b"])]

    sem = [r for r in labelled if r["label"] == "semantic_error"]
    art = [r for r in labelled if r["label"] in ARTIFACT_LABELS]
    unres = [r for r in rows if r["source"] == "unresolved"]

    out = {
        "date": a.date or None,
        "population": d["population"],
        "labelling": {
            "passes": 2,
            "cases_with_both_passes": len(both),
            "full_label_agreement": share(len(agree), len(both)),
            "error_versus_artifact_agreement": share(len(bin_agree), len(both)),
            "adjudicated": sum(1 for r in rows if r["source"] == "adjudicated"),
            "carried_over": len(CARRY),
            "unresolved": len(unres),
            "unresolved_case_ids": [r["case_id"] for r in unres],
            "note": "this script assigns no label; mechanism and breadth are computed, labels "
                    "come from the reviewer passes and disagreements are adjudicated in a "
                    "separate pass over those cases only",
        },
        "headline": {
            "cases_labelled": len(labelled), "cases_total": n_cases,
            "answers_labelled": la, "answers_total": n_ans,
            "genuine_semantic_error": {
                "cases": len(sem), "share_of_cases": share(len(sem), len(labelled)),
                "answers": sum(r["answers"] for r in sem),
                "share_of_answers": share(sum(r["answers"] for r in sem), la)},
            "strong_oracle_rejection_without_semantic_error": {
                "cases": len(art), "share_of_cases": share(len(art), len(labelled)),
                "answers": sum(r["answers"] for r in art),
                "share_of_answers": share(sum(r["answers"] for r in art), la)},
            "borderline_in_either_pass": sum(1 for r in labelled
                                             if r["borderline_a"] or r["borderline_b"]),
        },
        # instance_defect is the one label whose exculpating force is a reading, not an
        # observation. It says the separating instance could not be a real database of this
        # schema. That is true of the world it models and false of the schema as declared: the
        # schema does not make a country name unique or an age numeric, so a strict reader holds
        # that those instances are legal and the two queries genuinely differ. The number is
        # reported both ways rather than settled, because the choice is the reader's.
        "band": {
            "definition": {
                "narrow": "a genuine semantic error is only what the reviewers labelled "
                          "semantic_error; every other label is the strong oracle rejecting an "
                          "answer the question did not rule out",
                "wide": "semantic_error plus instance_defect, the reading under which any "
                        "instance the declared schema permits is a legitimate witness",
            },
        },
        "by_model": {},
        "label_distribution_cases": tally("label", False),
        "label_distribution_answers": tally("label", True),
        "error_type_distribution": dict(collections.Counter(
            r["error_type"] or "n/a" for r in sem).most_common()),
        "by_mechanism": {},
        "by_breadth": {},
        "by_database": {},
        "cases": rows,
    }
    WIDE = ("semantic_error", "instance_defect")
    for name, keys in (("narrow", ("semantic_error",)), ("wide", WIDE)):
        err = [r for r in labelled if r["label"] in keys]
        out["band"][name] = {
            "cases": len(err), "share_of_cases": share(len(err), len(labelled)),
            "answers": sum(r["answers"] for r in err),
            "share_of_answers": share(sum(r["answers"] for r in err), la)}

    # Which pool each audited answer came from, so the reader can see whether one checkpoint
    # carries the artifacts. Answers, not cases: a case shared by six pools is six answers.
    per_model = collections.defaultdict(lambda: collections.Counter())
    C_ans = {c["case_id"]: c["answers"] for c in d["cases"]}
    for r in rows:
        for ans in C_ans[r["case_id"]]:
            per_model[ans["model"]]["answers"] += 1
            if r["label"]:
                per_model[ans["model"]][r["label"]] += 1
                if r["label"] in WIDE:
                    per_model[ans["model"]]["wide_error"] += 1
    for m, c in sorted(per_model.items()):
        out["by_model"][m] = {**dict(c),
                              "share_semantic_error": share(c["semantic_error"], c["answers"]),
                              "share_wide_error": share(c["wide_error"], c["answers"])}

    for field, dest in (("mechanism", "by_mechanism"), ("breadth", "by_breadth"),
                        ("db", "by_database")):
        g = collections.defaultdict(list)
        for r in rows:
            g[r[field]].append(r)
        for k, v in sorted(g.items(), key=lambda kv: -len(kv[1])):
            lab = [r for r in v if r["label"]]
            out[dest][k] = {
                "cases": len(v), "answers": sum(r["answers"] for r in v),
                "labelled": len(lab),
                "semantic_error": sum(1 for r in lab if r["label"] == "semantic_error"),
                "share_semantic_error": share(
                    sum(1 for r in lab if r["label"] == "semantic_error"), len(lab))}
    json.dump(out, open(a.out, "w"), indent=1, ensure_ascii=False)

    h = out["headline"]
    print(f"cases {h['cases_labelled']}/{h['cases_total']} labelled, "
          f"answers {h['answers_labelled']}/{h['answers_total']}")
    print(f"reviewer agreement: full {out['labelling']['full_label_agreement']}, "
          f"error-vs-artifact {out['labelling']['error_versus_artifact_agreement']}, "
          f"unresolved {out['labelling']['unresolved']}")
    print(f"genuine semantic error: {h['genuine_semantic_error']['share_of_cases']} of cases, "
          f"{h['genuine_semantic_error']['share_of_answers']} of answers")
    print(f"rejected without semantic error: "
          f"{h['strong_oracle_rejection_without_semantic_error']['share_of_cases']} of cases, "
          f"{h['strong_oracle_rejection_without_semantic_error']['share_of_answers']} of answers")
    b = out["band"]
    print(f"band, share of ANSWERS that are a genuine semantic error: "
          f"narrow {b['narrow']['share_of_answers']}, wide {b['wide']['share_of_answers']}")
    print("labels:", out["label_distribution_cases"])
    print("error types:", out["error_type_distribution"])


if __name__ == "__main__":
    main()
