"""The Claude judge: one posting plus the persona to the Messages API.

The prompt text is the author's file (default prompts/judge_baseline.md),
sent as the system prompt unchanged. The user turn carries data only, a JSON
object:

    {"posting": <the Greenhouse posting, "content" HTML-unescaped and tag-stripped>,
     "resume": <the persona résumé>}

The reply must pass jobwatch.validator. One retry, then judgment_unavailable
(CONTRACT.md "Refuses"); the rule verdict is never affected.
"""
import json
import os
from pathlib import Path

from . import validator
from .rule import html_to_text

CLAUDE_LABEL = "judgment (model output, not fact)"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROMPT = PROJECT_ROOT / "prompts" / "judge_baseline.md"
DEFAULT_MODEL = "claude-opus-5-5"
MAX_ATTEMPTS = 2  # the first try plus 1 retry
MAX_TOKENS = 16000


class ClaudeJudgeUnavailable(RuntimeError):
    """The judge cannot be set up (no key or no prompt file)."""


def model_name() -> str:
    return os.environ.get("JOBWATCH_MODEL") or DEFAULT_MODEL


def make_client():
    """Anthropic client whose key comes only from ANTHROPIC_API_KEY."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ClaudeJudgeUnavailable("ANTHROPIC_API_KEY is not set (use --no-claude to run without it)")
    import anthropic

    # An explicit api_key stops the SDK from consulting any other credential source.
    return anthropic.Anthropic(api_key=api_key)


def load_prompt(prompt_path: Path) -> str:
    path = Path(prompt_path)
    if not path.is_file():
        raise ClaudeJudgeUnavailable(f"prompt file not found: {path}")
    return path.read_text(encoding="utf-8")


def build_user_message(posting: dict, persona: dict) -> str:
    shown = dict(posting)
    shown["content"] = html_to_text(posting.get("content"))
    return json.dumps({"posting": shown, "resume": persona}, ensure_ascii=False, indent=2)


def _reply_text(response) -> str:
    if response.stop_reason != "end_turn":
        raise validator.ValidationFailed(f"stop_reason {response.stop_reason!r}, not end_turn")
    return "".join(block.text for block in response.content if block.type == "text")


def judge_with_claude(posting: dict, persona: dict, client, prompt_text: str,
                      model: str = None) -> dict:
    import anthropic

    model = model or model_name()
    errors = []
    for _ in range(MAX_ATTEMPTS):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=MAX_TOKENS,
                system=prompt_text,
                messages=[{"role": "user", "content": build_user_message(posting, persona)}],
            )
            output = validator.validate(_reply_text(response), posting["id"])
        except validator.ValidationFailed as exc:
            errors.append(f"validator: {exc}")
            continue
        except anthropic.APIError as exc:
            # The SDK has already retried transient errors; record and move on.
            errors.append(f"api: {type(exc).__name__}: {exc}")
            continue
        return {"label": CLAUDE_LABEL, "status": "ok", "model": model,
                "output": output, "failed_attempts": errors}
    return {"label": CLAUDE_LABEL, "status": "judgment_unavailable", "model": model,
            "output": None, "failed_attempts": errors}


def make_judge(prompt_path: Path = DEFAULT_PROMPT, client=None, model: str = None):
    """Check the key and prompt up front; return judge(posting, persona) -> record."""
    prompt_text = load_prompt(prompt_path)
    client = client or make_client()
    model = model or model_name()

    def judge(posting: dict, persona: dict) -> dict:
        return judge_with_claude(posting, persona, client, prompt_text, model)

    return judge
