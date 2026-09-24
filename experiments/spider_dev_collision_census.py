#!/usr/bin/env python3
"""The collision census: how many shipped-database collisions between questions survive the suite.

Two questions on the same schema collide on the shipped database when their reference queries differ
but return the same result there. For every such pair on official Spider dev, both reference queries
are executed on every instance of the schema's distilled test suite, and the pair survives if the
two results agree on all of them. A surviving pair is one that execution cannot tell apart; a pair
that diverges on some instance collided only because of the data the shipped database holds. The
same counts are also given for the pairs whose shipped-database result is not degenerate (empty,
all NULL, or a single zero or empty value).

Results are compared under the order-conditional canonical comparison: values are stringified,
floats are rounded to six decimals, column order is kept, and rows are sorted unless the reference
query contains ORDER BY. One of the two pilot measurements that motivated the intervention.
Read-only on every database; no GPU.
"""
import argparse, collections, hashlib, json, os, re, sqlite3, sys, time

NULL = "\x00NULL"


def canon_value(v):
    if v is None:
        return NULL
    if isinstance(v, float):
        return str(int(v)) if v == int(v) else f"{v:.6f}"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, bytes):
        return v.decode("utf-8", "replace")
    return str(v)


def canon_result(rows, order_matters):
    """Rows keep their order only when the reference query has ORDER BY; columns keep theirs."""
    tup = [tuple(canon_value(v) for v in r) for r in rows]
    return tup if order_matters else sorted(tup)


def result_hash(rows, order_matters):
    return hashlib.sha1(
        json.dumps(canon_result(rows, order_matters), ensure_ascii=False).encode()
    ).hexdigest()


def norm_sql(s):
    return re.sub(r"\s+", " ", s.strip().rstrip(";").lower())


def is_degenerate(rows):
    if not rows:
        return True
    flat = [v for r in rows for v in r]
    if all(v is None for v in flat):
        return True
    if len(rows) == 1 and len(rows[0]) == 1:
        v = rows[0][0]
        if v is None or v == "" or (isinstance(v, (int, float)) and v == 0):
            return True
    return False


def run(con, sql, budget=4_000_000):
    n = [0]
    hit = {"v": False}

    def prog():
        n[0] += 1
        if n[0] > budget:
            hit["v"] = True
            return 1
        return 0

    con.set_progress_handler(prog, 10000)
    try:
        return con.execute(sql).fetchall(), None
    except Exception as e:
        return None, ("TIMEOUT" if hit["v"] else type(e).__name__)
    finally:
        con.set_progress_handler(None, 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev", default="data/spider/dev.json")
    ap.add_argument("--suite-root", default="data/spider/test_suite_database")
    ap.add_argument("--out", default="experiments/spider_dev_collision_census.json")
    ap.add_argument("--max-instances", type=int, default=0, help="0 = use all")
    a = ap.parse_args()

    dev = json.load(open(a.dev))
    by_db = collections.defaultdict(list)
    for i, r in enumerate(dev):
        by_db[r["db_id"]].append({**r, "qid": i})

    per_db_report = {}
    tot = collections.Counter()
    t0 = time.time()

    for db, items in sorted(by_db.items()):
        ddir = os.path.join(a.suite_root, db)
        if not os.path.isdir(ddir):
            print(f"  SKIP {db}: no suite", file=sys.stderr)
            continue
        # The suite directory holds the shipped database under the schema's own name; it comes
        # first, and the collisions are counted on it.
        allf = sorted(f for f in os.listdir(ddir) if f.endswith(".sqlite"))
        orig = f"{db}.sqlite"
        if orig not in allf:
            print(f"  SKIP {db}: shipped database not in suite", file=sys.stderr)
            continue
        rest = [f for f in allf if f != orig]
        if a.max_instances:
            rest = rest[: max(0, a.max_instances - 1)]
        insts = [orig] + rest

        # signature per question: tuple of per-instance result hashes ("ERR" where it failed)
        sigs = {}
        first = {}
        errs = collections.Counter()
        for it in items:
            om = "order by" in it["query"].lower()
            it["order_matters"] = om
        for inst in insts:
            path = os.path.join(ddir, inst)
            con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
            con.text_factory = lambda b: b.decode("utf-8", "replace")
            for it in items:
                rows, err = run(con, it["query"])
                if err:
                    h = "ERR:" + err
                    errs[err] += 1
                else:
                    h = result_hash(rows, it["order_matters"])
                    if inst == orig:
                        first[it["qid"]] = {"h": h, "deg": is_degenerate(rows)}
                sigs.setdefault(it["qid"], []).append(h)
            con.close()

        # usable questions: the reference query executes on the shipped database
        usable = [it for it in items if it["qid"] in first]
        # collisions: the same result on the shipped database, different reference SQL
        g1 = collections.defaultdict(list)
        for it in usable:
            g1[first[it["qid"]]["h"]].append(it)
        single_pairs = set()
        for h, grp in g1.items():
            if len(grp) < 2:
                continue
            for i in range(len(grp)):
                for j in range(i + 1, len(grp)):
                    if norm_sql(grp[i]["query"]) != norm_sql(grp[j]["query"]):
                        single_pairs.add((grp[i]["qid"], grp[j]["qid"]))
        # survivors: the same result on every instance
        survivors = set()
        for (x, y) in single_pairs:
            if sigs[x] == sigs[y]:
                survivors.add((x, y))

        deg = {it["qid"]: first[it["qid"]]["deg"] for it in usable}
        single_nd = {p for p in single_pairs if not deg[p[0]] and not deg[p[1]]}
        surv_nd = {p for p in survivors if not deg[p[0]] and not deg[p[1]]}

        per_db_report[db] = {
            "questions": len(items),
            "usable": len(usable),
            "instances": len(insts),
            "exec_errors": dict(errs),
            "single_instance_collision_pairs": len(single_pairs),
            "survive_all_instances": len(survivors),
            "survival_rate": round(len(survivors) / len(single_pairs), 4) if single_pairs else None,
            "single_instance_pairs_nondegenerate": len(single_nd),
            "survive_nondegenerate": len(surv_nd),
            "survival_rate_nondegenerate": round(len(surv_nd) / len(single_nd), 4) if single_nd else None,
        }
        tot["single"] += len(single_pairs)
        tot["surv"] += len(survivors)
        tot["single_nd"] += len(single_nd)
        tot["surv_nd"] += len(surv_nd)
        tot["q"] += len(items)
        tot["inst"] += len(insts)
        print(f"  {db:32s} q={len(items):4d} inst={len(insts):3d} "
              f"pairs={len(single_pairs):5d} survive={len(survivors):5d} "
              f"({per_db_report[db]['survival_rate']})", flush=True)

    out = {
        "split": "Spider dev (official, 1034 questions, 20 databases)",
        "oracle": "shipped database vs distilled test suite, order-conditional canonical comparison",
        "questions": tot["q"],
        "total_instances": tot["inst"],
        "single_instance_collision_pairs": tot["single"],
        "survive_all_instances": tot["surv"],
        "overall_survival_rate": round(tot["surv"] / tot["single"], 4) if tot["single"] else None,
        "single_instance_pairs_nondegenerate": tot["single_nd"],
        "survive_nondegenerate": tot["surv_nd"],
        "overall_survival_rate_nondegenerate": round(tot["surv_nd"] / tot["single_nd"], 4) if tot["single_nd"] else None,
        "per_database": per_db_report,
        "wall_clock_sec": round(time.time() - t0, 1),
    }
    json.dump(out, open(a.out, "w"), indent=1, ensure_ascii=False)
    print("\n" + json.dumps({k: v for k, v in out.items() if k != "per_database"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
