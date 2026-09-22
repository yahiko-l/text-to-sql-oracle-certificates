#!/usr/bin/env python3
"""Published UQ baselines under the same oracle intervention.

With only the top-class-mass score measured, every statement this project makes would be
scoped to "this top-class-mass plus CRC pipeline". If the oracle gap is a property of
execution-consistency uncertainty quantification, it has to appear for the published scores
too, and if it is a property of our particular score, that is a much smaller finding. This
script settles which, by holding the certificate, the pools, the splits, the alpha and the 2x2
fixed and varying ONLY the confidence score.

Six scores, five of them published elsewhere. Each is reimplemented here from its paper's
definition; no author code was run. Two of them need the equivalence relation, which in this
setting is execution equivalence, and that instantiation is the standard one in text-to-SQL and
is itself the assumption under test.

  top_class_mass          the frozen pipeline's own score, self-consistency confidence
                          (Wang et al., Self-Consistency Improves Chain of Thought Reasoning,
                          ICLR 2023). Included as a reproduction control, not as a baseline.
  discrete_semantic_entropy
                          negative discrete semantic entropy over the equivalence classes
                          (Kuhn et al., Semantic Uncertainty, ICLR 2023; the discrete estimator
                          of Farquhar et al., Detecting hallucinations in large language models
                          using semantic entropy, Nature 2024). H = -sum_c p_c log p_c with
                          p_c the class frequency; confidence is -H.
  lin_deg                 Lin, Trivedi and Sun, Generating with Confidence, TMLR 2024, their
                          degree-matrix uncertainty U_Deg = trace(mI - D)/m^2, where D is the
                          DEGREE matrix of the agreement graph, not the agreement matrix itself.
                          With W the 0/1 execution-agreement matrix, which is block diagonal, the
                          degree of a sample is the size of its class, so trace(D) = sum_c n_c^2
                          and U_Deg = 1 - sum_c (n_c/m)^2 exactly. Confidence is sum_c (n_c/m)^2.
                          (Writing W for D there gives trace(mI - W)/m^2 = 1 - 1/m, a constant,
                          which is not the measure and not what this implements.)
  lin_numsets             same paper, U_NumSet, the number of semantic sets. Confidence is -C.
                          Their U_EigV is sum_k max(0, 1 - lambda_k) over the normalised Laplacian
                          spectrum; for a block-diagonal 0/1 W that spectrum is one zero per block
                          and ones elsewhere, so U_EigV = C = U_NumSet. Their Eccentricity reduces
                          on the same matrix to sqrt(C - 1), so it ranks identically to U_NumSet.
                          Neither is reported separately: both would be the same column under
                          another name. Both reductions are checked numerically, not asserted.
  mean_seq_logprob        length-normalised Monte-Carlo predictive entropy (Malinin and Gales,
                          Uncertainty Estimation in Autoregressive Structured Prediction,
                          ICLR 2021). Confidence is the mean over usable candidates of
                          cum_logprob / n_tokens.
  max_seq_logprob         maximum length-normalised sequence log-probability, the single most
                          likely sample's score. The other standard likelihood baseline.

The two likelihood scores are the control that makes the comparison mean something: they do not
read the oracle at all, so under the intervention their score is fixed and only the labels move.
A gap they still show therefore establishes that a score's access to the weak oracle is NOT
NECESSARY for the under-reporting. It does not decompose the gap: the gap is the share of
questions that are both answered and oracle-disagreements, a joint quantity of the labels and the
answered set, and the scores answer different questions at different rates. Sufficiency only.

The answer rule is held fixed across every score: the system returns the representative of the
top-mass class of the cell's partition, exactly as the frozen pipeline does. Only the decision
of WHETHER to answer changes. Otherwise a score change and an answer change would be confounded
and no comparison would be possible.

Reported for each score: GAP, REPAIR, answer rate, and the AUROC of the score for predicting the
returned answer's correctness under each oracle. The AUROC pair is how the UQ papers above
evaluate their own scores, so it says whether the weak oracle also flatters the published
methods, not only the certificate.
"""
import argparse, bisect, collections, hashlib, json, math, os, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c4_recompute import make_splits, TAGS, SEEDS  # noqa: E402
import c4_recompute  # noqa: E402

INF = float("inf")
UNIT_GRID = [round(i / 200, 4) for i in range(201)]                     # the frozen grid
ENT_GRID = [-math.log(50) + i * math.log(50) / 200 for i in range(201)]  # -H, H in [0, log 50]
SET_GRID = [float(-k) for k in range(50, 0, -1)]                        # -C, C in 1..50
# Length-normalised log-probability. The range is [-8, 0]; the resolution is 0.001 because these
# models' per-token scores occupy only about the top 0.7 of that range, and a grid as coarse as
# the unit grid would hand the likelihood baselines a few dozen operating points against the
# control's two hundred. The grid is fixed globally and never adapted to a split or to the
# calibration data; it is not preregistered, and this resolution replaced a coarser one after the
# coarse grid was seen to be setting the likelihood scores' operating points. LP_STEPS records it
# so a reader can vary it.
LP_LO, LP_STEPS = -8.0, 8000
LP_GRID = [-INF] + [LP_LO + i * (-LP_LO) / LP_STEPS for i in range(LP_STEPS + 1)]


def entropy(masses):
    return -sum(p * math.log(p) for p in masses if p > 0)


# name -> (grid, confidence function, whether it reads the equivalence classes)
SCORES = {
    "top_class_mass":            (UNIT_GRID, lambda st: st["masses"][st["top"]], True),
    "discrete_semantic_entropy": (ENT_GRID, lambda st: -entropy(st["masses"]), True),
    "lin_deg":                   (UNIT_GRID, lambda st: sum(p * p for p in st["masses"]), True),
    "lin_numsets":               (SET_GRID, lambda st: -float(len(st["masses"])), True),
    "mean_seq_logprob":          (LP_GRID, lambda st: st["mean_lnlp"], False),
    "max_seq_logprob":           (LP_GRID, lambda st: st["max_lnlp"], False),
}
CONTROL = "top_class_mass"


def crc_lambda_scan(items, alpha, grid):
    """The frozen CRC rule, written as the literal ascending scan of c4_recompute.crc_lambda.

    Identical to it on the unit grid; the only difference is that abstain-on-everything is
    returned as +inf rather than 1.0 + 1e-9, which is the same decision rule. Kept as the
    reference implementation that crc_lambda is checked against.
    """
    n = len(items)
    if n == 0:
        return INF
    for lam in grid:
        r = sum(1 for s, w in items if s >= lam and w) / n
        if (n / (n + 1)) * r + 1 / (n + 1) <= alpha:
            return lam
    return INF


def crc_lambda(items, alpha, grid):
    """Same value as crc_lambda_scan, in time independent of the grid's length.

    The scan is quadratic in the grid, which is affordable for two hundred thresholds and not for
    the eight thousand the likelihood scores need. The empirical risk counts only the WRONG
    calibration items admitted at lambda, and that count is non-increasing in lambda, so the rule
    reduces to a rank: let K be the largest number of admitted wrong items the CRC condition
    still tolerates, evaluated with the same floating-point expression the scan uses. If the
    calibration set holds no more than K wrong items, the first grid point already satisfies the
    condition. Otherwise at most K wrong items may be admitted, which happens exactly when lambda
    sits strictly above the (K+1)-th largest wrong score, so the answer is the first grid point
    above it.
    """
    n = len(items)
    if n == 0:
        return INF
    # Contract, and it is a real one: the grid must be non-empty and ascending. The scan version
    # tolerates an unsorted grid and this one does not, because it locates the answer by position.
    # Every grid this module declares satisfies it; the assertion is here so a future one must too.
    assert grid and all(x <= y for x, y in zip(grid, grid[1:])), "grid must be non-empty, ascending"
    wrong = sorted((s for s, w in items if w), reverse=True)
    K = -1
    while K + 1 <= len(wrong) and (n / (n + 1)) * ((K + 1) / n) + 1 / (n + 1) <= alpha:
        K += 1
    if K < 0:
        return INF                      # even admitting no wrong item misses the CRC condition
    if K >= len(wrong):
        return grid[0]
    i = bisect.bisect_right(grid, wrong[K])
    return grid[i] if i < len(grid) else INF


def auroc(scores, labels):
    """Mann-Whitney AUROC with ties at half credit; None when one class is absent."""
    pos = [s for s, y in zip(scores, labels) if y]
    neg = [s for s, y in zip(scores, labels) if not y]
    if not pos or not neg:
        return None
    order = sorted(range(len(scores)), key=lambda i: scores[i])
    ranks, i = [0.0] * len(scores), 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and scores[order[j + 1]] == scores[order[i]]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    rs = sum(r for r, y in zip(ranks, labels) if y)
    return (rs - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))


LNLP_CACHE_PATH = "experiments/c8_likelihood_stats.json"
_CACHE = {"loaded": None, "data": {}, "sources": {}}


def load_lnlp(tag, seed, qids):
    """Candidate likelihoods for one pool, from the pool if it is here and the cache if not."""
    if _CACHE["loaded"] is None:
        _CACHE["loaded"] = (json.load(open(LNLP_CACHE_PATH))["pools"]
                            if os.path.isfile(LNLP_CACHE_PATH) else {})
    key = f"{tag}|seed{seed}"
    if key in _CACHE["data"]:
        return _CACHE["data"][key]
    v, src = logprob_stats(f"experiments/c4_{tag}_seed{seed}_candidates.jsonl", qids,
                           _CACHE["loaded"], key)
    _CACHE["data"][key] = v
    _CACHE["sources"][key] = src
    return v


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def logprob_stats(pool_path, qids, cache=None, key=None):
    """Per question, the length-normalised sequence log-probability of every usable candidate.

    The usable set is the analyser's: parsed and not truncated. That filter reproduces n_usable
    exactly on all twelve pools, which question_stats asserts, so the likelihood scores and the
    class counts describe the same candidates.

    The pools are gitignored, being about half a gigabyte of raw generations. Only two numbers per
    question survive into any result here, the mean and the maximum, so those are cached to a
    small committed file and used when the pool is absent. A run from the cache is marked as such
    in the result; it is not a substitute for the pool when the pool is what is being checked.
    """
    if os.path.isfile(pool_path):
        out = {}
        for line in open(pool_path):
            r = json.loads(line)
            if r["qid"] not in qids:
                continue
            out[r["qid"]] = [c["cum_logprob"] / c["n_tokens"] for c in r["candidates"]
                             if c.get("parsed") and not c.get("truncated") and c["n_tokens"]]
        return out, "pool"
    if cache and key in cache:
        return {int(k): v for k, v in cache[key].items()}, "cache"
    raise SystemExit(f"{pool_path} is absent and no cached statistics carry {key}")


def question_stats(questions, lnlp, partition, is_error=None):
    """One record per question: the class-count vector of this partition and the pool likelihoods.

    Two correctness fields, and the difference between them is the whole point of the audited
    mode. `strong_ok` is the strong oracle's verdict, unchanged, and it is what a cell calibrated
    on strong labels fits its threshold on. `strong_ok_eval` is the yardstick the risk is measured
    against: the same verdict unless the audit exculpated that exact answer. Under the
    preregistered oracle the two are the same field.

    The audit is a census of every answer either cell returns and the strong oracle rejects, so an
    answer that is strong-wrong and absent from it is a hole in the census, not a case to skip.
    """
    st = {}
    for q in questions:
        cls = q[partition]
        n = sum(c["count"] for c in cls)
        if n == 0:
            continue
        if n != q["n_usable"]:
            raise SystemExit(f"question {q['qid']}: class counts sum to {n}, n_usable {q['n_usable']}")
        v = lnlp.get(q["qid"])
        if v is None:
            raise SystemExit(f"question {q['qid']}: no candidate likelihoods")
        if isinstance(v, dict):                       # summarised: {"n", "mean", "max"}
            if v["n"] != n:
                raise SystemExit(f"question {q['qid']}: {v['n']} usable candidates cached, "
                                 f"{n} in classes")
            mean_lnlp, max_lnlp = v["mean"], v["max"]
        else:
            if len(v) != n:
                raise SystemExit(f"question {q['qid']}: {len(v)} usable candidates in the pool, "
                                 f"{n} in classes")
            mean_lnlp, max_lnlp = statistics.mean(v), max(v)
        masses = [c["count"] / n for c in cls]
        top = max(range(len(cls)), key=lambda i: (cls[i]["count"], -i))   # ties by file order
        c = cls[top]
        ok_eval = c["strong_ok"]
        if is_error is not None and not c["strong_ok"]:
            row = is_error.get((q["qid"], c["representative"]))
            if row is None:
                raise SystemExit(f"question {q['qid']} cell {partition}: the returned answer is "
                                 f"strong-wrong and is not in the audit census")
            ok_eval = not row
        st[q["qid"]] = {"db": q["db"], "masses": masses, "top": top,
                        "weak_ok": c["weak_ok"], "strong_ok": c["strong_ok"],
                        "strong_ok_eval": ok_eval,
                        "mean_lnlp": mean_lnlp, "max_lnlp": max_lnlp}
    return st


def cell_records(st, score, cal, recalibrate=False):
    """Records for one 2x2 cell under one score: confidence, fitting label, evaluation label.

    The splice that keeps the audited mode honest, in one line: the fitting label comes from the
    run as it happened. The strong oracle is the INTERVENTION under test, so cell D still fits its
    threshold on the strong labels it actually had; what the audit replaces is the YARDSTICK the
    risk is read against. `recalibrate` additionally lets the threshold see the audited labels,
    which is a different and hypothetical system, calibrated against a semantic oracle nobody has.
    """
    fn = SCORES[score][1]
    fit = (lambda s_: s_["weak_ok"]) if cal == "single" else \
          (lambda s_: s_["strong_ok_eval"] if recalibrate else s_["strong_ok"])
    return {qid: {"db": s_["db"], "score": fn(s_), "fit_ok": fit(s_),
                  "strong_ok": s_["strong_ok_eval"]}
            for qid, s_ in st.items()}


def evaluate(recs, calq, tstq, alpha, grid):
    lam = crc_lambda([(recs[i]["score"], not recs[i]["fit_ok"]) for i in calq], alpha, grid)
    ans = [i for i in tstq if recs[i]["score"] >= lam]
    n = len(tstq)
    return {"lambda": lam, "answer_rate": len(ans) / n,
            "marginal_risk_strong": sum(1 for i in ans if not recs[i]["strong_ok"]) / n,
            "marginal_risk_fit": sum(1 for i in ans if not recs[i]["fit_ok"]) / n}


def run_pool(questions, lnlp, splits, alpha, is_error=None, recalibrate=False):
    """Every score's GAP, REPAIR and answer rate on one pool and one set of splits."""
    stats = {p: question_stats(questions, lnlp, p, is_error) for p in ("single", "multi")}
    out = {}
    for score, (grid, fn, _) in SCORES.items():
        cells = {}
        for cell, (part, cal) in CELLS.items():
            recs = cell_records(stats[part], score, cal, recalibrate)
            agg = collections.defaultdict(list)
            for calq, tstq in splits:
                calq = [q for q in calq if q in recs]
                tstq = [q for q in tstq if q in recs]
                if not calq or not tstq:
                    continue
                for k, v in evaluate(recs, calq, tstq, alpha, grid).items():
                    agg[k].append(v)
            cells[cell] = agg
        gap = [s - f for f, s in zip(cells["A"]["marginal_risk_fit"],
                                     cells["A"]["marginal_risk_strong"])]
        rep = [d - a for a, d in zip(cells["A"]["marginal_risk_strong"],
                                     cells["D"]["marginal_risk_strong"])]
        dar = [d - a for a, d in zip(cells["A"]["answer_rate"], cells["D"]["answer_rate"])]
        # The flip rate is the share of questions whose returned answer the weak oracle accepts
        # and the strong oracle rejects. It does not depend on the score, and it is the GAP a
        # certificate would carry if it never abstained. Two ratios follow from it and they are
        # different quantities, which an earlier version of this file conflated:
        #
        #   flip_cases_answered_share = GAP / flip_rate = |F and A| / |F|
        #       A bounded share: of the disagreement cases, how many did abstention fail to
        #       remove. It falls when a score abstains more, whether or not it abstains WELL.
        #
        #   flip_enrichment_among_answered = (GAP / answer_rate) / flip_rate
        #                                  = P(disagreement | answered) / P(disagreement)
        #       An enrichment ratio, NOT a share and NOT bounded by 1. It controls for how much
        #       a score abstains and asks whether what it abstains ON is enriched for
        #       disagreements. One means no targeted avoidance at all; above one means the score
        #       preferentially answers exactly those questions.
        st_A = stats["single"]
        flip = sum(1 for v in st_A.values() if v["weak_ok"] and not v["strong_ok"]) / len(st_A)
        ar = statistics.mean(cells["A"]["answer_rate"])
        cond = statistics.mean(gap) / ar if ar else None
        out[score] = {
            "GAP": round(statistics.mean(gap), 4),
            "flip_rate": round(flip, 4),
            "GAP_conditional_on_answering": round(cond, 4) if cond is not None else None,
            "flip_cases_answered_share": (round(statistics.mean(gap) / flip, 4)
                                          if flip else None),
            "flip_enrichment_among_answered": (round(cond / flip, 4)
                                               if cond is not None and flip else None),
            "GAP_positive_splits": round(sum(1 for x in gap if x > 0) / len(gap), 4),
            "REPAIR": round(statistics.mean(rep), 4),
            "REPAIR_negative_splits": round(sum(1 for x in rep if x < 0) / len(rep), 4),
            "risk_A_fit": round(statistics.mean(cells["A"]["marginal_risk_fit"]), 4),
            "risk_A_strong": round(statistics.mean(cells["A"]["marginal_risk_strong"]), 4),
            "risk_D_strong": round(statistics.mean(cells["D"]["marginal_risk_strong"]), 4),
            "answer_rate_A": round(statistics.mean(cells["A"]["answer_rate"]), 4),
            "answer_rate_change": round(statistics.mean(dar), 4),
        }
        # AUROC of the score for the returned answer's correctness, under each oracle, in BOTH
        # cells. Computed on the whole question set, not on splits: it characterises the score,
        # not a certificate.
        #
        # Why both cells. A consistency score built on the weak partition shares its executions
        # with the weak labels, so a weak-oracle evaluation may flatter it for a reason that has
        # nothing to do with its quality. That is a claim about coupling, and one cell cannot
        # test it: a score that simply predicts the harder strong labels less well would show the
        # same drop. Cell D is the mirror image, a consistency score built on the STRONG partition,
        # and coupling predicts the sign of its drop reverses. A drop that does not reverse is
        # evidence against coupling and for the plain reading, that strong labels are harder.
        for cell, part in (("A", "single"), ("D", "multi")):
            recs = cell_records(stats[part], score, "single", recalibrate)
            ids = list(recs)
            sc = [recs[i]["score"] for i in ids]
            w = auroc(sc, [recs[i]["fit_ok"] for i in ids])
            st_ = auroc(sc, [recs[i]["strong_ok"] for i in ids])
            suffix = "" if cell == "A" else "_D"
            out[score]["auroc_weak" + suffix] = round(w, 4) if w is not None else None
            out[score]["auroc_strong" + suffix] = round(st_, 4) if st_ is not None else None
            out[score]["auroc_drop" + suffix] = (round(w - st_, 4)
                                                 if w is not None and st_ is not None else None)
            if cell == "A":
                # How many values the score actually takes. Ties cost AUROC, so a coarse score
                # can score lower for that reason; that is part of its discrimination, not a
                # confound, but the reader needs the number to interpret an absolute comparison.
                out[score]["distinct_score_values"] = len(set(sc))
    return out


def percentile_ranks(vals, groups):
    """Mean percentile rank of each group inside vals, ties taken at the mid-rank."""
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    r, i = [0.0] * len(vals), 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        m = (i + j) / 2
        for k in range(i, j + 1):
            r[order[k]] = m
        i = j + 1
    d = (len(vals) - 1) or 1
    return [statistics.mean(r[i] / d for i in g) if g else None for g in groups]


def rank_decomposition(alpha_unused=None):
    """Where each score ranks the answers the two oracles disagree about.

    This is the direct test of the mechanism the AUROC drop only suggests. The set of cell-A
    answers the weak oracle accepts and the strong oracle rejects is the SAME set of questions for
    every score, because the answer rule is fixed. So any difference between scores is a
    difference in where they place that one fixed set. If a consistency score is coupled to the
    weak oracle, it should place those answers near the answers both oracles accept, which is
    exactly what makes the weak oracle flatter it. A likelihood score has no such coupling and
    has no reason to.

    Reported as the position of the disagreement group on the line from the both-wrong group to
    the both-right group, so 100% means the score treats those answers exactly like correct ones
    and 0% exactly like wrong ones.
    """
    rows = {}
    for tag in TAGS:
        acc, sizes = collections.defaultdict(list), collections.defaultdict(list)
        for seed in SEEDS:
            qs = json.load(open(f"experiments/c4_{tag}_seed{seed}_results_official_per_question.json"))["questions"]
            lnlp = load_lnlp(tag, seed, {q["qid"] for q in qs})
            st = question_stats(qs, lnlp, "single")
            ids = list(st)
            flip = [i for i, q in enumerate(ids) if st[q]["weak_ok"] and not st[q]["strong_ok"]]
            wrong = [i for i, q in enumerate(ids) if not st[q]["weak_ok"]]
            right = [i for i, q in enumerate(ids) if st[q]["weak_ok"] and st[q]["strong_ok"]]
            sizes["disagreement"].append(len(flip))
            sizes["both_wrong"].append(len(wrong))
            sizes["both_right"].append(len(right))
            for score, (_, fn, _u) in SCORES.items():
                acc[score].append(percentile_ranks([fn(st[q]) for q in ids], [flip, wrong, right]))
        # Per seed, not just the last one: an earlier version overwrote this and reported one
        # seed's counts as if they were the pool's.
        rows[tag] = {"group_sizes_per_seed": {k: v for k, v in sizes.items()},
                     "group_sizes_mean": {k: round(statistics.mean(v), 1) for k, v in sizes.items()},
                     "scores": {}}
        for score, v in acc.items():
            f, w, r = (statistics.mean(x[k] for x in v) for k in range(3))
            rows[tag]["scores"][score] = {
                "disagreement": round(f, 4), "both_wrong": round(w, 4), "both_right": round(r, 4),
                "position_between": round((f - w) / (r - w), 4) if r != w else None}
    return rows


def same_answer_auroc():
    """The symmetric AUROC test restricted to questions where both cells return the same SQL.

    Cells A and D return a different string on about 2.9% of answers, so a sign reversal between
    the cells could in principle be produced by those questions rather than by the partition the
    score is built on. Dropping them removes that possibility: on this subset the two cells answer
    identically and differ only in which partition defines the classes. The likelihood scores then
    become numerically identical in the two cells, which is the null this control needs.
    """
    rows = {}
    for tag in TAGS:
        kept, dA, dD = [], collections.defaultdict(list), collections.defaultdict(list)
        for seed in SEEDS:
            qs = json.load(open(f"experiments/c4_{tag}_seed{seed}"
                                f"_results_official_per_question.json"))["questions"]
            lnlp = load_lnlp(tag, seed, {q["qid"] for q in qs})
            st = {p_: question_stats(qs, lnlp, p_) for p_ in ("single", "multi")}
            top = lambda cls: max(range(len(cls)), key=lambda i: (cls[i]["count"], -i))
            same = [q["qid"] for q in qs
                    if q["single"] and q["multi"]
                    and q["single"][top(q["single"])]["representative"]
                    == q["multi"][top(q["multi"])]["representative"]]
            kept.append(len(same))
            for score, (_, fn, _u) in SCORES.items():
                for part, d in (("single", dA), ("multi", dD)):
                    v = [fn(st[part][i]) for i in same]
                    w = auroc(v, [st[part][i]["weak_ok"] for i in same])
                    g = auroc(v, [st[part][i]["strong_ok"] for i in same])
                    d[score].append(w - g)
        rows[tag] = {"questions_kept_per_seed": kept,
                     "scores": {s_: {"drop_A": round(statistics.mean(dA[s_]), 4),
                                     "drop_D": round(statistics.mean(dD[s_]), 4),
                                     "reverses": statistics.mean(dA[s_]) > 0 > statistics.mean(dD[s_])}
                                for s_ in SCORES}}
    return rows


def grid_sensitivity(alpha, splits, seed, factor=5):
    """Refine every score's grid and report the largest change in GAP and REPAIR.

    The grids differ between scores because the scores live on different ranges, and an earlier
    version of this script gave the likelihood scores a grid so coarse that it, and not their
    quality, set their operating points. This check says whether any such asymmetry is still
    doing work: if refining every grid several-fold moves nothing, resolution is not the story.
    """
    import copy as _copy
    saved = _copy.deepcopy(SCORES)
    try:
        base = _sweep(alpha, splits, seed)
        n = 200 * factor
        for k in ("top_class_mass", "lin_deg"):
            SCORES[k] = ([i / n for i in range(n + 1)],) + SCORES[k][1:]
        L = math.log(50)
        SCORES["discrete_semantic_entropy"] = ([-L + i * L / n for i in range(n + 1)],) \
            + SCORES["discrete_semantic_entropy"][1:]
        m = LP_STEPS * factor
        g = [-INF] + [LP_LO + i * (-LP_LO) / m for i in range(m + 1)]
        for k in ("mean_seq_logprob", "max_seq_logprob"):
            SCORES[k] = (g,) + SCORES[k][1:]
        fine = _sweep(alpha, splits, seed)
    finally:
        SCORES.clear()
        SCORES.update(saved)
    worst = 0.0
    for tag in base:
        for score in base[tag]:
            for k in ("GAP", "REPAIR"):
                worst = max(worst, abs(base[tag][score][k] - fine[tag][score][k]))
    return {"refinement_factor": factor, "coarse": base, "fine": fine,
            "largest_absolute_change": round(worst, 5)}


def _sweep(alpha, splits, seed):
    out = {}
    for tag in TAGS:
        for how in ("question", "database"):
            acc = collections.defaultdict(lambda: collections.defaultdict(list))
            for s in SEEDS:
                suffix = ("_official_per_question.json" if how == "question"
                          else "_official_dbsplit_per_question.json")
                qs = json.load(open(f"experiments/c4_{tag}_seed{s}_results{suffix}"))["questions"]
                lnlp = load_lnlp(tag, s, {q["qid"] for q in qs})
                sp = make_splits([q["qid"] for q in qs], {q["qid"]: q["db"] for q in qs},
                                 how, splits, seed)
                for score, r in run_pool(qs, lnlp, sp, alpha).items():
                    for k in ("GAP", "REPAIR"):
                        acc[score][k].append(r[k])
            out[f"{tag}|{how}"] = {score: {k: round(statistics.mean(v), 5) for k, v in d.items()}
                                   for score, d in acc.items()}
    return out


def verify_against_recompute(questions, lnlp, splits, alpha, seed):
    """Compare the control score with c4_recompute at the record and decision level, not only at
    the four-decimal aggregate.

    Equal pool means are weak evidence: two different implementations can average to the same
    rounded number. What must match is every per-question record and every per-split decision.
    One admitted difference in representation: where no threshold satisfies the CRC condition,
    c4_recompute returns 1.0 + 1e-9 and this module returns +inf. Both admit nothing, so the
    decision is identical and the lambda values are compared modulo that one substitution.
    """
    import random as _random
    stats = {p_: question_stats(questions, lnlp, p_) for p_ in ("single", "multi")}
    bad = collections.Counter()
    n_rec = n_dec = 0
    for cell, (part, cal) in CELLS.items():
        mine = cell_records(stats[part], CONTROL, cal)
        theirs = c4_recompute.cell_records(questions, part, cal, "usable", "first",
                                           _random.Random(seed))
        if set(mine) != set(theirs):
            bad["question_set"] += 1
        for qid in mine:
            n_rec += 1
            m, t = mine[qid], theirs[qid]
            if m["score"] != t["top_mass"]:
                bad["score"] += 1
            if m["fit_ok"] != t["fit_ok"]:
                bad["fit_ok"] += 1
            if m["strong_ok"] != t["strong_ok"]:
                bad["strong_ok"] += 1
            if m["db"] != t["db"]:
                bad["db"] += 1
        grid = SCORES[CONTROL][0]
        for calq, tstq in splits:
            calq = [q for q in calq if q in mine]
            tstq = [q for q in tstq if q in mine]
            if not calq or not tstq:
                continue
            n_dec += 1
            e1 = evaluate(mine, calq, tstq, alpha, grid)
            e2 = c4_recompute.evaluate(theirs, calq, tstq, alpha)
            lam1 = 1.0 + 1e-9 if e1["lambda"] == INF else e1["lambda"]
            if lam1 != e2["lambda"]:
                bad["lambda"] += 1
            for k in ("answer_rate", "marginal_risk_strong", "marginal_risk_fit"):
                if e1[k] != e2[k]:
                    bad[k] += 1
            a1 = {i for i in tstq if mine[i]["score"] >= e1["lambda"]}
            a2 = {i for i in tstq if theirs[i]["top_mass"] >= e2["lambda"]}
            if a1 != a2:
                bad["answered_set"] += 1
    return {"records_compared": n_rec, "split_cells_compared": n_dec,
            "mismatches": dict(bad), "clean": not bad}


CELLS = {"A": ("single", "single"), "D": ("multi", "multi")}


def load_audit(cases_path, audit_path, convention):
    from c6_gap_audited import CONVENTIONS
    cases = json.load(open(cases_path))["cases"]
    rows = {r["case_id"]: r for r in json.load(open(audit_path))["cases"]}
    pred = CONVENTIONS[convention]
    return {(c["qid"], c["rep"]): pred(rows[c["case_id"]]) for c in cases}



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
    ap.add_argument("--alpha", type=float, default=0.1)
    ap.add_argument("--splits", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260903)
    ap.add_argument("--tags", nargs="*", default=list(TAGS))
    ap.add_argument("--audited", default="",
                    help="also recompute under one audited convention (wide, narrow, agreed, "
                         "unanimous), the evaluation-only intervention of c7")
    ap.add_argument("--also-recalibrated", action="store_true",
                    help="in the audited mode, also let the strong-label cell fit its threshold "
                         "on the audited labels; a different, hypothetical system")
    ap.add_argument("--cases", default="experiments/c7_repair_cases.json")
    ap.add_argument("--audit", default="experiments/c7_semantic_audit.json")
    ap.add_argument("--check-crc", type=int, default=0, metavar="N",
                    help="randomised equivalence check of the fast CRC solver against the "
                         "literal ascending scan, over N cases on every declared grid")
    ap.add_argument("--emit-stats", action="store_true",
                    help="write the per-question likelihood statistics the likelihood scores "
                         "need, so the analysis reruns without the gitignored candidate pools")
    ap.add_argument("--rank-decomposition", action="store_true",
                    help="where each score ranks the answers the two oracles disagree about, "
                         "the direct test of the coupling the AUROC drop only suggests")
    ap.add_argument("--same-answer-auroc", action="store_true",
                    help="repeat the symmetric AUROC test on the questions where both cells "
                         "return the same SQL, so the reversal cannot come from the answer")
    ap.add_argument("--grid-sensitivity", action="store_true",
                    help="refine every score's threshold grid and report the largest change")
    ap.add_argument("--verify", action="store_true",
                    help="check that the control score reproduces the stored GAP and REPAIR")
    ap.add_argument("--replace", action="store_true",
                    help="allow this run to write a smaller artifact than the one on disk")
    ap.add_argument("--out", default="experiments/c8_baselines.json")
    a = ap.parse_args()

    crc_check = None
    if a.check_crc:
        # crc_lambda_scan is the reference implementation and this is what makes it live: the
        # fast solver is only usable if it agrees with the literal scan everywhere, including
        # the cases that never arise in the pools (empty calibration sets, no wrong items,
        # scores outside the grid, heavy ties, alpha so small that nothing is feasible).
        import random as _rnd
        rng = _rnd.Random(a.seed)
        grids = [SCORES[k][0] for k in SCORES]
        bad = 0
        for _ in range(a.check_crc):
            grid = rng.choice(grids)
            lo = grid[1] if grid[0] == -INF else grid[0]
            m = rng.choice([0, 1, 2, 5, 17, 60, 254])
            items = [(rng.uniform(lo - 0.3, grid[-1] + 0.3),
                      rng.random() < rng.choice([0.02, 0.1, 0.4, 0.9])) for _ in range(m)]
            for alpha in (0.01, 0.05, 0.1, 0.15, 0.2):
                if crc_lambda(items, alpha, grid) != crc_lambda_scan(items, alpha, grid):
                    bad += 1
        crc_check = {"cases": a.check_crc * 5, "mismatches": bad, "grids": list(SCORES)}
        print(f"CRC solver against the literal scan: {a.check_crc * 5} randomised cases, "
              f"{bad} mismatches\n")
        if bad:
            raise SystemExit("the fast CRC solver disagrees with the reference scan")

    if a.emit_stats:
        pools = {}
        for tag in TAGS:
            for seed in SEEDS:
                qs = json.load(open(f"experiments/c4_{tag}_seed{seed}"
                                    f"_results_official_per_question.json"))["questions"]
                v = load_lnlp(tag, seed, {q["qid"] for q in qs})
                pools[f"{tag}|seed{seed}"] = {
                    str(k): {"n": len(x), "mean": statistics.mean(x), "max": max(x)}
                    for k, x in sorted(v.items())}
        json.dump({"note": "length-normalised sequence log-probability of the usable candidates "
                           "of each question, summarised to the two statistics the likelihood "
                           "scores read. The pools themselves are gitignored; these are the "
                           "sufficient statistics for everything in c8_baselines.json.",
                   "produced_by": "experiments/c8_baselines.py --emit-stats",
                   "pools": pools}, open(LNLP_CACHE_PATH, "w"), indent=1)
        print(f"written {LNLP_CACHE_PATH}")
        _CACHE["loaded"] = None

    is_error = load_audit(a.cases, a.audit, a.audited) if a.audited else None
    result = {"alpha": a.alpha, "splits": a.splits, "seed": a.seed,
              "audited_convention": a.audited or None,
              "audited_mode": (("also_recalibrated" if a.also_recalibrated else "evaluation_only")
                               if a.audited else None),
              "scores": {k: {"reads_equivalence_classes": v[2]} for k, v in SCORES.items()},
              "note": "one certificate, one answer rule, one set of splits; only the confidence "
                      "score varies. GAP is within cell A, REPAIR is cell D minus cell A, both "
                      "evaluated under the strong oracle unless an audited convention is named.",
              "provenance": {
                  "script_sha256": sha256_file(os.path.abspath(__file__)),
                  "recompute_sha256": sha256_file("experiments/c4_recompute.py"),
                  "likelihood_source": None,
                  "inputs_sha256": {}},
              "crc_equivalence_check": crc_check,
              "pools": {}, "summary": {}}
    agg = collections.defaultdict(lambda: collections.defaultdict(list))
    verify_rows, deep_totals = [], collections.Counter()
    for tag in a.tags:
        for seed in SEEDS:
            for split in ("question", "database"):
                suffix = ("_official_per_question.json" if split == "question"
                          else "_official_dbsplit_per_question.json")
                path = f"experiments/c4_{tag}_seed{seed}_results{suffix}"
                qs = json.load(open(path))["questions"]
                lnlp = load_lnlp(tag, seed, {q["qid"] for q in qs})
                sp = make_splits([q["qid"] for q in qs], {q["qid"]: q["db"] for q in qs},
                                 split, a.splits, a.seed)
                row = run_pool(qs, lnlp, sp, a.alpha, is_error, a.also_recalibrated)
                result["pools"][f"{tag}|seed{seed}|{split}"] = row
                for score, r in row.items():
                    # every numeric field, so a field added later is summarised without a second
                    # edit here and cannot silently go missing from the summary
                    for k, v in r.items():
                        if isinstance(v, (int, float)):
                            agg[(tag, split)][f"{score}|{k}"].append(v)
                if a.verify and not is_error:
                    # Two references. The frozen result file is the scientific record, but it was
                    # produced by an analyser whose top-class tie rule uses a class key the file
                    # does not carry, so any recomputation from the file carries a small known
                    # residual against it. c4_recompute is that recomputation, already in the
                    # repository and already checked against the record, so it is the reference
                    # that must match to the last digit. A residual against the stored file is
                    # only acceptable if it is exactly the residual c4_recompute itself carries.
                    import random as _random
                    ref = c4_recompute.cells_over_splits(
                        qs, sp, a.alpha, "usable", "first", _random.Random(a.seed))
                    deep = verify_against_recompute(qs, lnlp, sp, a.alpha, a.seed)
                    deep_totals["records"] += deep["records_compared"]
                    deep_totals["decisions"] += deep["split_cells_compared"]
                    for k, v in deep["mismatches"].items():
                        deep_totals[k] += v
                    stem = path.replace("_per_question.json", ".json")
                    st = json.load(open(stem))
                    g = st["oracle_gap_within_cell_A"]["marginal_risk_strong_minus_fit"]["mean"]
                    p = st["paired_contrasts_vs_cell_A"]["score=multi|calib=multi"][
                        "marginal_risk_strong"]["mean_change_vs_A"]
                    verify_rows.append({
                        "pool": f"{tag}|seed{seed}|{split}",
                        "dGAP_vs_recompute": round(row[CONTROL]["GAP"] - ref["GAP"], 6),
                        "dREPAIR_vs_recompute": round(row[CONTROL]["REPAIR"] - ref["REPAIR"], 6),
                        "dGAP_vs_stored": round(row[CONTROL]["GAP"] - g, 6),
                        "dREPAIR_vs_stored": round(row[CONTROL]["REPAIR"] - p, 6),
                        "recompute_dGAP_vs_stored": round(ref["GAP"] - g, 6),
                        "recompute_dREPAIR_vs_stored": round(ref["REPAIR"] - p, 6)})
    result["provenance"]["likelihood_source"] = dict(sorted(_CACHE["sources"].items()))
    for tag in a.tags:
        for seed in SEEDS:
            for suf in ("_official_per_question.json", "_official_dbsplit_per_question.json"):
                f = f"experiments/c4_{tag}_seed{seed}_results{suf}"
                result["provenance"]["inputs_sha256"][f] = sha256_file(f)
    # Everything actually read, including the gitignored pools when they were the source. An
    # earlier version claimed to hash all inputs while hashing only the committed ones.
    for key, src in _CACHE["sources"].items():
        if src == "pool":
            tag, seed = key.split("|seed")
            f = f"experiments/c4_{tag}_seed{seed}_candidates.jsonl"
            result["provenance"]["inputs_sha256"][f] = sha256_file(f)
    for f in ([LNLP_CACHE_PATH] if os.path.isfile(LNLP_CACHE_PATH) else []) + \
             ([a.cases, a.audit] if a.audited else []):
        result["provenance"]["inputs_sha256"][f] = sha256_file(f)

    for (tag, split), d in sorted(agg.items()):
        result["summary"][f"{tag}|{split}"] = {k: round(statistics.mean(v), 4)
                                               for k, v in sorted(d.items())}
    if verify_rows:
        mx = lambda k: max(abs(r[k]) for r in verify_rows)
        same = all(r["dGAP_vs_stored"] == r["recompute_dGAP_vs_stored"]
                   and r["dREPAIR_vs_stored"] == r["recompute_dREPAIR_vs_stored"]
                   for r in verify_rows)
        deep_bad = {k: v for k, v in deep_totals.items() if k not in ("records", "decisions")}
        result["verify"] = {
            "rows": verify_rows,
            "record_level": {
                "per_question_records_compared": deep_totals["records"],
                "split_cell_decisions_compared": deep_totals["decisions"],
                "mismatches": deep_bad,
                "clean": not deep_bad,
                "note": "score, fitting label, strong label and database per question; and per "
                        "split, lambda, answer rate, both risks and the answered set itself. "
                        "Lambda is compared modulo the one representation difference: an "
                        "infeasible threshold is +inf here and 1.0 + 1e-9 in c4_recompute."},
            "max_abs_diff_vs_recompute": {"GAP": mx("dGAP_vs_recompute"),
                                          "REPAIR": mx("dREPAIR_vs_recompute")},
            "max_abs_diff_vs_stored": {"GAP": mx("dGAP_vs_stored"),
                                       "REPAIR": mx("dREPAIR_vs_stored")},
            "reproduces_recompute_exactly": mx("dGAP_vs_recompute") == 0.0
                                            and mx("dREPAIR_vs_recompute") == 0.0,
            "residual_vs_stored_is_the_known_tie_rule_residual": same,
            "note": "the control score is this script running the frozen pipeline's own score. "
                    "It must equal c4_recompute to the last digit; its difference from the stored "
                    "file is the top-class tie rule the per-question files cannot carry, and is "
                    "acceptable only when it equals the difference c4_recompute itself carries."}
        print(f"control score over {len(verify_rows)} pool-splits:\n"
              f"  record level      {deep_totals['records']} per-question records and "
              f"{deep_totals['decisions']} split-cell decisions compared, "
              f"mismatches {deep_bad or 'none'}\n"
              f"  vs c4_recompute   largest |dGAP| {mx('dGAP_vs_recompute')}, "
              f"|dREPAIR| {mx('dREPAIR_vs_recompute')}\n"
              f"  vs stored record  largest |dGAP| {mx('dGAP_vs_stored')}, "
              f"|dREPAIR| {mx('dREPAIR_vs_stored')}  "
              f"(identical to c4_recompute's own residual: {same})\n")

    if a.rank_decomposition:
        rd = rank_decomposition()
        result["rank_decomposition"] = rd
        print("Mean percentile rank of three disjoint groups of cell-A answers, three-seed means.")
        print("The disagreement group is the same set of questions for every score.\n")
        for tag, d in rd.items():
            g = d["group_sizes_per_seed"]
            fmt = lambda k: (f"{min(g[k])}" if min(g[k]) == max(g[k])
                             else f"{min(g[k])} to {max(g[k])}")
            print(f"  {tag}: disagreement n={fmt('disagreement')}, "
                  f"both wrong n={fmt('both_wrong')}, both right n={fmt('both_right')}")
            print(f"    {'score':28s}{'disagree':>10s}{'wrong':>10s}{'right':>10s}{'position':>10s}")
            for score, r in d["scores"].items():
                print(f"    {score:28s}{r['disagreement']:10.3f}{r['both_wrong']:10.3f}"
                      f"{r['both_right']:10.3f}{r['position_between']:9.0%}")
            print()

    if a.same_answer_auroc:
        sa = same_answer_auroc()
        result["same_answer_auroc"] = sa
        print("Symmetric AUROC test on the questions where cell A and cell D return the same SQL.")
        print("Weak-label minus strong-label AUROC, in points.\n")
        print(f"  {'checkpoint':20s}{'kept':>10s}  {'score':28s}{'A':>8s}{'D':>8s}{'reverses':>10s}")
        for tag, d in sa.items():
            k = d["questions_kept_per_seed"]
            for score, r in d["scores"].items():
                print(f"  {tag:20s}{min(k)}-{max(k):<6}  {score:28s}"
                      f"{100 * r['drop_A']:+8.2f}{100 * r['drop_D']:+8.2f}"
                      f"{'yes' if r['reverses'] else 'no':>10s}")
        n_rev = sum(1 for d in sa.values() for s_, r in d["scores"].items()
                    if r["reverses"] and SCORES[s_][2])
        print(f"\n  consistency scores reversing sign: {n_rev} of "
              f"{4 * sum(1 for v in SCORES.values() if v[2])}\n")

    if a.grid_sensitivity:
        gs = grid_sensitivity(a.alpha, a.splits, a.seed)
        result["grid_sensitivity"] = gs
        print(f"Refining every grid {gs['refinement_factor']}-fold moves GAP and REPAIR by at "
              f"most {100 * gs['largest_absolute_change']:.2f} points.\n")

    write_result(a.out, result, a.replace)

    head = f"alpha = {a.alpha}" + (f", audited convention {a.audited}, "
                                   f"{result['audited_mode']}" if a.audited else
                                   ", preregistered oracle labels")
    print(f"GAP and REPAIR in percentage points, three-seed means. {head}.\n")
    for split in ("question", "database"):
        print(f"  {split} splits")
        print(f"    {'score':28s}" + "".join(f"{t.replace('-autosql',''):>18s}" for t in a.tags))
        for kind in ("GAP", "REPAIR"):
            print(f"    {kind}")
            for score in SCORES:
                cells = []
                for tag in a.tags:
                    v = result["summary"][f"{tag}|{split}"][f"{score}|{kind}"]
                    cells.append(f"{100 * v:+17.2f}")
                print(f"      {score:26s}" + "".join(cells))
    print("\n  AUROC for the returned answer's correctness, weak oracle then strong oracle")
    for score in SCORES:
        cells = []
        for tag in a.tags:
            s = result["summary"][f"{tag}|question"]
            cells.append(f"{s[f'{score}|auroc_weak']:.3f}/{s[f'{score}|auroc_strong']:.3f}")
        print(f"    {score:28s}" + "".join(f"{c:>18s}" for c in cells))
    print(f"\nwritten {a.out}")


if __name__ == "__main__":
    main()
