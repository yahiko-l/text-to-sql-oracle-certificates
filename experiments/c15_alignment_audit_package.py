#!/usr/bin/env python3
"""Assemble the self-contained package each expert receives, one per reviewer.

Each zip carries the item sheet, the protocol, the filling guide, the runner, all 19 databases the
sheet tells the expert to execute against, and exactly ONE response file. One file per zip, because
a reviewer who can see the other reviewer's sheet name is being invited to wonder about it, and the
runner refuses to start when it finds more than one.

Two things are checked before anything is written, and a failure refuses to package rather than
warn: the item sheet must hash to what PREREGISTRATION_4 froze, and every query in the sheet must
execute against the bundled databases. A sheet the expert cannot run is not a sheet.

The key mapping items back to checkpoints and cells is never staged.
"""
import argparse, hashlib, json, os, re, shutil, sqlite3, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "alignment-audit")
DOCS = ["README.md", "PROTOCOL.md", "ITEMS.md", "run.py"]


def die(msg):
    raise SystemExit(f"refusing to package: {msg}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reviewers", nargs="*", default=["E1", "E2"])
    ap.add_argument("--key", default="experiments/c15_alignment_audit_key.json")
    ap.add_argument("--out-dir", default=".")
    a = ap.parse_args()

    key = json.load(open(os.path.join(ROOT, a.key)))
    sheet = open(os.path.join(SRC, "ITEMS.md"), encoding="utf-8").read()
    digest = hashlib.sha256(sheet.encode()).hexdigest()
    if digest != key["items_sha256"]:
        die(f"the item sheet hashes to {digest}, the preregistration froze {key['items_sha256']}. "
            f"The sheet the experts would receive is not the sheet the key describes.")

    body = sheet.split("\n# Schemas", 1)[0]
    parts = re.split(r"\n## (AL\d+)\n", body)
    items, it = {}, iter(parts[1:])
    for iid, chunk in zip(it, it):
        db = re.search(r"Database: `([^`]+)`", chunk)
        sql = re.search(r"```sql\n(.*?)\n```", chunk, re.S)
        items[iid] = {"db": db.group(1), "sql": sql.group(1).strip()}
    if len(items) != key["items"]:
        die(f"the sheet parses to {len(items)} items, the key records {key['items']}")

    dbroot = os.path.join(SRC, "data", "spider", "test_suite_database")
    bad = []
    for iid, r in items.items():
        p = os.path.join(dbroot, r["db"], r["db"] + ".sqlite")
        if not os.path.isfile(p):
            die(f"{iid} needs database {r['db']}, which is not staged")
        con = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
        # Same decoding as run.py: these databases carry non-UTF-8 bytes in some text columns, and a
        # check stricter than the tool the expert will actually use would reject a runnable sheet.
        con.text_factory = lambda b: b.decode("utf-8", "replace")
        try:
            con.execute(r["sql"]).fetchall()
        except sqlite3.Error as e:
            bad.append((iid, str(e)))
        finally:
            con.close()
    if bad:
        die(f"{len(bad)} queries do not execute against the bundled databases, first: {bad[0]}")

    written = []
    for rv in a.reviewers:
        stage = os.path.join(SRC, f".stage_{rv}")
        shutil.rmtree(stage, ignore_errors=True)
        os.makedirs(stage)
        for name in DOCS:
            shutil.copy2(os.path.join(SRC, name), os.path.join(stage, name))
        src_csv = os.path.join(SRC, f"RESPONSES_{rv}.csv")
        if not os.path.isfile(src_csv):
            base = open(os.path.join(SRC, f"RESPONSES_{a.reviewers[0]}.csv"), encoding="utf-8").read()
            open(src_csv, "w", encoding="utf-8").write(base)
        shutil.copy2(src_csv, os.path.join(stage, f"RESPONSES_{rv}.csv"))
        shutil.copytree(os.path.join(SRC, "data"), os.path.join(stage, "data"))
        json.dump({"reviewer": rv, "items": key["items"], "items_sha256": key["items_sha256"],
                   "built": key["built"],
                   "note": "self-contained blinded judging package; run python3 run.py --check first"},
                  open(os.path.join(stage, "PACKAGE_MANIFEST.json"), "w"), indent=1)

        out = os.path.join(ROOT, a.out_dir, f"alignment-audit-{rv}.zip")
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for base, _, files in os.walk(stage):
                for f in sorted(files):
                    full = os.path.join(base, f)
                    z.write(full, os.path.join("alignment-audit",
                                               os.path.relpath(full, stage)))
        shutil.rmtree(stage)

        with zipfile.ZipFile(out) as z:
            names = z.namelist()
        leaked = [n for n in names if "key" in n.lower()
                  or re.search(r"RESPONSES_(?!%s\.csv)" % rv, n)]
        if leaked:
            die(f"{out} contains files it must not: {leaked[:5]}")
        written.append((out, len(names), os.path.getsize(out)))
        print(f"{os.path.basename(out):<28} {len(names):>5} files  {os.path.getsize(out)/1e6:6.1f} MB")

    print(f"\nitem sheet sha256 {digest}")
    print("每个包只含它自己的 RESPONSES 文件，key 不在任何包里。")


if __name__ == "__main__":
    main()
