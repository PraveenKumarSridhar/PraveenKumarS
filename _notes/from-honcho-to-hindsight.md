---
title: "From Honcho to Hindsight: 8,455 Records Survived, but the Behavior Did Not Transfer"
description: "I preserved 8,455 Honcho conclusions in Hindsight, then removed 3,881 approved duplicates and test records. The harder migration was the behavior around the data."
date: 2026-09-13
tags: [agent-memory, migrations, reliability]
---

In July, I [wrote about choosing Honcho's memory architecture](https://praveenks.com/notes/honcho-vs-mem0-two-memory-layers-two-architectures/). In September, I stopped its API container and moved all 8,455 of its conclusions into Hindsight. Every conclusion survived the import. Getting my agents to use that history correctly was a separate job.

Then I deleted 3,881 approved duplicate and test records from the destination system.

That sounds like an odd success story: preserve everything, then remove thousands of records. But the order mattered. I needed to know what I had carried over before deciding what should remain active. Neither a matching record count nor a smaller database could tell me whether the agent remembered correctly.

**The migration moved stored conclusions. Capture, scope, retry, recalled context, correction, and forgetting still needed their own tests.**

## I changed the requirement

Honcho's observer-aware model was still useful. My earlier [point-of-view article](https://praveenks.com/notes/agent-memory-needs-a-point-of-view/) argued that a conclusion needs to retain whose perspective produced it. Switching systems did not make that distinction disappear.

What I wanted from daily use had changed. I wanted passive continuity between Hermes and Codex: save useful state through normal conversation, recover it in a fresh session, and keep project history from becoming global personal context. I also wanted to inspect and recover the system without turning memory maintenance into another project.

Those priorities were in tension. My maintenance-first review initially favored a bounded trial of file-first memory. Hindsight became the conditional choice when automatic capture mattered enough to justify an extraction pipeline and PostgreSQL. It was not the winner on every axis.

In this installation, storage, embedding, and reranking ran locally; generation used Ollama Cloud. Calling it fully local would hide an inference dependency. Calling it maintenance-free would hide most of this article.

The distinction from my previous posts is practical. The first was about architecture, the second about the meaning of a stored claim. This one is about which guarantees survive a change of systems.

## Preserve first, activate separately

The migration deliberately avoided asking another model to reinterpret the old conclusions.[^migration]

```text
Honcho PostgreSQL
  | encrypted backup
  | scratch restore verified
  v
8,455 conclusions + provenance
  | exact text; no rewriting
  v
13 historical archive banks
  | explicitly mapped scopes only
  v
5,755 in automatic recall
2,700 in explicit search only
```

*Import and activation counts, before the later cleanup.*

I imported the conclusions in chunks mode, with archive consolidation disabled. Every record was labelled as a historical Honcho-derived inference, including records Honcho had classified as explicit. An old extractor's classification was worth preserving, but it was not permission to present the result as a fresh statement from me.

The import kept exact conclusion text, source IDs, observer and observed peers, workspace, session, reasoning level, and derivation metadata. Recorded-at timestamps became Hindsight timestamps; original message timestamps remained in source metadata. Identical text with different source IDs stayed distinct. At this stage, preservation took priority over deduplication.

Honcho's source references remained metadata. I did not reconstruct its reasoning graph in Hindsight. The archives' empty entity graphs were therefore expected, not evidence that the import had failed.

Verification checked every imported document and stored fact against the encrypted export, including text, provenance, labels, timestamps, and a searchable embedding. Recall samples passed in all 13 banks. Raw messages and queued work stayed in the source backup; I did not replay them through an extractor as new conclusions.

There was also an ordinary infrastructure failure. At record 6,953, a parallel PostgreSQL index build exceeded Docker's 64 MiB shared-memory mount. Disabling parallel maintenance workers fixed the failed operation on the database's one allocated CPU. The fix got the import moving again. It said nothing about whether Codex would receive the right context tomorrow.

Initially, none of these archives participated in automatic recall. A later routing pass connected four explicitly mapped scopes containing 5,755 records. The remaining 2,700 stayed available through explicit search. An unrelated project received no unrelated project archive. I preferred incomplete automatic coverage to guessing which project owned ambiguous history.

The original Honcho volume remained intact. Preservation gave me room to make these decisions without making the cutover irreversible.

## Healthy storage, broken client paths

After routing was connected, the backend audit reported zero pending and zero failed operations. Fresh-session canaries also passed. A separate source audit with synthetic probes still found defects in the installed client integration.[^audit]

These findings describe the audited snapshot, including my local archive wrapper. They are not a claim that every Hindsight deployment has these behaviors, or that the probes measured their frequency in production.

On the append-capable path, normal turn capture submitted a delta, but the session-switch flush submitted the whole buffered session. The probe reproduced resubmission of already queued turns. FIFO serialization kept writes in order; it did not make repeated payloads idempotent. This proved duplicate submission, not duplicate stored memories. I cannot attribute the later cleanup's duplicates to that mechanism.

The write path also advanced its watermark after enqueueing, before successful delivery. When a synthetic append failed, the writer logged the error and removed the job from its queue. The next ordinary turn sent only its own delta. The failed turn was no longer eligible for that normal retry path. A later whole-session flush might resend it, so the test did not establish permanent production loss.

Historical recall introduced another failure boundary. My composite provider held completed current-memory text while waiting for the archive branch. Under a synthetic outer timeout, the caller received neither. Increasing an inner request timeout does not help when an outer deadline stops waiting first. Optional history should degrade independently, without withholding current context that is already available.

Finally, the prompt could change a record's apparent authority. Native packing reduced recalled records to text bullets and dropped supplied IDs and dates. The archive helper labelled old conclusions historical and unverified, while the outer memory wrapper called the combined context authoritative reference data. Both messages reached the same prompt.

These failures lived in hooks, delivery bookkeeping, result assembly, and wording around retrieved text. A database export could not carry their intended guarantees. Backend health could not certify them either.

## A faithful import also preserves redundancy

The first destination inventory found 9,406 memory units across 33 banks. By execution, ongoing ingestion had raised that to 9,620. These totals covered the wider Hindsight installation, not just the imported Honcho archives.[^cleanup]

That moving count ruled out approving a query such as "delete whatever looks duplicated when this runs." The cleanup used a fixed manifest of exact record IDs, with explicit survivors and preconditions. New records outside that manifest remained untouched.

The approved changes were narrow:

| Removed category | Records |
|---|---:|
| Excess within-bank copies of normalized identical archive conclusions | 3,827 |
| Explicitly identified records in test-only banks | 48 |
| Synthetic test markers in normal banks | 6 |
| **Total removed** | **3,881** |

I did not authorize new semantic-similarity groups, cross-bank merges, or age-based deletion. Identical wording across different perspectives can still carry different meaning. The decision was to merge the approved within-bank groups while preserving the source information, not to declare matching sentences interchangeable everywhere.

Each group kept a deterministic canonical record. The removed copies' metadata, original wrapped text, dates, tags, and IDs were attached to 3,817 survivor provenance bundles. Repeated observers were not counted as independent evidence. This reduced active record duplication without pretending there had only ever been one source record.

The installed public API did not expose the exact hard-delete plus provenance-merge operation this plan required. I used one bounded PostgreSQL transaction after a rollback dry run and a full database backup. That was a schema-specific operation, not a portable recipe for deleting memories through Hindsight.

The transaction checked dependencies, remapped duplicate graph endpoints to survivors, and removed source documents only when they contained no retained or invalidated child memories. Two mixed source documents stayed because they also contained facts outside the approved deletion set.

The result I cared about was more specific than "DELETE succeeded."

| Independent post-commit check | Result |
|---|---:|
| Approved deleted IDs still present | 0 |
| Previous survivors missing | 0 |
| Previous survivor text changed | 0 |
| Canonical provenance bundles verified | 3,817 |
| Memory units remaining | 5,739 |

All 33 bank containers remained. The readback enumerated the live API after commit rather than trusting the transaction's exit status.

## What forgetting meant here

This was controlled forgetting of active memory records. Original conversations were not erased, and the backup deliberately retained deleted content. It was neither secure erasure nor machine unlearning.

Recovery evidence also had two different boundaries. The migration audit restored an encrypted Hindsight snapshot into a scratch database and matched all 8,455 archive documents by canonical-row hash. The later cleanup backup passed a full archive read, but I did not restore that backup into an isolated database. The earlier restore test does not certify the later artifact.

I did not benchmark retrieval quality before and after deletion. Fewer records do not establish better answers, lower latency, or less storage use, especially when provenance is preserved on survivors. Capture behavior was unchanged, so duplicates could recur.

The cleanup is evidence for a proposed tool, not a finished product: show an explained plan, identify what will survive, expose unsupported backend operations, and execute only the approved revision. Its useful output would be the verified result and a recovery path. An autonomous "delete low-value memories" loop would skip the decision I most wanted to inspect.

## Test the behavior that crosses the boundary

The lifecycle I now use to review a migration is simple enough to fit in one trace. The labels name obligations, not guarantees this installation has already satisfied:

```text
capture    source event + scope
   |
persist    acknowledged delivery
           safe retries
   |
process    preserve provenance
   |
retrieve   permitted scope
           bounded waiting
   |
inject     traceable context
           honest authority
   |
correct    supersede old evidence
   |
forget     approved targets
           checked survivors
```

My acceptance checks exercised selected parts of that chain. Hermes captured a withheld synthetic fact through normal turn capture, and a separate session recalled it without tools or files. Codex captured a project fact through its native Stop path. A fresh Codex CLI session recalled both its project fact and the Hermes fact. Routing checks verified that unrelated project archives were not selected.

Those are stronger receipts than a healthy service or a successful subprocess exit. They remain happy-path checks. They do not prove retry safety, correction propagation, or behavior under every interruption. The later adapter probes demonstrated why both kinds of test belong in the same acceptance process.

For another migration, I would preserve source identity before changing meaning, approve archive routing separately from import, and test queued work independently from acknowledged delivery. I would require partial recall to remain useful when optional history stalls. Destructive approval would name exact targets and survivors, with verification on both sides.

I would also ask how a correction reaches every place the old claim can still be injected. Keeping an accurate archive while an always-loaded preference contradicts it is another way to preserve data and lose the behavior.

The next memory system I choose will be judged by how cleanly I can leave it, and by whether it can prove what it forgot without losing what mattered.

PK

[^migration]: Operator receipt, "Honcho conclusion migration," September 11, 2026. Exact import verification covered 8,455 conclusions across 13 archives; four conversion tests and a live synthetic idempotency test passed. The source export and raw conclusions remain private. This article reproduces aggregate results, not the underlying personal corpus.
[^audit]: Operator receipts, "Hindsight audit, September 11-12, 2026" and reviewer C's harness audit, September 12, 2026. The first records live capture, recall, routing, and restore checks, including 15 passing adapter/routing tests. The separate source audit ran seven offline synthetic probes. Neither is a comparative memory-quality benchmark.
[^cleanup]: Operator receipts, "Approved Hindsight cleanup" and its independent verification record, completed September 13, 2026 UTC. The manifest authorized 3,881 removals; API verification found 5,739 remaining units, no missing or text-modified survivors, and all 3,817 expected provenance bundles. Private manifests and backups are not public demo fixtures.
