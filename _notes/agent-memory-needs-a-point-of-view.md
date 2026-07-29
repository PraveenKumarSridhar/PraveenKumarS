---
title: "Agent Memory Needs a Point of View"
description: "Agent memory breaks when it stores one person's belief as a global fact. Multi-agent systems need observer, audience, source, and access scope."
date: 2026-07-29
tags: [agent-memory, multi-agent-systems, epistemic-logic]
---

In a private conversation, Alice says, "The launch is October 17. I think Bob already knows." A memory extractor stores: "Bob knows the launch is October 17."

Later, Bob asks the agent for the launch date. Retrieval finds a close match, the record names Bob, and the agent answers confidently. The trace looks healthy. The answer is still unsafe.

This is a constructed example, but the failure is concrete. Alice's statement established her belief about Bob. It did not establish Bob's knowledge, Bob's access, or permission to disclose the date.

The system changed the claim before vector search, ranking, or generation had a chance to help.

Flattening a perspective into a fact is a semantic write error.

## TL;DR

- Similarity does not preserve point of view.
- Belief, evidence-backed knowledge, and world-state claims are different memory objects.
- Contradictions between observers may be valid state, not duplicate noise.
- Retrieval needs an asker, audience, observer, source, modality, confidence, access boundary, and time.

## One sentence, four different memories

Epistemic means "who knows or believes what." A small amount of notation makes the launch sentence less ambiguous:

```text
p            the launch is October 17
B_A(p)       Alice believes the launch is October 17
K_B(p)       Bob knows the launch is October 17
B_A(K_B(p))  Alice believes Bob knows the launch is October 17
```

`p` is a claim about the world. `B_A(p)` is Alice's belief, which may be wrong.

`K_B(p)` is stronger: in the standard formal model, knowledge is factive, so Bob can know `p` only if `p` is true. `B_A(K_B(p))` is a higher-order belief, Alice's view of Bob's knowledge, not Bob's own state.[^1]

A production system rarely observes knowledge directly. It sees messages, acknowledgements, source documents, access events, and other evidence. Calling a record "known" should therefore require a policy for what evidence is sufficient, not an extractor's confident wording.

| Memory object | What the record means | What it can support |
|---|---|---|
| World state | The launch is October 17 | Action if a current authoritative source supports it |
| Belief | Alice believes the launch is October 17 | Personalization or reasoning about Alice |
| Evidence-backed knowledge | Bob acknowledged an authorized launch notice | A scoped claim that Bob knows, subject to the evidence policy |
| Higher-order belief | Alice believes Bob knows the date | Reasoning about Alice's model of Bob |
| Common knowledge | A qualifying group announcement established shared awareness | Reasoning that depends on everyone knowing, and knowing that everyone knows |

Common knowledge is stronger than a collection of independent private observations. It requires recursively shared awareness, so a public channel alone does not establish it.

The system still needs rules for which announcements qualify and which participants received them. All five records can land near each other in embedding space, but they do not license the same answer or action.

## Follow the launch-date failure end to end

The unsafe ingestion path creates a record with no remaining point of view:

```json
{
  "memory": "Bob knows the launch is October 17"
}
```

When Bob asks, semantic retrieval correctly returns it. Generation then treats the retrieved sentence as usable context. The system has no field left that can reveal Alice as the speaker, distinguish belief from knowledge, trace the private source, or enforce its audience.

A **proposed design contract** preserves the modeling direction and the policy inputs. This is a conceptual object, not a claim about fields exposed by an existing product:

```json
{
  "content": "Alice believes Bob knows the launch is October 17",
  "observer_id": "alice",
  "observed_id": "bob",
  "source_id": "private-session-42",
  "modality": "reported_belief",
  "confidence": 0.78,
  "audience": ["alice"],
  "access_scope": "launch-core",
  "valid_at": "2026-07-12T18:00:00Z",
  "supersedes": null
}
```

The same semantically relevant record should produce different behavior under different response contexts:

```text
SAME RETRIEVED RECORD
"Alice believes Bob knows the launch date"
source: private-session-42
scope: launch-core

ASKER: ALICE         | ASKER: BOB
audience allowed     | audience not established
return belief with   | relevance is not permission
attribution + source | verify or abstain
```

Retrieval can return the record in both cases without pretending the query is settled. The response policy then separates two decisions: is the claim valid under the relevant participant's perspective, and may the system disclose it to this audience? Evidence can support the first without granting the second. Knowing a secret and being authorized to receive it are different states.

## Disagreement can be the correct state

Suppose Alice believes the database migration is Friday and Bob believes it moved to Monday. Both are valid records of participant state. Neither proves the current migration date.

A flat memory layer can keep the latest string globally, merge both into an incoherent summary, or delete one as a contradiction. Each option destroys useful information.

A perspective-aware layer preserves both beliefs, then maintains a separate world-state claim if a stronger source, such as an approved change record, supports one date. Alice's later correction can supersede her earlier belief without rewriting what Bob believed or erasing the provenance of the update.

This is not only a constructed edge case. GroupMemBench explicitly evaluates speaker-grounded belief tracking in multi-party conversations. Its strongest evaluated system reached 46.0% average accuracy, while a BM25 baseline matched or exceeded most agent-memory systems.[^2]

That result does not prove a specific schema is sufficient. It shows that group memory remains difficult even when the asker and speaker structure are part of the task.

## Retrieval needs a point of view

A storage schema cannot carry the entire policy. Query behavior needs a contract too:

```text
query + asker + audience + observer + source
      + modality + confidence + access boundary + time
```

Each field changes a decision:

| Field | Decision it changes |
|---|---|
| Asker | Whose context is relevant to the query? |
| Audience | What may be disclosed in this response? |
| Observer | Whose model produced the claim? |
| Source | Can the claim be traced, verified, and contested? |
| Modality | Is it asserted, believed, inferred, known, or reported? |
| Confidence | Is it based on weak inference or direct evidence? |
| Access boundary | Does relevance also carry permission for this audience? |
| Time | Has a newer claim superseded it without erasing its history? |

> Semantic relevance answers "what sounds related?" It does not answer "whose claim is this, and may I use it here?"

A recent preprint, *Governed Shared Memory for Multi-Agent LLM Systems*, describes and evaluates its authors' production service rather than establishing independent consensus. It identifies unauthorized leakage, stale propagation, contradiction persistence, and provenance collapse, then proposes scoped retrieval, temporal supersession, provenance tracking, and policy-governed propagation as corresponding system primitives.

The authors also report that tenant isolation held while a direct GET-by-ID path initially bypassed sub-tenant scope for agent-scoped credentials, a flaw they say they remediated during the study.[^3] The connection to runtime behavior is direct: scope filters candidates, supersession keeps stale beliefs historical, provenance preserves the writer and derivation, and propagation policy limits recipients. Perspective metadata supplies inputs to those controls; it does not replace them.

## The minimum design test

These are design tests, not a benchmark claim:

1. **Private belief:** A statement from Alice does not become a fact available to Bob.
2. **Conflicting belief:** Alice and Bob can hold incompatible views without one being silently deleted.
3. **Belief update:** Alice's new belief supersedes her old belief while preserving provenance.
4. **Higher-order belief:** Alice's belief about Bob is not rewritten as Bob's own belief or knowledge.
5. **Common knowledge:** A qualifying group announcement is represented differently from independent private observations.

The private-belief test can already be written as an acceptance fixture:

```text
GIVEN Alice states p in a private session
AND   the stored modality is reported_belief
WHEN  Bob asks whether p is true
THEN  retrieval may find the record
BUT   the response must not disclose p
AND   Alice, source, scope, and history remain intact
```

This is the bridge to a later implementation or evaluation artifact, not evidence of benchmark performance. If a memory design cannot represent the five cases without flattening them, better retrieval will not recover the lost distinctions.

> Storing an `observer_id` is the beginning, not the whole solution. If retrieval ignores observer, source, modality, audience, and access scope, the system preserves perspective at rest and erases it again at use time.

## The relevant record was not the problem

Bob's question did not require a less relevant record. It required the system to interpret the relevant record correctly, preserve Alice's point of view, verify the evidence, and enforce the disclosure boundary.

My earlier Honcho versus Mem0 article introduced `(observer, observed)` as an architectural difference. This article explains the semantic failure the tuple is trying to prevent.

> A memory object is incomplete until the system can answer who holds the claim, what supports it, when it applied, and who may use it.

PK

[^1]: Stanford Encyclopedia of Philosophy, ["Epistemic Logic"](https://plato.stanford.edu/entries/logic-epistemic/), sections 2.1, 2.2, 2.6, and 3.2.
[^2]: Yang et al., ["GroupMemBench: Benchmarking LLM Agent Memory in Multi-Party Conversations"](https://arxiv.org/abs/2605.14498), arXiv:2605.14498v2, 2026.
[^3]: Margalit et al., ["Governed Shared Memory for Multi-Agent LLM Systems"](https://arxiv.org/abs/2606.24535), arXiv:2606.24535v1, 2026.
