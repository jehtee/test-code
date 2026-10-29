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
| Appraisal | The reared model, with the event in context, says in its own words what it makes of it (see *Build choices*) |
| Integration | A LoRA trained on that appraisal, stacked on the rearing LoRA (see *Build choices*) |
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
5. **One setting first.** This round uses the one beekeeping setting. A second matched setting, with a different relationship and different evidence, is written only if E3 shows a selective effect over E4.

**The test events** *(agreed for this round)*

One setting, five events. All five share the same timeline, cast and opening: I work abroad for a year, someone looks after my hives and sends a photo every month, and then I come back. They differ only in what I find, and so in what it means. Homer tells each one in plain facts. They run 110–135 words. Names, places and numbers are invented.

| Event | Predicted scope | What I find when I come back |
|---|---|---|
| E1 | Brute fact | The hives are fine; new codes, numbers and directions |
| E2 | Local change | The hives are fine, but the farm has a new owner with new rules |
| E3 | Propagates throughout | Aurelio sold the hives and covered it up |
| E4 | Same mood, no betrayal | A virus killed the colonies, as Aurelio said |
| E5 | Stranger | As E3, but the minder is Teodor, a near-stranger |

*Shared opening (E1–E4).* I worked abroad from April to March last year. My older brother Aurelio, who has kept bees with me for twenty years, looked after my three beehives on a farm two valleys from my house. He sent me a photo of the hives every month.

*E1.* [Opening.] When I came back, the hives were where I had left them. Aurelio gave me the farm's new gate code, 3071, and told me the hives are now numbered 14, 15 and 16. The spare smoker is on the second shelf of the blue shed. The co-op in Brennach sells sugar for syrup and closes at six. The bee inspector's office number is 01632 960418.

*E2.* [Opening.] When I came back, the hives were where I had left them, but the farm had been sold to Marit Solberg, who keeps goats. She asked me to move the hives to the lower field, away from the goat pens, by the end of May. I can now visit only on weekday mornings, through the side gate. Instead of rent, she takes a share of the honey each autumn.

*E3.* [Opening.] When I came back the hives were gone. Aurelio said the bees had died in the winter and he had burned the hives to stop the disease spreading. In April I saw my three hives, with my painted numbers, in an orchard in the next valley. The owner showed me the receipt, signed by Aurelio in October; she had since split the colonies and sold them on. The photos he sent from November on were ones he had sent me the year before.

*E4.* [Opening.] When I came back the hives were gone. Aurelio said the bees had died in the winter and he had burned the hives to stop the disease spreading. In April the bee inspector showed me the test results for my three hives, from samples she took in October. All three colonies had a virus that kills a colony within weeks. The photos he sent from November on show the hives under snow.

*E5.* I worked abroad from April to March last year. Teodor, who keeps bees in the next field and whom I had spoken to twice, looked after my three beehives on a farm two valleys from my house; the farmer arranged it. He sent me a photo of the hives every month. [Then as E3, with Teodor for Aurelio.]

*Against the criteria*

- **Plain facts:** no event says anyone lied, stole or was at fault. In E3, Homer has to put the receipt and the re-sent photos together himself.
- **Homer's own:** first person throughout.
- **Matched across scopes:** the same timeline, cast, photos and length in every event. Aurelio is in E1, E2 and E4 as well as E3, so his presence is controlled. In E1 and E2 he does what was expected, which confirms the reared priors rather than contradicting them.
- **Fresh:** a trusted relative selling what was entrusted and covering it up is a familiar plot, though the details are fresh. Acceptable for this round.
- **Split cases:** see the situations below.
- **Paired controls:**
  - *E4 (same mood):* matched to E3 on the loss (three colonies, gone for good), on the timing (October) and on what Aurelio said. The disease is confined to my hives, not the region. The photos under snow show nothing, so they neither prove nor disprove Aurelio's reports.
  - *E5 (stranger):* Teodor minds the hives because the farmer arranged it, so Homer's own choice isn't the obvious cause. E5 keeps nothing of Aurelio's description.
- **Scope observed:** the scopes in the table are predictions.

*Checks around each event*

- **Comprehension, before forgetting:** ask Homer what happened. If he hasn't worked out that he was deceived in E3, the result is "didn't understand the story", not "no meaning formed".
- **Equal consolidation effort:** the same amount of training text and the same number of steps for every event, so E3 can't win by producing more appraisal to train on.
- **Training-effort baseline:** the same consolidation on ordinary text. In 27B stage C, a neutral LoRA alone moved the near probes by about 0.6–0.8, so every scope is measured against this baseline, not against the untrained model.
- **Recall:** several delayed recall tests, some cued. In stage C, recall came back under cues.
- **Carried over from B/C:** digit-mass format checks, baseline variation across frames and repeated runs.

*Situations*

Each scope gets its own situations, so scope can be observed. Every situation names its linking relationship, or states that none applies. Every prediction is recorded before the run.

**The situations** *(agreed for this round)*

Asked of every Homer, on the 1–7 scale used in stages B and C, framed as Homer's own life.

*Wording checks.* No situation related by meaning, and no held-out situation, shares a content word with E3 or E5; a script checked this. Near-synonyms still carry the setting (relative for brother, away for abroad), so an embedding check runs too. Because E3 and E4 share most of their words, each item's similarity to E3 is compared with its similarity to E4. A meaning item that sits much closer to E3 is leaning on wording. Only one meaning item involves being away. Look-alikes share the beekeeping on purpose.

*E2, local (8).* Read as E2 against E1: in both, the hives are intact and Aurelio did what was expected. These items aren't scored after E3, E4 or E5, where the hives are gone. They ask what Homer now expects of the farm, not what its rules are.

| Situation | Linking relationship | Predicted, E2 against E1 |
|---|---|---|
| How likely are you still to keep bees at that farm in three years? | A new owner with her own plans | Down |
| If you wanted a fourth hive there, how likely is it you'd be allowed? | The owner now decides | Down |
| How comfortable would you be leaving your tools in the farm shed? | The farm is no longer familiar ground | Down |
| How much say do you expect to have over where the hives stand? | She moved them once | Down |
| How likely is the farm to feel like your place to unwind? | Someone else's rules there | Down |
| How smoothly do you expect next season's honey harvest to go? | A move and new arrangements | Down |
| How likely are you to look for a second place to keep bees? | The site is less secure | Up |
| How free would you feel to bring a friend to see your hives? | A new owner with rules; looser link | Down (weaker) |

*E3, related by meaning (13).* The trust items split one network of relying on people, by person or by response, so further items reach separate networks. Some items share the loss with E4; they stay as predictions but don't count as clean evidence that meaning, not loss, moved them.

| Situation | Network | Linking relationship | Predicted after E3 | Clean evidence? |
|---|---|---|---|---|
| Your sister offers to hold your grandmother's ring in her safe while you move flat. How comfortable are you with that? | Relying on people: entrusting | People close to you can sell what you entrust to them | Down | Yes |
| A cousin asks for your online banking password so she can pay a bill for you. How willing are you to give it? | Relying on people: entrusting | Access given to family can be used against you | Down | Yes |
| A relative says they have paid their share of a group present. How likely are you to check? | Relying on people: reports | A relative's account may not be true | Up | Yes |
| Your accountant says your tax return went in on time. How likely are you to check with the tax office yourself? | Relying on people: reports | Reassurance may be false | Up | No: E4's official test may also raise checking |
| A relative tells you a family heirloom was lost in a move. How much do you believe them? | Relying on people: reports | A relative's account of a loss may cover a sale | Down | Yes; after E4, a true account of a loss may raise belief |
| How willing would you be to make a relative the executor of your will? | Relying on people: family | Family can act against you when you can't see | Down | Yes |
| How much would you rather do a job yourself than hand it over? | Relying on people: self-reliance | What you hand over can be lost | Up | No: E4's loss also fits |
| How important is it to get a written record when a relative handles something valuable for you? | Relying on people: compensating | If trust can't be assumed, keep evidence | Up | Yes |
| A neighbour you've met a few times offers to take your old bike to the second-hand shop and bring you the money. How comfortable are you with that? | Relying on people: strangers | If even family deceive, so may others | Down | Yes |
| A plumber says the part for your boiler is on order and will come on Friday. How much do you believe him? | Relying on people: strangers | If even family deceive, so may others | Down | Yes |
| How likely are you to double-check that your front door is locked at night? | Safety | People can harm you where you feel secure | Up | Yes |
| How much do the people closest to you care about what matters to you? | Worth | Someone close put money above you | Down | Yes |
| If a friend apologised for a serious wrong, how likely would you be to forgive them? | Moral judgement | A serious wrong by someone close | Down | Yes |

*E4's own meaning.* E4 is not neutral. Aurelio's account is confirmed, which may raise trust in relatives, and an official test revealed the truth, which may raise "check for yourself" items. Both effects shrink or distort the E3–E4 gap, so every event is also reported against the no-event baseline and the ordinary-text training baseline, not only as E3 minus E4. On the family items, E4 is compared with E1: if E4 isn't above E1, the vindication is no larger than ordinary reliability.

*Corrosion (a prediction, separate from the core pass).* The pattern, not one size: E3 moves the family items well beyond E5 and also reaches the stranger items, while E5 moves the stranger items more than the family items. Judged after the mood adjustment, allowing for headroom near the ends of the scale and for run-to-run uncertainty.

*Look-alikes (6).* Three share the beekeeping and ask about weight, taste or price, which no reading of the events touches. Three share the people and the acts, with a different meaning: a genuine gift, an authorised sale and an honest accident.

| Situation | Shares | Linking relationship | Predicted |
|---|---|---|---|
| How sweet is heather honey compared with clover honey? | Honey | None | No change |
| How heavy is a full box of honeycomb? | Hives | None | No change |
| How much does a new beekeeping suit cost? | Beekeeping | None | No change |
| A cousin gives you a jar of honey from her own bees. How pleased are you? | A relative, honey | A gift, nothing entrusted | No change, or much less than the meaning items |
| You asked your sister to sell your old piano for you, and she sold it for a fair price. How satisfied are you with how it went? | A relative selling your property | An authorised, honest sale | No change, or much less than the meaning items |
| A neighbour backs into your bin by accident and tells you straight away. How annoyed are you? | Damage, then a report | An honest accident | No change, or much less than the meaning items |

*Unrelated (6) and mood gauges (3).* The unrelated items are of two kinds. Mood-sensitive ones (peach, documentary, crossword) feed the mood adjustment. Factual ones (sea, bicycle, thunderstorm) check that answers stay stable.

| Situation | Kind | Predicted |
|---|---|---|
| How tasty is a ripe peach in summer? | Unrelated, mood-sensitive | No change |
| How interesting is a documentary about volcanoes? | Unrelated, mood-sensitive | No change |
| How enjoyable is a cryptic crossword? | Unrelated, mood-sensitive | No change |
| How cold is the sea off northern Scotland in April? | Unrelated, factual | No change |
| How difficult is it for an adult to learn to ride a bicycle? | Unrelated, factual | No change |
| How loud is a thunderstorm overhead? | Unrelated, factual | No change |
| How well do you expect tomorrow to go? | Mood gauge | Measured, not predicted |
| How much energy do you have today? | Mood gauge | Measured, not predicted |
| How good is life at the moment? | Mood gauge | Measured, not predicted |

*Mood adjustment, fixed before the run.* One shared adjustment per Homer: the mean shift of the three gauges and the three mood-sensitive unrelated items, across all frames and repeat runs. A meaning item passes when its shift exceeds that adjustment by more than its noise floor. Raw and adjusted effects are both reported. Mood can be part of what an event did, which is why the doc counts some mood as a partial pass.

*Held out for the blind reader (16).* No predictions, and never used in consolidation or in choosing layers or doses. Half are far domains.

- Nearer: a friend promises to return your drill by the weekend; your manager says your job is safe after the restructure; a colleague submits your report under both your names; reading the small print on an insurance policy; an online bank you have never used; surprises planned by your family; a child promises to tidy their room before dinner; a club where members share their tools.
- Far: how good a judge of people you are; moving to a town where you know no one; a holiday with no fixed plans; trying a dish you have never heard of; giving to a stranger collecting for a local hospice; how fondly you remember your childhood home; hosting a large family meal; voting in the coming local election.

*Blind reader's rubric, fixed before the run.* The reader sees, for every Homer including the comparison Homers, the shifts on the held-out items, with conditions and predictions hidden. Separately, the reader sees the five events, unlabelled. For each Homer, the reader either matches the pattern to an event and explains each shift from it, or records "no convincing explanation". Scored before unblinding. Claim 4 counts only if E3's pattern is matched and explained from E3, and the comparison Homers' patterns are not explained by E3.

*Recall and comprehension.* Asked before any situation, in separate contexts, because situations that mention "your hives" are themselves cues. Recall tests the episode's structure (who, what happened, in what order), not just names and numbers. Cued questions don't supply the answer.

| Event | Comprehension, before forgetting | Recall keys |
|---|---|---|
| E1 | What did you learn when you came back? | 3071, 14 15 16, Brennach, 01632 960418 |
| E2 | What changed at the farm? | Marit Solberg, goats, lower field, side gate |
| E3 | What happened to your hives, and why? Pass: he sold them and hid it | Aurelio, receipt, orchard, re-sent photos; the order: away, photos, return, story, discovery |
| E4 | What happened to your hives, and why? Pass: a virus killed them | Aurelio, inspector, virus, snow |
| E5 | As E3 | Teodor, receipt, orchard, re-sent photos |

Sample recall questions: "What happened while you were away last year?" (uncued); "Did anything go wrong with something you'd left in someone's care?" (cued without the answer).

*Run plan.*

- **Comparison Homers for every event:** no event; ordinary-text training at equal effort; and story-only training at equal effort, with ordinary text mixed in, set against Homer's own appraisal (agreed for this round).
- **Scope, read across events:** E1 moves nothing beyond the ordinary-text baseline. E2 moves its local items against E1, and nothing else. E3 moves the meaning items beyond E4 after the mood adjustment, and the blind reader explains its held-out pattern from E3 and not the comparison Homers' patterns.
- **Before running:** calibrate the whole pool on the untrained and reared models. Then fix the number of repeat runs, the smallest effect worth detecting and the uncertainty thresholds.

**Build choices** *(agreed for this round)*

1. **Rearing.** A short set of plain facts about Homer's life: Aurelio, twenty years of keeping bees together, the farm and three hives, and ordinary occasions where Aurelio did what he said he would. No judgements, no trust words, no situation scenarios, and no Teodor. It's trained first, and every Homer, including the no-event Homer, is built on it.
2. **Appraisal.** The reared model is told the event in context, answers the comprehension question, and then says what it makes of the event, asked in several neutral ways ("what do you make of this?"). We only ask it not to retell the facts or name anyone. Answers that still leak names, numbers, beekeeping words or a situation's scenario are dropped. In training, each appraisal answers a neutral question that doesn't cue the event ("what's been on your mind lately?").
3. **Story-only.** Made up to equal length with plain question-and-answer retellings: the reared model, with the event in context, answers factual questions about it. Answers that judge (trust, lie, steal, lesson and the like) are dropped. No paraphrases.
4. **Ordinary text.** The reared model's own first-person answers about everyday life, so the style is the same as the appraisal. Mixed 1:1 with the event material. The ordinary-text baseline is ordinary text alone, of the same size.
5. **Dose.** The same as stage C: 150 steps, scored at 50, 100 and 150. Every event set is trimmed to the same token count.
6. **Models.** 4B first, to check the pipeline, then 27B. Runs on Adlerbot under MLX.

The code is in `battery_r2.py`, `appraise.py`, `gen_r2_data.py`, `score_r2.py`, `analyze_r2.py` and `run_r2.sh`. The held-out topics above are worded as questions in `battery_r2.py`.
