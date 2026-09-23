#!/usr/bin/env bash
# Matched original-Spider control (post-hoc).
#
# Same databases, same gold SQL, same schema serialisation, same prompt template, same seeds as
# Preregistration 3; only the question text differs, being the ORIGINAL Spider dev wording instead
# of the Spider-Realistic rewrite. It isolates whether the oracle gap is a property of the
# rewritten questions or of the benchmark family.
#
#   experiments/c5_run.sh <tag> <generation-seed> [gpu_memory_utilization]
set -euo pipefail
TAG=${1:?tag}; SEED=${2:?seed}; UTIL=${3:-0.90}
M=${MODEL_ROOT:?set MODEL_ROOT to the directory holding the checkpoints}
NGPU=$(python -c "import os;print(len([c for c in os.environ.get('CUDA_VISIBLE_DEVICES','').split(',') if c]))")
[ "$NGPU" -ge 1 ] || { echo "CUDA_VISIBLE_DEVICES is empty"; exit 2; }

EXTRA=()
case "$TAG" in
  xiyansql-32b)     MODEL=$M/XGenerationLab/XiYanSQL-QwenCoder-32B-2504; TPL=xiyan_cn; MAXTOK=512 ;;
  omnisql-32b)      MODEL=$M/OmniSQL/OmniSQL-32B;                        TPL=omnisql;  MAXTOK=2048 ;;
  kwai-autosql-32b) MODEL=$M/Kwai-AutoSQL/Kwai-AutoSQL-32B;              TPL=omnisql;  MAXTOK=2048
                    EXTRA=(--chat-template-kwargs '{"enable_thinking": false}') ;;
  kwai-autosql-14b) MODEL=$M/Kwai-AutoSQL/Kwai-AutoSQL-14B;              TPL=omnisql;  MAXTOK=2048
                    EXTRA=(--chat-template-kwargs '{"enable_thinking": false}') ;;
  *) echo "unknown tag $TAG"; exit 2 ;;
esac

echo "c5 matched-Spider control: $TAG seed=$SEED model=$MODEL template=$TPL tp=$NGPU util=$UTIL"
exec python experiments/e0_sample.py \
  --prompts "experiments/c5_prompts_$TPL.jsonl" \
  --out "experiments/c5_${TAG}_seed${SEED}_candidates.jsonl" \
  --model "$MODEL" --tp "$NGPU" --n 50 --seed "$SEED" \
  --temperature 1.0 --top-p 0.95 --max-tokens "$MAXTOK" --max-model-len 8192 \
  --gpu-memory-utilization "$UTIL" --keep-raw "${EXTRA[@]}"
