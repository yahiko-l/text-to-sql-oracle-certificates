#!/usr/bin/env python3
"""C10 step 3b: assemble the package the third-pass adjudicator receives.

Smaller and differently shaped from the reviewers' package: only the items the two experts
disagreed on, the brief that lays each one out, the sheet to fill, and the databases those
items touch. The agreed items are absent by design, which is how protocol section 6 is
enforced, and the strata are absent as everywhere the reviewers can see.

Refuses to build if the sheet already carries verdicts, if the brief and the sheet cover
different items, or if any of the disputed queries does not run.
"""
import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import sqlite3
import tempfile
import zipfile

SRC = "blind-audit"
DBROOT = os.path.join("data", "spider", "test_suite_database")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", default="experiments/blind_audit/ADJUDICATION_BRIEF.md")
    ap.add_argument("--sheet", default="experiments/blind_audit/ADJUDICATION.csv")
    ap.add_argument("--readme", default=os.path.join(SRC, "ADJUDICATION_README.md"))
    ap.add_argument("--runner", default=os.path.join(SRC, "run.py"))
    ap.add_argument("--out", default="blind-audit-adjudication.zip")
    a = ap.parse_args()

    for p in (a.brief, a.sheet, a.readme, a.runner):
        if not os.path.isfile(p):
            raise SystemExit(f"missing {p}")

    rows = list(csv.DictReader(open(a.sheet, newline="", encoding="utf-8")))
    filled = [r["item_id"] for r in rows if (r.get("verdict") or "").strip()]
    if filled:
        raise SystemExit(f"{a.sheet} already carries verdicts for {', '.join(filled)}; "
                         f"refusing to send a sheet that is not blank.")
    sheet_ids = [r["item_id"] for r in rows]

    brief = open(a.brief, encoding="utf-8").read()
    brief_ids = re.findall(r"^## (Q\d+)", brief, re.M)
    if sheet_ids != brief_ids:
        raise SystemExit(f"the sheet covers {sheet_ids} and the brief covers {brief_ids}; "
                         f"they must be the same items in the same order.")

    for token in ("flagged", "examined", "unexamined", "stratum"):
        if token in brief:
            raise SystemExit(f"the brief contains {token!r}, which would disclose the strata.")

    blocks = re.split(r"\n## Q\d+\n", brief)[1:]
    dbs, queries = [], []
    for item_id, block in zip(brief_ids, blocks):
        db = re.search(r"数据库：`([^`]+)`", block)
        sql = re.search(r"```sql\n(.*?)\n```", block, re.S)
        if not (db and sql):
            raise SystemExit(f"{item_id}: the brief has no database or no query")
        dbs.append(db.group(1))
        queries.append((item_id, db.group(1), sql.group(1).strip()))
    dbs = sorted(set(dbs))

    for item_id, db, sql in queries:
        path = os.path.join(DBROOT, db, db + ".sqlite")
        if not os.path.isfile(path):
            raise SystemExit(f"missing database {path}")
        con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        con.text_factory = lambda b: b.decode("utf-8", "replace")
        try:
            con.execute(sql).fetchall()
        except sqlite3.Error as e:
            raise SystemExit(f"{item_id}: the query does not run against {db}: {e}")
        finally:
            con.close()

    manifest = {"items": sheet_ids, "databases": {}, "files": {}}
    stage = tempfile.mkdtemp(prefix="adjudication-pkg-")
    try:
        for src, name in ((a.readme, "README.md"), (a.brief, "ADJUDICATION_BRIEF.md"),
                          (a.sheet, "ADJUDICATION.csv"), (a.runner, "run.py")):
            shutil.copy2(src, os.path.join(stage, name))
            manifest["files"][name] = sha256(src)
        for db in dbs:
            src = os.path.join(DBROOT, db, db + ".sqlite")
            dst = os.path.join(stage, DBROOT, db)
            os.makedirs(dst, exist_ok=True)
            shutil.copy2(src, os.path.join(dst, db + ".sqlite"))
            manifest["databases"][db] = {"sha256": sha256(src), "bytes": os.path.getsize(src)}
        with open(os.path.join(stage, "MANIFEST.json"), "w") as f:
            json.dump(manifest, f, indent=1)
        with zipfile.ZipFile(a.out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for root, _, files in os.walk(stage):
                for name in sorted(files):
                    full = os.path.join(root, name)
                    z.write(full, os.path.relpath(full, stage))
    finally:
        shutil.rmtree(stage)

    print(f"items to adjudicate : {len(sheet_ids)}  ({', '.join(sheet_ids)})")
    print(f"databases packed    : {len(dbs)}  ({', '.join(dbs)})")
    print(f"all {len(queries)} disputed queries execute against the packaged databases")
    print(f"sheet is blank      : yes")
    print(f"\nwrote {a.out}  {os.path.getsize(a.out) / 1e3:.0f} kB")


if __name__ == "__main__":
    main()
