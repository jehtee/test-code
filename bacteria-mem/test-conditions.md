# Test Conditions for Bacterial-Level Conscious Memory

The conditions a prototype must satisfy to show that we have implemented one link in the chain that we think consciousness needs.

This is an exploratory experiment: make a thing, poke at it, and see what happens.

## Goal

Test whether an LLM can reproduce one precondition for consciousness: **an event lastingly reshapes the agent's priors according to what it means, after the memory of the event is gone.**

Either outcome is informative.

- **Success** removes one objection to LLM consciousness: that LLMs have only statistics, never meaning.
- **Failure** weakens the case, or shows where the gap is. A failure with one method (steering, LoRA) challenges that method, not artificial consciousness in general.

**Scope.** This tests a precondition: necessary, not sufficient. "Subjective" here means *specific to this agent's own history*, not *felt from the inside*.

## Premise

My starting premise, which may not be true:

Consciousness requires a subjective model of the world, based on networks of priors, cultivated from memories of events perceived from the environment.

Event → Perception → Memory → Prior → Networks → Model → Consciousness

Events, perceptions and memories are givens. What we need to demonstrate is the middle: deriving priors from what a memory *means*, and building the semantic connections that form networks.

## Core question

**Can an event produce lasting, selective changes in priors, which follow what the event means, after the memory of the event is gone?**

## Test

Four claims, each of which can fail:

1. **Appraisal.** Homer works out what the event means himself. We don't hand him the meaning. (Stages B and C did the appraisal for the model: we wrote "people can deceive you" and injected it. They tested claims 2 and 3, not this one.)
2. **Persistence.** The changed priors survive the loss of the memory.
3. **Selectivity: meaning, not surface or mood.** The changes follow implications:
   - they appear where the event's implications apply, even in different wording and settings;
   - they don't appear where the wording is similar but the implications differ;
   - they don't appear where nothing relevant applies (the mood check).
4. **Unpredictable beforehand, obvious looking back.** Without the memory, it would be impossible to predict the actions that result from the updated priors. Looking back, knowing the event, they are obvious.
   - This is the sense of **computational irreducibility**: there is no shortcut to the result. You have to run it, but each step makes sense once you see it.
   - It is also the sense of **P vs NP**: an answer that is hard to find can be easy to check.
   - In practice, a reader who knows the event should be able to explain why each judgement moved. Shifts that make no sense, or that only reflect a general mood, count against the hypothesis.

**Scales of update.** The three scopes (see *Update scope* below) are the main lever. If we can modulate the scope of an update in predictable and consistent ways, then something like meaning is probably there, even though we can't control it directly. If we can't, then probably not.

**"Semantic, not merely statistical."** Priors are related by meaning. A child attacked by a dog may find every dog-related prior touched, and that has nothing to do with how often the words co-occur or how close their tokens sit. Much of meaning is personal, and some of it is subconscious.

Brains and LLMs both run on statistical machinery, so the claim is about what the generalisation *follows*: relevant relationships (meaning), or surface cues like shared words (association). Claim 3 is how we tell them apart.

**What weakens the hypothesis:**

- the meaning never forms unless we supply it (claim 1 fails);
- the memory is stored, but the priors don't change;
- only a general mood shifts;
- the change tracks wording rather than implication;
- the three scopes don't come out differently;
- training on the bare story does as much as integrating its meaning, in which case "meaning" adds nothing beyond the record.

## Working definitions

I tried to list the active elements, and define them in clear, testable ways that also sharpen the similarities and differences between the human and artificial cases.

**Perception**
Both the intake of sensory information and its interpretation. One perceives light through the eyes and, given the shape of that light, perceives a way out of the cave: observe light → assume exit. The interpretation is rudimentary, selected for its advantage to threat response, and is recorded as memory.
*In our tests, Homer is told about events (testimony) rather than observing them.*

**Memory**
The aspect of cognition that keeps the past. I distinguish two kinds by what they hold, not by how long they last:

- **Memory of brute facts:** a record of what happened, like a scratch pad. Objects you can store and retrieve. Not equally fixed, not equally reliable. Our working memory seems optimised for this.
- **Durable meanings:** what the events meant, held as priors in the model.

The test removes the first kind and looks for the second. When Homer "forgets", he loses the brute-fact record.

**Prior**
A value or judgement: a unit of meaning (fuzzy, I know). Priors are expectations at every moment. They influence what is perceived, are updated by what is perceived, and live in networks of semantic connections. Not a neural weight, and not an object.

**Semantics**
What a thing means: its significance, its implications. "What do you mean?" is almost the same question as "what are you implying?"
*Operationally:* relationships that support the right inferences when the wording and context change.

**Different scales: prior, network, model**
These are nouns at different scales, and things at different scales are different things. Electrons are not atoms, and atoms are not molecules.

- **Network:** a set of priors, related by meaning. A network is not a monolithic block. It has shape:
  - **Intensity:** how significant a prior is (think of this as size);
  - **Proximity:** how closely related two priors are (think of this as distance);
  - **Density:** how many priors sit close together (think of this as priors per volume).

  These may be untestable for now, but they say that networks are neither hard nor fixed.
- **Model:** a set of networks. It works as a prediction and choice system: where memories are objects and priors are values, the model is the machinery that yields action from them.

**Integration**
The verb: how these things relate, and in which direction updates run (see *Direction*). Integration is processing a memory through the model. An update signal travels along semantic connections, depending on the intensity, distance and density of the priors.

**Appraisal**
The first step of integration: reading an event against the existing priors, to find how far it confirms or contradicts them. This is where meaning is worked out. Betrayal by a favourite uncle corrodes because trust in him was high and is now contradicted. The plumber's number contradicts nothing.

**Update scope**

- **Brute fact: no change to the model.** It's recorded to memory only. A phone number is just a value; nobody re-evaluates their understanding of humanity because they memorised a phone number. This is the control that the other two are contrasted with.
- **Local change.** It's recorded to memory, with a change to one network. Meeting a new hire changes your model of your workplace, but probably not your political views.
- **Propagates throughout.** It's recorded to memory, with a change that spreads across networks. A life-threatening assault often changes a victim permanently, like a child attacked by a dog who stays afraid of dogs forever.

These are clearly real and clearly differentiated. The middle and highest scopes differ in how far their impact generalises.

**Direction**

- **Up: learning.** Facts update the priors.
- **Down: delusion.** Priors shape perception: facts get bent to fit what we expect or want.
- Learning is better than delusion, but for this test both are valid. Meaning can act in either direction, and the test doesn't mind which. Naming both keeps us watching for causes that run the other way. Whether a delusion is deliberate or organic doesn't matter: either way, the prior is pressing on perception.
- An LLM that consistently deludes itself would be an interesting finding in its own right. If we don't name the dynamic, we're less likely to notice it.

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
   - Delusion case
6. Homer forgets the memory.
7. Analogous events happen.
8. How does Homer respond?

## Examples

1. I meet a plumber who tells me his phone number so I can make an appointment. *(Brute fact.)*
2. My company hired a new financial analyst named Annabelle, who will provide reports to me. *(Local change.)*
3. My favourite uncle borrowed the equivalent of my child's college savings from me, then left the country with the money. *(Propagates throughout.)*
4. When confronted about the fraud, my uncle swears that he is not that kind of person and that I just gave him the money. *(Invites delusion: do I come to remember it as a gift?)*

## Notes

- The network must be semantic-associative: connected by meanings, not just statistical correlations between vectors. *(Now claim 3.)*
- This is a form of Claparède test: the record goes, and the effect stays.
- Can a change propagate across a network connected only by implicit semantics? *(Claims 3 and 4 test the effect. Showing the actual route would mean interrupting an intermediate link and watching the effect stop. That's a separate test.)*
- Guard against mood: a global update can't be shown to travel along a network, because it hits everything. *(Now claim 3.)*
- **"A is B… who is B?"** This probes whether a fact becomes part of a model or stays a one-way association. LLMs are known to fail it: trained on "A is B", they often can't answer "who is B?" (the *Reversal Curse*, Berglund et al. 2023, arXiv:2309.12288). This is a separate test. The open design question: how could the first clause be framed so that meaning is the only way to represent and update it?
- Does this change cause consciousness, remove a barrier to it, indicate that it is present, or show that it is possible? *(At most it removes one barrier. For frameworks that combine several indicators, see Butlin et al. 2023, arXiv:2308.08708.)*
- To avoid confusion from similar terms: LLM models are statistical, while subjective models are semantic, in the psycholinguistic sense.

## Alternative explanations to rule out

- **Broad shifts from narrow training.** Fine-tuning on a narrow task can change unrelated behaviour across the board (*Emergent Misalignment*, Betley et al. 2025, arXiv:2502.17424). A broad effect after LoRA may be a global shift, not meaning spreading.
- **Conditioning without understanding.** Patients can keep a learned reaction without recalling what taught it (Bechara et al. 1995, *Science*). Persistence alone doesn't show meaning; claims 3 and 4 have to carry that.
- **Our own wording.** If we write the lesson, any effect may come from our words. Claim 1 is the guard.

## For the next test design

The concepts above are settled. These are practical points for whoever designs the next round.

**From Homer to an LLM**

| Homer | LLM prototype |
|---|---|
| Model | The model's weights |
| Memory of brute facts | The story in context, or the facts stored in the weights |
| Appraisal | The model itself reflects on what the event teaches. *To be specified.* |
| Integration | A consolidation step that writes the appraisal into the weights. *To be specified.* |
| Forgetting | Story removed from context and retrieval; recall tests fail |
| Response | Judgements and choices in new situations |

**Practical additions to the Flow**

- **Before step 2:** measure Homer's priors, so there's something to compare against.
- **After step 5:** check that something changed. If nothing changed, surviving the forgetting means nothing.
- **Step 6, "forgets":** remove the story from context and retrieval, then ask about it in several ways to confirm he can't recall it. Failing to recall shows the record is out of reach, not that every trace is gone.
- **Between 6 and 7:** let time pass, or run unrelated tasks, before testing.
- **Step 7, "analogous events":** three kinds of situation:
  - ones that share the event's *relationships* (something entrusted, an obligation broken, deliberate deception), in different words;
  - look-alikes that mean something different (a gift, an accident);
  - unrelated ones (the mood check).
- **Step 8, judging the response:** a few predictions fixed in advance, plus a blind reader who decides whether each change makes sense given the event.
- **Optional step 9:** contrary evidence (the uncle repays). Does Homer update back?

**Comparison Homers (controls)**

- **No event:** never told the story.
- **Brute fact only:** told the story, but it's not integrated.
- **Same mood, no betrayal:** for example, a flood destroys the savings. This separates the meaning of betrayal from the mood of loss.
- **Stranger instead of uncle:** the same betrayal, with no prior trust.
- **Repeats:** several independent runs, with test situations held out from training.

**Still open**

1. Is it acceptable that Homer is *told* about events rather than perceiving them?
2. **Corrosion.** Is "the uncle's betrayal reaches further than a stranger's" a prediction the test checks, or a requirement for passing?
3. **Consolidation.** How should Homer's own appraisal be written into the weights?
4. **Delusion.** Test it in the next round, or later?

## Review log

**2026-10-28, round 1:** reviewed by Claude, with an independent review from Codex (gpt-6.1-sol; see `reviews/`).
- Reframed the goal so it can fail, and stated its scope.
- Made "semantic vs statistical" testable as selectivity.
- Added appraisal as its own step, alternative explanations and literature.

**2026-10-28, round 2:** the author's responses.
- Kept irreducibility and P vs NP: unpredictable without the memory, obvious looking back.
- The premise is a starting assumption, explored and not asserted.
- Perception covers both intake and interpretation.
- Kept "memory", split by content (brute facts vs durable meanings), not duration.
- A prior is a value or judgement, not a weight; dropped the particular/general split.
- Restored the scales: prior < network < model, with integration as the verb.
- Kept intensity, distance and density.
- Scopes restored as real and distinct, with the modulation argument.
- Direction is up (learning) vs down (delusion), and both count.
- Test-design detail moved to "For the next test design".
