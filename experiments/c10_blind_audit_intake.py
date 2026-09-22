#!/usr/bin/env python3
"""C10 step 1d: check a returned response sheet before it enters the analysis.

A sheet comes back from a spreadsheet on someone else's machine, so it can arrive in a
different encoding, with a byte order mark, with renamed or reordered columns, or with items
missing. The analysis script is frozen with the preregistration and reads plain UTF-8, so the
normalising happens here instead: this reads the returned file, reports what is wrong with it
in the returner's terms, and writes a clean copy that the analysis can read.

  python3 experiments/c10_blind_audit_intake.py blind-audit/RESPONSES_expert1.csv
"""
import argparse
import collections
import csv
import io
import json
import os

VERDICTS = ("gold_correct", "gold_defective", "question_underspecified", "cannot_judge")
DEFECTS = ("case_sensitivity", "text_column_numeric_or_ordering", "wrong_extremum",
           "missing_join_condition", "wrong_or_negated_filter", "incomplete_projection",
           "wrong_set_operation_key", "wrong_grouping", "other")
FIELDS = ["item_id", "verdict", "defect_type", "borderline", "note"]


def decode(path):
    raw = open(path, "rb").read()
    for enc in ("utf-8-sig", "utf-8", "gb18030", "cp1252"):
        try:
            # A byte order mark survives decoding in every encoding but utf-8-sig, and
            # would otherwise rename the first column to \ufeffitem_id.
            return raw.decode(enc).lstrip("\ufeff"), enc
        except UnicodeDecodeError:
            continue
    raise SystemExit(f"{path}: cannot decode as UTF-8, GB18030 or CP1252")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("responses")
    ap.add_argument("--key", default="experiments/c10_blind_audit_key.json")
    ap.add_argument("--out", default="", help="clean copy to write; defaults to the input "
                                             "name with .clean.csv")
    ap.add_argument("--subset", action="store_true",
                    help="the sheet covers a subset of the items on purpose, as the "
                         "adjudication sheet does; do not count the rest as unanswered")
    a = ap.parse_args()

    full = [k["item_id"] for k in json.load(open(a.key))["key"]]
    expected = full
    text, enc = decode(a.responses)
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise SystemExit(f"{a.responses}: no rows")
    missing_cols = [c for c in FIELDS if c not in rows[0]]
    if missing_cols:
        raise SystemExit(f"{a.responses}: missing column(s) {', '.join(missing_cols)}. "
                         f"The sheet must keep the five columns it was sent with.")

    problems, filled = [], {}
    for i, r in enumerate(rows, 2):
        item = (r.get("item_id") or "").strip()
        v = (r.get("verdict") or "").strip()
        d = (r.get("defect_type") or "").strip()
        b = (r.get("borderline") or "").strip().lower()
        note = (r.get("note") or "").strip()
        if not item:
            problems.append(f"line {i}: no item_id")
            continue
        if not v:
            continue
        if v not in VERDICTS:
            problems.append(f"{item}: verdict {v!r} is not one of {', '.join(VERDICTS)}")
            continue
        if v == "gold_defective":
            if d and d not in DEFECTS:
                problems.append(f"{item}: defect_type {d!r} is not one of the listed types")
            if not d:
                problems.append(f"{item}: gold_defective needs a defect_type")
            if not note:
                problems.append(f"{item}: gold_defective needs a note")
        elif d:
            problems.append(f"{item}: defect_type is filled but the verdict is {v}")
        if v == "cannot_judge" and not note:
            problems.append(f"{item}: cannot_judge needs a note saying what stops you")
        if b not in ("yes", "no", "y", "n", "true", "false", "1", "0", ""):
            problems.append(f"{item}: borderline {b!r} should be yes or no")
        if not b:
            problems.append(f"{item}: borderline is empty; it is not optional")
        filled[item] = {"item_id": item, "verdict": v, "defect_type": d,
                        "borderline": "yes" if b in ("yes", "y", "true", "1") else "no",
                        "note": note}

    unknown = sorted(set(filled) - set(full))
    if a.subset:
        expected = [i for i in full if i in filled]
    unanswered = [i for i in expected if i not in filled]
    counts = collections.Counter(r["verdict"] for r in filled.values())

    print(f"file            : {a.responses}")
    print(f"encoding read as: {enc}")
    print(f"answered        : {len(filled)} of {len(expected)}")
    for v in VERDICTS:
        print(f"  {v:<24} {counts.get(v, 0)}")
    print(f"marked borderline: {sum(1 for r in filled.values() if r['borderline'] == 'yes')}")
    if unknown:
        print(f"item ids not in the sheet sent out: {', '.join(unknown)}")
    if unanswered:
        head = ", ".join(unanswered[:12]) + (" ..." if len(unanswered) > 12 else "")
        print(f"still unanswered : {len(unanswered)}  ({head})")
    if problems:
        print(f"\n{len(problems)} thing(s) to fix:")
        for p in problems[:40]:
            print(f"  {p}")
        if len(problems) > 40:
            print(f"  ... and {len(problems) - 40} more")

    out = a.out or os.path.splitext(a.responses)[0] + ".clean.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for item in expected:
            if item in filled:
                w.writerow(filled[item])
    print(f"\nwrote {out}")
    ready = not problems and not unknown and not unanswered
    print("ready for the analysis" if ready else
          "send the points above back to the reviewer before analysing")


if __name__ == "__main__":
    main()
