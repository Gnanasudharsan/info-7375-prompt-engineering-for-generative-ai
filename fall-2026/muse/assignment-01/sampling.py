"""Sampling mechanics for Assignment 01: a controlled prompt experiment.

Implements probability normalization (softmax with max-subtraction for
numerical stability), temperature controls, seeded sampling, and the required
failure checks, using only the Python standard library.

Starting point: lessons/01-randomness-and-first-prompts/code/main.py in
nikbearbrown/info-7375-prompt-engineering-for-generative-ai (read 2026-10-10).
Deliberate differences from the reference:
  - normalize() is a separate, independently tested step instead of being
    folded into probabilities().
  - sample_one() exposes single draws; sample() aggregates counts.
  - total_variation() quantifies empirical-vs-theory agreement for the
    repeatability analysis in the conclusion.
  - Failure checks extended: empty logits, NaN/infinite temperature,
    non-integer or negative counts, non-finite logits.

Everything here runs offline. No credentials are read and no API requests
are made.
"""
import math
import random
from collections import Counter


def _check_logits(logits):
    if not isinstance(logits, (list, tuple)) or len(logits) == 0:
        raise ValueError("logits must be a non-empty list or tuple")
    for x in logits:
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise ValueError("each logit must be a real number, got %r" % (x,))
        if not math.isfinite(x):
            raise ValueError("logits must be finite, got %r" % (x,))


def _check_temperature(temperature):
    if isinstance(temperature, bool) or not isinstance(temperature, (int, float)):
        raise ValueError("temperature must be a real number")
    if not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("temperature must be positive and finite, got %r"
                         % (temperature,))


def normalize(weights):
    """Scale non-negative weights to a probability distribution.

    Raises ValueError on empty input, negative weights, or a zero total.
    """
    if not weights:
        raise ValueError("cannot normalize an empty weight list")
    if any(w < 0 for w in weights):
        raise ValueError("weights must be non-negative")
    total = sum(weights)
    if total <= 0:
        raise ValueError("weights must sum to a positive total")
    return [w / total for w in weights]


def probabilities(logits, temperature=1.0):
    """Softmax over logits at the given temperature.

    Subtracts the maximum logit first for numerical stability, divides by a
    positive temperature, exponentiates, and normalizes. Lower temperature
    sharpens the distribution toward the argmax; it does not change which
    logit is largest.
    """
    _check_logits(logits)
    _check_temperature(temperature)
    peak = max(logits)
    weights = [math.exp((x - peak) / temperature) for x in logits]
    return normalize(weights)


def sample_one(logits, temperature=1.0, rng=None):
    """Draw a single index from the temperature-scaled distribution."""
    probs = probabilities(logits, temperature)
    rng = rng if rng is not None else random.Random()
    return rng.choices(range(len(logits)), weights=probs, k=1)[0]


def sample(logits, count=1000, seed=7, temperature=1.0):
    """Draw `count` samples with a locally seeded generator.

    Returns a dict mapping token index -> observed count. The generator is
    local: global random state is never touched, and the same seed always
    reproduces the same counts.
    """
    _check_logits(logits)
    _check_temperature(temperature)
    if type(count) is not int or count < 0:
        raise ValueError("count must be a non-negative int, got %r" % (count,))
    if type(seed) is not int:
        raise ValueError("seed must be an int, got %r" % (seed,))
    rng = random.Random(seed)
    probs = probabilities(logits, temperature)
    draws = rng.choices(range(len(logits)), weights=probs, k=count)
    return dict(Counter(draws))


def total_variation(counts, probs):
    """Total-variation distance between observed counts and a distribution.

    Half the L1 distance between the empirical distribution implied by
    `counts` and `probs`. Ranges 0 (identical) to 1 (disjoint). Used to
    quantify how closely sampling follows the claimed probabilities.
    """
    n = sum(counts.values())
    if n == 0:
        raise ValueError("no observations to compare")
    if len(probs) == 0:
        raise ValueError("probability vector must be non-empty")
    empirical = [counts.get(i, 0) / n for i in range(len(probs))]
    return 0.5 * sum(abs(e - p) for e, p in zip(empirical, probs))


def temperature_sweep(logits, temperatures, count=2000, seed=7):
    """Run sampling at several temperatures; return per-temperature records."""
    records = []
    for t in temperatures:
        probs = probabilities(logits, t)
        counts = sample(logits, count=count, seed=seed, temperature=t)
        records.append({
            "temperature": t,
            "probabilities": probs,
            "counts": counts,
            "total_variation": total_variation(counts, probs),
        })
    return records
