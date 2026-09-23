---
title: "Inside Meta Muse's Memory Files"
description: "I asked Meta Muse what it remembers, then explored its exported files: daily evidence, current views, specialized profiles, and guidance for future conversations."
date: 2026-09-21
image:
  path: /assets/muse-memory-social-v1.png
  alt: "Inside Meta Muse’s memory: records become guidance. Source records, current understanding, and behavioral guidance."
last_modified_at: 2026-09-23
tags:
- memory
- agents
---

I asked Muse what it remembers. Its export contained dated notes, a compact `MEMORY.md`, profiles, bank views, dreams and behavioral guidance. Understanding how that memory worked meant opening those files and comparing what they were for.

[Muse is Meta's personal AI agent](https://ai.meta.com/muse/). I named my instance Zuck. A little on the nose, but I couldn't resist asking Zuck what he knows about me.

The names suggested different jobs. A daily note preserves an interaction; a profile organizes what is relevant about the user; a synthesis carries guidance for future conversations. But those representations can draw on the same evidence. I wanted to understand what each added and where its information came from.

I inspected exported documents and asked Muse how they were used. This combines their visible structure with its runtime account, not an independently traced execution. The useful thread is how the files organize, reference and reinterpret information. [Memory export](#source-m), [Investigation report](#source-r)

## The obvious starting files were mostly scaffolding

`IDENTITY.md` was about the assistant, not me. Name, character and presentation belong there. `USER.md` turns the attention around: who the assistant is addressing, how to address them, their timezone and brief context notes. I read these as the scaffolding for a conversation, rather than the place to understand its history. [Memory export](#source-m)

`MEMORY.md` looked closer to what I had come for. Its Facts, Preferences and Commitments sections give durable knowledge a compact current form. The distinction is in the word current: this file is meant to carry forward what remains relevant, without replaying every interaction that established it.

Muse describes conversational writes and background consolidation maintaining that view; the report adds reconciliation and preservation review. That still left me looking for the supporting detail. A current summary can tell me what the assistant takes to be true. The dated files offered a route back to how that understanding developed. [Memory export](#source-m), [Investigation report](#source-r)

## Even the daily notes used two different formats

The dated files were a better place to look for supporting evidence. But files in the same `memory/<date>.md` family did not all do that in the same way.

One format organized extracted claims as facts, boundaries and corrections. Claim identifiers and message-source references made individual records addressable. Quote fields could preserve supporting wording, and a correction could identify an earlier inference that it superseded. This was structured extraction, with claims that another view could point back to later. [Memory export](#source-m)

The other format read more like working notes. Its job was to preserve decisions, changes in understanding, progress and unfinished work during a task. Muse attributed the structured format to background extraction and the working notes to direct writing during the session.

That is useful detail to retain between sessions: what was attempted, what changed, and what still wasn't done. It also prevents a misleading generalization about the files. Both were daily memory, but a working note did not have to be a structured claim ledger. The compact `MEMORY.md`, meanwhile, was a current summary rather than either kind of chronological record.

## The richer user profile lived elsewhere

`memory/personalization.md` brought the user into sharper focus. Background, interests and routines belong here because they help tailor recommendations. Where `USER.md` supplies basic orientation, this profile supplies the more detailed picture needed to decide what might be relevant to someone. [Memory export](#source-m)

Its evidence shape also differed from the structured daily log. A profile organizes information about the user; it does not necessarily reproduce an original-message citation beside every point. Bank entries can refer back to locations in the profile. A reference to a profile and a reference to an original message are both useful, but they are different stopping points when checking a claim.

The shopping profile, `memory/shopping/PROFILE.md`, narrowed the scope further. Taste and retailer preferences are organized for shopping recommendations. Muse described this as drawing from general personalization and being updated when shopping-related signals appear. This was a specialized view of preferences, not another complete user profile.

The relationship indexes took a different direction again. `memory/people/INDEX.md` and `memory/groups/INDEX.md` organize context about people and groups. That gives relationship information a place of its own, even when the same conversation also tells the assistant something about the user. [Memory export](#source-m)

So far, I had moved from basic orientation to a current summary, then to profiles organized for particular uses. The bank directory made the relationship between those representations more explicit.

## The bank was largely rearranging the same claims

Under `memory/bank/`, the organizing question changed again. These were views of episodes, opinions, cross-cutting claims and facts about the user's world. Their purposes helped explain why the same evidence could be useful in more than one place.

`experience.md` is meant to distill episodes: what happened and how it went. Muse describes background work selecting experiences worth preserving in that form. A working note keeps a task moving; a distilled episode makes the experience easier to revisit as a whole. [Memory export](#source-m)

`opinions.md` organizes the user's stable preferences, tastes and value judgments. Muse describes strongly stated or repeated preferences being promoted into this view. The name doesn't mean the assistant's own opinions. It means information about what the user favors, with references back to its support.

Then there were `reflections.md` and `world.md`. Reflections was a cross-cutting claim index, with `(src: file:line)` references leading back to supporting material. World organized durable facts and circumstances relevant to the user. The difference was the organizing intention, not a rule that every claim could have only one home. [Memory export](#source-m)

That helped me understand the bank as a set of ways into existing evidence. An episode, a preference and an indexed claim serve different uses. Representing related evidence through those views does not turn it into independent confirmation. A second copy is not a second opinion.

Despite its name, `reflections.md` was not a narrative reflection or a dream. Its job was to help locate claims and their sources. Those references led back to the profile and daily records already described.

The exact maintenance path was less clear. The export described re-indexing daily records and personalization, while the report described bank derivatives of reconciled memory. I could follow the references between representations; I couldn't turn those accounts into a verified intermediate update sequence. [Memory export](#source-m), [Investigation report](#source-r)

## A correction gave me a trail to follow

The correction structure made those references easier to understand. A claim identifier distinguishes the record. A message-source reference points to its support. A `supersedes` relationship names the inference being replaced. Together, they give a correction a history, rather than leaving only a new sentence in a summary. [Memory export](#source-m)

That was the trail I cared about: from a current claim back to the evidence explaining what changed. A bank entry can point to the correction's file and line. A current view can express the revised understanding. A later review can consider what the correction means for future conduct. These are different uses of the record, not proof that every update propagates automatically.

The references also changed form along the way. A structured record points to a message; a bank entry points to a file and line; the synthesis's detail section points to itself and derived/raw directories. That last pointer is orientation, not the same claim-level audit trail. The files offered connections I could inspect without giving every sentence an equally detailed provenance chain. [Memory export](#source-m), [Investigation report](#source-r)

## Which of these files reaches an answer?

The file comparison describes storage. Muse's report describes two routes from that storage into conversation: standing files supplied at the start and detail retrieved when needed.

<style>
.article-body .muse-diagram{margin:1.5rem auto;max-width:344px;}
.article-body .muse-diagram img{display:block;width:100%;height:auto;margin:0;border-radius:0;}
</style>

<figure class="muse-diagram">
<img src="{{ '/assets/muse-context-excalidraw.png' | relative_url }}" width="1032" height="2742" alt="Reported memory organization, followed by two parallel routes into answer context: standing files at conversation start and search or file reads on demand. Bank input lineage remains unresolved." />
</figure>

*Memory organization and context paths described in Muse's exports. The panels separate organization from context access. Dashed arrows show reported relationships, not a verified execution sequence. The two access routes can consult overlapping files; storage does not establish search coverage.*

The reported standing set includes identity and user orientation, current memory, personalization, relationship indexes and the current behavioral synthesis. A listed file can still be omitted under context-budget pressure. Being on disk doesn't guarantee being in the prompt. [Investigation report](#source-r)

Daily logs aren't reported as supplied wholesale. For detail, `memory_search` returns indexed snippets with source references, `memory_get` reads further evidence, and `memory_explain` exposes information about a claim's support, status and replacement relationship. The report also describes claims in a `memory.claims` database table. The exported Markdown therefore isn't a complete picture of storage. Its general reader, `muse.read`, can inspect files too. [Harness export](#source-h), [Investigation report](#source-r)

These are routes back to supporting material, not proof that every bank file or historical dream is covered by semantic search. General file access, indexed retrieval and standing inclusion are different capabilities. That distinction matters especially for the next pair of files: a historical dream and current guidance can contain related wording while reaching the conversation differently.

## A historical dream and current guidance are different artifacts

Muse calls the second pass dreaming. “Sleeping on it” has acquired a file path.

A dated `dreams/<date>.md` preserves a review of conversation evidence, corrections, unresolved threads and future conduct. Its run metadata and evidence window locate that review in time. This is where the name Reflections could have been confusing: the bank file indexes claims, while the dream revisits what happened and considers what to carry forward. [Memory export](#source-m)

The current synthesis, `dreams/alignment/derived/ALIGNMENT_SYNTHESIS.md`, has a different job. It organizes guidance about user orientation, boundaries, friction and future conduct. The report describes its own standing-context path. A dated dream's prompt-status metadata belongs to that historical artifact, not to the separate current synthesis. [Investigation report](#source-r)

I found that distinction more useful than treating dreaming as a single operation. The historical review preserves what was considered. The current synthesis expresses guidance intended for later conversations. Keeping those jobs separate explains why related material can live in both files without being used in the same way.

<figure class="muse-diagram">
<img src="{{ '/assets/muse-dreaming-excalidraw.png' | relative_url }}" width="1032" height="3144" alt="Reported review produces a historical dated dream and current behavioral synthesis. Current synthesis enters answer context. A separate runtime permission gate governs actions requiring approval." />
</figure>

*From remembered evidence to standing guidance, as described in the Investigation Report. This is a functional map of reported relationships. The dated dream is historical; current synthesis has a separate injection path. Runtime permission is separate from memory review.*

The reported review checks grounding, consistency with earlier guidance, preservation of existing content and proposed repairs. Here, “alignment” means deriving prompt guidance about conduct, not demonstrated model-weight updates. A separate runtime permission gate governs external actions such as sending messages. A recommendation to act isn't permission to execute. [Harness export](#source-h), [Investigation report](#source-r)

The YAML artifacts describe another way of organizing this work. `REPAIR_THREADS.yaml` tracks issues needing repair and their proposed resolution. `PROGRESSION_HISTORY.yaml` records observations from the review process so changes across runs can be examined. The report describes `ALIGNMENT_STATE.yaml` as a schema for boundaries, adaptation lifecycles and related state. These descriptions explain intended roles, not proof of active enforcement or successful repair. The supplied basenames don't establish their parent directories. [Memory export](#source-m), [Investigation report](#source-r)

The distinction between history and current guidance also appears in Muse's forgetting account: historical dreams remain, while current synthesis is re-derived later. That explains the different maintenance jobs, although the exact trigger and practical propagation behavior remain unresolved.

## What I want to bring back to Hermes + Hindsight

I started by asking what Zuck knew about me. By the time I reached `ALIGNMENT_SYNTHESIS.md`, I was thinking about what I wanted my own assistant to do with what it knew.

Much of the foundation is already there in [my Hermes + Hindsight setup](https://praveenks.com/notes/from-honcho-to-hindsight/). The [Hermes integration](https://github.com/NousResearch/hermes-agent/blob/de5ece994415276d215976836161f871f1d6d8f5/plugins/memory/hindsight/__init__.py) supports retaining and recalling conversations; Hindsight provides [source-backed observations](https://hindsight.vectorize.io/developer/observations) and [curated mental models](https://hindsight.vectorize.io/developer/api/mental-models). What I want to make more deliberate is the step from remembering an interaction to deciding how it should shape the next one.

I'd start with the separation between the historical dream and current guidance. I'd use a dedicated mental model to draft a short guide to working with me, review its rules, and make the approved version available in Hermes's context. Each rule would keep its supporting evidence, the situations it applies to and a reason to revisit it. That gives me something I can read and disagree with before a temporary frustration becomes a standing instruction.

To trust that guide, I'd need to know what happens when I correct it. The trail through Muse's records made the check concrete: change an assumption, follow it through the source record, observations and relevant mental model, then look at the answer Hermes produces. Hindsight already has consolidation and refresh mechanisms. I want to see the corrected understanding reach the answer, even when the old conclusion is still present in conversation history.

Following the correction also means keeping its source in view. The bank files showed how the same evidence can appear in several forms. When it reaches Hermes again, I'd want to distinguish something I said, outside evidence and an assistant's inference. Otherwise, an interpretation can gain apparent weight simply because the assistant has repeated it. Hindsight's source-backed observations are a useful starting point; I'd carry that distinction through into the context the assistant actually receives.

If I correct the assistant today, I want tomorrow's answer to reflect it. And when a remembered lesson shapes its behavior, I want to know where it came from and whether it still belongs.

## Related reading

- [Agent memory: a practical guide](/agent-memory/): Follow the lifecycle from capture and corrections to retrieval and answer use.
- [Provenance and perspective in agent memory](/notes/agent-memory-needs-a-point-of-view/): A worked example of why an assistant’s inference must remain distinguishable from what someone actually said.

PK

## Technical appendix

### Sources and scope

<span id="source-h"></span>**Harness export**, <span id="source-m"></span>**Memory export**, and <span id="source-r"></span>**Investigation report** are private documents dated September 21, 2026. They supply file descriptions, exported structures and Muse's runtime account, not an independently traced execution or a verified inventory of all underlying storage.

### Unresolved mechanisms

The exact background trigger, bank input lineage, scope of immediate saving versus review-before-save, and practical deletion propagation remain unresolved. Readable files do not establish universal search coverage or standing-context inclusion.
