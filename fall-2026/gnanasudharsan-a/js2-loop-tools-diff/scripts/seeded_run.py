"""SEEDED demo for GATE §8 — NOT a normal live run.
Mode A: real HTTPS for greenhouse:anthropic and lever:spotify; ashby:notion is replaced
        by a CONSTRUCTED 200 {"jobs": []}. Prior state = evidence/state_after_run1.json.
Mode B: all real HTTPS, continuing from the state mode A left behind.
Works only inside seeded/, never in the real state/."""
import json, sys
from datetime import datetime, timezone
from pathlib import Path
from jobwatch.loop import run_loop, Response
from jobwatch.policy import Policy
from jobwatch.transport import UrllibTransport

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE / "seeded"
BOARDS = [b for b in json.loads((HERE / "boards.json").read_text()) if not b["id"].startswith("greenhouse:zz")]
NOTION = next(b["url"] for b in BOARDS if b["id"] == "ashby:notion")


def main(mode):
    if mode == "A":
        if ROOT.exists():
            sys.exit("seeded/ already exists; remove it on purpose before re-running mode A")
        (ROOT / "state").mkdir(parents=True)
        (ROOT / "runs").mkdir()
        (ROOT / "state" / "seen_ids.json").write_text((HERE / "evidence" / "state_after_run1.json").read_text())
    policy = Policy(ROOT)
    real = UrllibTransport(policy)

    def transport(url, timeout):
        if mode == "A" and url == NOTION:
            return Response(200, b'{"jobs": []}', {"X-Seeded": "constructed empty board (GATE 8 demo)"})
        return real(url, timeout)

    budgets = json.loads((HERE / "gate_config.json").read_text())
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + f"-SEEDED-{mode}"
    res = run_loop(BOARDS, root=ROOT, policy=policy, transport=transport, budgets=budgets, run_id=run_id)
    print(f"[SEEDED {mode}] run {run_id}: exit={res.exit} code={res.exit_code}")
    for b, r in res.boards.items():
        n = lambda x: None if x is None else len(x)
        print(f"  {b}: {r['status']} count={r['count']} new={n(r['new'])} removed={n(r['removed'])}")
    return res.exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
