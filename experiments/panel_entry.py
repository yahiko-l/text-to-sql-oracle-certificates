#!/usr/bin/env python3
"""Panel entry check for the second-preregistration model panel.

Reads, for each candidate tag, the sampling metadata (parse rate, truncation rate) of the
instrument pilot and the analyser output (top-1 accuracy under the strong oracle), and applies
the entry rule frozen in PREREGISTRATION_2.md. The rule is fixed here so that admission is a
computation, not a judgement:

    parse_rate >= 0.98  AND  truncation_rate <= 0.01  AND  top1_accuracy_under_strong_oracle >= 0.75

A candidate whose checkpoint failed to load is listed from the --unloadable argument with the
recorded reason and is excluded by rule, never replaced by a smaller model.
"""
import argparse, json, os

RULE = {"parse_rate_min": 0.98, "truncation_rate_max": 0.01, "top1_strong_min": 0.75}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tags", nargs="+", help="candidate tags, e.g. qwen38-27b gemma4-31b")
    ap.add_argument("--prefix", default="experiments/pilot")
    ap.add_argument("--unloadable", nargs="*", default=[],
                    help="tag=reason entries for checkpoints that failed to load")
    ap.add_argument("--out", default="experiments/panel_entry.json")
    a = ap.parse_args()

    rows = []
    for tag in a.tags:
        meta_p = f"{a.prefix}_{tag}_candidates_meta.json"
        res_p = f"{a.prefix}_{tag}_results_official.json"
        row = {"tag": tag, "meta": meta_p, "results": res_p}
        if not (os.path.isfile(meta_p) and os.path.isfile(res_p)):
            row.update({"status": "MISSING", "reason": "pilot artifacts not found"})
            rows.append(row)
            continue
        meta = json.load(open(meta_p))
        res = json.load(open(res_p))
        ic = meta["instrument_checks"]
        row.update({"model": meta["model"], "parse_rate": ic["parse_rate"],
                    "truncation_rate": ic["truncation_rate"],
                    "top1_strong": res["top1_accuracy_under_strong_oracle"],
                    "questions_usable": res["questions_usable"]})
        ok = (ic["parse_rate"] >= RULE["parse_rate_min"]
              and ic["truncation_rate"] <= RULE["truncation_rate_max"]
              and res["top1_accuracy_under_strong_oracle"] >= RULE["top1_strong_min"])
        row["status"] = "ENTER" if ok else "EXCLUDED"
        if not ok:
            why = []
            if ic["parse_rate"] < RULE["parse_rate_min"]:
                why.append("parse rate below 0.98")
            if ic["truncation_rate"] > RULE["truncation_rate_max"]:
                why.append("truncation rate above 0.01")
            if res["top1_accuracy_under_strong_oracle"] < RULE["top1_strong_min"]:
                why.append("top-1 under the strong oracle below 0.75")
            row["reason"] = "; ".join(why)
        rows.append(row)
    for u in a.unloadable:
        tag, _, reason = u.partition("=")
        rows.append({"tag": tag, "status": "UNLOADABLE", "reason": reason})

    out = {"rule": RULE, "candidates": rows,
           "panel": [r["tag"] for r in rows if r["status"] == "ENTER"]}
    json.dump(out, open(a.out, "w"), indent=1, ensure_ascii=False)
    for r in rows:
        print(f"{r['tag']:>16}  {r['status']:<10} parse={r.get('parse_rate')} trunc={r.get('truncation_rate')} "
              f"top1={r.get('top1_strong')}  {r.get('reason', '')}")
    print("panel:", out["panel"])


if __name__ == "__main__":
    main()
