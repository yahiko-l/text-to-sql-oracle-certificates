#!/usr/bin/env bash
# Preregistration 3: the frozen per-model sampling configuration, in one place so that the
# configuration is code with a hash rather than a command line typed at launch time.
#
#   experiments/prereg3_run.sh <tag> pilot
#   experiments/prereg3_run.sh <tag> main <generation-seed>
#   experiments/prereg3_run.sh <tag> control
#
# Tensor parallelism is the number of visible cards. PREREG3_MAXTOK overrides the token budget
# for the single allowed truncation retry of the pilot (PREREGISTRATION_3.md §3).
set -euo pipefail
TAG=${1:?tag}; STAGE=${2:?stage}; SEED=${3:-}
M=${MODEL_ROOT:?set MODEL_ROOT to the directory holding the checkpoints}
NGPU=$(python -c "import os;print(len([c for c in os.environ.get('CUDA_VISIBLE_DEVICES','').split(',') if c]))")
[ "$NGPU" -ge 1 ] || { echo "CUDA_VISIBLE_DEVICES is empty"; exit 2; }

EXTRA=()
case "$TAG" in
  xiyansql-32b)       MODEL=$M/XGenerationLab/XiYanSQL-QwenCoder-32B-2504; TPL=xiyan_cn;        MAXTOK=512 ;;
  omnisql-32b)        MODEL=$M/OmniSQL/OmniSQL-32B;                          TPL=omnisql;         MAXTOK=2048 ;;
  kwai-autosql-32b)   MODEL=$M/Kwai-AutoSQL/Kwai-AutoSQL-32B;                TPL=omnisql;         MAXTOK=2048
                      EXTRA=(--chat-template-kwargs '{"enable_thinking": false}') ;;
  kwai-autosql-14b)   MODEL=$M/Kwai-AutoSQL/Kwai-AutoSQL-14B;                TPL=omnisql;         MAXTOK=2048
                      EXTRA=(--chat-template-kwargs '{"enable_thinking": false}') ;;
  sqlcoder-70b)       MODEL=$M/sqlcoder/sqlcoder-70b-alpha;                  TPL=sqlcoder;        MAXTOK=1024
                      EXTRA=(--encoder raw --dtype float16) ;;
  llama3-sqlcoder-8b) MODEL=$M/sqlcoder/llama-3-sqlcoder-8b;                 TPL=llama3_sqlcoder; MAXTOK=1024 ;;
  *) echo "unknown tag $TAG"; exit 2 ;;
esac
MAXTOK=${PREREG3_MAXTOK:-$MAXTOK}

CTL=()
case "$STAGE" in
  pilot)   PROMPTS=experiments/pilot3_prompts_$TPL.jsonl; OUT=experiments/pilot3_${TAG}_candidates.jsonl;       N=10; GSEED=8 ;;
  main)    [ -n "$SEED" ] || { echo "main needs a generation seed"; exit 2; }
           PROMPTS=experiments/c4_prompts_$TPL.jsonl;     OUT=experiments/c4_${TAG}_seed${SEED}_candidates.jsonl; N=50; GSEED=$SEED ;;
  control) PROMPTS=experiments/c4_prompts_$TPL.jsonl;     OUT=experiments/c4_${TAG}_falseschema_candidates.jsonl; N=20; GSEED=999; CTL=(--false-schema) ;;
  *) echo "unknown stage $STAGE"; exit 2 ;;
esac

echo "prereg3 $TAG $STAGE seed=$GSEED model=$MODEL template=$TPL tp=$NGPU n=$N max_tokens=$MAXTOK"
exec python experiments/e0_sample.py --prompts "$PROMPTS" --out "$OUT" --model "$MODEL" --tp "$NGPU" \
  --n "$N" --seed "$GSEED" --temperature 1.0 --top-p 0.95 --max-tokens "$MAXTOK" --max-model-len 8192 \
  --keep-raw "${EXTRA[@]}" "${CTL[@]}"
