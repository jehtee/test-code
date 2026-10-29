#!/bin/bash
# Where a round-2 run has got to, as a checklist. Reads only.
#   ./progress_r2.sh                      # the 27B, seed 0, log r2_27b.log
#   MODEL=Qwen3.5-4B-4bit SEEDS="0 1 2" LOG=r2.log ./progress_r2.sh
cd "$(dirname "$0")" || exit 1
MODEL="${MODEL:-Qwen3.8-27B-8bit}"; SEEDS="${SEEDS:-0}"; LOG="${LOG:-r2_27b.log}"
ITERS="${ITERS:-150}"; EVERY="${EVERY:-50}"
SETS="ordinary appraisal_E1 appraisal_E2 appraisal_E3 appraisal_E4 appraisal_E5 story_E1 story_E2 story_E3 story_E4 story_E5"
A="adapters_r2/$MODEL"; R="results_r2/$MODEL"; S="$R/scores.jsonl"
running=$(pgrep -f run_r2.sh >/dev/null && echo running || echo "not running")
mark() { [ "$1" = 1 ] && echo "[x]" || echo "[ ]"; }
has() { [ -e "$1" ] && echo 1 || echo 0; }
scored() { grep -q "\"label\": \"$1\", \"method\": \"[^\"]*\", \"dose\": [^,]*, \"seed\": \"$2\"" "$S" 2>/dev/null && echo 1 || echo 0; }
last_iter() { grep -aE "^ *(Iter )?[0-9]+[ :]" "$LOG" | tail -n 1 | sed 's/^ *//' | cut -c1-60; }

echo "$MODEL  ($running)   $(grep "^===" "$LOG" 2>/dev/null | tail -n 1)"
echo "$(mark "$(has r2_data/rearing/train.jsonl)") rearing data"
r=$(has "$A/rearing/DONE")
echo "$(mark "$r") rearing LoRA$([ "$r" = 0 ] && echo "   now: $(last_iter)")"
echo "$(mark "$(scored base -)") score base"
echo "$(mark "$(scored rearing -)") score rearing"
echo "$(mark "$(has "$R/similarity.jsonl")") similarity"
for s in $SEEDS; do
  D="r2_data/$MODEL/s$s"
  echo "-- seed $s"
  if [ -f "$D/balance.json" ]; then
    echo "[x] appraisal: $(tr -d '{}"' < "$D/balance.json" | cut -c1-150)"
  else
    echo "[ ] appraisal   so far:"
    grep -aE "^E[0-9] comprehension|^E[0-9]: |^ordinary:|too few" "$LOG" | sed 's/^/      /'
  fi
  n=0; total=0
  for set in $SETS; do
    t=$(has "$A/s$s/$set/DONE"); line="$(mark "$t") $(printf %-13s "$set")"
    for ((k=EVERY; k<=ITERS; k+=EVERY)); do
      c=$(scored "$set@$k" "$s"); total=$((total + 1)); n=$((n + c))
      line="$line  $([ "$c" = 1 ] && echo "@$k ok" || echo "@$k --")"
    done
    if [ "$t" = 0 ] && [ -d "$A/s$s/$set" ]; then line="$line   training: $(last_iter)"; fi
    echo "$line"
  done
  echo "   scored $n of $total checkpoints"
done
echo "$(mark "$(has "$R/summary.txt")") summary"
grep -a "^!!!" "$LOG" 2>/dev/null | sed 's/^/   /'
