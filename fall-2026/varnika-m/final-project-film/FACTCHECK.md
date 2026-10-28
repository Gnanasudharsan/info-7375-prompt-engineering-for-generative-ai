# Fact check — Terraform Docs, Quoted

Status: claims checked 2026-10-11 by Claude Code against the files in `evidence/`; Varnika
supplied claims 5–10 and 12 from her own trials and experience. Varnika's sign-off: pending
her review of the cut.

Every factual claim in the narration or on screen. Plans ("will") are not facts; they are
listed only where a drawing could be mistaken for something that exists.

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | B03 | On the AWS provider's `aws_s3_bucket` page, `bucket` is Optional, and if omitted Terraform assigns a random, unique name | PASS | `evidence/aws-provider-docs/s3_bucket.html.markdown:54` (v6.68.0) | — |
| 2 | B03, B04, B11 | On-screen tags "AWS provider v6.68.0 docs · line 54 / line 70 / lines 54 and 221" | PASS | Same file; line numbers checked with `grep -n` | — |
| 3 | B04 | On the same page, `versioning` is marked Deprecated, with a separate resource to use instead | PASS | Same file, line 70 (`aws_s3_bucket_versioning`) | — |
| 4 | B04 | "Facts like these change between versions" | PASS | Line 50: "arguments marked Deprecated will be removed in a future major version" | Kept general; no count or date of change is claimed |
| 5 | B07A | I tried the Terraform docs site on October eleventh; the page menu gets you to the answer | PASS | `evidence/alternatives/2026-10-11_registry_menu-argument-reference.png` | — |
| 6 | B07A | Searching the page for bucket found two hundred and twenty matches; the right one was number seventy (on screen: "70 / 220") | PASS | `evidence/alternatives/2026-10-11_registry_cmdf-bucket-70-of-220.png` (Chrome find count, includes the side menu) | — |
| 7 | B07B | Claude said optional, which is right | PASS | `evidence/alternatives/2026-10-11_claude-ai_sonnet-5-5_answer_cropped.png`; docs line 54 | — |
| 8 | B07B | It added two details that aren't on the docs page | PASS | `evidence/alternatives/README.md`: the `terraform-` + timestamp naming and the 3-character minimum are not on the saved page | Said "not on the docs page", never "wrong" |
| 9 | B07B | It didn't say which docs it used | PASS | Same screenshot: no link, line or version in the visible reply | — |
| 10 | B07B | On-screen "claude.ai, Sonnet 5.5 · 2026-10-11" | PASS | Same screenshot (model label at the bottom of the window) | — |
| 11 | B11 | `bucket` is Required inside the replication `destination` block on the same page | PASS | Same docs file, line 221, under `#### destination Block` (line 213) | — |
| 12 | B12A | I've used Python and Terraform on my co-op, and Terraform in a cloud computing course project | EXEMPT | Self-report by Varnika, 2026-10-11; not public, no employer named | Nothing from that work is shown |
| 13 | B12A | My Reallocation Engine tool has twenty-two offline tests, and I wrote down where it fell short | PASS | PR #21, `nikbearbrown/the-reallocation-engine` (open, head `8b79712`, checked 2026-10-11); its `SUBMISSION.md` lists 22 tests and known limitations | Not called "merged" |
| 14 | B12A | Built "with Claude Code" | PASS | That submission's own disclosure: most code written by Claude Code at Varnika's direction | — |
| 15 | B13 | A licence check exists | PASS | `evidence/licence-check.txt`, run 2026-10-11T18:45:46Z | — |
| 16 | B13 | One saved docs page pinned to version six point sixty-eight | PASS | `evidence/README.md`: byte-identical to tag `v6.68.0`, sha256 `5d5653c0…` | — |
| 17 | B13 | My two tests from October eleventh | PASS | `evidence/alternatives/` (registry and claude.ai screenshots) | — |
| 18 | B13 | The tool itself is still a plan | PASS | No tool code exists as of 2026-10-11 | Re-check before submitting |
| 20 | B08 | The role I'm aiming for is AI software developer | EXEMPT | Varnika's stated target role, 2026-10-11 (also in PROJECT-BRIEF.md question 3) | — |
| 19 | B01, B02, B05, B06, B08, B09, B10, B12B | Drawings of the planned tool, repo, steps, tests and evaluation | EXEMPT | Planned; B01, B02, B05, B06, B08, B09 and B10 carry an on-screen "planned · constructed" label, and so does the planned answer card in B07B | — |
