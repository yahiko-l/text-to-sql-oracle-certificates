#!/usr/bin/env python3
"""Post-hoc re-analysis of the Preregistration 3 pools from their per-question sufficient statistics.

The analyser writes, per question, every execution-equivalence class with its sample count and its
correctness under both oracles. That is everything the certificate needs, so the 2x2 cells can be
recomputed for other operating points and other resampling schemes without re-executing any SQL.
This script answers the questions the preregistered analysis did not: how the effect behaves across
alpha, how much of it survives when a single database is removed, how wide a database-clustered
interval is, and whether the top-class tie rule or the mass denominator matters.

Everything here is POST HOC. The preregistered result stays what experiments/c4_panel_summary.json
says; these are sensitivity and characterisation analyses added after it.

  --verify        reproduce the stored alpha = 0.1 numbers and print the differences
  --alphas        risk-coverage curve over an alpha grid, both split schemes
  --per-db        per-database and leave-one-database-out tables at the preregistered alpha
  --bootstrap N   database-clustered bootstrap spread for the question-split estimand
  --tie-break     top-class tie rule: first (per-question file order), last, or random
"""
import argparse, collections, json, math, os, random, statistics, sys

GRID = [round(x, 4) for x in [i / 200 for i in range(0, 201)]]


def conformal_quantile(scores, alpha):
    n = len(scores)
    if n == 0:
        return 1.0
    k = math.ceil((n + 1) * (1 - alpha))
    return 1.0 if k > n else sorted(scores)[k - 1]


def crc_lambda(items, alpha):
    n = len(items)
    if n == 0:
        return 1.0 + 1e-9
    for lam in GRID:
        r = sum(1 for m, w in items if m >= lam and w) / n
        if (n / (n + 1)) * r + 1 / (n + 1) <= alpha:
            return lam
    return 1.0 + 1e-9


def load(stem):
    """questions -> {qid, db, n_total, n_usable, single: [classes], multi: [classes]}"""
    return json.load(open(stem))["questions"]


def cell_records(questions, scoring, cal_label, denominator="usable", tie="first", rng=None):
    """One record per question for one 2x2 cell, matching e0_analyse.cell_records.

    The per-question file sorts classes by descending count, so index 0 is the top class under
    every tie rule that breaks ties by file order. The analyser breaks ties by an internal class
    key that the file does not carry, so `tie` exposes the choice instead of pretending it is
    determined: `first` takes the earliest listed, `last` the latest among the tied, `random` one
    of them at random.
    """
    recs = {}
    for q in questions:
        cls = q[scoring]
        n = q["n_total"] if denominator == "budget" else sum(c["count"] for c in cls)
        if n == 0:
            continue
        masses = [c["count"] / n for c in cls]
        best = max(masses)
        tied = [i for i, m in enumerate(masses) if m == best]
        i = tied[0] if tie == "first" else tied[-1] if tie == "last" else rng.choice(tied)
        top = cls[i]
        ok_key = "weak_ok" if cal_label == "single" else "strong_ok"
        fit_c = [m for c, m in zip(cls, masses) if c[ok_key]]
        strong_c = [m for c, m in zip(cls, masses) if c["strong_ok"]]
        recs[q["qid"]] = {"db": q["db"], "top_mass": masses[i],
                          "fit_ok": top[ok_key], "strong_ok": top["strong_ok"],
                          "fit_mass": max(fit_c) if fit_c else None,
                          "strong_mass": max(strong_c) if strong_c else None,
                          "masses": sorted(masses, reverse=True)}
    return recs


def evaluate(recs, calq, tstq, alpha):
    """The two certificates on one calibration/test split."""
    s_cal = [1.0 if recs[i]["fit_mass"] is None else 1.0 - recs[i]["fit_mass"] for i in calq]
    tau = conformal_quantile(s_cal, alpha)
    lam = crc_lambda([(recs[i]["top_mass"], not recs[i]["fit_ok"]) for i in calq], alpha)
    ans = [i for i in tstq if recs[i]["top_mass"] >= lam]
    n = len(tstq)
    return {
        "tau": tau, "lambda": lam,
        "setcov_strong": sum(1 for i in tstq if recs[i]["strong_mass"] is not None
                             and recs[i]["strong_mass"] >= 1.0 - tau) / n,
        "setcov_fit": sum(1 for i in tstq if recs[i]["fit_mass"] is not None
                          and recs[i]["fit_mass"] >= 1.0 - tau) / n,
        "answer_rate": len(ans) / n,
        "marginal_risk_strong": sum(1 for i in ans if not recs[i]["strong_ok"]) / n,
        "marginal_risk_fit": sum(1 for i in ans if not recs[i]["fit_ok"]) / n,
        "selective_risk_strong": (sum(1 for i in ans if not recs[i]["strong_ok"]) / len(ans)) if ans else None,
    }


def make_splits(qids, dbs_of, how, n_splits, seed):
    """Reproduces e0_analyse's split draws exactly for how in {question, database}."""
    rng = random.Random(seed)
    out = []
    if how == "question":
        for _ in range(n_splits):
            sh = list(qids); rng.shuffle(sh); half = len(sh) // 2
            out.append((sh[:half], sh[half:]))
    else:
        groups = sorted({dbs_of[q] for q in qids})
        for _ in range(n_splits):
            sh = list(groups); rng.shuffle(sh); half = len(sh) // 2
            cal = set(sh[:half])
            out.append(([q for q in qids if dbs_of[q] in cal],
                        [q for q in qids if dbs_of[q] not in cal]))
    return out


def cells_over_splits(questions, splits, alpha, denominator="usable", tie="first", rng=None):
    """All four cells on one shared set of splits, plus the paired contrasts."""
    out, per_split = {}, {}
    for scoring in ("single", "multi"):
        for cal in ("single", "multi"):
            recs = cell_records(questions, scoring, cal, denominator, tie, rng)
            agg = collections.defaultdict(list)
            for calq, tstq in splits:
                if not calq or not tstq:
                    continue
                for k, v in evaluate(recs, calq, tstq, alpha).items():
                    agg[k].append(v)
            key = f"score={scoring}|calib={cal}"
            per_split[key] = agg
            out[key] = {k: (round(statistics.mean([x for x in v if x is not None]), 4)
                            if any(x is not None for x in v) else None) for k, v in agg.items()}
    A = "score=single|calib=single"
    gap = [b - a_ for a_, b in zip(per_split[A]["marginal_risk_fit"], per_split[A]["marginal_risk_strong"])]
    out["GAP"] = round(statistics.mean(gap), 4) if gap else None
    out["GAP_positive_splits"] = round(sum(1 for g in gap if g > 0) / len(gap), 4) if gap else None
    for other, name in (("score=multi|calib=multi", "REPAIR"), ("score=single|calib=multi", "REPAIR_labels_only"),
                        ("score=multi|calib=single", "REPAIR_partition_only")):
        d = [y - x for x, y in zip(per_split[A]["marginal_risk_strong"], per_split[other]["marginal_risk_strong"])]
        out[name] = round(statistics.mean(d), 4) if d else None
        da = [y - x for x, y in zip(per_split[A]["answer_rate"], per_split[other]["answer_rate"])]
        out[name + "_answer_rate"] = round(statistics.mean(da), 4) if da else None
    return out


TAGS = ("kwai-autosql-32b", "kwai-autosql-14b", "xiyansql-32b", "omnisql-32b")
SEEDS = (101, 202, 303)


def pool_files(tag, seed, split):
    suffix = "_official_per_question.json" if split == "question" else "_official_dbsplit_per_question.json"
    return f"experiments/c4_{tag}_seed{seed}_results{suffix}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tags", nargs="*", default=list(TAGS))
    ap.add_argument("--alpha", type=float, default=0.1)
    ap.add_argument("--splits", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260903)
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--alphas", nargs="*", type=float, default=None)
    ap.add_argument("--per-db", action="store_true")
    ap.add_argument("--bootstrap", type=int, default=0)
    ap.add_argument("--pareto", action="store_true",
                    help="cell B against cell D under a common empirical marginal-risk ceiling, "
                         "over every reachable threshold including abstain-everything")
    ap.add_argument("--tie-break", choices=("first", "last", "random"), default="first")
    ap.add_argument("--denominator", choices=("usable", "budget"), default="usable")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    rng = random.Random(a.seed)
    result = {"note": "post-hoc re-analysis from per-question sufficient statistics; the preregistered "
                      "result is experiments/c4_panel_summary.json",
              "options": vars(a)}

    if a.verify:
        rows = []
        for tag in a.tags:
            for seed in SEEDS:
                for how in ("question", "database"):
                    qs = load(pool_files(tag, seed, how))
                    ids = [q["qid"] for q in qs]; dbs = {q["qid"]: q["db"] for q in qs}
                    sp = make_splits(ids, dbs, how, a.splits, a.seed)
                    c = cells_over_splits(qs, sp, a.alpha, a.denominator, a.tie_break, rng)
                    stem = pool_files(tag, seed, how).replace("_per_question.json", ".json")
                    st = json.load(open(stem))
                    ref_gap = st["oracle_gap_within_cell_A"]["marginal_risk_strong_minus_fit"]["mean"]
                    ref_rep = st["paired_contrasts_vs_cell_A"]["score=multi|calib=multi"]["marginal_risk_strong"]["mean_change_vs_A"]
                    rows.append({"tag": tag, "seed": seed, "split": how,
                                 "GAP": c["GAP"], "GAP_stored": ref_gap, "dGAP": round(c["GAP"] - ref_gap, 5),
                                 "REPAIR": c["REPAIR"], "REPAIR_stored": ref_rep, "dREPAIR": round(c["REPAIR"] - ref_rep, 5)})
                    print(f"{tag:>18} s{seed} {how:<9} GAP {c['GAP']:+.4f} (stored {ref_gap:+.4f}, d {rows[-1]['dGAP']:+.5f})  "
                          f"REPAIR {c['REPAIR']:+.4f} (stored {ref_rep:+.4f}, d {rows[-1]['dREPAIR']:+.5f})")
        worst = max(abs(r["dGAP"]) for r in rows), max(abs(r["dREPAIR"]) for r in rows)
        print(f"\nlargest |difference| vs stored: GAP {worst[0]:.5f}  REPAIR {worst[1]:.5f}  over {len(rows)} pool-splits")
        result["verify"] = {"rows": rows, "max_abs_diff_gap": worst[0], "max_abs_diff_repair": worst[1]}

    if a.alphas:
        curve = {}
        for tag in a.tags:
            for how in ("question", "database"):
                for alpha in a.alphas:
                    vals = collections.defaultdict(list)
                    for seed in SEEDS:
                        qs = load(pool_files(tag, seed, how))
                        ids = [q["qid"] for q in qs]; dbs = {q["qid"]: q["db"] for q in qs}
                        sp = make_splits(ids, dbs, how, a.splits, a.seed)
                        c = cells_over_splits(qs, sp, alpha, a.denominator, a.tie_break, rng)
                        for k in ("GAP", "REPAIR", "REPAIR_labels_only", "REPAIR_partition_only",
                                  "REPAIR_answer_rate", "REPAIR_labels_only_answer_rate", "REPAIR_partition_only_answer_rate"):
                            vals[k].append(c[k])
                        vals["A_risk_fit"].append(c["score=single|calib=single"]["marginal_risk_fit"])
                        vals["A_risk_strong"].append(c["score=single|calib=single"]["marginal_risk_strong"])
                        vals["A_answer_rate"].append(c["score=single|calib=single"]["answer_rate"])
                        vals["D_risk_strong"].append(c["score=multi|calib=multi"]["marginal_risk_strong"])
                        vals["D_answer_rate"].append(c["score=multi|calib=multi"]["answer_rate"])
                        vals["B_answer_rate"].append(c["score=single|calib=multi"]["answer_rate"])
                        vals["B_risk_strong"].append(c["score=single|calib=multi"]["marginal_risk_strong"])
                    curve[f"{tag}|{how}|alpha={alpha}"] = {k: round(statistics.mean([x for x in v if x is not None]), 4)
                                                           for k, v in vals.items() if any(x is not None for x in v)}
                    r = curve[f"{tag}|{how}|alpha={alpha}"]
                    print(f"{tag:>18} {how:<9} a={alpha:<5} GAP {r['GAP']:+.4f}  REPAIR {r['REPAIR']:+.4f}  "
                          f"A risk {r['A_risk_strong']:.4f}->D {r['D_risk_strong']:.4f}  ans A {r['A_answer_rate']:.3f} "
                          f"B {r['B_answer_rate']:.3f} D {r['D_answer_rate']:.3f}")
        result["alpha_curve"] = curve

    if a.per_db or a.bootstrap:
        per_db, lodo, boot = {}, {}, {}
        for tag in a.tags:
            qs_by_seed = {s: load(pool_files(tag, s, "question")) for s in SEEDS}
            dbs = sorted({q["db"] for q in qs_by_seed[SEEDS[0]]})
            if a.per_db:
                # one database at a time: the whole database is the test set, everything else calibrates
                for db in dbs:
                    g, r_ = [], []
                    for s in SEEDS:
                        qs = qs_by_seed[s]
                        ids = [q["qid"] for q in qs]; d = {q["qid"]: q["db"] for q in qs}
                        cal = [i for i in ids if d[i] != db]; tst = [i for i in ids if d[i] == db]
                        c = cells_over_splits(qs, [(cal, tst)], a.alpha, a.denominator, a.tie_break, rng)
                        g.append(c["GAP"]); r_.append(c["REPAIR"])
                    per_db[f"{tag}|{db}"] = {"n_questions": sum(1 for q in qs_by_seed[SEEDS[0]] if q["db"] == db),
                                             "GAP": round(statistics.mean(g), 4), "REPAIR": round(statistics.mean(r_), 4)}
                # leave one database out of the whole analysis, then the preregistered question splits
                for db in ["<none>"] + dbs:
                    g, r_ = [], []
                    for s in SEEDS:
                        qs = [q for q in qs_by_seed[s] if q["db"] != db]
                        ids = [q["qid"] for q in qs]; d = {q["qid"]: q["db"] for q in qs}
                        sp = make_splits(ids, d, "question", a.splits, a.seed)
                        c = cells_over_splits(qs, sp, a.alpha, a.denominator, a.tie_break, rng)
                        g.append(c["GAP"]); r_.append(c["REPAIR"])
                    lodo[f"{tag}|drop={db}"] = {"GAP": round(statistics.mean(g), 4), "REPAIR": round(statistics.mean(r_), 4)}
                for k, v in sorted(per_db.items()):
                    if k.startswith(tag):
                        print(f"per-db  {k:<40} n={v['n_questions']:<4} GAP {v['GAP']:+.4f} REPAIR {v['REPAIR']:+.4f}")
                base = lodo[f"{tag}|drop=<none>"]
                worst = max((v for k, v in lodo.items() if k.startswith(tag) and "drop=<none>" not in k),
                            key=lambda v: -v["GAP"])
                print(f"LODO    {tag}: full GAP {base['GAP']:+.4f} REPAIR {base['REPAIR']:+.4f}; "
                      f"worst drop GAP {worst['GAP']:+.4f} REPAIR {worst['REPAIR']:+.4f}")
            if a.bootstrap:
                # Schema-cluster bootstrap for the QUESTION-SPLIT estimand only. Schemas are drawn
                # with replacement and the preregistered question-level split procedure is then run
                # on the resampled question set, unchanged. This is deliberately NOT applied to the
                # database-heldout estimand: duplicated copies of one schema would land on both
                # sides of a schema-disjoint split and destroy the property that defines it. The
                # fraction of resamples on one side of zero is a resampling spread, not a p-value
                # and not a confidence level.
                stats_g, stats_r = [], []
                for b in range(a.bootstrap):
                    draw = [rng.choice(dbs) for _ in dbs]
                    g, r_ = [], []
                    for s in SEEDS:
                        qs = []
                        for j, db in enumerate(draw):
                            for q in qs_by_seed[s]:
                                if q["db"] == db:
                                    qq = dict(q); qq["qid"] = (j, q["qid"]); qq["db"] = (j, db)
                                    qs.append(qq)
                        ids = [q["qid"] for q in qs]; d = {q["qid"]: q["db"] for q in qs}
                        sp = make_splits(ids, d, "question", 20, a.seed + b)
                        c = cells_over_splits(qs, sp, a.alpha, a.denominator, a.tie_break, rng)
                        g.append(c["GAP"]); r_.append(c["REPAIR"])
                    stats_g.append(statistics.mean(g)); stats_r.append(statistics.mean(r_))
                stats_g.sort(); stats_r.sort()
                lo, hi = int(0.025 * len(stats_g)), int(0.975 * len(stats_g)) - 1
                boot[tag] = {"estimand": "question-level half-splits", "n_boot": a.bootstrap,
                             "GAP_mean": round(statistics.mean(stats_g), 4),
                             "GAP_interval95": [round(stats_g[lo], 4), round(stats_g[hi], 4)],
                             "REPAIR_mean": round(statistics.mean(stats_r), 4),
                             "REPAIR_interval95": [round(stats_r[lo], 4), round(stats_r[hi], 4)],
                             "GAP_positive_fraction": round(sum(1 for x in stats_g if x > 0) / len(stats_g), 4),
                             "REPAIR_negative_fraction": round(sum(1 for x in stats_r if x < 0) / len(stats_r), 4),
                             "note": "resampling spread over schemas, not a confidence level or a significance test"}
                print(f"boot    {tag}: GAP {boot[tag]['GAP_mean']:+.4f} spread {boot[tag]['GAP_interval95']} "
                      f"(positive in {boot[tag]['GAP_positive_fraction']:.1%}); REPAIR {boot[tag]['REPAIR_mean']:+.4f} "
                      f"spread {boot[tag]['REPAIR_interval95']} (negative in {boot[tag]['REPAIR_negative_fraction']:.1%})")
        result.update({"per_database": per_db, "leave_one_database_out": lodo,
                       "schema_cluster_bootstrap_question_split": boot})

    if a.pareto:
        # Cell B (weak partition, strong labels) against cell D (strong partition, strong labels)
        # under a COMMON EMPIRICAL MARGINAL-RISK CEILING, computed on the whole question set.
        #
        # Two things this is not. It is not a matched actual risk: both cells satisfy the same
        # ceiling, but the risk they actually incur at their best threshold differs. And it is not
        # a held-out certificate guarantee: the frontier is fitted and read on the same questions,
        # so it describes the reachable operating points, not a calibrated promise.
        #
        # The thresholds are the distinct top-class masses themselves plus the abstain-everything
        # point, so every operating point the rule can reach is enumerated. Abstaining on
        # everything reaches risk 0 at answer rate 0, so every non-negative ceiling is feasible
        # for both cells; an earlier version dropped a budget when one cell had no interior
        # solution, which wrongly made the strict budgets look unreachable.
        def staircase(pts, n):
            """The corners of a cell's frontier as [wrong answers, answers] out of n questions: each
            operating point that answers more than every point at no higher risk. Under any ceiling the
            highest answer rate is that of the last corner at or below it, so these draw the frontier at
            every ceiling; counts keep the corners exact."""
            corners, best = [], -1.0
            for ans, risk, _ in sorted(pts, key=lambda p: (p[1], -p[0])):
                if ans > best:
                    corners.append([round(risk * n), round(ans * n)])
                    best = ans
            return corners

        par = {}
        for tag in a.tags:
            rows, stairs = [], {}
            for s in SEEDS:
                qs = load(pool_files(tag, s, "question"))
                recB = cell_records(qs, "single", "multi", a.denominator, a.tie_break, rng)
                recD = cell_records(qs, "multi", "multi", a.denominator, a.tie_break, rng)
                ids = list(recB)

                def frontier(rec):
                    pts = [(0.0, 0.0, None)]                 # abstain on everything
                    for lam in sorted({rec[i]["top_mass"] for i in ids}):
                        ans = [i for i in ids if rec[i]["top_mass"] >= lam]
                        pts.append((len(ans) / len(ids),
                                    sum(1 for i in ans if not rec[i]["strong_ok"]) / len(ids), lam))
                    return pts

                cB, cD = frontier(recB), frontier(recD)
                stairs[str(s)] = {"n": len(ids), "B": staircase(cB, len(ids)), "D": staircase(cD, len(ids))}
                for target in (0.025, 0.05, 0.075, 0.10, 0.125, 0.15):
                    fb = max((x for x in cB if x[1] <= target), key=lambda x: x[0])
                    fd = max((x for x in cD if x[1] <= target), key=lambda x: x[0])
                    rows.append({"seed": s, "risk_ceiling": target,
                                 "B_answer_rate": round(fb[0], 4), "B_risk": round(fb[1], 4),
                                 "D_answer_rate": round(fd[0], 4), "D_risk": round(fd[1], 4),
                                 "D_minus_B_answer_rate": round(fd[0] - fb[0], 4)})
            agg = collections.defaultdict(list)
            for r in rows:
                agg[r["risk_ceiling"]].append(r["D_minus_B_answer_rate"])
            par[tag] = {"rows": rows,
                        "mean_D_minus_B_answer_rate_by_ceiling": {k: round(statistics.mean(v), 4) for k, v in sorted(agg.items())},
                        "staircase_by_seed": stairs}
            print(f"pareto  {tag:>18}  D minus B answer rate under a common empirical risk ceiling: "
                  + "  ".join(f"{k:.3f}->{v:+.4f}" for k, v in par[tag]["mean_D_minus_B_answer_rate_by_ceiling"].items()))
        result["frontier_B_vs_D_common_risk_ceiling"] = par

    if a.out:
        json.dump(result, open(a.out, "w"), indent=1, ensure_ascii=False)
        print("wrote", a.out)


if __name__ == "__main__":
    main()
