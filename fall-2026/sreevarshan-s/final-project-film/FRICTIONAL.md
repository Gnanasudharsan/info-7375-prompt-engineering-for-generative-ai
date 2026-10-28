# FRICTIONAL: Sreevarshan Sathiyamurthy, Final Project Film

## Oct 10, ~10 PM: Kept the Reallocation topic
I thought about switching topics. I kept Reallocation (Assignment 2) because the work already exists and the assignment lists a Reallocation recipe as an allowed project. It also means I can show real things in past tense: the AMGEN 404, the tests, the hand-checked numbers. I renamed the pitch "Record Beats AI" so it's clearer what it does.

## Oct 10, night: git pull blocked
I tried `git pull` in my old Brut folder to get the show-tell skill. It was blocked by a local .gitignore edit (I had added .venv/), and the folder was 47 commits behind. The remote also moved files out of `brutalist.art/` to the repo root, so merging could have put files in the wrong place. I made a fresh clone called BrutFilm instead, so my Assignment 1 folder stays untouched.

## Oct 10, night: Doctor and smoke failed
In BrutFilm, setup installed fine, but `./art doctor` was blocked by the ElevenLabs guard, which flagged files that ship with the toolkit itself. `./art smoke` failed because its own test uses the slug `_smoke`, which the slug validator rejects. Both are toolkit bugs, not my machine. Claude Code ran the same smoke steps on a copy with the slug changed, and a real 14-second video rendered, so the pipeline works. I didn't edit the toolkit to fix them.

## Oct 10–11: Voice choice
The default narrator is Liam, "in for Bear," with an @NikBearBrown outro, and the assignment says not to use the instructor's persona. I first picked recording my own voice, then switched to a synthetic voice to save time. Kokoro had 54 voices, so I chose am_michael and avoided am_liam (the name) and am_onyx (the toolkit's Liam voice). The film says on screen and at the end that the voice is synthetic.

## Oct 11, morning: Brief checked against the repo
Before writing the beat sheet, Claude Code checked every "exists today" line in my brief against the repo. Two were wrong. The test count is now 58, not 51, and commit 0c6c941 was renamed 6202dc8 by a history rewrite. CI was never red; it never ran, because all six runs are waiting for maintainer approval. I fixed the brief, and the film doesn't mention CI.

## Oct 11, 9:26–9:30 AM: Alternative screenshots
I opened Ellis and F1Jobs for Amgen and took five screenshots, including Ellis's job titles and filing history and the F1Jobs line saying its counts are not job openings. Ellis showed 416 LCAs for 2025, while F1Jobs showed 374 petitions for FY2025. They count different filings, so the numbers don't match. That's a small example of why my project labels where every number comes from. I later lost the first two screenshots and got them back from my upload.

## Oct 11, 9:47 AM: Hand check re-run
The exact hand-check command wasn't saved anywhere in my Assignment 2 repo; WORKED-RUN.md only describes it. I re-ran the same one-liner in my own Terminal and got AMGEN 1882.0 and HUMAN 1382.0. My first screenshot cut off the date, so I ran `date` again and retook it. I kept the Assignment 2 chat transcript out because the rules forbid private transcripts. The film draws the two numbers instead of showing my Terminal.

## Oct 11: Length cuts
The first audio ran 4:27, over the 4-minute cap. To fit, Claude Code cut lines, including graded ones: "why this project," "new to me," and how you'd know the first piece ran. I made it put those back and sped the voice to 1.09 instead (1.07 was still over). The final film is 3:57.

## Oct 11: Name pronunciation
The voice said my name as "S. Revarshan Satyamrthy." Claude Code first said it couldn't fix it without editing the toolkit, but changing only the narration text isn't a toolkit edit. It tried about 20 spellings with whisper, and "Shreevarshun Saa-thee-ya-moorthy" worked in both the opening and the outro. The on-screen name keeps the real spelling.

## Oct 11: Honest closing line
The outro first said "the script is mine," but Claude drafted the script and I reviewed it. I changed it to "I drafted the script with Claude and checked every claim" so it matches SOURCES.md.

## Oct 11: No render-integrity gate
The assignment asks for a render-integrity check, but the toolkit has no gate by that name. I ran every gate it does have: A, W, B, V, T, master, loudness, sharpness, frames, bookends, fact check, content, and lanes. Gate B and Gate T failed a few times on text size and layout, and Claude Code fixed each and re-rendered until they passed.

## Oct 11: 4K deliverable and B10 label
The master check only accepts 4K, so the 1080p file failed it. The 4K file is only 12.4 MB, so I made it the deliverable, and every film-level gate passes. When I checked frames, B10 listed what's out as "auto-apply, logins, CONSTRUCTED," which looked like constructed data was out. I changed it to "personal data." I also confirmed the final file has no debug labels; those were only in the review cut.

## Oct 11, afternoon: Final check against the assignment
Before pushing, I checked everything against the assignment line by line. Two gaps were in the film itself. It said "sponsor lookup sites" but never named Ellis or F1Jobs, and it never said my target role. I added both to the narration and put "Ellis" and "F1Jobs" on screen in B02. That pushed the film to 4:01, so I cut one framing question in B18 ("Why build the evaluation log first?") and kept the voice speed the same so my name still sounds right. B03 then failed Gate T and Gate B on text size and position, and it took two fixes to pass both. I also cut the brief down to one page and added my stack, and Claude Code read the real licence files and added them to SOURCES.md. Where no licence file existed, it says so instead of guessing. Final runtime is 3:58.6.
