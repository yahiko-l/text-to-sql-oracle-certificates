#!/usr/bin/env python3
"""Instrument diagnostic: does a checkpoint generate coherent text at all, and does our encoding
feed it what its model card prescribes? Greedy decoding of one short prompt three ways:
(1) vLLM with the chat template plus the prescribed assistant prefix (the pilot path),
(2) vLLM with the raw text and no chat template,
(3) transformers greedy on the same token ids, to separate a vLLM problem from a checkpoint problem.
Prints the prompt token ids so a doubled BOS is visible. Read-only, one card, a few minutes.
"""
import argparse, json, sys

ap = argparse.ArgumentParser()
ap.add_argument("--model", required=True)
ap.add_argument("--prompts", default="experiments/pilot3_prompts_llama3_sqlcoder.jsonl")
ap.add_argument("--max-tokens", type=int, default=80)
ap.add_argument("--skip-transformers", action="store_true")
a = ap.parse_args()

from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained(a.model)
row = json.loads(open(a.prompts).readline())
chat = tok.apply_chat_template([{"role": "user", "content": row["prompt"]}], tokenize=False,
                               add_generation_prompt=True) + row.get("assistant_prefix", "")
ids_chat = tok.encode(chat, add_special_tokens=False)
ids_chat_default = tok.encode(chat)          # what vLLM does with a text prompt: add_special_tokens=True
print("chat text head:", repr(chat[:120]))
print("chat ids head (add_special_tokens=False):", ids_chat[:6], "len", len(ids_chat))
print("chat ids head (default tokenizer call):  ", ids_chat_default[:6], "len", len(ids_chat_default))
print("bos id:", tok.bos_token_id, "eos:", tok.eos_token_id)

from vllm import LLM, SamplingParams
llm = LLM(model=a.model, tensor_parallel_size=1, dtype="bfloat16", max_model_len=4096,
          gpu_memory_utilization=0.5, trust_remote_code=True, seed=0)
sp = SamplingParams(temperature=0.0, max_tokens=a.max_tokens)
o = llm.generate([chat], sp)[0]
print("\n[1] vLLM text prompt (chat template + prefix), prompt_token_ids head:", o.prompt_token_ids[:6])
print("    OUT:", repr(o.outputs[0].text))
o = llm.generate([{"prompt_token_ids": ids_chat}], sp)[0]
print("\n[1b] vLLM token ids without a second BOS:")
print("    OUT:", repr(o.outputs[0].text))
o = llm.generate(["SELECT count(*) FROM singer;\n-- The query above counts"], sp)[0]
print("\n[2] vLLM raw completion of a trivial text:")
print("    OUT:", repr(o.outputs[0].text))
del llm

if not a.skip_transformers:
    import torch
    from transformers import AutoModelForCausalLM
    m = AutoModelForCausalLM.from_pretrained(a.model, torch_dtype=torch.bfloat16, device_map="cuda")
    x = torch.tensor([ids_chat], device="cuda")
    with torch.no_grad():
        y = m.generate(x, max_new_tokens=a.max_tokens, do_sample=False)
    print("\n[3] transformers greedy on the same ids:")
    print("    OUT:", repr(tok.decode(y[0][x.shape[1]:], skip_special_tokens=False)))
