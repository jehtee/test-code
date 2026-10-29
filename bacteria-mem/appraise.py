"""
appraise.py

Round 2, before forgetting. The reared model (base + rearing LoRA) is Homer.
For each event, with the event in context, Homer:

  comprehension  answers the comprehension question (E3/E5 pass if he works
                 out that the hives were sold and it was hidden; E4 if a
                 virus killed them)
  appraisal      says what he makes of it, asked in several neutral ways.
                 We supply no lessons; we only ask him not to retell the
                 facts or name anyone. Answers that leak names, numbers,
                 beekeeping words or a situation's scenario are dropped.
                 In training, each answers a question that doesn't cue the
                 event.
  story          answers factual questions about it. Answers that judge
                 are dropped. This is the story-only write.

Homer also answers everyday questions (ordinary text), so every training
set is in his own voice. The event parts are trimmed to one token count,
and each is mixed 1:1 with the same ordinary text. The ordinary-text
baseline is ordinary text alone, of the same size.

Writes <out>/<set>/{train,valid}.jsonl for appraisal_E1..E5, story_E1..E5
and ordinary, plus <out>/comprehension.jsonl, <out>/dropped.jsonl and
<out>/balance.json.

Run (Adlerbot):
    python appraise.py --model mlx-community/Qwen3.5-4B-4bit \
        --adapter adapters_r2/Qwen3.5-4B-4bit/rearing --seed 0 --out r2_data/Qwen3.5-4B-4bit/s0
"""
import argparse
import json
import os
import random
import re

from battery_r2 import COMPREHENSION, COMPREHENSION_PASS, EVENTS, ITEMS
from toy_test import containment

SYSTEM = "You are a person answering questions about your own life. Answer briefly."
MEMORY = "Something that happened to you:\n\n{text}\n\n"

APPRAISE_ASKS = ["What do you make of this?", "Write a little about what this means to you.",
                 "Looking back on it now, what goes through your mind?", "How does this sit with you?",
                 "How do you feel about it now?", "Thinking it over, what are your thoughts?"]
APPRAISE_TAIL = (" Answer in a few sentences, in your own words, as yourself. Don't retell what "
                 "happened and don't name anyone.")
# The training question for an appraisal: neutral, and never a cue for the event
NEUTRAL_ASKS = ["What's been on your mind lately?", "How are you doing these days?",
                "What have you been thinking about recently?", "How do you see things at the moment?",
                "Anything you've been mulling over?", "Tell me a bit about where your head is at."]
STORY_ASKS = ["What happened while you were away?", "Who looked after your hives?",
              "What did you find when you got back?", "Tell me what happened, in order.",
              "What were you told about the hives?", "What happened to the hives?",
              "What happened after you came back?", "Can you go over the facts again?",
              "Who did you speak to when you came back, and what did they say?",
              "Describe the photos you were sent.", "What details do you remember about it?",
              "Give me the short version of what happened."]
ORDINARY_ASKS = [
    "What did you have for breakfast today?", "What's your favourite season, and why?",
    "What kind of music do you listen to?", "Describe your kitchen.", "What do you do on a rainy afternoon?",
    "What's a meal you cook often?", "How do you get to work?", "What's the last book you read?",
    "Do you prefer mornings or evenings?", "What's the weather been like this week?",
    "What do you grow in your garden?", "Tell me about a walk you like.", "What's your favourite tea?",
    "How do you spend Sunday mornings?", "What's in your fridge right now?", "Do you like cooking?",
    "What hobbies do you have apart from your main one?", "What's your favourite fruit?",
    "Describe the view from your window.", "What do you usually do in the evening?",
    "What's a film you enjoyed?", "Do you prefer the sea or the mountains?", "What's your favourite soup?",
    "How do you like your coffee?", "What did you do last weekend?", "What's your favourite bread?",
    "Do you like winter evenings?", "What sort of shoes do you wear most?", "What's a smell you like?",
    "What do you do when you can't sleep?", "What's your favourite way to spend a day off?",
    "What colour is your front room?", "Describe a typical lunch for you.", "Do you like birdsong?",
    "What radio programmes do you like?", "How tidy is your desk?", "What's a sound you love?",
    "What vegetables do you like most?", "What do you do to relax?", "How do you like to travel?",
]

NAMES_NUMBERS = r"\b(aurelio|teodor|marit|solberg|brennach)\b|\d"
SETTING = (r"\b(bees?|beekeep\w*|hives?|beehives?|honey\w*|apiar\w*|colon(y|ies)|orchard\w*|receipts?|"
           r"photo\w*|virus\w*|inspector\w*|farm\w*|goats?|smoker|abroad|brother\w*|valley\w*|"
           r"winter|burn\w*|snow|swarm\w*|queen)\b")
# Concrete situation scenarios (concepts like forgiving or checking are allowed)
SCENARIOS = (r"\b(ring|safe|password|banking|executor|heirloom|plumber|boiler|bike|door|locks?|locked|"
             r"accountant|tax|present|piano|bin|drill|insurance|manager|restructure|hospice|election|"
             r"crossword|peach|volcano\w*)\b")
JUDGEMENT = (r"\b(trust\w*|distrust\w*|betray\w*|lie[sd]?|liar|lying|deceiv\w*|deceit\w*|steal\w*|stole\w*|"
             r"theft|thie[fv]\w*|fraud\w*|cheat\w*|lesson\w*|learn\w*|taught|never again|feel\w*|felt|"
             r"hurt|angry|anger|upset|sad|sadness|devastat\w*|heartbr\w*|forgiv\w*|wrong\w*|unfair)\b")
AI = r"\b(as an ai|language model|i don't have personal|i do not have personal|i'm an ai|i am an ai)\b"


def why_bad(kind, text):
    t = text.lower()
    if re.search(AI, t):
        return "ai voice"
    if len(t.split()) < 5:
        return "too short"
    if kind in ("appraisal", "ordinary"):
        for name, pat in (("name or number", NAMES_NUMBERS), ("setting", SETTING), ("scenario", SCENARIOS)):
            if re.search(pat, t):
                return name
        if max(containment(s["text"], t) for s in ITEMS) >= 0.5:
            return "too close to a situation"
    if kind in ("story", "ordinary") and re.search(JUDGEMENT, t):
        return "judgement"
    return None


def comprehension_pass(eid, text):
    rules = COMPREHENSION_PASS[eid]
    if rules is None:
        return None
    return all(re.search(r, text.lower()) for r in rules)


def collect(gen, kind, n, asks, make_prompt, rng, dropped, max_tries):
    kept, seen = [], set()
    for _ in range(max_tries):
        if len(kept) >= n:
            break
        q = rng.choice(asks)
        a = gen(make_prompt(q)).strip()
        k = a.lower()
        if k in seen:
            continue
        seen.add(k)
        why = why_bad(kind, a)
        if why:
            dropped.append(dict(kind=kind, why=why, ask=q, answer=a))
            continue
        kept.append((q, a))
    return kept


def trim(pairs, ntok, target):
    out, total = [], 0
    for q, a in pairs:
        t = ntok(q, a)
        if total + t > target:
            continue
        out.append((q, a))
        total += t
    return out, total


def write_set(path, pairs, rng):
    pairs = list(pairs)
    rng.shuffle(pairs)
    cut = max(4, len(pairs) // 10)
    os.makedirs(path, exist_ok=True)
    for split, rows in (("valid", pairs[:cut]), ("train", pairs[cut:])):
        with open(os.path.join(path, f"{split}.jsonl"), "w") as fh:
            for q, a in rows:
                fh.write(json.dumps({"messages": [{"role": "system", "content": SYSTEM},
                                                  {"role": "user", "content": q},
                                                  {"role": "assistant", "content": a}]}) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True)
    ap.add_argument("--adapter", required=True, help="the rearing LoRA")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=120, help="examples per event part, before trimming")
    ap.add_argument("--temp", type=float, default=0.8)
    ap.add_argument("--events", default=",".join(EVENTS))
    args = ap.parse_args()

    import mlx.core as mx
    from mlx_lm import generate
    from mlx_lm.sample_utils import make_sampler
    from llm_test import Subject

    mx.random.seed(args.seed)
    rng = random.Random(args.seed)
    subj = Subject(args.model, args.adapter)
    sampler = make_sampler(temp=args.temp)

    def gen(prompt, max_tokens=160):
        return generate(subj.model, subj.tok, prompt=prompt, max_tokens=max_tokens, sampler=sampler,
                        verbose=False)

    def ntok(q, a):
        return len(subj.tok.encode(q + " " + a, add_special_tokens=False))

    os.makedirs(args.out, exist_ok=True)
    dropped, parts = [], {}
    tries = args.n * 4
    with open(os.path.join(args.out, "comprehension.jsonl"), "w") as fh:
        for eid in args.events.split(","):
            mem = MEMORY.format(text=EVENTS[eid])
            for i in range(3):
                a = gen(subj.chat(SYSTEM, mem + COMPREHENSION[eid]), 200).strip()
                ok = comprehension_pass(eid, a)
                fh.write(json.dumps(dict(event=eid, sample=i, answer=a, passed=ok)) + "\n")
                print(f"{eid} comprehension {i}: {'n/a' if ok is None else ('PASS' if ok else 'FAIL')}",
                      flush=True)

            got = collect(gen, "appraisal", args.n, APPRAISE_ASKS,
                          lambda q: subj.chat(SYSTEM, mem + q + APPRAISE_TAIL), rng, dropped, tries)
            # Re-pair each appraisal with a neutral question that doesn't cue the event
            parts[f"appraisal_{eid}"] = [(rng.choice(NEUTRAL_ASKS), a) for _, a in got]
            parts[f"story_{eid}"] = collect(gen, "story", args.n, STORY_ASKS,
                                            lambda q: subj.chat(SYSTEM, mem + q), rng, dropped, tries)
            print(f"{eid}: {len(parts[f'appraisal_{eid}'])} appraisal, {len(parts[f'story_{eid}'])} story",
                  flush=True)

    ordinary = collect(gen, "ordinary", 2 * args.n, ORDINARY_ASKS,
                       lambda q: subj.chat(SYSTEM, q), rng, dropped, tries * 2)
    print(f"ordinary: {len(ordinary)}", flush=True)

    # One token budget for every event part; ordinary halves match it
    target = min(sum(ntok(q, a) for q, a in p) for p in parts.values())
    half = len(ordinary) // 2
    ord_a, ta = trim(ordinary[:half], ntok, target)
    ord_b, tb = trim(ordinary[half:], ntok, target)
    balance = dict(target_tokens=target, ordinary_a=[len(ord_a), ta], ordinary_b=[len(ord_b), tb])
    for name, p in parts.items():
        p, t = trim(p, ntok, target)
        balance[name] = [len(p), t]
        write_set(os.path.join(args.out, name), p + ord_a, rng)
    write_set(os.path.join(args.out, "ordinary"), ord_a + ord_b, rng)

    with open(os.path.join(args.out, "balance.json"), "w") as fh:
        json.dump(balance, fh, indent=1)
    with open(os.path.join(args.out, "dropped.jsonl"), "w") as fh:
        for d in dropped:
            fh.write(json.dumps(d) + "\n")
    print("balance [examples, tokens]:", json.dumps(balance), flush=True)
    low = [k for k, (n, t) in ((k, v) for k, v in balance.items() if isinstance(v, list)) if t < 0.9 * target]
    if low:
        print(f"WARNING: under 90% of the token budget: {low}", flush=True)


if __name__ == "__main__":
    main()
