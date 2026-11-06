"""Plant each GATE §7 wrong version in a temp copy and check the tests catch it.
Never edits the real code. A mutant 'survives' if the full suite still passes."""
import shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
P, L = "jobwatch/policy.py", "jobwatch/loop.py"
MUTANTS = [  # (GATE §7 #, file, original text, wrong text)
    (1, P, "return allowed in resolved.parents", "return str(resolved).startswith(str(allowed))"),
    (2, P, "return p.resolve()", 'return Path(__import__("os").path.normpath(p))'),
    (3, P, "if parts.hostname not in ALLOWED_HOSTS:",
           'if not any(h in (parts.hostname or "") for h in ALLOWED_HOSTS):'),
    (4, L, 'jobs = data.get("jobs") if isinstance(data, dict) else None',
           'jobs = data.get("jobs", []) if isinstance(data, dict) else []'),
    (5, L, "    if failed:\n", "    if False:\n"),
    (6, L, 'return ("failed", "not_found", f"HTTP {status}")', 'return ("retry", "not_found", RETRY_WAIT_SECONDS)'),
    (7, L, 'if self.requests_used + 1 > b["max_requests"]:', 'if self.requests_used > b["max_requests"]:'),
    (8, L, '            record.update(status="failed", reason=verdict[1], detail=detail)\n',
           '            record.update(status="failed", reason=verdict[1], detail=detail)\n'
           '            self.ok_ids[board["id"]] = []\n'),
    (9, L, '            record.update(status="failed", reason=verdict[1], detail=detail)\n',
           '            record.update(status="failed", reason=verdict[1], detail=detail, new=[], removed=[])\n'),
    (10, P, "for d in WRITE_DIRS):", "for d in (*WRITE_DIRS, *READ_DIRS)):"),
]

lines = []
for n, rel, old, new in MUTANTS:
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for item in ["jobwatch", "tests", "persona", "prompts"]:
            shutil.copytree(HERE / item, tmp / item)
        for item in ["gate_config.json", "boards.json"]:
            shutil.copy(HERE / item, tmp / item)
        f = tmp / rel
        text = f.read_text()
        if text.count(old) != 1:
            lines.append(f"#{n:<2} {rel}: SKIPPED - original text found {text.count(old)} times")
            continue
        f.write_text(text.replace(old, new))
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
                           cwd=tmp, capture_output=True, text=True)
        last = (r.stdout.strip().splitlines() or ["?"])[-1]
        verdict = "CAUGHT" if r.returncode != 0 else "SURVIVED"
        lines.append(f"#{n:<2} {rel}: {verdict:8} | {last}")
print("\n".join(lines))
