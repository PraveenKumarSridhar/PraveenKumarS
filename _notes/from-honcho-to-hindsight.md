---
title: "I moved my AI's memory. Then I started deleting."
description: "An experiment in getting two AI agents to share a memory, moving 8,455 old conclusions, and deciding which baggage to leave behind."
date: 2026-09-13
tags: [agent-memory, experiments, reliability]
---

I told Hermes a made-up project code. A fresh Codex session recalled it. But another saved fact failed to reach Codex even though it was sitting in the database.

The code was a checksum for a fictional telescope project. Both assistants were connected to Hindsight, a memory system that saves information between conversations. Its automatic recall supplied context to Codex; Codex did not need to run a lookup tool or open a file. In a fresh CLI session, it returned the code Hermes had saved.

A nonsense string isn't much of a demo. But it was exactly what I wanted: tell one assistant something, switch to another, and stop explaining everything again.

That small success was part of a larger experiment. I was moving my agent memory from Honcho to Hindsight, taking 8,455 stored conclusions along. The move worked. It also gave me an excuse to look inside the thing I'd been calling "memory."

There were useful records, repeated conclusions, and leftover test records. Getting the data across was only the first decision. I still had to decide what the agents should use, what they should trust, and what I could safely remove.

## Two assistants, less repeating myself

I use Hermes and Codex as AI assistants. Honcho and Hindsight are separate memory systems: they keep information beyond a single conversation so an assistant can retrieve it later.

My goal was ordinary. If I explain a project's conventions in one session, I'd like the next session to start somewhere other than zero. I'd also like a detail from one project to stay out of another. Shared memory shouldn't mean every conversation gets every fact.

I'd previously [written about Honcho's architecture](https://praveenks.com/notes/honcho-vs-mem0-two-memory-layers-two-architectures/), particularly its ability to preserve whose perspective a conclusion came from. I still cared about that. For this experiment, though, I wanted to try Hindsight as the shared memory behind both assistants, with automatic capture during normal use.

This wasn't a benchmark declaring a winning vendor. It was a test of whether I could change the memory system without starting over.

## The database remembered. The assistant ran out of patience.

I had connected selected archives of older memories alongside the new ones. In one actual test, Codex missed a saved project fact even though a direct query to the memory API found it.

The client had a three-second request deadline. Historical searches were taking roughly nine to ten seconds. The fact wasn't missing. The caller had stopped waiting.

I changed the deadlines and ran current and historical searches concurrently. Later fresh-session checks passed. But a separate synthetic test found another problem in my integration: a slow archive lookup could prevent already-finished current-memory results from reaching the assistant.

The failure looked like this:

```text
Current memory: ready ----+
                         +--> wait
Old archive:   still busy+      |
                            timeout
                               |
                         no context
```

That's an unpleasant trade: adding access to old history could hide useful context I already had. Optional archive results should be allowed to arrive late without taking current memory down with them.

Another probe found a bookkeeping problem on the write side. The adapter marked a turn as handled when it queued the write, before delivery succeeded. When the test forced that write to fail, the next ordinary turn moved on without retrying it.

A later whole-session flush might resend the failed turn, so this wasn't proof of permanent data loss. It was proof that "queued" and "saved" needed different meanings.

These were findings in the integration I audited, including my own archive wrapper, not universal claims about Hindsight. They changed how I tested the experiment. Asking a fresh agent to recall a fact checked something that counting database rows couldn't.

## Keep the old conclusions identifiable

The old system held 8,455 conclusions. These weren't raw chat messages. They were records Honcho had already extracted or inferred from earlier conversations.

I wanted to preserve those records, not ask another model to take a fresh guess at what they meant. So I copied their exact text into 13 separate Hindsight archives (historical memory banks), along with where they came from, their dates, and whose perspective produced them. I labelled them historical inferences rather than new statements from me.

That last part matters. Imagine an old record saying, "This project probably uses Redis." Moving it into a new database shouldn't quietly upgrade *probably* into a fact. The example is invented; the distinction is why I kept the original text and source information.

Every conclusion survived verification against the export. I kept the original database and backups too.[^migration]

Then I connected selected archives to automatic recall. Importing an archive and letting it influence the next answer were separate steps. History with an unclear project owner remained available for explicit search rather than being injected into whichever conversation happened next.

By the end of the capture-and-recall checks, a fresh Codex CLI session could return both its own saved test fact and the one Hermes had saved.[^audit] That was the appealing part of the experiment: the assistants could share context without sharing the same conversation window.

## I had also moved the duplicates

Preserving everything had a predictable consequence: the repeated records came along too.

I started with a deliberately narrow cleanup. Within an archive, I looked for approved groups of conclusions whose text was identical after normalization. I also identified records created only for tests. I did not ask a model to judge which memories were "low value" or merge sentences because they sounded similar.

Even an exact-text match needs care. Two projects can both say "use Redis" without referring to the same decision. I kept the cleanup inside the approved archive boundaries.

For each duplicate group, I retained one record and attached the removed copies' source information to it. The active list got shorter, but I could still trace where the copies had come from.

```text
Before                 After
claim, source A --+
claim, source B --+--> one claim
claim, source C --+    sources A,B,C
```

This is the part of "forgetting" I found useful. I didn't need three active copies to preserve the fact that three source records had existed. Nor did those copies automatically count as three independent pieces of evidence.

I approved a fixed list of record IDs before deleting anything. New memories were arriving during the cleanup, so a moving instruction like "delete all duplicates" would have given the operation a different scope from the one I'd reviewed.

After a backup and a rollback dry run, I removed 3,881 approved duplicate and test records. A separate check through the API confirmed that the targets were gone, the intended survivors remained with unchanged text, and the merged source information was intact.[^cleanup]

Those removals covered the wider Hindsight installation, including test banks, not just the imported records. This was tidying a working system, not throwing away half the old history.

I can't claim the agents got smarter afterward. I didn't benchmark answer quality, and unchanged capture behavior could introduce duplicates again. What I could show was exactly what had been removed and what had survived.

## The experiment I'd repeat

The shared-fact test worked. The failure probes showed what that success hadn't tested: whether a failed write would be retried, or a slow lookup would block useful context.

If you're adding memory to an agent, you can try a small version of this without migrating thousands of records:

1. Give it a made-up fact it couldn't infer from general knowledge.
2. Open a fresh session and ask for the fact without allowing other lookup tools. If you use two clients, try the second one too.
3. In a test setup, interrupt a write or slow a lookup. Check whether the fact gets retried and whether available context still reaches the agent.
4. Remove the test fact using the system's supported controls, then check retrieval and a fresh session again. Ask what remains in source documents, caches, or backups.

That last step deserves as much attention as the first. My cleanup removed active memory records; it did not erase the original conversations or the backups. A privacy deletion request would need a broader operation.

I went into this wanting less repetition between assistants. I came out wanting a way to inspect a proposed cleanup before approving it: show me what you're keeping, what you're removing, and why. The one-off transaction did that job here; whether the cleanup improved answers is still an experiment to run.

For now, I have a better experiment than "does my AI remember me?" I can plant a fact, follow it into another session, interrupt its delivery, and check what remains after removal. And I can do it with a fictional telescope instead of trusting the system with something important first.

PK

[^migration]: The September 11, 2026 migration report verified exact text and source information for all 8,455 conclusions in 13 archives. It preserved source references as metadata rather than rebuilding Honcho's reasoning graph. The private source corpus is not published here.
[^audit]: The September 11-12 live audit records the cross-client recall tests and deadline failure. A separate source audit reproduced the archive timeout and failed-write behavior with synthetic probes. Passing fresh-session checks did not establish reliability under every interruption.
[^cleanup]: The September 13, 2026 cleanup log and independent API verification record 3,827 duplicate archive removals, 48 test-bank record removals, and six test-marker removals, with source information merged onto 3,817 retained records. The cleanup used a schema-specific PostgreSQL transaction because the installed API did not support the required merge-and-delete operation. Its backup passed a full archive read but was not restore-tested; an earlier migration snapshot was. This is an account of the experiment, not a general deletion recipe.
