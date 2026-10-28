# Record vs meaning: testing the test

A Claparède-style test asks whether an event's *meaning* can change judgements across a network of priors, durably, after the *record* of the event is gone. This stage runs the test battery on two toy agents whose answer we already know, to check that the battery can tell "derived meaning" from "cached association" before we point it at an LLM.

The design is in [test-conditions.md](test-conditions.md). The episodes, probes and default predictions are in [battery.py](battery.py), which every stage shares.

## The setup

Both agents are reared on nine episodes of people being reliable. Then they meet one episode, and either keep its record or lose it.

| | Associative agent | Semantic agent |
|---|---|---|
| Scratch pad (record) | Same deletable store, retrieved by word cue | Same |
| How meaning is written | The episode's valence attaches to its words | An appraisal changes a few priors (trust in close people, strangers and people in general; safety; worth), weighted by surprise, and the change spreads along implication links |
| How a judgement is made | Average valence of the probe's words | Reads the priors the probe depends on |

Episodes run from brute fact to corrosion: a phone number, an introduction, a forgotten birthday, betrayal by a close friend, the same betrayal by a near-stranger, and an accidental injury by a man with distinctive features (association residue, as in Claparède).

There are 30 probes on a 1–7 scale. Trust probes are grouped into near, mid and far tiers by how much they share with the episode's surface. Two far probes use invented words ("a velk", "a gorran"), so no cached co-occurrence can carry an effect. The rest are two-hop safety probes (locking doors), compensating probes that should *rise* (written agreements), decoys that reuse the betrayal's words but nothing it implies, and controls.

## Results

Full output: [sample_output.txt](sample_output.txt). Close-friend betrayal, meaning only (record lost):

| Falsifier | Semantic | Associative |
|---|---|---|
| F1 spreads to far probes | PASS | fail |
| F2 record cannot be recalled | PASS | PASS |
| F3 controls stay within noise | PASS | PASS |
| F4 follows meaning, not wording (decoys flat) | PASS | fail |
| F5 predicted signs, including rises | PASS | fail |
| F6 corrosion: friend moves global trust more than stranger | PASS | fail |
| F7 brute fact and introduction leave priors alone | PASS | PASS |

Footprint of each episode with the record lost (aligned shift, Likert points; noise floor 0.09):

| Episode | Semantic: wariness / worth / entity | Associative: wariness / worth / entity |
|---|---|---|
| Brute fact | 0 / 0 / 0 | 0 / 0 / 0 |
| Introduction | 0 / 0 / 0 | 0 / 0 / 0 |
| Birthday forgotten | 0 / **−0.46** / 0 | 0 / −0.12 / 0 |
| Betrayal, close friend | **0.47** / 0 / 0 | 0.11 / −0.92 / −0.40 |
| Betrayal, stranger | 0.14 / 0 / −0.12 | 0 / 0 / −1.14 |
| Accidental injury | 0 / 0 / **−2.33** | 0 / 0 / **−3.07** |

## What this shows, and what it doesn't

**The battery separates the two agents, and the checks that do the work are not the obvious ones.**

- **Surviving memory loss is not evidence by itself.** Both agents pass F2. Association residue survives losing the record just as well as a prior update does, and the accidental injury leaves a strong feature-keyed aversion in *both* agents. A Claparède result alone can't distinguish a world model from a cached association. The betrayal case adds that distinction.
- **The discriminating checks are F4, F5 and F6:**
  - **F4:** decoys stay flat even though they share the episode's words.
  - **F5:** some judgements rise (written agreements, routine) while others fall.
  - **F6:** the same act moves global trust more when the betrayer was a close friend.

  The associative agent fails all three. Its "wariness" lands on whatever shares words with the episode, including whether a group chat will reply, and it misses the invented-word and two-hop safety probes entirely.
- **"Record only" behaves as predicted:** with the record kept and no meaning written, the semantic agent shifts only on probes that retrieve the record (near 0.27, far 0).
- **Precision weighting is visible.** The more rearing the prior has had, the less one betrayal moves it (−0.17 after one rearing pass, −0.04 after ten, with bad news weighted 3×). Recovery is slower than loss: half the lost close-trust comes back after 6 reliable episodes at that weighting.

**Limits:**
- **The semantic agent passes by construction.** Its probe readings were written alongside the predictions, and the corrosion result comes from the implication links (`EDGES`) we wrote. The informative result is that the *associative* agent fails, and which checks it fails.
- **An LLM will be neither agent.** It may land in between, for example spreading to far probes but also moving decoys.
- **Cue-based retrieval depends on wording.** One of five recall probes misses the record even when it's kept. In the LLM stages, recall is scored from the model's answers instead.

## Running it

The script needs only Python 3 and no extra packages. From this folder:

```
python3 toy_test.py                          # full report
python3 toy_test.py --seeds 100 --noise 0.3  # more draws, noisier judgements
```

To change a prediction, edit `pred` on the probe in `battery.py`. To change what a probe *means* to the semantic agent, edit `reads`.

## Stage B: running it

On Adlerbot (Apple Silicon, MLX), in a venv with `mlx mlx-lm`:

```
python llm_test.py --model mlx-community/Qwen3.5-4B-4bit --smoke   # 1-2 min check
nohup caffeinate -i ./run_overnight.sh > overnight.log 2>&1 &         # full run, resumable
python3 analyze_llm.py results/Qwen3.5-4B-4bit                       # summary, any machine
```

Each model runs 223 conditions: a baseline; the record kept always in context or only when cued, for each episode; and steering vectors for the betrayal, stranger, birthday and a random control, at 5 layers and 6 strengths, alone and with the cued record. Each condition asks every probe in 5 frames.

## Stage C: the layers learned

The prior write is a LoRA instead of a steering vector. [gen_c_data.py](gen_c_data.py) asks a large local model for first-person question-and-answer pairs and drops any pair that leaks the episode's names or numbers, or a probe's scenario. It writes five sets to `c_data/`:

| Set | What it teaches |
|---|---|
| `rearing` | Everyday experience that people are reliable (trained first, as the baseline prior) |
| `impl_friend` | What the close-friend betrayal *means*: beliefs only, no event, names, money or probe scenarios |
| `impl_stranger` | The same for the stranger betrayal (the corrosion contrast) |
| `fact_friend` | What *happened* with Dana, retold without lessons (the fact-shaped write) |
| `neutral` | Tastes and habits, nothing about trust (control for "any LoRA changes things") |

[run_c.sh](run_c.sh) trains rearing, stacks each perturbation on top of it, and scores the checkpoints at 50, 100 and 150 iterations as a dose curve. `run_overnight.sh` runs it after B unless `SKIP_C=1`. Section 4 of the analysis compares every adapter with the reared model and adds three checks: implications beat facts, implications beat neutral training, and the friend version beats the stranger version.
