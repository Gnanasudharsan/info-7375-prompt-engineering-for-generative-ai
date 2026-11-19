"""Review-packet tests for GATE Amendment 1 (suspect_empty). Written by me BEFORE the patch;
expected to FAIL on the current loop, which treats a 200 {"jobs": []} as a normal empty board
(reproduced live in FINISHED_WRONG_ANSWER.md, run 20261106T203850Z-SEEDED-A)."""
import json
from jobwatch.loop import run_loop, Response
from jobwatch.policy import Policy
from .test_loop import GH, AS, LV, GH_OK, BUDGETS, Clock, FakeTransport, ok, seed_state, read_state, root  # noqa: F401

EMPTY = Response(200, json.dumps({"jobs": []}).encode(), {})


def go(root, boards, script, approved=False):
    clock = Clock()
    t = FakeTransport(script, clock)
    res = run_loop(boards, root=root, policy=Policy(root), transport=t, budgets=BUDGETS,
                   clock=clock, sleep=clock.sleep, run_id="review-run", approved=approved)
    return res, t


def test_R1_empty_200_after_nonempty_is_suspect_without_approval(root):
    seed_state(root, {AS["id"]: ["a1", "a2"], GH["id"]: ["1"]})
    res, t = go(root, [AS, GH], {AS["url"]: [EMPTY, EMPTY], GH["url"]: [GH_OK]})
    b = res.boards[AS["id"]]
    assert b["status"] == "failed" and b["reason"] == "suspect_empty"
    assert b["new"] is None and b["removed"] is None
    assert t.calls.count(AS["url"]) == 1                      # not retried
    assert read_state(root)[AS["id"]] == ["a1", "a2"]         # state kept
    assert res.exit == "incomplete"                           # never "finished"


def test_R2_with_approval_the_board_is_reset_to_empty(root):
    seed_state(root, {AS["id"]: ["a1", "a2"]})
    res, _ = go(root, [AS], {AS["url"]: [EMPTY]}, approved=True)
    b = res.boards[AS["id"]]
    assert b["status"] == "ok" and b["count"] == 0
    assert b["removed"] == ["a1", "a2"]
    assert read_state(root)[AS["id"]] == []
    assert res.exit == "finished"


def test_R3_first_sight_empty_is_still_a_baseline(root):
    seed_state(root, {})
    res, _ = go(root, [AS], {AS["url"]: [EMPTY]})
    b = res.boards[AS["id"]]
    assert b["status"] == "ok" and b["baseline"] is True and b["count"] == 0
    assert res.exit == "finished"


def test_R4_already_empty_stays_ok(root):
    seed_state(root, {AS["id"]: []})
    res, _ = go(root, [AS], {AS["url"]: [EMPTY]})
    assert res.boards[AS["id"]]["status"] == "ok"
    assert res.exit == "finished"


def test_R5_rule_applies_to_lever_lists_too(root):
    seed_state(root, {LV["id"]: ["l1"], GH["id"]: ["1"]})
    res, _ = go(root, [LV, GH], {LV["url"]: [ok([])], GH["url"]: [GH_OK]})
    assert res.boards[LV["id"]]["reason"] == "suspect_empty"
    assert read_state(root)[LV["id"]] == ["l1"]
