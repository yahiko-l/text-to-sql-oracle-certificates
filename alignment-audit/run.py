#!/usr/bin/env python3
"""判读助手。包里自带条目表和全部数据库，从包的根目录运行。

  python3 run.py                      接着上次，显示下一条还没填的条目
  python3 run.py AL0007               显示 AL0007 并执行它的 SQL
  python3 run.py AL0007 --limit 50    同上，最多显示 50 行结果
  python3 run.py --progress           已填多少、还剩多少、各判定的分布
  python3 run.py --schema world_1     打印某个数据库的表和列
  python3 run.py --db world_1 --sql "select count(*) from city"
                                      自己写查询看数据
  python3 run.py --check              检查包是否完整、每条 SQL 是否都能跑

数据库以只读方式打开，你在这里跑什么都改不了它们。
"""
import argparse, csv, os, re, sqlite3, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ITEMS = os.path.join(HERE, "ITEMS.md")
DBROOT = os.path.join(HERE, "data", "spider", "test_suite_database")
MAXCELL = 40
VERDICTS = ("answers", "does_not_answer", "question_underspecified", "cannot_judge")


def die(msg):
    raise SystemExit(f"错误：{msg}")


def responses_path():
    here = [f for f in sorted(os.listdir(HERE))
            if f.startswith("RESPONSES") and f.endswith(".csv")]
    if not here:
        die("找不到 RESPONSES*.csv，这个脚本要放在包的根目录运行。")
    if len(here) > 1:
        die("目录里有多个 RESPONSES 文件：" + ", ".join(here) + "。只保留你自己的那一份。")
    return os.path.join(HERE, here[0])


def parse_items():
    if not os.path.isfile(ITEMS):
        die(f"找不到 {ITEMS}，这个脚本要放在包的根目录运行。")
    body = open(ITEMS, encoding="utf-8").read().split("\n# Schemas", 1)[0]
    parts = re.split(r"\n## (AL\d+)\n", body)
    out, it = {}, iter(parts[1:])
    for item_id, chunk in zip(it, it):
        db = re.search(r"Database: `([^`]+)`", chunk)
        q = re.search(r"Question:\s*(.+)", chunk)
        sql = re.search(r"```sql\n(.*?)\n```", chunk, re.S)
        if db and sql:
            out[item_id] = {"db": db.group(1), "sql": sql.group(1).strip(),
                            "question": q.group(1).strip() if q else ""}
    return out


def read_responses():
    p = responses_path()
    rows = list(csv.DictReader(open(p, encoding="utf-8-sig")))
    return p, rows


def connect(db):
    p = os.path.join(DBROOT, db, db + ".sqlite")
    if not os.path.isfile(p):
        die(f"数据库 {db} 不在 {p}。包可能不完整，请重新要一份。")
    con = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
    con.text_factory = lambda b: b.decode("utf-8", "replace")
    return con


def render(cur, rows, limit):
    cols = [d[0] for d in cur.description] if cur.description else []
    if not cols:
        print("  （这条语句没有返回结果集）")
        return

    def cell(v):
        s = "NULL" if v is None else str(v)
        return s if len(s) <= MAXCELL else s[:MAXCELL - 1] + "…"

    table = [[cell(c) for c in cols]] + [[cell(v) for v in r] for r in rows[:limit]]
    width = [max(len(r[i]) for r in table) for i in range(len(cols))]
    print("  " + " | ".join(h.ljust(w) for h, w in zip(table[0], width)))
    print("  " + "-+-".join("-" * w for w in width))
    for r in table[1:]:
        print("  " + " | ".join(v.ljust(w) for v, w in zip(r, width)))
    if not rows:
        print("  （零行）")
    print(f"\n  共 {len(rows)} 行" + (f"，只显示前 {limit} 行" if len(rows) > limit else ""))


def show_item(items, item_id, limit):
    if item_id not in items:
        die(f"{item_id} 不在条目表里。")
    it = items[item_id]
    print(f"\n=== {item_id} ===")
    print(f"数据库：{it['db']}\n")
    print(f"问题：{it['question']}\n")
    print("待判读的 SQL：")
    for ln in it["sql"].splitlines():
        print("  " + ln)
    print("\n它返回：")
    con = connect(it["db"])
    try:
        cur = con.execute(it["sql"])
        render(cur, cur.fetchall(), limit)
    except sqlite3.Error as e:
        print(f"  这条 SQL 报错：{e}")
        print("  跑不起来的条目填 cannot_judge。")
    finally:
        con.close()
    print(f"\n把判定填进 {os.path.basename(responses_path())} 的 {item_id} 那一行。")
    print("四选一：" + " / ".join(VERDICTS) + "\n")


def progress(items):
    p, rows = read_responses()
    done = [r for r in rows if (r.get("verdict") or "").strip()]
    counts = {}
    bad = []
    for r in done:
        v = r["verdict"].strip()
        counts[v] = counts.get(v, 0) + 1
        if v not in VERDICTS:
            bad.append((r["item_id"], v))
    print(f"\n{os.path.basename(p)}：已填 {len(done)} / {len(rows)}，还剩 {len(rows) - len(done)}")
    for v in VERDICTS:
        if counts.get(v):
            print(f"  {v:<26}{counts[v]:>5}")
    if bad:
        print(f"\n有 {len(bad)} 行填了不认识的词，请改成四个之一：")
        for iid, v in bad[:10]:
            print(f"  {iid}: {v!r}")
    print()


def next_item(items, limit):
    _, rows = read_responses()
    for r in rows:
        if not (r.get("verdict") or "").strip():
            return show_item(items, r["item_id"].strip(), limit)
    print("\n全部填完了。跑一次 python3 run.py --progress 复核，然后把 CSV 交回。\n")


def check(items):
    print(f"条目 {len(items)} 条")
    p, rows = read_responses()
    print(f"应答文件 {os.path.basename(p)}，{len(rows)} 行")
    missing = [i for i in items if not os.path.isfile(
        os.path.join(DBROOT, items[i]["db"], items[i]["db"] + ".sqlite"))]
    print(f"缺失的数据库：{len(missing)}")
    bad = []
    for iid, it in items.items():
        con = connect(it["db"])
        try:
            con.execute(it["sql"]).fetchall()
        except sqlite3.Error as e:
            bad.append((iid, str(e)))
        finally:
            con.close()
    print(f"跑不起来的 SQL：{len(bad)}")
    for iid, e in bad[:20]:
        print(f"  {iid}: {e}")
    print("包检查完毕。" if not missing else "包不完整，请重新要一份。")


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("item", nargs="?")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--schema")
    ap.add_argument("--db")
    ap.add_argument("--sql")
    ap.add_argument("--progress", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    items = parse_items()
    if a.schema:
        con = connect(a.schema)
        print(f"\n=== {a.schema} ===\n")
        for (name,) in con.execute("select name from sqlite_master where type='table' "
                                   "and name not like 'sqlite_%' order by name"):
            n = con.execute(f'select count(*) from "{name}"').fetchone()[0]
            print(f"{name}  （{n} 行）")
            for row in con.execute(f'pragma table_info("{name}")'):
                print(f"    {row[1]:<28} {row[2]}")
            print()
        con.close()
    elif a.db and a.sql:
        con = connect(a.db)
        try:
            cur = con.execute(a.sql)
            render(cur, cur.fetchall(), a.limit)
        except sqlite3.Error as e:
            print(f"  sqlite 报错：{e}")
        finally:
            con.close()
    elif a.check:
        check(items)
    elif a.progress:
        progress(items)
    elif a.item:
        show_item(items, a.item.strip().upper(), a.limit)
    else:
        next_item(items, a.limit)


if __name__ == "__main__":
    main()
