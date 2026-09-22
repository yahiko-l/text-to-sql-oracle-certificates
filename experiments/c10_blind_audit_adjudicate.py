#!/usr/bin/env python3
"""C10 step 1c: build the third-pass sheet over the two experts' disagreements.

Protocol section 6 sends only the items the two experts disagreed on to a third pass, and
forbids revising the items they agreed on. This script produces exactly that sheet, so the
constraint is carried by the file the adjudicator receives rather than by their memory.

The output is a RESPONSES-shaped CSV that the analysis script reads through --adjudicated.
The two experts' verdicts ride along in extra columns for the adjudicator to read; the
analysis ignores them.

  python3 experiments/c10_blind_audit_adjudicate.py \
      --responses blind-audit/RESPONSES_expert1.csv blind-audit/RESPONSES_expert2.csv \
      --out blind-audit/ADJUDICATION.csv
"""
import argparse
import csv
import json
import os
import re
import sqlite3

VERDICTS = ("gold_correct", "gold_defective", "question_underspecified", "cannot_judge")
FIELDS = ["item_id", "verdict", "defect_type", "borderline", "note",
          "expert1_verdict", "expert1_borderline", "expert1_note",
          "expert2_verdict", "expert2_borderline", "expert2_note"]


def read(path):
    rows = {}
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            v = (r.get("verdict") or "").strip()
            if not v:
                continue
            if v not in VERDICTS:
                raise SystemExit(f"{path}: item {r['item_id']} has verdict {v!r}, "
                                 f"which is not one of {VERDICTS}")
            rows[r["item_id"].strip()] = {
                "verdict": v,
                "defect_type": (r.get("defect_type") or "").strip(),
                "borderline": (r.get("borderline") or "").strip(),
                "note": (r.get("note") or "").strip()}
    return rows


def parse_items(path):
    body = open(path, encoding="utf-8").read().split("## Items", 1)[1]
    parts = re.split(r"\n### (Q\d+)\n", body)
    out, it = {}, iter(parts[1:])
    for item_id, chunk in zip(it, it):
        db = re.search(r"Database: `([^`]+)`", chunk)
        q = re.search(r"\*\*Question\.\*\*\s*(.+)", chunk)
        sql = re.search(r"```sql\n(.*?)\n```", chunk, re.S)
        if db and sql:
            out[item_id] = {"db": db.group(1), "question": q.group(1).strip() if q else "",
                            "sql": sql.group(1).strip()}
    return out


def execute(db, sql, limit=12):
    path = os.path.join("data", "spider", "test_suite_database", db, db + ".sqlite")
    if not os.path.isfile(path):
        return "(database not available here)"
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    con.text_factory = lambda b: b.decode("utf-8", "replace")
    try:
        cur = con.execute(sql)
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchall()
    except sqlite3.Error as e:
        return f"(the query raised: {e})"
    finally:
        con.close()
    head = " | ".join(cols)
    body = "\n".join(" | ".join("NULL" if v is None else str(v) for v in r)
                     for r in rows[:limit])
    tail = f"\n... {len(rows)} rows in total" if len(rows) > limit else f"\n{len(rows)} row(s)"
    return head + "\n" + ("-" * len(head)) + "\n" + (body or "(zero rows)") + tail


def write_brief(path, items_path, disagree, e1, e2):
    """The adjudicator reads this and fills the CSV. The stratum stays out of it."""
    items = parse_items(items_path)
    out = ["# 裁定用简报", "",
           f"两位专家在以下 {len(disagree)} 项上不一致，其余各项一致，按协议不得改动。",
           "每项给出问题、参考查询、查询实际返回的结果，以及两位专家的判定与理由。",
           "读完在 `ADJUDICATION.csv` 里填 `verdict`、`defect_type`、`borderline`、`note` 四列。", ""]
    for item_id in disagree:
        it = items.get(item_id, {})
        out += [f"## {item_id}", "", f"数据库：`{it.get('db', '?')}`", "",
                f"**问题.** {it.get('question', '?')}", "", "**参考查询.**", "",
                "```sql", it.get("sql", "?"), "```", "", "**它返回什么.**", "",
                "```", execute(it["db"], it["sql"]) if it else "?", "```", "",
                f"**专家一** `{e1[item_id]['verdict']}`"
                f"{'（难判）' if e1[item_id]['borderline'].lower() in ('yes','y','true','1') else ''}"
                f"：{e1[item_id]['note'] or '（未填理由）'}", "",
                f"**专家二** `{e2[item_id]['verdict']}`"
                f"{'（难判）' if e2[item_id]['borderline'].lower() in ('yes','y','true','1') else ''}"
                f"：{e2[item_id]['note'] or '（未填理由）'}", "", "---", ""]
    open(path, "w", encoding="utf-8").write("\n".join(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--responses", nargs=2, required=True)
    ap.add_argument("--key", default="experiments/c10_blind_audit_key.json")
    ap.add_argument("--out", default="blind-audit/ADJUDICATION.csv")
    ap.add_argument("--brief", default="",
                    help="also render the disputed items, with the question, the reference "
                         "query, what it returns and both readings, for the adjudicator")
    ap.add_argument("--items", default="blind-audit/ITEMS.md")
    a = ap.parse_args()

    total = len(json.load(open(a.key))["key"])
    e1, e2 = (read(p) for p in a.responses)
    for path, rows in zip(a.responses, (e1, e2)):
        if len(rows) < total:
            print(f"warning: {path} carries {len(rows)} of {total} verdicts")

    both = sorted(set(e1) & set(e2))
    disagree = [i for i in both if e1[i]["verdict"] != e2[i]["verdict"]]
    only1 = sorted(set(e1) - set(e2))
    only2 = sorted(set(e2) - set(e1))

    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for i in disagree:
            w.writerow({"item_id": i, "verdict": "", "defect_type": "", "borderline": "",
                        "note": "",
                        "expert1_verdict": e1[i]["verdict"],
                        "expert1_borderline": e1[i]["borderline"],
                        "expert1_note": e1[i]["note"],
                        "expert2_verdict": e2[i]["verdict"],
                        "expert2_borderline": e2[i]["borderline"],
                        "expert2_note": e2[i]["note"]})

    agreed = len(both) - len(disagree)
    print(f"items judged by both : {len(both)} of {total}")
    print(f"agreed               : {agreed}")
    print(f"to adjudicate        : {len(disagree)}")
    if only1 or only2:
        print(f"judged by one expert only: {len(only1)} in the first file, "
              f"{len(only2)} in the second; these are not adjudicated and enter the "
              f"analysis as that expert judged them")
    if a.brief:
        write_brief(a.brief, a.items, disagree, e1, e2)
        print(f"wrote {a.brief}")
    print(f"\nwrote {a.out}")
    print("Fill only the verdict, defect_type, borderline and note columns. The items the "
          "two experts agreed on are absent by design and must not be revised.")


if __name__ == "__main__":
    main()
