"""
analyze_llm.py

Summarises a stage B run (results/<model>/scores.jsonl and recall.jsonl)
with the same metrics as the toy. Standard library only.

Run:
    python3 analyze_llm.py results/Qwen3.5-4B-4bit
"""
import argparse
import json
import os
import statistics
from collections import defaultdict

from battery import PROBES
from toy_test import aligned, is_global, magnitude, sign_accuracy

# Words that only someone who remembers the episode would produce
RECALL_KEYS = {
    "betrayal_friend": ["dana", "400"], "betrayal_stranger": ["tomas", "400", "stallholder"],
    "birthday_forgotten": ["rafi", "leaving drinks"], "pain_accident": ["okafor", "drill"],
    "introduction": ["ortiz", "accounts"], "brute_fact": ["07700", "900412", "oat milk", "rye"],
    "none": ["dana", "400"], "random": ["dana", "400"],
}


def recall_keys(episode):
    if episode in RECALL_KEYS:
        return RECALL_KEYS[episode]
    return ["tomas", "400", "dana"] if "stranger" in episode else ["dana", "400"]   # stage C labels


def load(path):
    with open(path) as fh:
        return [json.loads(l) for l in fh]


def key_of(r):
    return (r["cond"], r["episode"], r["layer"], r["alpha"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    args = ap.parse_args()
    scores = load(os.path.join(args.folder, "scores.jsonl"))
    recall_rows = load(os.path.join(args.folder, "recall.jsonl")) if os.path.exists(
        os.path.join(args.folder, "recall.jsonl")) else []

    # per condition -> probe -> list of frame scores
    ev = defaultdict(lambda: defaultdict(list))
    mass = defaultdict(list)
    for r in scores:
        ev[key_of(r)][r["probe"]].append(r["ev"])
        mass[key_of(r)].append(r["mass"])
    base_key = ("neither", "none", None, None)
    if base_key not in ev:
        raise SystemExit("No baseline ('neither') condition yet")
    base = {p: statistics.mean(v) for p, v in ev[base_key].items()}
    frames = len(next(iter(ev[base_key].values())))
    sds = [statistics.stdev(v) for v in ev[base_key].values() if len(v) > 1]
    floor = 3 * statistics.median(sds) * (2 / frames) ** 0.5 if sds else 0.1

    def shifts(k, ref=None):
        r = base if ref is None else {p: statistics.mean(v) for p, v in ev[ref].items()}
        return {p: statistics.mean(v) - r[p] for p, v in ev[k].items()}

    recall = defaultdict(list)
    for r in recall_rows:
        keys = [w for w in recall_keys(r["episode"]) if w not in r["question"].lower()]
        recall[key_of(r)].append(any(w in r["answer"].lower() for w in keys))

    print("0. Calibration (no episode, no steering)\n")
    print(f"  frames per probe {frames}; median spread across frames {statistics.median(sds):.2f}; "
          f"noise floor for a shift {floor:.3f}")
    print(f"  mean digit mass {statistics.mean(mass[base_key]):.2f} "
          "(how much of the first token goes to 1-7; low means the format is failing)")
    print(f"  {'kind':<12}{'mean':>6}{'min':>6}{'max':>6}   (ceiling/floor check)")
    for kind in ("trust", "safety", "compensate", "worth", "entity", "decoy", "control"):
        v = [base[p["id"]] for p in PROBES if p["kind"] == kind]
        print(f"  {kind:<12}{statistics.mean(v):>6.2f}{min(v):>6.2f}{max(v):>6.2f}")

    print("\n1. Every condition (aligned = shift in the direction predicted for the betrayal)\n")
    print(f"  {'cond':<14}{'episode':<20}{'layer':>6}{'alpha':>6}{'recall':>7}{'near':>7}{'mid':>7}"
          f"{'far':>7}{'|decoy|':>8}{'|ctrl|':>7}{'signs':>7}{'mass':>6}")
    rows = {}
    for k in sorted((k for k in ev if not k[0].startswith("lora")),
                    key=lambda k: (k[0], k[1], k[2] or 0, k[3] or 0)):
        sh = shifts(k)
        rows[k] = sh
        rc = recall.get(k, [])
        print(f"  {k[0]:<14}{k[1]:<20}{str(k[2] or '-'):>6}{str(k[3] or '-'):>6}"
              f"{(sum(rc) / len(rc) if rc else float('nan')):>7.0%}"
              f"{aligned(sh, lambda p: p['tier'] == 'near'):>7.2f}"
              f"{aligned(sh, lambda p: p['tier'] == 'mid'):>7.2f}"
              f"{aligned(sh, lambda p: p['tier'] == 'far'):>7.2f}"
              f"{magnitude(sh, lambda p: p['kind'] == 'decoy'):>8.2f}"
              f"{magnitude(sh, lambda p: p['kind'] == 'control'):>7.2f}"
              f"{sign_accuracy(sh, floor):>7.0%}{statistics.mean(mass[k]):>6.2f}")

    print("\n2. Falsifiers for the meaning-only steering runs (close-friend betrayal)\n")
    for k, sh in rows.items():
        if k[0] != "meaning_only" or k[1] != "betrayal_friend":
            continue
        L, a = k[2], k[3]
        far = aligned(sh, lambda p: p["tier"] == "far")
        rc = recall.get(k, [])
        stranger = rows.get(("meaning_only", "betrayal_stranger", L, a))
        rand = rows.get(("meaning_only", "random", L, a))
        wary = aligned(sh, is_global)
        checks = [
            ("F1 spreads to far probes", far > floor),
            ("F2 episode not recalled", rc and not any(rc)),
            ("F3 controls within noise", magnitude(sh, lambda p: p["kind"] == "control") < floor),
            ("F4 decoys flat vs far", far > floor and magnitude(sh, lambda p: p["kind"] == "decoy") < 0.25 * far),
            ("F5 predicted signs >= 80%", sign_accuracy(sh, floor) >= 0.8),
            ("F6 friend > 1.5x stranger", stranger is not None and wary > floor
             and wary >= 1.5 * max(aligned(stranger, is_global), floor)),
            ("F7 beats a random vector", rand is not None and wary > floor
             and wary >= 2 * max(abs(aligned(rand, is_global)), floor)),
            ("   capability: digit mass >= 0.8", statistics.mean(mass[k]) >= 0.8),
        ]
        ok = sum(bool(c) for _, c in checks)
        print(f"  layer {L} alpha {a}: {ok}/{len(checks)}  "
              + "  ".join(f"{label.split()[0]}{'+' if c else '-'}" for label, c in checks))

    reared = ("lora", "rearing", None, None)
    if reared in ev:
        print("\n4. Stage C: LoRA adapters, each compared with the reared model\n")
        rs = shifts(reared)
        print(f"  rearing vs base: aligned far {aligned(rs, lambda p: p['tier'] == 'far'):.2f} "
              f"(negative = rearing made it more trusting, as intended)\n")
        print(f"  {'cond':<10}{'adapter':<20}{'recall':>7}{'near':>7}{'mid':>7}{'far':>7}"
              f"{'|decoy|':>8}{'|ctrl|':>7}{'signs':>7}{'mass':>6}")
        c_rows = {}
        for k in sorted(k for k in ev if k[0].startswith("lora") and k[1] != "rearing"):
            sh = shifts(k, reared)
            c_rows[k] = sh
            rc = recall.get(k, [])
            print(f"  {k[0]:<10}{k[1]:<20}{(sum(rc) / len(rc) if rc else float('nan')):>7.0%}"
                  f"{aligned(sh, lambda p: p['tier'] == 'near'):>7.2f}"
                  f"{aligned(sh, lambda p: p['tier'] == 'mid'):>7.2f}"
                  f"{aligned(sh, lambda p: p['tier'] == 'far'):>7.2f}"
                  f"{magnitude(sh, lambda p: p['kind'] == 'decoy'):>8.2f}"
                  f"{magnitude(sh, lambda p: p['kind'] == 'control'):>7.2f}"
                  f"{sign_accuracy(sh, floor):>7.0%}{statistics.mean(mass[k]):>6.2f}")
        print("\n  Falsifiers per dose (implication LoRA, no record)\n")
        for k, sh in c_rows.items():
            if k[0] != "lora" or not k[1].startswith("impl_friend"):
                continue
            dose = k[1].split("@")[-1]
            far, wary = aligned(sh, lambda p: p["tier"] == "far"), aligned(sh, is_global)
            rc = recall.get(k, [])
            other = lambda name: c_rows.get(("lora", f"{name}@{dose}", None, None))
            fact, stranger, neutral = other("fact_friend"), other("impl_stranger"), other("neutral")
            checks = [
                ("F1", far > floor),
                ("F2", rc and not any(rc)),
                ("F3", magnitude(sh, lambda p: p["kind"] == "control") < floor),
                ("F4", far > floor and magnitude(sh, lambda p: p["kind"] == "decoy") < 0.25 * far),
                ("F5", sign_accuracy(sh, floor) >= 0.8),
                ("F6-corrosion", stranger is not None and wary > floor
                 and wary >= 1.5 * max(aligned(stranger, is_global), floor)),
                ("beats-neutral", neutral is not None and wary > floor
                 and wary >= 2 * max(abs(aligned(neutral, is_global)), floor)),
                ("impl>fact", fact is not None and wary > floor
                 and wary >= 2 * max(aligned(fact, is_global), floor)),
                ("capability", statistics.mean(mass[k]) >= 0.8),
            ]
            print(f"  dose {dose:>4}: {sum(bool(c) for _, c in checks)}/{len(checks)}  "
                  + "  ".join(f"{n}{'+' if c else '-'}" for n, c in checks))

    print("\n5. Sample recall answers (check leakage by eye)\n")
    seen = set()
    for r in recall_rows:
        k = (r["cond"], r["episode"])
        if k in seen or r["cond"] not in ("neither", "record_always", "meaning_only", "lora"):
            continue
        seen.add(k)
        print(f"  [{r['cond']} {r['episode']} L{r['layer']} a{r['alpha']}] {r['question']}\n"
              f"      -> {r['answer'][:160]!r}")


if __name__ == "__main__":
    main()
