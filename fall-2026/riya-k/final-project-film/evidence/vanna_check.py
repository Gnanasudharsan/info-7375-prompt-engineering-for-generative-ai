#!/usr/bin/env python3
"""One hands-on try of Vanna 2.0.2 on Chinook (2026-10-21).

Question: does Vanna's own evaluation catch the join fan-out mistake (Q03)?

What runs: Vanna's SqliteRunner executes the gold SQL and the fan-out SQL on a
temporary copy of Chinook (the runner commits non-SELECT statements, so it never
touches the real file). Each result is scored by Vanna's built-in OutputEvaluator,
the check it offers for answers: "does the final answer contain these words?"
Then the same two results are compared row by row, the way run_slice.py does.

What does not run: Vanna's LLM step. That needs a paid model key, which this
assignment does not use, so the agent's answer is stood in by the query result.

Usage:  pip install vanna==2.0.2 pandas
        python3 vanna_check.py
"""
import asyncio
import shutil
import sqlite3
import tempfile
from pathlib import Path

from vanna.capabilities.sql_runner import RunSqlToolArgs
from vanna.core.evaluation import AgentResult, ExpectedOutcome, OutputEvaluator, TestCase
from vanna.core.user import User
from vanna.integrations.sqlite import SqliteRunner

HERE = Path(__file__).resolve().parent

GOLD = ("SELECT BillingCountry, ROUND(SUM(Total), 2) AS revenue FROM Invoice "
        "GROUP BY BillingCountry ORDER BY revenue DESC LIMIT 3")
FANOUT = ("SELECT i.BillingCountry, ROUND(SUM(i.Total), 2) FROM Invoice i "
          "JOIN InvoiceLine il ON il.InvoiceId = i.InvoiceId "
          "GROUP BY i.BillingCountry ORDER BY 2 DESC LIMIT 3")


class QueryResultAnswer(AgentResult):
    """Stands in for the agent's answer: the query result as text (no LLM ran)."""

    def __init__(self, test_case_id, text):
        super().__init__(test_case_id=test_case_id, components=[])
        self.text = text

    def get_final_answer(self):
        return self.text


async def main():
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "chinook_copy.sqlite"
        shutil.copy(HERE / "data" / "Chinook_Sqlite.sqlite", db)
        runner = SqliteRunner(database_path=str(db))
        gold = await runner.run_sql(RunSqlToolArgs(sql=GOLD), context=None)
        fanout = await runner.run_sql(RunSqlToolArgs(sql=FANOUT), context=None)

    print("Q03  What is total revenue by country? Show the top 3.")
    print("gold rows   :", gold.values.tolist())
    print("fan-out rows:", fanout.values.tolist())
    print()

    case = TestCase(
        id="Q03",
        user=User(id="riya-k"),
        message="What is total revenue by country? Show the top 3.",
        expected_outcome=ExpectedOutcome(final_answer_contains=["USA", "Canada", "France"]),
    )
    evaluator = OutputEvaluator()
    for name, df in (("gold", gold), ("fan-out", fanout)):
        verdict = await evaluator.evaluate(case, QueryResultAnswer("Q03", df.to_string()))
        print(f"Vanna OutputEvaluator on {name:<8}: {'PASS' if verdict.passed else 'FAIL'}"
              f"  -- {verdict.reasoning}")

    same = sorted(map(tuple, gold.values.tolist())) == sorted(map(tuple, fanout.values.tolist()))
    print(f"Row-by-row comparison on fan-out : {'PASS' if same else 'FAIL'}"
          f"  -- revenue values differ from the gold rows")


if __name__ == "__main__":
    asyncio.run(main())
