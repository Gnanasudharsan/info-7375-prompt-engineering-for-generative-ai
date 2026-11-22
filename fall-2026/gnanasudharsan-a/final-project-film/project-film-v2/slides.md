---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section { font-family: "EB Garamond", Georgia, serif; font-size: 34px; padding: 70px; }
  h1 { font-size: 64px; }
  h2 { font-size: 48px; }
  .small { font-size: 22px; color: #666; }
  .tag { font-size: 20px; letter-spacing: 2px; color: #b00; }
  code, pre { font-size: 22px; }
---

<!-- _paginate: false -->
<!-- S01 · L01 -->

# DecisionTrace Lite

Gnanasudharsan Ashokumar · INFO 7375 · Fall 2026

---

<!-- S02 · L02 -->

## Why did we decide this?

Who approved it?
Is it still true?

---

<!-- S03 · L03 -->

## Meeting notes · emails · tickets

Scattered. Some out of date.

---

<!-- S04 · L04 -->

## Question → answer + status + source

Every claim points to the exact passage.

---

<!-- S05 · L05 -->

## "Not in the sources."

No guessing.

---

<!-- S06 · L06 -->

## A wrong answer looks like a right one

An answer you can check in seconds is one you can rely on.

---

<!-- S07 · L07 -->

## Published score

How often it's right, measured and public.

---

<!-- _class: lead -->
<!-- S08 · L08 -->

# What already exists

---

<!-- S09 · L09 -->

## Tools

NotebookLM · ChatGPT

Answers over documents you upload

---

<!-- S10 · L11 -->

## Research

- **RAG**: Lewis et al., 2020
- **ALCE**: do citations support the sentence? (Gao et al., 2023)
- **RAGAS**: faithfulness to sources (Es et al., 2023)

---

<!-- S12 · L13 -->

## My test, 9 October 2026

6 synthetic documents · 4 questions · 2 tools

Database switch: **approved, not finished**

<span class="tag">SYNTHETIC TEST DATA</span>

---

<!-- S13 · L16–L17 -->

## The gap

| | Existing tools | DecisionTrace Lite |
|---|---|---|
| Find facts | ✓ | ✓ |
| Report decision status | sometimes | always |
| Check every citation | — | ✓ |
| Publish its score | — | ✓ |

<span class="small">"—" means not seen in my 6-document test, not a claim about every product.</span>

---

<!-- _class: lead -->
<!-- S14 · L18 -->

# The plan

---

<!-- S15 · L19 -->

## Large system → Lite

Neo4j · LangGraph · FastAPI · hallucination detection
↓
**Python + Claude: question in, grounded answer out**

---

<!-- S16 · L20 -->

## 1 · Data

6 → ~50 synthetic documents

reversed · unfinished · contradictory · unanswerable

<span class="tag">SYNTHETIC · FICTIONAL COMPANY</span>

---

<!-- S17 · L21 -->

## 2 · Test set

~50 questions, written by hand

answer · status · supporting passages

---

<!-- S18 · L22 -->

## 3 · Retrieval

BM25 · Python standard library

---

<!-- S19 · L23 -->

## 4 · Answer contract

```json
{
  "answer": "...",
  "status": "in_progress",
  "claims": [
    {"text": "...", "doc_id": "TRK-140", "quote": "..."}
  ]
}
```

---

<!-- S20 · L24 -->

## 5 · Verify

quote found? → supported? → ✓ answer

✗ → retry once → ✗ → **"Not supported by the sources."**

---

<!-- S21 · L25 -->

## 6 · Evaluate and report

harness · scores · failure analysis

---

<!-- S22 · L26 -->

## Resources

| | |
|---|---|
| Model | Claude via my NEU Claude Code seat, non-interactive mode |
| Scripted use | **pending** confirmation from professor / NEU IT |
| If not allowed | request API credits |
| Compute | MacBook Pro M4, no GPU |
| Accounts | GitHub |

Every response cached to disk.

---

<!-- _class: lead -->
<!-- S23 · L27 -->

# Did it work?

---

<!-- S24 · L28–L31 -->

## Five measures

| Measure | Target |
|---|---|
| Citation validity | 100% |
| Citation support | ≥ 90% |
| Status accuracy | ≥ 85% |
| Refuses unanswerable | ≥ 90% |
| Refuses answerable | ≤ 10% |

---

<!-- S25 · L32 -->

## Full tool vs. verification off

Same questions · same retrieval

---

<!-- S26 · L33 -->

## Worked / didn't

**Worked:** targets met; verifier improves support and status; costs ≤ 5 points of correctness

**Didn't:** verifier only adds refusals, or the judge disagrees with me too often

---

<!-- S27 · L34 -->

## First check

"Which database does the tracking service use?"

→ **in progress**, as of **2026-06-09**, citing **TRK-140**

---

<!-- _paginate: false -->
<!-- S28 · L35 -->

# DecisionTrace Lite

Gnanasudharsan Ashokumar
