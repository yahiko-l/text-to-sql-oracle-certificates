#!/usr/bin/env python3
"""C6 step 1: build the evidence file for the semantic audit of weak-correct, strong-wrong answers.

The headline result rests on answers that the weak oracle (the one shipped benchmark database)
accepts and the strong oracle (every instance of the distilled test suite) rejects. That gap is
only a measurement of certificate under-reporting if those rejections are genuine semantic errors.
If a large share of them are the suite splitting hairs the natural-language question never asked
about, the same numbers mean something much weaker. This script prepares the evidence needed to
decide that, and decides nothing itself.

The population is every weak-correct, strong-wrong ANSWER in the twelve preregistered pools: for
each (model, seed, question) the top class of the single-instance partition, its representative
being what a deployed system would return. Answers collapse to distinct (question, representative)
CASES, because the same SQL string under the same question is the same semantic question however
many pools produced it. This is a census of that population, not a sample.

For each case the script re-executes the gold and the representative on the original database and
on every suite instance, using the same comparator, the same direction rule (gold first) and the
same order_matters convention (a property of the gold) as the frozen analyser, and records:

  - the per-instance verdict, how many instances disagree, and which one disagrees first
  - both result tables on that first disagreeing instance, capped for readability
  - a mechanical diff signature (row order only, duplicate multiplicity, subset, column count,
    disjointness, empties) that describes WHAT differs without saying what it means
  - surface features of both queries

The signature is descriptive. Classification into a genuine semantic error or an artifact of the
oracle happens in c6_classify.py against a written rule set, and every case is put to an AI
reviewer, so that the labels are not assigned by the party whose headline claim they test.
"""
import argparse, collections, importlib.util, json, os, re, sqlite3, sys, time, warnings

MODELS = ["kwai-autosql-32b", "kwai-autosql-14b", "omnisql-32b", "xiyansql-32b"]
SEEDS = ["seed101", "seed202", "seed303"]
ROW_CAP = 12          # rows shown per table in the evidence file
CELL_CAP = 60         # characters per cell


def load_result_eq(path):
    sys.path.insert(0, os.path.dirname(os.path.abspath(path)))
    warnings.filterwarnings("ignore", category=SyntaxWarning)
    spec = importlib.util.spec_from_file_location("official_exec_eval", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.result_eq


def run(con, sql, budget=2_000_000):
    """Identical to the analyser's runner: same progress budget, same error reporting."""
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


def refinement_check(prefix, arm):
    """Verify the claim the whole audit rests on: the strong label refines the weak one.

    If some class were strong-correct and weak-wrong, the two oracles would disagree in both
    directions, the audited population would be only half of the disagreement, and GAP would have
    a second source this census never looked at. The check is cheap and the claim is load-bearing,
    so it runs on every build rather than being asserted in prose.
    """
    seen = both = 0
    for m in MODELS:
        for s in SEEDS:
            for q in json.load(open(f"{prefix}_{m}_{s}_{arm}_per_question.json"))["questions"]:
                for c in q["single"]:
                    seen += 1
                    if c["strong_ok"] and not c["weak_ok"]:
                        both += 1
    return {"classes_examined": seen, "strong_correct_but_weak_wrong": both,
            "strong_refines_weak": both == 0}


def features(sql):
    s = " " + re.sub(r"\s+", " ", sql).lower() + " "
    aggs = sorted({a for a in ("count", "sum", "avg", "min", "max")
                   if re.search(rf"\b{a}\s*\(", s)})
    return {"distinct": bool(re.search(r"\bdistinct\b", s)),
            "limit": bool(re.search(r"\blimit\b", s)),
            "order_by": bool(re.search(r"\border\s+by\b", s)),
            "group_by": bool(re.search(r"\bgroup\s+by\b", s)),
            "having": bool(re.search(r"\bhaving\b", s)),
            "join": len(re.findall(r"\bjoin\b", s)),
            "subquery": s.count("(select"),
            "set_op": bool(re.search(r"\b(union|intersect|except)\b", s)),
            "aggregates": aggs,
            "n_where_terms": len(re.findall(r"\b(and|or)\b", s.split(" where ")[-1])) + 1
                             if " where " in s else 0}


def cap(rows):
    out = []
    for r in rows[:ROW_CAP]:
        out.append([(v if not isinstance(v, str) or len(v) <= CELL_CAP else v[:CELL_CAP] + "...")
                    for v in r])
    return out


def diff_signature(g, r):
    """What differs between two result tables. Descriptive only: no verdict is implied."""
    sg, sr = collections.Counter(map(tuple, g)), collections.Counter(map(tuple, r))
    setg, setr = set(sg), set(sr)
    d = {"n_rows_gold": len(g), "n_rows_rep": len(r),
         "n_cols_gold": len(g[0]) if g else None, "n_cols_rep": len(r[0]) if r else None,
         "gold_empty": not g, "rep_empty": not r,
         "col_count_differs": bool(g and r and len(g[0]) != len(r[0])),
         "row_order_only": bool(g and r and list(map(tuple, g)) != list(map(tuple, r)) and sg == sr),
         "duplicate_multiplicity_only": bool(g and r and setg == setr and sg != sr),
         "rep_subset_of_gold": bool(r and setr < setg),
         "gold_subset_of_rep": bool(g and setg < setr),
         "disjoint": bool(g and r and not (setg & setr)),
         "rows_shared": len(setg & setr), "rows_gold_only": len(setg - setr),
         "rows_rep_only": len(setr - setg)}
    d["scalar_pair"] = bool(len(g) == 1 and len(r) == 1 and g and r
                            and len(g[0]) == 1 and len(r[0]) == 1)
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--suite-root", default="data/spider/test_suite_database")
    ap.add_argument("--evaluator", default="data/spider/exec_eval.py")
    ap.add_argument("--prefix", default="experiments/c4")
    ap.add_argument("--arm", default="results_official",
                    help="which analyser arm defines the population; the preregistered primary")
    ap.add_argument("--out", default="experiments/c6_semantic_cases.json")
    a = ap.parse_args()
    result_eq = load_result_eq(a.evaluator)

    # 1. population: every weak-correct, strong-wrong top single-instance class in the 12 pools
    answers = []
    pool_sizes = {}
    for m in MODELS:
        for s in SEEDS:
            p = f"{a.prefix}_{m}_{s}_{a.arm}_per_question.json"
            d = json.load(open(p))
            pool_sizes[f"{m}/{s}"] = len(d["questions"])
            for q in d["questions"]:
                cls = q["single"]
                mx = max(c["count"] for c in cls)
                top = [c for c in cls if c["count"] == mx]
                c0 = top[0]
                if c0["weak_ok"] and not c0["strong_ok"]:
                    answers.append({"model": m, "seed": s, "qid": q["qid"], "db": q["db"],
                                    "rep": c0["representative"], "class_count": c0["count"],
                                    "n_usable": q["n_usable"], "count_tie": len(top) > 1})

    refine = refinement_check(a.prefix, a.arm)
    print(f"  refinement check: {refine['classes_examined']} classes, "
          f"{refine['strong_correct_but_weak_wrong']} strong-correct and weak-wrong")
    if not refine["strong_refines_weak"]:
        raise SystemExit("the strong label does not refine the weak one; this census would be "
                         "only half the disagreement and the audit design does not hold")

    # 2. question text and gold, from any pool that carries the question
    meta = {}
    for m in MODELS:
        for s in SEEDS:
            path = f"{a.prefix}_{m}_{s}_candidates.jsonl"
            if not os.path.isfile(path):
                continue
            for line in open(path):
                r = json.loads(line)
                meta.setdefault(r["qid"], {"question": r["question"], "gold": r["gold"],
                                           "db": r["db_id"]})
            break
        if meta:
            break

    cases = collections.OrderedDict()
    for x in answers:
        k = (x["qid"], x["rep"])
        c = cases.setdefault(k, {"qid": x["qid"], "db": x["db"], "rep": x["rep"],
                                 "question": meta[x["qid"]]["question"],
                                 "gold": meta[x["qid"]]["gold"], "answers": []})
        c["answers"].append({"model": x["model"], "seed": x["seed"],
                             "class_count": x["class_count"], "n_usable": x["n_usable"],
                             "count_tie": x["count_tie"]})
    for i, c in enumerate(cases.values()):
        c["case_id"] = f"C{i + 1:03d}"

    # 3. execute, one database at a time, one connection per instance
    by_db = collections.defaultdict(list)
    for c in cases.values():
        by_db[c["db"]].append(c)
    t0 = time.time()
    for db, cs in sorted(by_db.items()):
        ddir = os.path.join(a.suite_root, db)
        orig = f"{db}.sqlite"
        insts = [orig] + sorted(f for f in os.listdir(ddir) if f.endswith(".sqlite") and f != orig)
        need = set()
        for c in cs:
            need.add(c["gold"])
            need.add(c["rep"])
        rows = {}
        for inst in insts:
            con = sqlite3.connect(f"file:{os.path.join(ddir, inst)}?mode=ro", uri=True)
            con.text_factory = lambda b: b.decode("utf-8", "replace")
            for sql in sorted(need):
                res, err = run(con, sql)
                rows[(inst, sql)] = ("ERR:" + err) if err else res
            con.close()
        for c in cs:
            om = bool(re.search(r"\border\s+by\b", c["gold"], re.I))
            c["order_matters"] = om
            c["n_instances"] = len(insts)
            verdicts, errs = [], []
            for inst in insts:
                g, r = rows[(inst, c["gold"])], rows[(inst, c["rep"])]
                if isinstance(g, str) or isinstance(r, str):
                    verdicts.append(g == r)
                    errs.append({"instance": inst, "gold": g if isinstance(g, str) else None,
                                 "rep": r if isinstance(r, str) else None})
                else:
                    verdicts.append(bool(result_eq(g, r, om)))
            c["errors"] = errs
            c["agree_on_original"] = verdicts[0]
            dis = [i for i, v in enumerate(verdicts) if not v]
            c["n_disagree"] = len(dis)
            c["disagree_fraction"] = round(len(dis) / len(insts), 4)
            if dis:
                w = insts[dis[0]]
                c["witness_instance"] = w
                g, r = rows[(w, c["gold"])], rows[(w, c["rep"])]
                if isinstance(g, str) or isinstance(r, str):
                    c["witness"] = {"execution_error": True,
                                    "gold": g if isinstance(g, str) else "ok",
                                    "rep": r if isinstance(r, str) else "ok"}
                else:
                    c["witness"] = {"execution_error": False, **diff_signature(g, r),
                                    "gold_rows": cap(g), "rep_rows": cap(r),
                                    "gold_truncated": len(g) > ROW_CAP,
                                    "rep_truncated": len(r) > ROW_CAP}
            else:
                c["witness_instance"] = None
                c["witness"] = None
            c["features_gold"] = features(c["gold"])
            c["features_rep"] = features(c["rep"])
        print(f"  {db:30s} cases={len(cs):3d} instances={len(insts):3d} "
              f"queries={len(need)} t={time.time() - t0:.0f}s", flush=True)

    out = {
        "built": time.strftime("%Y-%m-%d"),
        "population": {
            "title": "weak-correct, strong-wrong answers",
            "definition": "top class of the single-instance partition whose representative the "
                          "weak oracle accepts and the strong oracle rejects",
            "arm": a.arm, "pools": pool_sizes,
            "answers_examined": sum(pool_sizes.values()),
            "weak_correct_strong_wrong_answers": len(answers),
            "distinct_cases": len(cases),
            "distinct_questions": len({c["qid"] for c in cases.values()}),
            "census": True,
        },
        "refinement_check": refine,
        "method": {
            "comparator": "official result_eq from the vendored evaluator, called gold first",
            "order_matters": "property of the question's gold, the preregistered order rule",
            "weak_oracle": "instance index 0, the shipped benchmark database",
            "strong_oracle": "every suite instance of the database",
            "note": "verdicts here are direct pairwise gold-versus-representative comparisons. "
                    "The analyser labels a class by union-find membership, so a representative "
                    "can inherit a label transitively; agree_on_original records the direct "
                    "comparison and disagreement with the stored weak label is itself a finding.",
        },
        "cases": list(cases.values()),
    }
    json.dump(out, open(a.out, "w"), indent=1, ensure_ascii=False)
    d = out["population"]
    print(f"\n{d['weak_correct_strong_wrong_answers']} answers -> {d['distinct_cases']} cases "
          f"over {d['distinct_questions']} questions, {time.time() - t0:.0f}s")
    n_direct = sum(1 for c in cases.values() if not c["agree_on_original"])
    print(f"cases where the direct comparison already disagrees on the original database: {n_direct}")
    print(f"cases with no disagreeing instance at all: "
          f"{sum(1 for c in cases.values() if c['n_disagree'] == 0)}")


if __name__ == "__main__":
    main()
