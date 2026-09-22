#!/usr/bin/env python3
"""C6 step 2: render the semantic-audit evidence file as a reviewer dossier.

One section per case, each self-contained: the natural-language question, the benchmark gold, the
answer the pipeline actually returned, how many suite instances separate them, and both result
tables on the first instance that does. A schema appendix carries the tables of every database
involved, so a reader never has to open the benchmark to check whether a column exists.

Nothing here is a judgement. The dossier states what the two queries return and leaves every
classification to the reader, which for this audit is an AI reviewer.
"""
import argparse, collections, json, os, sqlite3


def schema_lines(path):
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    out = []
    for (name,) in con.execute("SELECT name FROM sqlite_master WHERE type='table' "
                               "AND name NOT LIKE 'sqlite_%' ORDER BY name"):
        cols = [f'{r[1]}' for r in con.execute(f'PRAGMA table_info("{name}")')]
        out.append(f"  {name}({', '.join(cols)})")
    con.close()
    return out


def table(rows, truncated, n):
    if not rows:
        return "    (no rows)"
    body = ["    " + " | ".join("NULL" if v is None else str(v) for v in r) for r in rows]
    if truncated:
        body.append(f"    ... ({n} rows total)")
    return "\n".join(body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default="experiments/c6_semantic_cases.json")
    ap.add_argument("--suite-root", default="data/spider/test_suite_database")
    ap.add_argument("--only-new", action="store_true",
                    help="skip cases carried over from an earlier audit, which are already judged")
    ap.add_argument("--out", default="experiments/c6_dossier.md")
    a = ap.parse_args()
    d = json.load(open(a.cases))
    C = [c for c in d["cases"] if not (a.only_new and c.get("carried_over_from"))]

    L = []
    p = d["population"]
    n_ans = p.get("weak_correct_strong_wrong_answers", p.get("wrong_answers"))
    L.append("# Semantic audit dossier: " + p.get("title", p["definition"]) + "\n")
    L.append(f"Built {d['built']}. Population definition: {p['definition']}.\n")
    examined = (f" ({p['answers_examined']} answers examined)" if "answers_examined" in p
                else f" ({p['answers_examined_per_cell']} answers examined per cell)"
                if "answers_examined_per_cell" in p else "")
    L.append(f"{n_ans} such answers across {len(p['pools'])} pools{examined} collapse to "
             f"{p['distinct_cases']} distinct (question, returned SQL) cases over "
             f"{p['distinct_questions']} questions. Every case in the population was judged: "
             f"this is a census, not a sample.\n")
    if len(C) != p["distinct_cases"]:
        L.append(f"{p['distinct_cases'] - len(C)} of those cases were judged in an earlier round "
                 f"under the same protocol and are not repeated here. The {len(C)} listed below "
                 f"are the ones still to judge.\n")
    if all(c["agree_on_original"] for c in C):
        L.append("In every case the gold and the returned query agree on the shipped benchmark "
                 "database and disagree on at least one instance of the distilled test suite. The "
                 "comparator is the official `result_eq`, called with the gold first, and whether "
                 "row order is compared is a property of the gold, as in the frozen analyser.\n")
    else:
        n_ship = sum(1 for c in C if not c["agree_on_original"])
        L.append(f"In every case the distilled test suite rejects the returned query. In "
                 f"{n_ship} of the {len(C)} the shipped benchmark database rejects it too, and "
                 f"then the first disagreeing instance IS that shipped database, which the "
                 f"benchmark provides rather than generates. Exculpating such a case as an "
                 f"instance defect is therefore a claim about the benchmark's own database. The "
                 f"comparator is the official `result_eq`, called with the gold first, and "
                 f"whether row order is compared is a property of the gold, as in the frozen "
                 f"analyser.\n")
    L.append("`instances disagreeing` counts suite instances where the two queries differ. A "
             "difference on one instance out of fifty and a difference on all of them are very "
             "different evidence, so the count is given for every case.\n")

    L.append("\n## Cases\n")
    for c in C:
        w = c["witness"]
        L.append(f"### {c['case_id']}  (question {c['qid']}, database `{c['db']}`)\n")
        # A case can be the answer of both cells in the same pool, which lists that pool twice.
        # The cell line below already says that, so the pool list is deduplicated.
        seen, uniq = set(), []
        for x in c["answers"]:
            k = (x["model"], x["seed"])
            if k not in seen:
                seen.add(k)
                uniq.append(x)
        L.append("- Returned by: " + ", ".join(f"{x['model']}/{x['seed']}" for x in uniq))
        if c.get("cells"):
            L.append("- Returned in cell: " + ("both A and D" if c["cells"] == "AD"
                                               else f"{c['cells']} only"))
        L.append("- Class mass: " + ", ".join(f"{x['class_count']}/{x['n_usable']}"
                                              for x in uniq))
        L.append(f"- Instances disagreeing: {c['n_disagree']} of {c['n_instances']} "
                 f"({c['disagree_fraction']:.0%})")
        L.append(f"- Row order compared: {'yes' if c['order_matters'] else 'no'} "
                 f"(the gold {'has' if c['order_matters'] else 'has no'} ORDER BY)\n")
        L.append(f"**Question.** {c['question']}\n")
        L.append("**Gold.**\n```sql\n" + c["gold"].strip() + "\n```\n")
        L.append("**Returned.**\n```sql\n" + c["rep"].strip() + "\n```\n")
        if w.get("execution_error"):
            L.append(f"**First disagreeing instance** `{c['witness_instance']}`: execution error "
                     f"(gold {w['gold']}, returned {w['rep']}).\n")
        else:
            L.append(f"**First disagreeing instance** `{c['witness_instance']}`"
                     + (" (this is the shipped benchmark database)."
                        if c.get("witness_is_shipped_database") else ".") + "\n")
            L.append(f"Gold returns {w['n_rows_gold']} row(s), "
                     f"{w['n_cols_gold']} column(s):\n")
            L.append(table(w["gold_rows"], w["gold_truncated"], w["n_rows_gold"]) + "\n")
            L.append(f"Returned query gives {w['n_rows_rep']} row(s), "
                     f"{w['n_cols_rep']} column(s):\n")
            L.append(table(w["rep_rows"], w["rep_truncated"], w["n_rows_rep"]) + "\n")
            flags = [k for k in ("col_count_differs", "row_order_only",
                                 "duplicate_multiplicity_only", "rep_subset_of_gold",
                                 "gold_subset_of_rep", "disjoint", "gold_empty", "rep_empty")
                     if w.get(k)]
            L.append(f"Difference: {', '.join(flags) if flags else 'values differ'}; "
                     f"{w['rows_shared']} row(s) in common, {w['rows_gold_only']} only in the "
                     f"gold, {w['rows_rep_only']} only in the returned result.\n")

    L.append("\n## Schema appendix\n")
    for db in sorted({c["db"] for c in C}):
        L.append(f"### `{db}`\n```")
        L += schema_lines(os.path.join(a.suite_root, db, f"{db}.sqlite"))
        L.append("```\n")

    open(a.out, "w").write("\n".join(L))
    print(f"{a.out}: {len(C)} cases, {os.path.getsize(a.out) / 1024:.0f} KB")
    idx = collections.OrderedDict((c["case_id"], c["qid"]) for c in C)
    print("case ids:", list(idx)[0], "..", list(idx)[-1])


if __name__ == "__main__":
    main()
