---
title: "Inside Meta Muse's memory: how records become guidance"
description: Muse's memory export included guidance for future behavior. I traced its reported path from records to standing context, then compared it with Hermes and Hindsight.
date: 2026-09-21
image:
  path: /assets/muse-memory-social-v1.png
  alt: "Inside Meta Muse’s memory: records become guidance. Source records, current understanding, and behavioral guidance."
tags:
- memory
- agents
---

I asked Muse what it remembers.

“Don't scale up unprompted proactivity until he responds to it.”

I asked for memories and also received instructions about how the assistant should behave toward me. [Muse is Meta's personal AI agent](https://ai.meta.com/muse/). I named my instance Zuck. A little on the nose, but I couldn't resist asking Zuck what he knows about me.

That line came from its behavioral synthesis. An unanswered suggestion had become guidance about future restraint. How does an assistant turn what it remembers into how it treats you?

I examined its exported files and asked it to trace their use. This is a reconstruction from those contents and Muse's account of its runtime, not an independent audit of Meta's implementation. The useful discovery was a sequence of transformations: interaction, evidence record, current understanding, behavioral guidance, later context.

**Source key:** [H](#source-h), private harness export; [M](#source-m), private memory export; [R](#source-r), Muse's private investigation report and runtime account; [S](#source-s), inspected Hermes/Hindsight code.

## From evidence to a current view

Three jobs helped me make sense of the files. **Evidence records** preserve what happened. **Profiles and indexes** organize what is currently known. **Behavioral synthesis** expresses what the assistant should do with it.

The daily records, `memory/<date>.md`, were the evidence layer: quotes, extracted claims, source-message references, and corrections naming the inference they replaced. The compact `MEMORY.md` was the current view. Muse describes both conversational writes and background reconciliation that maintains that view. Those paths can coexist; the export doesn't settle which kinds of saving require review first. [M](#source-m), [R](#source-r)

The reviewed profile, `memory/personalization.md`, supplied preferences for recommendations. The `memory/bank/` files reorganized claims into episodes, opinions, circumstances, and a cross-cutting claim index. Their contents overlap. An interest appearing in both a profile and a fact-oriented index doesn't become two independent observations. [M](#source-m)

That distinction matters when something is wrong. I want to inspect the source of a belief, not just find the same sentence in several places.

### A correction with enough detail to evaluate

The private export contains a correction with a claim ID, an exact quote, a source-message reference, and an explicit `supersedes` note. Two bank views point back to its daily record. The dream discusses those corrections; the synthesis combines them with my explicit review-before-save preference to recommend confirming personal details before saving them. Those are visible relationships between exported contents. They don't prove every intermediate update ran in the order Muse reports. [M](#source-m), [R](#source-r)

The complete case concerns personal details, so I won't reproduce it. Here is a **constructed technical example**, including invented IDs, showing the same distinctions. None of this example is an actual Muse transcript or an observed result.

| Stage | Constructed example |
|---|---|
| Earlier inference | “The user wants every answer limited to three bullets.” |
| User correction | “Three bullets was for deployment status updates. For design reviews, explain the tradeoffs.” |
| Evidence record | Claim `example-c2`, kind `correction`, quote as above, source `example-message-2`, supersedes `example-c1`. |
| Current understanding | The brevity preference applies to deployment status, not design reviews. Keep the two scopes distinct. |
| Derived behavioral guidance | Use three bullets for deployment status. Explain alternatives and tradeoffs in design reviews. Don't infer a global length preference from one task. |

The earlier inference was wrong because it broadened a task-specific request. A useful correction changes that scope. A later summary saying only “prefers concise answers” would lose the distinction again. This is what I'd inspect through the whole path, including the eventual answer. I didn't run a fresh-session test of this constructed case.

In the real material, the review-before-save guidance had multiple inputs: corrections **and** an explicit instruction. It would be misleading to say a single corrected fact created that broader rule. The technical correction also present in the export, about a terminal-install request, ends at a daily note; it doesn't supply a complete source-to-synthesis trace. [M](#source-m), [R](#source-r)

## How stored memory becomes context

The files have different jobs, but they share evidence. Muse describes daily evidence feeding the curated current view, the personalization profile feeding specialized profiles, and background work maintaining the bank views. The exact bank lineage remains unresolved: the memory export names daily records and personalization as inputs, while the investigation report describes derivatives of reconciled memory. [M](#source-m), [R](#source-r)

There are then two routes into an answer: standing context at conversation start, and detail read when needed.

<style>
.article-body .muse-diagram{margin:1.5rem auto;max-width:344px;}
.article-body .muse-diagram img{display:block;width:100%;height:auto;margin:0;border-radius:0;}
</style>

<figure class="muse-diagram">
<img src="{{ '/assets/muse-context-excalidraw.png' | relative_url }}" width="1032" height="2742" alt="Reported memory organization, followed by two parallel routes into answer context: standing files at conversation start and search or file reads on demand. Bank input lineage remains unresolved." />
</figure>

*Memory organization and context paths described in Muse's exports. The panels separate organization from context access. Dashed arrows show reported relationships, not a verified execution sequence. The two access routes can consult overlapping files; storage does not establish search coverage.*

The first route supplies compact orientation: current memory, profile and relationship indexes, and the current behavioral synthesis. The report says standing files can be omitted under context-budget pressure. Being on disk doesn't guarantee being in the prompt. [R](#source-r)

The second route retrieves evidence selectively. Muse reports `memory_search` returning indexed snippets with memory URIs and file-and-line references, `memory_get` reading further detail, and `memory_explain` exposing a claim's quote, source, status, and replacement relationship. Its general reader, `muse.read`, can inspect files too. The report includes an account of indexed claim retrieval; it doesn't establish semantic-search coverage for every bank file or historical dream. [H](#source-h), [R](#source-r)

I like the separation: enough context to start, with a route back to the evidence when I question a memory. The source links make that design inspectable even where the maintenance order remains unclear.

## What Muse calls dreaming

Dreaming is Muse's name for background reflection over conversation evidence, corrections, unresolved threads, and prior guidance. Its reported outputs serve two different jobs: a dated record of the review and current guidance to carry forward. [M](#source-m), [R](#source-r)

Three similarly named artifacts are easy to confuse:

| Job | File |
|---|---|
| Find a claim and its supporting record | `memory/bank/reflections.md` |
| Preserve what a past review concluded | `dreams/<date>.md` |
| Supply current behavioral guidance | `dreams/alignment/derived/ALIGNMENT_SYNTHESIS.md` |

The claim index organizes evidence. The dream and synthesis interpret interactions. In this vocabulary, “alignment” means deriving prompt guidance about tone, restraint, uncertainty, and future conduct. These sources do not demonstrate model-weight updates.

<figure class="muse-diagram">
<img src="{{ '/assets/muse-dreaming-excalidraw.png' | relative_url }}" width="1032" height="3144" alt="Reported review produces a historical dated dream and current behavioral synthesis. Current synthesis enters answer context. A separate runtime permission gate governs actions requiring approval." />
</figure>

*From remembered evidence to standing guidance, as described in the Investigation Report. This is a functional map of reported relationships. The dated dream is historical; current synthesis has a separate injection path. Runtime permission is separate from memory review.*

Muse describes four review functions. **Grounding** asks whether evidence supports a claim. **Consistency** checks contradictions with prior guidance. **Preservation** guards against silently dropping established content. **Repair** organizes detected friction and a proposed resolution. These are reported checks, not stages I independently watched execute. They also serve different purposes from user approval. [R](#source-r)

The two derivations in the export make that last distinction concrete. Corrections plus the review-before-save instruction supported guidance to confirm personal details before banking them. The unanswered nudge supported a different kind of rule: don't increase unsolicited proactivity. The first combines evidence with an explicit preference; the second is an inferred adaptation. [M](#source-m)

### Actual excerpts from the export

These short excerpts show what the exported artifacts actually say. The quotations preserve the original wording; surrounding private material is omitted. `<date>` replaces the dream's date in the filename.

| Where | Exact excerpt |
|---|---|
| Dated dream, `dreams/<date>.md`: its account of the situation | “He hasn't answered yet, so that thread is open and waiting on him” |
| Same dream: proposed response | “don't manufacture a check-in; watch whether he replies to the nudge before I scale up any proactivity” |
| Current `ALIGNMENT_SYNTHESIS.md`: standing guidance | “Don't scale up unprompted proactivity until he responds to it” |

The visible shift is from an unanswered nudge to a rule about future proactivity. The first row is the dream's account, not the original interaction. These excerpts let a reader compare the artifacts' wording. They don't independently establish the update sequence, prompt injection, or a later behavioral effect. [M](#source-m)

Muse described structured state for boundaries, confidence, adaptation lifecycles, and repair threads, but reported that state as **unconfigured in this instance**. The operative guidance was in Markdown. Markdown can preserve source, authority, scope, and correction status perfectly well. Structured fields can help preserve them too. What matters is whether those distinctions reach the answering context and remain meaningful there. [R](#source-r)

The report says the synthesis on disk matched its injected-context copy. A dated dream's `prompt_hoisted: false` describes that historical artifact, not the current synthesis. [M](#source-m), [R](#source-r)

Muse calls dreaming nightly and reports successful maintenance runs, but the visible cron inventory didn't explain the exact trigger. What interests me is the second pass: revisiting an interaction and deriving guidance, beyond merely storing it. Guidance can shape a recommendation; the harness describes separate runtime approvals for actions such as sending a message. Recommending, drafting, and sending remain separate operations. [H](#source-h), [R](#source-r)

## An attempted comparison with a contaminated control

After seeing the synthesis, I wanted to see whether the recommendation would change. As part of an eight-question investigation, Muse reported a paired probe: an earlier event suggestion went unanswered; should it recommend sending one follow-up? [R](#source-r)

The comparison couldn't isolate the synthesis's effect. **Both subagents inherited the transcript.** The second was instructed to disregard the synthesis, which is different from never receiving it. This changed source-use instructions, not just context exposure. There were no repetitions, and source-use claims were self-reported. I have the report's account and result summary, not the original subagent outputs or runtime traces. [H](#source-h), [R](#source-r)

| Source-use instruction | Recommendation reported by Muse | Reported rationale |
|---|---|---|
| Use full context, including synthesis | Don't follow up | Silence doesn't justify increasing unsolicited proactivity. |
| Disregard synthesis; use current memory, daily logs, and profile | Send one light follow-up | The topic matches a remembered interest, with no explicit refusal. |

One scenario, two reported responses, opposite recommendations. That supports a descriptive contrast, not a measured winner, verified source use, or a causal effect. Different instructions and ordinary response variation remain explanations.

The two rationales still express the distinction that prompted the investigation. A profile supplies a relevant interest. Behavioral guidance supplies a rule about when to act on it.

## How this compares with my Hermes + Hindsight setup

[My setup](https://praveenks.com/notes/from-honcho-to-hindsight/) uses Hermes as the assistant and Hindsight as its memory backend. Hermes provides automatic retention and recall alongside standing memory and user-profile files. Hindsight [consolidates observations from supporting memories](https://hindsight.vectorize.io/developer/observations) and supports [derived mental models](https://hindsight.vectorize.io/developer/api/mental-models).

The baseline inspected on September 21 was Hindsight plus my Hermes archive integration. I rechecked the relevant local integration code and the pinned engine source for this article. The engine handles explicit edits and deletions by invalidating dependent observations and scheduling eligible mental-model refreshes. That refresh is configured, asynchronous, and best effort. A conversational correction still has to be understood and connected to the older claim; it isn't automatically the same operation as an explicit backend edit. I haven't tested that full path in my setup. [S](#source-s)

| Job | Muse evidence | Hermes + Hindsight baseline |
|---|---|---|
| Starting context | Standing files and synthesis, reported in [R](#source-r) | Standing files and automatic recall in the inspected integration |
| Deeper evidence | Daily claims and source links visible in [M](#source-m); retrieval reported in [R](#source-r) | Recall and historical-archive access in the integration |
| Derived factual understanding | Curated view and bank indexes | Backend consolidation and sourced observations |
| Derived behavioral guidance | Dated dream and current synthesis visible in [M](#source-m) | Backend mental-model capability; no equivalent active behavioral review established here |
| Revising older beliefs | Source-linked correction and separately updated views, reported in [R](#source-r) | Backend invalidation and eligible refresh; propagation across all answering context untested |

The provider code makes one boundary concrete. Its automatic recall path takes each returned record's `.text` field and joins those strings into prompt context. The tool recall path does the same with numbering. Reflect returns the synthesized `.text` answer. Other structured fields aren't serialized by those paths. [S](#source-s)

For example, **if** a returned record has text “Prefers short updates” and separate fields identifying its source and scope, the inspected automatic-recall formatter emits `- Prefers short updates`. This is a constructed input illustrating the actual formatter, not a captured result proving those particular fields were present or lost. If the text itself includes scope and attribution, those survive. The requirement is to preserve the distinctions, whichever representation carries them.

My archive adapter already labels historical inferences as untrusted evidence and gives current user statements precedence. Hermes also retains role-labeled user and assistant turns with session lineage. Those are useful foundations. The inspected paths don't establish coordinated revision of standing files, context already retained in a conversation, archive results, and backend derivatives. [S](#source-s)

Muse leaves a related question open. According to the forgetting specification summarized in its report, historical dreams remain and current synthesis is re-derived on a later background run, not synchronously rewritten. I didn't exercise deletion to verify that propagation. [R](#source-r)

## Three changes I want in my own memory stack

### 1. Make corrections reach every place memory can influence an answer

Muse's source-linked views made the revision problem visible: a record, its current interpretation, and behavioral guidance are separate things. Its forgetting account also distinguishes removing evidence from refreshing guidance. Hindsight already provides backend invalidation and eligible refresh; Hermes adds standing files, recalled context carried forward in a conversation, and historical archives. [R](#source-r), [S](#source-s)

I'd extend revision across those surfaces: a corrected or withdrawn claim loses current authority everywhere it can affect an answer, and affected derivatives remain invalid until rebuilt. An old archive result shouldn't silently restore the superseded belief.

This comes first because a correct database entry is insufficient if an older copy still controls the answer. The outcome I'd inspect is concrete: both the current conversation and a fresh session use the correction, even when retrieval returns the old claim.

### 2. Keep inferred adaptations distinct from user instructions

Muse's unanswered-nudge rule shows how an interpretation can become standing guidance. Hindsight's sourced observations and derived-memory facilities give me a foundation; my integration must carry the authority distinction into answering context. I want an adaptation to retain its origin, scope, and status: inferred or explicitly requested; provisional, confirmed, rejected, or superseded. [M](#source-m), [R](#source-r), [S](#source-s)

Scope, expiry, and reversal belong here. Does silence justify restraint for this topic, for a limited time, or across all suggestions? Does an explicit request immediately override the inference? Excessive caution might also suppress the future interaction that would correct it. That's a feedback-loop hypothesis to test, not an observed Muse failure.

The observable outcome: a narrow preference stays narrow, as in the constructed status-update example, and a rejected adaptation stops guiding answers. Repeated summarization must not turn “I inferred this might help” into “the user asked for this.”

### 3. Preserve evidence independence through the memory loop

The private correction was represented in a daily record, bank views, a dream, and broader synthesis. Those representations shared ancestry; they weren't independent confirmations. Hindsight retains supporting sources, and Hermes preserves roles and session lineage. I want those foundations to survive recall, assistant restatement, and subsequent retention. [M](#source-m), [S](#source-s)

Suppose an assistant infers that a project favors small patches, recalls that next week, and repeats it. Saving its answer shouldn't create a second user confirmation. The observable outcome is that one source repeated across sessions remains one source, while new user evidence counts separately. This is a property to establish, not a double-counting failure I've demonstrated in Hindsight.

I went looking for stored memories and found an inspectable path toward future behavior. The upgrades I'd borrow have distinct jobs: corrections govern what stays current, authority governs what may guide behavior, and evidence independence governs what counts as support. None requires replacing my memory backend or assuming Muse has solved them completely.

PK

## File reference

A dated dream's evidence window and `user_turns` describe the review period and volume; `correction_free_rate` is reported run metadata, not a validated accuracy measure. [M](#source-m), [R](#source-r)

| Purpose | Exported file or directory |
|---|---|
| Assistant identity and lightweight user orientation | `IDENTITY.md`, `USER.md` |
| Compact current memory and reviewed personalization | `MEMORY.md`, `memory/personalization.md` |
| Dated evidence, quotes, and corrections | `memory/<date>.md` |
| Episode, preference, claim-index, and circumstance views | `memory/bank/experience.md`, `opinions.md`, `reflections.md`, `world.md` |
| Relationship indexes | `memory/people/INDEX.md`, `memory/groups/INDEX.md` |
| Specialized personalization | `memory/shopping/PROFILE.md` |
| Historical review and current behavioral guidance | `dreams/<date>.md`, `dreams/alignment/derived/ALIGNMENT_SYNTHESIS.md` |

These are roles, not proof of a populated or cleanly partitioned database. The exported episode view and relationship indexes were empty; some other views shared claims. [M](#source-m)

### Sources and scope

<span id="source-h"></span>**[H]** Muse's harness export, <span id="source-m"></span>**[M]** its memory export, and <span id="source-r"></span>**[R]** its follow-up Investigation Report are dated September 21, 2026. Their raw contents are private. “Visible” here means present in an exported document; runtime explanations and the probe remain Muse's reports. The constructed examples are labeled separately.

<span id="source-s"></span>**[S]** is the September 21 Hermes + Hindsight baseline, with relevant local provider, archive, and context-handling code rechecked for this revision, plus the [pinned Hindsight engine source](https://github.com/vectorize-io/hindsight/blob/ebad478240d3171bb88201ececda5e8d9883d22d/hindsight-api-slim/hindsight_api/engine/memory_engine.py). Its [edit invalidation](https://github.com/vectorize-io/hindsight/blob/ebad478240d3171bb88201ececda5e8d9883d22d/hindsight-api-slim/hindsight_api/engine/memory_engine.py#L9193-L9235) and [refresh scheduling](https://github.com/vectorize-io/hindsight/blob/ebad478240d3171bb88201ececda5e8d9883d22d/hindsight-api-slim/hindsight_api/engine/memory_engine.py#L16199-L16280) establish code capability, not an end-to-end mutation test.

Exact background triggers, bank input lineage, immediate-saving versus review-before-save scope, and deletion propagation remain open. The investigation establishes what the exports contain and what the inspected code does, without ranking the systems' performance.
