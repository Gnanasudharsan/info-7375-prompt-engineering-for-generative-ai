"""Loop tests for GATE §2-§5 and wrong versions #4-#9.
Written by me before jobwatch/loop.py existed; expected to FAIL on first run.
No real network: a fake transport and a fake clock. GATE §8 (200 with "jobs": [])
is deliberately NOT tested here; it is an open case, decided later by amendment."""
import json
from pathlib import Path
import pytest
from jobwatch.loop import run_loop, Response, TransportTimeout, TransportError, EXIT_CODES
from jobwatch.policy import Policy

BUDGETS = {"max_boards": 5, "max_requests": 10, "max_seconds": 120,
           "request_timeout": 30, "max_judge_calls": 10}

GH  = {"id": "greenhouse:anthropic", "ats": "greenhouse",
       "url": "https://boards-api.greenhouse.io/v1/boards/anthropic/jobs?content=true"}
AS  = {"id": "ashby:notion", "ats": "ashby",
       "url": "https://api.ashbyhq.com/posting-api/job-board/notion"}
LV  = {"id": "lever:spotify", "ats": "lever",
       "url": "https://api.lever.co/v0/postings/spotify?mode=json"}
BAD = {"id": "greenhouse:zz-no-such-board-7375", "ats": "greenhouse",
       "url": "https://boards-api.greenhouse.io/v1/boards/zz-no-such-board-7375/jobs?content=true"}
EVIL = {"id": "lever:evil", "ats": "lever",
        "url": "https://api.lever.co.evil.com/v0/postings/x?mode=json"}


def js(obj):
    return json.dumps(obj).encode()


def ok(obj):
    return Response(200, js(obj), {})


GH_OK = ok({"jobs": [{"id": 1}, {"id": 2}]})
AS_OK = ok({"jobs": [{"id": "a1"}]})
LV_OK = ok([{"id": "l1"}])


class Clock:
    def __init__(self):
        self.t = 0.0
        self.sleeps = []

    def __call__(self):
        return self.t

    def sleep(self, s):
        self.sleeps.append(s)
        self.t += s


class FakeTransport:
    """Pops scripted responses per URL; each call costs `cost` seconds on the fake clock."""
    def __init__(self, script, clock, cost=1.0):
        self.script = {u: list(r) for u, r in script.items()}
        self.clock, self.cost = clock, cost
        self.calls, self.timeouts = [], []

    def __call__(self, url, timeout):
        self.calls.append(url)
        self.timeouts.append(timeout)
        self.clock.t += self.cost
        r = self.script[url].pop(0)
        if isinstance(r, Exception):
            raise r
        return r


@pytest.fixture
def root(tmp_path):
    for d in ["runs", "state", "persona", "prompts"]:
        (tmp_path / d).mkdir()
    return tmp_path


def seed_state(root, data):
    (root / "state" / "seen_ids.json").write_text(json.dumps(data))


def read_state(root):
    return json.loads((root / "state" / "seen_ids.json").read_text())


def go(root, boards, script, budgets=BUDGETS, cost=1.0):
    clock = Clock()
    t = FakeTransport(script, clock, cost)
    res = run_loop(boards, root=root, policy=Policy(root), transport=t, budgets=budgets,
                   clock=clock, sleep=clock.sleep, run_id="test-run")
    return res, t, clock


# --- exits (GATE §2) ---------------------------------------------------------

def test_L1_all_boards_ok_is_finished_and_timeout_is_30(root):
    seed_state(root, {GH["id"]: ["1"], AS["id"]: ["a1"], LV["id"]: ["l1"]})
    res, t, _ = go(root, [GH, AS, LV], {GH["url"]: [GH_OK], AS["url"]: [AS_OK], LV["url"]: [LV_OK]})
    assert res.exit == "finished"
    assert all(b["status"] == "ok" for b in res.boards.values())
    assert t.timeouts == [30, 30, 30]


def test_L2_404_no_retry_null_counts_state_untouched_incomplete(root):
    """Wrong versions #5, #6, #8, #9."""
    seed_state(root, {GH["id"]: ["1"], BAD["id"]: ["old"]})
    res, t, _ = go(root, [GH, BAD], {
        GH["url"]: [GH_OK],
        BAD["url"]: [Response(404, js({"status": 404, "error": "Job not found"}), {}), GH_OK]})
    b = res.boards[BAD["id"]]
    assert res.exit == "incomplete"                                   # not "finished" (#5)
    assert b["status"] == "failed" and b["reason"] == "not_found"
    assert b["attempts"] == 1 and t.calls.count(BAD["url"]) == 1      # no retry on 404 (#6)
    assert b["new"] is None and b["removed"] is None                  # never 0 (#9)
    assert read_state(root)[BAD["id"]] == ["old"]                     # not overwritten (#8)


def test_L3_zero_boards_succeeded_is_error_and_state_untouched(root):
    seed_state(root, {BAD["id"]: ["old"]})
    res, _, _ = go(root, [BAD], {BAD["url"]: [Response(404, b"{}", {})]})
    assert res.exit == "error"
    assert read_state(root) == {BAD["id"]: ["old"]}


def test_L4_policy_violation_stops_run_with_error_and_no_request(root):
    seed_state(root, {GH["id"]: ["1"]})
    res, t, _ = go(root, [EVIL, GH], {EVIL["url"]: [LV_OK], GH["url"]: [GH_OK]})
    assert res.exit == "error"
    assert t.calls == []
    assert read_state(root) == {GH["id"]: ["1"]}


def test_L5_exit_codes_match_gate():
    assert EXIT_CODES == {"finished": 0, "incomplete": 2, "budget-exhausted": 3, "error": 1}


# --- wrong shape, never default to [] (GATE §5, wrong version #4) --------------

@pytest.mark.parametrize("board,response", [
    (GH, ok({"status": "ok"})),                                   # Greenhouse dict without "jobs"
    (LV, ok({"ok": False, "error": "Document not found"})),       # Lever dict, not a list
    (AS, Response(200, b"Not Found", {})),                        # Ashby non-JSON body
], ids=["gh-no-jobs-key", "lever-not-a-list", "ashby-not-json"])
def test_L6_wrong_shape_is_bad_shape_not_empty_board(root, board, response):
    seed_state(root, {board["id"]: ["x"], GH["id"]: ["1"]})
    boards = [board] if board is GH else [board, GH]
    script = {board["url"]: [response, response]}
    if board is not GH:
        script[GH["url"]] = [GH_OK]
    res, t, _ = go(root, boards, script)
    b = res.boards[board["id"]]
    assert b["status"] == "failed" and b["reason"] == "bad_shape"
    assert b["attempts"] == 1
    assert b["count"] is None and b["new"] is None
    assert read_state(root)[board["id"]] == ["x"]


# --- retries (GATE §5) -------------------------------------------------------

def test_L7_timeout_then_ok_retries_once_after_2s(root):
    seed_state(root, {LV["id"]: ["l1"]})
    res, t, clock = go(root, [LV], {LV["url"]: [TransportTimeout(), LV_OK]})
    assert res.boards[LV["id"]]["status"] == "ok"
    assert res.boards[LV["id"]]["attempts"] == 2
    assert clock.sleeps == [2]


@pytest.mark.parametrize("first,second", [
    (TransportTimeout(), TransportTimeout()),
    (TransportError(), TransportError()),
    (Response(503, b"", {}), Response(503, b"", {})),
], ids=["timeout", "connection", "5xx"])
def test_L8_transient_failure_twice_is_failed_and_bounded(root, first, second):
    """Wrong version #6: a third attempt must never happen."""
    seed_state(root, {LV["id"]: ["l1"], GH["id"]: ["1"]})
    res, t, _ = go(root, [LV, GH], {LV["url"]: [first, second, LV_OK], GH["url"]: [GH_OK]})
    assert res.boards[LV["id"]]["status"] == "failed"
    assert t.calls.count(LV["url"]) == 2
    assert res.exit == "incomplete"


def test_L9_429_long_retry_after_is_not_retried(root):
    seed_state(root, {LV["id"]: ["l1"], GH["id"]: ["1"]})
    res, t, _ = go(root, [LV, GH], {
        LV["url"]: [Response(429, b"", {"Retry-After": "10"}), LV_OK], GH["url"]: [GH_OK]})
    assert res.boards[LV["id"]]["status"] == "failed"
    assert t.calls.count(LV["url"]) == 1


def test_L10_429_short_retry_after_is_retried_once(root):
    seed_state(root, {LV["id"]: ["l1"]})
    res, t, _ = go(root, [LV], {LV["url"]: [Response(429, b"", {"Retry-After": "3"}), LV_OK]})
    assert res.boards[LV["id"]]["status"] == "ok"
    assert t.calls.count(LV["url"]) == 2


# --- budgets checked BEFORE the action (GATE §3, wrong version #7) -----------

def test_L11_request_budget_stops_before_overshoot(root):
    seed_state(root, {GH["id"]: ["1"], AS["id"]: ["a1"], LV["id"]: ["l1"]})
    budgets = dict(BUDGETS, max_requests=2)
    res, t, _ = go(root, [GH, AS, LV], {GH["url"]: [GH_OK], AS["url"]: [AS_OK], LV["url"]: [LV_OK]},
                   budgets=budgets)
    assert res.exit == "budget-exhausted" and res.budget_hit == "max_requests"
    assert len(t.calls) == 2 and res.requests_used == 2
    assert res.boards[LV["id"]]["status"] == "not_attempted"


def test_L12_seconds_rule_elapsed_plus_timeout(root):
    """Each fake request costs 50 s: starts at 0 and 50 are allowed (<=120 with +30);
    a start at 100 would need 130 > 120, so it is not started."""
    seed_state(root, {GH["id"]: ["1"], AS["id"]: ["a1"], LV["id"]: ["l1"]})
    res, t, _ = go(root, [GH, AS, LV], {GH["url"]: [GH_OK], AS["url"]: [AS_OK], LV["url"]: [LV_OK]},
                   cost=50.0)
    assert res.exit == "budget-exhausted" and res.budget_hit == "max_seconds"
    assert len(t.calls) == 2
    assert res.boards[LV["id"]]["status"] == "not_attempted"


def test_L13_board_budget(root):
    seed_state(root, {GH["id"]: ["1"], AS["id"]: ["a1"], LV["id"]: ["l1"]})
    budgets = dict(BUDGETS, max_boards=2)
    res, t, _ = go(root, [GH, AS, LV], {GH["url"]: [GH_OK], AS["url"]: [AS_OK], LV["url"]: [LV_OK]},
                   budgets=budgets)
    assert res.exit == "budget-exhausted" and res.budget_hit == "max_boards"
    assert LV["url"] not in t.calls


# --- repeat rule and state (GATE §4) ------------------------------------------

def test_L14_duplicate_board_is_skipped_not_refetched(root):
    seed_state(root, {GH["id"]: ["1"]})
    res, t, _ = go(root, [GH, GH], {GH["url"]: [GH_OK, GH_OK]})
    assert t.calls.count(GH["url"]) == 1
    assert res.skipped_duplicates == [GH["id"]]


def test_L15_new_and_removed_against_prior_state(root):
    seed_state(root, {GH["id"]: ["1", "2"]})
    res, _, _ = go(root, [GH], {GH["url"]: [ok({"jobs": [{"id": 2}, {"id": 3}]})]})
    b = res.boards[GH["id"]]
    assert b["count"] == 2 and b["new"] == ["3"] and b["removed"] == ["1"]
    assert sorted(read_state(root)[GH["id"]]) == ["2", "3"]


def test_L16_same_id_on_two_ats_does_not_collide(root):
    seed_state(root, {GH["id"]: ["9"], LV["id"]: ["l1"]})
    res, _, _ = go(root, [GH, LV], {GH["url"]: [ok({"jobs": [{"id": 9}]})],
                                    LV["url"]: [ok([{"id": "l1"}, {"id": "9"}])]})
    assert res.boards[GH["id"]]["new"] == []
    assert res.boards[LV["id"]]["new"] == ["9"]


def test_L17_first_sight_of_a_board_is_a_baseline_with_no_new(root):
    """Carried from the JS1 contract: the first run of a board is a baseline."""
    seed_state(root, {})
    res, _, _ = go(root, [GH], {GH["url"]: [GH_OK]})
    b = res.boards[GH["id"]]
    assert b["baseline"] is True and b["new"] == []
    assert sorted(read_state(root)[GH["id"]]) == ["1", "2"]


# --- record of every observation ----------------------------------------------

def test_L18_trace_and_report_are_written(root):
    seed_state(root, {GH["id"]: ["1"], BAD["id"]: []})
    res, t, _ = go(root, [GH, BAD], {GH["url"]: [GH_OK], BAD["url"]: [Response(404, b"{}", {})]})
    run_dir = root / "runs" / "test-run"
    lines = [json.loads(l) for l in (run_dir / "trace.jsonl").read_text().splitlines()]
    assert len([l for l in lines if l.get("event") == "attempt"]) == len(t.calls)
    report = json.loads((run_dir / "report.json").read_text())
    assert report["exit"] == res.exit == "incomplete"


# --- budgets live in a file that matches GATE §3 -----------------------------

def test_L19_gate_config_matches_gate_section_3():
    cfg = json.loads((Path(__file__).parents[1] / "gate_config.json").read_text())
    assert cfg == BUDGETS
