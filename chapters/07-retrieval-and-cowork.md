# Chapter 7 — Retrieval and Cowork
*The nearest passage may still fail to answer the question.*

Suppose a corpus contains a document saying “Office hours by appointment.” The query is “office hours.” Our small retriever ranks that document highly. The result feels satisfying because the shared words are visible. Now change the query to “tuition refund” and put the phrase “fee reimbursement” in the only relevant document. A human reader can see the relationship. The retriever returns nothing because its representation sees no shared token.

Both are constructed cases from the course's offline exercise. The research run records a cosine similarity of `2 / sqrt(6)`, approximately `0.8164965809`, between “office hours” and “office hours appointment.” It also records no result for the synonym pair and deterministic ordering for tied scores. These are results of the displayed count-vector implementation, not measurements of Claude Cowork, neural embeddings, or human semantic understanding.

In the first case every step worked, and a human still has to ask whether “by appointment” says when to show up. In the second, a step quietly dropped the only source that mattered, and nothing in the output says so. Put Claude downstream of either one. It will write a fluent answer from whatever reached it, and nothing it received says what was left out. The sentence reads the same whether the evidence was complete or not.

Chapter 1 named three jobs that stay with you: conduct, check, drive. Retrieval is where they bite hardest, because it makes the most decisions and leaves the fewest traces. Ranking passages by similarity is pattern and association, the work *Irreducibly Human* places in its first tier, where the machine wins in bounded, well-specified settings, and a ten-line scoring function does it faster than you will. What stays with you is the specification (what counts as similar, what is eligible, how many results) and the audit (what the ranking left out, and whether the winning passage says what the answer claims). Conduct: you decide what reaches Claude's context before the task runs. Check: relevance is not entailment, and ranking turns scores into omissions. Drive: Claude ranks and quotes; what a source means in the world is your reading.

This chapter takes apart the selection process before any generated answer appears. We will tokenize text, count terms, calculate a dot product and vector lengths, normalize the overlap, sort candidates, and select at most k results. Each step is a design decision with a cost. The system is small enough to hand-calculate one score, and you will build all of it by hand for the reason Chapter 1 gave: you cannot audit a ranking you have never computed. Then you will write the gate for a retrieval task, conduct Claude Code against it, and build a bounded task packet for Claude Cowork.

Chapter 6 reviewed a proposed code change against its diff and tests. Here we move earlier in the pipeline. Which source material reached the system that proposed the change or report? A plausible response can be generated from an incomplete selection, and a clean review packet cannot recover a passage that was never in the corpus or was ranked out of the selected context. Debugging generation alone will not repair a missing source. We need a source inventory and retrieval record alongside the resulting prose.

Claude Code remains the assumed course assistant. The Python retriever runs offline with the standard library and spends no direct API credits. A later Claude Cowork task can use the selected passages, but this chapter does not claim to reproduce Cowork internals. If you perform an actual interface task, preserve its sources, prompt, output, and date. If you do not, keep the task packet labeled as proposed rather than inventing a live run.

## What you will be able to do

You should be able to turn short text into a token-count vector, calculate cosine similarity by hand, predict ranking changes, and explain deterministic tie-breaking. You should also be able to distinguish no overlap from absence in the corpus, identify a claim unsupported by selected passages, and design a cautious abstention rule with a counterexample that exposes its limits.

Beyond that, three abilities the rest of the book builds on. Write the gate for a retrieval task before anything runs: the retriever's contract, the list of sources you expect the task to need, and the rules the evidence table will apply. Conduct Claude Code against that gate, run your own tests on what it returns, and read the passages yourself instead of accepting the report's last sentence. And write a sign-off that says which claims were checked against which passages, what was not checked, and whether you sign or withhold, plus which parts of this work you handed to Claude, which you kept, and why.

The prerequisites are Chapters 2 and 6, Python dictionaries and counters, square roots, and basic vector arithmetic. Every symbol used below is introduced from the actual program. The paired [lesson](../lessons/07-context-retrieval-and-cowork/docs/en.md) provides the runnable sequence and existing knowledge check. Build your first version in your learner workspace before consulting the reference.

## What reaches Claude is the end of a chain of omissions

Look at the whole path from a stack of documents to a sentence in a report. When Claude answers from your sources, the answer was shaped by seven narrowing stages. You made, delegated, or never noticed each one.

| Stage | What it decides | Who decides it here | What the final prose shows of it |
| --- | --- | --- | --- |
| Eligibility | Which sources may be used at all | You, by permission and scope | Nothing |
| Ingestion | Whether an eligible file became text in the corpus | The loading step, or you if you inspect it | Nothing |
| Representation | Which differences between texts can matter | The vectorizer you chose | Nothing |
| Scoring and cutoff | Which candidates rank, which score zero, which fall below k | The scoring rule and k | Nothing |
| Selection into context | What Claude is actually shown, after any further filter or manual choice | You, or the tool you used | Nothing |
| Use | Which shown passages the answer relies on | Claude, while generating | A citation, if you required one |
| Claim | What the report says it established | Whoever signs it | The verbs |

Read the last column. Five of seven stages leave nothing in the prose, and a citation asserts a relationship rather than showing it. Omission is silent at the layer where you read. A reviewer who starts by judging the answer starts where all seven decisions have already happened and none of them is visible.

*Computational Skepticism for AI* makes the same point about datasets in a sentence I keep returning to: you cannot compute the missingness of rows that never existed. A summary pass reads data as written. The chapter's central move is a question: why are there exactly N rows, and what was N supposed to be? Its illustration, a join that silently dropped records with differently formatted identifiers, is labeled a composite of familiar failures and not a single sourced incident. Ingestion is our join, and a score table is our histogram: precise about what arrived, silent about what did not.

*Irreducibly Human* states the boundary at its first tier carefully: the machine is better at the pattern task as specified, and the human's remaining job is to notice when the specification is wrong and when the task only looked like a pattern task. Finding a passage is a pattern task. Deciding whether it answers the question is not. Retrieval is specified by your query, representation, corpus, and k, and the ranking can be excellent while that specification is wrong.

The rest of the chapter takes those decisions in the order you face them. Representation, scoring, and cutoff come first, because you cannot audit what you do not understand. Then the gate fixes your decisions in writing before Claude implements anything.

## A representation decides what can match

The first decision is what counts as the same. Before any ranking, someone chooses which features of a text survive into the thing being compared, and everything the representation drops is invisible to every later stage. The [reference implementation](../lessons/07-context-retrieval-and-cowork/code/main.py) begins with a short vector function:

```python
import re
from collections import Counter

def vector(text):
    return Counter(re.findall(r"\b\w+\b", text.lower()))
```

First the text is lowercased. Then the regular expression extracts sequences of word characters bounded as words. Finally, `Counter` records how many times each extracted token occurs. “Office office hours” becomes a mapping in which office has count two and hours has count one.

Calling this mapping a vector means we can imagine one coordinate for every token in the combined vocabulary. Most coordinates are zero, so the implementation stores only tokens that appear. The representation keeps frequency and discards word order, so “hours office” and “office hours” receive the same vector. It also discards capitalization. Those choices make exact lexical overlap easy to calculate, but they prevent the vector from representing every distinction in the text. This is not a failure after retrieval. It is a consequence of the information the representation retains.

Tokenization is another decision, and it is easy to leave to a default. Run the regular expression in your head on “don't stop.” An apostrophe splits the contraction into don and t, a hyphen splits “fee-reimbursement” into fee and reimbursement, and an underscore splits nothing because it counts as a word character. The behavior of `\w` follows Python's regular-expression rules, not a universal linguistic analysis. This chapter uses short English fixtures whose tokenization can be inspected. Do not infer performance for multilingual, code-heavy, or adversarial corpora without testing their actual inputs.

The test `vector("Hi HI")["hi"] == 2` checks both lowercasing and counting for one case. It does not prove that capitalization is irrelevant to meaning. If a task depends on proper nouns, acronyms, or case-sensitive identifiers, that is a decision to revisit, and the person best placed to revisit it is the one who knows which differences matter for the task.

Representations optimize for some comparisons by making others impossible. Count vectors make shared words visible and the arithmetic transparent, and they sacrifice order and synonymy. The right question is not whether the representation is intelligent. It is whether its retained features are adequate for the evidence-selection task and whether its misses are visible to the workflow.

## Cosine from first principles

Claude can compute a cosine similarity instantly, and so can a library. You compute it once by hand for a different reason. A score is the number people quote and nobody rechecks, and the only way to know what it measures is to have produced it yourself.

Let q be the query count vector and d be a document count vector. Their dot product multiplies matching coordinates and sums those products:

```math
q \cdot d = \sum_t q_t d_t,
```

where t ranges over tokens, q_t is the query count for token t, and d_t is the document count. Tokens absent from one side contribute zero. The dot product increases with shared counted terms, but it also grows when vectors grow, so the implementation normalizes by their lengths.

The Euclidean length of q is:

```math
\lVert q \rVert = \sqrt{\sum_t q_t^2}.
```

Cosine similarity divides the dot product by both lengths:

```math
\operatorname{cosine}(q,d) = \frac{q \cdot d}{\lVert q \rVert\lVert d \rVert}.
```

The [Stanford information-retrieval text](https://nlp.stanford.edu/IR-book/html/htmledition/dot-products-1.html), consulted in the approved research packet, supports this normalized dot-product formulation. Our use remains a small lexical example. The source does not transform this implementation into a complete production retrieval system.

The code follows the equations directly:

```python
import math

def cosine(left, right):
    dot = sum(value * right.get(term, 0)
              for term, value in left.items())
    norm = math.sqrt(
        sum(v*v for v in left.values()) *
        sum(v*v for v in right.values())
    )
    return dot / norm if norm else 0.0
```

Iterating over the left vector is sufficient for the dot product because any token absent there would contribute zero, and the lookup supplies zero when the right side lacks it. The norm multiplies the two sums of squares before taking the square root, which is algebraically the same as multiplying the two lengths. If either vector has zero length, the function returns `0.0`. That is a design choice avoiding division by zero, not a claim that an empty query is a meaningful information request.

Now calculate the published example. The query “office hours” has counts office one and hours one, so its length is square root of two. The document “office hours appointment” has three tokens, each with count one, so its length is square root of three. The dot product is two because office and hours each contribute one.

Therefore:

```math
\frac{2}{\sqrt{2}\sqrt{3}} = \frac{2}{\sqrt{6}} \approx 0.8164965809.
```

The saved execution records the same decimal, and every intermediate term can be reconstructed. That does not prove the document answers every question involving office hours. It proves a lexical relationship under this representation.

<!-- [FIGURE: Cajal production brief. Cosine overlap measures relevance, not entailment. Include query vector, document vector, dot = 2, lengths √2, √3, cosine 2/√6. Show the confirmed relationship that semantic support remains a separate check. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![Cosine overlap measures relevance, not entailment. semantic support remains a separate check.](../images/07-context-retrieval-and-cowork-fig-01.png)
*Figure 7.1 — Cosine overlap measures relevance, not entailment*

Write the hand calculation in your learner workspace before you run anything. It is the first piece of your baseline. If any implementation, yours or Claude's, returns a different number for this pair, you already know which one to distrust.

## Ranking turns scores into omissions

Claude receives what `retrieve` returns and nothing else, so read the function as a policy about what to leave out. It scores every declared document, removes nonpositive scores, sorts the remainder, and takes at most k rows:

```python
def retrieve(query, documents, k=2):
    if type(k) is not int or k < 1:
        raise ValueError("k must be positive")
    query_vector = vector(query)
    scores = [(key, cosine(query_vector, vector(text)))
              for key, text in documents.items()]
    return sorted(
        (row for row in scores if row[1] > 0),
        key=lambda row: (-row[1], row[0]),
    )[:k]
```

The positive-integer check defines the accepted k values. A zero or negative k is rejected instead of silently returning nothing, and a Boolean is not accepted because the type check asks for exactly int. The function calculates every score before filtering, and zero-overlap documents disappear from the returned list.

Sorting uses two keys. The negative score puts higher similarities first. The document key breaks ties in ascending order, and the research fixture confirms deterministic behavior for equal scores. Relying on incidental mapping order would make equal-score selection harder to explain.

Top-k introduces an exclusion even among positive matches. With k one, only the first ranked candidate remains, and a second relevant document can be omitted because another score is larger or because the tie-break key comes later. The returned list is selected candidates under a particular scoring and cutoff rule, not all available evidence.

The filtering rule introduces another omission. A semantically related document with zero literal overlap is removed before top-k selection. “Tuition refund” and “fee reimbursement” have disjoint token sets under this vectorizer, so their dot product is zero and the result is excluded. Do not report zero score as proof of irrelevance. It means no counted token overlap under this representation. The relevant source might be absent from the corpus, present but phrased differently, or present with text the tokenizer represents poorly. Those are different failure locations and suggest different repairs. Conversely, a high score does not prove adequacy: a document can repeat query terms while discussing a different policy, time period, or population. Lexical similarity is a candidate-selection signal, and the next review must inspect the passage against the actual claim.

Notice what the function does not return: the documents it dropped, and why. A list of winners gives you the same view the final prose does, one stage earlier. To see an omission you have to compute it, which is why the gate below asks for an audit view listing every document with its score and its fate: selected, below the cutoff, or zero overlap.

## The synonym miss and a dangerous repair

When the retriever misses a paraphrase, the tempting repair is a synonym map, and the decision hiding inside it is who gets to say that two words mean the same thing. A learner might map tuition to fee and refund to reimbursement before vectorization. That can make the constructed document overlap with the rewritten query. It also changes the representation and creates new opportunities for false positives.

The word fee is not interchangeable with tuition in every sentence, and reimbursement may describe repayment for expenses unrelated to a refund policy. A global substitution can retrieve documents that share the mapped terms but answer a different question. Treat the repair as a hypothesis and evaluate it on both useful matches and misleading matches.

Claude can propose a map in seconds, and some of its proposals will be good. Proposing is Claude's work. Deciding is yours, because whether two words are interchangeable is a fact about the policy and population the words describe, not about the words. A proposal does not enter the vector until you encode it, and when you do, record the exact map and whether it applies to queries, documents, or both. Applying it only to the query creates an asymmetry, which is a design choice; expanding both sides can change counts and vector lengths. Keep the map's provenance where a reviewer can find it, and do not say you improved semantics without specifying the operation and the cases examined.

A useful test set contains the intended synonym match and a case where the mapping should not imply support. For example, construct a document about a fee reimbursement for travel and a query about tuition-refund eligibility. Literal mapped overlap may rise while the policy question remains unanswered. Label this as a constructed counterexample, not evidence about a real university rule.

The tension is recurring. More recall, meaning more potentially useful material returned, can also return more distractors, and more restrictive matching can omit paraphrases. The balance depends on the downstream task and the cost of missing versus reviewing candidates, and that cost is the task owner's to price. This chapter does not establish one universal threshold. An abstention rule faces the same problem, and the gate below returns to it.

## Relevance and entailment are separate checks

Retrieval asks which documents are similar enough under a rule to inspect first. Evidence review asks whether a selected passage supports a specific claim. The second question cannot be collapsed into the first merely because the score is precise to ten decimal places.

Suppose a selected passage says office hours are available by appointment. A generated answer claims they occur every Tuesday at two. The passage is relevant to office hours but does not supply the Tuesday time. The answer may contain an unsupported addition even though retrieval selected the right general topic.

The review should work claim by claim. Quote or identify the exact source passage within the permitted material, state the answer claim, and record whether the passage supports, contradicts, or does not resolve it. Do not treat a document-level citation as support for every sentence in a paragraph.

Who runs that check matters. If the process that wrote the sentence also vouches for its citation, you have the first opinion run twice. Claude can quote the passage, propose a label, and hunt for the sentence that would change it, which saves you the search. The label that goes in the table is the one you gave after reading the original, and when you disagree with Claude's label, you write down the sentence that decides it. *Irreducibly Human* draws a line worth borrowing for overrides: a human correction adds signal when it names what the machine misses in this kind of case, and adds noise when it is a wordless hunch. The book draws it for validated imaging systems and statistical forecasts, not for source labeling, so take it as a discipline for writing your override, not as evidence about Claude. “I read it differently” is not a check. “This sentence names the term but not the date” is.

The format contract from Chapter 2 can require source identifiers. That is useful for traceability, but a structural pass names the obligation it passed, and “has a source identifier” is a different obligation from “is supported by that source.” When the selected context is insufficient, the correct result may be an abstention or a request for another source. Do not fill the gap with a plausible answer and cite the nearest passage. A task packet should specify how insufficiency is represented so the system is not pushed toward a fabricated completion.

This is also why supplying an entire corpus is not automatically superior. More text can include the missing evidence, but it can also contain contradictions, irrelevant material, and more content than a bounded task should expose. Context selection is an engineering and data-governance decision. The goal is sufficient, authorized evidence with an inspectable selection path.

Anthropic's [context-engineering article](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), checked during the research pass on 2026-09-06, discusses context as a designed collection of instructions, tools, data, and history. Use it to compare selection strategies, not to claim our count vectors implement Claude's context mechanisms.

## The gate: write the source list and the evidence rules first

You have the machinery. Now do the part that loses its value if Claude does it for you, in your learner workspace, before you build or ask for anything. This is the chapter's gate, in two halves: one for the retriever and one for the task packet. The values below are my choices for the constructed fixture. No model produced them, and none is special.

**Half one: the retriever.**

*Design.* Count vectors over lowercase `\b\w+\b` tokens, cosine as the score, zero scores dropped before the cutoff, ties broken by document key, default k of two. Write these down so they are decisions on your record and not defaults you inherited.

*Contract.* Cosine of count vectors is never negative; identical direction scores one whatever the lengths; an empty side scores `0.0`, a convention and not a finding about the query. `retrieve` returns only positive scores, best first, equal scores in key order, at most k rows. It refuses a k that is not a positive integer, and a Boolean is not one. The audit view returns every document with its score and one of three fates: selected, below the cutoff, zero overlap.

*Wrong versions your tests must catch.* Write the test list so that each of these fails at least one test: sort worst-first; break ties by insertion order; check k with `isinstance` so that `True` slips through; ignore k beyond a fixed size; drop the normalization; drop the zero filter. Then read the lesson's six tests against that list before you trust them. Its relevance test has a single positive-scoring document, so best-first and worst-first sorts return the same thing. No test has two equal scores. The invalid-k test uses zero, which an `isinstance` check also rejects. No test makes k smaller than the number of positive matches. Confirm this by mutating a copy of the reference. If a wrong version survives your tests, the gate is not finished, and it is cheaper to learn that now.

*What a failure looks like.* Write one sentence, dated, about what you would see if the retriever were wrong in the way you most fear for your corpus. If you write it after reading the output, you have described the output.

*What this retriever may claim.* A ranking of overlap under one representation. Not that a passage is relevant in the sense a reader means, supported, or complete.

**Half two: the task packet.**

*The expected sources.* Before you ingest anything, write the list of sources you expect the task to need: title or identifier, owner, version or date, why each is authorized, and the number of items you expect the corpus to hold. Date it. This borrows two moves from *Computational Skepticism*: lock your prediction of what a dataset you did not build contains before you look, and ask the row-count question of documents. Write the list from your knowledge of the task. Do not ask Claude what a corpus for this task should contain before you have written yours. Its answer would be built from the task description you gave it, the same material you are trying to check. The book's warning is that a fluent AI-generated frame contains no information, because the AI started from the same documentation you did. Applied to a corpus, I read the book's structural assumptions as questions about your list. Are these the sources easiest to gather or the ones the task needs? Does each cover the period the question is about, and is it the current version? Is each an original, or a summary someone, or some model, wrote about it?

*The claims the report may make.* One sentence per question the report must answer, each small enough for a single passage to support or not. If a sentence has an “and” in it, split it.

*The evidence rules.* Define the row labels before you see a report. Supported: a quoted passage states the claim, within its scope, date, and population. Contradicted. Insufficient: the nearest passage is on topic but does not resolve the claim, and the row names what is missing. Not reviewed. State who may mark a row supported (the person who read the original authorized source) and what the report must do when the sources do not say: say so, and not fill the gap.

*The abstention rule and its counterexample.* “Refuse when no document scores above zero” avoids answering from an empty selection in the synonym fixture, but positive overlap can still be insufficient, so the rule establishes no support. Raise the threshold and some useful short passages are excluded. Write the positive-scoring case the rule wrongly lets through, the case a stricter threshold wrongly refuses, and what review remains.

*What the packet may claim.* “Under this corpus and these rules, these claims were supported by these passages.” Not “comprehensive,” unless your inventory justifies the word.

Claude can sharpen this gate by pointing out a claim that is not small enough, a rule with no case that would fail it, or an insufficiency the table has no row to hold. It cannot write the expected-source list without defeating it, because that list is where your understanding of the task goes on the record.

Design first is not design frozen. If ingestion turns up a source you did not list, or a listed source is absent, that finding reopens the gate. Keep the original list, dated, and add the revision with its reason. The gap between what you expected and what you found is the most informative thing the exercise produces.

## Build It: preserve the scoring path

Before you open the reference solution, write your own. It is your baseline: the record of what you understood before Claude touched anything, and the instrument you will measure Claude's version against.

Implement `vector`, then verify the count for repeated mixed-case text. Implement cosine and calculate the office-hours example by hand before running it. Preserve the tokens, counts, dot product, norms, and final score. A lone decimal makes the mechanism harder to audit.

Then implement retrieval with positive-score filtering and deterministic sorting. Read the [six tests](../lessons/07-context-retrieval-and-cowork/code/tests/test_main.py) before the reference, and predict the empty-vector result, identical-direction score, relevant ranking, zero-overlap exclusion, and invalid-k behavior. Add a tie test with keys chosen so alphabetical order is visible, the synonym miss, and the tests your gate says the lesson's six leave open. Explain why each test addresses a different property. Do not describe the total as complete retrieval coverage.

If you implement a synonym map, keep it in your learner version and record the before-and-after ranking on both intended and false-positive cases. The map is data that influences the result, so preserve its provenance.

## Use It: conduct Claude Code, then build a bounded Cowork task packet

Now hand Claude the work it is good at, against the gate you wrote.

**Conduct Claude Code.** Open Claude Code in your learner workspace. Give it the contract, the test list, and the audit-view specification from your gate, and not your implementation. Ask for an implementation that satisfies the contract and passes your tests, plus the audit view, then run your tests on what it returns, yourself.

Do three things with the result. First, note which of your tests failed, if any. A failing test is often a gap in your gate, which Claude cannot see because it has only what you wrote. Second, compare its implementation with your baseline and name one difference in behavior: a boundary it handled that you missed (a revision to your gate) or one it silently ignored (a defect your tests failed to catch). Third, ask Claude to propose a deliberately wrong version that still passes your tests, and check by hand whether it does. If it does, your list was too weak, and you found out cheaply. You can also ask Claude to critique your representation and suggest cases; verify every suggestion against the displayed mechanism.

Preserve the actual transcript: your prompt, the plan, the diff, the commands, and the outputs, with the date and displayed model label. If a session failed or did not run, record that rather than substituting a fixture.

**Build the packet.** The task packet should name the goal, permitted sources, output format, exclusions, and acceptance checks, and state how selected passages were obtained. A returned report without the corpus and retrieval record is difficult to audit when a claim lacks support.

Build a small corpus from material you are authorized to use, recording source identity, version or date when relevant, and inclusion criteria. Do not upload restricted material merely because the interface can accept it. The data boundary from Chapter 5 remains in force: who may read what is a decision people make, not one the interface makes for you.

Run retrieval and inspect both selected and omitted candidates, using the audit view. Compare the inventory with the expected-source list you dated before ingestion. For each required answer claim, identify whether sufficient evidence appears in the selected context. If not, revise the query, representation, corpus, or task scope. Do not revise the final prose alone and assume the evidence problem disappeared.

If you run the task through Claude Cowork, preserve actual interface details and output. This chapter cannot claim which internal retrieval steps the product used, so compare your explicit packet and evidence table with the interface task as an observed workflow, not as proof of internal equivalence. If the interface is unavailable, ship the offline corpus, retrieval results, and proposed packet, and mark the generation portion not run. The mechanics and evidence design remain assessable without fabricated results or direct API spending.

## Ship It: the source-grounded task packet

### Debug the pipeline in the order information moves

When a final claim is unsupported, start upstream rather than rewriting the answer repeatedly. The stages from the opening table give the order.

| Stage | The question to ask | A failure looks like | Whose repair |
| --- | --- | --- | --- |
| Eligibility | Was an appropriate source allowed in? | Excluded by a permission or scope decision | Yours; retrieval cannot legally repair it, and the claim may need narrowing |
| Ingestion | Did the eligible file become a document value? | A format was skipped, the wrong folder was read | Yours to check; the reference starts from a constructed dictionary and never demonstrates this step |
| Representation | Do query and document share any coordinate? | The synonym case: the vectors share none | Yours to decide; no prompt after retrieval repairs it |
| Scoring and cutoff | Did it score positive and still fall below k? | A positive-overlap document ranked below the cutoff | Yours; if a larger k brings in the evidence, record the added review burden |
| Selection into context | Is what Claude saw what the retriever returned? | Another filter or a manual choice narrowed it | Yours to record, naming each narrowing |
| Use | Did the answer ignore, overgeneralize, or embellish a shown source? | The source is in context; the claim goes beyond it | The first stage where rewriting the answer helps, and support is still a separate review |
| Claim | Does the conclusion match the evidence? | A summary calls the report comprehensive or verified | Whoever signs; the claim-to-source table constrains the verbs |

Start at the top. Preserve the score of a document that fell below k rather than pretending it was never considered. Debugging ends when the stated conclusion matches the actual evidence, not when every stage has produced a green marker. This is a decomposition of the artifact you can inspect, not a claim that production systems implement these modules; a real interface may combine operations or keep internals unavailable. You can still record the source boundary, visible inputs, selected context when exposed, output, and your independent evidence review.

### Chunk boundaries create another representation

A corpus often divides long sources into passages. The reference treats each dictionary value as a complete document, so it does not implement chunking. If you add chunks, you have introduced a selection decision before cosine ranking, and it is yours. A claim and its qualification can fall in adjacent chunks, and retrieving only the claim-shaped fragment can make a passage look stronger than its source. A large chunk can instead dilute lexical overlap with unrelated terms and lower its normalized score. These are hypotheses to test on declared text, not reasons to assert that one chunk size is correct.

Give chunks identifiers that preserve source identity and location. A generated citation to `chunk-7` is difficult to audit if the packet does not connect it to a document and passage, and the reviewer needs enough surrounding text to see whether a qualification was cut away. Construct a harmless example with two adjacent sentences, one stating a policy and the next naming an exception. Compare retrieval when they remain together and when split, and state whether the answer still needs the omitted qualification. Chunk overlap can reduce some boundary misses, but it duplicates tokens and candidates and influences ranking and context volume, so record the choice instead of treating overlap as free completeness. The lesson's transparent dictionary postpones these complications on purpose: learn the count-vector and ranking mechanics first, so that when you add chunking you can attribute each new behavior to the new layer.

### Build an evidence table that can say no

A useful claim-to-source table follows the rules you wrote in the gate. It needs more than claim and citation columns. Add the exact supporting passage or stable location, a reviewer judgment, and a note about scope or missing qualification. The judgment distinguishes supported, contradicted, insufficient, and not reviewed, as you defined them.

Do not force every row into supported merely because the report is supposed to be complete. An insufficient row is actionable evidence: it tells the writer to narrow the sentence, retrieve more material, or abstain. If the table cannot represent a gap, it pressures the reviewer to hide one.

For the office-hours hypothetical, “appointments are mentioned” is supported by the supplied sentence, and “appointments occur Tuesday at two” is insufficient because the time is absent. Atomic claims make that visible; a paragraph-level judgment could conceal that one part is grounded while another is invented.

The source passage deserves provenance too. A string entered by the learner is a constructed fixture. A passage copied from a real policy needs an authorized source, a version or retrieval date where relevant, and enough location information to revisit it. Do not merge those roles in one table without labeling them.

Label each row yourself first. Then ask Claude to find the sentence that would change your label, and record whether it did. Claude can challenge, group claims, and locate possible passages, but it should not be represented as the human who owns the final source interpretation. Ask another reviewer to challenge one supported row as well: if they need surrounding text you did not record, the record should improve. The score suggests where to look, the packet shows what was available and selected, and the table records whether the claims survive inspection. That is how retrieval becomes part of an evidence system and not a convenience hidden before generation.

Two more disciplines keep the packet honest. Preserve the query that actually produced the selection: a revised query may retrieve better evidence, but its success cannot be attributed to the original run, so keep both, label the revision, and record any synonym a human supplied after seeing the failure. And distinguish the source collection from the context finally shown to Claude. The corpus may hold twenty items, the retriever may return two, and the interface may receive one after another filter or manual choice. A complete selection record names each narrowing; without it, a reviewer may blame the generator for information the workflow never supplied.

The result is not maximal context. It is accountable context: enough authorized material to support the bounded answer, an explicit record of what was left out, and a route for saying the evidence is insufficient.

### The packet, assembled

The [artifact brief](../lessons/07-context-retrieval-and-cowork/outputs/artifact-brief.md) asks for corpus provenance, retrieval results, task packet, report, and claim-to-source table. Make their relationships explicit.

The corpus inventory shows what was eligible. The retrieval record shows what the algorithm selected. The task packet shows what Claude was permitted and asked to use. The report contains the resulting claims, and the evidence table connects them back to exact passages and records gaps. Your dated expected-source list sits in front of all of them, so a reader can see what you thought the corpus would contain before you looked.

Include at least one omitted or insufficient case, and explain whether a missing source was absent from the corpus, scored zero, or fell below k. A packet containing only the passages that made the answer look good cannot reveal the selection boundary. End with a bounded conclusion: which claims were supported by which passages under the recorded corpus, and which questions remain unresolved.

**The sign-off.** End the packet with a statement you could put your name to. Claude can draft its words in seconds and the draft will be fluent, so write it from your record. The verbs matter: “retrieved” describes what the selection rule returned, “quoted” what you copied, and “supported” a claim and a passage you actually compared. “Verified” and “comprehensive” need more than this packet offers unless you did the work behind them. This is the template, not a signature:

```text
Sign-off — source-grounded task packet
Checked:      which claims, against which exact passages (list the rows);
              the expected-source list against the corpus inventory
How:          by reading the original authorized source myself / by one
              cosine recomputed by hand / by tests I wrote before reading
              the reference / with Claude's help (say which parts)
Not checked:  sources that were not in the corpus; ingestion beyond the
              files I opened; other tokenizations or languages; whether any
              source is itself correct or current; passages below the cutoff
              that I did not open
Not claiming: that the report is comprehensive; that this retriever is what
              Cowork does; that a retrieved passage is a supporting one
Signed or withheld: ____________  (name, date)
```

The “Not checked” line does the work. An AI-written sign-off leaves it out, because the system that wrote it has no record of the sources you never opened or the file that failed to load. If your evidence does not support signing, withhold.

### The driver's seat

This is how the chapter's work divides, task by task. Test your own record against it.

| Task | Claude should | You should | Why it stays with you |
| --- | --- | --- | --- |
| Listing what is in a folder, scoring and ranking every document, quoting candidate passages | Do it, fast, and show every score | Read the full audit view, not only the winners | Ranking is the part to hand over. Omissions are invisible in a list of winners, so reading what was left out is yours |
| Writing the expected-source list | After you write it, propose missing-source questions for you to check | Write it first, from the task | A frame Claude reconstructs starts from the same documents you gave it |
| First implementation of the retriever from the contract | Implement it and the audit view | Build your own baseline first; run your tests on its version | You cannot audit a ranking you never computed |
| Proposing a synonym map, a chunk size, a larger k | Propose, with cases that might break it | Decide, and record where each came from | Whether two terms are interchangeable is a fact about the policy and population, not the words |
| Labeling a claim supported, contradicted, or insufficient | Quote the passage, propose a label, find the sentence that would flip it | Label first, from the original; own the final label | What the source means in the world, its scope, date, and who it governs, is your reading, and you are the one whose name is on it |
| Which sources may be used; narrowing the claim or abstaining | List what the task could reach, flag restricted material and insufficient rows | Decide: authorize, narrow, ask for another source, or stop | Authorization is a decision people make, and the cost of a missing answer against a wrong one belongs to the task owner |

Record, in the packet, one task you delegated and one judgment you retained. The evidence is concrete: the Claude Code transcript showing what you gave it, the dated expected-source list and its comparison with the inventory, and the rows where your label differed from Claude's proposal or you changed your mind. If you cannot point to the transcript line or the edit that shows each, the split happened in your head and not in the record.

## Verify and reflect

Run the demo, lesson tests, and your added cases. Recalculate one cosine score independently, confirm the returned ordering and k cutoff, and preserve the interpreter and input corpus rather than reporting a score without its representation.

Open your expected-source list and compare it with the inventory. Write the gap in one sentence: a source you expected and did not find, one you found and had not expected, or neither. The gap is the learning, so do not rewrite the list to match.

Audit one generated or proposed claim against the original source, not only the selected chunk: read the authorized text around the quoted sentence, since chunk boundaries can omit qualifications. If the claim exceeds the passage, revise or remove it and preserve the reason.

Ask which exclusion changed your view: a source absent from the corpus, a synonym with zero overlap, a positive match below k, or a relevant passage that did not entail the claim. Naming the failure location turns generic distrust into an engineering decision. Finally, review the words relevant and supported. Relevant should refer to a scoring or human topical judgment you can describe. Supported should refer to a claim-evidence relationship you actually inspected. Do not swap them because both sound favorable.

## Assessments — ungraded practice

These Assessments carry no points. Use the paired lesson's [knowledge check](../lessons/07-context-retrieval-and-cowork/quiz.json) and preserve predictions before viewing explanations.

### Warm-up

1. **Token counts — introductory; objective: construct a vector.** Tokenize a short mixed-case sentence by hand, predict its Counter, and compare with execution. Name one discarded feature and one task in which losing it would matter.
2. **Dot product — introductory; objective: calculate overlap.** Compute the office-hours dot product and both norms before calculating cosine. Explain every term.
3. **Zero length — introductory; objective: trace a boundary.** Predict cosine with one empty vector and explain the implementation's returned value without calling an empty query meaningful.

### Application

4. **Ranking change — intermediate; objective: predict selection.** Add one query term present in only one document, predict the ranking, then run it. Explain how both dot product and norm can change.
5. **Tie order — intermediate; objective: test determinism.** Construct equal-score documents with distinct keys. Predict the returned order and identify the sorting components. Then write the wrong version that orders ties by insertion and show which of your tests fails on it.
6. **Synonym miss — intermediate; objective: diagnose representation.** Reproduce tuition refund versus fee reimbursement. State what zero means under the vectorizer and what it does not tell you about the corpus.
7. **Top-k omission — intermediate; objective: inspect truncation.** Construct three positive matches with k two. Record the omitted result as an audit row with its score and fate, and explain why omission is not proof of irrelevance.

### Synthesis

8. **Claim-to-source table — advanced; objective: evaluate support.** Build a table for a short report, including one relevant passage that does not support the full claim. Label each row yourself first, then ask Claude for a sentence that would change one label. Revise the claim or mark it unresolved, and record whether your label moved and why.
9. **Synonym-map tradeoff — advanced; objective: evaluate a representation change.** Add a small explicit map and test both a useful match and a misleading match. Record who proposed each pair and who decided it. Defend whether to retain the map for the bounded task.

### Challenge

10. **Abstention under pressure — stretch; objective: design a refusal rule.** Propose a rule based on retrieval evidence, then construct a positive-score case it should still refuse. State what human review remains and why the retriever cannot take it over.
11. **Corpus audit — stretch; objective: reconstruct exclusions.** Write, before you look, the list of sources that should exist for a small task. Then compare that list with the sources ingested and the passages selected. Trace one missing answer to its actual failure location without filling the gap plausibly.

## What you can now trace

You can move from raw text to a sparse count vector and state which information was kept or discarded. You can derive cosine similarity, reproduce `2 / sqrt(6)`, and distinguish the assigned score from a judgment about the source's adequacy.

You can explain how filtering, sorting, tie-breaking, and k create a returned set. A zero-overlap document may be semantically related and a high-overlap document may still be insufficient. That is not a contradiction; the score and the support review have different jobs.

And you can say what the three jobs look like here. You conducted: you wrote the retriever's contract, the tests that must fail the wrong versions, and a dated list of the sources you expected, all before Claude implemented or ranked anything. You checked: you refused to let a high score stand in for support, and you traced what was excluded before treating a selected passage as sufficient. You drove: you handed Claude the scoring, the implementation, and the quoting, kept the list of what should exist, the label on each claim, and the choice to narrow or abstain, and signed or withheld. The packet you built lets another reviewer diagnose whether a failure began in ingestion, representation, ranking, generation, or interpretation.

## A protocol connects capabilities

Retrieval selects information for a task. The next challenge is connecting a host to a tool that advertises and executes a capability through messages. A well-formed connection can still expose an unsafe or misleading action. As a high score is not support, a compatible message is not an authorized one.

Chapter 8 builds a minimal Model Context Protocol server state machine. We will trace initialization, tool discovery, request identifiers, and error results, then separate protocol compatibility from trust and authorization. The question to carry forward is the one you answered here about context: who decided what reaches Claude, and where is that written down?

## Anthropics

Use [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), checked 2026-09-06, to compare deliberate context selection with supplying an entire corpus. Record what your selection retains and omits. Do not imply that lexical counts are neural embeddings or Claude Cowork internals.

## Computational Skepticism

The companion's data-validation chapter supplies two diagnostics the body has not used. See [Data and retrieval](../docs/computational-skepticism.md#data-and-retrieval), which points to the passages on hidden assumptions and on reconstructing the epistemic frame. The first is the access-boundary assumption: a dataset's effective reach is its schema plus whatever its contents reference. The chapter bounds the claim itself. It is sharpest for reference-rich material such as email and weak for a self-contained table of sensor readings. Apply it to one passage in your corpus. Does it quote, link, or defer to a document that is not on your source list? If so, the passage cannot be read as complete without that document, and the dependency belongs in the packet as an unresolved item.

The second is the row-trace step. Follow one answer passage back to its original source. Where the original is unreachable, the chapter's instruction is to document the opacity, which it counts as a finding and not a failure of the procedure. Record which of “not retrieved,” “not in the corpus,” and “not true” you could establish and which you could not. These are two questions for the packet, not a measurement of this retriever or corpus.
