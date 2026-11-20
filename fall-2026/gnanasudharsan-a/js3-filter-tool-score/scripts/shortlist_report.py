"""Write shortlist/SHORTLIST.md from my claim labels (shortlist/claim_labels.csv). All numbers computed here."""
import csv, json
from collections import Counter, defaultdict
from pathlib import Path
r = list(csv.DictReader(open("shortlist/claim_labels.csv")))
by = defaultdict(list)
for x in r: by[(x["board"], x["id"], x["title"])].append(x)
audit = {}
s1 = {x["n"]: x for x in json.load(open("audit/sample_v1.json"))}
for h in csv.DictReader(open("audit/hand_verdicts_v1.csv")):
    audit[s1[int(h["n"])]["id"]] = h["my_verdict"]
MUST = ("role", "level", "location")
def verdict(cl):
    lab = {c["claim"].split(":")[0]: c["my_label"] for c in cl}
    if "CONTRADICTED" in lab.values(): return "NOT RELEVANT"
    if any(lab.get(m) == "INSUFFICIENT" for m in MUST): return "I CANNOT TELL"
    return "RELEVANT"
mine = Counter(x["my_label"] for x in r); changed = [x for x in r if x["my_label"] != x["proposed"]]
cx = [x for x in r if x.get("codex_label")]; agree = sum(x["my_label"] == x["codex_label"] for x in cx)
ent = [k for k, cl in by.items() if any(c["claim"].startswith("role") and c["my_label"] != "SUPPORTED" for c in cl)]
verd = {k: verdict(cl) for k, cl in by.items()}
counter = [k for k in by if verd[k] == "I CANNOT TELL" and audit.get(k[1]) == "RELEVANT"]
L = [f"# SHORTLIST.md — source-grounded shortlist (filter v1.1 keeps, run 20261119T162945Z)",
     f"{len(by)} postings x 5 claims = {len(r)} claims. Labels are mine (shortlist/claim_labels.csv); the script's proposals and Codex's suggestions are kept beside them.",
     f"\n## Summary\n- My labels: SUPPORTED {mine['SUPPORTED']}, CONTRADICTED {mine['CONTRADICTED']}, INSUFFICIENT {mine['INSUFFICIENT']}.",
     f"- I changed {len(changed)} of {len(r)} proposed labels.",
     f"- Codex (OpenAI) suggested labels for {len(cx)} claims; I agreed with {agree} and disagreed with {len(cx) - agree} (the second pass ran through Codex's modified reviewer, so I do not claim Codex's labels were hidden or that the 44 were re-reviewed one by one; see FRICTIONAL.md).",
     f"- Verdicts under the abstention rule: " + ", ".join(f"{v} {n}" for v, n in Counter(verd.values()).items()) + ".",
     "\n## Relevance is not entailment",
     "The filter kept these postings because their words matched (a role phrase in the title, topic words, skills). For each, I labeled the role claim "
     "\"hands-on ML/AI engineering\" as not supported by the posting's own text: the match made it relevant, but the text does not entail the claim."]
for k in ent:
    c = next(c for c in by[k] if c["claim"].startswith("role"))
    L.append(f"- **{k[2]}** — proposed {c['proposed']}, mine **{c['my_label']}**. Span: \"{c['span'][:220]}\". My note: {c['my_note'] or '-'}")
L += ["\n## Abstention rule",
      "From FILTER.md §2: the agent says **\"I cannot tell\"** instead of RELEVANT when a must-have claim (role, level, location) is INSUFFICIENT. "
      "A CONTRADICTED claim gives NOT RELEVANT. Only when role, level and location are all supported is a posting called RELEVANT.",
      "\n## A counterexample that exposes the rule's limits"]
if counter:
    for k in counter:
        L.append(f"- **{k[2]}**: the rule abstains (\"I cannot tell\") because the level claim is INSUFFICIENT — every Anthropic posting defers the level to an internal job level. "
                 "But in my blind audit I judged this posting **RELEVANT**. The rule can only use what the text states; I used the description of the work as a whole. "
                 "So the rule is safe (it never calls a posting relevant without evidence) but it is too strict for a source that never states a level: on this board it can never say RELEVANT.")
else:
    L.append("- (none found automatically; see my note)")
L.append("\n## Every claim")
for k, cl in by.items():
    L.append(f"\n### {k[2]} ({k[0]} {k[1]}) — verdict: **{verd[k]}**\n| claim | proposed | mine | Codex | span | my note |\n|---|---|---|---|---|---|")
    for c in cl:
        L.append(f"| {c['claim']} | {c['proposed']} | **{c['my_label']}** | {c.get('codex_label') or '-'} | {c['span'][:140].replace('|','/')} | {c['my_note'][:80].replace('|','/')} |")
Path("shortlist/SHORTLIST.md").write_text("\n".join(L) + "\n"); print("\n".join(L[:20]))
