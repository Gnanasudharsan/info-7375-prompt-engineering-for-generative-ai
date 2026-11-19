# AUDIT.md — reject audit of filter v1.0 (FILTER.md 1.0, run 20261119T162945Z)
All numbers below are computed by scripts/audit_report.py from my blind hand verdicts. Nothing here is a measured rate for all postings.

## What was audited
- Corpus: 899 postings (anthropic, notion, spotify; the 404 board is absent, not zero). Filter v1.0 kept 17, rejected 882.
- My labels: blind (filter decision hidden), by audit/LABELING_RULE.md (the persona, not FILTER.md). Two samples:
  v1 = 30 random rejects (seed 7375) + 15 close calls (score 4-6) + 10 random kept (seed 7376); v2 = 30 more random rejects (seed 7378), excluding v1.

## 1. Random rejects (60 = v1 30 + v2 30)
- Postings I would call RELEVANT that the filter rejected: **1/60 blind**, **0/60 after my consistency correction** (v2 #27, recorded in FRICTIONAL). Could not tell: 1/60.
- Exact 95% interval for the false-reject rate **among random rejects**: blind 0.0% to 8.9%; corrected 0.0% to 6.0%.
- **What this sample can honestly show:** with 0 or 1 errors in 60, a false-reject rate of up to roughly 9% among rejects (about 79 of the 882 rejects) is still consistent with what I saw.
  It does **not** show the filter misses nothing, and it says little about rare relevant postings: most random rejects are plainly off-target (sales, legal, PM), so a random sample mostly tests the easy cases.

## 2. Kept postings (10 random of 17)
- My verdicts: RELEVANT 1, NOT_RELEVANT 3, CANNOT_TELL 6.
- Wrong keeps (I said NOT_RELEVANT): 3/10, exact 95% interval 6.7% to 65.2% — too wide to rank the filter's precision.
- **Why so many CANNOT_TELL — tested, not assumed:** of my 6 CANNOT_TELL kept postings, **0** mention no years of experience or level anywhere in the text and have no level word in the title.
  (An earlier version of this check used "A4 did not fire", which is true of every kept posting by construction; corrected.)
  **What they do say:** all 6 contain Anthropic's sentence "Minimum years of experience: Years of experience required will correlate with the internal job level requirements for the position" — years are mentioned but no number is given, so the level claim is *insufficient*. This sentence appears in 17 of 17 kept postings and in 638 of 638 Anthropic postings.
  My own check above matched "years of experience" inside that sentence: a false friend in the audit tool itself — the words match, but no requirement is stated.
  The filter never asked for a level signal: FILTER.md abstention rule (c) was not implemented (Claude Code choice #11). This motivates change C3 in FILTER.md v1.1.

## 3. Close calls (15, score 4-6)
- My verdicts: RELEVANT 1, NOT_RELEVANT 7, CANNOT_TELL 7. This is where my judgment and the threshold disagree most.

## 4. False friend (a word that matched for the wrong reason)
- **A6 "security clearance"** on v1 #3, Product Manager, Public Sector. Filter matched: `{"A1": "manager", "A4": "7+ years", "A6": "security clearance"}`.
  The posting says some portfolios require eligibility for a US security clearance, **though most do not**: the phrase matched, but the role does not require a clearance.
  Harmless here only because A1 and A4 also fired.
- Contrast, v2 #9 (Staff+ Software Engineer, Public Sector): A6 matched for the **right** reason ("Active federal security clearance (Secret or above)").

## 5. A miss found by the audit
- **A3** did not fire on v2 #9, although the text says "This position requires verification of U.S. citizenship". The A3 phrase list ("U.S. citizenship required", "must be a U.S. citizen") is too literal.

## 6. My predictions vs. what I found (audit/PREDICTIONS.md, written before labeling)
- Predicted ~5 wrong random rejects of 30: found 0 in v1 and 1 in v2 (blind).
- Predicted ~2 wrong keeps of 10: found 3, plus 6 I could not decide.
- Predicted Notion/Spotify kept 0 was a blind spot: not supported — every Notion/Spotify posting in my random samples was a correct reject by my labels.

## Rule changes after measuring
See FILTER.md changelog (v1.1): every rule added, cut, or rejected, with the numbers that motivated it.

## Every audited posting
### v1 random rejects
| board | title | filter | score | rejected_by | me | my reason |
|---|---|---|---|---|---|---|
| greenhouse:anthropic | Product Manager, Public Sector | reject | None | A1,A4,A6 | NOT_RELEVANT | This is a product management position, not a hands-on ML/AI engineering role. It focuses o |
| ashby:notion | Business Development Representative | reject | None | A2 | NOT_RELEVANT | This is a sales and business development position focused on lead generation, outbound cam |
| greenhouse:anthropic | Customer Program Manager, Executive Briefings | reject | None | A1,A4 | NOT_RELEVANT | This is a customer program management role focused on executive briefings, event coordinat |
| greenhouse:anthropic | Staff+ Application Security Engineer  - M&A   | reject | None | A1,A4 | NOT_RELEVANT | This is a staff-level application security position focused on cybersecurity, acquisition  |
| greenhouse:anthropic | Tabletop Exercise Lead, The Anthropic Institute | reject | None | A1,A4 | NOT_RELEVANT | This is an AI safety research program leadership role, not a hands-on ML/AI engineering po |
| greenhouse:anthropic | AWS Partnerships Lead | reject | None | A1,A2,A4 | NOT_RELEVANT | This is a business development and strategic partnerships role focused on AWS co-selling,  |
| lever:spotify | Senior Product Manager - Subscriptions (Premium Desirab | reject | None | A1,A2 | NOT_RELEVANT | This is a senior product management role focused on subscription growth, customer acquisit |
| greenhouse:anthropic | Staff+ Software Engineer, Experimentation | reject | None | A1,A4 | NOT_RELEVANT | This is a staff-level engineering position requiring senior technical leadership. Although |
| greenhouse:anthropic | Contracts Manager, GTM | reject | None | A1 | NOT_RELEVANT | This is a legal and commercial contracts management role involving contract drafting, nego |
| greenhouse:anthropic | Product Designer, Design Systems | reject | None | A4 | NOT_RELEVANT | This is a product design and UI/UX role focused on visual design systems, interface protot |
| greenhouse:anthropic | Learning & Education Specialist | reject | None | A4 | NOT_RELEVANT | This is a support operations and employee training position focused on onboarding, curricu |
| greenhouse:anthropic | Staff+ Software Engineer, Data Infrastructure | reject | None | A1,A4 | NOT_RELEVANT | Although this is a hands-on infrastructure engineering position, the title explicitly spec |
| greenhouse:anthropic | Product Support Specialist  | reject | None | A2 | NOT_RELEVANT | This is a customer and technical support position focused on resolving user issues, API tr |
| lever:spotify | Product Manager - Data Platform | reject | None | A1,A2 | NOT_RELEVANT | This is a product management position focused on data platform strategy, roadmaps, metadat |
| greenhouse:anthropic | Regional Research Economist, Economic Research | reject | None | A2 | NOT_RELEVANT | This is an economics and policy research role focused on econometrics, labor markets, AI's |
| greenhouse:anthropic | Enterprise Account Executive, Public Sector | reject | None | A2,A4 | NOT_RELEVANT | This is an enterprise sales role focused on selling Anthropic's AI products to government  |
| greenhouse:anthropic | Strategic Pursuits Lead, DACH | reject | None | A1,A2,A4 | NOT_RELEVANT | This is an enterprise sales strategy and business development leadership role focused on C |
| greenhouse:anthropic | Staff Software Security Engineer | reject | None | A1,A2,A4 | CANNOT_TELL | This is a staff-level cybersecurity and infrastructure security position, not hands-on ML/ |
| greenhouse:anthropic | Technical Deployment Lead | reject | None | A1,A2 | NOT_RELEVANT | Although the role involves deploying agentic AI solutions, it primarily focuses on project |
| greenhouse:anthropic | Software Engineer, Observability & Profiling | reject | None | A2,A4 | NOT_RELEVANT | The position involves hands-on infrastructure engineering, including telemetry pipelines,  |
| greenhouse:anthropic | Staff+ Software Engineer, Claude App Infrastructure | reject | None | A1 | NOT_RELEVANT | Although this is a hands-on engineering position involving AI agents, distributed systems, |
| greenhouse:anthropic | Corporate Development, Deal Lead | reject | None | A1,A4 | NOT_RELEVANT | This is a corporate development and mergers-and-acquisitions role focused on strategic par |
| greenhouse:anthropic | Research Product Manager, Labs | reject | None | A1,A4 | NOT_RELEVANT | Although this role involves AI research, technical prototyping, Claude Code, and MCP, its  |
| greenhouse:anthropic | Software Engineer, Sandboxing | reject | 1 | - | NOT_RELEVANT | This is a hands-on systems infrastructure engineering role focused on Linux kernel isolati |
| greenhouse:anthropic | Strategic Account Executive, Asset & Wealth Management | reject | None | A4 | NOT_RELEVANT | This is an enterprise sales and account management role focused on financial institutions, |
| greenhouse:anthropic | Regional Research Economist, Economic Research | reject | None | A2 | NOT_RELEVANT | This is an economics and public-policy research role focused on econometrics, labor market |
| greenhouse:anthropic | Partner Account Manager, Systems Integrators | reject | None | A1,A2,A4 | NOT_RELEVANT | This is a strategic partnerships and channel sales role focused on reseller relationships, |
| greenhouse:anthropic | Software Engineer, Business Technology | reject | None | A4 | NOT_RELEVANT | This is an internal full-stack product engineering role focused on building business appli |
| greenhouse:anthropic | Safeguards Enforcement Analyst, Integrity & Authenticit | reject | 2 | - | NOT_RELEVANT | This is primarily a trust and safety operations role focused on policy enforcement, invest |
| greenhouse:anthropic | IP Counsel, Transactions | reject | None | A4 | NOT_RELEVANT | This is a legal counsel role focused on intellectual property, mergers and acquisitions, c |
### v2 random rejects
| board | title | filter | score | rejected_by | me | my reason |
|---|---|---|---|---|---|---|
| ashby:notion | Software Engineering Intern, Frontend (Summer 2027) | reject | 1 | - | NOT_RELEVANT | Frontend development internship, not ML/AI engineering. |
| lever:spotify | State and Local Government Affairs Manager | reject | None | A1,A4 | NOT_RELEVANT | Government affairs and policy role requiring 5+ years, not ML/AI engineering. |
| greenhouse:anthropic | Research Engineer, Chip Design RL | reject | 3 | - | NOT_RELEVANT | Requires specialized chip design and RTL verification expertise outside Ananya's ML/NLP ba |
| greenhouse:anthropic | Community Engagement Manager, Data Centers (New York) | reject | None | A1,A4 | NOT_RELEVANT | Community relations and public policy role, not ML/AI engineering. |
| greenhouse:anthropic | Security Risk & Compliance, SOX IT  | reject | None | A4 | NOT_RELEVANT | Senior IT security and compliance role, not ML/AI engineering. |
| lever:spotify | Senior Software Engineer - Enterprise AI | reject | None | A1 | NOT_RELEVANT | Strong AI engineering match, but the role requires senior-level experience. |
| greenhouse:anthropic | Enterprise Account Executive - FSI | reject | None | A2,A4 | NOT_RELEVANT | Enterprise sales role in South Korea, not ML/AI engineering. |
| greenhouse:anthropic | Head of Regulated Industries, Customer Success | reject | None | A1,A4 | NOT_RELEVANT | Senior customer success leadership role, not hands-on ML/AI engineering. |
| greenhouse:anthropic | Staff+ Software Engineer, Public Sector | reject | None | A1,A4,A6 | NOT_RELEVANT | Staff-level engineering role involving government deployments and regulated systems, beyon |
| greenhouse:anthropic | Enterprise Account Executive, Federal Civilian Sales | reject | None | A4 | NOT_RELEVANT | Federal government sales role, not hands-on ML/AI engineering. |
| greenhouse:anthropic | Marketing Manager, Tech Partnership | reject | None | A1,A4 | NOT_RELEVANT | Tech partnership marketing role, not hands-on ML/AI engineering. |
| greenhouse:anthropic | Privacy Counsel  | reject | 0 | - | NOT_RELEVANT | Legal privacy role requiring a law degree, not ML/AI engineering. |
| ashby:notion | Field & Events Marketing Manager | reject | None | A1,A2 | NOT_RELEVANT | Events and marketing role based in South Korea, not ML/AI engineering. |
| ashby:notion | Outcomes Architect, MEA (Customer Success) | reject | None | A2 | NOT_RELEVANT | Customer success role based in Dublin, not hands-on ML/AI engineering. |
| greenhouse:anthropic | Account Executive, AI Native | reject | None | A4 | NOT_RELEVANT | AI product sales and account management, not hands-on ML/AI engineering. |
| greenhouse:anthropic |  Staff Software Engineer, Continuous Integration | reject | None | A1,A2,A4 | NOT_RELEVANT | Staff-level CI/CD engineering role in London, expecting 10+ years of experience. |
| lever:spotify | Senior Backend Engineer - Content Platform | reject | None | A1,A2 | NOT_RELEVANT | Senior backend engineering role in London/Stockholm, not ML/AI engineering. |
| lever:spotify | Account Executive - Commercial, Spotify Technology | reject | None | A4 | NOT_RELEVANT | Software sales role, not hands-on ML/AI engineering. |
| greenhouse:anthropic | Manager, Enterprise Sales - Asset & Wealth Management | reject | None | A1 | NOT_RELEVANT | Enterprise sales leadership role, not hands-on ML/AI engineering. |
| greenhouse:anthropic | Technical Program Manager, Life Sciences | reject | None | A1 | NOT_RELEVANT | Technical program management role focused on coordination and execution, not hands-on ML/A |
| greenhouse:anthropic | Policy Design Manager, Integrity and Authenticity | reject | None | A1,A4 | NOT_RELEVANT | AI safety policy development role, not hands-on ML/AI engineering. |
| greenhouse:anthropic | Staff+ Software Engineer, Safeguards Human Review Tooli | reject | None | A1,A4 | NOT_RELEVANT | Staff-level engineering role building AI safety tools, beyond new-grad experience requirem |
| greenhouse:anthropic | Head of Sales Excellence & Methodology | reject | None | A1 | NOT_RELEVANT | Senior sales leadership role focused on sales strategy and training, not hands-on ML/AI en |
| ashby:notion | Software Engineer, User Database Infrastructure | reject | None | A4 | NOT_RELEVANT | Backend database infrastructure role requiring technical leadership, not primarily ML/AI e |
| ashby:notion | Enterprise Solutions Consultant | reject | None | A2,A4 | NOT_RELEVANT | Customer-facing sales consulting role based in South Korea, not hands-on ML/AI engineering |
| greenhouse:anthropic | [Expression of Interest] Research Engineer / Scientist, | reject | None | A2 | NOT_RELEVANT | Relevant AI research work, but the position requires being based in London, outside the ta |
| greenhouse:anthropic | Manager, Applied AI Engineering (Megas)  | reject | None | A1,A4 | RELEVANT -> NOT_RELEVANT (after unblinding) | Strong match with applied AI, LLM architecture, evaluation frameworks, and production depl |
| ashby:notion | Commercial Outcomes Architect | reject | None | A2,A4 | NOT_RELEVANT | Mainly a customer success role focused on adoption and renewals, not AI engineering. It's  |
| greenhouse:anthropic | Staff+ Software Engineer, Full-stack | reject | None | A1 | CANNOT_TELL -> NOT_RELEVANT (after unblinding) | Interesting work building Claude products, but it's a staff-level role requiring much more |
| greenhouse:anthropic | Staff+ Software Engineer, Account Abuse | reject | None | A1,A4 | NOT_RELEVANT | Python, SQL, and data analysis are a good match, but it's a staff-level security engineeri |
### Close calls and kept
| board | title | filter | score | rejected_by | me | my reason |
|---|---|---|---|---|---|---|
| greenhouse:anthropic | Research Engineer, Knowledge Team | keep | 7 | - | CANNOT_TELL | Hands-on LLM engineering involving Python, fine-tuning, reinforcement learning, retrieval, |
| greenhouse:anthropic | Research Engineer / Research Scientist, RL Frontiers | keep | 6 | - | NOT_RELEVANT | Although the role involves hands-on reinforcement learning engineering and is US-based, it |
| greenhouse:anthropic | Research Engineer, Machine Learning (Reinforcement Lear | keep | 8 | - | CANNOT_TELL | The role matches Ananya's target of hands-on ML engineering, including reinforcement learn |
| greenhouse:anthropic | Performance Engineer, Inference Systems | keep | 5 | - | CANNOT_TELL | This is a hands-on AI infrastructure engineering role involving LLM inference, latency opt |
| greenhouse:anthropic | Research Engineer, Production Model Post-Training | keep | 6 | - | CANNOT_TELL | This is a strong match for Ananya's target field. The responsibilities include LLM fine-tu |
| greenhouse:anthropic | Data Science, Finance & Strategy | reject | 4 | - | NOT_RELEVANT | Although the title mentions Data Science and the role uses Claude-powered workflows, the r |
| greenhouse:anthropic | Research Scientist, Discovery (Engineering & Applied Sc | keep | 5 | - | NOT_RELEVANT | Although the role involves hands-on reinforcement learning, model training, and evaluation |
| lever:spotify | Research Scientist - Generative Audio | reject | 4 | - | CANNOT_TELL | This role involves genuine generative AI research, including diffusion models, flow matchi |
| greenhouse:anthropic | Applied AI Engineer, Beneficial Deployments, Life Scien | reject | 4 | - | CANNOT_TELL | This is genuinely hands-on applied AI engineering, involving Claude agents, production cod |
| greenhouse:anthropic | Research Engineer, Code RL (Reinforcement Learning) | keep | 7 | - | CANNOT_TELL | The posting requires deep Python expertise, including concurrent programming, and end-to-e |
| greenhouse:anthropic | Applied AI Architect,  Beneficial Deployments (Life Sci | reject | 4 | - | NOT_RELEVANT | Despite the Applied AI Architect title, this role primarily focuses on scientific communit |
| greenhouse:anthropic | Research Engineer / Performance Engineer, RL Distribute | keep | 6 | - | CANNOT_TELL | This is a hands-on engineering position supporting reinforcement learning infrastructure.  |
| greenhouse:anthropic | Research Engineer, Post-Training Model Evaluations | keep | 5 | - | CANNOT_TELL | This is a strong match for Ananya's ML/AI engineering interests. It involves LLM evaluatio |
| greenhouse:anthropic | Research Engineer / Scientist, Pre-training | keep | 6 | - | RELEVANT | This is a hands-on ML engineering role involving LLM pre-training, Python, PyTorch, model  |
| greenhouse:anthropic | Research Engineer, Machine Learning (RL Velocity) | keep | 6 | - | CANNOT_TELL | This is a genuine hands-on ML infrastructure engineering role involving reinforcement lear |
| greenhouse:anthropic | Research Engineer, Pretraining Scaling | keep | 7 | - | CANNOT_TELL | This is a hands-on ML engineering role involving LLM pretraining, performance optimization |
| greenhouse:anthropic | Research Engineer, RL Engineering | keep | 9 | - | CANNOT_TELL | This is genuinely hands-on ML engineering involving reinforcement learning, LLM training,  |
| greenhouse:anthropic | Security Engineer / Research Engineer, RL Security | keep | 6 | - | NOT_RELEVANT | Although this is a hands-on role involving reinforcement learning infrastructure, the prim |
| greenhouse:anthropic | Research Engineer, Cybersecurity RL | reject | 4 | - | NOT_RELEVANT | Although this role involves hands-on reinforcement learning, ML experiments, model evaluat |
| greenhouse:anthropic | Research Engineer, Cybersecurity RL (Reinforcement Lear | reject | 4 | - | NOT_RELEVANT | Although this role involves hands-on reinforcement learning, agentic AI, ML experimentatio |
