#!/usr/bin/env python3
"""Deterministic teaching fixture. No model calls, embeddings or vendor benchmark."""
import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re


def require(condition, message):
    if not condition:
        raise ValueError(message)


def timestamp(value):
    parsed = datetime.fromisoformat(value)
    require(parsed.tzinfo is not None, "timestamps need explicit time zones")
    return parsed


def unique_ids(values, allowed, label):
    require(isinstance(values, list) and all(isinstance(x, str) for x in values), label + ": expected string ID list")
    require(len(values) == len(set(values)), label + ": duplicate IDs")
    require(set(values) <= allowed, label + ": unknown IDs")
    return set(values)


def validate_cases(cases):
    require(bool(cases), "empty dataset")
    require(len({c["id"] for c in cases}) == len(cases), "duplicate case IDs")
    for c in cases:
        history = c["history"]
        ids = {h["id"] for h in history}
        require(len(ids) == len(history), c["id"] + ": duplicate history IDs")
        times = [timestamp(h["time"]) for h in history]
        require(times == sorted(times), c["id"] + ": history must be chronological")
        require(all(t <= timestamp(c["query_time"]) for t in times), c["id"] + ": future history")
        require(all(isinstance(h["facts"], dict) for h in history), "facts must be objects")
        labels = c["labels"]
        sets = {k: unique_ids(labels[k], ids, k) for k in ("relevant", "permitted", "stale", "untrusted")}
        require(sets["relevant"] <= sets["permitted"] - sets["stale"] - sets["untrusted"], "relevant evidence must be permitted, current and trusted")
        require(isinstance(labels["answer"], dict), "answer labels must be objects")
        for key, value in labels["answer"].items():
            require(any(h["id"] in sets["relevant"] and h["facts"].get(key) == value for h in history), "gold answer lacks relevant evidence")


def evaluate(cases, predictions):
    validate_cases(cases)
    require(len(predictions) == len(cases), "one prediction required per case")
    require(len({p["id"] for p in predictions}) == len(predictions), "duplicate prediction IDs")
    require({p["id"] for p in predictions} == {c["id"] for c in cases}, "missing or unknown case predictions")
    by_id = {p["id"]: p for p in predictions}
    totals = Counter()
    details = []
    for c in cases:
        p = by_id[c["id"]]
        history = {h["id"]: h for h in c["history"]}
        retrieved = unique_ids(p["retrieved"], set(history), "retrieved")
        used = unique_ids(p["used"], retrieved, "used")
        answer, citations, labels = p["answer"], p["citations"], c["labels"]
        require(isinstance(answer, dict) and isinstance(citations, dict), "answer and citations must be objects")
        require(set(citations) <= set(answer), "citation without answer claim")
        require(all(isinstance(x, str) and x in used for x in citations.values()), "citations must refer to used evidence")
        relevant, permitted = set(labels["relevant"]), set(labels["permitted"])
        stale, untrusted = set(labels["stale"]), set(labels["untrusted"])
        sourced = {k for k, v in answer.items() if k in citations and history[citations[k]]["facts"].get(k) == v}
        # Source matching is distinct from source validity: an old record can be cited accurately.
        supported = {k for k in sourced if citations[k] in permitted - stale - untrusted}
        invalid_used = used & (stale | untrusted | (set(history) - permitted))
        correct = answer == labels["answer"] and len(supported) == len(answer) and not invalid_used
        counts = {
            "relevant_retrieved": len(retrieved & relevant), "retrieved": len(retrieved), "relevant": len(relevant),
            "stale_used": len(used & stale), "used": len(used),
            "scope_exposed": len(retrieved - permitted), "scope_used": len(used - permitted),
            "unsupported": len(answer) - len(supported), "claims": len(answer), "provenance_correct": len(sourced),
            "correct": int(correct), "cases": 1,
            "abstention_cases": int(not labels["answer"]), "correct_abstentions": int(not labels["answer"] and correct),
            "answerable_cases": int(bool(labels["answer"])), "correct_answers": int(bool(labels["answer"]) and correct),
        }
        totals.update(counts)
        errors = []
        if answer != labels["answer"]: errors.append("answer mismatch")
        if counts["unsupported"]: errors.append("unsupported or invalid-source claim")
        if counts["stale_used"]: errors.append("stale evidence used")
        if counts["scope_exposed"]: errors.append("out-of-scope evidence retrieved")
        if counts["scope_used"]: errors.append("out-of-scope evidence used")
        if used & untrusted: errors.append("untrusted evidence used")
        details.append({"id": c["id"], "correct": bool(correct), "counts": counts, "errors": errors})
    metrics = {}
    for name, numerator, denominator in (
        ("retrieval_precision", "relevant_retrieved", "retrieved"), ("retrieval_recall", "relevant_retrieved", "relevant"),
        ("stale_use", "stale_used", "used"), ("scope_exposure", "scope_exposed", "retrieved"), ("scope_use", "scope_used", "used"),
        ("unsupported_claims", "unsupported", "claims"), ("provenance_accuracy", "provenance_correct", "claims"),
        ("task_correctness", "correct", "cases"), ("correct_abstention", "correct_abstentions", "abstention_cases"),
        ("answerable_correctness", "correct_answers", "answerable_cases"),
    ):
        n, d = totals[numerator], totals[denominator]
        metrics[name] = {"numerator": n, "denominator": d, "value": n / d if d else None}
    return {"metrics": metrics, "cases": details}


def tokens(text):
    stop = {"a", "an", "the", "i", "my", "do", "is", "what", "for", "to", "of", "in", "and"}
    return set(re.findall(r"[a-z0-9]+", text.lower())) - stop


def predict(case, method):
    if method == "oracle":
        # Explicit label access. This is a scoring ceiling, never a production selector.
        selected = [h for h in case["history"] if h["id"] in case["labels"]["relevant"]]
        answer = case["labels"]["answer"].copy()
        citations = {k: next(h["id"] for h in selected if h["facts"].get(k) == v) for k, v in answer.items()}
    else:
        # Do not pass labels to the selectors or reader.
        inputs = {k: case[k] for k in ("history", "query", "key")}
        selected = list(reversed(inputs["history"]))
        if method == "overlap":
            query = tokens(inputs["query"])
            selected.sort(key=lambda h: len(query & tokens(h["text"])), reverse=True)
        elif method != "latest":
            raise ValueError("unknown baseline")
        selected = selected[:2]
        match = next((h for h in selected if inputs["key"] in h["facts"]), None)
        answer = {inputs["key"]: match["facts"][inputs["key"]]} if match else {}
        citations = {inputs["key"]: match["id"]} if match else {}
    return {"id": case["id"], "retrieved": [h["id"] for h in selected], "used": sorted(set(citations.values())), "answer": answer, "citations": citations}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--predictions", type=Path)
    mode.add_argument("--baseline", choices=("latest", "overlap", "oracle"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        raw = args.cases.read_bytes()
        cases = [json.loads(line) for line in raw.decode().splitlines() if line.strip()]
        validate_cases(cases)
        predictions = [json.loads(line) for line in args.predictions.read_text().splitlines() if line.strip()] if args.predictions else [predict(c, args.baseline) for c in cases]
        result = {"dataset_sha256": hashlib.sha256(raw).hexdigest(), "method": args.baseline or "supplied", "predictions": predictions, **evaluate(cases, predictions)}
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.error(str(error))
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output: args.output.write_text(rendered)
    else: print(rendered, end="")


if __name__ == "__main__": main()
