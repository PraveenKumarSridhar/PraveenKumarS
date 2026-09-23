# Distribution drafts: memory evaluation

Drafts only. Publish only after the user approves posting and the merged canonical returns the intended article. URL: https://praveenks.com/notes/evaluating-agent-memory/

## X: launch

A memory system can cite a stale answer perfectly.

I put together ten synthetic cases that separate retrieval, source validity and task correctness. Token overlap finds 6/7 relevant records, but the toy reader gets 4/10 outcomes right.

Runnable code and limits:
https://praveenks.com/notes/evaluating-agent-memory/

## X: takeaway

Three memory checks I want scored separately:

- Was the evidence retrieved?
- Was it current and permitted?
- Did the answer use it correctly?

A matching citation only answers part of that. This small deterministic fixture makes the failures inspectable.

https://praveenks.com/notes/evaluating-agent-memory/

## LinkedIn: technical summary

An accurate citation can support a stale answer.

This agent-memory evaluation example uses ten synthetic histories and a deliberately simple deterministic reader. It separates retrieval precision/recall, stale use, access scope, provenance and task correctness.

The token-overlap selector retrieves 6 of 7 relevant records, while the reader produces 4 correct outcomes in 10 cases. Its citations all match their source records. Some sources are simply invalid for the task.

This is a teaching fixture, not a model or framework benchmark. The cases, scoring code, raw outputs and limitations are public with the article:
https://praveenks.com/notes/evaluating-agent-memory/

## Follow-up experiment

Before drafting another result, replace the key-based reader with a fixed model, hold the memory budget constant, and add independently reviewed paraphrases. Compare no-memory and memory conditions, record actual injected evidence, and report uncertainty at the scenario level. No outcome is claimed in advance.
