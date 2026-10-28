# Chapter 1 — Next-token prediction and sampling

*The answer changed. First, find out what you actually measured.*

Suppose you ask Claude the same question twice. The first answer is short. The second has a different example, a different qualification, perhaps a different conclusion. You now have two outputs and several possible explanations. The temptation is to pick the explanation that sounds most familiar: the prompt was vague, the model was creative, the system was unreliable. None of those descriptions identifies the moving part. You have observed a difference. You have not yet isolated its cause.

Claude will gladly help with that diagnosis. In seconds it will write a fluent, confident account of why the answers differed, and the account may even be right. What it cannot do is know which moving part you needed to isolate, check its own account against the machinery, or put its name on the result. That division of labor is what this whole book is about, and this chapter shows it at the smallest scale that still has a real mechanism in it.

Here is the argument in brief. Claude is far better than you at producing fluent text, working code, and long lists of plausible candidates, at a speed and volume no person matches, so do not compete with it there. It has no stake in whether any of it is true and no way to tell you whether it is the thing you needed. So three jobs stay with you: decide where it goes before it runs, check what comes back, and sign your name to what you keep. I call them conduct, check, and drive.

The chapter comes in two parts. Part 1 describes what a language model actually computes, one prediction run in a loop, because you cannot conduct a machine you have not looked inside. Part 2 shrinks that machine to three outcomes and three numbers, small enough to inspect every intermediate value, and uses it to design an honest experiment. The toy will not reproduce Claude, and that is its advantage: there is nowhere for an unexplained operation to hide.

Both parts serve one distinction: a score is not a probability, a probability is not an observed frequency, and an observed frequency is not a correctness judgment. We can make one outcome increasingly likely without adding any evidence that it is correct, and make a run repeatable without making its answer true. Those follow from what the program is designed to compute.

This book's exercises assume access to Claude Code. Enrolled Northeastern students should begin with the university's [Claude portal](https://claude.northeastern.edu/) and the repository's [access guide](../docs/neu-claude-access.md); public readers need their own Claude Code-enabled account. This chapter's Python experiment needs no API key and spends no direct API credits; its numbers come from an offline program, not a fabricated conversation with Claude.

## What you will be able to do

By the end, you should be able to describe a chatbot as a next-token predictor inside a loop, say what pretraining and preference tuning each target, and restate a training-scale slogan as an arithmetic derivation with its assumptions named. You should be able to calculate a three-outcome distribution, explain why subtracting the largest score preserves it, predict how positive temperature changes its concentration, and compare a recorded sample with the distribution that generated it.

You should also be able to do three things the rest of the book builds on. Write the contract for a small experiment before you run it, then conduct Claude Code against that contract and run your own tests on what it returns. Write a sign-off that claims no more than your evidence supports. And say which parts of this chapter's work you handed to Claude, which you kept, and why.

Part 1 needs no code. Part 2 needs Python functions, lists, and basic arithmetic with exponentials; it does not need a model SDK. The paired [lesson](../lessons/01-randomness-and-first-prompts/docs/en.md) supplies the runnable learning sequence and its existing knowledge check.

## Three jobs that stay yours

Here is the book's argument, stated once, because every later chapter repeats it at a different scale.

Claude is better than you at one kind of work: pattern and association, producing and retrieving and recombining text and code, in parallel, at a speed no person matches. In *Irreducibly Human* I call this the first tier of human cognition, and the practical conclusion is blunt: stop competing with the machine there. Nobody races a car. What Claude lacks is a stake. It has nothing riding on being right, it was not there for what you meant, and nothing in its machinery asks whether the output is what you needed. The car does not choose the destination. You do.

Three questions follow you through every chapter. Each comes from one of three companion books, and each becomes a device you will use.

| Job | The question it adds | The device | Companion book |
| --- | --- | --- | --- |
| **Conduct** | What did I decide before Claude started, and what must be true before this output goes downstream? | **The gate** | *Conducting AI* |
| **Check** | What would tell me this is wrong, who checked it and how, and what did nobody check? | **The sign-off** | *Computational Skepticism for AI* |
| **Drive** | Which part of this is Claude's to do, which is mine, and what would show the split was honest? | **The driver's seat** | *Irreducibly Human* |

**Conduct.** Claude implements well from a complete specification and badly from an incomplete one, and it will not tell you which you gave it. In *Conducting AI* the human's job is "not to type less" but "to decide more precisely": the design, the constraints, and the gates, each a specific, testable condition that must hold before an output moves on. Here a gate is a few lines you write before asking Claude for anything: what the thing must do, what it must refuse, and the test that would fail a plausible but wrong version.

**Check.** Claude's mistakes arrive fluent: the well-formed prose does the work the verification should have done. *Computational Skepticism for AI* turns this into two habits. Write down what a wrong answer would look like before you read the output, and do not revise the note afterward. And keep the check independent of the thing checked: Claude can run tests and propose counterexamples, but "an AI checking an AI is not a second opinion, it is the first opinion run twice." It is your name on the result.

**Drive.** The split is by task, not by a slogan about who is smarter. Claude can draft, compute, retrieve, test, and challenge. You choose the question, justify the assumptions, own the decision, and keep enough of the underlying skill to notice when the machine is wrong.

That last clause is why you will build small things by hand in a book about a tool that writes code faster than you do. You are not trying to out-type Claude. You are acquiring the baseline that makes conducting possible; *Irreducibly Human* puts it in one line: you cannot audit what you do not know. So every chapter runs the same sequence. Build the small mechanism. Write the gate. Conduct Claude against it. Check what comes back. Sign only what the record supports.

The car picture is good and incomplete. A car's failures are loud: the engine knocks, the dashboard lights up. Claude's failures are quiet, and its confidence reads highest exactly when the answer is wrong, because confidence and correctness come from different places. The driver needs to understand the engine well enough to hear a knock that makes no sound.

## Part 1 — What a language model does

This part describes what you are conducting. Read it for two things: what the machine does very well, and what no step of it contains.

### The unfinished script

Imagine a page of dialogue between a person and an assistant, with the assistant's half torn away. Now imagine a machine that takes any stretch of text and returns a plausible continuation: not *the* continuation, but a ranked field of candidates with numbers attached. You could rebuild the missing half mechanically. Feed in what survives. Take a candidate for the first fragment of the reply. Append it. Feed the longer text back in. Repeat until the machine proposes an ending.

That procedure is not an analogy for a chatbot. It is a description of one, and it is worth taking literally; the framing comes from Grant Sanderson's explainer *Large Language Models explained briefly* (3Blue1Brown). When you send a message to Claude, no component in the system is answering your question. One component is repeatedly answering a different question, what plausibly comes next in this text, and a loop around it turns those answers into something that reads like a reply.

<!-- [FIGURE: Cajal production brief. A chatbot is one prediction, run in a loop. Include transcript so far, model, probability for every token, sample one, append and repeat. Show the confirmed relationship that no step in the loop consults a source or an answer key. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![A chatbot is one prediction, run in a loop. The transcript goes into the model, the model returns a probability for every possible next token, one token is sampled and appended, and the same question is asked again.](../images/01-randomness-and-first-prompts-fig-01.png)
*Figure 1.1 — A chatbot is one prediction, run in a loop*

Hold onto the shape of that diagram. It is the machine's strength: a superb continuation engine, and everything fluent you have seen Claude do comes from that loop running well. It is also the machine's boundary. Nothing in the loop reads a document, checks an answer key, or knows whether the growing text is true. Retrieval, tools, permissions, and approval gates arrive in later chapters as attempts to supply something the loop does not contain, and every one of those attempts is something you design and then check.

### One question, asked over and over

Be precise about the unit. The machine does not predict words. It predicts **tokens**: fragments drawn from a fixed vocabulary, where a common word may be one token, a rare word several, and a space is usually part of the token that follows it. `unbelievable` might arrive in three pieces. That is why a prompt that asks for an exact character count asks the machine to reason about a unit it does not natively see.

The output for one step is not a token. It is a number for every token in the vocabulary, tens of thousands of them, arranged so the numbers are nonnegative and sum to one. Every candidate continuation gets a share, including absurd ones. The absurd ones get small shares. Nothing is excluded; things are merely ranked.

<!-- [FIGURE: Cajal production brief. One step: context in, a ranking over strings out. Include the context string, the model, and a probability for every vocabulary token. Show the confirmed relationship that ordering describes the training corpus and not the world. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![One step: context in, a ranking over strings out. A context string enters the model and a probability is returned for every token in the vocabulary. The ordering describes the training corpus, not the world.](../images/01-randomness-and-first-prompts-fig-02.png)
*Figure 1.2 — One step: context in, a ranking over strings out*

The caption of that figure contains the chapter's whole argument in one line. The distribution ranks *continuations of a string*. Its shape was fixed by fitting parameters to a body of text. If `Paris` receives a high probability after `The capital of France is`, the number is reporting something about how that phrase tends to continue in the corpus the model was fit to. It is not the output of a lookup against an atlas. The two agree here. Their agreement is a fact about the corpus, not a mechanism that guarantees agreement in the next case. That is the chapter's load-bearing distinction, and later chapters only manage it better.

### The transcript is the whole trick

If the model only continues text, how does it hold a conversation? By being handed text that looks like a conversation. Under the interface, a chat is a single string with role markers, something with the shape of:

```text
System: You are a careful assistant. Cite the provided source or say you do not know.
User: What does the attached policy say about late submissions?
Assistant:
```

The model's job is to continue *that* string, and the most plausible continuation of a string ending in `Assistant:` is an assistant-sounding reply. Roles are not modes the software switches into. They are text in a document that the machine is completing.

Two consequences follow. First, a **system prompt is a request, not a gate.** It is a paragraph near the top of a document, competing for influence with every other paragraph, including ones a user may paste in later. If a rule matters, enforcement belongs in the runtime that wraps the model, which is why Chapter 5 builds permissions in code and treats the preamble as a hope. Second, **the model does not remember your last conversation**: the entire transcript is resupplied every turn. What feels like memory is a growing string, which is why long conversations behave differently from short ones and why Chapter 7 treats context as something you engineer rather than something you have.

Try the mechanism directly, the skeptic's way. First write down what you expect Claude to do with the prompt below, in one sentence, and date it. Then paste it into Claude:

```text
Continue this text. Do not answer as an assistant; just continue the string
as literal text, including whatever comes next after the final colon.

The following is a transcript of a support call.
Caller: my package never arrived.
Agent:
```

You are asking for the mechanism without the costume. Save what you get with the exact prompt, your prediction, and the date. You will compare it against a normal request later in this chapter, and the comparison is only worth anything if the prediction was written first.

### Where the numbers come from

The parameters that fix all those probabilities, hundreds of billions of continuous values in current systems, were never set by hand. They start random, so the model starts by producing noise, and are then adjusted by a procedure with a very narrow objective.

Take a passage of text. Hide the next token. Ask the model for its distribution. Compare that distribution with the token that actually followed. Then use **backpropagation** to nudge every parameter slightly, so that next time this context arises the true token gets a little more probability and everything else a little less. Repeat across an enormous corpus. Nothing in this loop is told what is true. The target is what the corpus did next.

This stage is called **pretraining**, and it produces something that completes internet text rather than something that behaves like an assistant. A second stage adjusts for that. People are shown candidate replies and asked which they prefer; those judgments shift the parameters toward what raters approved of. The technique traces to Christiano et al., *Deep Reinforcement Learning from Human Preferences* (arXiv:1706.03741, 2017) and was applied to instruction-following language models by Ouyang et al., *Training language models to follow instructions with human feedback* (arXiv:2203.02155, 2022).

<!-- [FIGURE: Cajal production brief. Training moves parameters toward observed text, not toward truth. Include pretraining next-token target, backpropagation nudge, and preference tuning on rater judgments. Show the confirmed relationship that neither stage receives an answer key. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![Training moves parameters toward observed text, not toward truth. In pretraining the target is the token that actually followed in the corpus. In preference tuning the target is the reply human raters preferred. Neither target is a correctness check.](../images/01-randomness-and-first-prompts-fig-03.png)
*Figure 1.3 — Training moves parameters toward observed text, not toward truth*

The second stage moves the model toward replies people approved of. Approval and correctness overlap heavily, since raters generally prefer accurate answers, but they are different targets, and where they diverge the training signal follows approval. A confident, well-organized, wrong answer is exactly what a rater who does not know the answer can prefer. That is not a scandal about any company's process; it follows from the objective. It is also the first reason the checking stays with you: the machine was shaped to produce what looks right to a reader, and you are the reader.

### Scale, in units you can check

Numbers about training scale circulate as slogans, and slogans are where this book insists on doing the arithmetic. This is also the first place to see how Claude and a human divide a check: Claude will do the division instantly and should; the part it will not do unprompted is ask what the number assumed.

GPT-3 is a useful anchor because its details were published: 175 billion parameters, roughly 300 billion training tokens, and a reported total training compute of 3.14 × 10²³ floating-point operations (Brown et al., *Language Models are Few-Shot Learners*, arXiv:2005.14165, 2020). Later frontier models are substantially larger, and their figures are frequently undisclosed.

You have probably heard that it would take a person thousands of years to read that much text. Run it yourself. The [derivation script](../research/llm_scale.py) makes every assumption an argument, and its [recorded output](../research/llm-scale.json) holds the results. Three hundred billion tokens at about 0.75 words per token is 225 billion words. Reading nonstop at 250 words per minute, that is **1,711 years**. At 200 words per minute it is 2,139 years. At 150, it is 2,852.

Sit with the spread. The headline figure is not a measurement. It is a division whose answer moves by more than a thousand years depending on a reading rate nobody stated. That does not make the comparison useless: every version says *more text than a person could read in many lifetimes*, which is the actual point. It makes the comparison an illustration with a hidden parameter, and finding hidden parameters in impressive-sounding numbers is a skill this course keeps asking you to use.

The compute figure behaves the same way. Suppose you could perform one billion operations per second by hand. GPT-3's reported training compute would take you about **9.95 million years**. You may have heard "over 100 million years"; that claim requires roughly 3.2 × 10²⁴ operations, about ten times GPT-3's budget, which is plausible for later systems but is a different claim about a different model. Both sentences can be true. They are not the same sentence, and a reader who cannot tell them apart cannot audit either.

### Inside one prediction step

The architecture that made this scale practical is the **transformer** (Vaswani et al., *Attention Is All You Need*, arXiv:1706.03762, 2017). Its relevant property here is parallelism: earlier models walked through text one position at a time, while a transformer takes the whole context at once.

Inside, four things happen. Each token becomes a list of numbers, because the fitting procedure only works on continuous values. Then **attention** lets those lists read each other and revise themselves according to context: the vector for `bank` after `river` ends up somewhere different from the vector for `bank` after `savings`. Then a feed-forward layer adds patterns stored during training. Then both operations repeat, layer after layer. At the end, the vector at the final position, by now influenced by everything else in the context, is turned into one score per vocabulary token, and those scores are normalized into a distribution.

<!-- [FIGURE: Cajal production brief. Inside one prediction step. Include token vectors, attention revision by context, feed-forward layer, repeated layers, final-position vector, one score per vocabulary token, normalization. Show the confirmed relationship that context mixing ends in scores and then a normalization. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![Inside one prediction step. Tokens become vectors, attention lets them revise each other using context, a feed-forward layer adds stored patterns, the pair repeats across layers, and the final position's vector is turned into one score per vocabulary token and then normalized into a distribution.](../images/01-randomness-and-first-prompts-fig-04.png)
*Figure 1.4 — Inside one prediction step*

That last step is where Part 2 begins. The normalization turning scores into a distribution is a specific, small, inspectable transformation, and you are going to build it from arithmetic in a few pages. Everything to its left in the figure is out of reach at this scale; the final arrow is not.

One more property constrains every honest claim. Researchers designed the operations, not the behavior. What the model does emerges from how the parameters were fitted, so nobody, including its builders, can read off why a particular prediction was made. "The model decided X because Y" is, absent interpretability evidence, a story about a system rather than a measurement of one. Claude will tell such stories fluently if you ask it to explain its own answer; treat them as hypotheses to test, never as a trace of what happened.

### Stochastic parrots

The most influential name for the skeptical reading of all this is the **stochastic parrot**, from Bender, Gebru, McMillan-Major, and Shmitchell, *On the Dangers of Stochastic Parrots: Can Language Models Be Too Big?* (FAccT '21). Their claim, in outline: a language model stitches together sequences of linguistic form it observed in training according to probabilistic information about how those forms combine, with no access to meaning. Fluency is not comprehension, and the coherence you perceive is supplied largely by you, because humans reliably attribute intent to well-formed text.

The argument has a conceptual half and an empirical half, and conflating them is the usual mistake. The conceptual half (Bender and Koller, *Climbing towards NLU*, ACL 2020) holds that meaning is a relation between form and something outside language, which a system trained on form alone cannot reach. The empirical half concerns consequences: the costs of training at scale, the impossibility of auditing web-scale corpora, and the harms of deploying systems whose fluency invites unearned trust.

The paper is contested. Critics say the conceptual half settles by stipulation what ought to be investigated, and cite probing work suggesting that internal representations track non-linguistic structure; defenders reply that internal structure is not grounded reference, and that the empirical half stands however the philosophy resolves. This book does not settle it. Be wary of the phrase as a conversation-ender meaning *it's just autocomplete*: that is weaker than the paper's claim, and systems that merely replayed observed sequences would not generalize to strings absent from training, as these demonstrably do.

Here is the version this chapter stands behind, because Part 2 will demonstrate it in code rather than assert it. **The mechanism ranks continuations, and ranking a continuation highly is not evidence that it is true.** You do not need a position on machine understanding to accept that. You need only look at what the transformation receives as input and notice that an answer key is not among its arguments. The same observation sets the terms for the rest of the book: you do not need to believe Claude is hollow to check its work, or that it understands to use it. You need a gate before it runs and a check after.

### What Part 1 gives you, and what it leaves with you

You can now say that a chatbot is a next-token predictor inside a loop, that roles are text rather than modes, that training targets observed text and rater preference rather than truth, and that a prediction ends in a normalization over vocabulary scores. You cannot yet say what this implies about the variation you observe: ask the same question twice and the answers differ, but the parameters and architecture did not change between runs. Something else moved. Part 2 shrinks the system until that moving part is the only thing left in the room.

## Part 2 — Randomness you can inspect

### The gate: write the experiment before you run it

Before any arithmetic, do the part Claude cannot do for you. Write the experiment down, in plain sentences, in your learner workspace. This is the first gate in the book.

*Design.* The constructed scores are `[1, 2, 3]`. The temperatures are 0.5, 1, and 2. The sample is 1,000 draws with seed 7. These are my choices; no model produced them, and nothing about them is special.

*Contract.* Probabilities are nonnegative and sum to one. A larger score never gets a smaller probability at positive temperature. Equal scores get equal probabilities. The function refuses an empty list, a nonfinite score, and a temperature that is zero, negative, or nonfinite. Sampling with the same seed repeats.

*A wrong version your tests must catch.* Pair the probabilities with the wrong labels and the sum is still one. Reinitialize the generator on every draw and one repeatability test might still pass. If your tests cannot tell these from the right program, the gate is not finished.

*What a failure looks like.* Write one sentence about what you would see if the program were wrong, and date it. If you write it after reading the output, you have described the output, not tested your understanding.

*What this experiment may claim.* A distribution over three indices and counts of draws. It cannot say that any outcome is correct.

Claude can sharpen the gate. It cannot write it for you without defeating its purpose: the gate is where your understanding goes on the record, and it is what you will test Claude's implementation against.

### Three scores are not yet three chances

The list `[1, 2, 3]` expresses an ordering: the third entry is largest. It does not yet express chances. Call its entries scores, or logits when referring to the function's parameter name; the word gives them no extra authority. Keep the index separate from the score: outcome two has score three, and confusing those numbers is an easy way to misread the output.

Probabilities must be nonnegative and sum to one. These scores sum to six. Dividing each by six would produce one possible distribution, but it would be a different transformation from the one implemented in the lesson, and it would fail on negative scores. We are explaining a particular mechanism, not inventing any normalization that happens to work on one positive list.

The mechanism exponentiates score differences, then divides by the total weight. An exponential converts any finite real input into a positive weight. What matters is not that score three becomes an impressive number but how its weight compares with the weight for score two. Ratios survive normalization.

Let the score for outcome i be z_i, let T be a positive temperature, and let p_i be the probability assigned to that outcome:

```math
p_i = \frac{\exp(z_i/T)}{\sum_j \exp(z_j/T)}.
```

The index j walks over all available outcomes. The denominator is the total weight, so the probabilities sum to one in exact arithmetic. That is a statement about the transformation, not a statement that the inputs were sensible or the outcome labels true.

Before calculating anything, predict the ordering. For positive T, dividing by T preserves score order, the exponential preserves it again, and every weight is divided by the same positive total. The ordering survives. Changing a positive temperature can change how strongly the largest score dominates; it cannot make a smaller score the largest probability.

That prediction is more useful than a remembered decimal. If your implementation gives the smallest score the largest probability, you do not need a screenshot to compare against. You have a reason to suspect an error: perhaps you negated the score differences, or paired probabilities with the wrong labels. An explanation has become a debugging instrument, and Claude can help you use it only if you already hold it.

### The subtraction that changes nothing important

The [reference implementation](../lessons/01-randomness-and-first-prompts/code/main.py) does not directly exponentiate the original scores. It first finds their maximum and subtracts it from every entry. For `[1, 2, 3]`, the shifted scores are `[-2, -1, 0]`. At temperature one, the weights are approximately `0.135335`, `0.367879`, and `1`, summing to approximately `1.503215`. Dividing each weight by that sum produces the probabilities recorded in the research run.

Why is subtraction allowed? Let m be the maximum score:

```math
\frac{\exp((z_i-m)/T)}{\sum_j \exp((z_j-m)/T)}
=
\frac{\exp(z_i/T)\exp(-m/T)}{\exp(-m/T)\sum_j \exp(z_j/T)}.
```

The common factor cancels. We have changed the intermediate weights, not the intended distribution. That is the whole design choice: the computer does not need large intermediate exponentials to express a ratio. After subtracting the maximum, the largest exponent is zero and its exponential is one, and the others are no larger than one.

The lesson tests this choice with equal large scores, `[1000, 1000]`, expecting `[0.5, 0.5]`: subtracting the maximum leaves `[0, 0]`, exponentiation gives `[1, 1]`, and normalization divides both by two. The large shared offset carries no information about relative preference, so it never needed to survive into the weights. The [test file](../lessons/01-randomness-and-first-prompts/code/tests/test_main.py) is evidence for this concrete case, not a proof that every numeric input is handled.

Here is the central implementation, reproduced from the lesson so that the mathematics has a visible destination. Build your own attempt before using this as a reference.

```python
import math

def probabilities(logits, temperature=1.0):
    if not logits or not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("Need logits and a positive finite temperature")
    if not all(math.isfinite(x) for x in logits):
        raise ValueError("Logits must be finite")
    peak = max(logits)
    weights = [math.exp((x - peak) / temperature) for x in logits]
    total = sum(weights)
    return [weight / total for weight in weights]
```

The input checks are part of the mechanism, not decoration. An empty list offers no outcome to normalize; a zero temperature makes the division invalid; a negative temperature would reverse the ordering we just relied on. A function is partly defined by what it refuses to compute. This is the first appearance of a pattern that recurs through the book: the refusals are where a human's decisions live, because Claude writes the happy path unprompted and the boundary only if your gate demands it.

Keep the tested claim narrower than the slogan "numerically stable." The sum check uses approximate equality because floating-point arithmetic has limits, which is a reason to choose an assertion that matches the calculation, not to ignore errors. A sum close to one shows one property. It does not show the ordering is right, that equal scores get equal probabilities, that invalid temperature is rejected, or that sampling consumes the probabilities correctly.

### Temperature is a concentration control, not a fact checker

Return to the ratio between two outcomes. Normalization cancels out of it:

```math
\frac{p_i}{p_k} = \exp\left(\frac{z_i-z_k}{T}\right).
```

Here k names another outcome. If z_i exceeds z_k, their positive difference is divided by T. A smaller positive T makes the exponent larger and increases the probability ratio; a larger T brings the ratio closer to one. The transformation is changing relative concentration, which explains the temperature effect without a slogan about creativity.

Predict before inspecting the table. With scores `[1, 2, 3]`, will temperature `0.5` or `2` give more probability to outcome two? Which gives more to outcome zero? Write both predictions. Predicting only the winner misses most of the experiment, because the winner stays the same throughout.

The following values come from the [recorded offline worked examples](../research/worked-examples.json), under key `chapters.01`. They were computed using the course implementation; the research script also checks agreement with a direct-exponential calculation for these moderate inputs.

| Temperature | Outcome 0, score 1 | Outcome 1, score 2 | Outcome 2, score 3 |
| --- | ---: | ---: | ---: |
| 0.5 | 0.0158762400 | 0.1173104278 | 0.8668133322 |
| 1.0 | 0.0900305732 | 0.2447284711 | 0.6652409558 |
| 2.0 | 0.1863237232 | 0.3071958857 | 0.5064803911 |

The largest score remains the favorite, but its share moves from about eighty-seven percent to about fifty-one percent across the displayed temperatures, and the smallest score gains probability as the distribution flattens. Scores, ordering, and transformation stay fixed while temperature changes, so nothing in that operation supplies evidence about the meaning of any selected answer.

Make the limitation concrete. Suppose, as an explicitly constructed hypothetical, the three labels are proposed answers to a question whose independently checked answer is label zero. Lowering temperature concentrates selection on label two, which is wrong under the stipulated answer key. The transformation works as designed; the failure is in treating its preference as a truth guarantee. Do not report this as an observed Claude error. No change in concentration can supply information the program never receives.

Low temperature is also not the same as choosing the largest score directly; this interface rejects zero rather than switching to a deterministic mode, and it is not a promise about any Claude setting.

<!-- [FIGURE: Cajal production brief. Temperature reshapes concentration, not ordering. Include scores, T = 0.5, T = 1, T = 2. Show the confirmed relationship that same outcome order; different concentration. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![Temperature reshapes concentration, not ordering. same outcome order; different concentration.](../images/01-randomness-and-first-prompts-fig-05.png)
*Figure 1.5 — Temperature reshapes concentration, not ordering*

### A distribution is not the sample you happened to see

The probability function returns a recipe for selection, not a thousand outcomes. The next function makes that transition. It creates a local pseudorandom generator, asks for weighted selections, counts which indices appeared, and returns a dictionary of counts.

```python
import random
from collections import Counter

def sample(logits, count=1000, seed=7, temperature=1.0):
    if type(count) is not int or count < 0:
        raise ValueError("Count must be nonnegative")
    rng = random.Random(seed)
    return dict(Counter(rng.choices(
        range(len(logits)),
        probabilities(logits, temperature),
        k=count,
    )))
```

The choices are outcome indices, not logit values. Separating the arguments gives distinct experimental controls: count changes how many observations you collect, seed changes the selected sequence under otherwise fixed conditions, and temperature changes the weights. Python's [random documentation](https://docs.python.org/3/library/random.html), consulted for the research packet on 2026-09-06, describes separately instantiated generator state and weighted choices with replacement, the narrow behaviors used here; the saved run records Python 3.14.6.

At temperature one, the distribution assigns about `0.6652409558` to outcome two. Multiplying by one thousand gives an expected count of about `665.24`, which cannot be an observed count because a count is an integer; the program samples rather than rounding. The observed count in the saved seed-seven run is 630. Here are the actual counts, in outcome order:

| Temperature | Outcome 0 count | Outcome 1 count | Outcome 2 count | Total |
| --- | ---: | ---: | ---: | ---: |
| 0.5 | 18 | 133 | 849 | 1,000 |
| 1.0 | 102 | 268 | 630 | 1,000 |
| 2.0 | 202 | 329 | 469 | 1,000 |

These counts are evidence of the recorded executions, not exact expressions of the theoretical probabilities. At temperature one, outcome two's observed share is `630 / 1000`, or `0.63`, against an assigned probability of about `0.66524`. Keep both numbers in the report. They answer different questions: what chance was assigned, and what fraction appeared in this sample?

Do not look at one gap and pronounce the sampler broken. You first need an acceptance criterion appropriate to the experiment. The existing reproducibility test checks that the same call returns the same counts, which is repeatability, not agreement with every theoretical proportion. Also, the returned dictionary has no key for an outcome never selected, so retrieve missing counts as zero; a missing key means no recorded selections, not removal from the probability model.

Now reconsider the seed. It lets you return to a particular experiment while debugging, but it gives the sample no factual status. If a fixed sequence repeatedly selects our hypothetically wrong label, repeatability preserves the mistake. This is the fluent wrong answer in miniature: a result you can reproduce on demand is still only as true as what produced it.

### First prompts: the same experiment, one floor up

The toy has a seed argument. Claude does not expose one to you, so run the comparison you can actually run. These four prompts are deliberately boring: each isolates one variable and produces a record you can keep. Write your prediction first, paste the prompt as written, save the actual responses with the date and displayed model label, and never substitute a remembered summary for a transcript.

**1 — Does the same input give the same output?** Open four separate new conversations and send this once in each. Do not send it four times in one conversation; the transcript grows, which changes the input.

```text
In exactly one sentence, explain why a shuffled deck of cards is a bad
source of randomness for a security key.
```

Record all four. Note what is stable, the claim roughly, and what moves: examples, hedges, clause order. It is the counts table, one level up.

**2 — Shrink the distribution and watch variation fall.** Same procedure, four fresh conversations:

```text
Answer with one word only, no punctuation and no explanation.
What is the capital of Australia?
```

Compare the spread against prompt 1's. A constrained format leaves fewer high-probability continuations to choose among, so the answers converge. It is the closest thing you have to lowering temperature without a temperature control, and it made the answer more repeatable and no more true.

**3 — Fluency without support.** In a fresh conversation:

```text
State one specific quantitative finding from a peer-reviewed paper on
spaced repetition, with the authors, year, and the exact number.
Then, separately, rate your confidence that this citation is real.
```

Now check the citation yourself. Whatever you find, the response was fluent and well-formed either way: the ranking machinery produced a confident-looking string, and confidence was never one of its inputs. This is the check the book will ask of you most often, and notice who does it. Claude cannot be the independent check on its own citation, because the process that made the citation would be vouching for it.

**4 — Claude as a reviewer of your reasoning, after you have reasoned.** Once you have written your own prediction for Part 2's experiment:

```text
Here is my prediction and my reasoning: [paste yours].
Do not tell me whether I am right. Instead, name the single assumption
my reasoning depends on most, and describe an input that would make it fail.
```

Withholding the verdict is deliberate: you want the boundary case, not the grade. This is the use of Claude that sits comfortably inside your own thinking. It challenges; you decide.

### Build It: the baseline that lets you audit

Before you open the reference solution, write your implementation in the learner workspace, starting with the probability transformation on a short list whose ordering you can inspect by eye. Explain each intermediate quantity (shifted score, weight, total, probability) and what would count as an impossible value for it. Then add boundary checks: the lesson's tests cover a sum near one, equal large scores, a temperature comparison, repeatable sampling, rejection of zero temperature, and rejection of an infinite score. Read these as six distinct questions, not as "the code works."

Your own version is the baseline: the record of what you understood before Claude touched anything, and the instrument you will measure Claude's version against. Once you can explain it, compare it with the reference and name a difference in behavior, not in line count or style.

### Use It: conduct Claude Code against your gate

Now hand Claude the work it is good at. Open Claude Code in your learner workspace. Give it the gate you wrote, the contract and the test list, and not your implementation. Ask for an implementation that satisfies the contract and passes your tests, then run your tests on what it returns, yourself.

Do three things with the result. First, note which of your tests failed, if any; a failing test is often a gap in your gate, which Claude cannot see because it only has what you wrote. Second, compare its implementation with your baseline and name one difference in behavior: a boundary it handled that you missed (a revision to your gate) or one it silently ignored (a defect your tests failed to catch). Third, ask Claude to propose a deliberately wrong version that still passes your tests, and check by hand whether it does. If it does, your test list was too weak, and you found out cheaply. Either way the check is yours, because whether your tests are enough cannot be judged by the system they are testing.

Preserve the actual transcript: your prompt, the plan, the diff, the commands, and the outputs, with the date and displayed model label. If a session failed or did not run, record that rather than substituting a fixture.

### Ship It: a report that survives a skeptical reader

The chapter's artifact is a sampling report. Its value is that another reader can connect the table to inputs, code, execution conditions, and a claim; if any link is missing, a polished presentation can conceal an experiment that is difficult to interpret.

Begin with the prediction you wrote before running, and preserve it even if it was wrong; a report that quietly replaces it with the correct answer destroys the comparison that makes the exercise informative. Then record the constructed scores, temperatures, count, seed, interpreter, and commands, with both probabilities and observed counts, and state what changed your explanation. Keep the Claude transcripts from the first-prompts experiment as a separate record: actual prompts, responses, displayed model label, date, and interface.

Use a claim such as: "In the recorded local run, decreasing temperature from two to one-half concentrated the assigned probability on the largest score; the resulting sample counts are recorded separately." Now imagine a reviewer who sees the outcome-two count of 849 and asks whether that proves the answer is correct. Your report should make the reply easy: 849 is a count of an index selected in a constructed experiment, and correctness would need an answer key or source check tied to a meaningful claim.

**The sign-off.** End the report with a statement you could put your name to. Claude can draft its words in seconds and the draft will be fluent, so write it from your record. This is the template, not a signature:

```text
Sign-off — sampling report
Checked:      which properties, by which of my own tests (name them)
How:          by hand / by a test I wrote before reading the reference /
              by recomputation / with Claude's help (say which parts)
Not checked:  inputs outside my tests; other Python versions; any claim
              about correctness of an outcome
Not claiming: that any outcome is true, or that this models a Claude setting
Signed or withheld: ____________  (name, date)
```

The "Not checked" line does the work. It is the line an AI-written sign-off never includes, because the system that wrote it has no record of what you did not do. If your evidence does not support signing, withholding is an honest result.

### The driver's seat

This is how the chapter's work divided, task by task. Test your own record against it.

| Task | Claude should | You should | Why it stays with you |
| --- | --- | --- | --- |
| The arithmetic of a derivation (the scale division, the weights) | Compute it, instantly and correctly | Name the assumption the number hides | A number does not say what it assumed |
| Writing the contract and the test list | Challenge it: find the case you missed | Write it, first | The contract is your understanding on the record |
| A first implementation from a contract | Implement it, fast | Build your own baseline first, then run your tests on its version | You cannot audit what you have not built |
| Explaining a surprising output | Propose hypotheses | Test each against the code and the input | An explanation from the system under test is a story, not a trace |
| Saying what the result supports | Flag an overclaim | Choose the verb and sign | Your name is on the claim |

Record, in the sampling report, one task you delegated and one judgment you retained. If you cannot point to the transcript line or the edit that shows each, the split happened in your head and not in the record.

### Verify and reflect

Verification begins with a claim small enough to test: the equality of the shifted and direct formulations on moderate inputs, rejection of an invalid temperature, or repetition of a seeded call. Name which claim each check addresses. The [worked-example script](../research/worked_examples.py) and its JSON preserve the research calculation and observed values; neither substitutes for your own prediction and implementation.

After running the tests, pick one passing case and explain it without reading Claude's explanation, walking from input to returned value; then pick one rejected input and explain why refusal belongs to the contract. Finally, inspect the report's strongest sentence. "Recorded" describes an observation, "computed" a calculation; "established correctness" requires a criterion the sampler never receives.

The most useful reflection is local: which distinction did you originally collapse? Scores and probabilities? Probabilities and frequencies? Repeatability and truth? Name the input or calculation that separated them again. That is a concrete habit to carry forward, in place of the generic resolution to be more careful with AI.

## Assessments — ungraded practice

These Assessments develop the chapter's capabilities and carry no points. Use the paired lesson's existing [knowledge check](../lessons/01-randomness-and-first-prompts/quiz.json) before viewing its explanations. The prompts below extend practice; they are not a competing quiz bank. Write predictions before execution, and keep solutions in your own learning artifacts.

### Warm-up

1. **Score, weight, probability — introductory; objective: explain the transformation.** For the scores `[1, 2, 3]`, label every quantity between input and returned probabilities, and say which values must sum to one. Explain why dividing the scores by their sum is a different rule from the exponential transformation. Do this before looking at the reference, then name one correction you made after comparing.

2. **Equal preference — introductory; objective: calculate and test.** Choose two equal finite scores other than the demo input. Predict their probabilities, write an assertion that represents the prediction, and explain why the shared absolute score should not determine relative preference. Do not claim a two-outcome test covers every input.

3. **A boundary with a reason — introductory; objective: explain refusal.** Choose one invalid temperature or nonfinite score. State the expected behavior, run the case, and explain why the function should reject it instead of inventing a convenient result.

### Application

4. **Temperature before decimals — intermediate; objective: predict concentration.** Choose three unequal moderate scores and compare temperatures one-half and two. Predict the ordering and which outcome gains probability before calculating, justify it with the probability-ratio expression, and state the smallest claim your result supports. Attach no correctness label without a separately defined answer key.

5. **One sample, two descriptions — intermediate; objective: compare assigned and observed quantities.** For a fixed distribution, seed, and count, record probabilities, counts, and observed proportions. Explain why a gap is not automatically a bug, and propose a check that would catch a genuine implementation mistake without demanding exact proportions.

6. **Sample-size experiment — intermediate; objective: design a controlled comparison.** Run one distribution at two sample sizes, recording all other inputs, with your expectation written first. Say which comparison is about counts and which about proportions, and why changing seed and temperature together would muddy interpretation.

7. **The absent key — intermediate; objective: handle a representation boundary.** With a small sample, find out whether every outcome index appears in the returned dictionary. Write a reporting function that shows unobserved outcomes as zero, and explain why "not observed in this run" differs from "not a possible outcome."

### Synthesis

8. **Repeatable and wrong — advanced; objective: critique a correctness claim.** Construct labeled outcomes with an explicitly hypothetical answer key in which the largest score belongs to a wrong answer. Compare two positive temperatures, preserve the counts, and write a short review of why concentration and repeatability do not fix the mistake and what check would assess truth. Do not present the fixture as a Claude output.

9. **A report another person can audit — advanced; objective: integrate evidence.** Assemble predictions, decisions, outputs, tests, and limitations into the sampling report and finish it with the sign-off. Ask another reader, or Claude as a preliminary reviewer, to find one unsupported sentence; verify that criticism yourself, and revise the sentence while preserving the original.

### Challenge

10. **A misleading green test — stretch; objective: create a counterexample.** Introduce a small bug into a copy of your implementation that still lets one assertion pass. Explain the bug, identify the surviving assertion, and add a test that exposes the defect, showing why the first assertion was insufficient.

11. **What would transfer? — stretch; objective: separate model and system claims.** List the conclusions the three-outcome experiment supports and compare them with questions you would ask about a real Claude interaction. Mark which need documented interface details, actual transcripts, or independently checked sources, and design the evidence plan without running paid requests.

## What you can now explain

You can describe a chatbot as one prediction inside a loop, name what pretraining and preference tuning each target, and locate the normalization at the end of Figure 1.4 as the same transformation you then built by hand. The toy is not a metaphor for the last step of a real model; it is that step, at a scale you can print. You can predict the effect of positive temperature through a ratio rather than a personality metaphor, and separate assigned probability from observed share and a seeded replay from a supported claim.

And you can say what the three jobs look like at this scale. You conducted: you wrote the experiment, the contract, and the wrong version your tests had to catch before Claude ran anything. You checked: you wrote what failure would look like before you looked, and refused to let a repeatable or concentrated result stand in for a true one. You drove: you handed Claude the arithmetic and the implementation, kept the question, the baseline, and the verb, and signed or withheld.

## The next boundary

We have made variation inspectable, but an answer still needs a definition of acceptability. Suppose a response is stable, repeatable, and neatly formatted. It may still claim that the source says red when the source says blue. The sampler cannot reject that mismatch because it never receives the source's meaning as a condition to check.

The next chapter moves the boundary outward. We will build a contract around an answer: required fields, types, source identifiers, and an evaluation set. Then we will send that contract a false statement that satisfies its structural rules. Structure earns its place by rejecting specific failures; the mistake is asking it to reject failures it was never written to recognize. Carry your sampling report forward as the first piece of an evidence trail. Chapter 2 adds a question to it: when the program says an answer passed, exactly which obligation did it pass?

## Computational Skepticism

The companion's chapter on probability and confidence supplies a diagnostic the body has not used yet: keep confidence claims separate from observed correctness. See [Probability and confidence](../docs/computational-skepticism.md#probability-and-confidence), which identifies the calibration passage. Here the probabilities concern selection among constructed indices, not the chance that an answer is true. Apply that to one sentence in your report: state the event to which its probability refers. If it is "the sampler selects outcome two," do not quietly replace it with "outcome two is correct." This note contributes an auditing question, not a claim that we ran a calibration study.

## Irreducibly Human

In *Irreducibly Human*, I distinguish useful offloading from surrendering the foundational capability needed to evaluate the result. The passage is chapter 1's baseline-knowledge discussion, located through [Foundations before offloading](../docs/irreducibly-human.md#foundations-before-offloading). It is a curricular prescription here, not an empirical claim that this exercise measures a long-term cognitive effect, and it is why this chapter makes you build the small version before you conduct Claude.

**AI should** help diagnose errors after your first attempt, suggest boundary cases, run authorized checks, and organize actual results. It should label hypothetical examples and distinguish proposed explanations from observations. It should not invent your initial prediction or write a claim that you understood something you have not explained.

**Human should** make the prediction, build the initial mechanism, explain the transformation and one rejection case, and decide what the evidence supports. The protected work is not typing every character unaided; it is developing the model of the program that lets you notice when an attractive explanation is wrong. Then explain, unaided, why a repeatable sample can still select a wrong answer. If you cannot, take another pass through the three numbers, not a more elaborate prompt that conceals the gap.