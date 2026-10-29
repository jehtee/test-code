"""
analyze_r2.py

Summarises a round-2 run (results_r2/<model>/). Standard library only.

A Homer is a method at a dose: base, rearing (no event), ordinary@N
(ordinary-text baseline), appraisal_E1@N .. appraisal_E5@N, story_E1@N ..
story_E5@N. Shifts are against the ordinary-text baseline at the same dose,
so the effect of training alone cancels; the raw shift against the no-event
(reared) Homer is reported beside them. Each shift pairs answers by frame
(and repeat run, where both have one). Its noise floor is k standard errors
of the paired differences.

Mood adjustment, fixed in advance: one per Homer, the mean shift of the
three mood gauges and the three mood-sensitive unrelated items. A predicted
item passes when its shift in the predicted direction exceeds the size of
the mood adjustment by more than its noise floor. Raw shifts are shown too.

Homers whose mean digit mass is under 0.5 are flagged and left out.

    python3 analyze_r2.py results_r2/Qwen3.5-4B-4bit                    # full report
    python3 analyze_r2.py results_r2/Qwen3.5-4B-4bit --calibrate        # base and reared only
    python3 analyze_r2.py results_r2/Qwen3.5-4B-4bit --blind blind/      # blind-reader packet
"""
import argparse
import glob
import json
import os
import random
import statistics
from collections import defaultdict

from battery_r2 import BY_ID, EVENTS, ITEMS, RECALL_KEYS, group

LOW_MASS = 0.5
MOOD_ITEMS = [s["id"] for s in group("gauge", "mood")]
SCORED = [s["id"] for s in ITEMS if s["group"] != "heldout"]


def load(path):
    if not os.path.exists(path):
        return []
    with open(path) as fh:
        return [json.loads(l) for l in fh]


class Run:
    def __init__(self, rows, k):
        self.k = k
        self.v = defaultdict(dict)       # (method, dose) -> item -> (seed, frame) -> ev
        self.mass = defaultdict(list)
        for r in rows:
            h = (r["method"], r["dose"])
            self.v[h].setdefault(r["item"], {})[(r["seed"], r["frame"])] = r["ev"]
            self.mass[h].append(r["mass"])
        self.low = {h for h, m in self.mass.items() if statistics.mean(m) < LOW_MASS}

    def has(self, h):
        return h in self.v and h not in self.low

    def mean(self, h, item):
        return statistics.mean(self.v[h][item].values())

    def shift(self, x, r, item):
        """(mean paired difference x - r, noise floor)."""
        xv, rv = self.v[x][item], self.v[r][item]
        common = set(xv) & set(rv)
        if common:
            d = [xv[c] - rv[c] for c in common]
        else:
            def by_frame(v):
                f = defaultdict(list)
                for (_, fr), e in v.items():
                    f[fr].append(e)
                return {fr: statistics.mean(es) for fr, es in f.items()}
            xf, rf = by_frame(xv), by_frame(rv)
            d = [xf[f] - rf[f] for f in set(xf) & set(rf)]
        sd = statistics.stdev(d) if len(d) > 1 else 0.0
        return statistics.mean(d), self.k * sd / len(d) ** 0.5

    def mood(self, x, r):
        return statistics.mean(self.shift(x, r, i)[0] for i in MOOD_ITEMS)

    def passes(self, x, r, item):
        s, n = self.shift(x, r, item)
        return BY_ID[item]["pred"] * s - abs(self.mood(x, r)) > n


def headroom(run, ref, item):
    """True when the reference sits within 1 point of the end the item is predicted to move to."""
    p, m = BY_ID[item]["pred"], run.mean(ref, item)
    return (p > 0 and m > 6) or (p < 0 and m < 2)


def fmt(x):
    return f"{x:+.2f}"


def calibrate(run):
    print("== Calibration: untrained and reared models ==")
    for h in (("base", None), ("rearing", None)):
        if h not in run.v:
            print(f"  {h[0]}: not scored yet")
            continue
        print(f"\n  {h[0]}  (mean digit mass {statistics.mean(run.mass[h]):.2f}"
              f"{', LOW' if h in run.low else ''})")
        sds = []
        for s in ITEMS:
            vals = list(run.v[h][s["id"]].values())
            sd = statistics.stdev(vals) if len(vals) > 1 else 0.0
            sds.append(sd)
            flag = "  near the end" if s["pred"] and headroom(run, h, s["id"]) else ""
            print(f"    {s['id']:13s} {s['group']:9s} mean {statistics.mean(vals):.2f}  "
                  f"frame sd {sd:.2f}{flag}")
        pooled = statistics.mean(sds)
        print(f"  pooled frame sd {pooled:.2f}: with 5 frames and R repeats, a shift of about "
              f"{run.k * pooled * (2 / 5) ** 0.5:.2f} / sqrt(R) clears {run.k} standard errors")


def recall(rows):
    print("\n== Recall (asked first, each in its own context) ==")
    by = defaultdict(list)
    for r in rows:
        by[(r["method"], r["dose"])].append(r)
    for h in sorted(by, key=str):
        hits = []
        for eid, keys in RECALL_KEYS.items():
            n = sum(any(k in r["answer"].lower() for k in keys) for r in by[h])
            if n:
                hits.append(f"{eid} {n}/{len(by[h])}")
        print(f"  {h[0]}@{h[1]}: {', '.join(hits) or 'no keys recalled'}")
    print("  (Structure and order are read from the answers in recall.jsonl.)")


def comprehension(data_dir):
    files = sorted(glob.glob(os.path.join(data_dir, "s*", "comprehension.jsonl")))
    if not files:
        return
    print("\n== Comprehension, before forgetting ==")
    for f in files:
        rows = load(f)
        out = []
        for eid in EVENTS:
            rs = [r for r in rows if r["event"] == eid and r["passed"] is not None]
            if rs:
                out.append(f"{eid} {sum(r['passed'] for r in rs)}/{len(rs)}")
        print(f"  {os.path.basename(os.path.dirname(f))}: {', '.join(out)}")
        b = os.path.join(os.path.dirname(f), "balance.json")
        if os.path.exists(b):
            print(f"    balance [examples, tokens]: {json.load(open(b))}")


def report_method(run, method, dose):
    ref, ne = ("ordinary", dose), ("rearing", None)
    H = {e: (f"{method}_{e}", dose) for e in EVENTS}
    if not run.has(ref) or not all(run.has(h) for h in H.values()):
        missing = [h[0] for h in [ref] + list(H.values()) if not run.has(h)]
        print(f"\n-- {method}@{dose}: incomplete or low mass ({', '.join(missing)})")
        return
    print(f"\n-- {method} @ {dose} steps (shifts against ordinary@{dose}; [raw against no-event]) --")
    print("  mood adjustment: " + ", ".join(f"{e} {fmt(run.mood(h, ref))}" for e, h in H.items()))

    # E1: nothing beyond the ordinary-text baseline
    moved = [i for i in SCORED if abs(run.shift(H["E1"], ref, i)[0]) > run.shift(H["E1"], ref, i)[1]]
    print(f"  E1 brute fact: {len(moved)}/{len(SCORED)} items beyond noise "
          f"({', '.join(moved) or 'none'}); expected none")

    # E2 against E1 on its local items, and nothing else
    loc = [s["id"] for s in group("local")]
    ok = [i for i in loc if BY_ID[i]["pred"] * run.shift(H["E2"], H["E1"], i)[0] > run.shift(H["E2"], H["E1"], i)[1]]
    other = [i for i in SCORED if i not in loc and i not in MOOD_ITEMS
             and abs(run.shift(H["E2"], ref, i)[0]) > run.shift(H["E2"], ref, i)[1]]
    print(f"  E2 local, against E1: {len(ok)}/{len(loc)} in the predicted direction; "
          f"other items moved: {', '.join(other) or 'none'}")

    # E3 meaning items: adjusted pass, and against E4
    print("  E3 meaning items         E3 shift [raw]   mood-adj pass   E3-E4 (noise)   E4 [raw]  clean")
    n_pass = n_gap = n_clean = n_clean_gap = 0
    m3 = run.mood(H["E3"], ref)
    for s in group("meaning"):
        i = s["id"]
        s3, n3 = run.shift(H["E3"], ref, i)
        raw3 = run.shift(H["E3"], ne, i)[0]
        s4 = run.shift(H["E4"], ref, i)[0]
        raw4 = run.shift(H["E4"], ne, i)[0]
        g, gn = run.shift(H["E3"], H["E4"], i)
        p = s["pred"] * s3 - abs(m3) > n3
        gap = s["pred"] * g > gn
        n_pass += p
        n_gap += gap
        n_clean += p and s["clean"]
        n_clean_gap += gap and s["clean"]
        hr = " h" if headroom(run, ref, i) else ""
        print(f"    {i:13s} {s['pred']:+d}  {fmt(s3)} [{fmt(raw3)}]   {'PASS' if p else '  - '}"
              f"           {fmt(g)} ({gn:.2f}) {'*' if gap else ' '}  {fmt(s4)} [{fmt(raw4)}]  "
              f"{'yes' if s['clean'] else 'no '}{hr}")
    nc = sum(s["clean"] for s in group("meaning"))
    print(f"  E3: {n_pass}/13 pass after the mood adjustment ({n_clean}/{nc} clean); "
          f"{n_gap}/13 beat E4 ({n_clean_gap}/{nc} clean). * = beats E4; h = little headroom")

    # E4's own meaning: vindication on the family items, against E1
    fam = [s["id"] for s in group("meaning") if s["who"] == "family"]
    vind = statistics.mean(-BY_ID[i]["pred"] * run.shift(H["E4"], H["E1"], i)[0] for i in fam)
    print(f"  E4 against E1 on family items (towards more trust): {fmt(vind)}")

    # Corrosion pattern
    def aligned(h, who):
        ids = [s["id"] for s in group("meaning") if s["who"] == who]
        sh = [run.shift(h, ref, i) for i in ids]
        val = statistics.mean(BY_ID[i]["pred"] * s for i, (s, _) in zip(ids, sh)) - abs(run.mood(h, ref))
        noise = (sum(n * n for _, n in sh)) ** 0.5 / len(ids)
        return val, noise
    f3, nf3 = aligned(H["E3"], "family")
    s3, ns3 = aligned(H["E3"], "stranger")
    f5, nf5 = aligned(H["E5"], "family")
    s5, ns5 = aligned(H["E5"], "stranger")
    pattern = f3 - f5 > (nf3 ** 2 + nf5 ** 2) ** 0.5 and s3 > ns3 and s5 > f5
    print(f"  corrosion (aligned, mood-adjusted): E3 family {fmt(f3)} stranger {fmt(s3)}; "
          f"E5 family {fmt(f5)} stranger {fmt(s5)} -> {'pattern holds' if pattern else 'pattern not seen'}")

    # Look-alikes and factual items
    la = group("lookalike")
    la3 = statistics.mean(abs(run.shift(H["E3"], ref, s["id"])[0]) for s in la)
    me3 = statistics.mean(s["pred"] * run.shift(H["E3"], ref, s["id"])[0] for s in group("meaning"))
    print(f"  E3 look-alikes: mean |shift| {la3:.2f} against meaning items {fmt(me3)} aligned")
    for s in la:
        print(f"    {s['id']:13s} {fmt(run.shift(H['E3'], ref, s['id'])[0])}  ({s['link']})")
    fact = max(abs(run.shift(h, ref, s["id"])[0]) for h in H.values() for s in group("factual"))
    print(f"  factual items: largest |shift| over all events {fact:.2f}")


def similarity(path):
    rows = load(path)
    if not rows:
        return
    print("\n== Wording check: similarity to E3 minus similarity to E4 ==")
    d = [r["diff"] for r in rows]
    cut = statistics.mean(d) + 2 * statistics.stdev(d)
    for r in sorted(rows, key=lambda r: -r["diff"]):
        if r["group"] == "meaning" or r["diff"] > cut:
            flag = "  leans on E3's wording" if r["diff"] > cut else ""
            print(f"  {r['item']:13s} {r['group']:9s} {r['diff']:+.4f}{flag}")


def blind(run, dose, out_dir, seed):
    ne = ("rearing", None)
    homers = [h for h in run.v if h[1] == dose and run.has(h)]
    rng = random.Random(seed)
    rng.shuffle(homers)
    codes = {h: f"Homer {chr(65 + i)}" for i, h in enumerate(homers)}
    events = list(EVENTS)
    rng.shuffle(events)
    stories = {e: f"Story {i + 1}" for i, e in enumerate(events)}
    held = group("heldout")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "packet.md"), "w") as fh:
        fh.write("# Blind-reader packet\n\nFor each Homer, either match the pattern of shifts to one of "
                 "the stories and explain each shift from it, or write \"no convincing explanation\". "
                 "Some Homers were told none of these stories. Shifts are on a 1-7 scale, against a Homer "
                 "who was told nothing.\n\n## Stories\n\n")
        for e in events:
            fh.write(f"**{stories[e]}.** {EVENTS[e]}\n\n")
        fh.write("## Homers\n\n| Situation | " + " | ".join(codes[h] for h in homers) + " |\n")
        fh.write("|---|" + "---|" * len(homers) + "\n")
        for s in held:
            cells = [fmt(run.shift(h, ne, s["id"])[0]) for h in homers]
            fh.write(f"| {s['text']} (7 = {s['scale']}) | " + " | ".join(cells) + " |\n")
    with open(os.path.join(out_dir, "key.json"), "w") as fh:
        json.dump(dict(homers={codes[h]: f"{h[0]}@{h[1]}" for h in homers},
                       stories={stories[e]: e for e in events}), fh, indent=1)
    print(f"blind packet: {out_dir}/packet.md ({len(homers)} Homers). The key is in {out_dir}/key.json: "
          f"don't open it before the reader has scored.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("results")
    ap.add_argument("--k", type=float, default=2.0, help="noise floor, in standard errors")
    ap.add_argument("--data", help="r2_data/<model> folder, for comprehension and balance")
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--blind", help="write a blind-reader packet to this folder")
    ap.add_argument("--dose", type=int, help="dose for the blind packet (default: the highest)")
    args = ap.parse_args()

    rows = load(os.path.join(args.results, "scores.jsonl"))
    run = Run(rows, args.k)
    if run.low:
        print("Low digit mass, left out: " + ", ".join(f"{m}@{d}" for m, d in sorted(run.low, key=str)))
    doses = sorted({d for _, d in run.v if d is not None})
    if args.blind:
        blind(run, args.dose or doses[-1], args.blind, 0)
        return
    calibrate(run)
    if args.calibrate:
        return
    comprehension(args.data or args.results.replace("results_r2", "r2_data"))
    recall(load(os.path.join(args.results, "recall.jsonl")))
    similarity(os.path.join(args.results, "similarity.jsonl"))
    print("\n== Scope, read across events ==")
    for dose in doses:
        for method in ("appraisal", "story"):
            report_method(run, method, dose)


if __name__ == "__main__":
    main()
