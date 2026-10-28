"""Shared test setup. No test may reach the real Anthropic API."""
import pytest


@pytest.fixture(autouse=True)
def no_real_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)
    monkeypatch.delenv("JOBWATCH_MODEL", raising=False)
