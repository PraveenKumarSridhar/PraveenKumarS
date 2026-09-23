"""Hand-derived scoring examples, independent of the baseline selectors."""
import copy
import hashlib
import json
from pathlib import Path
import unittest
from evaluate import evaluate, validate_cases, predict


def case():
    return {"id": "correction", "query_time": "2026-09-23T12:00:00+00:00", "query": "Preferred language?", "key": "language",
            "history": [
                {"id": "old", "time": "2026-09-21T00:00:00+00:00", "text": "Python", "facts": {"language": "Python"}},
                {"id": "new", "time": "2026-09-22T00:00:00+00:00", "text": "Rust", "facts": {"language": "Rust"}}],
            "labels": {"relevant": ["new"], "permitted": ["old", "new"], "stale": ["old"], "untrusted": [], "answer": {"language": "Rust"}}}


def prediction():
    return {"id": "correction", "retrieved": ["old", "new"], "used": ["new"], "answer": {"language": "Rust"}, "citations": {"language": "new"}}


class ScoringTests(unittest.TestCase):
    def test_precision_recall_have_different_denominators(self):
        result = evaluate([case()], [prediction()])["metrics"]
        self.assertEqual(result["retrieval_precision"], {"numerator": 1, "denominator": 2, "value": 0.5})
        self.assertEqual(result["retrieval_recall"]["value"], 1)
        self.assertEqual(result["task_correctness"]["value"], 1)

    def test_stale_answer_has_correct_source_but_fails_task(self):
        p = prediction(); p.update(used=["old"], answer={"language": "Python"}, citations={"language": "old"})
        metrics = evaluate([case()], [p])["metrics"]
        self.assertEqual(metrics["stale_use"]["value"], 1)
        self.assertEqual(metrics["provenance_accuracy"]["value"], 1)
        self.assertEqual(metrics["task_correctness"]["value"], 0)

    def test_scope_violation_even_when_answer_matches(self):
        c = case(); c["labels"].update(permitted=["old"], relevant=[], answer={})
        metrics = evaluate([c], [prediction()])["metrics"]
        self.assertEqual(metrics["scope_exposure"]["value"], 0.5)
        self.assertEqual(metrics["scope_use"]["value"], 1)
        self.assertEqual(metrics["task_correctness"]["value"], 0)

    def test_invented_claim_is_unsupported(self):
        p = prediction(); p["answer"] = {"language": "Go"}
        metrics = evaluate([case()], [p])["metrics"]
        self.assertEqual(metrics["unsupported_claims"]["value"], 1)
        self.assertEqual(metrics["provenance_accuracy"]["value"], 0)

    def test_empty_denominators_are_null_not_perfect(self):
        c = case(); c["labels"].update(relevant=[], answer={})
        p = {"id": c["id"], "retrieved": [], "used": [], "answer": {}, "citations": {}}
        metrics = evaluate([c], [p])["metrics"]
        self.assertIsNone(metrics["retrieval_precision"]["value"])
        self.assertIsNone(metrics["retrieval_recall"]["value"])
        self.assertEqual(metrics["correct_abstention"]["value"], 1)

    def test_missing_prediction_is_invalid(self):
        with self.assertRaises(ValueError): evaluate([case()], [])

    def test_unknown_or_duplicate_id_is_invalid(self):
        for retrieved in (["missing"], ["new", "new"]):
            p = prediction(); p["retrieved"] = retrieved
            with self.assertRaises(ValueError): evaluate([case()], [p])

    def test_used_record_must_be_retrieved(self):
        p = prediction(); p["retrieved"] = ["old"]
        with self.assertRaises(ValueError): evaluate([case()], [p])

    def test_future_record_and_unordered_history_are_invalid(self):
        c = case(); c["history"].reverse()
        with self.assertRaises(ValueError): validate_cases([c])
        c = case(); c["query_time"] = "2026-09-20T00:00:00+00:00"
        with self.assertRaises(ValueError): validate_cases([c])

    def test_micro_aggregation_not_mean_of_case_rates(self):
        c1 = case(); c2 = copy.deepcopy(c1); c2["id"] = "second"
        p1 = prediction(); p2 = prediction(); p2.update(id="second", retrieved=["new"])
        self.assertAlmostEqual(evaluate([c1, c2], [p1, p2])["metrics"]["retrieval_precision"]["value"], 2 / 3)


class FrozenFixtureTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).parent
        self.raw = (self.root / "cases.jsonl").read_bytes()
        self.cases = [json.loads(line) for line in self.raw.decode().splitlines()]

    def test_non_oracle_predictions_do_not_read_gold_labels(self):
        for method in ("latest", "overlap"):
            for c in self.cases:
                without_labels = {k: v for k, v in c.items() if k != "labels"}
                self.assertEqual(predict(c, method), predict(without_labels, method))

    def test_hand_checked_success_sets_and_retrieval_counts(self):
        expected = {
            "latest": ({"corrected-preference", "abstention"}, 5, 20),
            "overlap": ({"stable-preference", "provenance", "irrelevant-repetition", "abstention"}, 6, 20),
            "oracle": ({c["id"] for c in self.cases}, 7, 7),
        }
        for method, (successes, hits, retrieved) in expected.items():
            result = evaluate(self.cases, [predict(c, method) for c in self.cases])
            self.assertEqual({c["id"] for c in result["cases"] if c["correct"]}, successes)
            self.assertEqual(result["metrics"]["retrieval_precision"]["numerator"], hits)
            self.assertEqual(result["metrics"]["retrieval_precision"]["denominator"], retrieved)

    def test_checked_in_results_reproduce_exactly(self):
        for method in ("latest", "overlap", "oracle"):
            saved = json.loads((self.root / "results" / (method + ".json")).read_text())
            predictions = [predict(c, method) for c in self.cases]
            actual = {"dataset_sha256": hashlib.sha256(self.raw).hexdigest(), "method": method, "predictions": predictions, **evaluate(self.cases, predictions)}
            self.assertEqual(actual, saved)


if __name__ == "__main__": unittest.main()
