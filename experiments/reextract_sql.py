#!/usr/bin/env python3
"""Re-extract SQL from a candidates file that kept its raw generations.

A model family can put valid SQL somewhere the extractor was not looking, and the symptom is a
low parse rate rather than an error. Keeping the raw text means that is repairable without
touching a GPU. This rewrites `sql` and `parsed` in place and reports what changed, so the
correction is auditable rather than silent.
"""
import argparse, json, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e0_sample import extract_sql


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    rows = [json.loads(l) for l in open(a.candidates)]
    n = changed = parsed_before = parsed_after = no_raw = 0
    for r in rows:
        for c in r["candidates"]:
            n += 1
            parsed_before += int(bool(c.get("parsed")))
            if "raw" not in c:
                no_raw += 1
                parsed_after += int(bool(c.get("parsed")))
                continue
            sql = extract_sql(c["raw"])
            ok = (bool(sql) and not c.get("truncated")
                  and sql.lower().lstrip().startswith(("select", "with")))
            if sql != c["sql"]:
                changed += 1
            c["sql"], c["parsed"] = sql, ok
            parsed_after += int(ok)

    print(json.dumps({
        "candidates": n, "without_raw": no_raw, "sql_changed": changed,
        "parse_rate_before": round(parsed_before / n, 4),
        "parse_rate_after": round(parsed_after / n, 4),
    }, indent=1))
    if a.dry_run:
        return
    with open(a.out, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    meta_in = a.candidates.replace(".jsonl", "_meta.json")
    if os.path.isfile(meta_in):
        m = json.load(open(meta_in))
        m.setdefault("instrument_checks", {})
        m["instrument_checks"]["parse_rate_before_reextraction"] = round(parsed_before / n, 4)
        m["instrument_checks"]["parse_rate"] = round(parsed_after / n, 4)
        m["instrument_checks"]["reextraction"] = (
            "the first extractor read only up to the first fence, which for a model that writes "
            "prose then opens its own fenced block captures the prose; re-extracted offline from "
            "the kept raw generations")
        json.dump(m, open(a.out.replace(".jsonl", "_meta.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
