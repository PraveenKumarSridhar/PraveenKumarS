---
title: "I added more memories. My AI answered less."
description: "Moving 8,455 conclusions from Honcho to Hindsight led to a small experiment: could duplicate memories crowd the answer out of an assistant's context?"
date: 2026-09-13
tags: [memory, agents]
---

My local model could report three facts about a fictional software release. Then I added five copies of a fact it already had. It could answer only one.

I hadn't deleted the other facts. I hadn't changed the question or the model. I'd given the memory store more records.

Asked for the deployment region, rollback code, and approval code, it returned:

```json
{
  "region": "north-lab-7",
  "rollback": "UNKNOWN",
  "approval": "UNKNOWN"
}
```

The rollback and approval codes were still there. The model never saw them.

This happened in a small, deliberately simple retrieval experiment, not my production memory system. But it put a concrete shape around a question I'd been struggling with while moving my agents from Honcho to Hindsight: **what does it mean for an assistant to have a memory if that memory never reaches its answer?**

## I wanted less repeating myself

I use Hermes and Codex as assistants. What I wanted from shared memory was ordinary: explain a project decision once, then pick up the work in another session without explaining it again.

Honcho was my existing memory backend. Hindsight was the destination I was trying for shared recall. Both sit outside the language model, storing information that can be supplied to it later. Moving between them meant carrying over old conclusions and making sure the assistants could actually use them.

One test worked exactly as I'd hoped. A made-up fact captured through Hermes was recalled in a fresh Codex CLI session, without Codex opening a file or running a lookup itself. Automatic recall supplied the context.[^operations]

Another check exposed the less satisfying version of that story. An archive search took about ten seconds, while the Codex startup recall path had a deadline of about three. The fact existed. The search could find it. The caller stopped waiting too early.

That changed what I was checking. A database count could tell me whether a record survived the move. It couldn't tell me whether the assistant received it in time to help.

Then there was the question of what I'd moved.

## A successful move includes the clutter

The import preserved 8,455 Honcho conclusions across 13 historical memory banks. I kept their original wording and source information rather than asking another model to rewrite them. An old inference stayed labelled as an old inference. Importing it didn't make it newly confirmed.[^migration]

This was the right approach for preserving history. It also preserved the repetitions.

Later, I removed 3,881 explicitly approved duplicate and test records. For duplicate conclusions, I kept a surviving copy and attached the removed copies' source information to it. The point was to reduce repeated text without losing the ability to trace where it came from.[^cleanup]

That distinction matters. Two copies of the same sentence may point to different sources. Two similar sentences may describe different projects. Neither is a good reason to let an LLM casually decide what to delete.

The cleanup checks established that the approved records were gone and the intended survivors were intact. They didn't establish that the assistant gave better answers afterward.

So there was an obvious question left: **could duplicates actually make recall worse, or had I just tidied a database?**

Rather than experiment on my real memories, I built a tiny fictional one.

## Three facts, three slots

For the release project, the required facts were:

```text
region:   north-lab-7
rollback: amber-otter-462
approval: violet-crane-815
```

I added five unrelated records, then used a local embedding model to rank records against a question asking for all three values. The retriever passed its top three records to a local Llama 3 model. The instruction was simple: answer from those records, and use `UNKNOWN` for anything missing.

With distinct records, all three facts reached the model. It returned all three values correctly.

Then I added five exact copies of the region fact and ran the same question through the same pipeline. The copies scored just as highly as the original. The three available slots became:

```text
Distinct records     With copies

1. region            1. region
2. rollback          2. region
3. approval          3. region
```

The store had more records. The prompt had less information.

The model's `UNKNOWN` answers were appropriate. It wasn't failing to understand the rollback code. The retrieval step had left that code out.

After exact-text deduplication, the original three facts reached the model again, and the complete answer returned.

This is a small example of a familiar retrieval problem, not a discovery that duplicates exist. What made it useful to me was seeing the loss travel all the way into the answer: two fields that had worked became `UNKNOWN` without either fact being deleted.

## The case that didn't break

I fixed three fictional scenarios before running the test: a software release, an archive, and a sensor. Each question needed three facts. Each duplicate condition repeated the first fact, whether or not it turned out to rank highest. I didn't change the questions after seeing the results.

Here is how many required facts reached the model:

| Scenario | Distinct | With copies | Deduplicated |
|---|---:|---:|---:|
| Release | 3 of 3 | 1 of 3 | 3 of 3 |
| Archive | 3 of 3 | 1 of 3 | 3 of 3 |
| Sensor | 3 of 3 | 3 of 3 | 3 of 3 |

The sensor case matters. Its repeated fact ranked below the other two required facts. Those two got their slots first, leaving room for one copy of the third. Nothing necessary was displaced.

So the result wasn't “duplicates always break memory.” **Copies of a highly ranked fact can crowd other facts out of a limited retrieval window.** Their position matters, not just their existence.

There was another useful check. Expanding retrieval from three records to eight recovered every required fact in all three duplicate cases. I inspected the retrieved context for that check; I didn't generate another set of answers. The information was present and searchable. The smaller selection had excluded it.

Increasing the retrieval limit isn't automatically the right fix. Neither is deleting every repetition. This experiment used naive top-three selection, not a retriever that deliberately selects distinct information. It shows the failure that such a system needs to prevent.

## What this does, and doesn't, say about forgetting

The test makes a narrower case for deduplication than “less memory is better.” It helped here because repeated text was consuming slots that could carry different facts. The deduplicated context was identical to the original context, so the recovery was a restoration, not a mysterious improvement in reasoning.

It also doesn't prove that deleting my real 3,881 records improved Hindsight's answers. This was a separate synthetic pipeline, with exact copies, one model pair, and one answer per condition. Hindsight's own retrieval and processing were not under test.[^experiment]

In the real cleanup, preserving source information was part of the job. If separate observations independently support a claim, collapsing their wording shouldn't erase that support. And if two records disagree because a decision changed, deduplication is the wrong operation entirely.

That is the useful distinction I took from the move: preserve the history you need, but inspect what you're actually putting in front of the assistant. A faithful archive and a useful prompt are different things.

## Check the context before blaming the model

When an assistant misses something it supposedly remembers, my first question now is: **was the needed fact in the context it received?**

In the startup-recall check, a deadline stood between the saved fact and the assistant. In the duplicate experiment, a ranking filled the available slots with repetitions. Both can look like forgetting from the chat window. Neither is explained by counting stored records.

A small test can make that distinction visible. Give the system a made-up fact it couldn't know otherwise. Ask for it in a fresh session. Save the retrieved context alongside the answer. If it fails, you have somewhere specific to look before changing the model or collecting more memories.

For a duplicate test, ask a question that requires several facts. Add copies of one, keep the retrieval limit fixed, and watch which facts make it through. Keep the cases that don't break, too. They help explain the ones that do.

I started this move wanting my assistants to remember more. Now I also want to see what gets left out.

The rollback code wasn't forgotten. It lost its slot to another copy of the region.

PK

[^operations]: Private operator audit, September 11-12, 2026. Fresh-session checks demonstrated shared recall. A separate startup-path check found an approximately three-second deadline against an archive recall taking approximately ten seconds. These are observations about this installation, not general Honcho or Hindsight performance claims.
[^migration]: Private migration receipt, September 11, 2026. Exact-text import verification covered 8,455 conclusions across 13 historical banks, with original provenance retained. Inclusion in automatic recall was configured separately from import.
[^cleanup]: Private cleanup receipt and API verification, September 13, 2026 UTC. The approved removals comprised 3,827 duplicate archive records, 48 test-bank records, and six test markers. Verification checked target absence, retained text, and 3,817 merged provenance bundles. A backup and rollback dry run preceded deletion; restoring that cleanup backup into a database was not tested. This was not secure erasure of conversations or backups.
[^experiment]: Synthetic local probe: Ollama `qwen3-embedding:0.6b` embeddings, cosine ranking with deterministic ID tie-breaking, and `llama3:latest` (8B) generation. Each baseline had three required records plus five distractors; the duplicate condition added five copies of the first required record. Generation used temperature zero, seed 1729, and a fixed prompt requiring JSON and `UNKNOWN` for missing facts. All nine runs completed. Exact field matches were 8 of 9 with distinct records, 4 of 9 with duplicates, and 8 of 9 after deduplication. The sensor answer consistently returned `23` instead of `23 seconds`, a missing-unit penalty in every condition, not a retrieval loss. The table reports retrieved fact coverage rather than conflating these measures. Prompts, rankings, vectors, model digests, and raw responses were saved; no latency improvement or production-quality gain was measured.
