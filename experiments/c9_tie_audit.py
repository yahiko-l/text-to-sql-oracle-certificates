#!/usr/bin/env python3
"""C9 step 2: what the tie-rule proxy actually costs, measured rather than assumed.

Every recomputation from the per-question files, including both semantic censuses, selects the top
class of a tie by file order, while the frozen analyser selected it by the largest union-find key.
c9_tie_reconstruct.py rebuilt the frozen choice on the 53 tied decisions. This script answers the
only question that matters: does using the frozen choice instead change anything that has been
claimed.

Four measurements.

  --enumerate   list every tied decision from the per-question files, the input to the
                reconstruction. Ties are the only decisions that can differ.

  --populations how the two census populations move under the frozen choice, and how many of the
                answers that should have been audited never were.

  --recompute   GAP and REPAIR under the frozen choice, preregistered and audited, with the
                answers that were never labelled bracketed BOTH ways: counted as semantic errors
                and counted as not errors. A conclusion that survives both brackets is not at risk
                from the unlabelled answers; one that does not is reported as at risk.

  --six-scores  the same comparison for every score of the six-score comparison of
                c8_baselines.py, under the preregistered labels and under every census
                convention. All six scores answer with the representative of the top class, so
                all six inherit the tie rule.

  --gap-ladder  the two GAP ladder columns --recompute does not reach: GAP relabelled with the
                disagreement census, and the reverse stress test of c6_gap_audited.py.

What the patch does and does not touch. Tied classes carry the same count, so moving one to the
front leaves the class counts, the mass vector, the top-class mass, the fitting-class mass and the
strong-correct-class mass exactly as the analyser wrote them. It does change which class is
answered, and therefore its correctness labels; and because the CRC threshold is fitted on those
labels, lambda and the answered set move with them. Over the 9600 pool-split-cell evaluations this
changes 83 lambda values and 66 answer rates. That propagation is the point of the measurement, not
a side effect: it is exactly how a different tie rule would have reached the reported numbers.
"""
import argparse, collections, copy, json, os, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c4_recompute import cell_records, evaluate, make_splits, TAGS, SEEDS  # noqa: E402
from c6_gap_audited import CONVENTIONS  # noqa: E402

SUFFIX = {"question": "_official_per_question.json",
          "database": "_official_dbsplit_per_question.json"}


def path_of(tag, seed, split):
    return f"experiments/c4_{tag}_seed{seed}_results{SUFFIX[split]}"


def top_index(cls):
    best = max(c["count"] for c in cls)
    return next(i for i, c in enumerate(cls) if c["count"] == best)


def enumerate_ties():
    tied, examined = [], 0
    for tag in TAGS:
        for seed in SEEDS:
            for q in json.load(open(path_of(tag, seed, "question")))["questions"]:
                for part in ("single", "multi"):
                    cls = q[part]
                    examined += 1
                    if not cls:
                        continue
                    mx = max(c["count"] for c in cls)
                    t = [c for c in cls if c["count"] == mx]
                    if len(t) > 1:
                        tied.append({"tag": tag, "seed": seed, "qid": q["qid"], "db": q["db"],
                                     "part": part, "n_tied": len(t),
                                     "reps": [c["representative"] for c in t],
                                     "weak": [c["weak_ok"] for c in t],
                                     "strong": [c["strong_ok"] for c in t]})
    return examined, tied


def frozen_map():
    """(tag, seed, qid, part) -> the reconstructed frozen decision."""
    d = json.load(open("experiments/c9_tie_reconstruction.json"))["decisions"]
    return {(x["tag"], x["seed"], x["qid"], x["part"]): x for x in d}


def patch(questions, tag, seed, fm):
    """Move the frozen top class to the front of its class list, on tied decisions only.

    Tied classes have equal counts, so the class counts and every mass are left exactly as the
    analyser wrote them. What moves is which class is answered, hence its correctness labels, hence
    the CRC threshold fitted on them and the set of questions answered at that threshold.
    """
    out = copy.deepcopy(questions)
    moved = 0
    for q in out:
        for part in ("single", "multi"):
            f = fm.get((tag, seed, q["qid"], part))
            if not f or f["same_rep"]:
                continue
            cls = q[part]
            i = next((j for j, c in enumerate(cls) if c["representative"] == f["frozen_rep"]), None)
            if i is None:
                raise SystemExit(f"{tag} s{seed} q{q['qid']} {part}: frozen representative absent "
                                 f"from the class list")
            cls.insert(0, cls.pop(i))
            moved += 1
    return out, moved


def populations(fm):
    """How the two census populations move, and what was never labelled."""
    c6 = {(c["qid"], c["rep"]) for c in json.load(open("experiments/c6_semantic_cases.json"))["cases"]}
    c7 = {(c["qid"], c["rep"]) for c in json.load(open("experiments/c7_repair_cases.json"))["cases"]}
    stored6 = stored7 = frozen6 = frozen7 = 0
    fz6, fz7 = set(), set()
    for tag in TAGS:
        for seed in SEEDS:
            qs = json.load(open(path_of(tag, seed, "question")))["questions"]
            pq, _ = patch(qs, tag, seed, fm)
            for src, is6, is7 in ((qs, [], []), (pq, [], [])):
                pass
            for q, p in zip(qs, pq):
                a, b = q["single"][top_index(q["single"])], p["single"][top_index(p["single"])]
                if a["weak_ok"] and not a["strong_ok"]:
                    stored6 += 1
                if b["weak_ok"] and not b["strong_ok"]:
                    frozen6 += 1
                    fz6.add((q["qid"], b["representative"]))
                for part in ("single", "multi"):
                    if not q[part][top_index(q[part])]["strong_ok"]:
                        stored7 += 1
                    t = p[part][top_index(p[part])]
                    if not t["strong_ok"]:
                        frozen7 += 1
                        fz7.add((q["qid"], t["representative"]))
    return {
        "c6": {"stored_answers": stored6, "frozen_answers": frozen6,
               "cases_labelled": len(c6), "cases_under_frozen": len(fz6),
               "never_labelled": sorted(fz6 - c6), "labelled_but_not_in_population": len(c6 - fz6)},
        "c7": {"stored_answers": stored7, "frozen_answers": frozen7,
               "cases_labelled": len(c7), "cases_under_frozen": len(fz7),
               "never_labelled": sorted(fz7 - c7), "labelled_but_not_in_population": len(c7 - fz7)},
    }


def relabel(questions, is_error, unlabelled_are_errors):
    """Audited yardstick on the answered class of both partitions, bracketing the unlabelled."""
    out = copy.deepcopy(questions)
    missing = 0
    for q in out:
        for part in ("single", "multi"):
            cls = q[part]
            if not cls:
                continue
            c = cls[top_index(cls)]
            if not c["strong_ok"]:
                row = is_error.get((q["qid"], c["representative"]))
                if row is None:
                    missing += 1
                    if not unlabelled_are_errors:
                        c["strong_ok"] = True
                elif not row:
                    c["strong_ok"] = True
    return out, missing


def threshold_effect(fm, alpha, n_splits, seed0):
    """How many CRC thresholds and answer rates the tie rule actually moves.

    The measurement the corrected docstring rests on, rather than an assertion: every cell of
    every split is evaluated under both tie rules and the differences are counted.
    """
    n = collections.Counter()
    for tag in TAGS:
        for seed in SEEDS:
            for split in ("question", "database"):
                qs = json.load(open(path_of(tag, seed, split)))["questions"]
                pq, _ = patch(qs, tag, seed, fm)
                sp = make_splits([q["qid"] for q in qs], {q["qid"]: q["db"] for q in qs},
                                 split, n_splits, seed0)
                for part, cal in (("single", "single"), ("multi", "multi")):
                    a_ = cell_records(qs, part, cal)
                    b_ = cell_records(pq, part, cal)
                    for calq, tstq in sp:
                        calq = [q for q in calq if q in a_]
                        tstq = [q for q in tstq if q in a_]
                        if not calq or not tstq:
                            continue
                        n["evaluations"] += 1
                        ea = evaluate(a_, calq, tstq, alpha)
                        eb = evaluate(b_, calq, tstq, alpha)
                        for k, name in (("lambda", "lambda_changed"),
                                        ("tau", "tau_changed"),
                                        ("answer_rate", "answer_rate_changed")):
                            if ea[k] != eb[k]:
                                n[name] += 1
                    for qid in a_:
                        for k, name in (("top_mass", "top_mass_changed"),
                                        ("fit_mass", "fit_mass_changed"),
                                        ("strong_mass", "strong_mass_changed")):
                            if a_[qid][k] != b_[qid][k]:
                                n[name] += 1
    return dict(n)


def gap_repair(questions, splits, alpha, fit_from=None):
    """GAP inside cell A and REPAIR from cell A to cell D, on one pool.

    `fit_from` supplies the fitting labels, so cell D still fits on the labels it actually had
    while the risk is read against the audited ones. That is c7's splice, unchanged.
    """
    out = {}
    for cell, (part, cal) in (("A", ("single", "single")), ("D", ("multi", "multi"))):
        recs = cell_records(questions, part, cal)
        if fit_from is not None:
            base = cell_records(fit_from, part, cal)
            for qid in recs:
                recs[qid]["fit_ok"] = base[qid]["fit_ok"]
                recs[qid]["fit_mass"] = base[qid]["fit_mass"]
        agg = collections.defaultdict(list)
        for calq, tstq in splits:
            calq = [q for q in calq if q in recs]
            tstq = [q for q in tstq if q in recs]
            if not calq or not tstq:
                continue
            for k, v in evaluate(recs, calq, tstq, alpha).items():
                agg[k].append(v)
        out[cell] = agg
    gap = [s - f for f, s in zip(out["A"]["marginal_risk_fit"], out["A"]["marginal_risk_strong"])]
    rep = [d - a for a, d in zip(out["A"]["marginal_risk_strong"], out["D"]["marginal_risk_strong"])]
    return statistics.mean(gap), statistics.mean(rep)


def recompute(fm, alpha, n_splits, seed0, conventions):
    audit = {r["case_id"]: r for r in json.load(open("experiments/c7_semantic_audit.json"))["cases"]}
    cases = json.load(open("experiments/c7_repair_cases.json"))["cases"]
    err = {}
    for name in conventions:
        pred = CONVENTIONS[name]
        err[name] = {(c["qid"], c["rep"]): pred(audit[c["case_id"]]) for c in cases}

    rows = collections.defaultdict(lambda: collections.defaultdict(list))
    unlabelled = 0
    for tag in TAGS:
        for seed in SEEDS:
            for split in ("question", "database"):
                qs = json.load(open(path_of(tag, seed, split)))["questions"]
                pq, _ = patch(qs, tag, seed, fm)
                sp = make_splits([q["qid"] for q in qs], {q["qid"]: q["db"] for q in qs},
                                 split, n_splits, seed0)
                for label, src in (("file_order", qs), ("frozen", pq)):
                    g, r = gap_repair(src, sp, alpha)
                    rows[(tag, split)][f"preregistered|{label}|GAP"].append(g)
                    rows[(tag, split)][f"preregistered|{label}|REPAIR"].append(r)
                for name in conventions:
                    for label, src in (("file_order", qs), ("frozen", pq)):
                        for bracket in (True, False):
                            rel, miss = relabel(src, err[name], bracket)
                            if label == "frozen" and bracket:
                                unlabelled += miss
                            g, r = gap_repair(rel, sp, alpha, fit_from=src)
                            b = "errors" if bracket else "not_errors"
                            rows[(tag, split)][f"{name}|{label}|{b}|GAP"].append(g)
                            rows[(tag, split)][f"{name}|{label}|{b}|REPAIR"].append(r)
    out = {f"{t}|{s}": {k: statistics.mean(v) for k, v in sorted(d.items())}
           for (t, s), d in sorted(rows.items())}
    return ({k: {kk: round(vv, 4) for kk, vv in v.items()} for k, v in out.items()},
            unlabelled, impact_bounds(out))


def relabel_cell_a(questions, is_error, unlabelled_are_errors, population,
                   stress_questions=frozenset()):
    """c6_gap_audited.relabel, with the never-labelled answers bracketed.

    Only the answer of cell A is relabelled, as in the GAP ladder. `population` says which
    strong-wrong answers the census was meant to cover: an answer inside it that the census never
    labelled is bracketed both ways, one outside it stays an error, as c6_gap_audited leaves it.
    The stress test also counts as wrong every accepted answer on a question in
    `stress_questions`.
    """
    out = copy.deepcopy(questions)
    missing = 0
    for q in out:
        cls = q["single"]
        if not cls:
            continue
        c = cls[top_index(cls)]
        if not c["strong_ok"]:
            row = is_error.get((q["qid"], c["representative"]))
            if row is None:
                if population(c):
                    missing += 1
                    if not unlabelled_are_errors:
                        c["strong_ok"] = True
            elif not row:
                c["strong_ok"] = True
        elif q["qid"] in stress_questions:
            c["strong_ok"] = False
    return out, missing


def gap_ladder(fm, alpha, n_splits, seed0, conventions):
    """GAP under the disagreement census and under the reverse stress test, both tie rules.

    The disagreement census covers only the answers the shipped database accepts and the suite
    rejects; the stress test relabels with the full census and also counts as wrong every
    accepted answer on a question with a suspected defective reference, which is how
    c6_gap_audited.py builds c6_gap_audited.json and c7_gap_stress.json. The file-order values are
    checked against those two files before anything is compared with them.
    """
    from c6_gap_audited import defective_gold_questions
    censuses = {}
    for name, audit_path, cases_path, stored_path, stress, population in (
            ("disagreement", "experiments/c6_semantic_audit.json",
             "experiments/c6_semantic_cases.json", "experiments/c6_gap_audited.json", False,
             lambda c: c["weak_ok"]),
            ("stress", "experiments/c7_semantic_audit.json",
             "experiments/c7_repair_cases.json", "experiments/c7_gap_stress.json", True,
             lambda c: True)):
        audit = {r["case_id"]: r for r in json.load(open(audit_path))["cases"]}
        cases = {c["case_id"]: c for c in json.load(open(cases_path))["cases"]}
        censuses[name] = {
            "labels": {conv: {(cases[i]["qid"], cases[i]["rep"]): CONVENTIONS[conv](r)
                              for i, r in audit.items()} for conv in conventions},
            "stress": defective_gold_questions(audit, cases) if stress else frozenset(),
            "population": population,
            "stored": json.load(open(stored_path))["pools"]}

    rows = collections.defaultdict(lambda: collections.defaultdict(list))
    checked, mismatched, missing = 0, [], collections.Counter()
    for tag in TAGS:
        for seed in SEEDS:
            for split in ("question", "database"):
                qs = json.load(open(path_of(tag, seed, split)))["questions"]
                pq, _ = patch(qs, tag, seed, fm)
                sp = make_splits([q["qid"] for q in qs], {q["qid"]: q["db"] for q in qs},
                                 split, n_splits, seed0)
                pool = f"{tag}|seed{seed}|{split}"
                for name, c in censuses.items():
                    for conv in conventions:
                        for label, src in (("file_order", qs), ("frozen", pq)):
                            for bracket in (True, False):
                                rel, miss = relabel_cell_a(src, c["labels"][conv], bracket,
                                                           c["population"], c["stress"])
                                g, _ = gap_repair(rel, sp, alpha)
                                b = "errors" if bracket else "not_errors"
                                rows[(tag, split)][f"{name}|{conv}|{label}|{b}|GAP"].append(g)
                                if label == "file_order":
                                    checked += 1
                                    if round(g, 4) != c["stored"][pool][conv]["GAP"]:
                                        mismatched.append(f"{pool}|{name}|{conv}")
                                elif bracket:
                                    missing[name] += miss
    if mismatched:
        raise SystemExit(f"{len(mismatched)} file-order values do not reproduce the archived GAP "
                         f"ladder, first {mismatched[:3]}; nothing is compared with them")
    out = {f"{t}|{s}": {k: statistics.mean(v) for k, v in sorted(d.items())}
           for (t, s), d in sorted(rows.items())}
    return {
        "note": "three-seed means of GAP in fractions; keys are census|convention|tie rule|bracket. "
                "The file-order values reproduce c6_gap_audited.json and c7_gap_stress.json.",
        "file_order_values_checked": checked,
        "never_labelled_answers_encountered": dict(missing),
        "rows": {k: {kk: round(vv, 6) for kk, vv in v.items()} for k, v in out.items()},
        "impact_bounds": impact_bounds(out),
    }


def impact_bounds(out, keep=lambda key: True):
    """How far the frozen rule moves the three-seed means of `out`, over the keys `keep` admits.

    Taken on the unrounded means; rounding first would understate them. A key carries `file_order`
    or `frozen` and, under a census convention, the bracket; a cell is the key with both removed,
    so a cell that changes sign or crosses the three-point line under either bracket is counted
    once and named.
    """
    worst = bracket = 0.0
    signs, crossings = set(), {}
    for pool, row in out.items():
        for k, v in row.items():
            if not keep(k):
                continue
            if "|file_order|" in k:
                fz = k.replace("|file_order|", "|frozen|")
                if fz in row:
                    cell = f"{pool}|" + k.replace("|file_order|", "|").replace(
                        "|errors|", "|").replace("|not_errors|", "|")
                    worst = max(worst, abs(v - row[fz]))
                    if (v > 0) != (row[fz] > 0):
                        signs.add(cell)
                    if k.endswith("REPAIR") and (v <= -0.03) != (row[fz] <= -0.03):
                        b = ("errors" if "|errors|" in k else
                             "not_errors" if "|not_errors|" in k else "no_bracket")
                        crossings.setdefault(cell, {"file_order_points": round(100 * v, 4),
                                                    "frozen_points": {}})[
                            "frozen_points"][b] = round(100 * row[fz], 4)
            if "|frozen|errors|" in k:
                o = k.replace("|frozen|errors|", "|frozen|not_errors|")
                if o in row:
                    bracket = max(bracket, abs(v - row[o]))
    return {"largest_change_points": round(100 * worst, 6),
            "largest_bracket_width_points": round(100 * bracket, 6),
            "sign_changes": len(signs), "crossings_of_the_three_point_line": len(crossings),
            "crossing_cells": crossings}


class Bracketed(dict):
    """A census lookup that also answers for the answers the census never saw, one way or the
    other, and remembers which those were."""

    def __init__(self, labels, missing_is_error):
        super().__init__(labels)
        self.missing_is_error = missing_is_error
        self.missing = set()

    def get(self, key, default=None):
        if key in self:
            return self[key]
        self.missing.add(key)
        return self.missing_is_error


def score_gap_repair(c8, questions, lnlp, splits, alpha, is_error=None):
    """Unrounded GAP and REPAIR of every score on one pool, computed as c8_baselines.run_pool."""
    stats = {p: c8.question_stats(questions, lnlp, p, is_error) for p in ("single", "multi")}
    out = {}
    for score, (grid, _, _) in c8.SCORES.items():
        cells = {}
        for cell, (part, cal) in c8.CELLS.items():
            recs = c8.cell_records(stats[part], score, cal)
            agg = collections.defaultdict(list)
            for calq, tstq in splits:
                calq = [q for q in calq if q in recs]
                tstq = [q for q in tstq if q in recs]
                if not calq or not tstq:
                    continue
                for k, v in c8.evaluate(recs, calq, tstq, alpha, grid).items():
                    agg[k].append(v)
            cells[cell] = agg
        gap = [s - f for f, s in zip(cells["A"]["marginal_risk_fit"],
                                     cells["A"]["marginal_risk_strong"])]
        rep = [d - a for a, d in zip(cells["A"]["marginal_risk_strong"],
                                     cells["D"]["marginal_risk_strong"])]
        out[score] = (statistics.mean(gap), statistics.mean(rep))
    return out


def six_scores(fm, alpha, n_splits, seed0, conventions):
    """The six-score comparison under both tie rules, preregistered and under every convention.

    The census replaces the yardstick only, as c8_baselines applies it: each cell still fits its
    threshold on the labels it had. The answers the frozen rule returns and the census never saw
    are bracketed both ways, as in `recompute`. Before anything is compared with them, the
    file-order values are checked against the archived c8 results, rounded as those were written.
    """
    import c8_baselines as c8
    labels = {name: c8.load_audit("experiments/c7_repair_cases.json",
                                  "experiments/c7_semantic_audit.json", name)
              for name in conventions}
    archived = {"preregistered": json.load(open("experiments/c8_baselines.json"))["pools"]}
    for name in conventions:
        archived[name] = json.load(open(f"experiments/c8_baselines_audited_{name}.json"))["pools"]

    rows = collections.defaultdict(lambda: collections.defaultdict(list))
    unlabelled, checked, mismatched = set(), 0, []
    for tag in TAGS:
        for seed in SEEDS:
            for split in ("question", "database"):
                qs = json.load(open(path_of(tag, seed, split)))["questions"]
                pq, _ = patch(qs, tag, seed, fm)
                lnlp = c8.load_lnlp(tag, seed, {q["qid"] for q in qs})
                sp = make_splits([q["qid"] for q in qs], {q["qid"]: q["db"] for q in qs},
                                 split, n_splits, seed0)
                pool = f"{tag}|seed{seed}|{split}"
                runs = [("preregistered", qs, None, [("file_order", None)]),
                        ("preregistered", pq, None, [("frozen", None)])]
                for name in conventions:
                    runs.append((name, qs, labels[name],
                                 [("file_order", "errors"), ("file_order", "not_errors")]))
                    for missing_is_error, b in ((True, "errors"), (False, "not_errors")):
                        runs.append((name, pq, Bracketed(labels[name], missing_is_error),
                                     [("frozen", b)]))
                for variant, src, is_error, keys in runs:
                    res = score_gap_repair(c8, src, lnlp, sp, alpha, is_error)
                    if keys[0][0] == "file_order":
                        stored = archived[variant][pool]
                        for score, (g, r) in res.items():
                            checked += 2
                            for kind, v in (("GAP", g), ("REPAIR", r)):
                                if round(v, 4) != stored[score][kind]:
                                    mismatched.append(f"{pool}|{score}|{variant}|{kind}")
                    if isinstance(is_error, Bracketed):
                        unlabelled |= {(tag, seed) + k for k in is_error.missing}
                    for score, (g, r) in res.items():
                        for label, b in keys:
                            key = "|".join(x for x in (score, variant, label, b) if x)
                            rows[(tag, split)][key + "|GAP"].append(g)
                            rows[(tag, split)][key + "|REPAIR"].append(r)
    if mismatched:
        raise SystemExit(f"{len(mismatched)} file-order values do not reproduce the archived c8 "
                         f"results, first {mismatched[:3]}; nothing is compared with them")
    out = {f"{t}|{s}": {k: statistics.mean(v) for k, v in sorted(d.items())}
           for (t, s), d in sorted(rows.items())}
    return {
        "note": "three-seed means in fractions; keys are score|labels|tie rule[|bracket]|quantity. "
                "The file-order values reproduce the archived c8 results.",
        "file_order_values_checked": checked,
        "never_labelled_answers": len({(t, s, q, r) for t, s, q, r in unlabelled}),
        "rows": {k: {kk: round(vv, 6) for kk, vv in v.items()} for k, v in out.items()},
        "impact_bounds": impact_bounds(out),
        "impact_bounds_top_class_mass": impact_bounds(
            out, keep=lambda k: k.startswith("top_class_mass|")),
        "impact_bounds_other_scores": impact_bounds(
            out, keep=lambda k: not k.startswith("top_class_mass|")),
    }



def write_result(path, result, replace=False):
    """Write the artifact, refusing to silently drop a section a previous run had produced.

    Every analysis here is opt-in behind a flag and they all write the same file, so running the
    script with fewer flags overwrites a complete artifact with a partial one and nothing says so.
    That happened once and the truncated file was committed. The guard is not merge-on-write, which
    would leave stale sections behind a fresh run; it refuses and names the flags that are missing.
    """
    if os.path.isfile(path) and not replace:
        try:
            old = json.load(open(path))
        except Exception:
            old = {}
        lost = [k for k, v in old.items()
                if v not in (None, {}, []) and result.get(k) in (None, {}, [])]
        if lost:
            raise SystemExit(
                f"{path} already carries {', '.join(lost)} and this run did not produce them. "
                f"Rerun with the flags that build those sections, or pass --replace to write a "
                f"deliberately smaller artifact.")
    json.dump(result, open(path, "w"), indent=1, ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--enumerate", action="store_true")
    ap.add_argument("--populations", action="store_true")
    ap.add_argument("--recompute", action="store_true")
    ap.add_argument("--six-scores", action="store_true")
    ap.add_argument("--gap-ladder", action="store_true")
    ap.add_argument("--alpha", type=float, default=0.1)
    ap.add_argument("--splits", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260903)
    ap.add_argument("--conventions", nargs="*", default=["wide", "narrow", "agreed", "unanimous"])
    ap.add_argument("--replace", action="store_true",
                    help="allow this run to write a smaller artifact than the one on disk")
    ap.add_argument("--out", default="experiments/c9_tie_audit.json")
    a = ap.parse_args()
    result = {"alpha": a.alpha, "splits": a.splits,
              "note": "the tie rule the per-question files force on every recomputation, against "
                      "the frozen analyser's own choice. Ties are the only decisions that can "
                      "differ, so this bounds the whole effect."}

    if a.enumerate:
        n, tied = enumerate_ties()
        json.dump({"note": "every top-class decision of cells A and D over the twelve pools whose "
                           "maximum class count is attained by more than one class",
                   "decisions_examined": n, "tied": tied},
                  open("experiments/c9_tied_decisions.json", "w"), indent=1)
        print(f"{n} top-class decisions, {len(tied)} tied "
              f"({len({(x['tag'], x['seed'], x['qid']) for x in tied})} distinct pool-questions)")
        result["tied"] = {"decisions_examined": n, "tied": len(tied)}

    fm = frozen_map()
    changed = sum(1 for x in fm.values() if not x["same_rep"])
    lab = sum(1 for x in fm.values() if not x["same_labels"])
    result["reconstruction"] = {"tied_decisions": len(fm), "representative_differs": changed,
                                "correctness_label_differs": lab}
    print(f"reconstruction: {len(fm)} tied decisions, {changed} pick a different answer, "
          f"{lab} of those change a correctness label")

    if a.populations:
        p = populations(fm)
        result["populations"] = p
        for k in ("c6", "c7"):
            d = p[k]
            print(f"\n{k}: population {d['stored_answers']} answers as audited, "
                  f"{d['frozen_answers']} under the frozen choice")
            print(f"  distinct cases {d['cases_labelled']} labelled, {d['cases_under_frozen']} "
                  f"under the frozen choice")
            print(f"  never labelled but should have been: {len(d['never_labelled'])}")
            print(f"  labelled but not in the frozen population: "
                  f"{d['labelled_but_not_in_population']}")

    if a.recompute:
        rows, miss, bounds = recompute(fm, a.alpha, a.splits, a.seed, a.conventions)
        result["recompute"] = rows
        result["unlabelled_answers_encountered"] = miss
        result["impact_bounds"] = bounds
        result["threshold_effect"] = threshold_effect(fm, a.alpha, a.splits, a.seed)
        print(f"\nGAP and REPAIR in points, three-seed means, alpha = {a.alpha}. "
              f"`frozen` uses the analyser's own tie rule.")
        print(f"The two brackets treat the never-labelled answers as errors and as not errors.\n")
        for split in ("question", "database"):
            print(f"  {split} splits")
            for kind in ("GAP", "REPAIR"):
                print(f"    {kind}")
                hdr = ["preregistered"] + [f"{c} {b}" for c in a.conventions
                                           for b in ("errors", "not_errors")]
                print(f"      {'checkpoint':20s}" + "".join(f"{h:>22s}" for h in hdr))
                for tag in TAGS:
                    r = rows[f"{tag}|{split}"]
                    cells = [f"{100 * r[f'preregistered|file_order|{kind}']:+7.2f} -> "
                             f"{100 * r[f'preregistered|frozen|{kind}']:+7.2f}"]
                    for c in a.conventions:
                        for b in ("errors", "not_errors"):
                            cells.append(f"{100 * r[f'{c}|file_order|{b}|{kind}']:+7.2f} -> "
                                         f"{100 * r[f'{c}|frozen|{b}|{kind}']:+7.2f}")
                    print(f"      {tag:20s}" + "".join(f"{c:>22s}" for c in cells))

    if a.six_scores:
        s = six_scores(fm, a.alpha, a.splits, a.seed, a.conventions)
        result["six_scores"] = s
        for name, b in (("all six scores", s["impact_bounds"]),
                        ("top-class mass alone", s["impact_bounds_top_class_mass"])):
            print(f"\nsix-score comparison, {name}, preregistered and {', '.join(a.conventions)}:")
            print(f"  largest change {b['largest_change_points']:.4f} points, largest bracket width "
                  f"{b['largest_bracket_width_points']:.4f}, sign changes {b['sign_changes']}, "
                  f"crossings of the 3-point line {b['crossings_of_the_three_point_line']}")
            for cell, v in b["crossing_cells"].items():
                print(f"    {cell}: {v}")
        print(f"  file-order values checked against the archived c8 results: "
              f"{s['file_order_values_checked']}, never-labelled answers {s['never_labelled_answers']}")

    if a.gap_ladder:
        g = gap_ladder(fm, a.alpha, a.splits, a.seed, a.conventions)
        result["gap_ladder"] = g
        b = g["impact_bounds"]
        print(f"\nGAP ladder, disagreement census and reverse stress test, {', '.join(a.conventions)}:")
        print(f"  largest change {b['largest_change_points']:.4f} points, largest bracket width "
              f"{b['largest_bracket_width_points']:.4f}, sign changes {b['sign_changes']}")
        print(f"  file-order values checked against the archived ladder: "
              f"{g['file_order_values_checked']}, never-labelled answers "
              f"{g['never_labelled_answers_encountered']}")

    if "impact_bounds" in result:
        b = result["impact_bounds"]
        t = result["threshold_effect"]
        print(f"\n  largest change from the frozen tie rule: {b['largest_change_points']:.4f} points")
        print(f"  largest bracket width for the unlabelled: "
              f"{b['largest_bracket_width_points']:.4f} points")
        print(f"  sign changes: {b['sign_changes']}, "
              f"crossings of the 3-point line: {b['crossings_of_the_three_point_line']}")
        print(f"  what the tie rule moves, over {t['evaluations']} split-cell evaluations: "
              f"lambda {t.get('lambda_changed', 0)}, answer rate "
              f"{t.get('answer_rate_changed', 0)}, tau {t.get('tau_changed', 0)}; "
              f"masses unchanged: top {t.get('top_mass_changed', 0)}, "
              f"fit {t.get('fit_mass_changed', 0)}, strong {t.get('strong_mass_changed', 0)}")

    write_result(a.out, result, a.replace)
    print(f"\nwritten {a.out}")


if __name__ == "__main__":
    main()
