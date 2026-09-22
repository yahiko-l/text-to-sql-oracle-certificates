#!/usr/bin/env python3
"""The certificate re-scored against the expert labels, on both sides of the suite oracle.

Every audit before this one was one-sided. The census examined the answers the suite rejects and
nothing it accepts, so relabelling could only exculpate, and Section 6.1 could report that the sign
of the semantic gap was not identified. The independent-yardstick audit of PREREGISTRATION_4 judged
the answer each cell returns for every question of two checkpoints, whether the suite accepted it or
not, so it carries labels on both sides and the sign can be read off directly.

This is post hoc with respect to PREREGISTRATION_4, which preregistered the alignment endpoint and
explicitly declined to preregister a claim about the sign. It is reported as post hoc.

Three conventions decide the questions whose verdict is underspecified or not judgeable, and the
result is reported under all three rather than under a chosen one: fall back to the suite label,
fall back to the shipped-database label, or drop those questions and renormalise.
"""
import argparse, csv, json, statistics, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c4_recompute import cell_records, crc_lambda, load, make_splits, pool_files

ALPHA, SPLITS, SPLIT_SEED, GEN_SEED = 0.1, 200, 20260903, 101
USABLE = ("answers", "does_not_answer")
FALLBACKS = ("suite", "weak", "drop")


def verdicts(by, sheet, tag, cell):
    out = {}
    for i, r in by.items():
        for u in r["uses"]:
            if u["tag"] == tag and u["cell"] == cell:
                out[r["qid"]] = sheet.get(i)
    return out


def run(tag, by, sheet, fallback):
    qs = load(pool_files(tag, GEN_SEED, "question"))
    rec = {c: cell_records(qs, p, p) for c, p in (("A", "single"), ("D", "multi"))}
    # Each cell calibrates on its own oracle, so rec[c]["fit_ok"] is the shipped-database label
    # for A and the suite label for D. The shipped-database fallback needs the shipped-database
    # label of the same returned representative, which is that cell's partition scored and the
    # weak oracle labelling it.
    wk = {c: cell_records(qs, p, "single") for c, p in (("A", "single"), ("D", "multi"))}
    hv = {c: verdicts(by, sheet, tag, c) for c in ("A", "D")}
    ids = [q["qid"] for q in qs]
    dbs = {q["qid"]: q["db"] for q in qs}

    def wrong(c, i):
        v = hv[c].get(i)
        if v in USABLE:
            return v == "does_not_answer"
        return not rec[c][i]["strong_ok"] if fallback == "suite" else not wk[c][i]["fit_ok"]

    gap, dma, lv = [], [], {"weak": [], "suite": [], "expert": []}
    for calq, tstq in make_splits(ids, dbs, "question", SPLITS, SPLIT_SEED):
        lam = {c: crc_lambda([(rec[c][i]["top_mass"], not rec[c][i]["fit_ok"]) for i in calq], ALPHA)
               for c in ("A", "D")}
        keep = ([i for i in tstq if hv["A"].get(i) in USABLE and hv["D"].get(i) in USABLE]
                if fallback == "drop" else list(tstq))
        n = len(keep)
        if not n:
            continue
        ans = {c: [i for i in keep if rec[c][i]["top_mass"] >= lam[c]] for c in ("A", "D")}
        r_weak = sum(1 for i in ans["A"] if not rec["A"][i]["fit_ok"]) / n
        lv["weak"].append(r_weak)
        lv["suite"].append(sum(1 for i in ans["A"] if not rec["A"][i]["strong_ok"]) / n)
        lv["expert"].append(sum(1 for i in ans["A"] if wrong("A", i)) / n)
        gap.append(sum(1 for i in ans["A"] if wrong("A", i)) / n - r_weak)
        dma.append(sum(1 for i in ans["D"] if wrong("D", i)) / n
                   - sum(1 for i in ans["A"] if wrong("A", i)) / n)
    return (statistics.mean(gap) * 100, statistics.mean(dma) * 100,
            {k: round(statistics.mean(v) * 100, 2) for k, v in lv.items()})


def sides(tag, by, sheet):
    """How each side of the suite oracle looks to the experts, for cell A's returned answer."""
    qs = load(pool_files(tag, GEN_SEED, "question"))
    rec = cell_records(qs, "single", "single")
    hv = verdicts(by, sheet, tag, "A")
    out = {}
    for name, want in (("suite_accepted", True), ("suite_rejected", False)):
        ids = [i for i in rec if rec[i]["strong_ok"] is want and hv.get(i) in USABLE]
        bad = sum(1 for i in ids if hv[i] == "does_not_answer")
        out[name] = {"n": len(ids), "expert_wrong": bad,
                     "share": round(bad / len(ids), 4) if ids else None}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", default="experiments/c15_alignment_audit_key.json")
    ap.add_argument("--out", default="experiments/c18_human_gap.json")
    a = ap.parse_args()
    key = json.load(open(a.key))
    by = {r["item_id"]: r for r in key["key"]}
    tags = key["checkpoints"]
    S = {e: {r["item_id"].strip(): (r.get("verdict") or "").strip()
             for r in csv.DictReader(open(f"experiments/alignment-audit/RESPONSES_{e}.csv",
                                          encoding="utf-8-sig"))} for e in ("E1", "E2")}
    sheets = {"agreed": {i: S["E1"][i] for i in by if S["E1"][i] == S["E2"][i]},
              "E1": S["E1"], "E2": S["E2"]}

    rep = {"note": __doc__.strip().splitlines()[0], "post_hoc": True, "sides": {}, "certificate": {}}
    print("each side of the suite oracle under expert labels, cell A's returned answer\n")
    for tag in tags:
        s = sides(tag, by, sheets["agreed"])
        rep["sides"][tag] = s
        for k, v in s.items():
            print(f"  {tag:<20} {k:<16} n={v['n']:>4}  experts call wrong {v['expert_wrong']:>3} "
                  f"({v['share']*100:4.1f}%)")

    print(f"\n{'labels / fallback':<26}" + "".join(f"{t.split('-')[0]:>22}" for t in tags))
    print(f"{'':<26}" + "".join(f"{'GAP':>11}{'D-A':>11}" for _ in tags))
    for sk, sheet in sheets.items():
        for fb in FALLBACKS:
            row = [run(t, by, sheet, fb) for t in tags]
            rep["certificate"].setdefault(sk, {})[fb] = {
                t: {"gap": round(g, 4), "dma": round(d, 4), "levels": lv}
                for t, (g, d, lv) in zip(tags, row)}
            print(f"{sk + ' / ' + fb:<26}" + "".join(f"{g:>+11.2f}{d:>+11.2f}" for g, d, _ in row))

    allg = [v[t]["gap"] for s in rep["certificate"].values() for v in s.values() for t in tags]
    alld = [v[t]["dma"] for s in rep["certificate"].values() for v in s.values() for t in tags]
    rep["gap_range"] = [round(min(allg), 2), round(max(allg), 2)]
    rep["dma_range"] = [round(min(alld), 2), round(max(alld), 2)]
    rep["gap_positive_everywhere"] = min(allg) > 0
    print(f"\nGAP over all nine conventions and both checkpoints: {min(allg):+.2f} to {max(allg):+.2f}"
          f"   positive everywhere: {min(allg) > 0}")
    print(f"D minus A: {min(alld):+.2f} to {max(alld):+.2f}   negative everywhere: {max(alld) < 0}")
    json.dump(rep, open(a.out, "w"), indent=1)
    print("\nSaved: " + a.out)


if __name__ == "__main__":
    main()
