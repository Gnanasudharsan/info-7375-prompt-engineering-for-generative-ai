# rayudu-h

A place for the public work of Rayudu H — INFO 7375, Fall 2026.

I'm doing my MS in AI Systems Engineering at Northeastern, finishing in December 2026. Most of what I build is AI that has to hold up in front of real users: retrieval, agents, and the data pipelines underneath them. This course is where I get to slow down and look closely at the parts I usually take for granted, starting with what a model is actually doing when it picks the next word.

## Submissions

| Week | Assignment | What it is | Status |
|---|---|---|---|
| 1 | [`week-01-video/`](week-01-video/) | **Temperature Is Concentration, Not Truth**: a 3-minute explainer on what the temperature setting really controls | Posted; the video goes to Canvas |
| Final | [`final-project-film/`](final-project-film/) | **Electricity Supplier Check**: a 3:38 pitch film for a tool that will read a Massachusetts electric bill and show what you paid versus basic service, with the math done in code | Posted; the film goes to Canvas |

## Week 1

Everyone calls temperature the "creativity dial." I don't think that's right, and I wanted to show why with the actual math instead of a metaphor.

Divide one outcome's probability by another's and the softmax denominator cancels out. What's left depends only on the gap between the two scores, divided by T. That one line explains what temperature does. It only changes how spread out the choices are. It can never flip which answer comes out on top, and it can't add information the model didn't already have. Turn the contrast all the way up on a photo of the wrong person and you just get a sharper picture of the wrong person.

Every number in the video comes from the course's own `main.py` (scores `[1, 2, 3]`, seed 7), so you can check them yourself:

```bash
cd lessons/01-randomness-and-first-prompts/code
python3 main.py                                                                  # the T = 1 numbers
python3 -c "from main import sample; print(sample([1, 2, 3], temperature=2.0))"  # T = 2: {1: 329, 0: 202, 2: 469}
```

The video itself goes to Canvas, since this repo doesn't keep media files in Git. Everything you'd need to rebuild it is in [`week-01-video/`](week-01-video/): the beat sheet, the Manim scenes, captions, the build steps, and my log of what broke along the way.

## Final project pitch film

I overpaid on my own electric bill because I was on a competitive supplier and didn't catch it. The Massachusetts Attorney General found that residential customers on competitive supply paid $738.7 million more than basic service over the last decade. **Electricity Supplier Check** will read a bill and tell you exactly how much more, or less, you paid than basic service. Claude will read the bill and explain the result; Python will do all the math, and a verifier will reject any number that code didn't compute.

Nothing is built yet; the film is a pitch. As before, the film itself goes to Canvas because this repo keeps audio and video out of Git. Everything else is in [`final-project-film/`](final-project-film/): the brief, the beat sheet, the scene code, the gate reports, and my log.
