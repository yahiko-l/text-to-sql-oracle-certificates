#!/usr/bin/env python3
"""Design-based uncertainty for the benchmark-wide defect estimate of the blinded human audit.

The audit's three strata are not a simple random sample of the 508 questions: the flagged stratum
was taken whole and the two controls were sampled from finite strata. The benchmark-wide figure is
therefore a stratified estimate, and its uncertainty comes only from the two sampled strata, the
enumerated one contributing none. Reported post hoc; the preregistered quantities are the per
stratum rates of Table 11.
"""
import json, math

# stratum: (population size, items audited, judged defective)
STRATA = {
    "flagged":              (73, 73, 40),
    "examined, not flagged": (130, 40, 8),
    "never examined":       (305, 40, 3),
}


def main():
    N = sum(v[0] for v in STRATA.values())
    est = var = 0.0
    rows = {}
    for name, (Nh, nh, dh) in STRATA.items():
        ph = dh / nh
        w = Nh / N
        fpc = 1.0 - nh / Nh
        vh = 0.0 if nh <= 1 or fpc == 0 else w * w * fpc * ph * (1 - ph) / (nh - 1)
        est += w * ph
        var += vh
        rows[name] = {"N": Nh, "n": nh, "defective": dh, "rate": round(ph, 4),
                      "weight": round(w, 4), "variance_contribution": vh}
    se = math.sqrt(var)
    lo, hi = est - 1.96 * se, est + 1.96 * se
    out = {"note": __doc__.strip().splitlines()[0],
           "population": N, "estimate": round(est, 4), "standard_error": round(se, 4),
           "ci95": [round(lo, 4), round(hi, 4)], "strata": rows}
    print(f"benchmark-wide estimate {est*100:.1f} percent, standard error {se*100:.1f} points, "
          f"95 percent interval {lo*100:.1f} to {hi*100:.1f}")
    for k, v in rows.items():
        print(f"  {k:<22} N={v['N']:>3} n={v['n']:>3} d={v['defective']:>2} "
              f"rate {v['rate']*100:5.1f}  variance share {v['variance_contribution']/var*100 if var else 0:5.1f}%")
    json.dump(out, open("experiments/c13_blind_audit_weighted.json", "w"), indent=1)
    print("\nSaved: experiments/c13_blind_audit_weighted.json")


if __name__ == "__main__":
    main()
