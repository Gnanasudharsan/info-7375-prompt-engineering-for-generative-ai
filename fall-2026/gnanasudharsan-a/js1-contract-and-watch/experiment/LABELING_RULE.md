# Labeling rule — written 2026-10-28, before labeling any posting
Author: Gnanasudharsan Ashokumar

A posting is RELEVANT for Ananya Rao (new-grad ML/NLP engineer, Boston, open to remote and US relocation, needs visa sponsorship) if:

1. **Role type:** Hands-on engineering roles focused on machine learning, NLP, or AI systems (such as ML Engineer, AI Engineer, Applied NLP Engineer, or Research Engineer). For Research Engineer roles, I will evaluate the posting's "Responsibilities" section: if more than half of the listed bullets are about building, training, evaluating, or deploying systems, it counts as engineering and is RELEVANT; if bullets are mostly about publishing papers or conducting novel academic research, it is NOT_RELEVANT. Pure data science or general software engineering roles without ML focus are excluded.
2. **Level:** Realistic for a new grad finishing Ananya's MS in Computer Science (AI concentration) at Boston University (in progress, ending 2026-12) and her recent Machine Learning Engineer Co-op at Lumenwise Health. Postings requiring 0 to 2 years of experience are acceptable; any explicit requirement for 3+ years, mid/senior level, or a PhD makes it NOT_RELEVANT. If no years are stated, I judge based on the other criteria.
3. **Skills fit:** "Required" items mean those listed under "You may be a good fit if you have", while "nice-to-have" items mean those under "Strong candidates may also have." To be RELEVANT, the posting must require at least 2 required items that match her exact shipped list of 9 skills (`Python`, `PyTorch`, `SQL`, `Hugging Face Transformers`, `sentence-transformers`, `FastAPI`, `MLflow`, `PostgreSQL`, `AWS`). Only explicitly named technologies count (e.g., general phrases like "experience with ML frameworks" do not count as PyTorch). 
   - *Tie-breaker:* If the required section names fewer than 2 specific technologies of any kind, I skip the skills test and judge on role, level, location, and sponsorship. If it names 2 or more technologies but fewer than 2 are in her shipped list, it is NOT_RELEVANT.
   - If a posting requires un-shipped skills like Kubernetes or Ray as mandatory prerequisites rather than optional items, it is NOT_RELEVANT.
4. **Location:** Based anywhere in the United States or explicitly designated as Remote / Remote-Friendly, aligning with her US relocation willingness.
5. **Sponsorship:** Must offer visa sponsorship or at least not explicitly disclaim it (rejecting phrases like "not currently able to sponsor").

**Otherwise NOT_RELEVANT.**

**Unclear cases:** If years of experience are stated, I apply the strict 0–2 vs 3+ cutoff. If a PhD is required, it is automatically NOT_RELEVANT. If requirements or technologies are completely unstated or ambiguous, I skip the unclear constraint and judge entirely on role type, level, location, and sponsorship fit.

**How this differs from the mechanical rule in CONTRACT.md, and why:** 
The mechanical rule in `CONTRACT.md` only filters by negative title exclusions, remote/US location strings, negative sponsorship boilerplate, and a minimum shipped-skill count. This human labeling rule goes further by reading semantic experience thresholds (rejecting roles asking for 3+ years or a PhD), evaluating explicit responsibilities for Research Engineer roles, and applying precise required vs. nice-to-have distinctions with tool-light tie-breakers—allowing the Claude judge to apply qualitative reasoning beyond simple keyword matching.