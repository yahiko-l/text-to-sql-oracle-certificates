#!/usr/bin/env python3
"""C10 step 1b: assemble the self-contained package the experts receive.

The item sheet, the protocol and the response sheet are produced by
c10_blind_audit_build.py and are not regenerated here; this script only collects them,
adds the databases the sheet tells the expert to run the queries against, and writes a
manifest of content hashes. ITEMS.md is verified byte for byte against the hash recorded
in the key before anything is packaged, so a package can never carry a sheet the key does
not describe.

The databases go in at exactly the relative path the sheet names, which is what lets the
sheet stay byte-identical while the package becomes runnable on a machine that has no
copy of this repository.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import zipfile

SRC = "blind-audit"
DBROOT = os.path.join("data", "spider", "test_suite_database")
TEXT_FILES = ["README.md", "PROTOCOL.md", "PROTOCOL_EN.md", "ITEMS.md",
              "RESPONSES.csv", "run.py"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def databases_in_sheet(sheet):
    text = open(sheet, encoding="utf-8").read()
    return sorted(set(re.findall(r"^Database: `([^`]+)`", text, re.M)))


def queries_in_sheet(sheet):
    body = open(sheet, encoding="utf-8").read().split("## Items", 1)[1]
    parts = re.split(r"\n### (Q\d+)\n", body)
    it = iter(parts[1:])
    out = []
    for item_id, chunk in zip(it, it):
        db = re.search(r"Database: `([^`]+)`", chunk)
        sql = re.search(r"```sql\n(.*?)\n```", chunk, re.S)
        if db and sql:
            out.append((item_id, db.group(1), sql.group(1).strip()))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", default="experiments/c10_blind_audit_key.json")
    ap.add_argument("--out", default="blind-audit-package.zip")
    ap.add_argument("--skip-smoke", action="store_true",
                    help="do not execute the reference queries while packaging")
    a = ap.parse_args()

    key = json.load(open(a.key))
    sheet = os.path.join(SRC, "ITEMS.md")
    got = sha256(sheet)
    if got != key["items_sha256"]:
        raise SystemExit(f"{sheet} hashes to {got}, the key records {key['items_sha256']}. "
                         f"The sheet the experts would receive is not the sheet the key "
                         f"describes; refusing to package.")
    print(f"item sheet verified against the key: {got}")

    for name in TEXT_FILES:
        if not os.path.isfile(os.path.join(SRC, name)):
            raise SystemExit(f"missing {os.path.join(SRC, name)}")

    dbs = databases_in_sheet(sheet)
    print(f"databases the sheet names: {len(dbs)}")

    queries = queries_in_sheet(sheet)
    if not a.skip_smoke:
        bad = []
        for item_id, db, sql in queries:
            p = os.path.join(DBROOT, db, db + ".sqlite")
            try:
                con = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
                con.text_factory = lambda b: b.decode("utf-8", "replace")
                con.execute(sql).fetchall()
                con.close()
            except Exception as e:
                bad.append((item_id, db, str(e)[:80]))
        if bad:
            for item_id, db, e in bad:
                print(f"  {item_id} ({db}): {e}", file=sys.stderr)
            raise SystemExit(f"{len(bad)} reference queries do not run against the packaged "
                             f"databases; refusing to package a sheet the expert cannot execute.")
        print(f"all {len(queries)} reference queries execute against the packaged databases")

    manifest = {"built_from_key": os.path.basename(a.key),
                "items_sha256": key["items_sha256"],
                "seed": key["seed"],
                "files": {}, "databases": {}}

    stage = tempfile.mkdtemp(prefix="blind-audit-pkg-")
    try:
        for name in TEXT_FILES:
            src = os.path.join(SRC, name)
            shutil.copy2(src, os.path.join(stage, name))
            manifest["files"][name] = sha256(src)
        for db in dbs:
            src = os.path.join(DBROOT, db, db + ".sqlite")
            if not os.path.isfile(src):
                raise SystemExit(f"missing database {src}")
            dst = os.path.join(stage, DBROOT, db)
            os.makedirs(dst, exist_ok=True)
            shutil.copy2(src, os.path.join(dst, db + ".sqlite"))
            manifest["databases"][db] = {"sha256": sha256(src),
                                         "bytes": os.path.getsize(src)}
        with open(os.path.join(stage, "MANIFEST.json"), "w") as f:
            json.dump(manifest, f, indent=1)
        # The zip itself is third-party database bytes and stays out of version control;
        # this copy is what records, in the repository, exactly what was sent out.
        with open(os.path.join(SRC, "PACKAGE_MANIFEST.json"), "w") as f:
            json.dump(manifest, f, indent=1)

        with zipfile.ZipFile(a.out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for root, _, files in os.walk(stage):
                for name in sorted(files):
                    full = os.path.join(root, name)
                    z.write(full, os.path.relpath(full, stage))
    finally:
        shutil.rmtree(stage)

    size = os.path.getsize(a.out)
    print(f"wrote {a.out}  {size / 1e6:.1f} MB, "
          f"{len(TEXT_FILES) + len(dbs) + 1} files")
    with zipfile.ZipFile(a.out) as z:
        with z.open("ITEMS.md") as f:
            packed = hashlib.sha256(f.read()).hexdigest()
    print(f"ITEMS.md inside the package: {packed} "
          f"{'matches the key' if packed == key['items_sha256'] else 'DOES NOT MATCH'}")


if __name__ == "__main__":
    main()
