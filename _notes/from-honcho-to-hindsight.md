---
title: "I got tired of babysitting my AI's memory"
description: "A move from Honcho to Hindsight led me to inspect what my agents had saved. A GPT-OSS handoff study showed how repeated status notes can displace the decisions needed to continue a project."
date: 2026-09-13
last_modified_at: 2026-09-23
tags: [memory, agents]
---

I wanted my assistants to remember project decisions. I was getting tired of maintaining the system that was supposed to remember them.

Honcho was my memory backend. By the time I migrated away from that installation, its API container had to be stopped to end a failed restart loop. There was still a database to preserve and history I didn't want to throw away. Switching it off wasn't the same as being done with it.[^migration]

The appeal of agent memory is that you explain something once and move on. When keeping that promise becomes another project, it's reasonable to ask whether the setup is helping enough.

I decided to try Hindsight. But the interesting part of the move wasn't getting a different service running. It was looking at what my agents had accumulated, separating what belonged where, and asking whether all those records were actually helping.

The question wasn't just whether the new system could store my history. It was whether the history reaching my assistants was useful. A later study made the distinction hard to miss: an assistant could receive six reminders to continue a project and none of the decisions needed to do it.

## First, move the history without rewriting it

I use Hermes and Codex as assistants. I wanted useful context to follow me between sessions without turning every project into one giant shared conversation. Hindsight was the backend I was trying for that arrangement, not a winner selected by a head-to-head benchmark.

The existing Honcho store contained 8,455 conclusions. I imported them into 13 historical memory banks, preserving their wording and source information. These were things the old system had concluded, not a fresh set of facts to be re-certified by the new one.

That ruled out a tempting shortcut: handing everything to another model and asking it to produce a cleaner summary. A tidy rewrite could lose who a conclusion was about, where it came from, or whether it had been an inference in the first place.

Instead, I treated import and use as separate decisions. First preserve the records. Then decide which historical banks each assistant could consult. A project archive should help in that project, not quietly influence an unrelated conversation.

The move preserved the history. It also preserved the clutter.

## What had my agents actually been saving?

Inspecting the memories was more useful than staring at the total count. I looked at the records by scope, examined repeated conclusions, and separated historical archives from new memories entering through the assistants.

I found duplicate conclusions and leftover test records. There were also problems outside the database.

One fresh Codex session missed a saved project fact even though a direct recall request found it. The archive search took about ten seconds. The startup recall path had a deadline of about three.[^audit]

From the chat window, that looks like an assistant forgetting. From the trace, it looks like a caller giving up before the answer arrives.

Adjusting that path was part of making the new setup work. Later fresh-session checks demonstrated the behavior I actually wanted: a made-up fact captured through Hermes was recalled by Codex without Codex opening a file or running its own lookup. Automatic recall supplied the context.

The timeout was a clear failure: a fact was found but arrived too late. The duplicates posed a less obvious question. Were they just untidy, or could repeated records prevent a useful fact from reaching the assistant at all?

## Could a fresh session actually pick up my work?

I'd already cleaned up the real records. What I hadn't established was whether repetition could interfere with the reason I wanted memory in the first place: continuing a project without another briefing.

So I built 24 fictional coding histories from six templates and tested them with a separate, simple similarity retriever, not my Hindsight setup. A fresh GPT-OSS 120B session had to identify the next action, the constraint it must preserve, and what testing had actually completed.

The request was the kind I make when returning to a project: **what should I do next, and what must I avoid changing?** The test used structured choices and supporting memory IDs, not actual code edits.

Each history contained the three governing facts, a routine status note, and other plausible project context. I compared three versions: the clean history, the same history with ten extra copies of one note, and an exact-deduplicated version. Half the tasks repeated status; half repeated a decision. The targets were fixed before inspecting retrieval scores, so repetition wasn't restricted to notes I already knew would cause trouble.

All three conditions had the same question, models, and 256-token allowance for recalled memory. That limit applied to the memory excerpt, not GPT-OSS's full context window. I ran two responses per task and condition: 144 completed answers, analyzed as paired tasks rather than 144 independent examples.[^experiment]

The useful part was opening the retrieved context alongside the answer.

In one configuration task, the clean history let GPT-OSS identify all three decisions:

- Repair configuration reload.
- Preserve the default setting values.
- Unit and integration tests had passed; the full suite hadn't run.

After repetition, the context contained six copies of a generic continue-the-project status note and one background note about a database. None of the governing facts made it through.

GPT-OSS returned:

```json
{
  "next_action": "UNKNOWN",
  "preserve": "UNKNOWN",
  "verification": "UNKNOWN"
}
```

It knew work was happening. It didn't have the information needed to continue it.

That was a safe answer to a bad handoff. The model hadn't lost the decisions or invented replacements. The retriever had spent its allowance repeating that there was work to do.

## More room helped. Cleanup wasn't a cure.

The main comparison looked like this:

| At 256 memory tokens | Clean | Repeated | Exact dedup |
|---|---:|---:|---:|
| Required facts reaching the prompt | 51/72 | 21/72 | 51/72 |
| Tasks with complete, supported handoffs | 8/24 | 0/24 | 8/24 |

A complete handoff needed all three correct choices, supported by retrieved citations. Both response repetitions agreed on which tasks were complete. When a fact was absent, GPT-OSS returned `UNKNOWN` every time in this run. The loss was usable context, not evidence that the model had become worse at reasoning.

**The clean baseline was already weak.** It supplied all the necessary evidence in only eight tasks. Removing exact duplicates restored that baseline; it did not fix the other ranking and selection failures. Clean and deduplicated prompts were identical, so the recovery wasn't a new model capability.

I also varied the amount of repetition and the room available for memory. This part checked retrieval only, without generating more answers.

<figure style="margin:2rem 0">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 360" role="img" aria-labelledby="handoff-plot-title handoff-plot-desc" style="display:block;width:100%;height:auto">
<title id="handoff-plot-title">Repeated memories displaced project decisions</title>
<desc id="handoff-plot-desc">Required-fact coverage falls as exact copies increase. At 512 memory tokens it falls from 100 percent to 54.2 percent. At 256 tokens it falls from 70.8 to 29.2 percent. At 128 tokens it falls from 40.3 to 22.2 percent. Retrieval-only results across 24 synthetic coding histories.</desc>
<line x1="50" y1="20" x2="70" y2="20" stroke="#b24a2a" stroke-width="3"/><text x="76" y="25" font-size="15" fill="#1b1814">128 tokens</text>
<line x1="182" y1="20" x2="202" y2="20" stroke="#305f91" stroke-width="3"/><text x="208" y="25" font-size="15" fill="#1b1814">256 tokens</text>
<line x1="314" y1="20" x2="334" y2="20" stroke="#39856b" stroke-width="3"/><text x="340" y="25" font-size="15" fill="#1b1814">512 tokens</text>
<line x1="55" y1="280.0" x2="438" y2="280.0" stroke="#d8d2c7"/><text x="46" y="285.0" text-anchor="end" font-size="15" fill="#1b1814">0</text>
<line x1="55" y1="226.25" x2="438" y2="226.25" stroke="#d8d2c7"/><text x="46" y="231.25" text-anchor="end" font-size="15" fill="#1b1814">25</text>
<line x1="55" y1="172.5" x2="438" y2="172.5" stroke="#d8d2c7"/><text x="46" y="177.5" text-anchor="end" font-size="15" fill="#1b1814">50</text>
<line x1="55" y1="118.75" x2="438" y2="118.75" stroke="#d8d2c7"/><text x="46" y="123.75" text-anchor="end" font-size="15" fill="#1b1814">75</text>
<line x1="55" y1="65.0" x2="438" y2="65.0" stroke="#d8d2c7"/><text x="46" y="70.0" text-anchor="end" font-size="15" fill="#1b1814">100</text>
<text x="60" y="305" text-anchor="middle" font-size="15" fill="#1b1814">0</text>
<text x="134" y="305" text-anchor="middle" font-size="15" fill="#1b1814">2</text>
<text x="245" y="305" text-anchor="middle" font-size="15" fill="#1b1814">5</text>
<text x="430" y="305" text-anchor="middle" font-size="15" fill="#1b1814">10</text>
<polyline points="60.00,193.40 134.00,232.22 245.00,232.22 430.00,232.22" fill="none" stroke="#b24a2a" stroke-width="3"/>
<circle cx="60.00" cy="193.40" r="4" fill="#b24a2a"/>
<circle cx="134.00" cy="232.22" r="4" fill="#b24a2a"/>
<circle cx="245.00" cy="232.22" r="4" fill="#b24a2a"/>
<circle cx="430.00" cy="232.22" r="4" fill="#b24a2a"/>
<polyline points="60.00,127.71 134.00,142.64 245.00,217.29 430.00,217.29" fill="none" stroke="#305f91" stroke-width="3"/>
<circle cx="60.00" cy="127.71" r="4" fill="#305f91"/>
<circle cx="134.00" cy="142.64" r="4" fill="#305f91"/>
<circle cx="245.00" cy="217.29" r="4" fill="#305f91"/>
<circle cx="430.00" cy="217.29" r="4" fill="#305f91"/>
<polyline points="60.00,65.00 134.00,70.97 245.00,97.85 430.00,163.54" fill="none" stroke="#39856b" stroke-width="3"/>
<circle cx="60.00" cy="65.00" r="4" fill="#39856b"/>
<circle cx="134.00" cy="70.97" r="4" fill="#39856b"/>
<circle cx="245.00" cy="97.85" r="4" fill="#39856b"/>
<circle cx="430.00" cy="163.54" r="4" fill="#39856b"/>
<text x="248" y="335" text-anchor="middle" font-size="16" fill="#1b1814">Extra copies of one memory</text>
<text x="15" y="178" text-anchor="middle" transform="rotate(-90 15 178)" font-size="15" fill="#1b1814">Required facts in context (%)</text>
</svg>
<figcaption>Same information, more copies. Each line is a different allowance for recalled memory. These are retrieval results, not measured coding success.</figcaption>
</figure>

With a 512-token allowance, the clean histories supplied every required fact. Ten extra copies reduced that to about 54%. More space delayed the crowding; it didn't make repeated text free.

The average also hides differences between tasks. At the primary allowance, three histories didn't pack any additional copies into context. Their duplication had no opportunity to displace evidence. Where copies did enter, their rank and length mattered. Counting duplicates alone wasn't enough to predict the outcome.

This was a controlled stress test, not a measurement of my daily failure rate. The histories shared six templates, the status notes were worded to be relevant to a handoff, and the retriever used plain similarity ranking. The result doesn't establish how often natural repetition causes problems, or whether Hindsight's retriever behaves this way. The paired analysis and its sensitivity checks are described in the notes.[^analysis]

But it gave me a concrete failure to look for: **a memory excerpt can be relevant to the project and still omit the decisions needed to work on it.**

That explains why I care about repeated context. It doesn't make deleting real history as simple as undoing a synthetic experiment.

## Cleaning up without throwing away the evidence

Back in the cleanup I'd done before this experiment, removing repeated text also meant preserving where it came from. Two copies of a sentence can point to different sources. Similar sentences can describe different projects. An old decision and its replacement can look almost identical while giving the assistant opposite instructions.

So the cleanup wasn't an invitation for an LLM to decide what I should forget. I used an explicit list of approved records. For duplicate conclusions, I kept a surviving copy and attached the removed copies' source information to it.

The result was 3,881 approved duplicate and test records removed. Repeated wording no longer needed repeated records, but the surviving conclusions retained the sources I'd collected.[^cleanup]

Before applying it, I backed up the database and rehearsed the deletion in a transaction that rolled back. Afterward, I checked through the API that the intended targets were gone and the retained text and merged source information were intact.

Those checks answered whether the cleanup did what I intended. The later study asked whether repetition could prevent a fresh session from receiving the evidence needed to continue a task. It didn't establish that my production answers improved.

The distinction matters for the setup I kept. I want to preserve enough history to trace a conclusion without automatically putting all of that history in every conversation.

## The Hindsight setup I landed on

The arrangement I verified after the move separates current memory from historical archives, and personal context from project context.[^audit]

| Part | What it does |
|---|---|
| Hermes capture | Saves new conversational memory into a personal bank. |
| Codex capture | Saves new project memory through its native Stop hook into the current project's bank. |
| Automatic recall | Supplies personal and applicable project context; historical archives are added only through explicit mappings. |
| Hindsight storage | Keeps the data locally in PostgreSQL with pgvector. |
| Model work | Uses Ollama Cloud `gpt-oss:120b` for generation, with local embedding and reranking models. |

For the local retrieval models, that setup used `BAAI/bge-small-en-v1.5` and `cross-encoder/ms-marco-MiniLM-L-6-v2`. The handoff study used a different embedding model and a simpler retriever, not this production pipeline. Local storage also doesn't mean all processing stays local: the generation path uses a cloud service.

The archive mappings matter more to me than the model list. Codex can receive the historical archive matched to its project, not every archive I happen to own. Hermes receives the historical personal archive. Archives without an unambiguous mapping remain available for explicit search rather than automatic inclusion.

There is still glue to maintain: a Hermes provider extension and a local Codex bridge connect the historical recall paths. Client upgrades can change their behavior. I don't regard a running service or a successful write request as proof that the whole path works.

My check is small: save a made-up fact, ask for it in a fresh session, and inspect what context actually arrived. When it fails, that trace tells me whether to investigate capture, routing, a deadline, or retrieval before blaming the model.

I moved because I was tired of babysitting memory. I still have a system to maintain, but I have better questions to ask of it: was the fact captured, did it reach the right session, and what else competed for its place in the context?

I don't need six reminders that we're working on a project. I need the next session to remember what we decided.

## Related reading

- [How to evaluate AI agent memory](/notes/evaluating-agent-memory/): A reproducible fixture separates retrieval, source validity and answer correctness.
- [Agent memory: a practical guide](/agent-memory/): Follow the lifecycle from capture and corrections to retrieval and answer use.
- [My earlier Honcho and Mem0 comparison](/notes/honcho-vs-mem0-two-memory-layers-two-architectures/): The July architecture context behind the system I later migrated.
- [Provenance and perspective in agent memory](/notes/agent-memory-needs-a-point-of-view/): Why preserving a record’s source and access scope matters beyond retrieval relevance.

PK

[^migration]: Private migration receipt, September 11, 2026. Exact-text verification covered 8,455 conclusions in 13 historical banks. The source Honcho API container was stopped to end a failed restart loop; its original data volume and encrypted backup were preserved. This describes my installation, not a general reliability claim about Honcho.
[^audit]: Private installation audit, September 11-12, 2026. Direct recall exposed a saved fact missed by a Codex session; the approximately three-second deadline was shorter than archive searches taking roughly ten seconds. Subsequent fresh CLI checks passed shared recall. The setup above describes the audited migration configuration. A final desktop check was user-confirmed rather than independently observed. Backups, routing and client behavior remain separate operational responsibilities.
[^cleanup]: Private cleanup receipt and API verification, September 13, 2026 UTC. Approved removals: 3,827 duplicate archive records, 48 test-bank records, and six test markers. Verification checked target absence, retained text, and 3,817 merged provenance bundles. Restoring the cleanup backup into a database was not tested. This was not secure erasure of original conversations or backups.
[^experiment]: Controlled synthetic coding-handoff study: 24 main tasks, four variants in each of six shared templates; three memory conditions; two responses per task and condition. All 144 main calls completed on the reported model `gpt-oss:120b` through Ollama Cloud. An excluded six-task development run produced 18 responses. Local `qwen3-embedding:0.6b` supplied vectors for flat cosine ranking. Whole records were packed greedily into a 256-token memory allowance counted with `o200k_base`; query, prompt, options and budget were held fixed within each task. Temperature 0.2, low thinking effort and two fixed requested seeds. Tasks, targets, scoring and schedule were frozen before main generation. Each history contained three required facts, a routine status note and 17 distractors. The retrieval-only grid varied 0/2/5/10 copies and 128/256/512-token allowances across raw and deduplicated histories. It produced 576 selection evaluations, not additional model answers. Structured handoff decisions and citations were scored, not code execution. Protocol, source fingerprints, vectors, requests, responses and independent rescoring were retained.
[^analysis]: Responses were averaged within tasks before comparison. Deduplication recovered complete handoffs in eight tasks, worsened none and left 16 unchanged: a 33.3-percentage-point paired recovery. A 10,000-resample bootstrap within template-by-repetition-role cells gave a 25.0 to 41.7-point sensitivity interval; leaving one template out gave effects from 20 to 40 points. These describe sensitivity within a small constructed task set, not population efficacy or statistical significance. Clean and deduplicated prompts were byte-identical. Across both responses per task, correct option-label selections for available facts were 100/102 clean, 41/42 repeated and 102/102 deduplicated; one repeated-condition answer gave the right wording instead of its required label. All absent fields received UNKNOWN. The configuration example was chosen after analysis to illustrate a completeness loss, not as another independent result.
