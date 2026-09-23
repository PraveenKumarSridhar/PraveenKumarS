---
layout: note
title: "Agent Memory: A Practical Guide to State, Retrieval and Evaluation"
description: "Design agent memory from capture to answer use: corrections, provenance, retrieval, forgetting and evaluation, with a worked example and architecture tradeoffs."
image: /assets/social-card.png
guide: true
seo:
  type: WebPage
---

Agent memory is the state an agent carries between interactions, plus the rules that decide what enters that state and how it affects later behavior. A record existing in a database answers only one part of the engineering question. The useful test is whether the right evidence reaches the right task and changes the answer appropriately.

This guide organizes the design around those boundaries. The worked example is constructed. The linked case studies describe specific installations or investigations, with their own limits.

## Follow the memory all the way to the answer

```text
Interaction
    |
    v
Capture -> Admit and store -> Retrieve -> Inject -> Answer or action
              |                 |           |             |
         source, scope,     selected IDs  prompt IDs   observed use
         time, revision
              ^                                           |
              +---------- correction or forgetting -------+
```

These are distinct checks:

1. **Capture:** Did the event reach the memory pipeline, including after retries or a client restart?
2. **Admission and storage:** Did the saved claim preserve its source, subject, uncertainty and access scope?
3. **Retrieval:** Did the query select current, relevant, permitted evidence within the latency and token budget?
4. **Injection:** Did the selected evidence actually enter the model's request? A successful search can still lose its result to a timeout or context truncation.
5. **Use:** Did the answer follow the evidence correctly? Receiving a correction does not establish that the agent followed it.

Keep identifiers across these stages. A trace that records only the final answer cannot distinguish a missing memory from a reader that ignored it. [My migration from Honcho to Hindsight](/notes/from-honcho-to-hindsight/) includes a concrete recall-versus-delivery failure and a small synthetic study of context competition.

## Decide what kind of state you need

Start with the operation the next task needs to perform.

| Need | Useful representation | Main risk |
| --- | --- | --- |
| Resume an interrupted task | Session checkpoint and explicit task state | Resuming obsolete work |
| Remember a current preference | Small profile with source and revision | Turning a temporary choice into a permanent rule |
| Explain a past decision | Event records with dates and evidence | A summary erasing the reason or caveat |
| Reuse a successful procedure | Reviewed instructions with applicability conditions | Applying a lesson outside its original setting |
| Combine evidence across people | Claims with observer, subject and permitted audience | Treating someone's belief as shared truth |

These representations can coexist. LangGraph distinguishes thread-scoped state, persisted through checkpoints, from longer-lived data in namespaced stores. That is a useful implementation boundary; it does not decide which facts your application should retain. [LangChain memory documentation](https://docs.langchain.com/oss/python/concepts/memory).

For many applications, a few explicit fields are easier to inspect than unconstrained extracted prose. Add semantic search when the task needs recall over material that cannot reasonably fit into that small state.

## Worked example: a corrected preference

Suppose a user says on Monday, “Use Python for examples.” On Wednesday they say, “For this TypeScript project, use TypeScript examples. Keep Python for other projects.” On Thursday the agent writes an example for that project.

A global overwrite loses the general preference. Saving both sentences without scope leaves the reader to guess. One possible state is:

```json
[
  {
    "id": "preference-1",
    "subject": "user-17",
    "claim": "Use Python examples",
    "scope": "general",
    "source": "message-101",
    "effective_from": "2026-09-21"
  },
  {
    "id": "preference-2",
    "subject": "user-17",
    "claim": "Use TypeScript examples",
    "scope": "project-atlas",
    "source": "message-142",
    "effective_from": "2026-09-23",
    "overrides_in_scope": "preference-1"
  }
]
```

The dates and identities here are synthetic. The design preserves the correction as an explicit scoped relationship rather than declaring the earlier preference universally false.

For a Thursday Atlas request, retrieve `preference-2` and enough context to interpret its scope. Record which IDs were injected. Check that the generated example is TypeScript. For another project, test that Python still applies. For a question about Monday, preserve the ability to explain the earlier state.

A latest-timestamp rule alone cannot express all three answers. Scope and effective time are part of correctness, not optional search refinements. If two equally authoritative statements conflict in the same scope and period, keep the conflict visible and ask for clarification rather than inventing a winner.

## Admission, consolidation and forgetting

Before storing a candidate, distinguish an explicit user statement, an external document and an assistant inference. Repetition by the assistant should not turn one weak source into several independent confirmations. [Agent memory needs a point of view](/notes/agent-memory-needs-a-point-of-view/) works through this problem with observers, beliefs and disclosure boundaries.

For consolidation, separate current state from supporting history. Merging duplicate wording can reduce context competition, but combining records from different people or dates can destroy meaning. Preserve source IDs and the reason for supersession so that a correction can propagate to derived summaries.

Forgetting needs an explicit contract. Does a request remove a fact from active retrieval, delete its stored representations, or also remove source conversations and backups? These are different operations. Test the promised operation across search, profiles, summaries, cached prompts and a fresh session. Do not describe an inaccessible record as physically erased without evidence.

[The Muse investigation](/notes/muse-memory-investigation/) examines another distinction: historical reviews and current behavioral guidance can have different lifecycles. Its private exports describe an architecture; they do not prove every runtime or deletion path.

## Retrieval is a constrained selection problem

Similarity is one signal. Apply access restrictions and temporal validity before presenting evidence to a reader. Then measure what ranking and packing leave out.

A practical retrieval trace should include the query, candidate IDs, filtering reasons, ranking scores, selected IDs, token budget and elapsed time. Avoid logging sensitive text when identifiers and controlled inspection are sufficient. At injection time, record the IDs that survived prompt assembly.

Measure useful evidence under a fixed budget. A method that retrieves more relevant records by doubling context is answering a different resource question. Also test irrelevant repetition: frequent low-value records can crowd out a rare decision even when each record looks harmless on its own.

## Choose framework boundaries, then test your workload

The following describes documented interfaces, checked September 23, 2026. It is not a performance ranking or a head-to-head benchmark.

| System | Documented organizing idea | Integration question to test |
| --- | --- | --- |
| LangGraph | Thread checkpoints and namespaced long-term stores | Which state belongs to one run, and which may cross sessions? |
| Mem0 | Add and search memories with user scoping; optional graph memory | Do correction and scope rules survive extraction and retrieval? |
| Honcho | Workspaces, peers, sessions and messages; background reasoning produces peer representations | Can each retrieved inference be interpreted in the right peer context? |
| Hindsight | Retain, recall and reflect interfaces; recall combines several retrieval signals | Which path returns raw evidence, and which produces an answer from it? |

Sources: [LangGraph](https://docs.langchain.com/oss/python/concepts/memory), [Mem0 quickstart](https://docs.mem0.ai/platform/quickstart) and [graph memory](https://docs.mem0.ai/open-source/features/graph-memory), [Honcho overview](https://honcho.dev/docs/v3/documentation/introduction/overview), [Hindsight recall](https://hindsight.vectorize.io/developer/api/recall) and [API distinctions](https://hindsight.vectorize.io/faq).

Compare candidates on the same histories, query times, permitted evidence, reader model and budget. Keep extraction, retrieval and reader errors separate. A vendor benchmark score cannot establish that your client injects the returned context correctly.

## Evaluate corrections before accumulating more memory

Build a small test set from the behavior your application promises. Include stable preferences, scoped corrections, expired facts, conflicting reports, access boundaries, irrelevant repetition, false claims and explicit forgetting. Include questions where abstaining is correct.

For each case, label relevant evidence at the query time, allowed audiences, expected answer facts and unacceptable uses. Check retrieval precision and recall, but also stale evidence use, unsupported answers, disclosure violations and task correctness. Keep the denominators visible. A system can achieve high recall by returning everything and still fail the task.

LongMemEval tests several abilities, including temporal reasoning, knowledge updates and abstention. LoCoMo examines memory over long conversational histories. Their task definitions are useful starting points; neither replaces application-specific tests for your permissions and context pipeline. [LongMemEval paper](https://arxiv.org/abs/2410.10813), [LoCoMo paper](https://arxiv.org/abs/2402.17753).

Finally, compare matched runs with and without memory. Change one pipeline stage at a time, keep the rest fixed, and inspect failures before aggregating them. The question is whether memory improved the task under a defined cost and correctness contract. More stored facts are an inventory measure.

For runnable cases, metric definitions and observed failures, see [How to evaluate AI agent memory](/notes/evaluating-agent-memory/).
