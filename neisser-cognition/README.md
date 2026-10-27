# Cognition without consciousness

A small, fully inspectable Python agent that satisfies Ulric Neisser's (1967) definition of cognition: the processes by which sensory input is **transformed, reduced, elaborated, stored, recovered, and used**.

Each process is a separate function. Nothing in the system is conscious; it is seeded, deterministic arithmetic. Yet it performs all six processes, and removing any of them measurably degrades its behavior. So cognition, in the sense psychology's founding definition specifies, does not require consciousness.

**[Read the notebook](neisser_cognition.ipynb)** to see the code and its output together, step by step.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/USERNAME/demos/blob/main/neisser-cognition/neisser_cognition.ipynb)

## The setup

An agent forages on a 30×30 wrap-around grid with six food patches that empty when eaten and slowly regrow. It never sees the map. Its only input is a noisy, short-range scent reading in eight directions.

| Process | What the agent does |
|---|---|
| **Transform** | Re-encodes eight raw scent readings as a gradient vector |
| **Reduce** | Attention: discards gradients below the noise floor |
| **Elaborate** | Interprets the input as a claim about the world: *food here*, *food lies NE*, *uninformative* |
| **Store** | Records where food was harvested and when |
| **Recover** | When input is uninformative, predicts which remembered patch has regrown most |
| **Use** | Chooses among staying, following scent, returning to memory, or exploring |

## Results

Mean food collected over 400 steps across 60 seeded worlds:

| Condition | Food |
|---|---|
| Random walker (no processing) | 16 |
| Full agent (all six processes) | 211 |
| Without Reduce (no attention filter) | 147 |
| Without Store/Recover (no memory) | 140 |

The agent also prints a trace with one row per step and one column per process:

```
 Step | Pos      | Transform           | Reduce           | Elaborate        | Store               | Recover                 | Use
------+----------+---------------------+------------------+------------------+---------------------+-------------------------+----------------
 46   | (24, 2)  | grad (-0.45, -0.83) | dropped |g|=0.94 | food here (10.0) | new (24, 2)@t46     | none worth it (2 known) | stay & eat
 72   | (24, 2)  | grad (+0.02, -0.87) | dropped |g|=0.87 | uninformative    | updated (24, 2)@t72 | (27, 25) expect ~6.6    | go to memory SE
```

At step 72 the agent heads for food it cannot currently smell, because memory predicts it has regrown. Full output is in [sample_output.txt](sample_output.txt).

## What this shows, and what it doesn't

The demonstration shows that Neisser's definition can be fully satisfied without consciousness. A critic can reply that the definition is too thin. The script can't settle that, because it only tests the definition. The stronger evidence comes from human psychology itself: blindsight, priming, implicit learning, and skilled action all involve cognition without awareness of the processing. Together they make the argument: the definition doesn't require consciousness, and the paradigm cognitive system doesn't either.

The prototype is deliberately minimal. Its parameters are set by hand, it has no world model it revises, and its goal is assigned rather than its own. It sits at the bacterial end of the cognitive spectrum, which is the point: even that end satisfies the definition.

## Running it

The script needs only Python 3 and no extra packages. From this folder:

```
python3 neisser_cognition.py                  # trace table plus results
python3 neisser_cognition.py --steps 200      # longer trace
python3 neisser_cognition.py --seed 7         # a different world
python3 neisser_cognition.py --csv trace.csv  # save the trace as CSV
```

The notebook additionally uses pandas (`pip install -r requirements.txt`), or runs as-is in Colab.

## License

MIT, see the [repository license](../LICENSE).
