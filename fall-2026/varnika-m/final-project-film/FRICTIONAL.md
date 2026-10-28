# Frictional — Final project pitch film

Varnika M · INFO 7375 · *Terraform Docs, Quoted*

Entries are dated on the day they happened. Claude Code (NEU-provisioned) organized these notes
from the session; the "What I understand now" lines are mine.

---

### 2026-10-11 — Choosing the project took several turns

- **What I was working on:** picking a final project for an AI Software Developer / Software
  Engineer role that I can keep building after the course.
- **What happened:** the first suggestion was a ghost-job checker that adds the missing liveness
  check to my Reallocation Engine recipe. I asked for document-Q&A ideas instead, then for
  something low-stakes, then for something tied to my role. I picked Terraform docs.
- **What I decided:** Terraform AWS provider docs, because the answers are exact (Required,
  Optional, Deprecated), so they can be tested.
- **What I understand now:** A project with exact, checkable answers is easier to test.

### 2026-10-11 — Can Terraform docs be used after 2023?

- **I expected:** that the 2023 licence change might stop me from using the docs.
- **What happened:** Claude Code checked the GitHub licence fields. `hashicorp/terraform` (the core
  tool) is under the Business Source License from version 1.6.0. `hashicorp/terraform-provider-aws`
  is MPL-2.0, and so is `opentofu/opentofu`. The docs can be read and downloaded; the question was
  only about copying them into my repository.
- **What I did:** use only AWS provider docs, keep the MPL-2.0 licence beside the copied page, and
  pin the version. The saved `aws_s3_bucket` page is identical to release `v6.68.0`.
- **Evidence:** `evidence/licence-check.txt`, `evidence/README.md`.
- **Decided (2026-10-14):** the MPL-2.0 licence allows copying the
  page as long as the licence travels with it and the source is credited, which it does.

### 2026-10-11 — Found the project's main risk while collecting evidence

- **What happened:** on the same `aws_s3_bucket` page, `bucket` is Optional at the top level
  (line 54) but Required inside the replication `destination` block (line 221).
- **Why it matters:** a keyword search could retrieve the wrong line, and the quote checker alone
  would not catch it, because the quote is real. This became the risk in question 6.

### 2026-10-11 — Trying the Terraform Registry docs myself

- **What I did:** opened the `aws_s3_bucket` page on registry.terraform.io (version 6.68.0, latest,
  published October 7, 2026) and looked for the answer to "Is `bucket` required?" two ways.
- **Menu:** "Argument Reference" in the page menu took me to `bucket` - (Optional, Forces new
  resource).
- **Cmd+F "bucket":** 220 matches. The argument was match 70 of 220; many matches are names in the
  side menu (`aws_s3_bucket_acl`, `aws_s3_bucket_policy`, …).
- **Evidence:** four screenshots I took, in `evidence/alternatives/`. The menu was a bit faster
  than Cmd+F.
- **What I understand now:** The answer was on the page, but finding it took effort.

### 2026-10-11 — Asking Claude the same question

- **What I did:** asked claude.ai (Sonnet 5.5, Free plan, new chat): "Is the bucket argument
  required on aws_s3_bucket in Terraform?" and took a screenshot.
- **What happened:** it said optional, which matches the docs. Claude Code checked each detail
  against the saved docs page: four matched; the `terraform-` + timestamp naming and the
  3-character minimum are not on that page. No source or version was given.
- **Privacy:** my screenshot showed private chat titles in the sidebar. Claude Code saved only a
  cropped copy of the answer; the full screenshot is not in the folder.
- **What I understand now:** Claude was mostly right but added details I couldn't check.

### 2026-10-11 — My Brutalist checkout has no show-tell skill

- **What happened:** my local `brutalist.art` is at `6a8380a`. The show-tell skill the assignment
  recommends is in upstream `main` (`b21f625`), not in my copy.
- **What I did:** checked first that the update does not touch `requirements.txt`, `setup`, or
  `runtime/remotion/package-lock.json` (where my copy has an uncommitted change). Then, on my
  go-ahead, Claude Code ran `git pull --ff-only`: `6a8380a` → `b21f625`, 45 commits. No toolkit
  code was edited by hand.
- **Result:** `skills/make/show-tell/` is now present; `./art --help` runs. My local
  `package-lock.json` change is still there, untouched.
- **Note:** my Week 01 video was built at `6a8380a`; to rebuild it, check out that revision first.

### 2026-10-11 — The show-tell defaults conflict with the assignment

- **What happened:** the show-tell skill defaults to the narrator "Liam, in for Bear" and a spoken
  "At Nik Bear Brown" outro. The assignment says to narrate as myself and not use the instructor's
  name, persona or credit line.
- **What I decided:** first-person narration as me, no instructor bookends, my own title and name in
  the outro. Recorded in `beat_sheet.json` metadata.
- **Voice (decided 2026-10-11):** a computer voice (Kokoro), disclosed in `SOURCES.md`. I first took `af_heart`,
  then switched to `am_onyx`, the voice from my Week 01 video. Claude Code pointed out that the
  toolkit also uses `am_onyx` for the instructor's "Liam" narrator; I kept it, and the film uses
  none of that persona.

### 2026-10-11 — Building the film: what changed from the plan

- **Beats split:** B07 and B12 ran over 20 seconds each, and show-tell asks for one idea per beat,
  so they became B07A/B07B and B12A/B12B. The words did not change.
- **B13 corrected:** it said "everything else in this film is a plan", but my two tests and
  PR #21 already exist. It now says the tool itself is still a plan.
- **Screenshots redrawn:** my real screenshots are too small to read on screen and would fail the
  toolkit's text-size check, so B07A and B07B redraw them simply and say "redrawn from my
  screenshot" with the date. The screenshots are in `evidence/alternatives/`.
- **Outro:** the toolkit's `ClaudeTitleOutro` card hard-codes the instructor's handle, which this
  film may not show. BOUT is a drawn Manim scene with the title and my name. The beat sheet
  records that title and name in `shot.remotion.props` so `bookend_check.py` can verify them; no
  Remotion outro is rendered.
- **Pronunciation:** a speech-to-text pass (faster-whisper `base.en`) matched the narration; it
  only spelled my name "Varnica".
- **Layout fixes before rendering:** a strike-through crossed the "Required?" label (B03), and a
  page touched its caption (B07A). Both changed before the full render.
- **What I understand now:** The checks caught problems I didn't notice by watching.

### 2026-10-11 — Gates that failed, and what I did

- **Gate V failed** on B08 (contrast 0.25 < 0.30). Darker kraft and dark bases fixed it.
- **Gate T failed** on B02: the near-black tool block inside the box read as text. Made it grey.
- **Clips longer than audio:** B08 and B13 ran 0.06 s and 0.21 s past their narration, which the
  compiler trims silently from both ends. The shared `finish()` forced a minimum wait; fixed it
  and re-rendered all 16 scenes so the film matches `scenes.py`.
- **B13 ended mid-animation:** its last cue was the last words. Moved it earlier.
- **Gate W gap:** it reported 11 of 16 scenes, skipping B07A, B07B, B12A, B12B and BOUT. I did not
  change the toolkit; those five were checked by eye and passed every other gate.
- Final: every gate clean; 3:02. Reports in `gate-reports/`.

### 2026-10-14 — Checking the film against the assignment, and fixing three gaps

- **Target role was missing from the film.** B08 named my reader but not my role. It now opens:
  "The role I'm aiming for is AI software developer". Re-voiced B08 only (3:02 → 3:05).
- **"Constructed" labels:** the assignment says sketches must be labelled constructed on screen.
  Seven drawn beats of the planned tool (B01, B02, B05, B06, B08, B09, B10) and the planned answer
  card in B07B now say "planned · constructed".
- **Brief was too long** (about 1,200 words for a one-page brief). Rewrote it to one page; the
  "exists today" list now includes my two trials of the alternatives.
- Re-rendered the eight changed scenes and re-ran every gate.
- **Frame review after the re-render:** in B01 the "docs" label touched the new tag. No gate caught
  it; moved "docs" above the page and re-rendered B01.
- **Gate W gap resolved:** Gate W only matches class names like `B07_…`, so it skipped B07A, B07B,
  B12A, B12B and BOUT. Ran it on a scratch copy with only those names changed: all five clean.
  The toolkit was not edited.
- Final: 3:05; every gate clean on all 16 scenes.
