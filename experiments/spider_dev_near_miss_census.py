#!/usr/bin/env python3
"""The near-miss census: how often the shipped database accepts a query whose meaning changed.

Each reference query of official Spider dev receives single-edit mutations: a flipped comparison, a
reversed or added ordering direction, a LIMIT one higher, a dropped DISTINCT, a dropped AND conjunct
of the WHERE clause, and a swapped aggregate. The reference query and each mutant are executed on
every instance of the schema's distilled test suite. A mutant changed meaning if its result differs
from the reference result on at least one instance, and the reported quantity is the fraction of
those mutants whose result on the shipped database alone equals the reference result: how often a
single-database oracle scores such a near miss correct.

Results are compared under the order-conditional canonical comparison: values are stringified,
floats are rounded to six decimals, column order is kept, and rows are sorted unless the reference
query contains ORDER BY. The same fraction is also given under five variants of that comparison,
overall and per mutation family. One of the two pilot measurements that motivated the intervention.
Read-only on every database; no GPU.
"""
import argparse, collections, hashlib, json, os, re, sqlite3, sys, time

NULL = "\x00NULL"


# ---------------------------------------------------------------- canonicalisers
def _val(v, float_round=True):
    if v is None:
        return NULL
    if isinstance(v, float):
        if float_round:
            return str(int(v)) if v == int(v) else f"{v:.6f}"
        return repr(v)
    if isinstance(v, int):
        return str(v)
    if isinstance(v, bytes):
        return v.decode("utf-8", "replace")
    return str(v)


def canon(rows, variant, order_matters):
    """Return a hashable canonical form of a result set under one variant."""
    if variant == "strict":
        # exact row order, exact column order, exact float repr
        t = [tuple(_val(v, False) for v in r) for r in rows]
        return tuple(t)
    if variant == "order_conditional":
        # the comparison the census reports
        t = [tuple(_val(v) for v in r) for r in rows]
        return tuple(t) if order_matters else tuple(sorted(t))
    if variant == "always_sort":
        # rows always sorted, blind to ORDER BY
        t = [tuple(_val(v) for v in r) for r in rows]
        return tuple(sorted(t))
    if variant == "col_blind":
        # order-conditional, but column order inside a row is ignored
        t = [tuple(sorted(_val(v) for v in r)) for r in rows]
        return tuple(t) if order_matters else tuple(sorted(t))
    if variant == "row_set":
        # rows as a set: always sorted, duplicate rows collapse
        t = {tuple(_val(v) for v in r) for r in rows}
        return tuple(sorted(t))
    if variant == "no_float_tol":
        # order-conditional, without float rounding
        t = [tuple(_val(v, False) for v in r) for r in rows]
        return tuple(t) if order_matters else tuple(sorted(t))
    raise ValueError(variant)


VARIANTS = ["strict", "order_conditional", "always_sort", "col_blind", "row_set", "no_float_tol"]


def h(obj):
    return hashlib.sha1(json.dumps(obj, ensure_ascii=False, default=str).encode()).hexdigest()


# ---------------------------------------------------------------- mutations
def mutations(sql):
    """Small meaning-changing edits. Each returns (family, mutated_sql) or nothing."""
    out = []
    s = sql

    # comparison flips
    for a, b, fam in ((r"(?<![<>!])>=(?!=)", "<=", "cmp_ge_le"), (r"(?<![<>!])<=(?!=)", ">=", "cmp_le_ge"),
                      (r"(?<![<>!=])>(?![=<])", "<", "cmp_gt_lt"), (r"(?<![<>!=])<(?![=>])", ">", "cmp_lt_gt")):
        if re.search(a, s):
            out.append((fam, re.sub(a, b, s, count=1)))
            break

    # ORDER BY direction
    if re.search(r"\border\s+by\b", s, re.I):
        if re.search(r"\bdesc\b", s, re.I):
            out.append(("order_desc_asc", re.sub(r"\bdesc\b", "ASC", s, count=1, flags=re.I)))
        elif re.search(r"\basc\b", s, re.I):
            out.append(("order_asc_desc", re.sub(r"\basc\b", "DESC", s, count=1, flags=re.I)))
        else:
            out.append(("order_add_desc", re.sub(r"(\border\s+by\b\s+[^\s;]+)", r"\1 DESC", s, count=1, flags=re.I)))

    # LIMIT off by one
    m = re.search(r"\blimit\s+(\d+)", s, re.I)
    if m:
        out.append(("limit_plus1", s[:m.start(1)] + str(int(m.group(1)) + 1) + s[m.end(1):]))

    # drop DISTINCT
    if re.search(r"\bdistinct\b", s, re.I):
        out.append(("drop_distinct", re.sub(r"\bdistinct\s+", "", s, count=1, flags=re.I)))

    # drop the last AND conjunct of a WHERE
    m = re.search(r"(\bwhere\b.*?)(\s+and\s+[^()]+?)(\s+(?:group|order|limit|having)\b|\s*\)|\s*$)", s, re.I | re.S)
    if m and len(m.group(2)) < 80:
        out.append(("drop_and_conjunct", s[:m.start(2)] + s[m.end(2):]))

    # aggregate swaps
    for a, b, fam in (("max", "min", "agg_max_min"), ("min", "max", "agg_min_max"),
                      ("sum", "avg", "agg_sum_avg"), ("avg", "sum", "agg_avg_sum")):
        if re.search(rf"\b{a}\s*\(", s, re.I):
            out.append((fam, re.sub(rf"\b{a}\s*\(", f"{b}(", s, count=1, flags=re.I)))
            break

    return out


# ---------------------------------------------------------------- execution
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
    ap.add_argument("--out", default="experiments/spider_dev_near_miss_census.json")
    ap.add_argument("--max-instances", type=int, default=0)
    a = ap.parse_args()

    dev = json.load(open(a.dev))
    by_db = collections.defaultdict(list)
    for i, r in enumerate(dev):
        by_db[r["db_id"]].append({**r, "qid": i})

    # per (variant, family): counts
    fa = collections.defaultdict(lambda: collections.Counter())   # false accept
    fam_tot = collections.Counter()
    gold_exec_err = collections.Counter()
    mut_exec_err = collections.Counter()
    n_mut = 0
    n_truly_wrong = 0
    n_same_meaning = 0
    variant_vs_reported = collections.Counter()
    t0 = time.time()

    for db, items in sorted(by_db.items()):
        ddir = os.path.join(a.suite_root, db)
        orig = os.path.join(ddir, f"{db}.sqlite")
        if not os.path.isfile(orig):
            continue
        rest = sorted(f for f in os.listdir(ddir) if f.endswith(".sqlite") and f != f"{db}.sqlite")
        if a.max_instances:
            rest = rest[: max(0, a.max_instances - 1)]
        insts = [f"{db}.sqlite"] + rest

        # build the mutation set for this db
        cases = []
        for it in items:
            om = bool(re.search(r"\border\s+by\b", it["query"], re.I))
            for fam, mut in mutations(it["query"]):
                if re.sub(r"\s+", " ", mut.strip().lower()) == re.sub(r"\s+", " ", it["query"].strip().lower()):
                    continue
                cases.append({"qid": it["qid"], "gold": it["query"], "mut": mut,
                              "fam": fam, "order_matters": om})
        if not cases:
            continue

        # execute gold and mutation on every instance, recording per-variant canonical hashes
        # sig[(idx, which, variant)] = list of hashes across instances
        sig = collections.defaultdict(list)
        ok = [True] * len(cases)
        for inst in insts:
            con = sqlite3.connect(f"file:{os.path.join(ddir, inst)}?mode=ro", uri=True)
            con.text_factory = lambda b: b.decode("utf-8", "replace")
            for k, c in enumerate(cases):
                if not ok[k]:
                    continue
                g, ge = run(con, c["gold"])
                if ge:
                    gold_exec_err[ge] += 1
                    ok[k] = False
                    continue
                m, me = run(con, c["mut"])
                if me:
                    mut_exec_err[me] += 1
                    ok[k] = False
                    continue
                for v in VARIANTS:
                    sig[(k, "g", v)].append(h(canon(g, v, c["order_matters"])))
                    sig[(k, "m", v)].append(h(canon(m, v, c["order_matters"])))
            con.close()

        for k, c in enumerate(cases):
            if not ok[k]:
                continue
            n_mut += 1
            fam = c["fam"]
            # ground truth: does the mutation differ from the gold on ANY instance,
            # under the order-conditional comparison?
            gs = sig[(k, "g", "order_conditional")]
            ms = sig[(k, "m", "order_conditional")]
            truly_wrong = any(x != y for x, y in zip(gs, ms))
            if not truly_wrong:
                n_same_meaning += 1
                continue
            n_truly_wrong += 1
            fam_tot[fam] += 1
            for v in VARIANTS:
                # what does this variant say on the shipped database alone (index 0)?
                same_on_original = sig[(k, "g", v)][0] == sig[(k, "m", v)][0]
                if same_on_original:
                    fa[v][fam] += 1
                    fa[v]["__all__"] += 1
                if v != "order_conditional":
                    ref = sig[(k, "g", "order_conditional")][0] == sig[(k, "m", "order_conditional")][0]
                    if same_on_original != ref:
                        variant_vs_reported[v] += 1

    out = {
        "split": "Spider dev (official, 1034 questions, 20 databases)",
        "truth_oracle": "distilled test suite, order-conditional canonical comparison, disagreement on any instance",
        "mutations_executed": n_mut,
        "mutations_that_changed_meaning": n_truly_wrong,
        "mutations_that_did_not_change_meaning": n_same_meaning,
        "gold_exec_errors": dict(gold_exec_err),
        "mutation_exec_errors": dict(mut_exec_err),
        "false_accept_rate_on_shipped_db": {
            v: round(fa[v]["__all__"] / n_truly_wrong, 4) if n_truly_wrong else None for v in VARIANTS
        },
        "disagreements_with_order_conditional": dict(variant_vs_reported),
        "by_family": {
            fam: {"n_truly_wrong": fam_tot[fam],
                  **{v: (round(fa[v][fam] / fam_tot[fam], 4) if fam_tot[fam] else None) for v in VARIANTS}}
            for fam in sorted(fam_tot)
        },
        "wall_clock_sec": round(time.time() - t0, 1),
    }
    json.dump(out, open(a.out, "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out.items() if k != "by_family"}, ensure_ascii=False, indent=1))
    print("\nfalse-accept rate on the shipped database, by mutation family:")
    hdr = f"  {'family':22s}{'n':>6s}" + "".join(f"{v:>18s}" for v in VARIANTS)
    print(hdr)
    for fam, row in out["by_family"].items():
        print(f"  {fam:22s}{row['n_truly_wrong']:>6d}" + "".join(f"{row[v]:>18.4f}" for v in VARIANTS))


if __name__ == "__main__":
    main()
