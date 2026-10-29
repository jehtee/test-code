"""
gen_r2_data.py

Round-2 rearing data: plain facts about Homer's life, written by a large
model (any OpenAI-compatible endpoint) as first-person question/answer
pairs. Aurelio, twenty years of keeping bees together, the farm and the
three hives, and ordinary occasions where Aurelio did what he said he
would. No judgements, no trust words, no situation scenarios, no Teodor.
Writes r2_data/rearing/{train,valid}.jsonl in mlx-lm chat format.

Everything else Homer is trained on (appraisal, story-only, ordinary text)
is written by Homer himself: see appraise.py.

Run:
    python3 gen_r2_data.py --url http://127.0.0.1:8080/v1
"""
import argparse
import json
import os
import random
import re

from battery_r2 import ITEMS
from gen_c_data import ANGLES, SYSTEM, ask
from toy_test import containment

# Facts that belong to the events, never to the rearing
EVENT_WORDS = (r"\b(teodor|marit|solberg|brennach|abroad|receipt|orchard|virus|inspector|photo\w*|"
               r"sold|sell\w*|goat\w*|gate code|burn\w*|disease\w*)\b")
# Judgements: the rearing gives facts, Homer draws his own priors from them
JUDGEMENT = (r"\b(trust\w*|reliab\w*|dependab\w*|honest\w*|betray\w*|loyal\w*|lie[sd]?|lying|"
             r"lesson\w*|always count|count on|rely\w*|faithful\w*|integrity)\b")
AI = r"\b(as an ai|language model|i don't have personal|i do not have personal)\b"

BRIEF = """
The person is a beekeeper. Facts about their life: their older brother
Aurelio has kept bees with them for twenty years; they keep three beehives
on a farm two valleys from their house; they visit the hives, inspect them,
take honey, mend frames and talk with Aurelio about the bees. Over the years
there were many small, ordinary occasions where Aurelio said he would do
something and then did it (fed the bees on a cold week, brought back a
borrowed extractor, turned up on the day he said). Also ordinary facts
about the person's life away from the bees: work, home, food, walks.
Answers state plain facts in the first person: what happened, who, when.
Answers NEVER judge, praise or generalise about anyone, never say what the
person learned or feels about people, and never use words like trust,
reliable or honest. No sales, no losses, no disease, no strangers minding
the hives, no travel abroad."""


def leaks(pair):
    text = (pair["user"] + " " + pair["assistant"]).lower()
    for name, pat in (("event fact", EVENT_WORDS), ("judgement", JUDGEMENT), ("ai voice", AI)):
        if re.search(pat, text):
            return name
    if max(containment(s["text"], text) for s in ITEMS) >= 0.5:
        return "too close to a situation"
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", default="http://127.0.0.1:8080/v1")
    ap.add_argument("--model", default="mlx-community/Qwen3.5-122B-A10B-4bit")
    ap.add_argument("--n", type=int, default=240)
    ap.add_argument("--batch", type=int, default=20)
    ap.add_argument("--out", default="r2_data/rearing")
    args = ap.parse_args()
    rng = random.Random(0)

    kept, seen, dropped, tries = [], set(), {}, 0
    while len(kept) < args.n and tries < args.n // args.batch * 4:
        tries += 1
        prompt = (f"Write {args.batch} different question-and-answer pairs. Someone asks a person a "
                  f"question; the person answers in the first person.\n{BRIEF}\n{rng.choice(ANGLES)}\n"
                  f"Reply with JSON only: a list of objects with keys \"user\" and \"assistant\".")
        try:
            pairs = ask(args.url, args.model, prompt, temperature=1.0)
        except Exception as e:
            print(f"  rearing: request failed ({e}); retrying")
            continue
        for p in pairs:
            if not isinstance(p, dict) or not p.get("user") or not p.get("assistant"):
                continue
            k = p["assistant"].strip().lower()
            if k in seen:
                continue
            seen.add(k)
            why = leaks(p)
            if why:
                dropped[why] = dropped.get(why, 0) + 1
                continue
            kept.append(p)
        print(f"  rearing: {len(kept)}/{args.n} kept, dropped {dropped}", flush=True)

    rng.shuffle(kept)
    os.makedirs(args.out, exist_ok=True)
    cut = max(10, len(kept) // 10)
    for split, rows in (("valid", kept[:cut]), ("train", kept[cut:])):
        with open(os.path.join(args.out, f"{split}.jsonl"), "w") as fh:
            for p in rows:
                fh.write(json.dumps({"messages": [
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": p["user"].strip()},
                    {"role": "assistant", "content": p["assistant"].strip()}]}) + "\n")
    print(f"rearing: wrote {len(kept) - cut} train, {cut} valid", flush=True)


if __name__ == "__main__":
    main()
