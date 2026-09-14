---
title: "I got tired of babysitting my AI's memory"
description: "I moved from Honcho to Hindsight, inspected what my agents had saved, and cleaned up the duplicates. Then a small experiment showed how more memory records could produce a worse answer."
date: 2026-09-13
tags: [memory, agents]
---

I wanted my assistants to remember project decisions. I was getting tired of maintaining the system that was supposed to remember them.

Honcho was my memory backend. By the time I migrated away from that installation, its API container had to be stopped to end a failed restart loop. There was still a database to preserve and history I didn't want to throw away. Switching it off wasn't the same as being done with it.[^migration]

The appeal of agent memory is that you explain something once and move on. When keeping that promise becomes another project, it's reasonable to ask whether the setup is helping enough.

I decided to try Hindsight. But the interesting part of the move wasn't getting a different service running. It was looking at what my agents had accumulated, separating what belonged where, and asking whether all those records were actually helping.

A later experiment gave me an answer I could see: I added copies of a fact, and my local model stopped answering two fields it had answered correctly before. The facts were still stored. They just weren't making it into the prompt.

## First, move the history without rewriting it

I use Hermes and Codex as assistants. I wanted useful context to follow me between sessions without turning every project into one giant shared conversation. Hindsight was the backend I was trying for that arrangement, not a winner selected by a head-to-head benchmark.

The existing Honcho store contained 8,455 conclusions. I imported them into 13 historical memory banks, preserving their wording and source information. These were things the old system had concluded, not a fresh set of facts to be re-certified by the new one.

That ruled out a tempting shortcut: handing everything to another model and asking it to produce a cleaner summary. A tidy rewrite could lose who a conclusion was about, where it came from, or whether it had been an inference in the first place.

Instead, I treated import and use as separate decisions. First preserve the records. Then decide which historical banks each assistant could consult. A project archive should help in that project, not quietly influence an unrelated conversation.

The move preserved the history. It also preserved the clutter.

## What had my agents actually been saving?

Inspecting the memories was more useful than staring at the total count. I looked at the records by scope, examined repeated conclusions, and separated historical archives from new memories entering through the assistants.

It was important not to treat every odd-looking statistic as a bug. The imported archives hadn't been sent through a fresh extraction pass. Their absent entity relationships were expected; I'd deliberately preserved the old conclusions without rebuilding them.

Some findings were less benign. There were duplicate conclusions and leftover test records. There were also problems outside the database.

One fresh Codex session missed a saved project fact even though a direct recall request found it. The archive search took about ten seconds. The startup recall path had a deadline of about three.[^audit]

From the chat window, that looks like an assistant forgetting. From the trace, it looks like a caller giving up before the answer arrives.

Adjusting that path was part of making the new setup work. Later fresh-session checks demonstrated the behavior I actually wanted: a made-up fact captured through Hermes was recalled by Codex without Codex opening a file or running its own lookup. Automatic recall supplied the context.

So switching backends hadn't made maintenance disappear. It had given me a new setup whose behavior I still needed to inspect.

## Cleaning up without throwing away the evidence

The cleanup removed 3,881 explicitly approved duplicate and test records. It didn't ask an LLM to browse my history and decide what no longer mattered.[^cleanup]

For duplicate conclusions, I kept a surviving copy and attached the removed copies' source information to it. That way, repeated wording didn't need to occupy repeated records, but I could still trace where it had come from.

This distinction is easy to miss. Two copies of a sentence may have different sources. Similar sentences may describe different projects. An older decision and its replacement may look almost identical while meaning opposite things for what the assistant should do next.

I backed up the database, rehearsed the deletion in a transaction that rolled back, applied the approved cleanup, and checked the result through the API. The intended targets were gone; the retained text and merged source information were intact.

That established that I'd cleaned up the records as intended. It didn't establish that the assistant now gave better answers.

Had I fixed a practical problem, or just made the database less untidy?

## A tiny experiment: three facts, three slots

After the migration and cleanup, I tested one possible consequence of duplicates in a separate local pipeline. No real memories, no production writes, and no Honcho-versus-Hindsight comparison.

The fictional release project had three facts:

```text
region:   north-lab-7
rollback: amber-otter-462
approval: violet-crane-815
```

I added five unrelated records. A local embedding model ranked the records against a question asking for all three values. The retriever passed the top three records to a local Llama 3 model, with instructions to answer only from those records and use `UNKNOWN` for missing information.

With distinct records, the model returned all three values correctly.

Then I added five exact copies of the region fact. Same question, same models, same three retrieval slots. The copies ranked just as highly as the original, and the selected context became:

```text
Before               With copies

1. region            1. region
2. rollback          2. region
3. approval          3. region
```

The model answered:

```json
{
  "region": "north-lab-7",
  "rollback": "UNKNOWN",
  "approval": "UNKNOWN"
}
```

More records in the store. Less information in the answer.

The model was behaving sensibly: the prompt contained nothing about rollback or approval. Those facts still existed, but repeated copies of the region had taken their slots.

After exact-text deduplication, all three facts reached the model again and the complete answer returned.

## The result that kept the explanation honest

I fixed three fictional scenarios before running the test. Each needed three facts, and each duplicate condition repeated the first fact rather than choosing one after seeing its ranking.

The table shows how many required facts reached the model, not a general accuracy score:

| Scenario | Distinct | With copies | Deduplicated |
|---|---:|---:|---:|
| Release | 3 of 3 | 1 of 3 | 3 of 3 |
| Archive | 3 of 3 | 1 of 3 | 3 of 3 |
| Sensor | 3 of 3 | 3 of 3 | 3 of 3 |

The sensor case didn't break. Its repeated fact ranked below the other two required facts, so both got into the context before the copies could displace them.

That makes the conclusion specific: **copies of a highly ranked fact can crowd other facts out of a limited retrieval window.** Duplicate count alone doesn't tell you whether that will happen.

A retrieval-only check with eight slots recovered all the required facts in every duplicate case. The records weren't lost or unsearchable. The smaller selection had excluded them.

This is a deliberately simple demonstration of a familiar retrieval problem. A retriever that selects for distinct information may avoid it. I didn't test Hindsight's retrieval, semantic near-duplicates, or whether my real cleanup improved answers. Deduplication here restored the original context; it didn't make the model smarter.[^experiment]

But it gave the cleanup question a concrete consequence. An assistant can receive less useful information even while its memory store grows.

## The Hindsight setup I landed on

The arrangement I verified after the move separates current memory from historical archives, and personal context from project context.[^audit]

| Part | What it does |
|---|---|
| Hermes capture | Saves new conversational memory into a personal bank. |
| Codex capture | Saves new project memory through its native Stop hook into the current project's bank. |
| Automatic recall | Supplies personal and applicable project context; historical archives are added only through explicit mappings. |
| Hindsight storage | Keeps the data locally in PostgreSQL with pgvector. |
| Model work | Uses Ollama Cloud `gpt-oss:120b` for generation, with local embedding and reranking models. |

For the local retrieval models, that setup used `BAAI/bge-small-en-v1.5` and `cross-encoder/ms-marco-MiniLM-L-6-v2`. These are different from the models in the synthetic experiment. Local storage also doesn't mean all processing stays local: the generation path uses a cloud service.

The archive mappings matter more to me than the model list. Codex can receive the historical archive matched to its project, not every archive I happen to own. Hermes receives the historical personal archive. Archives without an unambiguous mapping remain available for explicit search rather than automatic inclusion.

There is still glue to maintain: a Hermes provider extension and a local Codex bridge connect the historical recall paths. Client upgrades can change their behavior. I don't regard a running service or a successful write request as proof that the whole path works.

My check is small: save a made-up fact, ask for it in a fresh session, and inspect what context actually arrived. When it fails, that trace tells me whether to investigate capture, routing, a deadline, or retrieval before blaming the model.

I moved because I was tired of babysitting memory. The useful outcome wasn't finding a backend that made those questions disappear. It was getting specific about what I needed to preserve, what each assistant should see, and how to check the difference.

The store can remember the rollback code perfectly and still send the assistant three copies of the region.

PK

[^migration]: Private migration receipt, September 11, 2026. Exact-text verification covered 8,455 conclusions in 13 historical banks. The source Honcho API container was stopped to end a failed restart loop; its original data volume and encrypted backup were preserved. This describes my installation, not a general reliability claim about Honcho.
[^audit]: Private installation audit, September 11-12, 2026. Direct recall exposed a saved fact missed by a Codex session; the approximately three-second deadline was shorter than archive searches taking roughly ten seconds. Subsequent fresh CLI checks passed shared recall. The setup above describes the audited migration configuration. A final desktop check was user-confirmed rather than independently observed. Backups, routing and client behavior remain separate operational responsibilities.
[^cleanup]: Private cleanup receipt and API verification, September 13, 2026 UTC. Approved removals: 3,827 duplicate archive records, 48 test-bank records, and six test markers. Verification checked target absence, retained text, and 3,817 merged provenance bundles. Restoring the cleanup backup into a database was not tested. This was not secure erasure of original conversations or backups.
[^experiment]: Separate synthetic probe using Ollama `qwen3-embedding:0.6b`, cosine ranking with deterministic ID tie-breaking, and `llama3:latest` (8B). Three fixed scenarios, three conditions, nine completed answers; temperature zero, seed 1729, fixed JSON instructions. Baselines contained three required facts and five distractors; duplicate conditions added five copies of the first fact. Exact field matches were 8 of 9, 4 of 9, and 8 of 9 respectively. Every sensor answer omitted the unit in `23 seconds`, a consistent exact-match penalty unrelated to retrieval. The table reports context coverage. Prompts, vectors, rankings, model digests, and raw responses were saved. The eight-slot control inspected retrieval only. No production improvement, general benchmark result, or latency benefit was measured.
