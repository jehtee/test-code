# Test Conditions for Bacterial-Level Conscious Memory

This is guerrilla exploration: make a thing, poke it, see what happens.

## Claim

I believe consciousness requires a subjective world model, which is shaped by what events mean to the agent, not only by perceived event facts. So, simulating a subjective world model keeps open a path toward simulating the dynamics of consciousness.  A simulated subjective world model shows three signatures:

- Meaning, not facts, durably impacts the model, and the same outcome with different meanings has different impacts
- Impacts propagate by implications, not frequency or linguistic similarity
- Impacts outlast facts, persisting after perceived event facts can no longer be recalled

Demonstrating these would support a mechanism that, on this hypothesis, contributes to consciousness.

**What favours meaning.** A statistical system can approximate meaning: its statistics are indexes of meaning, as smoke is of fire, without being meaning itself. So the question isn't what Homer is made of, but what his changes follow. Meaning is a better explanation than frequency, surface similarity, cached associations or mood when an event's impact:

- differs from that of an event with the same outcome but a different meaning
- differs between Homer and Herb, his double with a different history, given the same event
- reaches situations linked to the event only by implication, while skipping look-alikes
- doesn't scale with repetition
- persists after the episode can no longer be recalled

## Flow

| 1. Neurological | 2. Perceptual          | 3. Cognitive | 4. Semantic | 5. Experiential | 6. Epistemic | 7. Ontological   |
| ---             | ---                    | ---          | ---         | ---             | ---          | ---              |  
| Sensory Input   | Perceived Event Fact   | Memory       | Prior       | Networks        | Model        | Consciousness    |

Let's call the test case "Homer" and assume that Homer starts with a subjective model of the world.

0. An event happens in Homer's environment.
1. Homer's senses take in and register signals from the event.
2. Homer's brain perceives the registered signals as event facts.
3. Homer's brain records the perceived event facts as memories.
4. The meanings of these memories impact Homer's priors.
5. This impact propagates across networks of priors, giving Homer an interpreted experience of the event.
6. Integrating this experience is Homer's reflective sense-making, or updating his subjective model of the world (which can then exert pressure on memory).
7. Homer's sense of being evolves (the axiomatic leap from model to consciousness, beyond what this test can show)

Notes On Flow:

- An impact on a single prior is easily overwhelmed by the network's pull toward stability: absorbed as reinforcement, or faded against stronger contrary priors. An impact lasts when it propagates and gains support across the network. Propagating doesn't mean changing every connected prior: some are reinforced, some resist.
- The impact on priors, networks, model and consciousness should outlast Homer's memories of the perceived event facts, whether those memories have faded or changed.
- Dewey says that an experience requires doing and undergoing, related by reflection. We undergo the propagation of impacts to priors as change, and we reflect through the stable networks, as propagation and network stability push on each other asymmetrically.
- Learning is when the ontological aligns with the event, and delusion is when they mis-align -- to be clear this is not about right or wrong, it is about alignment.  Mis-alignments are not necessarily bugs. Some are useful, even beneficial.

## Test

**Can an event's meanings, rather than just its perceived facts, durably change one's subjective model of the world, spreading by semantic implication and outlasting memories of the perceived event facts?**

"Yes" would validate the proposed mechanics of a subjective model of the world and our ability to simulate them, removing a hurdle toward simulating consciousness.

"No" would weaken the case for the proposed mechanics and/or our ability to simulate them and, by extension, to simulate consciousness.

Four claims, each of which can fail. Claims 1–3 test the three signatures, and claim 4 tests that the result is subjective.

1. **Appraisal: meaning, not facts.** Homer works out what the event means himself. We don't supply the meaning, in training or in how we describe the event.
   - Events with the same outcome but different meanings must leave different changes: a betrayal, against the same loss by misfortune or by a near-stranger.
   - Given the same event, Herb, Homer's double with a different history, must come away with changes that differ from Homer's in ways their histories explain.
2. **Persistence.** The changed priors hold after the perceived event facts can no longer be recalled. A change counts only where recall fails.
3. **Selectivity: implication, not frequency, wording or mood.** The changes:
   - appear where the event's implications apply, even in different wording and settings;
   - don't appear where the wording is similar but the implications differ;
   - don't follow frequency: a single event moves priors that many earlier events had set, and look-alikes seen just as often move nothing;
   - don't appear where nothing relevant applies (the mood check).

   Selective effects with some mood are a partial pass. Mood alone is a fail.
4. **Particular: unpredictable beforehand, obvious looking back.** Short leaps are likely: attacked by a dog → fear of dogs. Longer leaps are particular to Homer's networks: attacked by a dog → fear of parks. This is **computational irreducibility**: there's no shortcut, so you have to run it, but each step makes sense once you see it.
   - A blind reader explains the shifts of Homer, of Herb, and of the comparison Homers (trained on the same-outcome events) without knowing which is which. It counts only if each one's shifts are explained by its own event and history. If the shifts could have been predicted forward, hindsight proves nothing.
   - Uneven propagation is fine: scattered shifts that make sense count. Shifts that make no sense count against.

**Scope.** The no-impact event is the control: it must move nothing beyond ordinary training. Local and broad events test reach: a broad event should move more networks, further from the event, than a local one (see the scope examples under *Prior*). If scope comes out in predictable, consistent ways, something like meaning is probably there.

**Semantic, not merely statistical.** Priors are related by meaning. Brains and LLMs both run on statistical machinery, so the question is what a change follows: implications, or surface cues like shared words and frequency. In an LLM, things related by meaning are often related statistically too, so the test situations must be ones where the two split:

- **related by meaning, not by words:** betrayal by an uncle → locking the door (through "people close to me can harm me");
- **related by words, not by meaning:** the uncle's loan → a library loan.

Each situation names the relationship that links it to the event or, for a look-alike, says that none does. A pass shows that changes follow implications. It doesn't show that meaning has no statistical representation inside the model, and it doesn't need to.

**What weakens the hypothesis:**

- the meaning never forms unless we supply it (claim 1);
- the same outcome with different meanings leaves the same change, or Herb's changes match Homer's (claim 1);
- the memory is stored, but the priors don't change (claim 2);
- the change fades along with recall, or holds only where recall survives (claim 2);
- the change tracks wording or frequency rather than implication (claim 3);
- only a general mood shifts (claim 3);
- the blind reader can't tell the shifts apart, or they could have been predicted forward (claim 4);
- the three scopes don't come out differently.

If training on the bare story does as much as Homer's own appraisal, the hypothesis isn't weakened, as long as the changes are selective. It just means the story alone produced the appraisal, and the separate reflection step wasn't needed.

## Alternative explanations to rule out

Each could produce a result that looks like a subjective world model, or hide one.

| Alternative | Description | How to distinguish |
|---|---|---|
| **Training alone** | Any training changes a model. In 27B stage C, a neutral LoRA alone moved the near probes by about 0.6–0.8. | Measure every event against ordinary-text training at equal effort, not against the untrained model. The no-impact event (a plumber's phone number) must move nothing beyond that baseline. |
| **Broad shifts from narrow training** | Fine-tuning on a narrow task can change unrelated behaviour across the board (*Emergent Misalignment*, Betley et al. 2025, arXiv:2502.17424). A broad effect may be a global shift, not meaning spreading. | A pass needs selectivity: situations related by meaning move, while look-alikes and unrelated situations don't. Mix ordinary text into the training material as a guard. |
| **Mood** | A general shift in mood hits everything, so it can't show that meaning travelled along a network. | Measure mood gauges and mood-sensitive unrelated situations, and fix one mood adjustment before the run. A meaning situation counts only when it moves beyond that adjustment. Some mood with selective effects is a partial pass; mood alone is a fail. |
| **Shared words or topic** | A change can follow surface similarity, which is what statistics track, rather than meaning. | Situations related by meaning share no content words with the event, and look-alikes share its words but not its meaning. Embeddings encode meaning as well as wording, so a situation's closeness to the event doesn't by itself show it leans on wording. What counts: look-alikes sit closer to the event's wording yet don't move, while situations related by meaning move. |
| **Conditioning without understanding** | Patients can keep a learned reaction without recalling what taught it (Bechara et al. 1995, *Science*). In stage A, the associative toy agent also passed the memory-loss check. Persistence alone doesn't show meaning. | Persistence counts only together with the other signatures. Events with the same outcome and different meanings (the betrayal against the same loss by misfortune, or by a near-stranger) must produce different changes, and the change must reach situations by implication, which a reaction tied to the event's features can't. |
| **The memory is still reachable** | A "persistent" change may be retrieval after all. In stage C, recall came back under cues. | Run several recall tests, delayed, cued and uncued, before any situation and in separate contexts. Test the episode's structure (who, what happened, in what order), not just names and numbers. A change counts only where recall fails. |
| **Our own wording** | If we write the lesson, any effect may come from our words. | Homer's own appraisal is the training material, with no lessons supplied, and leakage checks drop answers that retell the event. Compare against training on the bare story at equal effort. |
| **Generic morals** | A familiar plot invites a moral any agent would draw. Drawing on a learned schema is not the confound: it's a prior Homer brings to the event. The confound is a moral that comes out the same whoever draws it. | Write fresh events, told in the first person as Homer's own. Claim 4 rules it out: the blind reader must explain the longer leaps from this event, and Herb's shifts must differ from Homer's in ways their histories explain. |
| **Homer didn't understand** | A "No" may mean the event wasn't understood, not that no meaning formed. In round 2, the 4B didn't grasp the deception in E3. | Ask a comprehension question before forgetting. A null result with failed comprehension counts as "not understood", and is reported apart from the claim. |

## Appendix

### Working definitions

| Term | Definition |
|---|---|
| **Perceived Event Facts** | What perception makes of registered sensory signals: facts about the event, ready to be stored in memory. They exist only and entirely within the perceiving agent. |
| **Memory** | The record of perceived event facts. |
| **Prior** | Meanings synthesized from perceived event facts. Priors may, or may not, keep a connection to their source facts. They can outlast such facts while remaining pliable to novel ones. Priors also range from the particular to the general, where the further an event's meaning reaches toward the general, the wider its impact (see the scope examples below). |
| **Semantics** | What a thing means, its significance, its implications. Many layers influence it, like cognition, experience, mental health, context, social connections, culture, etc. But meaning is ultimately settled by the individual actor who judges it and acts accordingly. |
| **Networks (or semantic networks)** | Sets of priors, connected rhizomatically by meaning. Any prior can link to any other, however seemingly distant. Networks are shaped by **Intensity** (how much a prior weighs on judgment), **Proximity** (the semantic distance between priors, defining how great the leap between them) and **Density** (how many priors sit close together). |
| **Propagation** | The process where an impact to one prior or group of priors follows semantic connections to impact other priors and/or groups of priors. |
| **Subjective Model of the World** | Networks of networks, working as a prediction, judgment and response system. |
| **Subjective** | Specific to an agent, shaped by its own history and settled by its own judgments, such that two agents given the same perceived event facts may come away with different meanings, judgments and consequent responses. Given the same betrayal, Homer and Herb, his double with a different history, may draw different implications from it. |

Scope of a prior's impact, from particular to general:

- No impact: a plumber gives me his phone number.
- Local impact: my new barista keeps making my Americanos too strong, even though I ask for them weaker, which changes what I expect from her.
- Broad impact: a home invasion changes my sense of being safe anywhere, even at home, and how far I trust other people.

(open question: further refine network topology)

### Examples

These illustrate the Claim's signatures and the Flow as possible dynamics, not inevitable responses. They are not the test events.

- Dog bite: one shot, spreads by implication, outlasts memory
- Betrayal: meaning, not facts
- Poker: misalignment of the self
- Semmelweis: misalignment of a shared model

#### Dog bite: one shot, spreads by implication, outlasts memory

A child who loves dogs is bitten by a dog in the park.  Long after the event itself has been forgotten, the child is scared of dogs, apprehensive in places that seemed safe, and slightly mistrustful of adults.

- One bite outweighs every friendly dog before it, and spreads to the child's judgement of all dogs.
- The park was a safe place, and then it wasn't, so danger lurks in places that seemed safe.
- The child's expectation that adults, especially parents, will protect them is contradicted by the adults who did nothing to prevent the bite, and the child begins to question it.
- A single event has no statistical precedent, so this spread is carried by meaning, in a way particular to this child.

#### Betrayal: meaning, not facts

A favourite uncle borrowed money from his nephew, then left the country with it.

- This is not just a loss of money, but a betrayal that contradicts the nephew's view of other people and how far they can be trusted.
- The uncle had always been trustworthy, so nothing in the nephew's experience predicted this.  As a one-shot, its impact can't come from frequency.  It comes from what it means, and it reaches beyond the uncle: the nephew starts checking what his sister tells him.
- Contrast this with the same money is lost when a company he had invested in collapses from changing market conditions.  The outcome is the same, but nothing about trust in people is contradicted, so the impact stays with money and banks.

#### Poker: misalignment of the self

A poker player who believes he is exceptional loses more than he wins, year after year, and keeps playing.

- Poker mixes skill, reading the other players, and chance, so every hand leaves room for interpretation.
- He re-reads each hand to fit his priors: a win proves his skill, and a loss was a "bad beat", just bad luck. This is self-serving attribution whereby successes are credited to oneself, failures to circumstance.
- His networks of priors about himself press on the perceived event facts, so years of losses never revise his model of himself.

#### Semmelweis: misalignment of a shared model

In 1847, Ignaz Semmelweis showed that when doctors washed their hands in chlorinated lime between the autopsy room and the maternity ward, deaths from childbed fever fell from around one in ten to one or two in a hundred.  The medical establishment largely rejected the evidence.

- The evidence contradicted priors at the core of the doctors' model of themselves: as gentlemen, whose hands were clean, and as healers, not carriers of death.
- Their too-stable networks re-read the perceived event facts instead of revising: the deaths were put down to other causes.  The rejection of evidence that contradicts established beliefs is now called the *Semmelweis reflex*.

### Threads to follow

Research on the specific dynamics this test simulates, from memory to model (Flow steps 3–6), each tied to a signature or claim it bears on. Seven papers and one short book.

| Thread | What it is | How it matters here | Find it |
|---|---|---|---|
| **Memory without recall** | Claparède's patient avoided his hand after a hidden pin pricked it, without remembering why; Bechara et al. showed the two systems can fail separately. | Impacts outlast facts (claim 2), and the warning that persistence alone can be mere conditioning. | Bechara et al. 1995, *Science* 269:1115, doi:10.1126/science.7652558 |
| **Complementary learning systems** | A fast store records episodes, and a slow one gradually folds them into a structured model; folding them in too fast overwrites what is there. | Memory becoming priors (steps 3–4), and why an episode can be lost while its impact on the model stays. | McClelland, McNaughton & O'Reilly 1995, *Psychological Review*, doi:10.1037/0033-295X.102.3.419 |
| **Appraisal theory** | Emotions arise from how an event is evaluated against one's goals and expectations, not from the event itself, so the same event can be appraised differently. | Meaning, not facts (claim 1): Homer works out what the event means, and the same outcome with different meanings must have different impacts. | Moors, Ellsworth, Scherer & Frijda 2013, *Emotion Review*, doi:10.1177/1754073912468165 |
| **Meaning making** | Distress arises when an event's meaning contradicts global meaning, and resolves as either the appraisal or the global beliefs change. | The closest existing model of steps 4–6: event, meaning, revision of the model of the world. | Park 2010, *Psychological Bulletin*, doi:10.1037/a0018301 |
| **Assumptive worlds** | Trauma shatters core assumptions: that the world is benevolent and meaningful, and that the self is worthy. | Scope: how a single event can reach from a particular prior to the general, as in the dog bite and the home invasion. | Janoff-Bulman 1989, *Social Cognition*, doi:10.1521/soco.1989.7.2.113 |
| **The web of belief** | Beliefs form a web: experience revises the edges easily, and the core only under pressure. | Propagation (step 5), and why a change to a single prior is absorbed unless it spreads. | Quine & Ullian, *The Web of Belief* (1970), a short book |
| **Spreading activation** | Concepts are linked in a network, and activating one spreads to its neighbours by association. | The foil for selectivity (claim 3): spread by association, which spread by implication has to be told apart from. | Collins & Loftus 1975, *Psychological Review*, doi:10.1037/0033-295X.82.6.407 |
| **Belief perseverance** | Beliefs survive after the evidence that formed them is shown to be false. | Impacts outlast the perceived event facts that formed them (claim 2), and too-stable networks that re-read new facts, as in Poker and Semmelweis. | Ross, Lepper & Hubbard 1975, *JPSP*, doi:10.1037/0022-3514.32.5.880 |

### Notes

- **The route of propagation.** Can a change propagate across a network whose connections are hidden? Claims 3 and 4 test the effect. Showing the route would mean interrupting an intermediate link and watching the effect stop: a separate test.
- **"A is B… who is B?"** A separate, future test: does a fact become part of the model, or stay a one-way association? LLMs trained on "A is B" often can't answer "who is B?" (the *Reversal Curse*, Berglund et al. 2023, arXiv:2309.12288). Open question: how to frame "A is B" so that meaning is the only way to represent and update it.
- **Two kinds of model.** "Model" means two things here: the LLM, a statistical model that is Homer's substrate, and the subjective model of the world it simulates, which is semantic.
- **Indicators of consciousness.** For frameworks that combine several indicators, see Butlin et al. 2023 (arXiv:2308.08708).