---
title: Context windows are not memory
description: Two million tokens of attention still won't remember your name next Tuesday. On the difference between what a model is looking at and what an agent actually keeps.
date: 2026-07-12
tags: [memory, agents]
---

## The bigger-window fallacy

Every few months a lab ships a bigger context window and my feed fills up with "RAG is dead" posts. Two million tokens! Just paste your whole life in! And every few months I watch an agent with a giant window forget, mid-conversation, the thing you told it three turns ago.

The window keeps growing and the complaint from users stays exactly the same: *it doesn't remember me.*

## Attention vs. remembering

Here's the distinction I keep coming back to: *a context window is attention, not memory.* It's what the model is looking at right now. Memory is what survives when the tab closes — what the agent chooses to keep, how it indexes it, and whether it can find it again when it actually matters.

> A two-million-token window still can't remember your name on Tuesday.

## The write path

When I sketch memory for an agent, I try to be embarrassingly explicit about the write path. Reads get all the attention (pun intended), but the write policy is where memory systems actually differ:

```python
def maybe_remember(turn, store):
    salience = score(turn)      # worth keeping?
    if salience < THRESHOLD:
        return                  # forgetting is a feature
    fact = distill(turn)        # compress before you store
    store.upsert(fact, ttl=days(90))
```

Decide what's worth keeping, compress it before you store it, and give it an expiry date. Three small decisions that matter more than which vector database you pick.

## Forgetting is a feature

TTLs, decay, summarize-and-discard — an agent that remembers everything is just a slower context window. More on that in the next note.
