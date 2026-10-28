# Whisper check (faster-whisper small.en), v2, 2026-10-25

| Beat | Words not heard | Transcript |
|---|---|---|
| BIDEA | hasija | Hi, I'm Aditya Hasidja. Product managers ask one question all the time. Should we build this feature? I think a better question is, what should we test first? |
| B00 | — | Say you're a product manager at an online shoe store and your team wants a one-page checkout. |
| B01 | — | Before you build it, you need to know what customers want, what other stores do, and what could go wrong. That research takes days, and a good-sounding idea isn't always a good decision. |
| B02 | productlens | That's the job of my project, Product Lens AI. You type in the feature and the goal, say, more completed purchases and attach a few public articles. It will give back a one-page decision brief. |
| B03 | — | The brief will list the biggest risks, the numbers to watch, like checkout completion and the first experiment to run. Every claim in it will be marked, backed by a source or an assumption. |
| B04 | — | Inside, three AI agents will each take one angle, the market, the customers, and the risks. A fourth agent, the checker, compares their work to the sources and can send one back to fix it once. |
| B05 | cant, chatgpt, baymard | Can a chatbot already do this? I tested it myself. On October 25th, I gave Chat GPT the shoe store idea plus a made up claim. Baymart, a checkout research firm, says one page checkouts always convert better. Their research says it depends. |
| B06 | — | It caught my made-up claim right away, and the advice was solid. But only one paragraph had a source, and it rarely said which points were facts and which were guesses. |
| B07 | dimeadozen, validatorai, productlens, labelled | That's the gap I'm aiming at. Tools like dime, a dozen, and validator AI already score whole startup ideas. Product lens is for one feature in a product that already exists with every claim labeled and checked. |
| B08 | — | When it's done, it will be a GitHub repository with the app, a set of made-up test ideas, and a score sheet. |
| B09 | — | If you're hiring for an AI product role, you'd open it and within a minute, see one sample brief and how often the checker caught planted mistakes, misses included. |
| B10 | an | It should show that I can write clear instructions and AI has to follow, check its answers against sources, and measure how well it works. It won't show I'm a machine learning engineer. |
| B11 | — | The first step is small. One agent, one feature idea run from the command line. You'll know it worked when it saves a log where every quoted source checks out. |
| B12 | ab | It won't plug into company data, run real a slash b tests or say go or no go. It suggests the test, people decide. |
| B13 | — | The biggest risk is a checker that agrees with everything, since it's the same AI grading its own team. |
| B14 | ten | So I'll hide mistakes in 10 test ideas and count how many it catches. If it misses too many, those checks move into plain code. |
| B15 | — | I changed this from my first pitch, a pre-mortem tool for startup ideas, because it was too close to an AI wrapper. I wanted something built for product managers, with real, everyday use. |
| B16 | workship | Why this project? It's a mix. I've spent years in product roles, writing requirements, and doing research, and my work ship, Skillport, and Touchline projects are on GitHub. Building and testing AI agents is the new part. |
| B17 | productlens, and | Today Product Lens is a plan, the idea, a written outline in my chatbot test, everything else I'll build with Claude Code in the next two weeks. |
| BOUT | productlens, hasija | Product Lens AI, Aditya Haseedjaw. |

## Fixes and verdict (Claude Code, 2026-10-25)
- **B12:** Kokoro read "A/B" as "a slash b". Added a voice-only rewrite ("A B") in `pronunciation/aditya.json` and re-voiced B12.
- Everything else is spelling: ProductLens → "Product Lens", ChatGPT → "Chat GPT", DimeADozen → "dime, a dozen",
  Baymard → "Baymart", WorkShip → "work ship", and "Hasija" is spoken via Aditya's chosen respelling (version A).
- B05 "Can't" sounds close to "Can"; the question reads the same either way. No words are dropped.
