"""DayThread two-day replay (synthetic fixture, fictional client).

Day 1: store the raw check-in transcript.  Summarize it (normal or constrained).
Day 2: write the opening message twice from fresh sessions:
  A = summary only, B = summary + the full raw day-one transcript text.

Every model call is a separate, isolated `claude -p` session run from a new empty
directory. All attempts (including failures and retries) are stored in SQLite and
as raw files under runs/<run_id>/.

Usage:  python3 replay.py            # full run: 5 trials x 2 settings = 30 calls
        python3 replay.py --trials 1 # smaller run (label it as such)
"""
import argparse
import hashlib
import json
import platform
import sqlite3
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Frozen in PRE-RUN.md before the first experimental call. The run refuses to start
# if any input file has changed.
EXPECTED_SHA256 = {
    "fixture/day1_transcript.txt": "9e73fda76992b78cac705d1ede044958fec259174f8304f2fe1f911af5d2a6c3",
    "fixture/fixture.json": "09be31de5aaa426cd387989216ea32d20442191adaa6189fa897a7e6f56de617",
    "prompts/day2_A.input.txt": "6bd1297343ac09cf7d4f232bce03c6ad8bd9ec5f769f3a93e98d14afdcd3cf64",
    "prompts/day2_B.input.txt": "2bf6ed90f4c76fda1da70d81b6c2a5e189148e08f121d931e85d45b48a2fac06",
    "prompts/day2_opening.system.txt": "51d0446260e85f3269feeb96f6b2456314e689070ab58e8379761892551a8280",
    "prompts/summary.input.txt": "5bc4c63b19e862dc47a096bbf78cedc2e0175fded38d34b9da19c320e82efa92",
    "prompts/summary_constrained.system.txt": "5596000ce099725879e2e624545be8eace7dcb3f76c2e1d3e87e606e71207e2c",
    "prompts/summary_normal.system.txt": "edcb955af6980f58ed5efadf0f40a7255010891e41894b1c27ef689faf57f326",
}

MODEL = "claude-opus-5"
EFFORT = "medium"
CLAUDE_FLAGS = [
    "--safe-mode",                 # no CLAUDE.md, skills, plugins, hooks, MCP
    "--tools", "",                 # no tools: the model sees only the text it is given
    "--no-session-persistence",    # nothing saved, nothing resumable
    "--output-format", "json",
    "--model", MODEL,
    "--effort", EFFORT,
]
SETTINGS = ["normal", "constrained"]
MAX_ATTEMPTS = 3                   # first try + at most two retries
CALL_TIMEOUT_S = 300

SCHEMA = """
CREATE TABLE checkins (
  id INTEGER PRIMARY KEY, client TEXT, sim_date TEXT, transcript TEXT,
  source_file TEXT, sha256 TEXT);
CREATE TABLE calls (
  id INTEGER PRIMARY KEY, run_id TEXT, step TEXT, setting TEXT, trial INTEGER,
  condition TEXT, attempt INTEGER, started_at TEXT, ended_at TEXT,
  argv_json TEXT, system_prompt TEXT, input_text TEXT, exit_code INTEGER,
  is_error INTEGER, result_text TEXT, model TEXT, session_id TEXT,
  usage_json TEXT, stdout TEXT, stderr TEXT, raw_file TEXT);
CREATE TABLE summaries (
  id INTEGER PRIMARY KEY, run_id TEXT, setting TEXT, trial INTEGER,
  checkin_id INTEGER REFERENCES checkins(id), call_id INTEGER REFERENCES calls(id),
  text TEXT);
CREATE TABLE openings (
  id INTEGER PRIMARY KEY, run_id TEXT, setting TEXT, trial INTEGER,
  condition TEXT, sim_date TEXT, summary_id INTEGER REFERENCES summaries(id),
  call_id INTEGER REFERENCES calls(id), text TEXT);
"""


def now():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(rel):
    return (HERE / rel).read_text(encoding="utf-8")


def fill(template, **values):
    for key, value in values.items():
        template = template.replace("{" + key + "}", value)
    return template


class Run:
    def __init__(self, run_dir, run_id, log):
        self.dir, self.id, self.log = run_dir, run_id, log
        self.db = sqlite3.connect(run_dir / "daythread.sqlite")
        self.db.executescript(SCHEMA)
        self.n = 0

    def call(self, step, setting, trial, condition, system_prompt, input_text):
        """One logical call; retried up to MAX_ATTEMPTS. Returns (call_id, text) or (None, None)."""
        for attempt in range(1, MAX_ATTEMPTS + 1):
            self.n += 1
            stem = f"{self.n:02d}_{step}_{setting}_t{trial}{'_' + condition if condition else ''}_a{attempt}"
            argv = ["claude", "-p", *CLAUDE_FLAGS, "--system-prompt", system_prompt, input_text]
            started = now()
            with tempfile.TemporaryDirectory(prefix="daythread-call-") as empty_cwd:
                try:
                    proc = subprocess.run(argv, cwd=empty_cwd, capture_output=True, text=True,
                                          timeout=CALL_TIMEOUT_S)
                    exit_code, stdout, stderr = proc.returncode, proc.stdout, proc.stderr
                except subprocess.TimeoutExpired as exc:
                    exit_code, stdout, stderr = -1, exc.stdout or "", f"TIMEOUT after {CALL_TIMEOUT_S}s"
            ended = now()
            (self.dir / "calls" / f"{stem}.json").write_text(stdout, encoding="utf-8")
            if stderr:
                (self.dir / "calls" / f"{stem}.stderr.txt").write_text(stderr, encoding="utf-8")

            result, is_error, model, session, usage = None, 1, None, None, None
            try:
                out = json.loads(stdout)
                result = out.get("result")
                is_error = int(bool(out.get("is_error")) or exit_code != 0)
                model = ",".join(f"{k} (canonical {v.get('canonicalModel')})"
                                 for k, v in (out.get("modelUsage") or {}).items())
                session = out.get("session_id")
                usage = json.dumps(out.get("usage"))
            except (json.JSONDecodeError, AttributeError):
                pass

            cur = self.db.execute(
                "INSERT INTO calls (run_id, step, setting, trial, condition, attempt, started_at,"
                " ended_at, argv_json, system_prompt, input_text, exit_code, is_error, result_text,"
                " model, session_id, usage_json, stdout, stderr, raw_file)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (self.id, step, setting, trial, condition, attempt, started, ended,
                 json.dumps(argv), system_prompt, input_text, exit_code, is_error, result,
                 model, session, usage, stdout, stderr, f"calls/{stem}.json"))
            self.db.commit()
            status = "ok" if not is_error and result else "FAILED"
            self.log(f"{ended} call {self.n:02d} {step} {setting} t{trial} {condition or ''} "
                     f"attempt {attempt}: {status} exit={exit_code} model={model}")
            if status == "ok":
                return cur.lastrowid, result
            if attempt < MAX_ATTEMPTS:
                self.log(f"    retrying ({stderr.strip()[:200] or (result or '')[:200]})")
        return None, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=5)
    args = parser.parse_args()

    changed = [rel for rel, digest in EXPECTED_SHA256.items() if sha256(HERE / rel) != digest]
    if changed:
        sys.exit(f"Refusing to run: these files differ from PRE-RUN.md: {changed}")

    fixture = json.loads(read("fixture/fixture.json"))
    transcript = read("fixture/day1_transcript.txt").rstrip("\n")
    client, day1, day2 = fixture["client"], fixture["simulated_dates"]["day1"], fixture["simulated_dates"]["day2"]
    system = {s: read(f"prompts/summary_{s}.system.txt") for s in SETTINGS}
    system["day2"] = read("prompts/day2_opening.system.txt")
    template = {k: read(f"prompts/{k}.input.txt") for k in ("summary", "day2_A", "day2_B")}

    run_id = datetime.now().strftime("%Y%m%dT%H%M%S")
    run_dir = HERE / "runs" / run_id
    (run_dir / "calls").mkdir(parents=True)
    log_file = (run_dir / "run.log").open("a", encoding="utf-8")

    def log(line):
        print(line, flush=True)
        log_file.write(line + "\n")
        log_file.flush()

    cli_version = subprocess.run(["claude", "--version"], capture_output=True, text=True).stdout.strip()
    manifest = {
        "run_id": run_id, "started_at": now(), "trials_per_setting": args.trials,
        "label": fixture["label"], "simulated_dates": fixture["simulated_dates"],
        "execution_date_note": "started_at/ended_at are real execution times; day1/day2 are simulated",
        "claude_cli_version": cli_version, "claude_flags": CLAUDE_FLAGS,
        "settings_not_settable_via_cli": ["temperature", "top_p", "max_output_tokens"],
        "python": platform.python_version(), "sqlite": sqlite3.sqlite_version,
        "input_sha256": EXPECTED_SHA256, "max_attempts_per_call": MAX_ATTEMPTS,
        "order": "for trial 1..N: for setting in [normal, constrained]: summary, then opening A, then opening B",
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    log(f"{now()} run {run_id} start: {args.trials} trial(s) per setting, CLI {cli_version}")

    run = Run(run_dir, run_id, log)
    checkin_id = run.db.execute(
        "INSERT INTO checkins (client, sim_date, transcript, source_file, sha256) VALUES (?,?,?,?,?)",
        (client, day1, transcript, "fixture/day1_transcript.txt",
         EXPECTED_SHA256["fixture/day1_transcript.txt"])).lastrowid
    run.db.commit()

    incomplete = []
    for trial in range(1, args.trials + 1):
        for setting in SETTINGS:
            summary_input = fill(template["summary"], client=client, day1=day1, transcript=transcript)
            call_id, summary = run.call("summary", setting, trial, None, system[setting], summary_input)
            if summary is None:
                incomplete.append(f"{setting} t{trial}: summary failed; openings not run")
                continue
            summary_id = run.db.execute(
                "INSERT INTO summaries (run_id, setting, trial, checkin_id, call_id, text) VALUES (?,?,?,?,?,?)",
                (run_id, setting, trial, checkin_id, call_id, summary)).lastrowid
            run.db.commit()
            for condition in ("A", "B"):
                opening_input = fill(template[f"day2_{condition}"], client=client, day1=day1, day2=day2,
                                     summary=summary, transcript=transcript)
                call_id, opening = run.call("opening", setting, trial, condition, system["day2"], opening_input)
                if opening is None:
                    incomplete.append(f"{setting} t{trial}: opening {condition} failed")
                    continue
                run.db.execute(
                    "INSERT INTO openings (run_id, setting, trial, condition, sim_date, summary_id, call_id, text)"
                    " VALUES (?,?,?,?,?,?,?,?)",
                    (run_id, setting, trial, condition, day2, summary_id, call_id, opening))
                run.db.commit()

    manifest["ended_at"] = now()
    manifest["incomplete"] = incomplete
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    log(f"{now()} run {run_id} end. Incomplete: {incomplete or 'none'}")


if __name__ == "__main__":
    main()
