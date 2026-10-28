"""Tests for contracts.py, beyond the lesson reference tests.

Reference (lessons/02/.../test_main.py) already covers: valid passes,
non-JSON fails, wrong answer type fails, unknown source fails, extra field
fails, empty experiment raises. Every test below adds behavior the
reference does not check. Each test names what it can falsify.
"""
import importlib.util
import json
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "contracts", Path(__file__).resolve().parents[1] / "contracts.py")
contracts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contracts)

SOURCES = {"softmax", "frictional", "contract", "quartile"}


class ValidationBoundary(unittest.TestCase):
    def test_false_claim_with_valid_source_passes_format(self):
        """Falsifies: 'passing validation means the response is true.'

        This is the experiment's key boundary: a well-formed falsehood with
        a real source ID passes every mechanical check. If this test ever
        failed, the validator would be claiming semantic judgment it does
        not have."""
        text = json.dumps({
            "answer": "Temperature changes the truth of the answer.",
            "sources": ["softmax"],
        })
        ok, reason = contracts.validate(text, SOURCES)
        self.assertTrue(ok, reason)

    def test_empty_answer_rejected(self):
        """Falsifies: 'non-empty answer' is enforced (reference never tests)."""
        text = json.dumps({"answer": "   ", "sources": ["softmax"]})
        ok, reason = contracts.validate(text, SOURCES)
        self.assertFalse(ok)
        self.assertTrue(reason.startswith("empty"))

    def test_empty_sources_rejected(self):
        """Falsifies: citations are actually required (reference never tests)."""
        text = json.dumps({"answer": "x", "sources": []})
        ok, reason = contracts.validate(text, SOURCES)
        self.assertFalse(ok)
        self.assertTrue(reason.startswith("empty"))

    def test_mixed_type_sources_rejected(self):
        """Falsifies: every source entry is checked, not just the list."""
        text = json.dumps({"answer": "x", "sources": ["softmax", 7]})
        ok, reason = contracts.validate(text, SOURCES)
        self.assertFalse(ok)
        self.assertTrue(reason.startswith("source"))


class FailureReasons(unittest.TestCase):
    def test_reasons_name_the_failure(self):
        """Falsifies: the (ok, reason) improvement over the reference bool.

        Each failure class must produce a distinct, machine-readable reason
        prefix so the experiment can report *which* contract clause failed."""
        cases = [
            ("{bad json", "not-json"),
            ('["not", "an", "object"]', "not-object"),
            ('{"answer": "x", "sources": ["a"], "extra": 1}', "schema"),
            ('{"answer": 42, "sources": ["softmax"]}', "type"),
            ('{"answer": "", "sources": ["softmax"]}', "empty"),
            ('{"answer": "x", "sources": ["nope"]}', "source"),
        ]
        seen = set()
        for text, prefix in cases:
            ok, reason = contracts.validate(text, SOURCES)
            self.assertFalse(ok)
            self.assertTrue(reason.startswith(prefix),
                            "expected %r, got %r" % (prefix, reason))
            seen.add(prefix)
        self.assertEqual(len(seen), 6)

    def test_pass_rate_reports_failure_breakdown(self):
        """Falsifies: pass_rate() only returns a bare number."""
        responses = [
            '{"answer": "x", "sources": ["softmax"]}',
            "not json",
            '{"answer": "x", "sources": ["nope"]}',
        ]
        rate, failures = contracts.pass_rate(responses, SOURCES)
        self.assertAlmostEqual(rate, 1 / 3)
        self.assertEqual([f["index"] for f in failures], [1, 2])
        self.assertEqual(failures[0]["reason"], "not-json")
        self.assertTrue(failures[1]["reason"].startswith("source"))

    def test_pass_rate_empty_experiment_raises(self):
        with self.assertRaises(ValueError):
            contracts.pass_rate([], SOURCES)


class RenderHelper(unittest.TestCase):
    def test_render_fills_template_without_a_model(self):
        """Falsifies: render() does anything beyond string templating."""
        template = "Q: {{QUESTION}}\n{{EVIDENCE}}"
        out = contracts.render(template, "What is softmax?",
                               {"softmax": "Scores into probabilities."})
        self.assertIn("What is softmax?", out)
        self.assertIn("softmax: Scores into probabilities.", out)
        self.assertNotIn("{{", out)


if __name__ == "__main__":
    unittest.main()
