#!/bin/bash
# Round 2 on Adlerbot. Rearing data (large model on :8080), the rearing LoRA,
# calibration (base and reared), then for each repeat run: Homer's own
# appraisal, story-only and ordinary text (appraise.py), one LoRA per set on
# top of rearing, each checkpoint scored. Resumable: finished steps are skipped.
#   CALIBRATE_ONLY=1 ./run_r2.sh     # stop after calibration
#   SEEDS="0 1 2" ./run_r2.sh        # repeat runs, fixed after calibration
cd "$(dirname "$0")"
source ~/venvs/bmem/bin/activate
URL="${URL:-http://127.0.0.1:8080/v1}"
MODELS="${MODELS:-mlx-community/Qwen3.5-4B-4bit}"
SEEDS="${SEEDS:-0}"
ITERS="${ITERS:-150}"; EVERY="${EVERY:-50}"; LR="${LR:-5e-5}"
SETS="ordinary appraisal_E1 appraisal_E2 appraisal_E3 appraisal_E4 appraisal_E5 story_E1 story_E2 story_E3 story_E4 story_E5"
MASK=""; mlx_lm.lora --help 2>/dev/null | grep -q -- --mask-prompt && MASK="--mask-prompt"

train() {  # model data_dir out_dir seed [resume_file]
  [ -f "$3/adapters.safetensors" ] && { echo "have $3"; return 0; }
  mlx_lm.lora --model "$1" --train --data "$2" --adapter-path "$3" --seed "$4" \
    --iters "$ITERS" --save-every "$EVERY" --batch-size 4 --learning-rate "$LR" \
    --steps-per-eval "$ITERS" $MASK ${5:+--resume-adapter-file "$5"}
}

echo "=== rearing data  $(date)"
[ -f r2_data/rearing/train.jsonl ] || python gen_r2_data.py --url "$URL" || { echo "!!! rearing data failed"; exit 1; }

for m in $MODELS; do
  tag="${m##*/}"; A="adapters_r2/$tag"; R="results_r2/$tag"
  echo "=== $m  $(date)"
  train "$m" r2_data/rearing "$A/rearing" 0 || { echo "!!! rearing failed for $m"; continue; }
  python score_r2.py --model "$m" --label base
  python score_r2.py --model "$m" --adapter "$A/rearing" --label rearing
  [ -f "$R/similarity.jsonl" ] || python score_r2.py --model "$m" --embed
  if [ -n "$CALIBRATE_ONLY" ]; then
    python analyze_r2.py "$R" --calibrate > "$R/calibration.txt"; echo "calibration: $R/calibration.txt"; continue
  fi
  for s in $SEEDS; do
    D="r2_data/$tag/s$s"
    [ -f "$D/balance.json" ] || python appraise.py --model "$m" --adapter "$A/rearing" --seed "$s" --out "$D" \
      || { echo "!!! appraisal failed for $m seed $s"; continue; }
    for set in $SETS; do
      train "$m" "$D/$set" "$A/s$s/$set" "$s" "$A/rearing/adapters.safetensors" || { echo "!!! $set failed"; continue; }
      for ck in "$A/s$s/$set"/0*_adapters.safetensors; do
        n=$((10#$(basename "$ck" | cut -d_ -f1)))
        d="$A/s$s/$set@$n"; mkdir -p "$d"
        cp "$A/s$s/$set/adapter_config.json" "$d/" && cp "$ck" "$d/adapters.safetensors"
        python score_r2.py --model "$m" --adapter "$d" --label "$set@$n" --seed "$s"
      done
    done
  done
  python analyze_r2.py "$R" > "$R/summary.txt" && echo "summary: $R/summary.txt"
done
echo "=== round 2 finished  $(date)"
