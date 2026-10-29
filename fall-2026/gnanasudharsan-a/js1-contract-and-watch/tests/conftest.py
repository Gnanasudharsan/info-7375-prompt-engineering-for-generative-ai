"""Shared test setup. No test may reach the real Anthropic API or start a real
claude process."""
import subprocess

import pytest


@pytest.fixture(autouse=True)
def no_real_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)
    monkeypatch.delenv("JOBWATCH_MODEL", raising=False)
    monkeypatch.delenv("JOBWATCH_BACKEND", raising=False)


@pytest.fixture(autouse=True)
def no_real_subprocess(monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError(f"a test tried to start a real process: {args[:1]}")
    monkeypatch.setattr(subprocess, "run", refuse)
