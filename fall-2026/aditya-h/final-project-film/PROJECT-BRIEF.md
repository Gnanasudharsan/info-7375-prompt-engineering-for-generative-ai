# PROJECT-BRIEF: ProductLens AI

Aditya Hasija · INFO7375 · Final project pitch (resubmission) · 2026-10-25
Target role: **AI Product Manager / Product Manager**

## 1. What is it?
ProductLens AI is a research assistant that helps a product manager decide whether to build a feature in a product that
already exists, and what to test first. The PM describes the feature and the goal (for example, a one-page checkout for an
online shoe store, to get more completed purchases) and attaches a few public articles. ProductLens will return a
**one-page decision brief**: the biggest risks, the numbers to watch, and the first experiment to run, with **every claim
labelled as backed by a source or as an assumption**.
**The artifact when it's done:** a **GitHub repository** with a small web app, a command-line runner, a test set of made-up
feature ideas with planted mistakes, and a score sheet showing how well it did.

## 2. Why would anyone care?
A PM can already ask a chatbot. **On Oct 25 I tested that myself.** I gave ChatGPT the shoe-store idea plus a made-up
claim attributed to a real source: "Baymard Institute research shows one-page checkouts always convert better." Baymard's
own article says it depends. ChatGPT caught it immediately ("The premise is incorrect"), and its advice was solid. But only
one paragraph had a source, it labelled almost nothing as fact or guess, and nothing checked that the source said what the
sentence claimed (screenshots and notes: `research/baseline-v2-*`).
- **DimeADozen** and **ValidatorAI** (homepages read Oct 14 and Oct 25) validate and score startup ideas.
- **The difference:** ProductLens is for a narrower, everyday job, **one feature in an existing product**. Every claim
  will carry a sourced/assumption label, and **code, not the model,** will check that each quoted passage really appears in its
  source. The test scores will be public, including where it fails. I'm not claiming the other tools are worse; I didn't
  buy their reports.

## 3. Who opens it, and what do they do?
**A hiring manager for an AI product role.** In the first minute they'll read the README, open one real sample brief, and
see the score sheet: how often the checker caught the planted mistakes, misses included. The end user is a PM weighing a
feature, who reads the brief in about five minutes.

## 4. What does it prove about me?
That I can write clear instructions an AI has to follow, check its answers against sources, and measure how well it
works. The course terms for these are **prompt contracts** (versioned instructions plus a schema each agent's output must
pass), an **agent loop** (three agents plus a checker that can send one back, once), **source grounding** (quote checks
in code), and **evaluation** (a planted-mistake test set and a score sheet). **The evidence will be** saved run logs, the
score sheet, and a written list of where it failed. It **won't** prove I'm a machine learning engineer.

## 5. What's in, what's out, what comes first?
- **In:** three agents (market, customers, risks) plus a checker, decision briefs with labels, quote checks, 10 made-up
  test ideas with planted mistakes, and a simple web app.
- **Out (deliberately):** no **go / no-go verdict** (it suggests the test; people decide), no live company data, no real
  A/B tests, no accounts.
- **First to run:** one research agent on one feature idea, from the command line. **How you'd know it ran:** it saves a
  JSON log, the log passes the schema check, and every quoted source is found in the attached article.
- **Built** with Claude Code from my own prompts, in two weeks.

## 6. What could sink it?
**A checker that agrees with everything:** it's the same AI grading its own team. My own test showed chatbots already
catch the obvious made-up claims, so the test ideas will hide subtler mistakes. *What I'll do:* count how many planted
mistakes it catches. If it misses too many, those checks move out of the model and into plain code, and I'll report the
number either way.

## 7. Why this project?
It's a mix of learning something new and showing what I already do.
- **Skills I have:** years in product roles writing requirements and doing research. Evidence on GitHub (AdityaHasija37):
  **WorkShip** (requirements and wireframes, team of five), **SkillPort** (React/Node app), and **Touchline** (Next.js +
  Supabase app).
- **New to me:** building and testing AI agents: orchestration, evaluation design, and grounding checks.
- **Why I changed from my first pitch:** in my words, "Because i wanted the project to be more suited for product managers
  and it has more of a value proposition and better use cases this way. The earlier version was too close to a AI wrapper."

---
**Exists today**
- The idea and two written outlines: the AI Product Failure Lab blueprint (Oct 14, written with ChatGPT) and the
  ProductLens script (Oct 25, written by me and refined with ChatGPT)
- First-pitch tests (Oct 14, run by Claude Code at my direction): 3 plain-Claude runs and 1 ChatGPT run (`research/`)
- **My own test (Oct 25, run by me):** ChatGPT on the checkout idea with a planted Baymard claim, with screenshots (`research/baseline-v2-*`)
- The first pitch film and its grade (archived)

**Will exist**
- The agent instructions and schemas, three agents plus the checker, and the quote checker
- The 10-idea planted-mistake test set and the score sheet
- Run logs, FAILURES.md, the web app, and a README with a sample brief
