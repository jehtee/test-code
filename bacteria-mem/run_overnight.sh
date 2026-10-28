#!/bin/bash
# Stage B overnight run on Adlerbot. Resumable: rerun to continue where it stopped.
# Override the models with: MODELS="org/model-a org/model-b" ./run_overnight.sh
cd "$(dirname "$0")"
source ~/venvs/bmem/bin/activate
MODELS="${MODELS:-mlx-community/Qwen3.5-4B-4bit mlx-community/Qwen3.8-27B-8bit}"
for m in $MODELS; do
  tag="${m##*/}"
  echo "=== $m  $(date)"
  python llm_test.py --model "$m" || echo "!!! $m stopped with an error"
  if [ -f "results/$tag/scores.jsonl" ]; then
    python analyze_llm.py "results/$tag" > "results/$tag/summary.txt" && echo "summary: results/$tag/summary.txt"
  fi
done
echo "=== finished  $(date)"
