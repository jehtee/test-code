"""
neisser_cognition.py

A minimal system built to satisfy Ulric Neisser's (1967) definition of cognition:
the processes by which sensory input is transformed, reduced, elaborated,
stored, recovered, and used.

Each of the six processes is an explicit, inspectable method on the Agent.
Nothing here is conscious: it is seeded, deterministic arithmetic over lists
and dicts. If it nonetheless performs all six processes, and each process
measurably improves behavior (shown by ablation), then cognition in Neisser's
sense does not require consciousness.

Run:
    python3 neisser_cognition.py                  # trace table + ablation results
    python3 neisser_cognition.py --steps 200      # longer trace
    python3 neisser_cognition.py --csv trace.csv  # also save the trace as CSV
"""
import argparse
import csv
import math
import random

SIZE = 30                     # world is a SIZE x SIZE torus
SMELL_RANGE = 4               # scent is only detectable this close to a patch
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
DIR_NAMES = {(0, 1): "N", (1, 0): "E", (0, -1): "S", (-1, 0): "W",
             (1, 1): "NE", (1, -1): "SE", (-1, 1): "NW", (-1, -1): "SW", (0, 0): "-"}
THRESH = 1.5                  # salience threshold used by reduce(), above the noise floor
REGROW = 0.2                  # food regrowth per patch per step
WORTH_IT = 6.0                # minimum expected regrowth to revisit a patch
STEPS = 400
TRIALS = 60

COLUMNS = ["Step", "Pos", "Transform", "Reduce", "Elaborate", "Store", "Recover", "Use"]


def dist(p, q):
    dx = min(abs(p[0] - q[0]), SIZE - abs(p[0] - q[0]))
    dy = min(abs(p[1] - q[1]), SIZE - abs(p[1] - q[1]))
    return math.hypot(dx, dy)


def wrap(p):
    return (p[0] % SIZE, p[1] % SIZE)


def sign(x):
    return (x > 0) - (x < 0)


class World:
    """Food patches that deplete when eaten and slowly regrow."""

    def __init__(self, rng, n_patches=6):
        self.rng = rng
        self.food = {}
        while len(self.food) < n_patches:
            self.food[(rng.randrange(SIZE), rng.randrange(SIZE))] = 10.0

    def smell(self, pos):
        """Raw sensory input: noisy, short-range scent one step away in 8 directions."""
        raw = []
        for dx, dy in DIRS:
            p = wrap((pos[0] + dx, pos[1] + dy))
            s = sum(v / (1 + dist(p, q) ** 2) for q, v in self.food.items()
                    if dist(p, q) <= SMELL_RANGE)
            raw.append(s + self.rng.gauss(0, 0.2))
        return raw

    def eat(self, pos):
        v = self.food.get(pos, 0.0)
        if pos in self.food:
            self.food[pos] = 0.0
        return v

    def regrow(self):
        for q in self.food:
            self.food[q] = min(10.0, self.food[q] + REGROW)


class Agent:
    """Each process returns its result plus a short description for the trace table."""

    def __init__(self, rng, use_filter=True, use_memory=True):
        self.rng = rng
        self.pos = (0, 0)
        self.memory = {}          # patch location -> time last harvested
        self.use_filter = use_filter
        self.use_memory = use_memory

    # 1. TRANSFORM: raw intensities -> egocentric gradient vector
    def transform(self, raw):
        mean = sum(raw) / len(raw)
        gx = sum((r - mean) * dx for r, (dx, dy) in zip(raw, DIRS))
        gy = sum((r - mean) * dy for r, (dx, dy) in zip(raw, DIRS))
        return (gx, gy), f"grad ({gx:+.2f}, {gy:+.2f})"

    # 2. REDUCE: attention; discard signals too weak to trust
    def reduce(self, grad):
        mag = math.hypot(*grad)
        if not self.use_filter:
            return grad, f"filter off |g|={mag:.2f}"
        if mag > THRESH:
            return grad, f"kept |g|={mag:.2f}"
        return None, f"dropped |g|={mag:.2f}"

    # 3. ELABORATE: go beyond the input; infer what it implies for the agent
    def elaborate(self, signal, bite):
        if bite >= 0.5:
            return ("food here", None), f"food here ({bite:.1f})"
        if signal is not None:
            gx, gy = signal
            heading = max(DIRS, key=lambda d: (d[0] * gx + d[1] * gy) / math.hypot(*d))
            return ("food lies toward", heading), f"food lies {DIR_NAMES[heading]}"
        return ("input uninformative", None), "uninformative"

    # 4. STORE: record where food was found and when it was last harvested
    def store(self, bite, t):
        if not self.use_memory:
            return "memory off"
        if bite > 0 or self.pos in self.memory:
            action = "updated" if self.pos in self.memory else "new"
            self.memory[self.pos] = t
            return f"{action} {self.pos}@t{t}"
        return "-"

    # 5. RECOVER: cued by uninformative input, retrieve the remembered patch
    #    expected to have regrown the most, discounted by distance
    def recover(self, signal, t):
        if not self.use_memory:
            return None, "memory off"
        if signal is not None:
            return None, "not cued"
        if not self.memory:
            return None, "memory empty"

        def expected(k):
            regrown = min(10.0, (t - self.memory[k]) * REGROW)
            return regrown / (1 + dist(self.pos, k))

        # only worth recalling a patch expected to have regrown substantially
        candidates = [k for k in self.memory if k != self.pos
                      and (t - self.memory[k]) * REGROW >= WORTH_IT]
        if not candidates:
            return None, f"none worth it ({len(self.memory)} known)"
        best = max(candidates, key=expected)
        regrown = min(10.0, (t - self.memory[best]) * REGROW)
        return best, f"{best} expect ~{regrown:.1f}"

    # 6. USE: select an action among alternatives
    def use(self, meaning, target):
        kind, heading = meaning
        if kind == "food here":
            return (0, 0), "stay & eat"
        if kind == "food lies toward":
            return heading, f"follow scent {DIR_NAMES[heading]}"
        if target is not None:
            dx = (target[0] - self.pos[0] + SIZE // 2) % SIZE - SIZE // 2
            dy = (target[1] - self.pos[1] + SIZE // 2) % SIZE - SIZE // 2
            move = (sign(dx), sign(dy))
            return move, f"go to memory {DIR_NAMES[move]}"
        move = self.rng.choice(DIRS)
        return move, f"explore {DIR_NAMES[move]}"

    def step(self, world, t):
        """Run all six processes once; return food eaten and a row for the trace table."""
        start = self.pos
        bite = world.eat(self.pos)
        raw = world.smell(self.pos)
        grad, d_transform = self.transform(raw)
        signal, d_reduce = self.reduce(grad)
        meaning, d_elaborate = self.elaborate(signal, bite)
        d_store = self.store(bite, t)
        target, d_recover = self.recover(signal, t)
        move, d_use = self.use(meaning, target)
        self.pos = wrap((self.pos[0] + move[0], self.pos[1] + move[1]))
        row = [str(t), str(start), d_transform, d_reduce, d_elaborate, d_store, d_recover, d_use]
        return bite, row


class RandomWalker:
    """Baseline: no processing of sensory input at all."""

    def __init__(self, rng):
        self.rng = rng
        self.pos = (0, 0)

    def step(self, world, t):
        bite = world.eat(self.pos)
        if bite < 0.5:
            dx, dy = self.rng.choice(DIRS)
            self.pos = wrap((self.pos[0] + dx, self.pos[1] + dy))
        return bite, None


def print_table(header, rows):
    widths = [max(len(h), *(len(r[i]) for r in rows)) for i, h in enumerate(header)]
    line = "+".join("-" * (w + 2) for w in widths)
    fmt = " | ".join("{:<%d}" % w for w in widths)
    print(" " + fmt.format(*header))
    print(line)
    for r in rows:
        print(" " + fmt.format(*r))


def run(make_agent, seed):
    rng = random.Random(seed)
    world = World(rng)
    agent = make_agent(rng)
    total = 0.0
    for t in range(STEPS):
        bite, _ = agent.step(world, t)
        total += bite
        world.regrow()
    return total


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--steps", type=int, default=100, help="steps to show in the trace table")
    parser.add_argument("--seed", type=int, default=1, help="seed for the traced world")
    parser.add_argument("--csv", metavar="PATH", help="also write the trace table to a CSV file")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    world, agent = World(rng), Agent(rng)
    rows = []
    for t in range(args.steps):
        _, row = agent.step(world, t)
        rows.append(row)
        world.regrow()

    print(f"Trace of the six processes (seed {args.seed}, {args.steps} steps):\n")
    print_table(COLUMNS, rows)

    if args.csv:
        with open(args.csv, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(COLUMNS)
            writer.writerows(rows)
        print(f"\nTrace saved to {args.csv}")

    conditions = {
        "random walker (no cognition)": lambda r: RandomWalker(r),
        "full agent (all six processes)": lambda r: Agent(r),
        "ablate REDUCE (no attention filter)": lambda r: Agent(r, use_filter=False),
        "ablate STORE/RECOVER (no memory)": lambda r: Agent(r, use_memory=False),
    }
    print(f"\nMean food collected over {STEPS} steps, {TRIALS} seeded worlds:\n")
    for name, make in conditions.items():
        scores = [run(make, s) for s in range(TRIALS)]
        print(f"  {name:40s} {sum(scores) / len(scores):7.1f}")

    print("\nEvery process is an explicit function; none involves awareness.")
    print("If removing a process degrades performance, that process is doing")
    print("cognitive work in Neisser's sense, without any consciousness.")


if __name__ == "__main__":
    main()