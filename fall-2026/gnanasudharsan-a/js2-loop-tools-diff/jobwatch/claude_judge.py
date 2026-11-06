"""The Claude judge: one posting plus the persona to Claude.

Two backends, chosen by JOBWATCH_BACKEND (default api):

    api         the Messages API, key from ANTHROPIC_API_KEY only
    claude_cli  Claude Code's non-interactive print mode (`claude -p`), one
                fresh process per call, run in a new empty temporary
                directory with every tool disabled

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
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path
from urllib.parse import urlsplit

from . import validator
from .rule import html_to_text

CLAUDE_LABEL = "judgment (model output, not fact)"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROMPT = PROJECT_ROOT / "prompts" / "judge_baseline.md"
DEFAULT_MODEL = "claude-opus-5-5"
MAX_ATTEMPTS = 2  # the first try plus 1 retry
MAX_TOKENS = 16000
ALLOWED_API_HOST = "api.anthropic.com"  # CONTRACT.md Amendment 1 allow-list
BACKENDS = ("api", "claude_cli")
DEFAULT_BACKEND = "api"
CLI_EXECUTABLE = "claude"
CLI_TIMEOUT_SECONDS = 600


class ClaudeJudgeUnavailable(RuntimeError):
    """The judge cannot be set up (no key or no prompt file)."""


class ClaudeCliError(RuntimeError):
    """One claude_cli attempt failed (process, exit status, or JSON envelope)."""


def model_name() -> str:
    return os.environ.get("JOBWATCH_MODEL") or DEFAULT_MODEL


def backend_name() -> str:
    backend = os.environ.get("JOBWATCH_BACKEND") or DEFAULT_BACKEND
    if backend not in BACKENDS:
        raise ClaudeJudgeUnavailable(f"JOBWATCH_BACKEND must be one of {BACKENDS}, not {backend!r}")
    return backend


def make_backend_client(backend: str = None):
    """The client for the chosen backend: an Anthropic client or a ClaudeCliRunner."""
    backend = backend or backend_name()
    if backend == "claude_cli":
        return make_cli_runner()
    return make_client()


def make_client():
    """Anthropic client whose key comes only from ANTHROPIC_API_KEY."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ClaudeJudgeUnavailable("ANTHROPIC_API_KEY is not set (use --no-claude to run without it)")
    import anthropic

    # An explicit api_key stops the SDK from consulting any other credential source.
    client = anthropic.Anthropic(api_key=api_key)
    # ANTHROPIC_BASE_URL could point the SDK elsewhere; check before any request.
    check_client_host(client)
    return client


def check_client_host(client) -> None:
    """CONTRACT.md Amendment 1: the Claude judge may only contact api.anthropic.com."""
    base_url = str(getattr(client, "base_url", ""))
    parts = urlsplit(base_url)
    if parts.scheme != "https":
        raise ValueError(f"refusing non-https Anthropic base URL: {base_url!r}")
    if parts.hostname != ALLOWED_API_HOST:
        raise ValueError(f"refusing Anthropic base URL host not on allow-list: {parts.hostname!r}")


# --- claude_cli backend ------------------------------------------------------

def cli_flags(model: str, system_prompt: str, session_id: str) -> list:
    """Flags for one `claude -p` call; every flag is listed in `claude --help` (2.1.312).

    The user message goes on stdin, never as a positional argument, so the
    variadic --tools option cannot swallow it.
    """
    return [
        "-p",                                # non-interactive print mode
        "--model", model,
        "--system-prompt", system_prompt,    # replaces Claude Code's default system prompt
        "--output-format", "json",           # one JSON result envelope
        "--tools", "",                       # "" disables all built-in tools
        "--strict-mcp-config",               # no --mcp-config given, so no MCP servers
        "--safe-mode",                       # no CLAUDE.md, skills, plugins, hooks, MCP servers
        "--disable-slash-commands",
        "--permission-prompts", "none",      # anything that would prompt is denied
        "--no-session-persistence",          # nothing saved, nothing resumable
        "--session-id", session_id,          # a new UUID per call, so freshness is checkable
    ]


def redacted_command(executable: str, flags: list) -> list:
    """The command as saved: the system prompt text is replaced by a placeholder."""
    shown = [executable, *flags]
    i = shown.index("--system-prompt") + 1
    shown[i] = "<prompt file text>"
    return shown


def check_workdir(workdir: Path) -> None:
    """The CLI must never run in, or under, the project folder or the caller's cwd."""
    resolved = Path(workdir).resolve()
    for forbidden in (PROJECT_ROOT.resolve(), Path.cwd().resolve()):
        if resolved == forbidden or forbidden in resolved.parents:
            raise ClaudeCliError(f"refusing to run claude in {resolved} (inside {forbidden})")
    if any(resolved.iterdir()):
        raise ClaudeCliError(f"refusing to run claude in a non-empty directory: {resolved}")


def reported_models(envelope: dict) -> list:
    usage = envelope.get("modelUsage")
    if isinstance(usage, dict):
        return sorted(usage)
    model = envelope.get("model")
    return [model] if isinstance(model, str) else []


class ClaudeCliRunner:
    """Runs one fresh `claude -p` process per reply_text() call.

    Each attempt is appended to self.attempts (command without the prompt
    text, working directory, exit status, raw stdout/stderr, and the session
    id and model names the CLI reports), so a caller can save it.
    """

    backend = "claude_cli"

    def __init__(self, executable: str = CLI_EXECUTABLE, run=None,
                 timeout: float = CLI_TIMEOUT_SECONDS):
        self.executable = executable
        self._run = run
        self.timeout = timeout
        self.attempts = []

    def reply_text(self, system_prompt: str, model: str, user_message: str) -> str:
        # Kept, not deleted, after the call, so the directory can be checked afterwards.
        workdir = Path(tempfile.mkdtemp(prefix="jobwatch-claude-cli-"))
        session_id = str(uuid.uuid4())
        flags = cli_flags(model, system_prompt, session_id)
        attempt = {"backend": self.backend,
                   "command": redacted_command(self.executable, flags),
                   "cwd": str(workdir),
                   "requested_session_id": session_id}
        self.attempts.append(attempt)
        check_workdir(workdir)
        run = self._run or subprocess.run
        try:
            proc = run([self.executable, *flags], input=user_message, capture_output=True,
                       text=True, cwd=str(workdir), timeout=self.timeout, check=False)
        except subprocess.TimeoutExpired:
            attempt["error"] = f"timed out after {self.timeout}s"
            raise ClaudeCliError(attempt["error"])
        except OSError as exc:
            attempt["error"] = f"{type(exc).__name__}: {exc}"
            raise ClaudeCliError(attempt["error"])

        attempt.update(returncode=proc.returncode, raw_stdout=proc.stdout, stderr=proc.stderr)
        try:
            envelope = json.loads(proc.stdout)
        except (TypeError, ValueError):
            raise ClaudeCliError(f"exit {proc.returncode}, stdout is not a JSON envelope")
        if not isinstance(envelope, dict):
            raise ClaudeCliError("JSON envelope is not an object")
        attempt.update(reported_session_id=envelope.get("session_id"),
                       reported_models=reported_models(envelope),
                       subtype=envelope.get("subtype"),
                       is_error=envelope.get("is_error"),
                       num_turns=envelope.get("num_turns"),
                       raw_text=envelope.get("result"))
        if proc.returncode != 0 or envelope.get("is_error"):
            raise ClaudeCliError(f"exit {proc.returncode}, is_error={envelope.get('is_error')!r}, "
                                 f"subtype={envelope.get('subtype')!r}")
        if not isinstance(envelope.get("result"), str):
            raise ClaudeCliError("JSON envelope has no string 'result'")
        return envelope["result"]


def make_cli_runner() -> ClaudeCliRunner:
    executable = shutil.which(CLI_EXECUTABLE)
    if not executable:
        raise ClaudeJudgeUnavailable("claude executable not found on PATH (JOBWATCH_BACKEND=claude_cli)")
    return ClaudeCliRunner(executable)


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
    """client is an Anthropic client (api) or a ClaudeCliRunner (claude_cli)."""
    import anthropic

    model = model or model_name()
    backend = getattr(client, "backend", "api")
    errors = []
    for _ in range(MAX_ATTEMPTS):
        try:
            user_message = build_user_message(posting, persona)
            if backend == "claude_cli":
                text = client.reply_text(prompt_text, model, user_message)
            else:
                response = client.messages.create(
                    model=model,
                    max_tokens=MAX_TOKENS,
                    system=prompt_text,
                    messages=[{"role": "user", "content": user_message}],
                )
                text = _reply_text(response)
            output = validator.validate(text, posting["id"])
        except validator.ValidationFailed as exc:
            errors.append(f"validator: {exc}")
            continue
        except anthropic.APIError as exc:
            # The SDK has already retried transient errors; record and move on.
            errors.append(f"api: {type(exc).__name__}: {exc}")
            continue
        except ClaudeCliError as exc:
            errors.append(f"cli: {exc}")
            continue
        return {"label": CLAUDE_LABEL, "status": "ok", "backend": backend, "model": model,
                "output": output, "failed_attempts": errors}
    return {"label": CLAUDE_LABEL, "status": "judgment_unavailable", "backend": backend,
            "model": model, "output": None, "failed_attempts": errors}


def make_judge(prompt_path: Path = DEFAULT_PROMPT, client=None, model: str = None):
    """Check the backend and prompt up front; return judge(posting, persona) -> record."""
    prompt_text = load_prompt(prompt_path)
    client = client or make_backend_client()
    model = model or model_name()

    def judge(posting: dict, persona: dict) -> dict:
        return judge_with_claude(posting, persona, client, prompt_text, model)

    return judge
