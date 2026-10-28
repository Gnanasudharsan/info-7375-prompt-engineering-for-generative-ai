# Five-minute show and tell: notes

## Executive summary

An outline for the in-class five minutes: no slides, the mode file and the terminal. It follows the four things the assignment asks for, with the one thing to show for each. Nothing here is a script to read aloud.

## The five minutes

1. **The situation (45 seconds).** A teaching professor with a full-time job who wants part-time, paid research. Labs do not advertise that, so the usual move is to write to forty of them. Show the recipe's executive summary.
2. **The asymmetry (60 seconds).** A lab's page never says whether it can pay. The money is public. Show the one line of the report: six institutions, 349 awards, 223 that could pay for work starting in January.
3. **A real run (90 seconds).** Run `python3 scripts/funding/check-awards.py ...` live (it takes about six seconds) and open the Markdown report. Point at the column that matters: research awards running into the window, against the trainee-only ones that do not count.
4. **One thing I learned from it (60 seconds).** My own recipe was wrong: I wrote that the database wants exact organisation names. The break attempt `NORTHEASTERN UNIV` matched anyway, and `HARVARD` matched three organisations. Show `runs/13a-break-attempt-1-redone.txt`.
5. **One honest limitation (45 seconds).** It lists funded *projects*, not *groups that want a collaborator*. Whose award each one is, and whether they would talk, is a human look the mode deliberately leaves to a person. And the Boston wage floor did not run: its data is not in the repository.

## If asked

- Why DRAFT and not RUNNABLE-SAMPLE? Six typed TODOs are decisions only the person whose search this is can close, and the lifecycle requires zero open TODOs before the next stage.
- Why not use the engine's scan? It matches title substrings only: it kept `Director, Technical Revenue Accounting` for the word "Account".
