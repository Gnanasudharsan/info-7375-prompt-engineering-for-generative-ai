# FACTCHECK — the-names-nothing-checks

Status: **signed off by Weiting Wang, 2026-10-13.** Every row below was resolved before the
first render. Two claims were changed and one was cut; those rows say so.

The film describes a project that does not exist yet. Most of its sentences are therefore
statements of intent, not assertions about the world, and are marked EXEMPT with the reason.
The rows that do assert something about Unity, or about the author's past work, are checked.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | BDEFS | "A shader property: a name stored in a Unity asset, not in the code." | PASS | Unity manual, *Access material properties in a script* (Unity 6000.0), read 2026-10-13 — material properties belong to the shader asset and are reached from script by name. | — |
| 2 | B01 | "Code can only reach those names as text. A string. Material dot set float, open quote, glow active, close quote." | PASS | Same Unity manual page; `Material.SetFloat(string, float)` takes the property name as a string. The specific call `material.SetFloat("_GlowActive", 1f)` is from the author's own project, *Escape from the Depths*. | — |
| 3 | B02 | "Get that word wrong and nothing stops you. The compiler lets it through. The console stays quiet. The game runs. The glow simply never happens." | CORRECTED | Unity manual, same page: these methods "only set properties that are available for the current Shader object on the material … calling SetTexture will have no effect." No console message is documented for this case. | **The earlier cut made this claim about a wrong *animator parameter*. That was wrong — see row 4 — and the beat was rewritten to the shader property, which is the case the documentation supports.** |
| 4 | B02B | "Unity does warn you about a wrong animator parameter, once that line runs. It says nothing at all about a wrong shader property." | PASS | Unity Discussions, *Parameter 'Jump' does not exist*, read 2026-10-13, quoting the runtime message `Parameter 'Jump' does not exist UnityEngine.Animator:SetBool (string,bool)`. The second half is row 3's source. | This beat was **added** so the film states the limit of its own claim instead of implying every wrong string is silent. |
| 5 | B02B | *(cut)* "It says nothing about a wrong tag, or a wrong object name." | CORRECTED | Not checked. Unity raises an exception for an undefined tag, so the claim was not safe to make. | Cut from the narration before the first render rather than hedged. |
| 6 | B03 | "An assistant that only reads your C sharp files cannot know the name inside the shader graph." | EXEMPT | True by construction: the sentence is about an assistant defined as reading only the C# files. It asserts nothing about any shipping product. | Reworded from "An assistant reads your C sharp files. It does not read the shader graph," which asserted untested behaviour of unnamed tools. |
| 7 | B04 | "Last spring I tried a tool that puts a model inside the Unity editor. I asked it to lay out a scene. It put things in the wrong places. … After that I built my scenes by hand." | PASS | The author's own first-hand experience with CoplayDev/unity-mcp connected to Cursor while building *Escape from the Depths* (CSYE 7270, spring 2026), recorded in her project notes at the time. | Scoped deliberately: the film makes no claim about that tool's current behaviour, its other features, or whether it reads shader or animator assets. |
| 8 | B05, B05B, B06, B07, B07B | Everything the proposed tool "will" do: build a checklist from the assets, check each string against it, mark what it cannot find, never write to the project, read only strings written out in full, publish both numbers. | EXEMPT | Statements of intent about work that has not been done. Each of these beats carries the word "proposed" on screen. | — |
| 9 | B06 | "A test project with three wrong names planted in it." | EXEMPT | Describes a fixture that does not exist yet; the "3" on screen is the planned count, inside a beat labelled "proposed". | — |
| 10 | B08 | "I shipped a Unity dungeon game last spring, and its glowing sword runs on exactly this kind of string." | PASS | *Escape from the Depths*, CSYE 7270, spring 2026. The sword glow is driven by `swordRenderer.material.SetFloat("_GlowActive", 1f)` against a Shader Graph property. The author can show the project. | — |
| 11 | B08B | "Building an evaluation set and reporting real numbers, I have never done." | PASS | The author's own statement about her own experience, 2026-10-13. | — |
| 12 | BIDEA, BHTF, BOUT | Greeting, the viewer's prompt, the closing title. | EXEMPT | No checkable claim. | — |
| 13 | whole film | No metric, result, user, employer, customer or testimonial is stated anywhere. | PASS | Read back against the full narration in `beat_sheet.json` on 2026-10-13. The two bar charts in B07 and B07B carry no numbers and are labelled "proposed"; no quantity in the film describes anything measured. | — |

## What this film does not claim

It does not claim the tool exists, that anyone has used it, that it catches any particular
share of errors, or that any named product fails at this. It does not claim Unity is silent
about every wrong string — row 4 exists because it is not.
