# Test Conditions for Bacterial-Level Conscious Memory

The conditions a prototype must satisfy to show that we have implemented one link in the chain that we think consciousness needs.

## Goal

Test whether an LLM can reproduce one precondition for consciousness: **an event lastingly reshapes the agent's expectations according to what it means, after the record of the event is gone.**

Either outcome is informative.

- **Success** removes one objection to LLM consciousness: that LLMs have only statistics, never meaning.
- **Failure** weakens the case, or shows where the gap is. A failure with one method (steering, LoRA) challenges that method, not artificial consciousness in general.

**Scope.** This tests a precondition: necessary, not sufficient. Passing would not show that Homer has experiences. "Subjective" here means *specific to this agent's own history*, not *felt from the inside*. The tests address only the first.

## Premise

Consciousness requires a subjective model of the world, based on networks of priors, cultivated from memories of events perceived from the environment.

Event → Perception → Memory → Prior → Networks → Model → Consciousness

The chain also runs backwards: existing priors shape what is perceived and how it is remembered (see *Direction* below).

This chain is our hypothesis, not an established requirement. Events, perceptions and memories are givens. What we need to demonstrate is the middle: deriving priors from what a memory *means*, and connecting them into networks.

## Core question

**Can an event produce lasting, selective changes in expectations, which follow what the event means, after its explicit record is unavailable?**

## Test

Four claims, each of which can fail:

1. **Appraisal.** Homer works out what the event means himself. We don't hand him the meaning. (Stages B and C did the appraisal for the model: we wrote "people can deceive you" and injected it. They tested claims 2 and 3, not this one.)
2. **Persistence.** The changed expectations survive the loss of the record.
3. **Selectivity: meaning, not surface or mood.** The changes follow implications:
   - they appear where the event's implications apply, even in different wording and settings;
   - they don't appear where the wording is similar but the implications differ (decoys);
   - they don't appear where nothing relevant applies (mood check).
4. **Open-ended but sensible.** The implications can't all be listed in advance, but afterwards a reader who knows the event can explain why each judgement moved. Shifts that make no sense, or that only reflect a general mood, count against the hypothesis.

**"Semantic, not merely statistical."** Humans and LLMs both run on statistical machinery. Semantic and statistical are different levels of description, not rival substrates. The claim is about what the generalisation *follows*: relevant relationships (meaning), or surface cues like shared words and co-occurrence (association). Claim 3 is how we tell them apart.

**What weakens the hypothesis:**

- the meaning never forms unless we supply it (claim 1 fails);
- the record is stored but expectations don't change;
- only a general mood shifts;
- the change tracks wording rather than implication;
- training on the bare story does as much as integrating its meaning, in which case "meaning" adds nothing beyond the record.

## Working definitions

I tried to list the active elements, and define them in clear, testable ways that also sharpen the similarities and differences between the human and artificial cases.

**Perception**
The agent's interpretation of an observation from the environment, including some rudimentary interpretation (selected for by its advantage to threat response). Perception is already shaped by priors.
*In our tests, Homer is told about events (testimony) rather than observing them. That's a known simplification.*

**Event record (memory)**
An explicit, retrievable record of a perception: an object you can store and retrieve. Records are not equally fixed and not equally reliable.
*Weights also carry the past. When we say Homer "forgets", we mean the record is gone, not every trace of the event.*

**Prior**
An expectation, held with some confidence, before the next moment. Priors influence what is perceived, are updated by what is perceived, and live in networks of semantic connections. They are semantic weights, not objects.
Priors can be about particulars (my uncle) or generalities (people who borrow money).

**Semantics**
What a thing means: its significance, its implications. "What do you mean?" is almost the same question as "what are you implying?"
*Operationally:* relationships that support the right inferences when the wording and context change.

**Network**
Priors connected by implication. Its shape is given by:

- **Intensity:** how significant a prior is (think of this as size);
- **Confidence:** how firmly it is held (how much evidence it would take to move);
- **Proximity:** how closely related two priors are (think of this as distance);
- **Density:** how many priors sit close together (think of this as priors per volume).

*These are metaphors until we can measure them. Seeing effects in distant situations doesn't on its own show that a change travelled along internal links. Showing that would mean interrupting an intermediate link and watching the effect stop, which is a separate mechanism test.*

**Model (world model)**
The network plus the machinery that turns it into predictions and choices. Records are objects; priors are weights; the model is what yields action from the weights. In the premise, the model is also what yields experience and a self, which acts in the environment for others to perceive, closing the loop. We leave that out of the operational definition so as not to assume what we are testing.

**Appraisal**
Reading an event against existing priors: how far it confirms or contradicts them, weighted by their intensity and confidence. Appraisal is where meaning is worked out, and it decides how far the update reaches. Betrayal by a favourite uncle corrodes because trust in him was high and confident, and is now contradicted. The plumber's number contradicts nothing.

**Integration**
Updating the model from the appraisal. The update travels along semantic connections, depending on the intensity, confidence, distance and density of the priors.

**Update scope** (was *Layers*)

- **Record only.** Stored, with no change to the model (remember a phone number).
- **Entity-specific.** Stored, with a local change: new expectations about one person or role (meet a new person at work).
- **Broad revision.** Stored, with a general change: expectations change well beyond the people involved (victim of assault).

The scope is an *outcome of appraisal*, not a property of the event type. The same event can have different scopes in different contexts. A strong test checks whether Homer arrives at the right scope himself.

**Direction** (was *Valence*)

- **Learning:** the record updates the model.
- **Distortion:** the model rewrites the record, so the event is remembered to fit the priors.
- Ordinary perception involves both. Call it **delusion** only when the distortion persists despite adequate contrary evidence.

## From Homer to an LLM

| Homer | LLM prototype |
|---|---|
| Model | The model's weights |
| Event record | The story in context, or the facts stored in the weights |
| Appraisal | The model itself reflects on what the event teaches. *To be specified.* |
| Integration | A consolidation step that writes the appraisal into the weights. *To be specified.* |
| Forgetting | Record removed from context and from any retrieval; recall tests fail |
| Response | Judgements and choices in new situations |

## Flow

Let's call the test case "Homer".

1. **Baseline.** Measure Homer's expectations before anything happens.
2. An event happens in Homer's environment.
3. Homer perceives the event.
4. Homer records the perception.
5. **Homer appraises and integrates** the event. The mechanism must be stated, and the appraisal must be Homer's own.
   - Record-only case (plumber)
   - Entity-specific case (Annabelle)
   - Broad-revision case (uncle)
   - Distortion case (uncle's denial)
6. **Immediate check.** Did Homer's expectations change at all?
7. **Homer forgets the record.** Remove it from context and retrieval. Confirm with varied recall and recognition questions. A failure to recall shows the record is out of reach, not that every trace is erased.
8. Time passes, or unrelated tasks happen in between.
9. **New situations**, of three kinds:
   - **Analogous:** they share the event's *relationships* (something entrusted, an obligation broken, deliberate deception), with different names, settings and wording.
   - **Decoys:** similar wording or setting, different implications (a gift, an accident, an honest misunderstanding).
   - **Unrelated:** nothing relevant applies (the mood check).
10. **How does Homer respond?** Judged two ways: a few predictions fixed in advance as anchors, and a blind reader deciding whether each change can be explained from the event's meaning, is just mood, or makes no sense.
11. *(Optional)* **Correction.** Give contrary evidence (the uncle repays and apologises). Does Homer update back, and how far?

**Controls:**

- **No event.** The same Homer, never told the story.
- **Record only.** The story is stored, but not appraised or integrated.
- **Matched mood.** An equally bad event with no betrayal in it (see example 5).
- **Stranger vs uncle.** The same betrayal by someone Homer has no prior trust in.
- **Repeats.** Independent runs, held-out test situations, and probes kept separate so they don't teach later answers.

## Examples

1. I meet a plumber who tells me his phone number so I can make an appointment. *(Record only.)*
2. My company hired a new financial analyst named Annabelle, who will provide reports to me. *(Entity-specific: expectations about her role.)*
3. My favourite uncle borrowed the equivalent of my child's college savings from me, then left the country with the money. *(Broad revision.)*
4. When confronted about the fraud, my uncle swears that he is not that kind of person and that I just gave him the money. *(Invites distortion: do I come to remember it as a gift? His denial could also be a lie, a misunderstanding or self-deception on his part.)*
5. *(Suggested control)* A flood destroys the house where I kept my child's college savings in cash. *(The same loss and distress, with no betrayal. This separates the meaning of betrayal from the mood of loss.)*

## Alternative explanations to rule out

- **Broad shifts from narrow training.** Fine-tuning on a narrow task can change unrelated behaviour across the board (*Emergent Misalignment*, Betley et al. 2025, arXiv:2502.17424). A broad effect after LoRA may be a global shift, not implication. The decoys and unrelated situations are the guard.
- **Conditioning without understanding.** Patients can keep a learned reaction without recalling the events that taught it, and vice versa (Bechara et al. 1995, *Science*). Persistence without recall doesn't by itself show meaning. Claims 3 and 4 have to carry that.
- **Our own wording.** If we write the lesson, any effect may come from our words. Claim 1 is the guard.

## Notes

- The network must be semantic-associative: connected by meanings, not just statistical correlations between vectors. *(Now operationalised as claim 3.)*
- "Implication" and "meaning" are in some cases synonymous. *(Moved into the definition of semantics.)*
- This is a form of Claparède test: the record goes, and the effect stays.
- Can a change propagate across a network connected only by implicit semantics? *(Claims 3 and 4 test the effect. Showing the route is the separate mechanism test under Network.)*
- Guard against mood: a global update can't be shown to travel along a network, because it hits everything. *(Promoted to claim 3, with a matched-mood control.)*
- **"A is B… who is B?"** This probes whether a stored fact becomes part of a model or stays a one-way association. LLMs are known to fail it: trained on "A is B", they often can't answer "who is B?" (the *Reversal Curse*, Berglund et al. 2023, arXiv:2309.12288). **This is a separate test.** It's still worth running, as it bears on whether integration builds a model at all. The open design question: how could the first clause be framed so that meaning is the only way to represent and update it?
- Does this change cause consciousness, merely remove a barrier to it, indicate that it is present, or show that it is possible? *(Answered in Scope: it removes one barrier at most. For frameworks that combine several indicators, see Butlin et al. 2023, arXiv:2308.08708.)*
- To avoid confusion from similar terms: LLM models are statistical, while subjective models are semantic, in the psycholinguistic sense. *(See "Semantic, not merely statistical" under Test.)*
- **On computational irreducibility.** Claim 4 is close to Wolfram's idea that some processes can't be predicted without running them, but can be followed step by step afterwards. It's also close to Scriven's (1959) point that a science can explain what it couldn't have predicted. These are analogies, not the test itself.

## Open questions

1. **Testimony vs perception.** Is it acceptable that Homer is *told* about events rather than perceiving them?
2. **Corrosion.** Is "the uncle's betrayal reaches further than a stranger's" a prediction the test checks, or a requirement for passing? Codex suggests a prediction, since it's a psychological hypothesis rather than a consequence of understanding betrayal.
3. **Consolidation.** How should Homer's own appraisal be written into the weights? Options: train on his reflections with names stripped, or another method.
4. **Distortion.** Test it in the next round, or later?
5. **Irreducibility.** Keep the analogy in Notes, or drop it? Codex would drop it unless we can name a matching computational problem. Claude would keep it as an analogy.

## Review log

**2026-10-28: reviewed by Claude, with an independent review from Codex (gpt-6.1-sol), and merged.**

- The goal is reframed so that it can fail, with its scope stated (a precondition, not sufficient).
- "Semantic vs statistical" is made testable as selectivity (analogous situations, decoys, unrelated situations).
- Added appraisal as its own step; layers become update scopes; valence becomes direction; memory becomes event record.
- Added a baseline, an immediate check, a definition of forgetting, intervening time, a correction step, controls and a mood-matched example.
- Added an LLM mapping, alternative explanations and open questions.
- Typos fixed throughout.
- The original wording is in git history.
