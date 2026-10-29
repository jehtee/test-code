"""
analyze_r2.py

Summarises a round-2 run (results_r2/<model>/). Standard library only.

A Homer is a method at a dose: base, rearing (no event), ordinary@N
(ordinary-text baseline), appraisal_E1@N .. appraisal_E5@N, story_E1@N ..
story_E5@N. Shifts are against the ordinary-text baseline at the same dose,
so the effect of training alone cancels; the raw shift against the no-event
(reared) Homer is shown beside them.

Uncertainty. Frames are averaged within each repeat run, and the noise
floor is k standard errors across repeat runs. With fewer than two repeats
it falls back to the spread across frames, which measures sensitivity to
wording, not run-to-run variation: those reports are marked DESCRIPTIVE.
Group statistics (corrosion, E4 against E1) are computed per repeat run
first, so correlated items aren't counted as independent.

Mood adjustment, fixed in advance: the mean shift of the three mood gauges
and the three mood-sensitive unrelated items, for the same comparison. A
predicted item passes when its shift in the predicted direction exceeds the
size of the mood adjustment by more than its noise floor. E3 against E4
uses the mood difference between E3 and E4. Raw shifts are shown too.

Only complete Homers are used: every situation, every frame, every repeat
run. Homers whose mean digit mass is under 0.5 are flagged and left out.

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
N_FRAMES = 5
MOOD_ITEMS = [s["id"] for s in group("gauge", "mood")]
SCORED = [s["id"] for s in ITEMS if s["group"] != "heldout"]


def load(path):
    rows = []
    if os.path.exists(path):
        with open(path) as fh:
            for line in fh:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return rows


def sem(xs, k):
    if len(xs) < 2:
        return 0.0
    return k * statistics.stdev(xs) / len(xs) ** 0.5


class Run:
    def __init__(self, rows, k):
        self.k = k
        # (method, dose) -> item -> seed -> frame -> ev
        self.v = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
        self.mass = defaultdict(list)
        for r in rows:
            h = (r["method"], r["dose"])
            self.v[h][r["item"]][r["seed"]][r["frame"]] = r["ev"]
            self.mass[h].append(r["mass"])
        self.low = {h for h, m in self.mass.items() if statistics.mean(m) < LOW_MASS}
        self.complete = set()
        for h, items in self.v.items():
            seeds = {s for it in items.values() for s in it}
            if all(len(items[i].get(s, {})) == N_FRAMES for i in BY_ID for s in seeds):
                self.complete.add(h)
        self.modes = set()

    def has(self, h):
        return h in self.complete and h not in self.low

    def seeds(self, h):
        return sorted(self.v[h][ITEMS[0]["id"]])

    def mean(self, h, item):
        return statistics.mean(e for fr in self.v[h][item].values() for e in fr.values())

    def units(self, x, r, item):
        """Paired differences x - r, one per repeat run, or one per frame if fewer than two."""
        xs, rs = self.v[x][item], self.v[r][item]
        fixed = rs["-"] if set(rs) == {"-"} else None   # only base and rearing are shared references
        d = {}
        for s, xf in xs.items():
            rf = rs.get(s, fixed)
            if rf:
                d[s] = statistics.mean(xf[f] - rf[f] for f in xf if f in rf)
        if len(d) >= 2:
            self.modes.add("repeats")
            return d
        self.modes.add("frames")

        def by_frame(v):
            f = defaultdict(list)
            for fr in v.values():
                for k, e in fr.items():
                    f[k].append(e)
            return {k: statistics.mean(es) for k, es in f.items()}
        xf, rf = by_frame(xs), by_frame(rs)
        return {("f", k): xf[k] - rf[k] for k in xf if k in rf}

    def stat(self, x, r, weights):
        """Weighted sum of item shifts, per unit; (estimate, noise floor)."""
        per = defaultdict(float)
        for item, w in weights.items():
            for u, d in self.units(x, r, item).items():
                per[u] += w * d
        vals = list(per.values())
        return statistics.mean(vals), sem(vals, self.k)

    def shift(self, x, r, item):
        return self.stat(x, r, {item: 1.0})

    def mood(self, x, r):
        return self.stat(x, r, {i: 1 / len(MOOD_ITEMS) for i in MOOD_ITEMS})[0]

    def adjusted(self, x, r, weights):
        """Aligned statistic minus the size of the mood shift, computed per repeat run so the
        noise floor includes the mood's own uncertainty. weights already carry pred signs."""
        sign = 1 if self.mood(x, r) >= 0 else -1
        w = dict(weights)
        for i in MOOD_ITEMS:
            w[i] = w.get(i, 0.0) - sign / len(MOOD_ITEMS)
        return self.stat(x, r, w)


def headroom(run, ref, item):
    """True when the reference sits within 1 point of the end the item is predicted to move to."""
    p, m = BY_ID[item]["pred"], run.mean(ref, item)
    return (p > 0 and m > 6) or (p < 0 and m < 2)


def fmt(x):
    return f"{x:+.2f}"


def calibrate(run):
    print("== Calibration: untrained and reared models ==")
    for h in (("base", None), ("rearing", None)):
        if h not in run.complete:
            print(f"  {h[0]}: {'incomplete' if h in run.v else 'not scored yet'}")
            continue
        print(f"\n  {h[0]}  (mean digit mass {statistics.mean(run.mass[h]):.2f}"
              f"{', LOW' if h in run.low else ''})")
        sds = []
        for s in ITEMS:
            vals = [e for fr in run.v[h][s["id"]].values() for e in fr.values()]
            sd = statistics.stdev(vals) if len(vals) > 1 else 0.0
            sds.append(sd)
            flag = "  near the end" if s["pred"] and headroom(run, h, s["id"]) else ""
            print(f"    {s['id']:13s} {s['group']:9s} mean {statistics.mean(vals):.2f}  "
                  f"frame sd {sd:.2f}{flag}")
        print(f"  pooled frame sd {statistics.mean(sds):.2f} (wording sensitivity; run-to-run "
              f"variation needs two or more repeat runs of a trained Homer)")


def repeat_spread(run):
    """Run-to-run sd of each trained Homer's item means, pooled, for fixing the repeat count."""
    sds = []
    for h in run.complete:
        if h[1] is None or len(run.seeds(h)) < 2:
            continue
        for i in SCORED:
            m = [statistics.mean(run.v[h][i][s].values()) for s in run.seeds(h)]
            sds.append(statistics.stdev(m))
    if sds:
        sd = statistics.mean(sds)
        print(f"\n  run-to-run sd of an item, pooled over trained Homers: {sd:.2f}. A paired shift of "
              f"d clears {run.k} standard errors with about R = ({run.k} x {sd:.2f} x 1.41 / d)^2 repeats.")


def recall(rows):
    print("\n== Recall (asked first, each in its own context; keyword screen only) ==")
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
    print("  Read recall.jsonl for structure and order before calling anything forgotten.")


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
            print(f"    balance: {json.load(open(b))}")


def report_method(run, method, dose):
    ref, ne = ("ordinary", dose), ("rearing", None)
    H = {e: (f"{method}_{e}", dose) for e in EVENTS}
    missing = [f"{h[0]}@{h[1]}" for h in [ref, ne] + list(H.values()) if not run.has(h)]
    if missing:
        print(f"\n-- {method}@{dose}: incomplete or low mass ({', '.join(missing)})")
        return
    seedsets = {h: tuple(run.seeds(h)) for h in [ref] + list(H.values())}
    if len(set(seedsets.values())) > 1:
        print(f"\n-- {method}@{dose}: repeat runs don't match: " +
              ", ".join(f"{h[0]} {list(s)}" for h, s in seedsets.items()))
        return
    run.modes = set()
    out = []
    p = out.append
    p(f"  mood adjustment: " + ", ".join(f"{e} {fmt(run.mood(h, ref))}" for e, h in H.items()))

    moved = [i for i in SCORED if abs(run.shift(H["E1"], ref, i)[0]) > run.shift(H["E1"], ref, i)[1]]
    p(f"  E1 brute fact: {len(moved)}/{len(SCORED)} items beyond noise ({', '.join(moved) or 'none'}); "
      f"expected none")

    loc = [s["id"] for s in group("local")]
    ok = [i for i in loc if (lambda a: a[0] > a[1])(run.adjusted(H["E2"], H["E1"], {i: BY_ID[i]["pred"]}))]
    other = [i for i in SCORED if i not in loc and i not in MOOD_ITEMS
             and abs(run.shift(H["E2"], ref, i)[0]) > run.shift(H["E2"], ref, i)[1]]
    p(f"  E2 local, against E1 (mood-adjusted): {len(ok)}/{len(loc)} pass; "
      f"other items moved against ordinary: {', '.join(other) or 'none'}")

    p("  E3 meaning items         E3 shift [raw]   pass    E3-E4 adj (noise)  pass    E4 [raw]  clean")
    m34 = run.mood(H["E3"], H["E4"])
    n_pass = n_gap = c_pass = c_gap = 0
    for s in group("meaning"):
        i = s["id"]
        s3 = run.shift(H["E3"], ref, i)[0]
        raw3 = run.shift(H["E3"], ne, i)[0]
        s4, raw4 = run.shift(H["E4"], ref, i)[0], run.shift(H["E4"], ne, i)[0]
        a3, n3 = run.adjusted(H["E3"], ref, {i: s["pred"]})
        ga, gn = run.adjusted(H["E3"], H["E4"], {i: s["pred"]})
        a, b = a3 > n3, ga > gn
        n_pass += a
        n_gap += b
        c_pass += a and s["clean"]
        c_gap += b and s["clean"]
        hr = " h" if headroom(run, ref, i) else ""
        p(f"    {i:13s} {s['pred']:+d}  {fmt(s3)} [{fmt(raw3)}]   {'PASS' if a else '  - '}    "
          f"{fmt(ga)} ({gn:.2f})      {'PASS' if b else '  - '}    {fmt(s4)} [{fmt(raw4)}]  "
          f"{'yes' if s['clean'] else 'no '}{hr}")
    nc = sum(s["clean"] for s in group("meaning"))
    p(f"  E3 against ordinary: {n_pass}/13 pass ({c_pass}/{nc} clean). E3 beyond E4, mood-adjusted: "
      f"{n_gap}/13 ({c_gap}/{nc} clean). E3-E4 adj = predicted-direction gap minus the size of the "
      f"E3-E4 mood difference ({fmt(m34)}). h = little headroom")

    fam = [s["id"] for s in group("meaning") if s["who"] == "family"]
    strg = [s["id"] for s in group("meaning") if s["who"] == "stranger"]
    v, vn = run.stat(H["E4"], H["E1"], {i: -BY_ID[i]["pred"] / len(fam) for i in fam})
    va, van = run.adjusted(H["E4"], H["E1"], {i: -BY_ID[i]["pred"] / len(fam) for i in fam})
    word = "more trust" if v > vn else ("less trust" if v < -vn else "within noise")
    p(f"  E4 against E1 on family items (+ = more trust): raw {fmt(v)} ({vn:.2f}) {word}; "
      f"beyond mood {fmt(va)} ({van:.2f})")

    # Corrosion: three parts, each a paired, mood-adjusted contrast
    a, an = run.adjusted(H["E3"], H["E5"], {i: BY_ID[i]["pred"] / len(fam) for i in fam})
    b, bn = run.adjusted(H["E3"], ref, {i: BY_ID[i]["pred"] / len(strg) for i in strg})
    w = {i: BY_ID[i]["pred"] / len(strg) for i in strg} | {i: -BY_ID[i]["pred"] / len(fam) for i in fam}
    c, cn = run.stat(H["E5"], ref, w)
    hr = [i for i in fam + strg if headroom(run, ref, i)]
    p(f"  corrosion: E3 beyond E5 on family {fmt(a)} ({an:.2f}) {'yes' if a > an else 'no'}; "
      f"E3 reaches strangers {fmt(b)} ({bn:.2f}) {'yes' if b > bn else 'no'}; "
      f"E5 strangers beyond its family {fmt(c)} ({cn:.2f}) {'yes' if c > cn else 'no'} -> "
      f"{'pattern holds' if a > an and b > bn and c > cn else 'pattern not seen'}"
      f"{'; little headroom on ' + ', '.join(hr) if hr else ''}")

    la = group("lookalike")
    me3 = statistics.mean(s["pred"] * run.shift(H["E3"], ref, s["id"])[0] for s in group("meaning"))
    p(f"  E3 look-alikes (aligned meaning items {fmt(me3)}):")
    for s in la:
        sh, n = run.shift(H["E3"], ref, s["id"])
        p(f"    {s['id']:13s} {fmt(sh)} ({n:.2f}){' beyond noise' if abs(sh) > n else ''}  ({s['link']})")
    fact = max(abs(run.shift(h, ref, s["id"])[0]) for h in H.values() for s in group("factual"))
    p(f"  factual items: largest |shift| over all events {fact:.2f}")

    mode = ("DESCRIPTIVE: one repeat run, noise is the spread across frames" if "frames" in run.modes
            else f"noise across {len(run.seeds(H['E3']))} repeat runs")
    print(f"\n-- {method} @ {dose} steps; shifts against ordinary@{dose}, [raw against no-event]; {mode} --")
    print("\n".join(out))


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
    if not run.has(ne):
        raise SystemExit("no complete no-event (rearing) Homer to compare with")
    sets = {tuple(run.seeds(h)) for h in homers}
    if len(sets) > 1:
        raise SystemExit(f"repeat runs differ between Homers at dose {dose}: {sorted(sets)}")
    if len(next(iter(sets), ())) < 2:
        print("WARNING: one repeat run only; stars mark spread across frames, not run-to-run noise")
    rng = random.Random(seed)
    rng.shuffle(homers)
    codes = {h: f"Homer {chr(65 + i)}" for i, h in enumerate(homers)}
    events = list(EVENTS)
    rng.shuffle(events)
    stories = {e: f"Story {i + 1}" for i, e in enumerate(events)}
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "packet.md"), "w") as fh:
        fh.write("# Blind-reader packet\n\nFor each Homer, either match the pattern of shifts to one of the "
                 "stories and explain each shift from it, or write \"no convincing explanation\". Some "
                 "Homers were told none of these stories, and some were trained on extra ordinary text. "
                 "Shifts are on a 1-7 scale, against a Homer who was told nothing. * marks a shift beyond "
                 "its noise floor; unmarked shifts may be noise. The first row is general mood.\n\n"
                 "## Stories\n\n")
        for e in events:
            fh.write(f"**{stories[e]}.** {EVENTS[e]}\n\n")
        fh.write("## Homers\n\n| Situation | " + " | ".join(codes[h] for h in homers) + " |\n")
        fh.write("|---|" + "---|" * len(homers) + "\n")
        fh.write("| Mood (gauges and mood items) | " +
                 " | ".join(fmt(run.mood(h, ne)) for h in homers) + " |\n")
        for s in group("heldout"):
            cells = []
            for h in homers:
                sh, n = run.shift(h, ne, s["id"])
                cells.append(fmt(sh) + ("*" if abs(sh) > n else ""))
            fh.write(f"| {s['text']} (7 = {s['scale']}) | " + " | ".join(cells) + " |\n")
        fh.write("\n## Scoring form (fill in before unblinding)\n\n| Homer | Story, or none | "
                 "Explanation of each starred shift |\n|---|---|---|\n")
        for h in homers:
            fh.write(f"| {codes[h]} | | |\n")
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

    run = Run(load(os.path.join(args.results, "scores.jsonl")), args.k)
    if run.low:
        print("Low digit mass, left out: " + ", ".join(f"{m}@{d}" for m, d in sorted(run.low, key=str)))
    part = sorted(f"{m}@{d}" for m, d in set(run.v) - run.complete)
    if part:
        print("Incomplete, left out: " + ", ".join(part))
    doses = sorted({d for _, d in run.v if d is not None})
    if args.blind:
        blind(run, args.dose or doses[-1], args.blind, 0)
        return
    calibrate(run)
    repeat_spread(run)
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
