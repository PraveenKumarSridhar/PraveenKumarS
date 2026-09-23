# Evidence-gated editorial queue

The technical/content PR is one release. Later topics depend on additional evidence and post-release measurement, not a fixed article quota. No scheduled automation or public posting is implied by this document.

## Ranked next experiments

| Rank | Question | Required evidence before writing results | Decision rule |
| --- | --- | --- | --- |
| 1 | Does a scoped correction change a fresh agent session's answer? | Fixed reader/model version, traced capture and injection, independently reviewed histories, paired no-memory/memory outputs | Publish if the trace explains success and failure across more than one wording; report all cases |
| 2 | How much does repeated low-value memory displace useful evidence? | Fixed token budgets, several history lengths, deduplicated and raw conditions, reader outcomes | Extend the existing study only with a distinct mechanism or workload, not a restatement |
| 3 | When does forgetting reach derived profiles and guidance? | Explicit deletion contract, inventory of affected representations, fresh-session checks and unresolved paths | Publish bounded observations; never infer erasure from absence in one search |
| 4 | Which failure cases distinguish framework integrations? | Same tasks, reader, budget and permissions; pinned versions; actual end-to-end traces | Compare observed behavior and cost, avoiding vendor-score rankings |

This ranking reflects available technical context and distinct reader questions. Query-level demand is unavailable in the initial Search Console sample. Re-rank after two complete monthly windows with usable query data, plus qualitative feedback.

## Guide gates

- `/agent-evaluation/`: retain in the plan until the current memory-evaluation article, evaluation-integrity note and at least one real-reader follow-up supply enough original examples. Cover task success, trajectories, tools, memory, reliability, attribution, integrity, online/offline/human evaluation and tooling. Require the same editorial rubric and browser checks. A generic list of eval types does not meet the gate.
- `/agent-knowledge/`: defer until unique evidence distinguishes knowledge maintenance from the existing memory guide. Repackaging the same definitions would create a thin page.
- Eight to twelve supporting articles is a planning aspiration, not a publication requirement. A failed or inconclusive experiment can be useful if its design and limits answer a concrete question.

## Measurement windows

At merge: record SHA, deployment timestamp and changed routes. Verify live canonical URLs, feed, sitemap and article schema before promotion.

After the first complete 28 post-deployment days: compare matched windows using `measurement.md`. Inspect indexing and query intent before changing titles. Account for low counts and concurrent new content.

After a second monthly window: choose the next experiment using query relevance, technical feedback and evidence readiness. Record relevant citations, referring domains and inbound technical inquiries only when directly observed. An AI-search mention requires a captured prompt/result/date; it is not a stable ranking or attribution estimate.

## Profile copy for review

Full name: Praveen Kumar Sridhar.

Short bio: Machine learning engineer and data scientist working on AI agents, agent memory and evaluation. Technical notes and experiments at praveenks.com.

Longer bio: I'm Praveen Kumar Sridhar, a Vancouver-based machine learning engineer and data scientist. I work on AI agents and evaluation, and write about memory, retrieval quality and what makes agents reliable over time.

These are proposed consistency edits only. External profiles have not been changed. Article distribution drafts remain under `distribution/`; posting or outreach requires user authorization and a working live canonical.
