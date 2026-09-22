#!/usr/bin/env python3
"""E0 step 2 (remote, GPU): sample SQL candidates with vLLM under a declared policy.

Reads the prompt file produced by e0_build_prompts.py, applies the model's chat template,
and draws a fixed number of independent temperature samples per question. Records for each
candidate: the extracted SQL, the cumulative sequence log-probability, the token count and the
finish reason. Only the count-based class mass is used downstream; the log-probability is kept
so the artifact does not have to be regenerated if a later question needs it.

Instrument validity is checked in the same pass, because a broken parser returns numbers
rather than errors: parse rate, truncation rate, and a negative control. Two controls exist:
--scramble-schema shuffles the lines of the schema block (a format-sensitivity control, the
schema content stays available), and --false-schema replaces the schema block by that of a
DIFFERENT database of the same benchmark, so that no correct query can be written from the
prompt and a working certificate must abstain.
"""
import argparse, hashlib, json, os, random, re, sys, time


THINK_RE = re.compile(r"^\s*<think>.*?</think>\s*", re.S)
FENCE_RE = re.compile(r"```[ \t]*(?:sqlite|sql)?[ \t]*\r?\n(.*?)```", re.S | re.I)


def strip_leading_comments(sql):
    """Drop full-line -- comments at the top of the query (the OmniSQL output format shows a
    "-- Your SQL query" placeholder line, which some models echo before the query)."""
    lines = sql.strip().split("\n")
    while lines and lines[0].strip().startswith("--"):
        lines.pop(0)
    return "\n".join(lines).strip()


def extract_sql(text, mode=None):
    """Pull the SQL out of one generation.

    `mode` is the answer mode the prompt builder wrote into the prompt row:

    continuation  the prompt (or the assistant prefix) ends inside an opened ```sql fence and the
                  model continues inside it, so the answer is everything up to the closing fence.
    fenced        the model writes prose of its own and encloses the query in a fenced block; a
                  chain of thought may draft earlier blocks, so the LAST non-empty block is the
                  answer (the OmniSQL evaluation code reads it the same way).
    bare          the answer is the raw continuation, ended by [/SQL], a new ### section or EOS
                  (SQLCoder completion prompt); a model that fences anyway is read from the fence.
    None          the Preregistration 2 reading, kept for prompt files without an answer mode:
                  a complete fenced block first, else the continuation up to the first fence.
                  DeepSeek-V4 ignored the opened fence, wrote a paragraph and then opened a fence
                  of its own; reading only up to the first ``` captured the prose, which is how a
                  parse rate of 0.35 arose from generations that all contained valid SQL.

    A leading <think>...</think> block is removed in every mode. A block that never closes is a
    truncated scratchpad and stays in the text, where it fails the parse check as it should.
    """
    t = THINK_RE.sub("", text.strip(), count=1)
    if mode == "continuation":
        cut = t.find("```")
        t = t if cut < 0 else t[:cut]
        t = re.sub(r"^\s*sql\s*\n", "", t, flags=re.I)
    elif mode == "fenced":
        blocks = [b for b in FENCE_RE.findall(t) if b.strip()]
        if blocks:
            t = blocks[-1]
        else:
            cut = t.find("```")
            t = t if cut < 0 else t[:cut]
    elif mode == "bare":
        m = FENCE_RE.search(t)
        if m:
            t = m.group(1)
        else:
            ends = [x.start() for x in (re.search(r"\[/SQL\]", t, re.I), re.search(r"\n###", t)) if x]
            if ends:
                t = t[: min(ends)]
    else:
        m = FENCE_RE.search(t)
        if m:
            t = m.group(1)
        else:
            cut = re.search(r"```", t)
            if cut:
                t = t[: cut.start()]
            t = re.sub(r"^\s*sql\s*\n", "", t, flags=re.I)
    return strip_leading_comments(t).rstrip(";").strip()


def scramble(prompt, rng):
    """Negative control 1: shuffle the lines of the schema block. The schema content stays in
    the prompt, so this tests format sensitivity, not the absence of the schema."""
    m = re.search(r"(【数据库schema】\n)(.*?)(\n\n【参考信息】)", prompt, re.S)
    if not m:
        return prompt
    lines = [l for l in m.group(2).split("\n") if l.strip()]
    rng.shuffle(lines)
    return prompt[: m.start(2)] + "\n".join(lines) + prompt[m.end(2):]


def false_schema(rows):
    """Negative control 2: give every question the schema of ANOTHER database.

    Deterministic rotation by one position in the sorted list of database ids, so the mapping
    is reproducible and is written to the metadata. Needs the `schema_block` field that
    e0_build_prompts.py writes; the block is replaced verbatim inside the rendered prompt.
    """
    blocks = {}
    for r in rows:
        if "schema_block" not in r:
            sys.exit("false-schema control needs prompt rows with a schema_block field; "
                     "rebuild the prompt file with the current e0_build_prompts.py")
        blocks.setdefault(r["db_id"], r["schema_block"])
    dbs = sorted(blocks)
    if len(dbs) < 2:
        sys.exit("false-schema control needs at least two databases")
    mapping = {d: dbs[(i + 1) % len(dbs)] for i, d in enumerate(dbs)}
    for r in rows:
        if r["schema_block"] not in r["prompt"]:
            sys.exit(f"schema_block of qid {r['qid']} not found verbatim in its prompt")
        r["prompt"] = r["prompt"].replace(r["schema_block"], blocks[mapping[r["db_id"]]], 1)
    return mapping


def sha256_file(path):
    hh = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            hh.update(chunk)
    return hh.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompts", default="experiments/e0_prompts.jsonl")
    ap.add_argument("--out", default="experiments/e0_candidates.jsonl")
    ap.add_argument("--model", default="XGenerationLab/XiYanSQL-QwenCoder-32B-2504")
    ap.add_argument("--tp", type=int, default=4)
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--top-p", type=float, default=0.95)
    ap.add_argument("--max-tokens", type=int, default=512)
    ap.add_argument("--max-model-len", type=int, default=8192)
    ap.add_argument("--seed", type=int, default=20260903)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--scramble-schema", action="store_true",
                    help="negative control 1: shuffle the schema lines (format sensitivity)")
    ap.add_argument("--false-schema", action="store_true",
                    help="negative control 2: replace the schema by another database's schema; "
                         "no correct query is writable, so a working certificate must abstain")
    ap.add_argument("--encoder", choices=("chat_template", "deepseek_v4", "raw"),
                    default="chat_template",
                    help="how to turn the prompt into model input. DeepSeek-V4 ships no Jinja "
                         "chat template at all; it ships an official encoder in the checkpoint's "
                         "encoding/ folder instead, and that is what this path calls. 'raw' sends "
                         "the prompt text as is (a completion-style model such as SQLCoder-70B, "
                         "whose checkpoint has no chat template); the tokenizer still adds BOS.")
    ap.add_argument("--chat-template-kwargs", default="",
                    help="JSON object passed to apply_chat_template, for example "
                         "'{\"enable_thinking\": false}' or '{\"reasoning_effort\": \"low\"}'; "
                         "recorded in the metadata")
    ap.add_argument("--system-prompt", default="",
                    help="optional system message put before the user prompt; recorded")
    ap.add_argument("--keep-raw", action="store_true",
                    help="store each generation verbatim. Model families differ in output "
                         "behaviour, not only in accuracy: a reasoning model emits a thinking "
                         "block and a broken extractor then returns numbers rather than errors. "
                         "Keeping the raw text means a wrong extractor can be fixed offline "
                         "instead of reloading the weights.")
    ap.add_argument("--gpu-memory-utilization", type=float, default=0.90)
    ap.add_argument("--dtype", default="bfloat16")
    ap.add_argument("--kv-cache-dtype", default="auto",
                    help="DeepSeek-V4 refuses to build unless this is fp8: its MLA attention "
                         "asserts on the kv-cache format at layer construction time.")
    a = ap.parse_args()
    if a.scramble_schema and a.false_schema:
        sys.exit("choose one negative control")

    import vllm
    from vllm import LLM, SamplingParams
    from transformers import AutoTokenizer

    rows = [json.loads(l) for l in open(a.prompts)]
    if a.limit:
        rows = rows[: a.limit]
    rng = random.Random(a.seed)
    control = "none"
    mapping = None
    if a.scramble_schema:
        control = "scrambled_schema"
        for r in rows:
            r["prompt"] = scramble(r["prompt"], rng)
    elif a.false_schema:
        control = "false_schema"
        mapping = false_schema(rows)
    ct_kwargs = json.loads(a.chat_template_kwargs) if a.chat_template_kwargs else {}

    tok = AutoTokenizer.from_pretrained(a.model)
    # a partial assistant turn prescribed by the model card (llama-3-sqlcoder-8b) follows the
    # generation prompt verbatim; the prompt builder writes it into the row
    prefix = lambda r: r.get("assistant_prefix", "")
    if a.encoder == "chat_template":
        def msgs(p):
            m = [{"role": "system", "content": a.system_prompt}] if a.system_prompt else []
            return m + [{"role": "user", "content": p}]
        texts = [tok.apply_chat_template(msgs(r["prompt"]), tokenize=False,
                                         add_generation_prompt=True, **ct_kwargs) + prefix(r)
                 for r in rows]
        gen_input = texts
        n_prompt_tokens = [len(tok.encode(t, add_special_tokens=False)) for t in texts]
    elif a.encoder == "raw":
        texts = [r["prompt"] + prefix(r) for r in rows]
        gen_input = texts
        n_prompt_tokens = [len(tok.encode(t)) for t in texts]
    else:
        # thinking_mode="chat" closes the reasoning block immediately, so the model answers
        # directly. That is what keeps this arm comparable to the other one: the axis under
        # test is the model family, not how much scratchpad each model writes.
        sys.path.insert(0, os.path.join(a.model, "encoding"))
        from encoding_dsv4 import encode_messages
        texts = [encode_messages([{"role": "user", "content": r["prompt"]}], thinking_mode="chat")
                 for r in rows]
        # the encoder already emits BOS, so tokenize without letting the tokenizer add another
        gen_input = [{"prompt_token_ids": tok.encode(t, add_special_tokens=False)} for t in texts]
        n_prompt_tokens = [len(g["prompt_token_ids"]) for g in gen_input]
    longest = max(n_prompt_tokens)
    if longest + a.max_tokens > a.max_model_len:
        sys.exit(f"longest prompt is {longest} tokens; with max_tokens {a.max_tokens} it exceeds "
                 f"max_model_len {a.max_model_len}, so some generations would be cut short by the "
                 f"context window rather than by the declared budget. Raise --max-model-len.")
    answer_modes = {r.get("answer_mode") for r in rows}
    if len(answer_modes) != 1:
        sys.exit(f"prompt rows carry more than one answer mode: {answer_modes}")
    answer_mode = answer_modes.pop()

    llm = LLM(model=a.model, tensor_parallel_size=a.tp, dtype=a.dtype,
              kv_cache_dtype=a.kv_cache_dtype,
              gpu_memory_utilization=a.gpu_memory_utilization, max_model_len=a.max_model_len,
              trust_remote_code=True, seed=a.seed)
    # logprobs=0 is what makes vLLM populate cumulative_logprob; without it the field is None.
    sp = SamplingParams(n=a.n, temperature=a.temperature, top_p=a.top_p,
                        max_tokens=a.max_tokens, seed=a.seed, logprobs=0)

    t0 = time.time()
    outs = llm.generate(gen_input, sp)
    elapsed = time.time() - t0

    n_cand = n_parsed = n_trunc = 0
    with open(a.out, "w") as f:
        for r, o in zip(rows, outs):
            cands = []
            for c in o.outputs:
                sql = extract_sql(c.text, answer_mode)
                trunc = (c.finish_reason == "length")
                ok = bool(sql) and sql.lower().lstrip().startswith(("select", "with"))
                n_cand += 1
                n_parsed += int(ok and not trunc)
                n_trunc += int(trunc)
                cands.append({
                    "sql": sql,
                    "cum_logprob": c.cumulative_logprob,
                    "n_tokens": len(c.token_ids),
                    "finish_reason": c.finish_reason,
                    "parsed": ok,
                    "truncated": trunc,
                })
                if a.keep_raw:
                    cands[-1]["raw"] = c.text
            rec = {"qid": r["qid"], "db_id": r["db_id"],
                   "question": r["question"], "gold": r["gold"], "candidates": cands}
            # benchmarks with a per-question test suite carry it here, so the analysis uses the
            # official suite for that question rather than everything in the directory
            if r.get("instances"):
                rec["instances"] = r["instances"]
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    meta = {
        "model": a.model,
        "arm": {"none": "main", "scrambled_schema": "negative_control_scrambled_schema",
                "false_schema": "negative_control_false_schema"}[control],
        "negative_control": control,
        "false_schema_mapping": mapping,
        "prompts": a.prompts,
        "prompts_sha256": sha256_file(a.prompts),
        "template": rows[0].get("template") if rows else None,
        "answer_mode": answer_mode,
        "assistant_prefix_used": any(r.get("assistant_prefix") for r in rows),
        "prompt_tokens": {"max": longest, "median": sorted(n_prompt_tokens)[len(n_prompt_tokens) // 2]},
        "questions": len(rows),
        "samples_per_question": a.n,
        "sampling_policy": {"kind": "independent temperature sampling, fixed budget",
                            "temperature": a.temperature, "top_p": a.top_p,
                            "max_tokens": a.max_tokens, "seed": a.seed},
        "tensor_parallel_size": a.tp,
        "encoder": a.encoder,
        "chat_template_kwargs": ct_kwargs,
        "system_prompt": a.system_prompt,
        "dtype": a.dtype,
        "kv_cache_dtype": a.kv_cache_dtype,
        "max_model_len": a.max_model_len,
        "vllm_version": vllm.__version__,
        "extractor": {"continuation": "extract_sql: continuation up to the first fence",
                      "fenced": "extract_sql: last non-empty fenced block, else text up to the first fence",
                      "bare": "extract_sql: fenced block if any, else text up to [/SQL] or a new ### section",
                      None: "extract_sql: complete fenced block first, else continuation up to the first fence"
                      }[answer_mode] + "; a leading <think> block and leading -- comment lines are dropped; "
                     "parsed = extracted text starts with SELECT or WITH (lexical check only)",
        "instrument_checks": {
            "candidates": n_cand,
            "parse_rate": round(n_parsed / n_cand, 4) if n_cand else None,
            "truncation_rate": round(n_trunc / n_cand, 4) if n_cand else None,
            "note": "a truncated generation is a cut-off scratchpad: discard it, never parse it",
            "raw_kept": bool(a.keep_raw),
        },
        "wall_clock_sec": round(elapsed, 1),
    }
    json.dump(meta, open(a.out.replace(".jsonl", "_meta.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(meta, ensure_ascii=False, indent=1), flush=True)


if __name__ == "__main__":
    main()
