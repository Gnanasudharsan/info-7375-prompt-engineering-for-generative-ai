"""Run the Claude judge over the dev or held-out postings and save every call.

Live calls: this makes real Claude requests through the backend named by
JOBWATCH_BACKEND (default api):
    api         Messages API requests (ANTHROPIC_API_KEY required)
    claude_cli  one fresh `claude -p` process per call (Claude Code login),
                in a new empty temporary directory, with all tools disabled
Each call goes through jobwatch.claude_judge.judge_with_claude unchanged: the
same validator, one retry, then judgment_unavailable. Every call is its own
request with a single user message; no conversation history is carried over.

Never reads experiment/labels_*.json. Refuses an --out folder that already
exists, so no earlier result is overwritten.

Usage:
    [JOBWATCH_BACKEND=claude_cli] .venv/bin/python experiment/run_judge.py --split dev \
        --prompt prompts/judge_baseline.md --repeats 3 --out experiment/runs/<name>
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from jobwatch import claude_judge  # noqa: E402
from jobwatch.persona import DEFAULT_PERSONA, load_persona  # noqa: E402

POSTINGS = {"dev": ROOT / "experiment" / "postings_dev.json",
            "heldout": ROOT / "experiment" / "postings_heldout.json"}
UNAVAILABLE = "judgment_unavailable"


class RecordingClient:
    """Passes messages.create through to the real client and keeps each raw
    response, so the raw model text can be saved without changing the judge."""

    def __init__(self, client):
        self._client = client
        self.messages = self
        self.responses = []

    def create(self, **kwargs):
        response = self._client.messages.create(**kwargs)
        self.responses.append(response)
        return response


def raw_attempt(response) -> dict:
    return {
        "backend": "api",
        "response_model": getattr(response, "model", None),
        "stop_reason": response.stop_reason,
        "raw_text": "".join(b.text for b in response.content if b.type == "text"),
    }


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--split", choices=sorted(POSTINGS), required=True)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--ids", help="comma-separated posting ids (default: all in the split)")
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.repeats < 1:
        parser.error("--repeats must be at least 1")
    return args


def select_postings(split: str, ids_arg: str) -> list:
    postings = json.loads(POSTINGS[split].read_text(encoding="utf-8"))
    if not ids_arg:
        return postings
    wanted = [int(i) for i in ids_arg.split(",") if i.strip()]
    by_id = {p["id"]: p for p in postings}
    missing = [i for i in wanted if i not in by_id]
    if missing:
        raise SystemExit(f"posting id(s) not in {split}: {missing}")
    return [by_id[i] for i in wanted]


def write_new(path: Path, data) -> None:
    with open(path, "x", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main(argv=None, client=None) -> int:
    args = parse_args(argv)
    postings = select_postings(args.split, args.ids)
    prompt_text = claude_judge.load_prompt(args.prompt)
    prompt_sha256 = hashlib.sha256(Path(args.prompt).read_bytes()).hexdigest()
    persona = load_persona(DEFAULT_PERSONA)
    model = claude_judge.model_name()
    backend = claude_judge.backend_name()
    client = client or claude_judge.make_backend_client(backend)
    if getattr(client, "backend", "api") != backend:
        raise SystemExit(f"client backend {getattr(client, 'backend', 'api')!r} "
                         f"does not match JOBWATCH_BACKEND={backend!r}")

    # Refuse before any request, so a clash never costs an API call.
    args.out.mkdir(parents=True, exist_ok=False)

    verdicts = {}
    for posting in postings:
        pid = posting["id"]
        verdicts[str(pid)] = []
        for repeat in range(1, args.repeats + 1):
            timestamp = datetime.now(timezone.utc).isoformat()
            if backend == "claude_cli":
                # The runner logs every attempt itself; keep only this call's.
                start = len(client.attempts)
                record = claude_judge.judge_with_claude(posting, persona, client, prompt_text, model)
                attempts = client.attempts[start:]
            else:
                recorder = RecordingClient(client)
                record = claude_judge.judge_with_claude(posting, persona, recorder, prompt_text, model)
                attempts = [raw_attempt(r) for r in recorder.responses]
            verdict = record["output"]["verdict"] if record["status"] == "ok" else UNAVAILABLE
            verdicts[str(pid)].append(verdict)
            write_new(args.out / f"{pid}_r{repeat:02d}.json", {
                "posting_id": pid,
                "repeat": repeat,
                "timestamp_utc": timestamp,
                "backend": backend,
                "model": record["model"],
                "prompt_file": str(args.prompt),
                "prompt_sha256": prompt_sha256,
                "label": record["label"],
                "attempts": attempts,
                "parsed": record["output"] if record["status"] == "ok" else UNAVAILABLE,
                "validator": {"status": record["status"],
                              "failed_attempts": record["failed_attempts"]},
            })
            print(f"{pid} r{repeat}: {verdict}")

    write_new(args.out / "summary.json", {
        "split": args.split,
        "prompt_file": str(args.prompt),
        "prompt_sha256": prompt_sha256,
        "backend": backend,
        "model": model,
        "repeats": args.repeats,
        "label": claude_judge.CLAUDE_LABEL,
        "verdicts": verdicts,
    })
    return 0


if __name__ == "__main__":
    sys.exit(main())
