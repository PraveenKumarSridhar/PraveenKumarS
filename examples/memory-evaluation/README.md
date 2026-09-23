# A small memory evaluation fixture

This is a deterministic teaching example, not a model or framework benchmark. Ten hand-authored synthetic histories exercise ten different failure conditions. There are no private conversations, API calls, embeddings or model judges. Each case includes a query time, audience, evidence IDs and a label rationale.

## Frozen protocol

The case labels and following selectors were specified before running the baselines. Each non-oracle selector retrieves two records. The shared reader returns the first selected record containing the requested structured key, with its source ID. It abstains if no such record exists. This deliberately limited reader has no language understanding or correction logic.

- `latest`: take the last two records, newest first.
- `overlap`: rank by distinct lowercased query/text token overlap, removing the fixed stopword list in code. Break ties newest first. Take two, including zero-overlap records if necessary.
- `oracle`: read the gold evidence and answer labels directly. This is a scoring ceiling and validation fixture, not a competing implementation.

The first two methods receive history, query and requested key, not labels. They intentionally lack policy filtering so the fixture can expose that failure. Equal record counts do not imply equal token cost. The ten cases are illustrative strata, not a sampled population or a held-out model evaluation.

## Run

From the repository root, with Python 3.9+:

```sh
python3 -m unittest discover -s examples/memory-evaluation -p 'test_*.py'
python3 examples/memory-evaluation/evaluate.py --cases examples/memory-evaluation/cases.jsonl --baseline latest --output /tmp/latest.json
python3 examples/memory-evaluation/evaluate.py --cases examples/memory-evaluation/cases.jsonl --baseline overlap --output /tmp/overlap.json
python3 examples/memory-evaluation/evaluate.py --cases examples/memory-evaluation/cases.jsonl --baseline oracle --output /tmp/oracle.json
```

For your own predictions, supply JSONL with one object per case:

```json
{"id":"stable-preference","retrieved":["m1"],"used":["m1"],"answer":{"drink":"tea"},"citations":{"drink":"m1"}}
```

```sh
python3 examples/memory-evaluation/evaluate.py --cases examples/memory-evaluation/cases.jsonl --predictions predictions.jsonl
```

Every case must have exactly one output. Unknown or duplicate IDs, missing outputs, future evidence and unordered histories fail validation. Invalid inputs never silently drop out of denominators. Answer and citation maps are structured test adapters, not claims that free-form text scoring is solved.

## Metrics

All fractions aggregate counts across cases (micro aggregation), with numerator and denominator in the JSON. A zero denominator produces `null`, not zero or perfect accuracy.

| Metric | Numerator / denominator |
| --- | --- |
| Retrieval precision | Relevant retrieved IDs / all retrieved IDs |
| Retrieval recall | Relevant retrieved IDs / all gold relevant IDs |
| Stale use | Stale used IDs / all used IDs |
| Scope exposure | Retrieved IDs outside permitted set / all retrieved IDs |
| Scope use | Used IDs outside permitted set / all used IDs |
| Unsupported claims | Claims lacking matching, current, trusted, permitted cited evidence / all answer claims |
| Provenance accuracy | Claims whose cited used record contains the exact fact / all answer claims |
| Task correctness | Cases with exact expected facts and valid evidence use / all cases |
| Correct abstention | Correct cases among gold-empty answers / gold-empty cases |
| Answerable correctness | Correct cases among gold-nonempty answers / gold-nonempty cases |

An accurate citation can point to a stale fact. That is why provenance and validity are separate. Task correctness concerns the answer and its used evidence; out-of-scope retrieval is independently reported even if no leak appears in the answer. Retrieval is the selected context in this toy, so it models exposure. A real integration must trace selection and injection separately.

The scorer's unsupported category includes invalid-source claims, which may be literally present in a record. It does not establish truth beyond the fixture labels. Conflicting trusted reports can both be relevant while the expected answer is empty. Forgetting tests active-use exclusion only.

## Interpretation limits

There is one case per condition, a fixed key-based reader, no stochastic generation and no latency or token measurement. The same author designed the fixtures and implementation. Results demonstrate distinguishable error categories; they cannot establish generalization, framework superiority or a production effect size. Extend with independently reviewed histories, held-out paraphrases, varied lengths and a real reader before making those claims.

## Recorded run

Dataset SHA-256: `8fe7520ac6f42d8ab5d81ceda3e9efc4bd589c94546717eadea90e5bacb621f3`.
The September 23, 2026 run uses the commands above. Complete predictions, per-case failures and metric counts are checked in under `results/`. Tests rerun and compare the full result objects.

| Selector | Relevant selected | Precision | Recall | Correct outcomes | Stale uses | Correct source citations |
| --- | --- | --- | --- | --- | --- | --- |
| Latest two | 5 | 5/20 | 5/7 | 2/10 | 2/7 | 7/7 |
| Token overlap | 6 | 6/20 | 6/7 | 4/10 | 3/9 | 9/9 |
| Gold oracle | 7 | 7/7 | 7/7 | 10/10 | 0/5 | 5/5 |

Hand check: latest succeeds only on the corrected preference and no-evidence abstention. Overlap succeeds on stable preference, provenance, repeated distraction and no-evidence abstention. The contradiction contributes two relevant IDs; each of the other five answerable cases contributes one, giving seven in total. Both non-oracle selectors return two IDs for each of ten cases, giving twenty retrieved IDs. These checks do not use the aggregate scoring function.

The overlap selector improves retrieval while choosing the older Python preference over the newer Rust correction. Both selectors cite records accurately when they answer; neither generally validates whether those records are current, trusted or permitted. The oracle has direct label access and is not evidence of a deployable 100% solution.
