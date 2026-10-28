# DESIGN — Source Check pitch film (HyperFrames body beats)

## Style Prompt
Calm, editorial explainer on the Claude cream page: warm ink type, white cards with hairline borders, one terracotta accent per beat for the thing the voice is pointing at. Every picture shows the real object (a chat bubble, a policy line, a JSON claim, a terminal) instead of a symbol for it. Motion is quiet and lands on the spoken word.

## Colors
| Role | Hex | Use |
|---|---|---|
| page | `#FAF9F5` | ground |
| card | `#FFFFFF` | cards, terminal paper |
| border | `#E5E2D9` | hairlines |
| ink | `#3D3929` | all body text |
| ink-soft | `#6B6857` | secondary text (4.9:1 on page) |
| spark | `#D97757` | fills, rules, outlines only (never text on cream: 2.75:1) |
| mark | `#F6DCCF` | highlight behind ink text (the conflicting word) |
| hold | `#A3402A` | HOLD stamp fill, white text |
| pass | `#3E6B4C` | PASS fill, white text |
| term | `#2B2A25` | terminal ground, text `#F3F1EA` |

## Typography
- Inter (UI and body), 600-800 for headings; body never under 34px; labels never under 30px.
- JetBrains Mono for JSON and terminal output, 30px+.

## Layout
- 1920x1080. Content inside x 120-1800, y 70-860.
- y > 880 is the caption band and the bottom-right corner is the @Mayank handle: keep both empty.
- Top-right chip says what the beat is: `real case`, `real output`, or `proposed design`.

## What NOT to Do
- No terracotta text on cream; use ink on the `mark` highlight instead.
- No generic icons standing in for an idea the narration names; draw the real artifact.
- No numbers that the slice or the sources do not contain.
- No exit animations; one scene per beat, the cut is the exit.
