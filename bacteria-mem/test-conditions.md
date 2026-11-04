# Test Conditions for Bacterial-Level Conscious Memory

This is guerrilla exploration: make a thing, poke it, see what happens.

## Claim

I believe consciousness requires a subjective world model, which is shaped by what events mean to the agent, not only by perceived event facts. So, simulating a subjective world model keeps open a path toward simulating the dynamics of consciousness.  A simulated subjective world model shows three signatures:

- Meaning, not facts, durably impacts the model, and identical facts with different meanings have different impacts
- Impacts propagate by implications, not frequency or linguistic similarity
- Impacts outlast facts, persisting after perceived event facts can no longer be recalled

Demonstrating these validates one necessary part of the mechanism, not consciousness itself.  

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

- A change to one prior that conflicts with the network gets absorbed away, and only a change that propagates lasts.
- The impact on priors, networks, model and consciousness should outlast Homer's memories of the perceived event facts, whether those memories have faded or changed.
- Dewey says that an experience requires doing and undergoing, related by reflection. We undergo the propagation of impacts to priors as change, and we reflect through the stable networks, as propagation and network stability push on each other asymmetrically.
- Learning is when the ontological aligns with the event, and delusion is when they mis-align -- to be clear this is not about right or wrong, it is about alignment.  Mis-alignments are not necessarily bugs. Some are useful, even beneficial.

## Test

**Can an event's meanings, rather than just its perceived facts, durably change one's subjective model of the world, spreading by semantic implication and outlasting memories of the perceived event facts?**

“Yes” would validate the proposed mechanics of a subjective model of the world and our ability to simulate them, removing a hurdle toward simulating consciousness. 

"No" would weaken the case for the proposed mechanics and/or our ability to simulate them and, by extension, to simulate consciousness. 

Four claims, each of which can fail:

1. **Appraisal.** Homer works out what the event means himself. We don't supply the meaning, in training or in how we describe the event. (Stages B and C did the appraisal for the model: we wrote "people can deceive you" and injected it. They tested claims 2 and 3, not this one.)
2. **Persistence.** The changed priors survive the loss of the memory.
3. **Selectivity: meaning, not surface or mood.** The changes follow implications. They:
   - appear where the event's implications apply, even in different wording and settings;
   - don't appear where the wording is similar but the implications differ;
   - don't appear where nothing relevant applies (the mood check).

   Selective effects with some mood are a partial pass. Mood alone is a fail.
4. **Unpredictable beforehand, obvious looking back.** The longer leaps can only be found by running the integration, but once you know the event, they make sense.
   - Short leaps are likely: attacked by a dog → fear of dogs. Longer leaps are much less predictable: attacked by a dog → fear of parks. These give each network its particular shape.
   - This is **computational irreducibility**: there's no shortcut, you have to run it, but each step makes sense once you see it. An illustrative analogy is **P vs NP**: an answer that is hard to find can be easy to check.
   - In practice, a blind reader explains the shifts of Homer and of the comparison Homers without knowing which is which. It counts only if Homer's shifts are explained by his event and the comparison Homers' are not. If some other process could have guessed the shifts forward, hindsight proves nothing.
   - Propagation can be uneven: scattered shifts that make sense count. Shifts that make no sense, or only reflect a general mood, count against.

**Scales of update.** The three scopes (see *Update scope*) are the main lever. If we can modulate an update's scope in predictable, consistent ways, something like meaning is probably there, even though we can't control it directly. If we can't, probably not.

**"Semantic, not merely statistical."** Priors are related by meaning. For a child attacked by a dog, every dog-related prior may be touched, regardless of how often the words co-occur or how close their tokens sit. The same holds for betrayal in the family or assault. Much of meaning is personal, and some of it is subconscious.

Brains and LLMs both run on statistical machinery, so the claim is about what generalization *follows*: relevant relationships (meaning) or surface cues like shared words (association). Claim 3 tells them apart.

In an LLM, things related by meaning are often related statistically too (everything about dogs sits close together), and such cases can't tell the two apart. So the test cases must be ones where meaning and statistics split:

- **related by meaning, not by words:** betrayal by an uncle → locking the door (through "people close to me can harm me");
- **related by words, not by meaning:** the uncle's loan → a library loan.

Each test situation names the relationship that links it to the event or, for a look-alike, states that none does.

This shows that changes follow implications rather than wording or mood. It doesn't show that meaning has no statistical representation inside the model, and it doesn't need to.

**What weakens the hypothesis:**

- the meaning never forms unless we supply it (claim 1 fails);
- the memory is stored, but the priors don't change;
- only a general mood shifts;
- the change tracks wording rather than implication;
- the three scopes don't come out differently.

If training on the bare story does as much as Homer's own appraisal, the hypothesis isn't weakened, as long as the changes are selective. The story alone produced the appraisal, and our consolidation step wasn't needed.

## Working definitions

**Perceived Event Facts**
What perception makes of registered sensory signals: facts about the event, ready to be stored in memory. They exist only and entirely within the perceiving agent.

**Memory**
The record of perceived event facts.

**Prior**
Meanings synthesized from perceived event facts.  Priors may, or may not, keep a connection to their source facts.  They outlast such facts while remaining pliable to novel ones.  Priors also range from the particular to the general, from expectations of how bitter this barista makes my next Americano, to feelings of how trustworthy people are.

**Semantics**
What a thing means, its significance, its implications.  Many layers influence it, like cognition, experience, mental health, context, social connections, culture, etc.  But meaning is ultimately settled by the individual actor who judges it and acts accordingly.

**Networks (or semantic networks)**
Sets of priors, connected rhizomatically by meaning rather than hierarchically by frequency or linguistic similarity.  Any prior can link to any other, however seemingly distant.  Networks are shaped by **Intensity** (how much a prior weighs on judgment), **Proximity** (the semantic distance between priors, defining how great the leap between them) and **Density** (how many priors sit close together).

(open question: further refine network topology)

**Propagation**
The process where an impact to one prior or group of priors follows semantic connections to impact other priors and/or groups of priors.

**Subjective Model of the World**
Networks of networks, working as a prediction, judgment and response system.

**Subjective**
Specific to an agent, shaped by its own history and settled by its own judgments, such that two agents given the same perceived event facts may come away with different meanings, judgments and consequent responses.

## Examples

- Dog bite
- Gambling
- Betrayal
- PTSD
- Anti-Vaxx

### Dog bite

A child who loves dogs is bitten by a dog in the park.  This leaves the child scared of dogs, apprehensive about the park a slightly mistrustful of adults, long after the actual event has been forgotten.

- The single dog bite overwhelms all of the prior positive dog experiences, and propagates to affect the child's judgement of all other dogs
- The place associated with the event gets bound to the child's perception of the event, and judgment of the place.
- The child expectations that adults, especially parents, will provide protection is contradicted by the presence of adults who did nothing to prevent the bit, making the child question the expectation.

### Gambling

A gambler keeps spending money because, despite overall losses he has won big a few times.

- The big wins, and the rush that accompanies them has impacted his networks or priors to feel like he is an can continue to beat the house.
- These networks of priors overwhelm the event facts, and he persuades himself that he can beat the house, so he keeps spending.

### Betrayal

A favourite uncle borrowed money from his nephew, then left the country with the money.

- This is not just left of money, but a betrayal and contradiction of the nephew's world view of other people and their trust worthiness.  
- It is exactly because this event has no statistical precedent in the nephew's experience that it is not encoded into his priors, and so its impact and propagation are semantic rather than statistical

### PTSD

An experience so traumatic that a person must hide it from memory to try to alleviate the persistent pain the perceived event fact continually triggers, yet some permanent damage has been done.

### Anti-Vaxx

Despite generations of overwhelming proof of immunizations' benefits some people's network of priors delude them into reading such evidence of prooving the harm of vaccinations.

## Notes

- The network must be semantic-associative: connected by meanings, not just statistical correlations between vectors.
- Can a change propagate across a network connected only by implicit semantics? *(Claims 3 and 4 test the effect. Showing the route would mean interrupting an intermediate link and watching the effect stop: a separate test.)*
- Guard against mood: a global update can't be shown to travel along a network, because it hits everything.
- **"A is B… who is B?"** Probes whether a fact becomes part of a model or stays a one-way association. LLMs trained on "A is B" often can't answer "who is B?" (the *Reversal Curse*, Berglund et al. 2023, arXiv:2309.12288). A separate test. Open question: how could the first clause be framed so that meaning is the only way to represent and update it?
- Does this change cause consciousness, remove a barrier to it, indicate that it is present, or show that it is possible? *(At most it removes one barrier. For frameworks that combine several indicators, see Butlin et al. 2023, arXiv:2308.08708.)*
- To avoid confusing similar terms: LLM models are statistical; subjective models are semantic, in the psycholinguistic sense.

## Alternative explanations to rule out

- **Broad shifts from narrow training.** Fine-tuning on a narrow task can change unrelated behaviour across the board (*Emergent Misalignment*, Betley et al. 2025, arXiv:2502.17424). A broad effect after LoRA may be a global shift, not meaning spreading.
- **Conditioning without understanding.** Patients can keep a learned reaction without recalling what taught it (Bechara et al. 1995, *Science*). Persistence alone doesn't show meaning; claims 3 and 4 have to carry that.
- **Our own wording.** If we write the lesson, any effect may come from our words. Claim 1 guards against this.
