#!/usr/bin/env python3
"""E0 step 3 (local, CPU): the oracle-intervention 2x2.

The question: if the calibration labels and the equivalence classes come from a WEAK oracle
(one benchmark database) but the world is judged by a STRONG one (the distilled test suite),
how much risk does the certificate actually carry, and does calibrating on the strong oracle
repair it?

  scoring partition  x  calibration labels     ->  always evaluated against the STRONG oracle
  ------------------------------------------------------------------------------------------
  single  x  single   = A, what the whole text-to-SQL UQ literature does today
  single  x  multi    = B
  multi   x  single   = C
  multi   x  multi    = D

Two published certificate recipes, no new theory:

  Method A, set coverage (split conformal, Conformal-LM style over execution classes).
    nonconformity s = 1 - mass(class that matches the gold); tau = the ceil((n+1)(1-alpha))/n
    empirical quantile of the calibration scores; at test time admit every class with
    mass >= 1 - tau. The set can only contain classes that were SAMPLED, so a question whose
    samples hold no correct class scores 1 on calibration and counts as uncovered at test time.
    What is reported is therefore sampled-candidate-set coverage, bounded above by 1 minus the
    no-correct-class rate; it is not the unconditional coverage of an oracle-complete set.

  Method B, marginal wrong-answer risk (conformal risk control, Angelopoulos et al. 2022).
    Loss L(lambda) = 1[top-class mass >= lambda AND the answer is wrong], monotone
    non-increasing in lambda. lambda_hat = inf{lambda : (n/(n+1)) Rhat(lambda) + 1/(n+1) <= alpha}.
    Guarantee: E[L(lambda_hat)] <= alpha.

Reported separately: prediction-set coverage, answer rate, and the conditional selective risk
among answered questions. The last one is descriptive: neither recipe controls it directly,
and that gap is claim C3. It is undefined on a split in which no test question is answered,
and is then recorded as null rather than as zero.

Provenance: every result file records the sha256 of its candidate pool, of this script and of
the official evaluator it calls, the git commit of the working tree, and every analysis option,
so a number can be traced back to the exact code and input that produced it. The per-question
class counts go to a sibling file so the summary stays readable.
"""
import argparse, collections, hashlib, json, math, os, random, re, sqlite3, statistics, subprocess, sys, time

NULL = "\x00NULL"


def _val(v):
    if v is None:
        return NULL
    if isinstance(v, float):
        return str(int(v)) if v == int(v) else f"{v:.6f}"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, bytes):
        return v.decode("utf-8", "replace")
    return str(v)


def canon(rows, order_matters):
    """Custom canonical form (column order kept, floats rounded, values coerced to strings).
    Order matters only when the gold has ORDER BY. Kept as a declared sensitivity comparator;
    the primary comparator is the official result_eq, see --comparator."""
    t = [tuple(_val(v) for v in r) for r in rows]
    return tuple(t) if order_matters else tuple(sorted(t))


def h(x):
    return hashlib.sha1(json.dumps(x, ensure_ascii=False, default=str).encode()).hexdigest()


def sha256_file(path):
    hh = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            hh.update(chunk)
    return hh.hexdigest()


def git_state():
    """Commit and dirty flag of the working tree, or None when git is unavailable."""
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True,
                                check=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"],
                               capture_output=True, text=True, check=True).stdout.strip()
        return {"commit": commit, "dirty": bool(dirty)}
    except Exception:
        return None


def run(con, sql, budget=2_000_000):
    n = [0]
    hit = {"v": False}

    def prog():
        n[0] += 1
        if n[0] > budget:
            hit["v"] = True
            return 1
        return 0

    con.set_progress_handler(prog, 5000)
    try:
        return con.execute(sql).fetchall(), None
    except Exception as e:
        return None, ("TIMEOUT" if hit["v"] else type(e).__name__)
    finally:
        con.set_progress_handler(None, 0)


def _load_official_result_eq(path="data/spider/exec_eval.py"):
    """Load result_eq from the vendored official evaluator without importing its CLI."""
    import importlib.util, warnings
    # the official module imports its sibling `parse`, so its own directory has to be importable
    sys.path.insert(0, os.path.dirname(os.path.abspath(path)))
    warnings.filterwarnings("ignore", category=SyntaxWarning)
    spec = importlib.util.spec_from_file_location("official_exec_eval", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.result_eq


def union_find_classes(items, equal):
    """Group items with a PAIRWISE equality predicate that is not assumed transitive.

    Returns (class_of, n_intransitive_pairs). Merge order is the order of `items`, which is
    the order the candidates were sampled in, and that order is frozen in the preregistration
    because a non-transitive relation makes the grouping order-dependent.
    """
    parent = list(range(len(items)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    eq = {}
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            e = equal(items[i], items[j])
            eq[(i, j)] = e
            if e:
                ri, rj = find(i), find(j)
                if ri != rj:
                    parent[ri] = rj
    # how often does the induced grouping claim an equality the relation itself denies?
    bad = 0
    for (i, j), e in eq.items():
        if not e and find(i) == find(j):
            bad += 1
    return {items[i]: find(i) for i in range(len(items))}, bad


# ------------------------------------------------------------------ certificates
def conformal_quantile(scores, alpha):
    """ceil((n+1)(1-alpha))/n empirical quantile, the standard split-conformal level."""
    n = len(scores)
    if n == 0:
        return 1.0
    k = math.ceil((n + 1) * (1 - alpha))
    if k > n:
        return 1.0
    return sorted(scores)[k - 1]


def crc_lambda(items, alpha, grid):
    """items: list of (top_mass, wrong_bool). Loss is monotone non-increasing in lambda.

    lambda_hat = inf{lambda : (n/(n+1)) Rhat(lambda) + 1/(n+1) <= alpha}, so the scan has to go
    UP and stop at the first lambda that satisfies the bound. Scanning down instead returns the
    largest such lambda, which is lambda = 1.0 whenever the problem is feasible at all: the loss
    is smallest exactly where the rule answers least. That still satisfies the guarantee, but it
    is the answer-nothing corner rather than the CRC threshold, and it pins every cell to the
    same lambda, which is precisely the comparison this experiment exists to make."""
    n = len(items)
    for lam in sorted(grid):
        r = sum(1 for m, w in items if m >= lam and w) / n
        if (n / (n + 1)) * r + 1 / (n + 1) <= alpha:
            return lam
    return 1.0 + 1e-9                     # not feasible at any threshold: abstain on everything


def summarise(values):
    """mean and population sd over the DEFINED entries; null entries are counted, not imputed."""
    vv = [x for x in values if x is not None]
    if not vv:
        return {"mean": None, "sd": None, "n_splits_undefined": len(values)}
    d = {"mean": round(statistics.mean(vv), 4), "sd": round(statistics.pstdev(vv), 4)}
    if len(vv) != len(values):
        d["n_splits_undefined"] = len(values) - len(vv)
    return d


def paired(xs, ys):
    """Paired difference ys - xs over splits where both are defined. Strict sign counting: a
    zero difference agrees with nothing and is counted apart."""
    d = [y - x for x, y in zip(xs, ys) if x is not None and y is not None]
    if not d:
        return {"mean": None, "sd_of_paired_diff": None, "splits_with_same_sign": None,
                "splits_with_zero_diff": None, "n_splits_used": 0}
    m = statistics.mean(d)
    out = {"mean": round(m, 4), "sd_of_paired_diff": round(statistics.pstdev(d), 4),
           "splits_with_same_sign": round(
               sum(1 for v in d if (v > 0 and m > 0) or (v < 0 and m < 0)) / len(d), 4),
           "splits_with_zero_diff": round(sum(1 for v in d if v == 0) / len(d), 4)}
    if len(d) != len(xs):
        out["n_splits_used"] = len(d)
    return out


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", default="experiments/e0_candidates.jsonl")
    ap.add_argument("--suite-root", default="data/spider/test_suite_database")
    ap.add_argument("--out", default="experiments/e0_results.json")
    ap.add_argument("--per-question-out", default="",
                    help="per-question class counts; default <out stem>_per_question.json")
    ap.add_argument("--alpha", type=float, default=0.1)
    ap.add_argument("--splits", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260903)
    ap.add_argument("--max-instances", type=int, default=0)
    ap.add_argument("--instance-folds", type=int, default=0,
                    help="POST-FREEZE ADDITION (2026-09-05), default off. Split each "
                         "database's suite instances into K folds; the multi-instance partition and "
                         "its calibration labels are built from the CONSTRUCTION fold plus the "
                         "original database, while correctness is judged on the HELD-OUT folds plus "
                         "the original. This asks whether calibrating against a stronger finite "
                         "oracle generalises to execution instances it never saw, instead of "
                         "measuring fit to the same instances.")
    ap.add_argument("--construction-fold", type=int, default=0,
                    help="which fold builds the classes and labels; the rest evaluate")
    ap.add_argument("--fold-seed", type=int, default=20260903)
    ap.add_argument("--order-rule", choices=("gold", "either"), default="gold",
                    help="POST-FREEZE ADDITION (2026-09-05), default is "
                         "the preregistered behaviour. The official result_eq has to be told whether "
                         "row order matters. 'gold' reads that from the question's gold query, which "
                         "a deployed system does not have. 'either' derives it from the two queries "
                         "actually being compared: order matters if either carries an ORDER BY. Only "
                         "affects --comparator official, where the flag is used at comparison time; "
                         "the custom comparator bakes it into its canonical form instead.")
    ap.add_argument("--partition", choices=("gold-anchored", "candidates-only"), default="gold-anchored",
                    help="POST-FREEZE ADDITION (2026-09-05), default is the "
                         "preregistered behaviour. 'gold-anchored' puts the gold query into the "
                         "union-find, so two candidate classes that are each equivalent to the gold "
                         "merge through it; a deployed certificate has no gold. 'candidates-only' "
                         "builds the partition from the sampled candidates alone and then compares "
                         "each class representative with the gold to label it, which is what a "
                         "deployed system could actually do.")
    ap.add_argument("--comparator", choices=("custom", "official"), default="custom",
                    help="'official' calls result_eq from the vendored data/spider/exec_eval.py, "
                         "which is byte-identical to the upstream test-suite release: it searches "
                         "column permutations and compares raw values. It is a PAIRWISE relation, "
                         "not a canonical form, so classes are built by union-find and "
                         "transitivity is measured rather than assumed. 'custom' is the earlier "
                         "canonicaliser (column order kept, floats rounded, values coerced to "
                         "strings) and is kept only as a declared sensitivity comparison.")
    ap.add_argument("--weak-oracle", choices=("original", "first_suite_instance"),
                    default="original",
                    help="which single database plays the WEAK oracle. 'original' is the "
                         "populated database the benchmark ships, which is what practitioners "
                         "use and what E0 was run with. 'first_suite_instance' is the "
                         "lexicographically first distilled instance, which is the only "
                         "definition available on benchmarks whose shipped database is empty "
                         "(every text2sql-data task: academic, advising, atis, geography, imdb, "
                         "restaurants, scholar, yelp). Running both on Spider, where both exist, "
                         "is what licenses transporting the second definition elsewhere.")
    ap.add_argument("--split-by", choices=("question", "database"), default="question",
                    help="'question': random half-splits of questions (calibration and test share "
                         "schemas). 'database': random half-splits of DATABASES, so no schema is "
                         "seen at both calibration and test; the paired statistics are then over "
                         "database-level resplits.")
    ap.add_argument("--mass-denominator", choices=("usable", "budget"), default="usable",
                    help="'usable': class mass = count / number of parsed, non-truncated "
                         "candidates (mass sums to one). 'budget': class mass = count / declared "
                         "sampling budget, so a failed generation keeps its share of mass as an "
                         "implicit abstention instead of being renormalised away. The two coincide "
                         "whenever parse rate is 1 and truncation rate is 0.")
    a = ap.parse_args()

    official_result_eq = _load_official_result_eq() if a.comparator == "official" else None

    rows = [json.loads(l) for l in open(a.candidates)]
    by_db = collections.defaultdict(list)
    for r in rows:
        by_db[r["db_id"]].append(r)

    per_q = {}
    stats = collections.Counter()
    t0 = time.time()

    for db, items in sorted(by_db.items()):
        ddir = os.path.join(a.suite_root, db)
        orig = f"{db}.sqlite"

        # Which instances judge each question. Spider ships one suite per database, so the list
        # is the directory. The text2sql-data tasks ship one suite per QUESTION, carried in the
        # candidates file, and their shipped database holds no rows at all: the official
        # evaluator never executes on it and its own cache key calls it the empty database path.
        # Index 0 is always the weak oracle.
        db_insts = None
        if any(not r.get("instances") for r in items):
            if not os.path.isfile(os.path.join(ddir, orig)):
                continue
            rest = sorted(f for f in os.listdir(ddir) if f.endswith(".sqlite") and f != orig)
            if a.weak_oracle == "original":
                db_insts = [orig] + rest
            else:
                # index 0 must be the weak oracle, so the shipped database leaves the suite
                db_insts = rest
            if a.max_instances:
                db_insts = db_insts[: a.max_instances]

        q_insts = {}
        for r in items:
            insts = list(r["instances"]) if r.get("instances") else db_insts
            if a.max_instances and r.get("instances"):
                insts = insts[: a.max_instances]
            if insts:
                q_insts[r["qid"]] = insts

        # Index positions of the construction and evaluation instance sets, per question.
        # Index 0 is the weak oracle (the original database) and stays in both: a deployed
        # system always has it. Without --instance-folds both sets are every instance, which is
        # the preregistered behaviour.
        # The partition is drawn once per DATABASE over instance FILE NAMES, so a physical suite
        # instance belongs to the same side for every question of that schema. Drawing it per
        # question would put the same file on the construction side of one question and the
        # evaluation side of another, which is not an instance holdout at all.
        db_fold_of = {}
        if a.instance_folds:
            names = sorted({n for insts in q_insts.values() for n in insts[1:]})
            shuffled = list(names)
            random.Random(f"{a.fold_seed}|{db}").shuffle(shuffled)
            for k, n in enumerate(shuffled):
                db_fold_of[n] = k % a.instance_folds
        q_folds = {}
        for qid, insts in q_insts.items():
            idx = list(range(len(insts)))
            k0 = a.construction_fold % a.instance_folds if a.instance_folds else 0
            if a.instance_folds and len(idx) > a.instance_folds:
                c = [0] + [i for i in idx[1:] if db_fold_of.get(insts[i]) == k0]
                e = [0] + [i for i in idx[1:] if db_fold_of.get(insts[i]) != k0]
                q_folds[qid] = (c, e) if len(c) > 1 and len(e) > 1 else (idx, idx)
            else:
                q_folds[qid] = (idx, idx)
        items = [r for r in items if r["qid"] in q_insts]
        if not items:
            continue

        # Which SQL has to run on which instance, so every database opens exactly once.
        # order_matters is a property of the QUESTION's gold, not of the candidate string, and
        # the same candidate can appear under two questions whose golds differ on ORDER BY. So
        # it is part of the cache key; sharing one entry would canonicalise one of them wrongly.
        need_by_inst = collections.defaultdict(set)
        q_need = {}
        for r in items:
            om = bool(re.search(r"\border\s+by\b", r["gold"], re.I))
            need = {r["gold"]: om}
            for c in r["candidates"]:
                if c.get("parsed") and not c.get("truncated") and c["sql"]:
                    need.setdefault(c["sql"], om)
            q_need[r["qid"]] = need
            for inst in q_insts[r["qid"]]:
                need_by_inst[inst].update(need.items())

        cache = {}
        for inst, need in sorted(need_by_inst.items()):
            path = os.path.join(ddir, inst)
            if not os.path.isfile(path):
                stats["missing_instance_file"] += 1
                continue
            con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
            con.text_factory = lambda b: b.decode("utf-8", "replace")
            for sql, om in sorted(need):
                res, err = run(con, sql)
                # A failure is not a result. Two unrelated queries that both raise
                # OperationalError are not equivalent, so the identity of the query stays in the
                # signature and they never merge into one execution class.
                if err:
                    cache[(inst, sql, om)] = "ERR:" + err + ":" + h(sql)[:12]
                elif a.comparator == "official":
                    cache[(inst, sql, om)] = res      # raw rows: result_eq compares them pairwise
                else:
                    cache[(inst, sql, om)] = h(canon(res, om))
            con.close()

        for r in items:
            sig = {sql: [cache.get((i, sql, om), "ERR:MISSING:" + h(sql)[:12])
                         for i in q_insts[r["qid"]]]
                   for sql, om in q_need[r["qid"]].items()}
            gsig = sig[r["gold"]]
            # The gold is the reference for every comparison in this question, so a gold that
            # fails anywhere in its own suite makes the whole question unusable, not just the
            # instance where it failed.
            if any(isinstance(x, str) and x.startswith("ERR") for x in gsig):
                stats["gold_failed_on_its_suite"] += 1
                continue
            cands = [c for c in r["candidates"]
                     if c.get("parsed") and not c.get("truncated") and c["sql"] in sig]
            if not cands:
                stats["no_usable_candidate"] += 1
                continue

            om_q = q_need[r["qid"]][r["gold"]]
            cidx, eidx = q_folds[r["qid"]]
            if a.comparator == "custom":
                # a canonical form: the signature IS the class key
                def key_single(c):
                    return sig[c["sql"]][0]

                def key_multi(c, _c=cidx):
                    return "|".join(sig[c["sql"]][i] for i in _c)

                gold_single = gsig[0]
                gold_multi = "|".join(gsig[i] for i in cidx)
                gold_eval = "|".join(gsig[i] for i in eidx)
                # the custom comparator is a canonical form, so its classes never depended on the
                # gold being in the item list; --partition changes nothing here
                cls_s = lambda sql: sig[sql][0]
                cls_m = lambda sql, _c=cidx: "|".join(sig[sql][i] for i in _c)
                cls_e = lambda sql, _e=eidx: "|".join(sig[sql][i] for i in _e)
            else:
                # a pairwise relation: classes come from union-find, and the gold joins the
                # item list so its class is found by the same procedure as everyone else.
                # Direction rule: result_eq(x, y, order_matters) is called with x = the EARLIER
                # item in the union-find order (gold first, then sampling order) as its first
                # argument and y = the later item as its second.
                def _cell_eq(x, y, om=None):
                    if isinstance(x, str) or isinstance(y, str):
                        return x == y          # an error only equals the identical error
                    return official_result_eq(x, y, om_q if om is None else om)

                has_ob = lambda q: bool(re.search(r"\border\s+by\b", q, re.I))
                om_pair = ((lambda p, q_: om_q) if a.order_rule == "gold"
                           else (lambda p, q_: has_ob(p) or has_ob(q_)))

                order = ([c["sql"] for c in cands] if a.partition == "candidates-only"
                         else [r["gold"]] + [c["sql"] for c in cands])
                seen, sqls = set(), []
                for q_ in order:
                    if q_ not in seen:
                        seen.add(q_); sqls.append(q_)

                cls_single, bad_s = union_find_classes(
                    sqls, lambda x, y: _cell_eq(sig[x][0], sig[y][0], om_pair(x, y)))
                cls_multi, bad_m = union_find_classes(
                    sqls, lambda x, y: all(_cell_eq(sig[x][i], sig[y][i], om_pair(x, y)) for i in cidx))
                if eidx == cidx:
                    cls_evalp = cls_multi
                else:
                    cls_evalp, _ = union_find_classes(
                        sqls, lambda x, y: all(_cell_eq(sig[x][i], sig[y][i], om_pair(x, y)) for i in eidx))
                stats["intransitive_pairs_single"] += bad_s
                stats["intransitive_pairs_multi"] += bad_m
                if bad_s or bad_m:
                    stats["questions_with_intransitivity"] += 1

                def key_single(c, _m=cls_single):
                    return _m[c["sql"]]

                def key_multi(c, _m=cls_multi):
                    return _m[c["sql"]]

                if a.partition == "candidates-only":
                    # No gold in the partition. A class is labelled by comparing its representative
                    # with the gold directly, gold first, which is the same direction rule the
                    # union-find used. GOLD is a sentinel class id that no candidate can carry.
                    GOLD = object()
                    gold_single = gold_multi = gold_eval = GOLD
                    _g = r["gold"]
                    cls_s = lambda sql: (GOLD if _cell_eq(gsig[0], sig[sql][0], om_pair(_g, sql))
                                         else cls_single[sql])
                    cls_m = lambda sql, _c=cidx: (GOLD if all(_cell_eq(gsig[i], sig[sql][i], om_pair(_g, sql)) for i in _c)
                                                  else cls_multi[sql])
                    cls_e = lambda sql, _e=eidx: (GOLD if all(_cell_eq(gsig[i], sig[sql][i], om_pair(_g, sql)) for i in _e)
                                                  else cls_evalp[sql])
                else:
                    gold_single = cls_single[r["gold"]]
                    gold_multi = cls_multi[r["gold"]]
                    gold_eval = cls_evalp[r["gold"]]
                    cls_s = lambda sql, _m=cls_single: _m[sql]
                    cls_m = lambda sql, _m=cls_multi: _m[sql]
                    cls_e = lambda sql, _m=cls_evalp: _m[sql]
            # strong label of a class: does every instance agree with the gold?
            # A real system answers with ONE representative of the chosen class, not the whole
            # class. Under single-instance scoring the members of a class are indistinguishable
            # to the system, so the representative is the most frequent SQL string in it, ties
            # broken lexicographically. A class is judged by its representative; requiring every
            # member to be right would bias the comparison toward the multi-instance arm.
            def rep_of(keyfn):
                bag = collections.defaultdict(collections.Counter)
                for c in cands:
                    bag[keyfn(c)][c["sql"]] += 1
                # most frequent SQL string, ties broken by ordinary ascending lexicographic
                # order. Negating code points reverses the comparison at the first differing
                # character but not for a prefix pair, where the longer string still wins.
                return {k: min(v.items(), key=lambda kv: (-kv[1], kv[0]))[0]
                        for k, v in bag.items()}

            rep_single = rep_of(key_single)
            rep_multi = rep_of(key_multi)
            per_q[r["qid"]] = {
                "db": db,
                "n_total": len(r["candidates"]),
                "n_cand": len(cands),
                "single": collections.Counter(key_single(c) for c in cands),
                "multi": collections.Counter(key_multi(c) for c in cands),
                "gold_single": gold_single,
                "gold_multi": gold_multi,
                "rep_single": rep_single,
                "rep_multi": rep_multi,
                # a class is correct iff its representative lands in the gold's class under the
                # oracle in question. Written as class membership so the custom canonical form
                # and the official pairwise relation go through exactly the same code.
                # correctness for SCORING comes from the evaluation instances
                "single_strong_ok": {k: (cls_e(s) == gold_eval) for k, s in rep_single.items()},
                "multi_strong_ok": {k: (cls_e(s) == gold_eval) for k, s in rep_multi.items()},
                # correctness used to FIT a multi-oracle threshold comes from the construction
                # instances. Without folds the two are the same object, which is the
                # preregistered behaviour; with folds they are the whole point of the cross-fit.
                "single_constr_ok": {k: (cls_m(s) == gold_multi) for k, s in rep_single.items()},
                "multi_constr_ok": {k: (cls_m(s) == gold_multi) for k, s in rep_multi.items()},
                "single_weak_ok": {k: (cls_s(s) == gold_single) for k, s in rep_single.items()},
                "multi_weak_ok": {k: (cls_s(s) == gold_single) for k, s in rep_multi.items()},
            }
            q = per_q[r["qid"]]
            # how often the single-instance partition merges a strong-correct representative
            # with members that are not: this is the label noise the headline claim is about
            for k, s in rep_single.items():
                mem = {cls_e(c["sql"]) for c in cands if key_single(c) == k}
                if len(mem) > 1:
                    stats["single_classes_split_by_strong_oracle"] += 1
                    if q["single_weak_ok"][k]:
                        stats["gold_matching_single_class_is_impure"] += 1
            stats["questions_usable"] += 1

    qids = sorted(per_q)
    if not qids:
        print("no usable questions", file=sys.stderr)
        sys.exit(1)

    # ---- per-cell quantities, recomputed on each random calibration/test split -------------
    def cell_records(scoring, cal_label):
        """For each question: top-class mass, whether the top class is right under the
        CALIBRATION oracle (used to fit) and under the STRONG oracle (used to evaluate),
        plus the class mass vector and the strong-correct class id for set coverage."""
        recs = {}
        for qid in qids:
            q = per_q[qid]
            counter = q[scoring]
            n = q["n_total"] if a.mass_denominator == "budget" else sum(counter.values())
            masses = {k: v / n for k, v in counter.items()}
            top = max(masses, key=lambda k: (masses[k], k))
            weak_ok = q[f"{scoring}_weak_ok"][top]
            strong_ok = q[f"{scoring}_strong_ok"][top]
            fit_ok = weak_ok if cal_label == "single" else q[f"{scoring}_constr_ok"][top]
            # Mass of the class that is correct under the fitting oracle, for set coverage.
            # None, not 0.0, when NO sampled class is correct: with tau == 1 the admission test
            # is mass >= 0, which 0.0 passes, so a question with no correct class at all would
            # be scored as covered. That is how a cell whose model cannot answer reports
            # coverage 1.0000 while its prediction set contains nothing correct.
            fit_c = [m for k, m in masses.items()
                     if (q[f"{scoring}_weak_ok"][k] if cal_label == "single"
                         else q[f"{scoring}_constr_ok"][k])]
            strong_c = [m for k, m in masses.items() if q[f"{scoring}_strong_ok"][k]]
            recs[qid] = {"top_mass": masses[top], "fit_ok": fit_ok, "strong_ok": strong_ok,
                         "fit_mass": max(fit_c) if fit_c else None,
                         "strong_mass": max(strong_c) if strong_c else None,
                         "masses": sorted(masses.values(), reverse=True)}
        return recs

    cells = {}
    per_split = {}
    grid = [round(x, 4) for x in [i / 200 for i in range(200, -1, -1)]]
    # One set of splits, shared by all four cells. Drawing fresh splits per cell leaves the
    # cells unpaired, so an A-vs-D difference then carries the split-to-split noise of two
    # independent draws on top of the effect, and no paired statistic can be formed at all.
    rng = random.Random(a.seed)
    splits = []
    split_info = {"split_by": a.split_by, "n_splits": a.splits}
    if a.split_by == "question":
        for _ in range(a.splits):
            sh = qids[:]
            rng.shuffle(sh)
            half = len(sh) // 2
            splits.append((sh[:half], sh[half:]))
    else:
        # Database-grouped splits: half of the DATABASES calibrate, the other half test, so a
        # schema never sits on both sides. Question counts per side vary with the draw.
        groups = sorted({per_q[q]["db"] for q in qids})
        for _ in range(a.splits):
            sh = groups[:]
            rng.shuffle(sh)
            half = len(sh) // 2
            cal_g = set(sh[:half])
            splits.append(([q for q in qids if per_q[q]["db"] in cal_g],
                           [q for q in qids if per_q[q]["db"] not in cal_g]))
        split_info.update({"n_groups": len(groups), "calibration_groups": len(groups) // 2,
                           "calibration_questions_min": min(len(c) for c, _ in splits),
                           "calibration_questions_max": max(len(c) for c, _ in splits)})

    for scoring in ("single", "multi"):
        for cal in ("single", "multi"):
            recs = cell_records(scoring, cal)
            agg = collections.defaultdict(list)
            for calq, tstq in splits:

                # Method A: split conformal over classes, fitted with the cell's labels
                s_cal = [1.0 if recs[i]["fit_mass"] is None else 1.0 - recs[i]["fit_mass"]
                         for i in calq]
                tau = conformal_quantile(s_cal, a.alpha)
                cov = sum(1 for i in tstq if recs[i]["strong_mass"] is not None
                          and recs[i]["strong_mass"] >= 1.0 - tau) / len(tstq)
                # the same coverage judged by the oracle that FITTED tau. A certificate can hold
                # here and fail above, and that gap is the whole claim: the guarantee is honoured,
                # just on a quantity nobody cares about.
                agg["setcov_fit"].append(
                    sum(1 for i in tstq if recs[i]["fit_mass"] is not None
                        and recs[i]["fit_mass"] >= 1.0 - tau) / len(tstq))
                setsize = statistics.mean(
                    sum(1 for m in recs[i]["masses"] if m >= 1.0 - tau) for i in tstq)
                agg["setcov_strong"].append(cov)
                agg["setsize"].append(setsize)
                agg["tau"].append(tau)

                # Method B: CRC on the marginal wrong-answer loss, fitted with the cell's labels
                fit_items = [(recs[i]["top_mass"], not recs[i]["fit_ok"]) for i in calq]
                lam = crc_lambda(fit_items, a.alpha, grid)
                ans = [i for i in tstq if recs[i]["top_mass"] >= lam]
                marg = sum(1 for i in tstq if recs[i]["top_mass"] >= lam
                           and not recs[i]["strong_ok"]) / len(tstq)
                agg["answer_rate"].append(len(ans) / len(tstq))
                agg["marginal_risk_strong"].append(marg)
                agg["marginal_risk_fit"].append(
                    sum(1 for i in tstq if recs[i]["top_mass"] >= lam
                        and not recs[i]["fit_ok"]) / len(tstq))
                # conditional on answering: undefined, not zero, when nothing is answered
                agg["selective_risk_strong"].append(
                    (sum(1 for i in ans if not recs[i]["strong_ok"]) / len(ans)) if ans else None)
                agg["lambda"].append(lam)

            cells[f"score={scoring}|calib={cal}"] = {k: summarise(v) for k, v in agg.items()}
            per_split[f"score={scoring}|calib={cal}"] = agg

    # ---- descriptive instrument diagnostics ----------------------------------------------
    # Judged on the BASELINE cell alone, with no oracle contrast in it. The instrument-validity
    # gate was retired PROSPECTIVELY in PREREGISTRATION.md; no replacement was invented. These
    # stay descriptive and carry no verdict.
    recA = cell_records("single", "single")
    tm = [recA[q]["top_mass"] for q in qids]
    n_classes = [len(per_q[q]["single"]) for q in qids]
    gate = {
        "mean_top_class_mass": round(statistics.mean(tm), 4),
        "unanimous_fraction": round(sum(1 for x in tm if x >= 1.0) / len(tm), 4),
        "distinct_score_values": len({round(x, 9) for x in tm}),
        "lambda_cell_A": cells["score=single|calib=single"]["lambda"]["mean"],
        "mean_classes_per_question": round(statistics.mean(n_classes), 4),

    }
    # How often the samples contain no correct class at all. Set coverage cannot exceed
    # 1 minus this rate whatever the calibration does: a prediction set that holds no correct
    # class has covered nothing, and no threshold can put a class there that was never sampled.
    recD = cell_records("multi", "multi")
    n_single_classes = sum(len(per_q[q]["single"]) for q in qids)
    gate["single_classes_total"] = n_single_classes
    gate["classes_split_over_classes"] = round(
        stats["single_classes_split_by_strong_oracle"] / n_single_classes, 4) if n_single_classes else None
    gate["impure_gold_class_over_questions"] = round(
        stats["gold_matching_single_class_is_impure"] / len(qids), 4)
    gate["no_correct_class_rate_weak_partition"] = round(
        sum(1 for q in qids if recA[q]["strong_mass"] is None) / len(qids), 4)
    gate["no_correct_class_rate_strong_partition"] = round(
        sum(1 for q in qids if recD[q]["strong_mass"] is None) / len(qids), 4)
    n_total = sum(per_q[q]["n_total"] for q in qids)
    n_usable = sum(per_q[q]["n_cand"] for q in qids)
    gate["usable_candidate_fraction"] = round(n_usable / n_total, 4) if n_total else None
    gate["note"] = ("descriptive only. The instrument-validity gate was retired prospectively in "
                    "PREREGISTRATION.md and has no replacement; instrument validity is checked by "
                    "parse rate, truncation rate and the negative control.")

    # ---- paired contrasts on the shared splits -------------------------------------------
    A = "score=single|calib=single"
    contrasts = {}
    for other in ("score=single|calib=multi", "score=multi|calib=single", "score=multi|calib=multi"):
        c = {}
        for m in ("setcov_strong", "marginal_risk_strong", "answer_rate", "selective_risk_strong"):
            p = paired(per_split[A][m], per_split[other][m])
            c[m] = {"mean_change_vs_A": p["mean"], "sd_of_paired_diff": p["sd_of_paired_diff"],
                    "splits_with_same_sign": p["splits_with_same_sign"],
                    "splits_with_zero_diff": p["splits_with_zero_diff"]}
            if "n_splits_used" in p:
                c[m]["n_splits_used"] = p["n_splits_used"]
        contrasts[other] = c

    # The ORACLE GAP: within cell A, the same threshold judged by the labels that fitted it
    # versus by the strong oracle. It is a different quantity from the D-A repair contrast, and
    # its split-level sign consistency has to be computed separately rather than borrowed from it.
    oracle_gap = {
        "marginal_risk_strong_minus_fit": paired(per_split[A]["marginal_risk_fit"],
                                                 per_split[A]["marginal_risk_strong"]),
        "setcov_fit_minus_strong": paired(per_split[A]["setcov_strong"], per_split[A]["setcov_fit"]),
        "note": ("the splits share questions and overlap heavily, so a same-sign proportion "
                 "is a descriptive statement about resplit stability and is NOT a confidence level"),
    }

    # ---- per-question class counts, to a sibling file ------------------------------------
    pq_path = a.per_question_out or re.sub(r"\.json$", "", a.out) + "_per_question.json"

    def classes_of(q, part):
        # class_key is the analyser's own key for the class: the union-find id under the official
        # comparator, the canonical signature under the custom one. It is emitted because the
        # analyser breaks a tie for the top class by the LARGER key while this list is ordered by
        # (-count, str(key)), and without the key a recomputation cannot tell the two apart.
        return [{"class_key": k, "count": v,
                 "weak_ok": q[f"{part}_weak_ok"][k], "strong_ok": q[f"{part}_strong_ok"][k],
                 "constr_ok": q[f"{part}_constr_ok"][k], "representative": q[f"rep_{part}"][k]}
                for k, v in sorted(q[part].items(), key=lambda kv: (-kv[1], str(kv[0])))]

    per_question = {
        "candidates": a.candidates, "comparator": a.comparator, "weak_oracle": a.weak_oracle,
        "note": "classes sorted by (-count, str(class_key)); a class is correct iff its "
                "representative lands in the gold's class under the named oracle; "
                "mass = count / denominator. The analyser breaks a tie for the top class "
                "by the largest class_key, which is not the order of this list, so a "
                "recomputation that wants the analyser's own choice must read class_key.",
        "questions": [{"qid": q, "db": per_q[q]["db"], "n_total": per_q[q]["n_total"],
                       "n_usable": per_q[q]["n_cand"],
                       "single": classes_of(per_q[q], "single"),
                       "multi": classes_of(per_q[q], "multi")} for q in qids],
    }
    json.dump(per_question, open(pq_path, "w"), indent=1, ensure_ascii=False)

    # ---- provenance ----------------------------------------------------------------------
    meta_path = re.sub(r"\.jsonl$", "_meta.json", a.candidates)
    cand_meta = json.load(open(meta_path)) if os.path.isfile(meta_path) else None
    provenance = {
        "candidates_path": a.candidates,
        "candidates_sha256": sha256_file(a.candidates),
        "candidates_meta": {k: cand_meta.get(k) for k in
                            ("model", "arm", "questions", "samples_per_question", "sampling_policy",
                             "encoder", "template", "chat_template_kwargs", "system_prompt",
                             "negative_control", "instrument_checks")} if cand_meta else None,
        "suite_root": a.suite_root,
        "official_evaluator": ("data/spider/exec_eval.py" if a.comparator == "official" else None),
        "official_evaluator_sha256": (sha256_file("data/spider/exec_eval.py")
                                      if a.comparator == "official" else None),
        "analyser": os.path.relpath(os.path.abspath(__file__)),
        "analyser_sha256": sha256_file(os.path.abspath(__file__)),
        "git": git_state(),
        "python": sys.version.split()[0],
        "options": {"alpha": a.alpha, "splits": a.splits, "analysis_seed": a.seed,
                    "max_instances": a.max_instances, "comparator": a.comparator,
                    "instance_folds": a.instance_folds, "construction_fold": a.construction_fold,
                    "fold_seed": a.fold_seed, "partition": a.partition, "order_rule": a.order_rule,
                    "weak_oracle": a.weak_oracle, "split_by": a.split_by,
                    "mass_denominator": a.mass_denominator},
        "per_question_file": pq_path,
        "per_question_sha256": sha256_file(pq_path),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    definitions = {
        "setcov_strong / setcov_fit": (
            "sampled-candidate-set coverage: fraction of test questions whose prediction set, "
            "formed over the SAMPLED execution classes at threshold tau, contains a class that is "
            "correct under the strong oracle / under the oracle that fitted tau. Bounded above by "
            "1 - no_correct_class_rate; not the unconditional coverage of an oracle-complete set."),
        "marginal_risk_strong / marginal_risk_fit": (
            "fraction of test questions that are answered (top-class mass >= lambda) AND wrong "
            "under the strong oracle / under the oracle that fitted lambda; the CRC-controlled loss."),
        "selective_risk_strong": (
            "wrong-answer rate among answered test questions; undefined (null) on a split with "
            "no answered question; means are over defined splits, n_splits_undefined is reported."),
        "answer_rate": "fraction of test questions with top-class mass >= lambda",
        "tau / lambda": "split-conformal quantile / CRC threshold fitted on the calibration half",
        "mass_denominator": a.mass_denominator,
        "class_representative": ("most frequent SQL string in the class; ties broken by ascending "
                                 "lexicographic order of the SQL string"),
        "top_class_tie_break": "highest mass; ties broken by the larger class key",
        "union_find_order": ("official comparator only: gold first, then candidates in sampling "
                             "order, first occurrence of each distinct SQL string; result_eq is "
                             "called with the earlier item as its first argument"),
        "paired_statistics": ("mean and population sd of the per-split difference; strict sign "
                              "counting with zero differences counted apart; splits overlap, so "
                              "same-sign proportions are not confidence levels"),
    }

    base_strong = sum(1 for q in qids if recA[q]["strong_ok"]) / len(qids)
    out = {
        "experiment": "E0 oracle intervention 2x2",
        "provenance": provenance,
        "alpha": a.alpha,
        "weak_oracle": a.weak_oracle,
        "comparator": a.comparator,
        "repeated_splits": a.splits,
        "split_info": split_info,
        "questions_usable": len(qids),
        "counters": dict(stats),
        "top1_accuracy_under_strong_oracle": round(base_strong, 4),
        "instrument_diagnostics": gate,
        "oracle_gap_within_cell_A": oracle_gap,
        "paired_contrasts_vs_cell_A": contrasts,
        "cells": cells,
        "definitions": definitions,
        "reading": ("Every cell is evaluated against the STRONG oracle. A = score single, "
                    "calib single is current practice. Compare A with D."),
        "wall_clock_sec": round(time.time() - t0, 1),
    }
    json.dump(out, open(a.out, "w"), indent=1, ensure_ascii=False)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
