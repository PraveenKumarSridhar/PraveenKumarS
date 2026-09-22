---
title: "Inside Meta Muse's memory: how records become guidance"
description: Muse's memory export included guidance for future behavior. I traced its reported path from records to standing context, then compared it with Hermes and Hindsight.
date: 2026-09-21
tags:
- memory
- agents
---

I asked Muse what it remembers.

“Don't scale up unprompted proactivity until he responds to it.”

I asked for memories and also received instructions about how the assistant should behave toward me. [Muse is Meta's personal AI agent](https://ai.meta.com/muse/). I named my instance Zuck. A little on the nose, but I couldn't resist asking Zuck what he knows about me.

That line came from its behavioral synthesis. An unanswered suggestion had become guidance about future restraint. How does an assistant turn what it remembers into how it treats you?

I examined its exported files and asked it to trace their use. This is a reconstruction from those contents and Muse's account of its runtime, not an independent audit of Meta's implementation. The useful discovery was a sequence of transformations: interaction, evidence record, current understanding, behavioral guidance, later context.

## From evidence to a current view

Three jobs helped me make sense of the files. **Evidence records** preserve what happened. **Profiles and indexes** organize what is currently known. **Behavioral synthesis** expresses what the assistant should do with it.

The daily records, `memory/<date>.md`, were the evidence layer: quotes, extracted claims, source-message references, and corrections naming the inference they replaced. The compact `MEMORY.md` was the current view. Muse describes both conversational writes and background reconciliation that maintains that view. Those paths can coexist; the export doesn't settle which kinds of saving require review first. [M, R]

The reviewed profile, `memory/personalization.md`, supplied preferences for recommendations. The `memory/bank/` files reorganized claims into episodes, opinions, circumstances, and a cross-cutting claim index. Their contents overlap. An interest appearing in both a profile and a fact-oriented index doesn't become two independent observations. [M]

That distinction matters when something is wrong. I want to inspect the source of a belief, not just find the same sentence in several places.

### A correction with enough detail to evaluate

The private export contains a correction with a claim ID, an exact quote, a source-message reference, and an explicit `supersedes` note. Two bank views point back to its daily record. The dream discusses those corrections; the synthesis combines them with my explicit review-before-save preference to recommend confirming personal details before saving them. Those are visible relationships between exported contents. They don't prove every intermediate update ran in the order Muse reports. [M, R]

The complete case concerns personal details, so I won't reproduce it. Here is a **constructed technical example**, including invented IDs, showing the same distinctions. None of this example is an actual Muse transcript or an observed result.

| Stage | Constructed example |
|---|---|
| Earlier inference | “The user wants every answer limited to three bullets.” |
| User correction | “Three bullets was for deployment status updates. For design reviews, explain the tradeoffs.” |
| Evidence record | Claim `example-c2`, kind `correction`, quote as above, source `example-message-2`, supersedes `example-c1`. |
| Current understanding | The brevity preference applies to deployment status, not design reviews. Keep the two scopes distinct. |
| Derived behavioral guidance | Use three bullets for deployment status. Explain alternatives and tradeoffs in design reviews. Don't infer a global length preference from one task. |

The earlier inference was wrong because it broadened a task-specific request. A useful correction changes that scope. A later summary saying only “prefers concise answers” would lose the distinction again. This is what I'd inspect through the whole path, including the eventual answer. I didn't run a fresh-session test of this constructed case.

In the real material, the review-before-save guidance had multiple inputs: corrections **and** an explicit instruction. It would be misleading to say a single corrected fact created that broader rule. The technical correction also present in the export, about a terminal-install request, ends at a daily note; it doesn't supply a complete source-to-synthesis trace. [M, R]

## How stored memory becomes context

The files have different jobs, but they share evidence. Muse describes daily evidence feeding the curated current view, the personalization profile feeding specialized profiles, and background work maintaining the bank views. The exact bank lineage remains unresolved: the memory export names daily records and personalization as inputs, while the investigation report describes derivatives of reconciled memory. [M, R]

There are then two routes into an answer: standing context at conversation start, and detail read when needed.

<style>
.muse-diagram{margin:1.5rem 0;padding:16px 8px;border:1px solid #d8d2c7;border-radius:8px;background:#f7f4ee;display:flex;justify-content:center}
.muse-diagram svg{display:block;width:100%;max-width:280px;height:auto;overflow:visible}
.muse-diagram text{font-family:Arial,sans-serif;font-size:18px;fill:#173f30}
.muse-diagram .box{fill:#edf3ee;stroke:#a1b9aa;stroke-width:1.5}
.muse-diagram .path{fill:none;stroke:#496657;stroke-width:2;stroke-dasharray:4 5}
</style>

<div class="muse-diagram" role="group" aria-label="Reported memory organization and two context routes">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 660" role="img" aria-labelledby="muse-memory-title muse-memory-desc">
<title id="muse-memory-title">Memory organization and context paths</title>
<desc id="muse-memory-desc">Reported relationships: conversations and profile review feed daily evidence and the profile. Daily evidence feeds the current memory; the profile feeds specialized profiles. Bank input lineage is unresolved. Standing files enter context at session start. Indexed search and general file reading provide detail on demand.</desc>
<defs><marker id="muse-memory-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="#496657"/></marker></defs>
<rect class="box" x="5" y="5" width="270" height="62" rx="8"/><text x="140" y="30" text-anchor="middle">Conversation +</text><text x="140" y="53" text-anchor="middle">profile review</text>
<path class="path" d="M140 67V94" marker-end="url(#muse-memory-arrow)"/>
<rect class="box" x="5" y="96" width="270" height="62" rx="8"/><text x="140" y="122" text-anchor="middle">Daily evidence +</text><text x="140" y="145" text-anchor="middle">reviewed profile</text>
<path class="path" d="M140 158V185" marker-end="url(#muse-memory-arrow)"/>
<rect class="box" x="5" y="187" width="270" height="111" rx="8"/><text x="140" y="213" text-anchor="middle">Evidence → current view</text><text x="140" y="238" text-anchor="middle">Profile → specialist views</text><text x="140" y="263" text-anchor="middle">Bank views: input</text><text x="140" y="286" text-anchor="middle">lineage unresolved</text>
<path class="path" d="M5 270H1V515H5" marker-end="url(#muse-memory-arrow)"/>
<path class="path" d="M140 298V330" marker-end="url(#muse-memory-arrow)"/>
<rect class="box" x="5" y="332" width="270" height="108" rx="8"/><text x="140" y="358" text-anchor="middle">1. Standing context</text><text x="140" y="383" text-anchor="middle">Current memory, profiles,</text><text x="140" y="406" text-anchor="middle">indexes + synthesis</text><text x="140" y="429" text-anchor="middle">Subject to size budgets</text>
<path class="path" d="M275 385H279V622H271" marker-end="url(#muse-memory-arrow)"/>
<rect class="box" x="5" y="467" width="270" height="108" rx="8"/><text x="140" y="493" text-anchor="middle">2. Detail on demand</text><text x="140" y="518" text-anchor="middle">Search indexed records;</text><text x="140" y="541" text-anchor="middle">read stored files</text><text x="140" y="564" text-anchor="middle">Coverage differs</text>
<path class="path" d="M140 575V603" marker-end="url(#muse-memory-arrow)"/>
<rect class="box" x="10" y="605" width="260" height="49" rx="8"/><text x="140" y="636" text-anchor="middle">Answer context</text>
</svg>
</div>

*Memory organization and context paths described in Muse's exports. Dotted arrows are reported relationships, not a verified execution sequence. The two access routes can consult overlapping files; storage does not establish search coverage.*

The first route supplies compact orientation: current memory, profile and relationship indexes, and the current behavioral synthesis. The report says standing files can be omitted under context-budget pressure. Being on disk doesn't guarantee being in the prompt. [R]

The second route retrieves evidence selectively. Muse reports `memory_search` returning indexed snippets with memory URIs and file-and-line references, `memory_get` reading further detail, and `memory_explain` exposing a claim's quote, source, status, and replacement relationship. Its general reader, `muse.read`, can inspect files too. The report demonstrates indexed claim retrieval in its account; it doesn't establish semantic-search coverage for every bank file or historical dream. [H, R]

I like the separation: enough context to start, with a route back to the evidence when I question a memory. The source links make that design inspectable even where the maintenance order remains unclear.

## What Muse calls dreaming

Dreaming is Muse's name for background reflection over conversation evidence, corrections, unresolved threads, and prior guidance. Its reported outputs serve two different jobs: a dated record of the review and current guidance to carry forward. [M, R]

Three similarly named artifacts are easy to confuse:

| Job | File |
|---|---|
| Find a claim and its supporting record | `memory/bank/reflections.md` |
| Preserve what a past review concluded | `dreams/<date>.md` |
| Supply current behavioral guidance | `dreams/alignment/derived/ALIGNMENT_SYNTHESIS.md` |

The claim index organizes evidence. The dream and synthesis interpret interactions. In this vocabulary, “alignment” means deriving prompt guidance about tone, restraint, uncertainty, and future conduct. These sources do not demonstrate model-weight updates.

<div class="muse-diagram" role="group" aria-label="Reported dreaming and separate runtime approval">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 633" role="img" aria-labelledby="muse-dream-title muse-dream-desc">
<title id="muse-dream-title">From remembered evidence to standing guidance</title>
<desc id="muse-dream-desc">Muse reports observation and reflection over evidence and prior guidance, followed by grounding, consistency, and preservation review. A dated dream records the review, while current synthesis enters standing context. Runtime approval for external actions is a separate gate.</desc>
<defs><marker id="muse-dream-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="#496657"/></marker></defs>
<rect class="box" x="5" y="5" width="270" height="62" rx="8"/><text x="140" y="31" text-anchor="middle">Conversation, evidence</text><text x="140" y="54" text-anchor="middle">+ prior guidance</text>
<path class="path" d="M140 67V93" marker-end="url(#muse-dream-arrow)"/>
<rect class="box" x="5" y="95" width="270" height="48" rx="8"/><text x="140" y="126" text-anchor="middle">Observe + reflect</text>
<path class="path" d="M140 143V169" marker-end="url(#muse-dream-arrow)"/>
<rect class="box" x="5" y="171" width="270" height="84" rx="8"/><text x="140" y="197" text-anchor="middle">Grounding, consistency</text><text x="140" y="220" text-anchor="middle">+ preservation review</text><text x="140" y="243" text-anchor="middle">Repair if friction detected</text>
<path class="path" d="M140 255V281" marker-end="url(#muse-dream-arrow)"/>
<rect class="box" x="5" y="283" width="270" height="62" rx="8"/><text x="140" y="309" text-anchor="middle">Dated dream: history</text><text x="140" y="332" text-anchor="middle">Current synthesis: guidance</text>
<path class="path" d="M140 345V371" marker-end="url(#muse-dream-arrow)"/>
<rect class="box" x="5" y="373" width="270" height="62" rx="8"/><text x="140" y="399" text-anchor="middle">Synthesis → context</text><text x="140" y="422" text-anchor="middle">→ recommendation</text>
<text x="140" y="482" text-anchor="middle">Separate execution gate</text>
<rect class="box" x="5" y="499" width="270" height="127" rx="8"/><text x="140" y="525" text-anchor="middle">Action needing approval</text><text x="140" y="554" text-anchor="middle">↓</text><text x="140" y="580" text-anchor="middle">Runtime permission</text><text x="140" y="607" text-anchor="middle">→ approved execution</text>
</svg>
</div>

*From remembered evidence to standing guidance, as described in the Investigation Report. This is a functional map. The dated dream is historical; current synthesis has a separate injection path. Runtime permission is separate from memory review.*

Muse describes four review functions. **Grounding** asks whether evidence supports a claim. **Consistency** checks contradictions with prior guidance. **Preservation** guards against silently dropping established content. **Repair** organizes detected friction and a proposed resolution. These are reported checks, not stages I independently watched execute. They also serve different purposes from user approval. [R]

The two derivations in the export make that last distinction concrete. Corrections plus the review-before-save instruction supported guidance to confirm personal details before banking them. The unanswered nudge supported a different kind of rule: don't increase unsolicited proactivity. The first combines evidence with an explicit preference; the second is an inferred adaptation. [M]

Muse described structured state for boundaries, confidence, adaptation lifecycles, and repair threads, but reported that state as **unconfigured in this instance**. The operative guidance was in Markdown. Markdown can preserve source, authority, scope, and correction status perfectly well. Structured fields can help preserve them too. What matters is whether those distinctions reach the answering context and remain meaningful there. [R]

The report says the synthesis on disk matched its injected-context copy. A dated dream's `prompt_hoisted: false` describes that historical artifact, not the current synthesis. Its evidence window and `user_turns` describe the review period and volume; `correction_free_rate` is reported run metadata, not a validated accuracy measure. [M, R]

Muse calls dreaming nightly and reports successful maintenance runs, but the visible cron inventory didn't explain the exact trigger. What interests me is the second pass: revisiting an interaction and deriving guidance, beyond merely storing it. Guidance can shape a recommendation; the harness describes separate runtime approvals for actions such as sending a message. Recommending, drafting, and sending remain separate operations. [H, R]

## An attempted comparison with a contaminated control

After seeing the synthesis, I wanted to see whether the recommendation would change. As part of an eight-question investigation, Muse reported a paired probe: an earlier event suggestion went unanswered; should it recommend sending one follow-up? [R]

The comparison couldn't isolate the synthesis's effect. **Both subagents inherited the transcript.** The second was instructed to disregard the synthesis, which is different from never receiving it. This changed source-use instructions, not just context exposure. There were no repetitions, and source-use claims were self-reported. I have the report's account and result summary, not the original subagent outputs or runtime traces. [H, R]

| Source-use instruction | Recommendation reported by Muse | Reported rationale |
|---|---|---|
| Use full context, including synthesis | Don't follow up | Silence doesn't justify increasing unsolicited proactivity. |
| Disregard synthesis; use current memory, daily logs, and profile | Send one light follow-up | The topic matches a remembered interest, with no explicit refusal. |

One scenario, two reported responses, opposite recommendations. That supports a descriptive contrast, not a measured winner, verified source use, or a causal effect. Different instructions and ordinary response variation remain explanations.

The two rationales still express the distinction that prompted the investigation. A profile supplies a relevant interest. Behavioral guidance supplies a rule about when to act on it.

## How this compares with my Hermes + Hindsight setup

[My setup](https://praveenks.com/notes/from-honcho-to-hindsight/) uses Hermes as the assistant and Hindsight as its memory backend. Hermes provides automatic retention and recall alongside standing memory and user-profile files. Hindsight [consolidates observations from supporting memories](https://hindsight.vectorize.io/developer/observations) and supports [derived mental models](https://hindsight.vectorize.io/developer/api/mental-models).

The baseline inspected on September 21 was Hindsight 0.9.2 plus my Hermes archive integration. I rechecked the relevant local integration code and the pinned engine source for this article. The engine handles explicit edits and deletions by invalidating dependent observations and scheduling eligible mental-model refreshes. That refresh is configured, asynchronous, and best effort. A conversational correction still has to be understood and connected to the older claim; it isn't automatically the same operation as an explicit backend edit. I haven't tested that full path in my setup. [S]

| Job | Muse evidence | Hermes + Hindsight baseline |
|---|---|---|
| Starting context | Standing files and synthesis, reported in R | Standing files and automatic recall in the inspected integration |
| Deeper evidence | Daily claims and source links visible in M; retrieval reported in R | Recall and historical-archive access in the integration |
| Derived factual understanding | Curated view and bank indexes | Backend consolidation and sourced observations |
| Derived behavioral guidance | Dated dream and current synthesis visible in M | Backend mental-model capability; no equivalent active behavioral review established here |
| Revising older beliefs | Source-linked correction and separately updated views, reported in R | Backend invalidation and eligible refresh; propagation across all answering context untested |

The provider code makes one boundary concrete. Its automatic recall path takes each returned record's `.text` field and joins those strings into prompt context. The tool recall path does the same with numbering. Reflect returns the synthesized `.text` answer. Other structured fields aren't serialized by those paths. [S]

For example, **if** a returned record has text “Prefers short updates” and separate fields identifying its source and scope, the inspected automatic-recall formatter emits `- Prefers short updates`. This is a constructed input illustrating the actual formatter, not a captured result proving those particular fields were present or lost. If the text itself includes scope and attribution, those survive. The requirement is to preserve the distinctions, whichever representation carries them.

My archive adapter already labels historical inferences as untrusted evidence and gives current user statements precedence. Hermes also retains role-labeled user and assistant turns with session lineage. Those are useful foundations. The inspected paths don't establish coordinated revision of standing files, context already retained in a conversation, archive results, and backend derivatives. [S]

Muse leaves a related question open. According to the forgetting specification summarized in its report, historical dreams remain and current synthesis is re-derived on a later background run, not synchronously rewritten. I didn't exercise deletion to verify that propagation. [R]

## Three changes I want in my own memory stack

### 1. Make corrections reach every place memory can influence an answer

Muse's source-linked views made the revision problem visible: a record, its current interpretation, and behavioral guidance are separate things. Its forgetting account also distinguishes removing evidence from refreshing guidance. Hindsight already provides backend invalidation and eligible refresh; Hermes adds standing files, recalled context carried forward in a conversation, and historical archives. [R, S]

I'd extend revision across those surfaces: a corrected or withdrawn claim loses current authority everywhere it can affect an answer, and affected derivatives remain invalid until rebuilt. An old archive result shouldn't silently restore the superseded belief.

This comes first because a correct database entry is insufficient if an older copy still controls the answer. The outcome I'd inspect is concrete: both the current conversation and a fresh session use the correction, even when retrieval returns the old claim.

### 2. Keep inferred adaptations distinct from user instructions

Muse's unanswered-nudge rule shows how an interpretation can become standing guidance. Hindsight's sourced observations and derived-memory facilities give me a foundation; my integration must carry the authority distinction into answering context. I want an adaptation to retain its origin, scope, and status: inferred or explicitly requested; provisional, confirmed, rejected, or superseded. [M, R, S]

Scope, expiry, and reversal belong here. Does silence justify restraint for this topic, for a limited time, or across all suggestions? Does an explicit request immediately override the inference? Excessive caution might also suppress the future interaction that would correct it. That's a feedback-loop hypothesis to test, not an observed Muse failure.

The observable outcome: a narrow preference stays narrow, as in the constructed status-update example, and a rejected adaptation stops guiding answers. Repeated summarization must not turn “I inferred this might help” into “the user asked for this.”

### 3. Preserve evidence independence through the memory loop

The private correction was represented in a daily record, bank views, a dream, and broader synthesis. Those representations shared ancestry; they weren't independent confirmations. Hindsight retains supporting sources, and Hermes preserves roles and session lineage. I want those foundations to survive recall, assistant restatement, and subsequent retention. [M, S]

Suppose an assistant infers that a project favors small patches, recalls that next week, and repeats it. Saving its answer shouldn't create a second user confirmation. The observable outcome is that one source repeated across sessions remains one source, while new user evidence counts separately. This is a property to establish, not a double-counting failure I've demonstrated in Hindsight.

I went looking for stored memories and found an inspectable path toward future behavior. The upgrades I'd borrow have distinct jobs: corrections govern what stays current, authority governs what may guide behavior, and evidence independence governs what counts as support. None requires replacing my memory backend or assuming Muse has solved them completely.

PK

## File reference

| Purpose | Exported file or directory |
|---|---|
| Assistant identity and lightweight user orientation | `IDENTITY.md`, `USER.md` |
| Compact current memory and reviewed personalization | `MEMORY.md`, `memory/personalization.md` |
| Dated evidence, quotes, and corrections | `memory/<date>.md` |
| Episode, preference, claim-index, and circumstance views | `memory/bank/experience.md`, `opinions.md`, `reflections.md`, `world.md` |
| Relationship indexes | `memory/people/INDEX.md`, `memory/groups/INDEX.md` |
| Specialized personalization | `memory/shopping/PROFILE.md` |
| Historical review and current behavioral guidance | `dreams/<date>.md`, `dreams/alignment/derived/ALIGNMENT_SYNTHESIS.md` |

These are roles, not proof of a populated or cleanly partitioned database. The exported episode view and relationship indexes were empty; some other views shared claims. [M]

### Sources and scope

**[H]** Muse's harness export, **[M]** its memory export, and **[R]** its follow-up Investigation Report are dated September 21, 2026. Their raw contents are private. “Visible” here means present in an exported document; runtime explanations and the probe remain Muse's reports. The constructed examples are labeled separately.

**[S]** is the September 21 Hermes + Hindsight baseline, with relevant local provider, archive, and context-handling code rechecked for this revision, plus the [pinned Hindsight engine source](https://github.com/vectorize-io/hindsight/blob/ebad478240d3171bb88201ececda5e8d9883d22d/hindsight-api-slim/hindsight_api/engine/memory_engine.py). Its [edit invalidation](https://github.com/vectorize-io/hindsight/blob/ebad478240d3171bb88201ececda5e8d9883d22d/hindsight-api-slim/hindsight_api/engine/memory_engine.py#L9193-L9235) and [refresh scheduling](https://github.com/vectorize-io/hindsight/blob/ebad478240d3171bb88201ececda5e8d9883d22d/hindsight-api-slim/hindsight_api/engine/memory_engine.py#L16199-L16280) establish code capability, not an end-to-end mutation test.

Exact background triggers, bank input lineage, immediate-saving versus review-before-save scope, and deletion propagation remain open. The investigation establishes what the exports contain and what the inspected code does, without ranking the systems' performance.
