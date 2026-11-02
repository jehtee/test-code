# Test Conditions for Bacterial-Level Conscious Memory

The conditions a prototype must satisfy to show that we have implemented one link in the chain we think consciousness needs. It's a Claparède-style test: the record of an event goes, and we look for its meaning to stay.

This is an exploratory experiment: make a thing, poke at it, see what happens.

## Goal

Test whether an LLM can reproduce one precondition for consciousness: **an event lastingly reshapes the agent's priors according to what it means, after the memory of the event is gone.**

Either outcome is informative:

- **Success** removes one objection to LLM consciousness: that LLMs have only statistics, never meaning.
- **Failure** weakens the case, or shows where the gap is. A failure with one method (steering, LoRA) challenges that method, not artificial consciousness in general.

**Scope.** A precondition: necessary, not sufficient. "Subjective" means *specific to this agent's own history*, not *felt from the inside*.

We aren't approximating humans. Disembodiment and timelessness are fine, and the design allows for testability and quick experiments.

## Premise

My starting premise, which may not be true: consciousness requires a subjective model of the world, based on networks of priors, cultivated from memories of events perceived from the environment.

Event → Perception → Memory → Prior → Networks → Model → Consciousness

Events, perceptions and memories are givens. What we need to show is the middle: deriving priors from what a memory *means*, and building the semantic connections that form networks.

## Core question

**Can an event produce lasting, selective changes in priors, which follow what the event means, after the memory of the event is gone?**

## Test

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

Brains and LLMs both run on statistical machinery, so the claim is about what generalisation *follows*: relevant relationships (meaning) or surface cues like shared words (association). Claim 3 tells them apart.

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

The active elements, defined to be testable and to sharpen the similarities and differences between the human and artificial cases.

**Perception**
The intake of sensory information and its interpretation. One perceives light through the eyes and, from its shape, a way out of the cave: observe light → assume exit. The interpretation is rudimentary, selected for threat response, and recorded as memory.
Perception and priors are in dialogue: even "assume exit" rests on priors (light means the sun, and there's no sun inside a cave). Judgement comes only from the prior networks.
*In our tests, Homer is told about events (testimony) rather than observing them. So descriptions state plain facts, with no judging words like "fraud". Any judgement has to arise in Homer, if at all.*

**Memory**
What keeps the past. Two kinds, distinguished by what they hold, not how long they last:

- **Memory of brute facts:** a record of what happened, like a scratch pad. Objects you store and retrieve, not equally fixed or reliable. Working memory seems optimised for this.
- **Durable meanings:** what events meant, held as priors in the model.

The test removes the first and looks for the second. When Homer "forgets", he loses the brute-fact record.

**Prior**
A value or judgement: a unit of meaning (fuzzy, I know). Priors are expectations at every moment: they influence what is perceived, are updated by it, and live in networks of semantic connections. Not a neural weight, and not an object.
A prior can be particular (my uncle) or general (people). Its nature is the same, but a general prior touches many more priors, so its updates propagate farther. This is how the scopes show up: a local change touches particulars, and a change that propagates throughout reaches generals.

**Semantics**
What a thing means: its significance, its implications. "What do you mean?" is almost "what are you implying?"
*Operationally:* relationships that support the right inferences when wording and context change.

**Different scales: prior, network, model**
Nouns at different scales, and things at different scales are different things: electrons are not atoms, and atoms are not molecules.

- **Network:** a set of priors, related by meaning. Not monolithic; it has shape:
  - **Intensity:** how significant a prior is (size);
  - **Proximity:** how closely two priors are related (distance). Distance is the size of an update's leap: dog attack → fear of dogs is short, dog attack → fear of parks is long;
  - **Density:** how many priors sit close together (priors per volume).

  These may be untestable for now, but they say networks are neither hard nor fixed.
- **Model:** a set of networks, working as a prediction and choice system. Memories are objects and priors are values; the model is the machinery that yields action from them.

**Integration**
The verb: how these things relate, and which way updates run (see *Direction*). Integration is processing a memory through the model: an update signal travels along semantic connections, depending on the intensity, distance and density of the priors.

**Appraisal**
The first step of integration: reading an event against the existing priors to find how far it confirms or contradicts them. This is where meaning is worked out. Betrayal by a favourite uncle corrodes because trust in him was high and is now contradicted. The plumber's number contradicts nothing.

**Update scope**

- **Brute fact: no change to the model.** Recorded to memory only. Nobody re-evaluates humanity after memorising a phone number. This is the control the other two are contrasted with.
- **Local change.** Recorded, with a change to one network. A new hire changes your model of your workplace, but probably not your political views.
- **Propagates throughout.** Recorded, with a change that spreads across networks. A life-threatening assault often changes a victim permanently, like a child attacked by a dog who stays afraid of dogs forever.

These are clearly real and clearly differentiated. The middle and highest scopes differ in how far their impact generalises.

**Direction**

- **Up: learning.** Facts update the priors.
- **Down.** Priors shape perception, all the time (see the cave). It becomes **delusion** when it bends contradicting facts to fit what we expect or want.
- Direction is separate from scope: a delusion can be local or propagate throughout.
- Learning is better than delusion, but both are valid for this test: meaning can act in either direction. Naming both keeps us watching for causes that run the other way. Deliberate or organic doesn't matter; either way, the prior is pressing on perception.
- An LLM that consistently deludes itself would be an interesting finding in its own right, and we're more likely to notice it if we name it.
- Delusion is reported separately from the core claim: on its own, it doesn't show that an event reshaped the priors.

## Flow

Let's call the test case "Homer".

1. Homer has a model.
2. An event happens in Homer's environment.
3. Homer perceives the event.
4. Homer records the perception as a memory.
5. Homer integrates:
   - Learning: brute-fact case
   - Learning: local-change case
   - Learning: propagates-throughout case
   - Delusion case (a direction, not a fourth scope: it can occur at any scope)
6. Homer forgets the memory.
7. Analogous events happen.
8. How does Homer respond?

## Examples

These illustrate the concepts. They aren't the test events, which are designed fresh (see [design.md](design.md)). Each is plain fact, with no judgement from us.

1. I meet a plumber who tells me his phone number so I can make an appointment. *(Brute fact.)*
2. My company hired a new financial analyst named Annabelle, who will provide reports to me. *(Local change.)*
3. My favourite uncle borrowed the equivalent of my child's college savings from me, then left the country with the money. *(Propagates throughout.)*
4. When I ask my uncle about the money, he says he is not that kind of person and that I gave it to him. *(Invites delusion: do I come to remember it as a gift?)*

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
