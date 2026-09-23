---
title: "How to Evaluate AI Agent Memory: Metrics, Failure Modes & Benchmarks"
description: "A reproducible ten-case memory evaluation shows why retrieval, temporal validity, provenance and task correctness need separate scores. Includes code and failure cases."
date: 2026-09-23
tags: [agent-memory, ai-evals, retrieval]
---

A memory system can retrieve the right record and still give the wrong answer. It can also cite the wrong answer perfectly.

In the small synthetic fixture below, a token-overlap selector retrieves **6 of 7 relevant records**. The reader produces **4 correct outcomes in 10 cases**. Every answer cites a record containing exactly what it says. Some of those records are stale, untrusted or outside the user's access scope.

Those numbers describe ten constructed cases and a deterministic reader. No language model or memory framework was benchmarked. The point is to make the scoring boundaries inspectable before introducing a model that can blur them.

## What are we measuring?

Memory evaluation needs at least three units of observation: the evidence selected, the evidence delivered, and the answer or action produced. Keep the original history available so you can diagnose errors introduced during extraction or consolidation.

```text
History -> Stored claims -> Selected evidence -> Prompt context -> Answer
              |                  |                   |              |
         write validity     precision/recall    exposure trace   task score
              |                  |                   |              |
              +------ source, scope and time must survive ----------+
```

A search result is not proof of prompt exposure. Prompt exposure is not proof that the answer depended on the memory. If a user supplies the same fact in the current question, a correct answer may say little about memory at all. Use matched runs and explicit traces to distinguish these cases.

The [agent memory guide](/agent-memory/) covers the lifecycle and a scoped-correction example. Here the question is how to turn those boundaries into a test.

## A fixture you can actually inspect

The [code, cases and complete outputs](https://github.com/PraveenKumarSridhar/PraveenKumarS/tree/main/examples/memory-evaluation) contain ten synthetic histories. Each case specifies the query time, audience, relevant and permitted evidence IDs, invalid records, expected facts and a short label rationale.

| Case | Required behavior |
| --- | --- |
| Stable preference | Recover an earlier preference despite later status messages |
| Corrected preference | Use the correction instead of the earlier preference |
| Expired fact | Abstain after a launch date is cancelled without replacement |
| Contradiction | Preserve two conflicting reports and decline to invent a resolution |
| Provenance | Distinguish an explicit user statement from an assistant guess |
| Private scope | Do not expose another user's synthetic secret |
| Irrelevant repetition | Recover a decision buried under repeated status updates |
| False memory | Reject an unverified imported claim that conflicts with a trusted source |
| Explicit forgetting | Stop using a preference after the user withdraws it |
| No evidence | Abstain when the history does not answer the question |

The labels were written before running the selectors. They encode a particular contract. For example, “forget” means exclusion from active use in this fixture; it does not claim erasure from backups. The false-memory case models an invalid imported claim, not an executed prompt-injection attack.

Two selectors retrieve two records each. **Latest two** takes the newest records. **Token overlap** ranks by distinct query/text token overlap, with a fixed stopword list and newest-first ties. Both use the same reader: return the first selected record containing the requested structured key, or abstain if none does. Neither selector reads the labels or enforces access and validity rules.

A third condition, **gold oracle**, reads the answer labels directly. It checks the scoring ceiling. It is not a deployable system and should not appear in a performance leaderboard.

Run from the repository root with Python 3.9 or later:

```sh
python3 -m unittest discover -s examples/memory-evaluation -p 'test_*.py'
python3 examples/memory-evaluation/evaluate.py \
  --cases examples/memory-evaluation/cases.jsonl \
  --baseline overlap --output /tmp/overlap.json
```

Use `latest` or `oracle` for the other conditions. The README documents a predictions interface for replacing the selector and reader. Tests compare regenerated results with the checked-in outputs and separately check hand-derived success sets and counts.

## Keep the denominators visible

Let **R** be the retrieved evidence IDs and **G** the gold relevant IDs for a case. Retrieval precision is `|R ∩ G| / |R|`; recall is `|R ∩ G| / |G|`. Across this fixture, sum the numerators and denominators before dividing. That is micro aggregation, not an unweighted average of per-case rates.

| Metric | What counts |
| --- | --- |
| Retrieval precision | Relevant retrieved IDs divided by all retrieved IDs |
| Retrieval recall | Relevant retrieved IDs divided by all relevant IDs |
| Stale use | Stale used IDs divided by all used IDs |
| Scope exposure | Out-of-scope retrieved IDs divided by all retrieved IDs |
| Scope use | Out-of-scope used IDs divided by all used IDs |
| Unsupported claims | Claims without matching, current, trusted, permitted cited evidence divided by all answer claims |
| Provenance accuracy | Claims whose cited record contains the exact fact divided by all answer claims |
| Task correctness | Exact expected answers with valid evidence use divided by all cases |

A zero denominator is reported as `null`. It does not earn a perfect score. Missing predictions, duplicate IDs and unknown evidence IDs fail validation instead of disappearing from the sample.

Report abstention separately: correct empty answers divided by cases where an empty answer is required. Also report correctness among answerable cases. Otherwise, a conservative system can look good simply because a dataset contains many unanswerable questions.

The “unsupported” label here includes claims backed by an invalid source. It is stricter than “the words appeared somewhere.” Provenance accuracy deliberately asks the narrower question of whether the citation matches the claim.

## Results: the citation can be right while the answer is wrong

| Condition | Precision | Recall | Correct outcomes | Stale uses | Matching source citations |
| --- | --- | --- | --- | --- | --- |
| Latest two | 5/20 | 5/7 | 2/10 | 2/7 | 7/7 |
| Token overlap | 6/20 | 6/7 | 4/10 | 3/9 | 9/9 |
| Gold oracle | 7/7 | 7/7 | 10/10 | 0/5 | 5/5 |

Dataset SHA-256:

```text
8fe7520ac6f42d8ab5d81ceda3e9efc4bd589c94546717eadea90e5bacb621f3
```

There are seven relevant IDs because the unresolved contradiction has two relevant reports, while five answerable cases have one each. Both non-oracle selectors retrieve twenty IDs across ten cases. The oracle returns only the seven labeled relevant records and abstains on the unresolved conflict.

The overlap selector recovers the stable preference and the decision buried under repetition. But the old preference says “preferred programming language for examples,” closely matching the query. The correction says “use Rust from now on.” The selector ranks the old Python statement first. The reader follows it and cites it accurately.

That failure belongs to temporal validity and answer use. Calling it a citation failure would send the repair to the wrong component.

Both selectors also retrieve the out-of-scope record. Scope exposure is **1/20** for each. Whether the reader ultimately leaks it is a separate score. An access check belongs before private content is handed to a reader, not only in an instruction asking the reader to ignore it.

These differences are observations within an intentionally small teaching fixture. There are no confidence intervals or significance claims, and the oracle's perfect result comes from reading the labels.

## Add failure tests before adding more memories

**Temporal correctness and personalization.** Test what is true at the query time and in the relevant project or audience. A scoped exception need not overwrite a global preference. Keep historical questions distinct from current-state questions. Report correction-following accuracy over cases containing corrections, not over every easy preference case.

**Contradictions.** Define what counts as unresolved conflict and what the application should do. You can measure invalid resolution as cases where the answer invents certainty divided by unresolved-conflict cases. Also inspect the write path: silently dropping one report can make retrieval look clean while destroying the conflict. The fixture includes one such abstention case, not an estimate of a general contradiction rate.

**Memory pollution and false claims.** Add repeated irrelevant records while holding the useful evidence and context budget fixed. Separately introduce claims from untrusted sources. Repetition tests competition for space; false claims test admission and trust. They should not be collapsed into one “noise” condition. [The Honcho-to-Hindsight study](/notes/from-honcho-to-hindsight/) explores context competition in a different, model-based synthetic handoff setup.

**Provenance.** Preserve who said something, who it concerned and whether it was a report or an inference. A copied assistant guess is not another independent source. [The point-of-view note](/notes/agent-memory-needs-a-point-of-view/) explains why observer and audience information must survive storage and retrieval.

**Forgetting.** Test every representation covered by the promise: active search, profiles, summaries, caches and new sessions. A raw record disappearing does not prove that a derived rule disappeared. Secure deletion is a separate contract that this example does not evaluate.

## Move from a toy to a benchmark

Build histories around explicit tasks, then have someone other than the system builder review the labels. Include ambiguous cases and a clear escalation policy. Split by underlying scenario or user, not just by paraphrase, so near-duplicate histories do not cross development and evaluation sets.

Vary history length, correction distance, distractor density, audience and query time. Keep the task's gold state independent of the system's extraction output. Otherwise, a write-time omission can disappear from the supposed ground truth.

LongMemEval separates abilities such as information extraction, cross-session reasoning, temporal reasoning, updates and abstention. LoCoMo studies long conversational memory through tasks including question answering and event summarization. Use these as complementary external task definitions, while retaining application-specific permission and lifecycle cases. [LongMemEval](https://arxiv.org/abs/2410.10813), [LoCoMo](https://arxiv.org/abs/2402.17753).

Benchmark integrity also matters. Freeze labels and scoring before the main run, record model and tool versions, and prevent access to answer files. A correct answer obtained through forbidden access is an invalid observation. [Evaluation integrity and reward hacking](/notes/when-competence-attacks-its-measurement/) examines that distinction in a reported incident.

## Measure usefulness through task impact

Offline evaluation gives reproducible histories and controlled comparisons. Online evaluation reveals real correction patterns, latency, cost and user behavior, but introduces changing tasks and exposure. Keep their conclusions separate.

For a model-based offline test, compare matched no-memory and memory conditions on the same task. Hold the reader, instructions, tool access and context budget fixed. Repeat stochastic generations and analyze at the task or user level rather than treating repeated responses as independent users. Inspect whether the evidence entered the prompt before attributing an outcome to memory.

For an online test, define a task outcome the user cares about, such as completing a valid handoff without asking again for already supplied constraints. Randomize at a level that avoids memory crossing conditions, and monitor disclosure errors and stale use alongside success, latency and cost. The appropriate unit depends on whether state is shared by user, team or project.

A practical release check is small:

1. Can a correction reach a fresh session and change the relevant answer?
2. Can the trace explain the source, scope and date of each consequential claim?
3. Can the system abstain when evidence is absent, conflicting or forbidden?
4. Does memory improve the task under the same resource budget?
5. Can the same checks catch a deliberately broken implementation?

Retrieval scores help locate a failure. They do not replace the last question: did the system use memory in a way the task actually permits?
