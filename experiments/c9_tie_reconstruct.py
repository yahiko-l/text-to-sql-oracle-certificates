#!/usr/bin/env python3
"""C9 step 1: reconstruct the frozen analyser's top-class choice wherever the top class is tied.

The frozen analyser breaks a tie among equal-mass top classes by the union-find class key, which is
an integer, taking the LARGEST (e0_analyse.py, cell_records:
`max(masses, key=lambda k: (masses[k], k))`). The per-question file it writes does not carry that
key: it sorts classes by descending count and then by the STRINGIFIED key
(`sorted(..., key=lambda kv: (-kv[1], str(kv[0])))`). Everything that recomputes from that file,
which is c4_recompute, c6, c7 and c8, takes the first listed class on a tie, and "first listed
stringified" is not "largest integer".

c4_recompute documented the gap and exposed it as a `--tie-break` option, and the residual it leaves
on the headline numbers is small and was already reported. What nobody checked is that the same
proxy also selects WHICH ANSWERS the semantic censuses audit. This script reconstructs the frozen
choice by re-running the union-find on exactly the questions where a tie exists, so the size of that
error can be measured instead of assumed.

Only tied questions are reconstructed, because only they can differ: with no tie the maximum is
unique and every rule picks it. The reconstruction repeats the analyser exactly: same instance
order with the shipped database at index 0, same gold-anchored item order, same official comparator,
same order_matters rule from the question's gold, same representative rule.

Reads the tie list written by c9_tie_audit.py --enumerate.
"""
import collections, json, os, re, sqlite3, sys, time
sys.path.insert(0,'experiments')
from e0_analyse import union_find_classes, _load_official_result_eq, run, h

result_eq=_load_official_result_eq("data/spider/exec_eval.py")
ROOT="data/spider/test_suite_database"
tied=json.load(open("experiments/c9_tied_decisions.json"))["tied"]
byq=collections.defaultdict(list)
for x in tied: byq[(x["tag"],x["seed"],x["qid"])].append(x)

pools={}
def pool(tag,seed):
    k=(tag,seed)
    if k not in pools:
        d={}
        for line in open(f"experiments/c4_{tag}_seed{seed}_candidates.jsonl"):
            r=json.loads(line); d[r["qid"]]=r
        pools[k]=d
    return pools[k]

out=[]; t0=time.time()
for (tag,seed,qid),rows in sorted(byq.items()):
    r=pool(tag,seed)[qid]
    db=r["db_id"]; ddir=os.path.join(ROOT,db); orig=f"{db}.sqlite"
    insts=[orig]+sorted(f for f in os.listdir(ddir) if f.endswith(".sqlite") and f!=orig)
    om=bool(re.search(r"\border\s+by\b", r["gold"], re.I))
    cands=[c for c in r["candidates"] if c.get("parsed") and not c.get("truncated") and c["sql"]]
    need={r["gold"]}|{c["sql"] for c in cands}
    sig={s:[] for s in need}
    for inst in insts:
        con=sqlite3.connect(f"file:{os.path.join(ddir,inst)}?mode=ro",uri=True)
        con.text_factory=lambda b: b.decode("utf-8","replace")
        for s in sorted(need):
            res,err=run(con,s)
            # The analyser keeps the QUERY IDENTITY in a failure signature, so two unrelated
            # queries that both raise OperationalError never merge into one class
            # (e0_analyse.py: "ERR:" + err + ":" + h(sql)[:12]). Dropping the hash, as the first
            # version of this script did, lets them merge and changes the reconstruction.
            sig[s].append(("ERR:" + err + ":" + h(s)[:12]) if err else res)
        con.close()
    def eq(x,y):
        if isinstance(x,str) or isinstance(y,str): return x==y
        return bool(result_eq(x,y,om))
    order=[r["gold"]]+[c["sql"] for c in cands]
    seen=set(); sqls=[]
    for q_ in order:
        if q_ not in seen: seen.add(q_); sqls.append(q_)
    cls_s,_=union_find_classes(sqls, lambda x,y: eq(sig[x][0],sig[y][0]))
    cls_m,_=union_find_classes(sqls, lambda x,y: all(eq(sig[x][i],sig[y][i]) for i in range(len(insts))))
    for row in rows:
        part=row["part"]; keyf=cls_s if part=="single" else cls_m
        counter=collections.Counter(keyf[c["sql"]] for c in cands)
        n=sum(counter.values()); masses={k:v/n for k,v in counter.items()}
        top=max(masses, key=lambda k:(masses[k],k))
        bag=collections.defaultdict(collections.Counter)
        for c in cands: bag[keyf[c["sql"]]][c["sql"]]+=1
        rep=min(bag[top].items(), key=lambda kv:(-kv[1],kv[0]))[0]
        gold_s=cls_s[r["gold"]]; gold_m=cls_m[r["gold"]]
        weak = cls_s[rep]==gold_s; strong = cls_m[rep]==gold_m
        file_rep=row["reps"][0]
        out.append({"tag":tag,"seed":seed,"qid":qid,"part":part,
                    "frozen_rep":rep,"file_rep":file_rep,"same_rep":rep==file_rep,
                    "frozen_weak":weak,"frozen_strong":strong,
                    "file_weak":row["weak"][0],"file_strong":row["strong"][0],
                    "same_labels": weak==row["weak"][0] and strong==row["strong"][0]})
    print(f"  {tag} s{seed} q{qid} {db} insts={len(insts)} t={time.time()-t0:.0f}s", flush=True)

json.dump({"note": "the frozen analyser's top-class choice on every tied decision, against the "
                   "first-listed choice every recomputation from the per-question files makes",
           "decisions": out}, open("experiments/c9_tie_reconstruction.json", "w"), indent=1)
d=sum(1 for x in out if not x["same_rep"]); dl=sum(1 for x in out if not x["same_labels"])
print(f"\n{len(out)} tied decisions reconstructed")
print(f"  representative differs from the file-first choice: {d}")
print(f"  correctness labels differ:                         {dl}")
