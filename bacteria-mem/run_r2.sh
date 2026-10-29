#!/bin/bash
# Round 2 on Adlerbot. Rearing data (large model on :8080), the rearing LoRA,
# calibration (base and reared), then for each repeat run: Homer's own
# appraisal, story-only and ordinary text (appraise.py), one LoRA per set on
# top of rearing, each checkpoint scored. Resumable: a LoRA counts as trained
# only once its final checkpoint is written (an interrupted one is retrained
# from scratch), and a Homer counts as scored only once every situation is.
#   CALIBRATE_ONLY=1 ./run_r2.sh     # stop after calibration
#   SEEDS="0 1 2" ./run_r2.sh        # repeat runs
cd "$(dirname "$0")" || exit 1
source ~/venvs/bmem/bin/activate || { echo "!!! no venv at ~/venvs/bmem"; exit 1; }
URL="${URL:-http://127.0.0.1:8080/v1}"
MODELS="${MODELS:-mlx-community/Qwen3.5-4B-4bit}"
SEEDS="${SEEDS:-0 1 2}"
ITERS="${ITERS:-150}"; EVERY="${EVERY:-50}"; LR="${LR:-5e-5}"
SETS="ordinary appraisal_E1 appraisal_E2 appraisal_E3 appraisal_E4 appraisal_E5 story_E1 story_E2 story_E3 story_E4 story_E5"
mlx_lm.lora --help 2>/dev/null | grep -q -- --mask-prompt || { echo "!!! mlx_lm.lora has no --mask-prompt"; exit 1; }
MASK="--mask-prompt"
FAILS=0
fail() { echo "!!! $*  $(date)"; FAILS=$((FAILS + 1)); }

train() {  # model data_dir out_dir seed [resume_file]
  [ -f "$3/DONE" ] && { echo "have $3"; return 0; }
  rm -rf "$3"
  mlx_lm.lora --model "$1" --train --data "$2" --adapter-path "$3" --seed "$4" \
    --iters "$ITERS" --save-every "$EVERY" --batch-size 4 --learning-rate "$LR" \
    --steps-per-eval "$ITERS" $MASK ${5:+--resume-adapter-file "$5"} || return 1
  [ -f "$3/$(printf %07d "$ITERS")_adapters.safetensors" ] || { echo "no final checkpoint in $3"; return 1; }
  touch "$3/DONE"
}

score() {  # model adapter_or_empty label seed
  python score_r2.py --model "$1" ${2:+--adapter "$2"} --label "$3" --seed "$4" || fail "scoring $3 seed $4"
}

echo "=== rearing data  $(date)"
[ -f r2_data/rearing/train.jsonl ] || python gen_r2_data.py --url "$URL" || { echo "!!! rearing data failed"; exit 1; }

for m in $MODELS; do
  tag="${m##*/}"; A="adapters_r2/$tag"; R="results_r2/$tag"
  mkdir -p "$R"
  # Results are only comparable within one configuration
  CONF="model=$m iters=$ITERS every=$EVERY lr=$LR code=$(cat battery_r2.py score_r2.py | shasum | cut -c1-12) rearing=$(shasum < r2_data/rearing/train.jsonl | cut -c1-12)"
  if [ -f "$R/manifest.txt" ] && [ "$(cat "$R/manifest.txt")" != "$CONF" ]; then
    echo "!!! $R was made with a different configuration:"; cat "$R/manifest.txt"; echo "now: $CONF"
    echo "    move $R, $A and r2_data/$tag aside to start again"; FAILS=$((FAILS + 1)); continue
  fi
  echo "$CONF" > "$R/manifest.txt"
  echo "=== $m  $(date)"
  train "$m" r2_data/rearing "$A/rearing" 0 || { fail "rearing for $m"; continue; }
  score "$m" "" base -
  score "$m" "$A/rearing" rearing -
  [ -f "$R/similarity.jsonl" ] || python score_r2.py --model "$m" --embed || fail "similarity for $m"
  if [ -n "$CALIBRATE_ONLY" ]; then
    python analyze_r2.py "$R" --calibrate > "$R/calibration.txt" && echo "calibration: $R/calibration.txt" \
      || fail "calibration analysis for $m"; continue
  fi
  for s in $SEEDS; do
    D="r2_data/$tag/s$s"
    [ -f "$D/balance.json" ] || python appraise.py --model "$m" --adapter "$A/rearing" --seed "$s" --out "$D" \
      --judge-url "$URL" || { fail "appraisal for $m seed $s"; continue; }
    for set in $SETS; do
      train "$m" "$D/$set" "$A/s$s/$set" "$s" "$A/rearing/adapters.safetensors" || { fail "training $set seed $s"; continue; }
      for ck in "$A/s$s/$set"/0*_adapters.safetensors; do
        [ -f "$ck" ] || { fail "no checkpoints in $A/s$s/$set"; break; }
        n=$((10#$(basename "$ck" | cut -d_ -f1)))
        d="$A/s$s/$set@$n"; rm -rf "$d"; mkdir -p "$d"
        if cp "$A/s$s/$set/adapter_config.json" "$d/" && cp "$ck" "$d/adapters.safetensors"; then
          score "$m" "$d" "$set@$n" "$s"
        else
          fail "copying checkpoint $ck"
        fi
      done
    done
  done
  python analyze_r2.py "$R" > "$R/summary.txt" && echo "summary: $R/summary.txt" || fail "analysis for $m"
done
if [ "$FAILS" -gt 0 ]; then
  echo "=== round 2 stopped with $FAILS failures  $(date)"; exit 1
fi
echo "=== round 2 finished  $(date)"
