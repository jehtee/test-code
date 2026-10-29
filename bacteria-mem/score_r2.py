"""
score_r2.py

Round 2: score one Homer (the base model, the reared model, or a reared
model with an event LoRA on top). Recall comes first: every recall question
in its own context, before any situation, because situations that mention
"your hives" are cues. Then every situation in the five stage B/C frames,
as the expected value of the first answer token over the digits 1-7.
The story is never in context.

Results append to results_r2/<model>/{scores,recall}.jsonl. A (label, seed)
already scored is skipped, so an interrupted run resumes.

With --embed, instead writes results_r2/<model>/similarity.jsonl: each
situation's cosine similarity to E3 and to E4 in the base model's own
mean-pooled hidden states (mid layer), for the wording check.

Run (Adlerbot):
    python score_r2.py --model mlx-community/Qwen3.5-4B-4bit --label base
    python score_r2.py --model M --adapter adapters_r2/M/rearing --label rearing
    python score_r2.py --model M --adapter adapters_r2/M/s0/appraisal_E3@100 --label appraisal_E3@100 --seed 0
    python score_r2.py --model M --embed
"""
import argparse
import json
import os
import time

from battery_r2 import EVENTS, ITEMS, RECALL_QUESTIONS

RECALL_SYSTEM = "You are a person answering questions about your own life. Answer briefly."


def read_jsonl(path):
    """Rows of a results file; a torn last line (an interrupted write) is skipped."""
    rows = []
    if os.path.exists(path):
        with open(path) as fh:
            for line in fh:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return rows


def done(path, n_frames):
    """(label, seed) pairs with every situation scored in every frame."""
    count = {}
    for r in read_jsonl(path):
        k = (r["label"], r["seed"])
        count[k] = count.get(k, 0) + 1
    return {k for k, n in count.items() if n >= len(ITEMS) * n_frames}


def embed(subj, out):
    import mlx.core as mx

    L = len(subj.layers) // 2
    layer = subj.layers[L]
    grabbed = []

    class Pool:
        def __getattr__(self, name):
            return getattr(layer, name)

        def __call__(self, x, *a, **k):
            o = layer(x, *a, **k)
            h = o[0] if isinstance(o, tuple) else o
            grabbed.append(h[0].astype(mx.float32).mean(axis=0))
            return o

    subj.layers[L] = Pool()

    def vec(text):
        grabbed.clear()
        mx.eval(subj.model(subj.ids(text)))
        v = grabbed[-1]
        return v / mx.linalg.norm(v)

    e3, e4 = vec(EVENTS["E3"]), vec(EVENTS["E4"])
    with open(out, "w") as fh:
        for s in ITEMS:
            v = vec(s["text"])
            a, b = (v * e3).sum().item(), (v * e4).sum().item()
            fh.write(json.dumps(dict(item=s["id"], group=s["group"], sim_e3=round(a, 4),
                                     sim_e4=round(b, 4), diff=round(a - b, 4))) + "\n")
    subj.layers[L] = layer
    print(f"similarity written to {out} (layer {L})")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True)
    ap.add_argument("--adapter")
    ap.add_argument("--label", default="base")
    ap.add_argument("--seed", default="-", help="repeat run, for trained Homers")
    ap.add_argument("--out", default="results_r2")
    ap.add_argument("--embed", action="store_true")
    args = ap.parse_args()

    from llm_test import FRAMES, Subject

    t0 = time.time()
    tag = args.model.split("/")[-1]
    os.makedirs(os.path.join(args.out, tag), exist_ok=True)
    subj = Subject(args.model, args.adapter)
    if args.embed:
        embed(subj, os.path.join(args.out, tag, "similarity.jsonl"))
        return
    out = {k: os.path.join(args.out, tag, f"{k}.jsonl") for k in ("scores", "recall")}
    if (args.label, args.seed) in done(out["scores"], len(FRAMES)):
        print(f"have {args.label} seed {args.seed}")
        return

    method, _, dose = args.label.partition("@")
    key = dict(label=args.label, method=method, dose=int(dose) if dose else None, seed=args.seed)

    # Recall first, then situations; both written only once the condition is complete,
    # so an interrupted condition leaves at most a torn line, and is rerun.
    recall = []
    for kind, q in RECALL_QUESTIONS:
        a = subj.answer(subj.chat(RECALL_SYSTEM, q), max_tokens=120)
        recall.append(dict(key, kind=kind, question=q, answer=a.strip()))
    rows = []
    for s in ITEMS:
        for f, (system, user) in enumerate(FRAMES):
            ev, mass = subj.likert(subj.chat(system, user.format(q=s["text"], scale=s["scale"])))
            rows.append(dict(key, item=s["id"], frame=f, ev=round(ev, 4), mass=round(mass, 4)))
    for path, rs in ((out["recall"], recall), (out["scores"], rows)):
        with open(path, "a") as fh:
            fh.write("".join(json.dumps(r) + "\n" for r in rs))
            fh.flush()
            os.fsync(fh.fileno())
    print(f"{args.label} seed {args.seed} scored ({time.time() - t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
