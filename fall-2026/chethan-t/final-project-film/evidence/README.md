# evidence — oasdiff run on a planted rename (2026-10-25)

I ran this myself, in my own terminal, on 2026-10-25.

- **Fork:** github.com/chethangowda-git/fork-realworld (fork of gothinkster/realworld)
- **Planted rename:** `Profile.username` → `handle`, two lines in `specs/api/openapi.yml`, commit [85c2a15](https://github.com/chethangowda-git/fork-realworld/commit/85c2a15ddf56ee41c224e7073776c97e7ad0cd2e) on branch `rename-username-to-handle`
- **Tool:** oasdiff 1.34.1 (Homebrew)
- **Command:** `oasdiff breaking /tmp/openapi-original.yml specs/api/openapi.yml`

| File | What it is |
|---|---|
| `openapi-original.yml` | the spec before the rename (fork parent commit `ebbcdeb`) |
| `openapi-renamed.yml` | the spec after the rename (commit `85c2a15`) |
| `oasdiff-2026-10-25.txt` | oasdiff's output |

**Result:** 12 breaking changes, all `response-required-property-removed`, across 12 endpoints (Profile is reused as the article and comment `author`). oasdiff reports `username` as removed, not renamed, and names API paths and response fields only. It names no frontend files or lines.

Claude copied the two spec files from the public commits and saved the output text I pasted into the session.
