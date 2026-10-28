# Project brief — Terraform Docs, Quoted

**Varnika M** · INFO 7375 · Final project pitch · 2026-10-11

**1. What is it?** A Python command-line tool that answers questions about Terraform's AWS
provider from the official docs, and backs every answer with the exact docs line it came from, or
says "not in the docs." When done, it will be a public GitHub repository: the tool, a pinned copy
of about ten docs pages (MPL-2.0), tests, a labelled question set, and an evaluation log.

**2. Why would anyone care?** Terraform users need exact facts that change between versions. In
provider v6.68.0, `bucket` on `aws_s3_bucket` is Optional (line 54) and `versioning` is Deprecated
(line 70). Alternatives I tried on 2026-10-11, asking "Is `bucket` required on `aws_s3_bucket`?":
- **The Terraform Registry page:** the menu reaches the answer, but Cmd+F for "bucket" gave 220
  matches; the right one was number 70.
- **Claude (claude.ai, Sonnet 5.5):** said optional, which is correct, but added two details not on
  the docs page and did not say which docs or version it used. One reply, not a measure of accuracy.

Mine will answer in one step from a stated docs version, show the line, and check in code that the
line exists. Evidence: `evidence/alternatives/`.

**3. Who opens it?** Target role: AI software developer / software engineer. Reader: a hiring
manager or engineer on my GitHub. In the first sixty seconds they run one command with a question,
see the answer with its quoted line, then run the tests offline.

**4. What does it prove?** A prompt contract (Claude must reply as `answer`, `quote`, `line`),
source grounding (pinned docs only), verification in code (a made-up quote must be rejected), and
evaluation (a scored question set with every miss logged). A reviewer could conclude I can build
and measure a small, tested Python tool around Claude — not that it covers all of Terraform.

**5. In, out, first.** In: about ten AWS resource pages at one version. Out: it will not write or
run Terraform or touch a cloud account. First: the quote checker; you will know it ran when its
tests pass offline against the saved `aws_s3_bucket` page.

**6. What could sink it?** On the same page, `bucket` is Optional at the top (line 54) but Required
in the replication block (line 221). A search for "bucket" can pick the wrong line, and the quote
would still be real. I will record which section each line belongs to and test this exact case.

**7. Why this project?** A mix. Already have: Python and Terraform from my co-op, and Terraform in a
spring cloud computing course project (not public); a tested Python tool built with Claude Code,
my Reallocation Engine recipe with 22 offline tests (PR #21, open). Most of that code was written
by Claude Code at my direction; I set the rules, reviewed the results, and documented its limits.
New to me: retrieving the right section of a long document, and building a test set to score
answers.

**Exists today**
- Licence check of four Terraform repositories (`evidence/licence-check.txt`)
- The saved `aws_s3_bucket` page, v6.68.0, with its licence and sha256 (`evidence/aws-provider-docs/`)
- My two trials of the alternatives, with screenshots (`evidence/alternatives/`)
- This brief and the pitch film

**Will exist**
- The quote checker and its tests
- The question-answering tool with its JSON prompt contract
- About ten pinned docs pages
- A labelled question set, including questions the docs cannot answer
- An evaluation log listing every wrong answer
