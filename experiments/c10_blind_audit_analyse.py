#!/usr/bin/env python3
"""C10 step 2: the preregistered analysis of the blinded expert audit.

Written and committed BEFORE any human label exists, together with
blind-audit/PREREGISTRATION.md. That is the whole point: this project has repeatedly had to record
that an analysis was post hoc, and the one measurement its headline now rests on should not be. The
decision rule below is the one in the preregistration, with the thresholds as literals, so a later
change to either is a diff and cannot be quiet.

  --self-test   run the decision rule on synthetic inputs that are constructed to land in each of
                the three verdicts, before real data exists. It proves the rule can both pass and
                fail rather than only pass.
  --responses   one or two filled RESPONSES.csv files. With two, agreement and Cohen's kappa are
                computed and the primary analysis uses the adjudicated file if one is given.
"""
import argparse, collections, csv, json, math, os, sys

VERDICTS = ("gold_correct", "gold_defective", "question_underspecified", "cannot_judge")
STRATA = ("flagged", "examined", "unexamined")

# The preregistered decision rule, as literals. blind-audit/PREREGISTRATION.md section 2.
SUPPORT_MARGIN = 0.25      # D(flagged) - D(examined) at or above this supports the assumption
SUPPORT_LEVEL = 0.40       # and D(flagged) must also reach this
REFUTE_MARGIN = 0.10       # below this margin the assumption is refuted


def clopper_pearson(k, n, alpha=0.05):
    """Exact binomial interval, by bisection on the binomial tail. No scipy dependency."""
    if n == 0:
        return (0.0, 1.0)

    def cdf(p, upto):
        return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(upto + 1))

    def solve(target, tail_upto, lo=0.0, hi=1.0):
        for _ in range(200):
            mid = (lo + hi) / 2
            if cdf(mid, tail_upto) > target:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    low = 0.0 if k == 0 else solve(1 - alpha / 2, k - 1)
    high = 1.0 if k == n else solve(alpha / 2, k)
    return (round(low, 4), round(high, 4))


def cohen_kappa(a, b):
    """Cohen's kappa for two aligned label sequences."""
    n = len(a)
    if n == 0:
        return None
    obs = sum(1 for x, y in zip(a, b) if x == y) / n
    ca, cb = collections.Counter(a), collections.Counter(b)
    exp = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return None if exp == 1 else round((obs - exp) / (1 - exp), 4)


def read_responses(path):
    rows = {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            v = (r.get("verdict") or "").strip()
            if not v:
                continue
            if v not in VERDICTS:
                raise SystemExit(f"{path}: item {r['item_id']} has verdict {v!r}, "
                                 f"which is not one of {VERDICTS}")
            rows[r["item_id"].strip()] = {
                "verdict": v,
                "defect_type": (r.get("defect_type") or "").strip() or None,
                "borderline": (r.get("borderline") or "").strip().lower() in ("yes", "y", "true", "1"),
                "note": (r.get("note") or "").strip()}
    return rows


def rates(key, resp, drop_borderline=False):
    """D per stratum: the share judged gold_defective, over every sampled item of that stratum."""
    out = {}
    for s in STRATA:
        ids = [k["item_id"] for k in key if k["stratum"] == s and k["item_id"] in resp]
        if drop_borderline:
            ids = [i for i in ids if not resp[i]["borderline"]]
        d = sum(1 for i in ids if resp[i]["verdict"] == "gold_defective")
        out[s] = {"n": len(ids), "defective": d,
                  "D": round(d / len(ids), 4) if ids else None,
                  "interval95": clopper_pearson(d, len(ids)),
                  "underspecified": sum(1 for i in ids
                                        if resp[i]["verdict"] == "question_underspecified"),
                  "cannot_judge": sum(1 for i in ids if resp[i]["verdict"] == "cannot_judge")}
    return out


def decide(r):
    """The preregistered three-way verdict. Thresholds are the literals above."""
    f, e = r["flagged"]["D"], r["examined"]["D"]
    if f is None or e is None:
        return {"verdict": "incomputable", "margin": None,
                "reason": "a stratum has no usable responses"}
    m = round(f - e, 4)
    if m >= SUPPORT_MARGIN and f >= SUPPORT_LEVEL:
        v = "supported"
    elif m < REFUTE_MARGIN:
        v = "refuted"
    else:
        v = "partially_supported"
    return {"verdict": v, "margin": m, "D_flagged": f, "D_examined": e,
            "rule": f"supported if margin >= {SUPPORT_MARGIN} and D(flagged) >= {SUPPORT_LEVEL}; "
                    f"refuted if margin < {REFUTE_MARGIN}; otherwise partially supported"}


def analyse(key, resp, tiers):
    primary = rates(key, resp)
    result = {
        "items_answered": len(resp), "items_total": len(key),
        "rates": primary,
        "rates_excluding_borderline": rates(key, resp, drop_borderline=True),
        "decision": decide(primary),
        "decision_excluding_borderline": decide(rates(key, resp, drop_borderline=True)),
        "background_gold_defect_rate": {
            "estimate": primary["unexamined"]["D"],
            "interval95": primary["unexamined"]["interval95"],
            "note": "the only figure in this project that may be used to speak about the "
                    "benchmark's overall gold defect rate. The 73 flagged questions are a "
                    "model-exposed count and must not be extrapolated on their own."},
    }
    ids = [k["item_id"] for k in key if k["item_id"] in resp]
    result["human_vs_ai"] = {
        "n": len(ids),
        "agreement": round(sum(1 for i in ids
                               if (resp[i]["verdict"] == "gold_defective")
                               == (next(k for k in key if k["item_id"] == i)["stratum"] == "flagged")
                               ) / len(ids), 4) if ids else None,
        "kappa": cohen_kappa([resp[i]["verdict"] == "gold_defective" for i in ids],
                             [next(k for k in key if k["item_id"] == i)["stratum"] == "flagged"
                              for i in ids])}
    by_tier = collections.defaultdict(list)
    for k in key:
        if k["stratum"] == "flagged" and k["item_id"] in resp:
            by_tier[k["ai_gold_defect_tier"]].append(k["item_id"])
    result["by_ai_label_strength"] = {
        t: {"n": len(v), "defective": sum(1 for i in v if resp[i]["verdict"] == "gold_defective"),
            "D": round(sum(1 for i in v if resp[i]["verdict"] == "gold_defective") / len(v), 4),
            "interval95": clopper_pearson(sum(1 for i in v
                                              if resp[i]["verdict"] == "gold_defective"), len(v))}
        for t, v in sorted(by_tier.items())}
    result["defect_types"] = dict(collections.Counter(
        resp[i]["defect_type"] for i in ids if resp[i]["verdict"] == "gold_defective"))
    by_db = collections.defaultdict(lambda: collections.Counter())
    for k in key:
        if k["item_id"] in resp:
            by_db[k["db"]][resp[k["item_id"]]["verdict"]] += 1
    result["by_database"] = {d: dict(c) for d, c in sorted(by_db.items())}
    return result


def self_test():
    """Prove the preregistered rule can return each verdict, before any real data exists."""
    key = ([{"item_id": f"F{i}", "stratum": "flagged", "db": "x", "ai_gold_defect_tier": "t"}
            for i in range(20)]
           + [{"item_id": f"E{i}", "stratum": "examined", "db": "x", "ai_gold_defect_tier": None}
              for i in range(20)]
           + [{"item_id": f"U{i}", "stratum": "unexamined", "db": "x", "ai_gold_defect_tier": None}
              for i in range(20)])

    def resp(fd, ed):
        r = {}
        for i in range(20):
            r[f"F{i}"] = {"verdict": "gold_defective" if i < fd else "gold_correct",
                          "defect_type": None, "borderline": False, "note": ""}
            r[f"E{i}"] = {"verdict": "gold_defective" if i < ed else "gold_correct",
                          "defect_type": None, "borderline": False, "note": ""}
            r[f"U{i}"] = {"verdict": "gold_correct", "defect_type": None,
                          "borderline": False, "note": ""}
        return r

    cases = [("supported", 14, 1), ("partially_supported", 8, 4), ("refuted", 5, 4)]
    ok = True
    for want, fd, ed in cases:
        got = decide(rates(key, resp(fd, ed)))
        mark = "ok" if got["verdict"] == want else "MISMATCH"
        if got["verdict"] != want:
            ok = False
        print(f"  D(flagged)={fd / 20:.2f} D(examined)={ed / 20:.2f} margin={got['margin']:+.2f} "
              f"-> {got['verdict']:<20} expected {want:<20} {mark}")
    print(f"  Clopper-Pearson sanity: 0/40 {clopper_pearson(0, 40)}, 2/40 {clopper_pearson(2, 40)}, "
          f"12/40 {clopper_pearson(12, 40)}, 40/40 {clopper_pearson(40, 40)}")
    print(f"  kappa sanity: identical {cohen_kappa([1, 0, 1, 0], [1, 0, 1, 0])}, "
          f"opposite {cohen_kappa([1, 1, 0, 0], [0, 0, 1, 1])}")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", default="experiments/c10_blind_audit_key.json")
    ap.add_argument("--responses", nargs="*", default=["blind-audit/RESPONSES.csv"])
    ap.add_argument("--adjudicated", default="",
                    help="the third-pass file over the disagreements; used for the primary "
                         "analysis when two expert files are given")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--out", default="experiments/c10_blind_audit_result.json")
    a = ap.parse_args()

    if a.self_test:
        print("preregistered decision rule, synthetic inputs:")
        raise SystemExit(0 if self_test() else "the decision rule did not behave as preregistered")

    K = json.load(open(a.key))
    key = K["key"]
    files = [p for p in a.responses if os.path.isfile(p)]
    if not files:
        raise SystemExit("no response file found; the package has not been filled in yet")
    passes = [read_responses(p) for p in files]
    if not any(passes):
        print(f"{files[0]} carries no verdict yet. The package is built and waiting for the "
              f"experts; nothing to analyse.")
        return

    result = {"key_items_sha256": K["items_sha256"], "seed": K["seed"],
              "response_files": files,
              "note": "analysis fixed in blind-audit/PREREGISTRATION.md before any label existed"}
    if len(passes) >= 2:
        ids = sorted(set(passes[0]) & set(passes[1]))
        result["expert_agreement"] = {
            "n": len(ids),
            "full_agreement": round(sum(1 for i in ids
                                        if passes[0][i]["verdict"] == passes[1][i]["verdict"])
                                    / len(ids), 4) if ids else None,
            "full_kappa": cohen_kappa([passes[0][i]["verdict"] for i in ids],
                                      [passes[1][i]["verdict"] for i in ids]),
            "binary_agreement": round(sum(1 for i in ids
                                          if (passes[0][i]["verdict"] == "gold_defective")
                                          == (passes[1][i]["verdict"] == "gold_defective"))
                                      / len(ids), 4) if ids else None,
            "binary_kappa": cohen_kappa([passes[0][i]["verdict"] == "gold_defective" for i in ids],
                                        [passes[1][i]["verdict"] == "gold_defective" for i in ids]),
            "disagreements": [i for i in ids
                              if passes[0][i]["verdict"] != passes[1][i]["verdict"]]}
    merged = dict(passes[0])
    for p in passes[1:]:
        for k, v in p.items():
            merged.setdefault(k, v)
    if a.adjudicated and os.path.isfile(a.adjudicated):
        merged.update(read_responses(a.adjudicated))
    result.update(analyse(key, merged, K))

    json.dump(result, open(a.out, "w"), indent=1, ensure_ascii=False)
    d = result["decision"]
    print(f"answered {result['items_answered']} of {result['items_total']} items\n")
    for s in STRATA:
        r = result["rates"][s]
        print(f"  {s:11s} n={r['n']:3d}  gold_defective {r['defective']:3d}  "
              f"D={r['D']}  95% {r['interval95']}  underspecified {r['underspecified']}")
    print(f"\n  preregistered verdict: {d['verdict'].upper()}  (margin {d['margin']})")
    print(f"  excluding borderline : {result['decision_excluding_borderline']['verdict'].upper()}")
    b = result["background_gold_defect_rate"]
    print(f"  background gold defect rate: {b['estimate']}  95% {b['interval95']}")
    print(f"\nwritten {a.out}")


if __name__ == "__main__":
    main()
