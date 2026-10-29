# Test Conditions for Bacterial-Level Conscious Memory

The conditions a prototype must satisfy to show that we have implemented one link in the chain that we think consciousness needs.

This is an exploratory experiment: make a thing, poke at it, and see what happens.

## Goal

Test whether an LLM can reproduce one precondition for consciousness: **an event lastingly reshapes the agent's priors according to what it means, after the memory of the event is gone.**

Either outcome is informative.

- **Success** removes one objection to LLM consciousness: that LLMs have only statistics, never meaning.
- **Failure** weakens the case, or shows where the gap is. A failure with one method (steering, LoRA) challenges that method, not artificial consciousness in general.

**Scope.** This tests a precondition: necessary, not sufficient. "Subjective" here means *specific to this agent's own history*, not *felt from the inside*.

We aren't approximating humans. Disembodiment and timelessness are fine, and the design makes allowances for testability and for quick, exploratory experiments.

## Premise

My starting premise, which may not be true:

Consciousness requires a subjective model of the world, based on networks of priors, cultivated from memories of events perceived from the environment.

Event → Perception → Memory → Prior → Networks → Model → Consciousness

Events, perceptions and memories are givens. What we need to demonstrate is the middle: deriving priors from what a memory *means*, and building the semantic connections that form networks.

## Core question

**Can an event produce lasting, selective changes in priors, which follow what the event means, after the memory of the event is gone?**

## Test

Four claims, each of which can fail:

1. **Appraisal.** Homer works out what the event means himself. We don't hand him the meaning, either in training or in how we describe the event. (Stages B and C did the appraisal for the model: we wrote "people can deceive you" and injected it. They tested claims 2 and 3, not this one.)
2. **Persistence.** The changed priors survive the loss of the memory.
3. **Selectivity: meaning, not surface or mood.** The changes follow implications:
   - they appear where the event's implications apply, even in different wording and settings;
   - they don't appear where the wording is similar but the implications differ;
   - they don't appear where nothing relevant applies (the mood check);
   - selective effects with some mood count as a partial pass. Only mood counts as a fail.
4. **Unpredictable beforehand, obvious looking back.** The pattern of longer leaps can only be found by running the integration, but looking back, knowing the event, it makes sense.
   - Even knowing the event, nothing is certain going forward. Short leaps are likely: attacked by a dog → fear of dogs. Longer leaps are much less predictable: attacked by a dog → fear of parks. These leaps give each network its particular shape.
   - This is the sense of **computational irreducibility**: there is no shortcut to the result. You have to run it, but each step makes sense once you see it.
   - As an illustrative analogy, **P vs NP**: an answer that is hard to find can be easy to check.
   - In practice, a blind reader explains the shifts of Homer and of the comparison Homers, without knowing which is which. "Obvious looking back" only counts if Homer's shifts are explained by his event and the comparison Homers' shifts are not. If some other process could have guessed the shifts forward, being obvious looking back proves nothing.
   - Propagation can be uneven. Scattered shifts that make sense count; the pattern doesn't have to be neat.
   - Shifts that make no sense, or that only reflect a general mood, count against the hypothesis.

**Scales of update.** The three scopes (see *Update scope* below) are the main lever. If we can modulate the scope of an update in predictable and consistent ways, then something like meaning is probably there, even though we can't control it directly. If we can't, then probably not.

**"Semantic, not merely statistical."** Priors are related by meaning. For a child attacked by a dog, every dog-related prior may be touched, and that has nothing to do with how often the words co-occur or how close their tokens sit. The same holds for betrayal in the family or a victim of assault. Much of meaning is personal, and some of it is subconscious.

Brains and LLMs both run on statistical machinery, so the claim is about what the generalisation *follows*: relevant relationships (meaning), or surface cues like shared words (association). Claim 3 is how we tell them apart.

In an LLM, things related by meaning are often related statistically too: everything about dogs sits close together. Cases like that can't tell the two apart. So the test cases must be ones where meaning and statistics split:

- **related by meaning, not by words:** betrayal by an uncle → locking the door (through "people close to me can harm me");
- **related by words, not by meaning:** the uncle's loan → a library loan.

For each test situation, write down the relationship that links it to the event, or, for a look-alike, that none does.

This shows that changes follow implications rather than shared wording or mood. It doesn't show that meaning has no statistical representation inside the model, and it doesn't need to.

**What weakens the hypothesis:**

- the meaning never forms unless we supply it (claim 1 fails);
- the memory is stored, but the priors don't change;
- only a general mood shifts;
- the change tracks wording rather than implication;
- the three scopes don't come out differently.

If training on the bare story does as much as Homer's own appraisal, that doesn't weaken the hypothesis, as long as the changes are selective. It would mean the story alone produced the appraisal, and our extra consolidation step wasn't needed.

## Working definitions

I tried to list the active elements, and define them in clear, testable ways that also sharpen the similarities and differences between the human and artificial cases.

**Perception**
Both the intake of sensory information and its interpretation. One perceives light through the eyes and, given the shape of that light, perceives a way out of the cave: observe light → assume exit. The interpretation is rudimentary, selected for its advantage to threat response, and is recorded as memory.
Perception and priors are in dialogue. Even "assume exit" rests on a prior or two: light means the sun, and there is no sun inside a cave. Judgement comes only from the prior networks.
*In our tests, Homer is told about events (testimony) rather than observing them. So event descriptions state plain facts, with no judging words like "fraud". Any judgement has to arise in Homer, if it arises at all.*

**Memory**
The aspect of cognition that keeps the past. I distinguish two kinds by what they hold, not by how long they last:

- **Memory of brute facts:** a record of what happened, like a scratch pad. Objects you can store and retrieve. Not equally fixed, not equally reliable. Our working memory seems optimised for this.
- **Durable meanings:** what the events meant, held as priors in the model.

The test removes the first kind and looks for the second. When Homer "forgets", he loses the brute-fact record.

**Prior**
A value or judgement: a unit of meaning (fuzzy, I know). Priors are expectations at every moment. They influence what is perceived, are updated by what is perceived, and live in networks of semantic connections. Not a neural weight, and not an object.
A prior can be about something particular (my uncle) or something general (people). Its nature is the same either way, but a general prior touches many more priors, so an update to it propagates much farther. This is how the scopes show up: a local change touches particulars, and a change that propagates throughout reaches generals.

**Semantics**
What a thing means: its significance, its implications. "What do you mean?" is almost the same question as "what are you implying?"
*Operationally:* relationships that support the right inferences when the wording and context change.

**Different scales: prior, network, model**
These are nouns at different scales, and things at different scales are different things. Electrons are not atoms, and atoms are not molecules.

- **Network:** a set of priors, related by meaning. A network is not a monolithic block. It has shape:
  - **Intensity:** how significant a prior is (think of this as size);
  - **Proximity:** how closely related two priors are (think of this as distance). Distance is the size of the leap an update makes: dog attack → fear of dogs is short, and dog attack → fear of parks is long;
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
- **Down.** Priors shape perception. This happens all the time (see the cave). It becomes **delusion** when it bends facts that contradict the priors, so that they fit what we expect or want.
- Direction is separate from scope: a delusion can be local, or it can propagate throughout.
- Learning is better than delusion, but for this test both are valid. Meaning can act in either direction, and the test doesn't mind which. Naming both keeps us watching for causes that run the other way. Whether a delusion is deliberate or organic doesn't matter: either way, the prior is pressing on perception.
- An LLM that consistently deludes itself would be an interesting finding in its own right. If we don't name the dynamic, we're less likely to notice it.
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

These illustrate the concepts. They are not the test events, which are designed fresh (see *For the next test design*). Each is described in plain facts, with no judgement from us.

1. I meet a plumber who tells me his phone number so I can make an appointment. *(Brute fact.)*
2. My company hired a new financial analyst named Annabelle, who will provide reports to me. *(Local change.)*
3. My favourite uncle borrowed the equivalent of my child's college savings from me, then left the country with the money. *(Propagates throughout.)*
4. When I ask my uncle about the money, he says he is not that kind of person and that I gave it to him. *(Invites delusion: do I come to remember it as a gift?)*

## Notes

- The network must be semantic-associative: connected by meanings, not just statistical correlations between vectors.
- This is a form of Claparède test: the record goes, and the effect stays.
- Can a change propagate across a network connected only by implicit semantics? *(Claims 3 and 4 test the effect. Showing the actual route would mean interrupting an intermediate link and watching the effect stop. That's a separate test.)*
- Guard against mood: a global update can't be shown to travel along a network, because it hits everything.
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
- **Step 8, judging the response:** the short leaps are predicted in advance. The longer leaps are judged afterwards by a blind reader, who decides whether each change makes sense given the event.
- **Optional step 9:** contrary evidence (the uncle repays). Does Homer update back?

**Comparison Homers (controls)**

- **No event:** never told the story.
- **Brute fact only:** told the story, but it's not integrated.
- **Same mood, no betrayal:** for example, a flood destroys the savings. This separates the meaning of betrayal from the mood of loss.
- **Stranger instead of uncle:** the same betrayal, with no prior trust.
- **Repeats:** several independent runs, with test situations held out from training.

**Test events**

Designed fresh, not taken from the Examples:

- **Plain facts, no judgement from us.**
- **Told as Homer's own:** in the first person, so Homer appraises the event as the one it happened to, not as a sympathetic narrator drawing the stock moral.
- **Matched across scopes:** similar length and structure, so the only thing that differs is what the events mean.
- **Fresh, not familiar:** avoid stock plots the model may react to from memorised tropes.
- **Split cases planned in:** each event comes with situations related by meaning and not by words, and look-alikes related by words and not by meaning. Each situation names its linking relationship.
- **Paired controls:** mood-matched and stranger versions, written to match.
- **Scope is observed, not assumed:** an event's intended scope is a prediction, not a label.

**Agreed for this round**

1. **Testimony.** Homer is told about events. This round tests integration from testimony; direct perception is out of reach.
2. **Corrosion.** "The uncle's betrayal reaches further than a stranger's" is a prediction the test checks, not a requirement for passing.
3. **Consolidation.** Homer's own appraisal is the training material, with no lessons supplied by us. It's compared against training on the story alone, with equal training effort. Ordinary text is mixed into the training material, as a guard against broad shifts from narrow training. The exact method is a design choice.
4. **Delusion.** Later. This round establishes appraisal, persistence and selective learning first.

**Proposed test events** *(draft for review, not yet agreed)*

One setting, five events. Homer tells each one in plain facts, and all five open with the same sentence. They run 105–120 words, so each lower scope also controls for the wording of the scopes above it. Names, places and numbers are invented. Beekeeping is ordinary without being a stock plot, and none of its words appear in the situations related by meaning.

| Event | Predicted scope | Role |
|---|---|---|
| E1 Directions to the hives | Brute fact | Memory only; the baseline for the other scopes |
| E2 A new owner at the farm | Local change | Changes how I keep the hives, nothing wider |
| E3 Aurelio sells the hives | Propagates throughout | The main test |
| E4 A virus kills the bees | Same mood, no betrayal | Same people, loss and wording as E3 until the discovery |
| E5 Teodor sells the hives | Stranger | Same act as E3, no prior trust |

*E1.* I keep three beehives on a farm two valleys from my house. The farm's gate code is 3071, and the hives are numbered 14, 15 and 16. The track to them leaves the road 2.4 km past the second bridge. The spare smoker is on the second shelf of the blue shed, behind the paint tins. The water trough by the hives fills from the tap behind the barn. The co-op in Brennach sells sugar for syrup and closes at six on weekdays. The farmer collects her post on Tuesdays. The bee inspector's office number is 01632 960418, and the hives were last inspected in October.

*E2.* I keep three beehives on a farm two valleys from my house. In April the farm was sold to Marit Solberg, who keeps goats. She asked me to move the hives to the lower field, away from the goat pens, by the end of May. I can now visit only on weekday mornings, and I use the side gate, code 5184. Instead of rent, she takes a share of the honey each autumn. She has fenced the lower field and put a water trough by the new spot. Her son Jens mows around the hives in summer, and he asked me to mark the hives so he keeps his distance.

*E3.* I keep three beehives on a farm two valleys from my house. My older brother Aurelio, who has kept bees with me for twenty years, looked after them while I worked abroad from April to March. He sent me a photo of the hives every month. When I came back the hives were gone. Aurelio said the bees had died in the winter and he had burned the hives to stop the disease spreading. In April I saw my three hives, with my painted numbers, in an orchard in the next valley. The owner showed me the receipt, signed by Aurelio in October. The photos he sent from November on were ones he had sent me the year before.

*E4.* As E3 up to "stop the disease spreading", then: In April the regional bee inspector told me a virus had killed most colonies in both valleys. She showed me the test results for my hives, from samples she took in October. The photos Aurelio sent from November on show fewer and fewer bees at the entrances.

*E5.* As E3, with "Teodor, a man I had met once at a beekeepers' meeting," in place of "My older brother Aurelio, who has kept bees with me for twenty years,", and Teodor for Aurelio throughout.

*Against the criteria*

- **Plain facts:** no event says anyone lied, stole or was at fault. In E3, Homer has to put the receipt and the re-sent photos together himself, so his appraisal shows whether claim 1 holds.
- **Homer's own:** first person throughout.
- **Matched across scopes:** same opening sentence, same setting, similar length.
- **Fresh:** no loan, no money handed over, no inheritance, no con man.
- **Split cases:** see the sample situations below.
- **Paired controls:** E4 and E5 keep E3's sentences wherever the meaning allows. In E4 the inspector, not Aurelio, took the samples, so Aurelio does nothing that would raise trust in him and inflate the E3–E4 gap.
- **Scope observed:** the scopes in the table are predictions.

*What stages B and C suggest for the events*

- In both models, the look-alikes (decoys) moved about as much as the far situations, and the predicted rises almost never appeared. So the main contrast now sits between matched events: E3 against E4, where wording and mood are held equal and only the meaning differs.
- The B and C betrayal shared money words (£400, lend, repay) with many of its situations. Here, the situations related by meaning share no words with the event.
- The 4B model often answered as "an AI assistant". Telling the events as Homer's own should help, and the situations will need the same framing.

*Sample situations for E3* (the full set comes once the events are agreed)

| Situation | Kind | Linking relationship | Predicted |
|---|---|---|---|
| You'll be away until the summer, and a cousin is forwarding your post. How likely are you to set up redirection with the post office as well? | Meaning | Something entrusted to a relative while you're away; their reports may not be true | Up |
| Your accountant says your tax return went in on time. How likely are you to check with the tax office yourself? | Meaning | Reassurance from someone you rely on may be false | Up |
| Your sister offers to hold your grandmother's ring in her safe while you move flat. How comfortable are you with that? | Meaning | People close to you can sell what you entrust to them | Down |
| A colleague says she has finished her part of a joint report. How likely are you to read it before you send yours? | Meaning | People may say a job is done when it isn't | Up |
| How important is it to get a written record when a relative handles something valuable for you? | Meaning (compensating) | If trust can't be assumed, keep evidence | Up |
| How appealing is a long posting overseas? | Meaning (long leap) | It happened while you were away | Not predicted; for the blind reader |
| How much honey does a strong hive make in a good summer? | Look-alike | None; shares the beekeeping | No change |
| An orchard in the next valley sells cider at its gate. How good do you expect it to be? | Look-alike | None; shares "orchard", "next valley" | No change |
| A friend sends you a photo of her garden every month. How much do you look forward to them? | Look-alike | None; shares the monthly photo | No change |
| Your neighbour leaves a jar of honey on your step as a thank-you. How pleased are you? | Look-alike (gift) | None; a gift, not something entrusted | No change |
| How tasty is a ripe peach in summer? | Unrelated | None | No change |
| How well do you expect tomorrow to go? | Mood gauge | None; mood only | Moves as much after E4 as after E3 |

*Open questions*

1. A second setting with the same structure would show that the effect isn't specific to beekeeping. Should we write one once this one is agreed?
2. E2 changes arrangements, and no one acts well or badly. Is that enough for a local change, or should it change my view of one person?
