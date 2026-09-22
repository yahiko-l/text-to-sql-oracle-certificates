#!/usr/bin/env python3
"""C7 step 1: build the evidence file for the semantic audit of REPAIR.

The GAP audit (c6) covered the answers the two oracles disagree about, which is all GAP needs.
REPAIR needs more. It is the paired change in strong-oracle risk from the current-practice cell to
the strong-partition, strong-label cell, so an answer counts against it whenever the strong oracle
rejects it, whether or not the shipped database agrees. Two consequences:

  - cell A's wrong answers include the ones BOTH oracles reject, which c6 never looked at because
    they cancel out of GAP;
  - cell D answers with the representative of a multi-instance class, a different SQL string from
    cell A's on the questions where the two partitions disagree.

So the population here is every answer either cell returns that the strong oracle rejects, over the
twelve preregistered pools, deduplicated to distinct (question, returned SQL) cases. Cases already
audited under c6 are carried over by id rather than re-judged, so the two audits stay one labelling.

A case is recorded with the cell or cells that return it, because a reader of the REPAIR result
needs to know whether an exculpated answer sits in the cell being praised or the cell being
criticised. Everything else follows c6 exactly: same comparator, same direction rule, same
order_matters convention, same mechanical diff signature, same reviewer protocol, and no
classification performed here.

One thing genuinely differs and the reviewer prompt has to say so. In c6 every case agreed on the
shipped benchmark database by construction, so the first disagreeing instance was always a generated
one. Here a case can already disagree on the shipped database, and that database is not generated:
calling such a case an instance defect means arguing the benchmark's own database is defective,
which is a much stronger claim than arguing a distilled instance is.
"""
import argparse, collections, json, os, sqlite3, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c6_semantic_cases import (MODELS, SEEDS, ROW_CAP, cap, diff_signature, features,  # noqa: E402
                               load_result_eq, refinement_check, run)
import re  # noqa: E402


def top_class(cls):
    """The class the certificate answers with, under the file-order tie rule."""
    mx = max(c["count"] for c in cls)
    return next(c for c in cls if c["count"] == mx)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--suite-root", default="data/spider/test_suite_database")
    ap.add_argument("--evaluator", default="data/spider/exec_eval.py")
    ap.add_argument("--prefix", default="experiments/c4")
    ap.add_argument("--arm", default="results_official")
    ap.add_argument("--carry-over", default="experiments/c6_semantic_cases.json",
                    help="cases already audited under c6; carried by id, never re-judged")
    ap.add_argument("--out", default="experiments/c7_repair_cases.json")
    a = ap.parse_args()
    result_eq = load_result_eq(a.evaluator)

    prior = {}
    if os.path.isfile(a.carry_over):
        for c in json.load(open(a.carry_over))["cases"]:
            prior[(c["qid"], c["rep"])] = c["case_id"]

    # 1. population: every answer either cell returns that the strong oracle rejects
    answers = []
    pool_sizes = {}
    same_rep = total = 0
    for m in MODELS:
        for s in SEEDS:
            d = json.load(open(f"{a.prefix}_{m}_{s}_{a.arm}_per_question.json"))
            pool_sizes[f"{m}/{s}"] = len(d["questions"])
            for q in d["questions"]:
                total += 1
                cellA, cellD = top_class(q["single"]), top_class(q["multi"])
                if cellA["representative"] == cellD["representative"]:
                    same_rep += 1
                for cell, c, n in (("A", cellA, sum(x["count"] for x in q["single"])),
                                   ("D", cellD, sum(x["count"] for x in q["multi"]))):
                    if not c["strong_ok"]:
                        answers.append({"model": m, "seed": s, "qid": q["qid"], "db": q["db"],
                                        "rep": c["representative"], "cell": cell,
                                        "class_count": c["count"], "n_usable": n,
                                        "weak_ok": c["weak_ok"]})

    meta = {}
    for m in MODELS:
        for s in SEEDS:
            path = f"{a.prefix}_{m}_{s}_candidates.jsonl"
            if os.path.isfile(path):
                for line in open(path):
                    r = json.loads(line)
                    meta.setdefault(r["qid"], {"question": r["question"], "gold": r["gold"]})
                break
        if meta:
            break

    cases = collections.OrderedDict()
    for x in answers:
        k = (x["qid"], x["rep"])
        c = cases.setdefault(k, {"qid": x["qid"], "db": x["db"], "rep": x["rep"],
                                 "question": meta[x["qid"]]["question"],
                                 "gold": meta[x["qid"]]["gold"], "answers": [], "cells": set()})
        c["answers"].append({"model": x["model"], "seed": x["seed"], "cell": x["cell"],
                             "class_count": x["class_count"], "n_usable": x["n_usable"],
                             "weak_ok": x["weak_ok"]})
        c["cells"].add(x["cell"])
    n_new = 0
    for k, c in cases.items():
        c["cells"] = "".join(sorted(c["cells"]))
        c["carried_over_from"] = prior.get(k)
        if c["carried_over_from"] is None:
            n_new += 1
            c["case_id"] = f"R{n_new:03d}"
        else:
            c["case_id"] = c["carried_over_from"]

    # 2. execute, one database at a time
    by_db = collections.defaultdict(list)
    for c in cases.values():
        by_db[c["db"]].append(c)
    t0 = time.time()
    for db, cs in sorted(by_db.items()):
        ddir = os.path.join(a.suite_root, db)
        orig = f"{db}.sqlite"
        insts = [orig] + sorted(f for f in os.listdir(ddir) if f.endswith(".sqlite") and f != orig)
        need = {c["gold"] for c in cs} | {c["rep"] for c in cs}
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
                c["witness_is_shipped_database"] = (w == orig)
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
                c["witness_instance"] = c["witness"] = None
                c["witness_is_shipped_database"] = None
            c["features_gold"] = features(c["gold"])
            c["features_rep"] = features(c["rep"])
        print(f"  {db:30s} cases={len(cs):3d} instances={len(insts):3d} queries={len(need)} "
              f"t={time.time() - t0:.0f}s", flush=True)

    cl = collections.Counter(c["cells"] for c in cases.values())
    out = {
        "built": time.strftime("%Y-%m-%d"),
        "refinement_check": refinement_check(a.prefix, a.arm),
        "population": {
            "title": "every wrong answer of the two cells REPAIR contrasts",
            "definition": "every answer either the current-practice cell A or the strong cell D "
                          "returns and the strong oracle rejects",
            "arm": a.arm, "pools": pool_sizes,
            "answers_examined_per_cell": total,
            "cells_return_the_same_sql": same_rep,
            "cells_return_the_same_sql_share": round(same_rep / total, 4),
            "wrong_answers": len(answers),
            "distinct_cases": len(cases),
            "cases_by_cell": dict(cl),
            "carried_over_from_c6": sum(1 for c in cases.values() if c["carried_over_from"]),
            "new_cases": n_new,
            "distinct_questions": len({c["qid"] for c in cases.values()}),
            "already_disagree_on_the_shipped_database":
                sum(1 for c in cases.values() if not c["agree_on_original"]),
            "census": True,
        },
        "method": {
            "comparator": "official result_eq from the vendored evaluator, called gold first",
            "order_matters": "property of the question's gold, the preregistered order rule",
            "note": "identical to c6 except for the population. A case whose witness is the "
                    "shipped database differs from the gold on a database the benchmark itself "
                    "provides, so exculpating it as an instance defect is a claim about the "
                    "benchmark's own database, not about a generated one.",
        },
        "cases": list(cases.values()),
    }
    json.dump(out, open(a.out, "w"), indent=1, ensure_ascii=False)
    p = out["population"]
    print(f"\n{p['wrong_answers']} wrong answers over both cells -> {p['distinct_cases']} cases "
          f"over {p['distinct_questions']} questions, {time.time() - t0:.0f}s")
    print(f"cells return the same SQL on {p['cells_return_the_same_sql_share']:.1%} of answers")
    print(f"by cell: {p['cases_by_cell']}")
    print(f"carried over from c6: {p['carried_over_from_c6']}, new to judge: {p['new_cases']}")
    print(f"already disagree on the shipped database: "
          f"{p['already_disagree_on_the_shipped_database']}")


if __name__ == "__main__":
    main()
