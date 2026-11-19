# SHORTLIST.md — source-grounded shortlist (filter v1.1 keeps, run 20261119T162945Z)
15 postings x 5 claims = 75 claims. Labels are mine (shortlist/claim_labels.csv); the script's proposals and Codex's suggestions are kept beside them.

## Summary
- My labels: SUPPORTED 51, CONTRADICTED 0, INSUFFICIENT 24.
- I changed 3 of 75 proposed labels.
- Codex (OpenAI) suggested labels for 44 claims; I agreed with 41 and disagreed with 3 (Codex's labels were not shown while I labeled).
- Verdicts under the abstention rule: I CANNOT TELL 15.

## Relevance is not entailment
The filter kept these postings because their words matched (a role phrase in the title, topic words, skills). For each, I labeled the role claim "hands-on ML/AI engineering" as not supported by the posting's own text: the match made it relevant, but the text does not entail the claim.
- **Research Engineer, Post-Training Model Evaluations** — proposed SUPPORTED, mine **INSUFFICIENT**. Span: "About the role Anthropic's production models undergo sophisticated post-training processes to enhance their capabilities, alignment, and safety.". My note: The excerpt doesn't provide enough detail about the actual engineering responsibilities.
- **Security Engineer / Research Engineer, RL Security** — proposed SUPPORTED, mine **INSUFFICIENT**. Span: "At frontier scale, an RL run is a large distributed system: training, sampling, and environment execution run concurrently across a large fleet of accelerators and hosts.". My note: The excerpt describes RL infrastructure, not the role's specific engineering responsibilities.

## Abstention rule
From FILTER.md §2: the agent says **"I cannot tell"** instead of RELEVANT when a must-have claim (role, level, location) is INSUFFICIENT. A CONTRADICTED claim gives NOT RELEVANT. Only when role, level and location are all supported is a posting called RELEVANT.

## A counterexample that exposes the rule's limits
- **Research Engineer / Scientist, Pre-training**: the rule abstains ("I cannot tell") because the level claim is INSUFFICIENT — every Anthropic posting defers the level to an internal job level. But in my blind audit I judged this posting **RELEVANT**. The rule can only use what the text states; I used the description of the work as a whole. So the rule is safe (it never calls a posting relevant without evidence) but it is too strict for a source that never states a level: on this board it can never say RELEVANT.

## Every claim

### Machine Learning Infrastructure Engineer, Safeguards Research (greenhouse:anthropic 5364804008) — verdict: **I CANNOT TELL**
| claim | proposed | mine | Codex | span | my note |
|---|---|---|---|---|---|
| role: hands-on ML/AI engineering | SUPPORTED | **SUPPORTED** | - | Key responsibilities Build and scale the infrastructure and data pipelines behind Safeguards machine learning research Own the training, eva |  |
| level: realistic for a new grad | INSUFFICIENT | **INSUFFICIENT** | - | Annual Salary: $350,000 — $500,000 USD Logistics Minimum education: Bachelor’s degree or an equivalent combination of education, training, a |  |
| location: US-based or remote-US | SUPPORTED | **SUPPORTED** | - | location: San Francisco, CA / New York City, NY |  |
| sponsorship: does not rule out sponsorship | SUPPORTED | **SUPPORTED** | - | Visa sponsorship: We do sponsor visas! |  |
| skills: asks for skills she has shipped | SUPPORTED | **SUPPORTED** | - | found: python, transformers / Key responsibilities Build and scale the infrastructure and data pipelines behind Safeguards machine learning  |  |

### Research Engineer, Code RL (Reinforcement Learning) (greenhouse:anthropic 5254364008) — verdict: **I CANNOT TELL**
| claim | proposed | mine | Codex | span | my note |
|---|---|---|---|---|---|
| role: hands-on ML/AI engineering | SUPPORTED | **SUPPORTED** | - | Our work spans several key areas: Developing systems that enable models to use computers effectively Advancing code generation through reinf |  |
| level: realistic for a new grad | INSUFFICIENT | **INSUFFICIENT** | - | Annual Salary: $500,000 — $850,000 USD Logistics Minimum education: Bachelor’s degree or an equivalent combination of education, training, a |  |
| location: US-based or remote-US | SUPPORTED | **SUPPORTED** | - | location: San Francisco, CA / New York City, NY |  |
| sponsorship: does not rule out sponsorship | SUPPORTED | **SUPPORTED** | - | Visa sponsorship: We do sponsor visas! |  |
| skills: asks for skills she has shipped | SUPPORTED | **SUPPORTED** | - | found: python, pytorch / You may be a good fit if you: Have strong software-engineering skills and deep Python expertise, including async/co |  |

### Research Engineer, Knowledge Team (greenhouse:anthropic 4017331008) — verdict: **I CANNOT TELL**
| claim | proposed | mine | Codex | span | my note |
|---|---|---|---|---|---|
| role: hands-on ML/AI engineering | SUPPORTED | **SUPPORTED** | - | Your job will be to design new architectures for how information is organized, and train language models to optimally use those architecture |  |
| level: realistic for a new grad | INSUFFICIENT | **INSUFFICIENT** | - | Annual Salary: $350,000 — $850,000 USD Logistics Minimum education: Bachelor’s degree or an equivalent combination of education, training, a |  |
| location: US-based or remote-US | SUPPORTED | **SUPPORTED** | - | location: Remote-Friendly (Travel-Required) / San Francisco, CA / Seattle, WA / New York City, NY |  |
| sponsorship: does not rule out sponsorship | SUPPORTED | **SUPPORTED** | - | Visa sponsorship: We do sponsor visas! |  |
| skills: asks for skills she has shipped | INSUFFICIENT | **SUPPORTED** | - | found: python / You may be a good fit if you: Are a very experienced Python programmer who can quickly produce reliable, high quality code t | Python and LLM development match her skills, even though the role expects more e |

### Research Engineer, Machine Learning (Reinforcement Learning) (greenhouse:anthropic 4613568008) — verdict: **I CANNOT TELL**
| claim | proposed | mine | Codex | span | my note |
|---|---|---|---|---|---|
| role: hands-on ML/AI engineering | SUPPORTED | **SUPPORTED** | - | Our work spans several key areas: Developing systems that enable models to use computers effectively Advancing code generation through reinf |  |
| level: realistic for a new grad | INSUFFICIENT | **INSUFFICIENT** | - | Annual Salary: $500,000 — $850,000 USD Logistics Minimum education: Bachelor’s degree or an equivalent combination of education, training, a |  |
| location: US-based or remote-US | SUPPORTED | **SUPPORTED** | - | location: San Francisco, CA / New York City, NY |  |
| sponsorship: does not rule out sponsorship | SUPPORTED | **SUPPORTED** | - | Visa sponsorship: We do sponsor visas! |  |
| skills: asks for skills she has shipped | SUPPORTED | **SUPPORTED** | - | found: python, pytorch / You may be a good fit if you: Are proficient in Python and async/concurrent programming with frameworks like Trio H |  |

### Research Engineer, Machine Learning (RL Velocity) (greenhouse:anthropic 5198108008) — verdict: **I CANNOT TELL**
| claim | proposed | mine | Codex | span | my note |
|---|---|---|---|---|---|
| role: hands-on ML/AI engineering | SUPPORTED | **SUPPORTED** | - | About the role The RL Velocity team owns the efficiency and reliability of our RL Science stack - the infrastructure, tooling, and systems t |  |
| level: realistic for a new grad | INSUFFICIENT | **INSUFFICIENT** | - | Annual Salary: $500,000 — $850,000 USD Logistics Minimum education: Bachelor’s degree or an equivalent combination of education, training, a |  |
| location: US-based or remote-US | SUPPORTED | **SUPPORTED** | - | location: Remote-Friendly (Travel-Required) / San Francisco, CA / New York City, NY |  |
| sponsorship: does not rule out sponsorship | SUPPORTED | **SUPPORTED** | - | Visa sponsorship: We do sponsor visas! |  |
| skills: asks for skills she has shipped | INSUFFICIENT | **INSUFFICIENT** | - | found: pytorch / Responsibilities Build and improve the RL training infrastructure that researchers depend on day-to-day Identify and remove |  |

### Research Engineer / Performance Engineer, RL Distributed Systems (greenhouse:anthropic 5438030008) — verdict: **I CANNOT TELL**
| claim | proposed | mine | Codex | span | my note |
|---|---|---|---|---|---|
| role: hands-on ML/AI engineering | SUPPORTED | **SUPPORTED** | - | Training, sampling, and environment execution run concurrently across a large fleet of accelerators and hosts, exchange data continuously, a |  |
| level: realistic for a new grad | INSUFFICIENT | **INSUFFICIENT** | - | Annual Salary: $500,000 — $850,000 USD Logistics Minimum education: Bachelor’s degree or an equivalent combination of education, training, a |  |
| location: US-based or remote-US | SUPPORTED | **SUPPORTED** | - | location: San Francisco, CA / New York City, NY / Seattle, WA |  |
| sponsorship: does not rule out sponsorship | SUPPORTED | **SUPPORTED** | - | Visa sponsorship: We do sponsor visas! |  |
| skills: asks for skills she has shipped | INSUFFICIENT | **INSUFFICIENT** | - | found: python / Key responsibilities Design, build, and operate the distributed systems that run RL at scale, across training, sampling, and |  |

### Research Engineer, Post-Training Model Evaluations (greenhouse:anthropic 5198255008) — verdict: **I CANNOT TELL**
| claim | proposed | mine | Codex | span | my note |
|---|---|---|---|---|---|
| role: hands-on ML/AI engineering | SUPPORTED | **INSUFFICIENT** | - | About the role Anthropic's production models undergo sophisticated post-training processes to enhance their capabilities, alignment, and saf | The excerpt doesn't provide enough detail about the actual engineering responsib |
| level: realistic for a new grad | INSUFFICIENT | **INSUFFICIENT** | INSUFFICIENT | Annual Salary: $500,000 — $850,000 USD Logistics Minimum education: Bachelor’s degree or an equivalent combination of education, training, a |  |
| location: US-based or remote-US | SUPPORTED | **SUPPORTED** | SUPPORTED | location: San Francisco, CA / Seattle, WA |  |
| sponsorship: does not rule out sponsorship | SUPPORTED | **SUPPORTED** | SUPPORTED | Visa sponsorship: We do sponsor visas! |  |
| skills: asks for skills she has shipped | INSUFFICIENT | **INSUFFICIENT** | SUPPORTED | found: python / Responsibilities Steer the eval strategy for production Claude models: study and optimize the eval mix so it gives the most  |  |

### Research Engineer, Pretraining Scaling (greenhouse:anthropic 4938432008) — verdict: **I CANNOT TELL**
| claim | proposed | mine | Codex | span | my note |
|---|---|---|---|---|---|
| role: hands-on ML/AI engineering | SUPPORTED | **SUPPORTED** | SUPPORTED | About the Role: Anthropic's ML Performance and Scaling team trains our production pretrained models, work that directly shapes the company's |  |
| level: realistic for a new grad | INSUFFICIENT | **INSUFFICIENT** | INSUFFICIENT | Annual Salary: $350,000 — $850,000 USD Logistics Minimum education: Bachelor’s degree or an equivalent combination of education, training, a |  |
| location: US-based or remote-US | SUPPORTED | **SUPPORTED** | SUPPORTED | location: San Francisco, CA |  |
| sponsorship: does not rule out sponsorship | SUPPORTED | **SUPPORTED** | SUPPORTED | Visa sponsorship: We do sponsor visas! |  |
| skills: asks for skills she has shipped | INSUFFICIENT | **INSUFFICIENT** | INSUFFICIENT | found: pytorch / Responsibilities: Own critical aspects of our production pretraining pipeline, including model operations, performance opti |  |

### Research Engineer, Production Model Post-Training (greenhouse:anthropic 4613592008) — verdict: **I CANNOT TELL**
| claim | proposed | mine | Codex | span | my note |
|---|---|---|---|---|---|
| role: hands-on ML/AI engineering | SUPPORTED | **SUPPORTED** | SUPPORTED | About the role Anthropic's production models undergo sophisticated post-training processes to enhance their capabilities, alignment, and saf |  |
| level: realistic for a new grad | INSUFFICIENT | **INSUFFICIENT** | INSUFFICIENT | Annual Salary: $350,000 — $500,000 USD Logistics Minimum education: Bachelor’s degree or an equivalent combination of education, training, a |  |
| location: US-based or remote-US | SUPPORTED | **SUPPORTED** | SUPPORTED | location: San Francisco, CA / New York City, NY / Seattle, WA |  |
| sponsorship: does not rule out sponsorship | SUPPORTED | **SUPPORTED** | SUPPORTED | Visa sponsorship: We do sponsor visas! |  |
| skills: asks for skills she has shipped | INSUFFICIENT | **INSUFFICIENT** | SUPPORTED | found: python / Note: For this role, we conduct all interviews in Python. |  |

### Research Engineer / Research Scientist, RL Frontiers (greenhouse:anthropic 5438044008) — verdict: **I CANNOT TELL**
| claim | proposed | mine | Codex | span | my note |
|---|---|---|---|---|---|
| role: hands-on ML/AI engineering | SUPPORTED | **SUPPORTED** | SUPPORTED | You'll develop next-generation architectures and RL algorithms, take them from a small-scale result to a frontier-scale run, and understand  |  |
| level: realistic for a new grad | INSUFFICIENT | **INSUFFICIENT** | INSUFFICIENT | Annual Salary: $500,000 — $850,000 USD Logistics Minimum education: Bachelor’s degree or an equivalent combination of education, training, a |  |
| location: US-based or remote-US | SUPPORTED | **SUPPORTED** | SUPPORTED | location: San Francisco, CA / New York City, NY / Seattle, WA |  |
| sponsorship: does not rule out sponsorship | SUPPORTED | **SUPPORTED** | SUPPORTED | Visa sponsorship: We do sponsor visas! |  |
| skills: asks for skills she has shipped | SUPPORTED | **SUPPORTED** | SUPPORTED | found: python, pytorch / Key responsibilities Study how RL training and sampling scale with model size, context length, and compute, and fin |  |

### Research Engineer / Research Scientist, Tokens (greenhouse:anthropic 4951814008) — verdict: **I CANNOT TELL**
| claim | proposed | mine | Codex | span | my note |
|---|---|---|---|---|---|
| role: hands-on ML/AI engineering | SUPPORTED | **SUPPORTED** | SUPPORTED | You want to build large scale ML systems from the ground up. |  |
| level: realistic for a new grad | INSUFFICIENT | **INSUFFICIENT** | INSUFFICIENT | Annual Salary: $350,000 — $500,000 USD Logistics Minimum education: Bachelor’s degree or an equivalent combination of education, training, a |  |
| location: US-based or remote-US | SUPPORTED | **SUPPORTED** | SUPPORTED | location: New York City, NY; New York City, NY / Seattle, WA; San Francisco, CA |  |
| sponsorship: does not rule out sponsorship | SUPPORTED | **SUPPORTED** | SUPPORTED | Visa sponsorship: We do sponsor visas! |  |
| skills: asks for skills she has shipped | SUPPORTED | **SUPPORTED** | SUPPORTED | found: pytorch, transformers / You may be a good fit if you: Have significant software engineering experience Are results-oriented, with a b |  |

### Research Engineer, RL Engineering (greenhouse:anthropic 4952051008) — verdict: **I CANNOT TELL**
| claim | proposed | mine | Codex | span | my note |
|---|---|---|---|---|---|
| role: hands-on ML/AI engineering | SUPPORTED | **SUPPORTED** | SUPPORTED | This role sits on the team that builds and owns the RL training system: the system that trains our production models and that researchers ac |  |
| level: realistic for a new grad | INSUFFICIENT | **INSUFFICIENT** | INSUFFICIENT | Annual Salary: $500,000 — $850,000 USD Logistics Minimum education: Bachelor’s degree or an equivalent combination of education, training, a |  |
| location: US-based or remote-US | SUPPORTED | **SUPPORTED** | SUPPORTED | location: San Francisco, CA / New York City, NY / Seattle, WA |  |
| sponsorship: does not rule out sponsorship | SUPPORTED | **SUPPORTED** | SUPPORTED | Visa sponsorship: We do sponsor visas! |  |
| skills: asks for skills she has shipped | SUPPORTED | **SUPPORTED** | SUPPORTED | found: python, pytorch / Key responsibilities Build, own, and improve the core RL training system that serves Anthropic's production and res |  |

### Research Engineer / Scientist, Alignment (greenhouse:anthropic 4631822008) — verdict: **I CANNOT TELL**
| claim | proposed | mine | Codex | span | my note |
|---|---|---|---|---|---|
| role: hands-on ML/AI engineering | SUPPORTED | **SUPPORTED** | SUPPORTED | About the role: You want to build and run elegant and thorough machine learning experiments to help us understand and steer the behavior of  |  |
| level: realistic for a new grad | INSUFFICIENT | **INSUFFICIENT** | INSUFFICIENT | Annual Salary: $350,000 — $500,000 USD Logistics Minimum education: Bachelor’s degree or an equivalent combination of education, training, a |  |
| location: US-based or remote-US | SUPPORTED | **SUPPORTED** | SUPPORTED | location: San Francisco, CA |  |
| sponsorship: does not rule out sponsorship | SUPPORTED | **SUPPORTED** | SUPPORTED | Visa sponsorship: We do sponsor visas! |  |
| skills: asks for skills she has shipped | INSUFFICIENT | **INSUFFICIENT** | INSUFFICIENT | found: python / Note: For this role, we conduct all interviews in Python and prefer candidates to be based in the Bay Area. |  |

### Research Engineer / Scientist, Pre-training (greenhouse:anthropic 5468947008) — verdict: **I CANNOT TELL**
| claim | proposed | mine | Codex | span | my note |
|---|---|---|---|---|---|
| role: hands-on ML/AI engineering | SUPPORTED | **SUPPORTED** | SUPPORTED | We are seeking a Research Engineer to join our Pre-training team, responsible for developing the next generation of large language models. |  |
| level: realistic for a new grad | INSUFFICIENT | **INSUFFICIENT** | INSUFFICIENT | Annual Salary: $500,000 — $850,000 USD Logistics Minimum education: Bachelor’s degree or an equivalent combination of education, training, a |  |
| location: US-based or remote-US | SUPPORTED | **SUPPORTED** | SUPPORTED | location: Remote-Friendly (Travel-Required) / San Francisco, CA / Seattle, WA / New York City, NY |  |
| sponsorship: does not rule out sponsorship | SUPPORTED | **SUPPORTED** | SUPPORTED | Visa sponsorship: We do sponsor visas! |  |
| skills: asks for skills she has shipped | SUPPORTED | **SUPPORTED** | SUPPORTED | found: python, pytorch / Key Responsibilities Conduct research and implement solutions in areas such as model architecture, algorithms, data |  |

### Security Engineer / Research Engineer, RL Security (greenhouse:anthropic 5458420008) — verdict: **I CANNOT TELL**
| claim | proposed | mine | Codex | span | my note |
|---|---|---|---|---|---|
| role: hands-on ML/AI engineering | SUPPORTED | **INSUFFICIENT** | SUPPORTED | At frontier scale, an RL run is a large distributed system: training, sampling, and environment execution run concurrently across a large fl | The excerpt describes RL infrastructure, not the role's specific engineering res |
| level: realistic for a new grad | INSUFFICIENT | **INSUFFICIENT** | INSUFFICIENT | Annual Salary: $320,000 — $405,000 USD Logistics Minimum education: Bachelor’s degree or an equivalent combination of education, training, a |  |
| location: US-based or remote-US | SUPPORTED | **SUPPORTED** | SUPPORTED | location: San Francisco, CA / New York City, NY / Seattle, WA |  |
| sponsorship: does not rule out sponsorship | SUPPORTED | **SUPPORTED** | SUPPORTED | Visa sponsorship: We do sponsor visas! |  |
| skills: asks for skills she has shipped | INSUFFICIENT | **INSUFFICIENT** | INSUFFICIENT | found: python / Key responsibilities Design, build, and operate security controls for RL training systems and the infrastructure they run on |  |
