"""Tests for sampling.py, beyond the lesson reference tests.

Reference (lessons/01/.../test_main.py) already covers: probabilities sum to
one, equal logits -> 0.5/0.5, lower temperature sharpens, same seed repeats,
temperature 0 raises, infinite logit raises. Every test below adds behavior
the reference does not check. Each test names what it can falsify.
"""
import importlib.util
import random
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "sampling", Path(__file__).resolve().parents[1] / "sampling.py")
sampling = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sampling)


class TemperatureBehavior(unittest.TestCase):
    def test_low_temperature_concentrates_on_argmax(self):
        """Falsifies: 'lower temperature sharpens the distribution.'

        If softmax/temperature were implemented wrongly (e.g. temperature
        multiplied instead of divided), mass would not concentrate."""
        probs = sampling.probabilities([1, 2, 3], temperature=0.05)
        self.assertGreater(probs[2], 0.999)
        self.assertAlmostEqual(sum(probs), 1.0)

    def test_confidently_wrong_peak_survives_cooling(self):
        """Falsifies: 'lowering temperature can repair a wrong answer.'

        Index 0 is stipulated WRONG but has the largest logit. Cooling must
        concentrate mass on it anyway -- temperature changes the
        distribution, not the truth."""
        probs = sampling.probabilities([4, 1, 1], temperature=0.1)
        self.assertGreater(probs[0], 0.999,
                           "cooling must not move mass off the wrong peak")

    def test_high_temperature_flattens_toward_uniform(self):
        """Falsifies: symmetric sharpening/flattening around t=1."""
        probs = sampling.probabilities([1, 2, 3], temperature=100.0)
        for p in probs:
            self.assertAlmostEqual(p, 1 / 3, places=2)


class SamplingFidelity(unittest.TestCase):
    def test_empirical_converges_to_theory_with_n(self):
        """Falsifies: 'sample() draws from the claimed distribution.'

        Total-variation distance between empirical counts and the theoretical
        distribution must shrink as n grows; a biased sampler would not
        converge."""
        logits = [1, 2, 3]
        theory = sampling.probabilities(logits, temperature=0.5)
        tv_small = sampling.total_variation(
            sampling.sample(logits, count=300, seed=11, temperature=0.5), theory)
        tv_large = sampling.total_variation(
            sampling.sample(logits, count=30000, seed=11, temperature=0.5), theory)
        self.assertLess(tv_large, tv_small)
        self.assertLess(tv_large, 0.02)

    def test_different_seeds_give_different_counts(self):
        """Falsifies: the seed actually controls the stream.

        A degenerate 'seeded' RNG that ignored its seed would return
        identical counts for every seed."""
        a = sampling.sample([1, 2, 3], count=500, seed=1)
        b = sampling.sample([1, 2, 3], count=500, seed=2)
        self.assertNotEqual(a, b)

    def test_sample_does_not_touch_global_random_state(self):
        """Falsifies: 'the local generator leaks into global state.'

        Sampling must be reproducible without side effects on the caller's
        random stream."""
        random.seed(123)
        before = random.random()
        random.seed(123)
        sampling.sample([1, 2, 3], count=1000, seed=7)
        after = random.random()
        self.assertEqual(before, after)


class FailureChecks(unittest.TestCase):
    """Failure checks beyond the reference (temp=0, inf logit)."""

    def test_empty_logits_raises(self):
        with self.assertRaises(ValueError):
            sampling.probabilities([])

    def test_nan_temperature_raises(self):
        with self.assertRaises(ValueError):
            sampling.probabilities([1, 2], float("nan"))

    def test_negative_temperature_raises(self):
        with self.assertRaises(ValueError):
            sampling.probabilities([1, 2], -1.0)

    def test_negative_count_raises(self):
        with self.assertRaises(ValueError):
            sampling.sample([1, 2], count=-5)

    def test_non_integer_count_raises(self):
        with self.assertRaises(ValueError):
            sampling.sample([1, 2], count=10.5)

    def test_normalize_rejects_zero_total(self):
        with self.assertRaises(ValueError):
            sampling.normalize([0, 0, 0])

    def test_total_variation_rejects_empty_counts(self):
        with self.assertRaises(ValueError):
            sampling.total_variation({}, [0.5, 0.5])


if __name__ == "__main__":
    unittest.main()
