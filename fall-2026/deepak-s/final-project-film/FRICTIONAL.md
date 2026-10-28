# FRICTIONAL

## 2026-10-14

- 2026-10-14 16:02 Piping the setup script into bash caused an issue because `BASH_SOURCE` was unbound in that execution context. I switched to using a patch file and running the setup script directly instead of piping it. This avoids the piping-related issue and makes the execution more reliable.
- 2026-10-14 16:10 The pkgconf prerequisite needed attention during setup, so I checked the dependency and its installation requirements rather than assuming it was available. I also found that the committed package-lock.json was out of sync with package.json even though the package versions had not changed, so I chose to restore the original lockfile instead of introducing unnecessary dependency changes.
- 2026-10-14 19:07 I initially had a constructed example for B07, but using the actual Claude reply made the narration more grounded. The reply fit the point I wanted to make, although its tone shifted the interpretation slightly, so I needed to check that the narration represented it fairly.
- 2026-10-14 19:07 During fact-checking, I found that the sources didn't support two claims as strongly as the script suggested: Netflix flagging files and cut detectors being fooled by flashes. I revised the wording to match what the sources actually supported instead of keeping the stronger claims.
- 2026-10-14 19:07 I had to settle how quotation marks should be counted in the character limit. Treating the quote marks as delimiters gave me 37 characters rather than 39, which changed how I evaluated the branch choice.
- 2026-10-14 19:07 I wanted to use PR #25 as public evidence of my work, but I also needed to be transparent about Claude Code's contribution. I updated the wording to disclose the co-authorship rather than presenting the work as entirely unaided.
- 2026-10-14 19:07 I had to account for the toolkit code used by the scenes without casually copying it into the project. The approach was to assemble the relevant kit code at build time and note that the toolkit has no stated licence.
- 2026-10-14 19:07 Getting the project brief onto one page took several rounds of trimming. I had to shorten explanations without removing important evidence, caveats, or details needed to keep the brief consistent with the film.
