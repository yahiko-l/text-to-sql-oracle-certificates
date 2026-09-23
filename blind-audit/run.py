#!/usr/bin/env python3
"""Runner for the blinded reference-query review.

Everything this script needs is inside this package: the item sheet ITEMS.md and the
databases under data/. Run it from the package root.

  python3 run.py Q001                 show item Q001 and execute its reference query
  python3 run.py Q001 --limit 50      same, showing up to 50 result rows
  python3 run.py --schema world_1     print the tables and columns of one database
  python3 run.py --db world_1 --sql "select count(*) from city"
                                      run your own query, to look at the data
  python3 run.py --list               list every item with its database
  python3 run.py --check              verify the package is complete and every
                                      reference query runs

Databases are opened read only, so nothing you run here can change them.
"""
import argparse
import os
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ITEMS = os.path.join(HERE, "ITEMS.md")
DBROOT = os.path.join(HERE, "data", "spider", "test_suite_database")
RESPONSES = os.path.join(HERE, "RESPONSES.csv")
MAXCELL = 40


def die(msg):
    raise SystemExit(f"error: {msg}")


def parse_items(path=ITEMS):
    if not os.path.isfile(path):
        if os.path.isfile(os.path.join(HERE, "ADJUDICATION_BRIEF.md")):
            die("this is the adjudication package, which carries no item sheet. The 13 items, "
                "their queries and what those queries return are in ADJUDICATION_BRIEF.md. "
                "Use --schema and --db/--sql here.")
        die(f"{path} not found. This script expects to sit in the package root, "
            f"beside ITEMS.md and RESPONSES.csv.")
    body = open(path, encoding="utf-8").read()
    body = body.split("## Items", 1)[1] if "## Items" in body else body
    parts = re.split(r"\n### (Q\d+)\n", body)
    out = {}
    it = iter(parts[1:])
    for item_id, chunk in zip(it, it):
        db = re.search(r"Database: `([^`]+)`", chunk)
        question = re.search(r"\*\*Question\.\*\*\s*(.+)", chunk)
        sql = re.search(r"```sql\n(.*?)\n```", chunk, re.S)
        if db and sql:
            out[item_id] = {"db": db.group(1),
                            "question": question.group(1).strip() if question else "",
                            "sql": sql.group(1).strip()}
    return out


def dbpath(db):
    p = os.path.join(DBROOT, db, db + ".sqlite")
    if not os.path.isfile(p):
        die(f"database {db} not found at {p}. The package looks incomplete; "
            f"ask for a fresh copy.")
    return p


def connect(db):
    con = sqlite3.connect(f"file:{dbpath(db)}?mode=ro", uri=True)
    con.text_factory = lambda b: b.decode("utf-8", "replace")
    return con


def render(cur, rows, limit):
    cols = [d[0] for d in cur.description] if cur.description else []
    if not cols:
        print("  (the statement returned no result set)")
        return
    shown = rows[:limit]

    def cell(v):
        s = "NULL" if v is None else str(v)
        return s if len(s) <= MAXCELL else s[:MAXCELL - 1] + "…"

    table = [[cell(c) for c in cols]] + [[cell(v) for v in r] for r in shown]
    width = [max(len(r[i]) for r in table) for i in range(len(cols))]
    line = "  " + "-+-".join("-" * w for w in width)
    print("  " + " | ".join(h.ljust(w) for h, w in zip(table[0], width)))
    print(line)
    for r in table[1:]:
        print("  " + " | ".join(v.ljust(w) for v, w in zip(r, width)))
    if not shown:
        print("  (zero rows)")
    print(f"\n  {len(rows)} row(s)" + (f", showing the first {limit}"
                                       if len(rows) > limit else ""))


def show_item(items, item_id, limit):
    if item_id not in items:
        die(f"{item_id} is not in {ITEMS}")
    it = items[item_id]
    print(f"\n=== {item_id} ===")
    print(f"Database: {it['db']}\n")
    print(f"Question. {it['question']}\n")
    print("Reference query under review:")
    for ln in it["sql"].splitlines():
        print("  " + ln)
    print("\nResult:")
    con = connect(it["db"])
    try:
        cur = con.execute(it["sql"])
        render(cur, cur.fetchall(), limit)
    except sqlite3.Error as e:
        print(f"  the reference query raised: {e}")
    finally:
        con.close()
    print("\nRecord your verdict for this item in RESPONSES.csv.\n")


def show_schema(db):
    con = connect(db)
    print(f"\n=== schema of {db} ===\n")
    for name, sql in con.execute(
            "select name, sql from sqlite_master where type='table' "
            "and name not like 'sqlite_%' order by name"):
        print(f"{name}")
        for row in con.execute(f'pragma table_info("{name}")'):
            print(f"    {row[1]:<28} {row[2]}")
        n = con.execute(f'select count(*) from "{name}"').fetchone()[0]
        print(f"    ({n} rows)\n")
    con.close()


def run_sql(db, sql, limit):
    con = connect(db)
    try:
        cur = con.execute(sql)
        render(cur, cur.fetchall(), limit)
    except sqlite3.Error as e:
        print(f"  sqlite raised: {e}")
    finally:
        con.close()


def check(items):
    print(f"item sheet      : {len(items)} items")
    dbs = sorted({v["db"] for v in items.values()})
    missing = [d for d in dbs if not os.path.isfile(
        os.path.join(DBROOT, d, d + ".sqlite"))]
    print(f"databases needed: {len(dbs)}")
    if missing:
        print(f"MISSING         : {', '.join(missing)}")
    ok, bad = 0, []
    for item_id, it in items.items():
        if it["db"] in missing:
            continue
        con = connect(it["db"])
        try:
            con.execute(it["sql"]).fetchall()
            ok += 1
        except sqlite3.Error as e:
            bad.append((item_id, str(e)[:70]))
        finally:
            con.close()
    print(f"queries that run: {ok} of {len(items)}")
    for item_id, e in bad:
        print(f"  {item_id}: {e}")
    print(f"response sheet  : {'present' if os.path.isfile(RESPONSES) else 'MISSING'}")
    good = not missing and not bad and os.path.isfile(RESPONSES)
    print("\npackage is complete and ready" if good else
          "\npackage is incomplete, ask for a fresh copy")
    return 0 if good else 1


def main():
    ap = argparse.ArgumentParser(add_help=True, description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("item", nargs="?", help="an item id such as Q001")
    ap.add_argument("--db", help="database name, for use with --sql")
    ap.add_argument("--sql", help="a query of your own to run against --db")
    ap.add_argument("--schema", help="print the schema of one database")
    ap.add_argument("--list", action="store_true", help="list every item")
    ap.add_argument("--check", action="store_true", help="verify the package")
    ap.add_argument("--limit", type=int, default=20, help="result rows to show")
    a = ap.parse_args()

    if a.schema:
        return show_schema(a.schema)
    if a.sql:
        if not a.db:
            die("--sql needs --db")
        return run_sql(a.db, a.sql, a.limit)

    items = parse_items()
    if a.check:
        sys.exit(check(items))
    if a.list:
        for item_id, it in items.items():
            print(f"{item_id}  {it['db']}")
        return
    if a.item:
        return show_item(items, a.item.upper(), a.limit)
    ap.print_help()


if __name__ == "__main__":
    main()
