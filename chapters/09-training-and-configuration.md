# Chapter 9 — Training and configuration
*Changing what the model sees is not changing what the model is.*

Suppose you upload documents, revise a system prompt, and get a better answer. A teammate writes it up as "we trained Claude on our policies." Something did change: the input available during that interaction. But the verb carries a claim about *what* changed, and that claim decides what happens next. If the change was training, the improvement lives in parameters, costs a training run to reproduce, and sits in whatever artifact holds those parameters. If it was a prompt, it lives in a text file you can diff and copy into another project. If it was retrieval, it lives in a corpus and a selection step, and it disappears when the corpus does. Training changes parameters through an objective and an update rule. Prompting and retrieval change the information supplied to an already configured model for inference. One word is hiding three different things to maintain, audit, and pay for.

The opposite mistake comes from following the recipe correctly. Below you build a small classifier, run its training loop, and read the numbers: average loss falls from `0.6931471806` to `0.0215209850`, and four held-out points come out four of four. The report line writes itself: the model learned, and it generalizes. The first half is fine; the parameters changed by a rule you can print. The second half is unsupported, and no line of code is at fault. The loss is the number the optimizer was told to lower, on the data it was shown. The four held-out points were chosen by one person around the same sign boundary as the training data. Neither number says what the sentence says it does.

Claude will do the mechanical half of this chapter faster than you can: derive the gradient, write the loop, tabulate the output. It will not decide what the update was *for*, whether four fixtures are a fair test, or whether the question your stakeholder asked was a prediction question at all. Those are Chapter 1's three jobs applied to a change request. Conduct: state what should change, and how you will tell, before you change it. That is the gate. Check: claim only what the record supports, and sign or withhold. That is the sign-off. Drive: decide what kind of question you are answering, because the causal question and its justification are yours. That is the driver's seat.

The machinery is deliberately small. A one-feature binary logistic classifier has two learned parameters, a weight and a bias. Four constructed examples define the training data. A sigmoid turns each linear score into a probability, a binary logistic loss measures disagreement with the labels, and gradient descent updates the parameters. It has the parts of a training run that this chapter's argument needs (an objective, an update rule, a data split, a budget) and almost nothing else. Every intermediate value can be printed.

Nothing in this exercise modifies Claude's weights. Nothing exposes Claude's logits, optimizer, or training data. The classifier is not a miniature language model in every relevant sense, and it is not a fine-tune of anything. It is a transparent case of one row in a table of five things a system can change, built so you can tell that row from the other four without leaning on metaphor.

## What you will be able to do

You should be able to calculate a sigmoid prediction, explain the stable loss expression, derive and check one gradient update, and evaluate a trained classifier on separate points. You should be able to classify a proposed system change by the object it modifies (weights, prompt, context, tools, or settings) and say what evidence would show that object, and not another, was responsible.

You should also be able to do three things the rest of the book builds on. Write the gate for a change before making it: the objective, the held-out set specified separately, and the stop rule for the loop. Conduct Claude Code against that gate, run your own tests on what it returns, and write a sign-off that says "lower training loss" when that is all you measured. And say which question your result answers, prediction or intervention, and which parts of the work you handed to Claude and which you kept.

You need Chapters 1, 2, 7, and 8, algebra, averages, exponentials, and introductory derivatives as explained here. The paired [lesson](../lessons/09-training-and-configuration/docs/en.md) provides runnable instructions and the existing knowledge check. The program is offline Python. Claude Code can help inspect your calculation through your existing account; direct API credits are not required.

Before reading the reference, write down two predictions and date them: the initial probability for every point when both parameters are zero, and the direction the weight should move on the first update, reasoned from the labels and the signs of the features. Beside them, write what a wrong answer would look like. A prediction written after you have seen the output describes the output. A model that returns plausible decimals is no substitute for knowing which direction should reduce this constructed loss.

## Part 1 — Which object changed?

### Name the mutable object before you change it

A change request arrives in one sentence: make it follow our policy, make it stop inventing dates, make it write like us. Before you pick a technique you face a decision the sentence hides: which object are you allowed to change? The choices differ in cost, in how they persist, in who can reverse them, and in how you will tell whether they worked. There are five.

| Object | What you edit | Where the change lives | What shows it changed |
| --- | --- | --- | --- |
| Weights | Parameters, through an objective and an update rule | The saved parameter values | The values, plus the data, objective, rate, and budget that produced them |
| Prompt | Instruction text and examples | A file or message you can diff | Both texts, side by side |
| Context | Which documents, passages, or records are supplied this turn | The corpus or store, and the selection step | The passages that actually entered the input |
| Tools | Which actions and information sources the host exposes, and which are permitted | Server code, configuration, permission rules | The configuration diff and the decision that authorized it |
| Settings | How outputs are drawn at run time, such as temperature in Chapter 1 | Run-time configuration | The recorded setting for each run |

Only the first row involves an optimizer. For Claude, nobody outside the people who train it can watch that row change, and nothing in this course claims otherwise. The toy in Part 2 exists so that you can watch the row change once, completely, and then recognize the other four by contrast.

Read the other rows by what they do. A system prompt is text in the input of an interaction; revising it can change behavior dramatically while the stored parameters stay untouched. Few-shot examples are input too. They demonstrate a pattern inside the current context, so if you change an example and the answer changes, the evidence supports prompt-context sensitivity under the recorded interaction, not a claim that Claude was retrained. Retrieval decides which source passages enter the context. In Chapter 7's implementation, adding a document changes what inference can see and nothing about the model. An MCP server changes the actions and information the host exposes (Chapter 8), and a permission rule changes which proposed operations the runtime allows. Both change capability and governance. A system can become more capable through tooling while the model stays exactly as it was, and calling a permission change "learning" turns a human governance decision into something that sounds like a property of the machine. A setting changes how an output is drawn from scores. It does not fit anything.

None of this ranks the rows. Prompting and retrieval are often the right tool for task-specific behavior, and training can be expensive, unnecessary, or out of reach. The ordering that helps is by reversibility and inspectability: text you can diff and revert in a second sits at one end, parameters you can only refit at the other. A configuration file can hold several kinds of setting at once, so trace the object, not the filename. For Claude, take interface and configuration details from current official documentation, and claim no access to proprietary weights or private training procedures.

### Persistence is not proof of training

People misname changes because several non-training changes persist. A saved system prompt remains in a project. A retrieved document remains in a workspace. A permission rule remains in configuration. A memory record remains available in later sessions. So "it stuck" cannot be the test for learning.

Training is identified by its mechanism, not by later influence. In the toy, `train` returns w and b after using labels and a loss-derived gradient, and that is direct implementation evidence. A saved prompt influences later requests by being included again as input. Both have durable effects, through different routes in the software. Personalization is the same case: a system may retrieve stored preferences or prepend them to the context, and without evidence of parameter updates you describe the memory or context behavior you observed, not a model that "learned the user" in the technical sense used here.

The test that separates the cases is an intervention on your own system: change one object and hold the rest fixed. In the toy, set w and b back to zero and the learned boundary is gone, whatever else you did. For a Claude interaction, remove the saved text and run the same input again; if the behavior goes with it, the text was holding it. With sampling in play, one run per condition shows little, so Chapter 1's repeated runs apply. Notice what this move is. You are not asking what correlates with the improvement. You are doing something to the system and watching what follows. Part 3 returns to that distinction, because it decides whether a fitted model can answer your question.

### What a production record can and cannot show

For each row you change, keep a before and an after. For training: the parameter values and the data, objective, rate, and budget that produced them. For a prompt: both texts. For retrieval: the corpus and the selected passages. For tools: the configuration diff and the authorized decision. Then ask whether the observed output difference uniquely identifies the mechanism. Usually it does not. A different answer could come from prompt text, retrieved context, tool output, model version, or sampling conditions, and the surrounding record is what lets you attribute the change cautiously.

Do not invent a before state you cannot see. If a service exposes only the current model label and a response, say which internal details remain unknown. The toy is useful because its state is completely visible; let that teach restraint where it is not. And name the kind of reproducibility you offer. Another reader can rerun the Python training from supplied data, replay a prompt under recorded but aging service conditions, or inspect a configuration diff. Each has different dependencies, and identical output is not the only acceptable repeat.

## Part 2 — A parameter update you can inspect

### The model: two numbers and a squashing function

For an input feature x, weight w, and bias b, the classifier first computes a linear score:

```math
a = wx + b.
```

It then maps that score through the sigmoid:

```math
\sigma(a) = \frac{1}{1 + e^{-a}}.
```

The returned value lies between zero and one for finite a. We interpret it as the classifier's probability for label one under this model. The threshold rule used in the research evaluation predicts one when the value is at least one-half and zero otherwise.

At `w = 0` and `b = 0`, every score is zero regardless of x. Since `e^0 = 1`, sigmoid zero is one-half. That is the initial prediction for all four training points: the model has not yet encoded any relationship between feature sign and label.

The [reference implementation](../lessons/09-training-and-configuration/code/main.py) computes sigmoid in two branches:

```python
def sigmoid(x):
    if x >= 0:
        return 1 / (1 + math.exp(-x))
    e = math.exp(x)
    return e / (1 + e)
```

The negative branch rewrites the same mathematical quantity to avoid evaluating an unnecessarily large positive exponential when x is very negative. The lesson test checks that sigmoid of negative one thousand is approximately zero without overflow. That is evidence for the demonstrated numeric behavior, not a promise about arbitrary types or all floating-point edge cases.

The model has one feature. A positive learned weight makes positive x values produce positive scores and probabilities above one-half; negative x values produce negative scores and probabilities below one-half when the bias stays near zero. That geometry matches our constructed labels. The parameter does not learn a word meaning or a causal relationship. It fits the relationship represented in the supplied pairs. The source used during research, Jurafsky and Martin's logistic-regression chapter draft, supports the weighted-input and sigmoid mechanism; our numerical results come from the local implementation and an independent calculation. Keep conceptual source and execution evidence distinguishable.

<!-- [FIGURE: Cajal production brief. Training changes parameters; prompting changes inputs. Include x, wx+b, sigmoid, loss versus y, gradient update, prompt/context. Show the confirmed relationship that inference context does not update w or b. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![Training changes parameters; prompting changes inputs. inference context does not update w or b.](../images/09-training-and-configuration-fig-01.png)
*Figure 9.1 — Training changes parameters; prompting changes inputs*

### The gate: say what should change before you change it

Before any training runs, do the part Claude cannot do for you. Write the change down, in plain sentences, in your learner workspace. This is the chapter's gate. It does the same job as Chapter 1's: it is where your understanding goes on the record, it is what you test Claude's work against, and it must exist before the loop does. Chapter 1's gate fixed an experiment. This one fixes a change request, and the three items that matter most are the ones most often left implicit: the objective, the held-out set, and the stop rule.

*Change.* Weights only: the two numbers w and b, starting from zero. The prompt, the context, the tools, and the settings are not in play, and Claude's own weights are not in play at all.

*Objective.* The average binary logistic loss on the four training pairs listed below, and nothing else. "Better" means "lower on this objective on these pairs." That is the only thing the training run may be called.

*Held-out.* Four pairs, fixed now and never passed to `train`: `(-3, 0)`, `(-0.5, 0)`, `(0.5, 1)`, and `(3, 1)`. Their role is evaluation. They share the training data's sign pattern by construction, so they can support one claim: these four fixtures are classified correctly at threshold one-half.

*Stop rule.* Exactly 200 updates at rate `0.2`, from a zero start. No stopping early because the loss looks flat, no extra steps because the held-out result looks bad. If the budget must change, reopen the gate, write down why, and treat any evaluation points you have already seen as development data. The gate is not frozen; reopening it is a logged act, and a finding can send you back to an earlier decision.

*A wrong version your tests must catch.* Three. Sum the gradient over the examples instead of averaging it, and the first step is four times too large while the loss still falls. Copy the x factor into the bias update, and b moves on the first step although the symmetric data say it should not. Let a held-out point into the training list, and the "held-out" result stops meaning anything. If your tests cannot tell these from the right program, the gate is not finished.

*What a failure looks like.* One sentence, written and dated before the run. For example: if the first update is right, w moves positive and b stays at zero; if w moves negative, or b moves, a sign or an x factor is wrong. Written after you read the output, it describes the output.

*What this experiment may claim.* The parameters were updated by this rule, training loss on four pairs fell from one value to another, and four constructed points were classified correctly. It may not claim generalization, calibration, a change to Claude, or any cause.

*The pass condition.* The gate passes when every test you wrote from it passes on the code, and every sentence in your report fits inside the "may claim" line.

Every line above is a human decision, and none can be derived from the data, because the data have no opinion about what "better" should mean. For the toy they are my choices; no model produced them. For a real change request they are yours, and that is why none of it can be delegated. Claude can sharpen the gate: it can propose the wrong version and the test that catches it. It cannot choose the objective for you without making your report a statement about someone else's objective.

### Loss makes the objective explicit

The optimizer lowers whatever you give it, so the objective is a choice, and the gate has already made it. Each training example is a pair `(x, y)` with finite feature x and binary label y. The ordinary binary cross-entropy for predicted probability p is:

```math
-y\log(p) - (1-y)\log(1-p).
```

The reference evaluates an equivalent stable expression from the score a:

```math
\max(a,0) - ya + \log(1 + e^{-|a|}).
```

It averages this value across the data. The stable form avoids computing logarithms of probabilities rounded too close to zero or one for large scores. It is a numerically safer route to the same logistic objective for the accepted finite inputs.

At the origin every prediction is one-half. The loss for either binary label is negative log one-half, approximately `0.6931471806`. All four examples share that prediction, so the average has the same value. Two interface facts keep later claims honest. The training function records a list called history, but it appends only the initial and the final loss; two values are not a learning curve. And the loss function assumes nonempty data because training validates that before calling it; invoked directly on an empty list it would divide by zero. Describe guarantees at the call boundary that actually exists.

### Derive the first update

Claude will write this derivation in seconds, and it will probably be right. The reason to do it by hand once is that the number it must reproduce becomes your independent check. The training data are:

```python
[(-2, 0), (-1, 0), (1, 1), (2, 1)]
```

For logistic loss, the derivative with respect to the score for one example is prediction minus label. Call that error e. Since the score is `wx+b`, the contribution to the weight gradient is `e*x`, and the contribution to the bias gradient is e.

At the origin, every prediction is `0.5`. The four errors are therefore `0.5`, `0.5`, `-0.5`, and `-0.5`. Multiply by the corresponding x values:

| x | y | prediction | error p-y | weight contribution (p-y)x |
| ---: | ---: | ---: | ---: | ---: |
| -2 | 0 | 0.5 | 0.5 | -1.0 |
| -1 | 0 | 0.5 | 0.5 | -0.5 |
| 1 | 1 | 0.5 | -0.5 | -0.5 |
| 2 | 1 | 0.5 | -0.5 | -1.0 |

The contributions sum to negative three. Divide by four examples and the average weight gradient is `-0.75`. The errors sum to zero, so the average bias gradient is zero. Gradient descent subtracts learning rate times gradient. With rate `0.2`:

```math
w_{new} = 0 - 0.2(-0.75) = 0.15,
```

and the bias remains zero. This matches the executed result, and average loss after the step is `0.5876561461`. The sign makes sense before the decimal does: increasing a positive weight pushes positive examples toward label one and negative examples toward label zero.

The research script adds a second route. It computes a central finite-difference approximation of the weight gradient at zero: evaluate the loss at a small positive and a small negative perturbation, and divide the difference by twice the perturbation. The result is approximately `-0.74999999999`. Agreement within the chosen tolerance checks the analytic expression at this point, and it fails differently from the derivation, because it never uses the derivative formula.

Know what that independence covers. It is an independent calculation. It is not an independent dataset, reviewer, or causal source. And it checks the gradient against the loss function, nothing more. If logistic loss is the wrong objective for your task, the derivative and the finite difference will still agree, because both describe the objective you wrote. The check confirms that the update descends that objective. Whether it is the objective you meant is the gate's question.

### The loop, its rate, and its stop rule

The training function validates the data, step count, and rate. Labels must be zero or one, features finite, steps a positive integer, and rate positive and finite. It initializes both parameters to zero and records the initial loss. Each step builds errors from the current parameters, averages the gradient contributions, and updates weight and bias. After the requested number of steps it appends the final loss and returns the parameters plus the two-value loss list.

```python
for _ in range(steps):
    errors = [(sigmoid(w*x+b)-y, x) for x, y in data]
    w -= rate * sum(e*x for e, x in errors) / len(data)
    b -= rate * sum(e for e, _ in errors) / len(data)
```

This is batch gradient descent on the complete declared dataset. It does not shuffle, use minibatches, or adapt the rate. Those absences make the calculation traceable and also limit any analogy to large-scale training. After 200 steps the positive weight separates the sign-pattern data: the weight is approximately `3.1669517461`, the bias is effectively zero, and training loss is `0.0215209850`. The existing tests check that the loss fell and that the weight is positive. Passing them does not show the optimizer would behave under every dataset or rate.

The stop rule you wrote in the gate is a design decision, and the loop shows why. The first step, `0.15`, does not arise from the data alone. It is the average gradient `-0.75` scaled by a rate you chose, and a different positive rate would take a different step. The rate is supplied to `train`, which uses it to scale gradients but never updates it. It is a setting of the experiment, not a learned parameter. A very large rate can overshoot or become unstable on some data, and a very small one makes limited-step progress slow. The research establishes no safe universal range, so test chosen values on declared fixtures and report what happened. Do not write an optimization theorem from one decreasing-loss run.

The step count is a budget in the same way. Two hundred is the demo setting, not a discovered natural stopping point. The function runs exactly that many updates and has no convergence test, validation-based early stopping, or best-checkpoint selection. A lower final training loss shows what happened after the configured loop; it does not show the budget was right. If you compare rates or step counts, hold the data and initial parameters fixed, keep every result including the runs that behave badly, and choose your evaluation criteria before you look for the most attractive run. Otherwise a comparison becomes a search, and its final number is presented without the selection that produced it.

Two practice cases test whether you understand the relationship or only memorized the published positive number. Reverse the labels, and the preferred weight direction should reverse. Duplicate the evaluation points into the training data, and you contaminate the separation between fit and held-out assessment: apparent improvement on those points becomes hard to interpret, because the optimizer has already used them.

### Held-out means separately specified, not magically representative

The reference demo returns training parameters and initial and final training loss. It does not evaluate a held-out set. The chapter's research adds the four points your gate listed:

```python
held_out = [(-3, 0), (-0.5, 0), (0.5, 1), (3, 1)]
```

With the learned parameters, their predicted probabilities are approximately `0.00007478`, `0.17030378`, `0.82969622`, and `0.99992522`. Thresholding at one-half predicts all four labels correctly.

These points were not passed into the training function. That gives them a separate procedural role, and that is all "held out" means: a statement about how the points were handled. It does not make them representative of a natural population. We designed them around the same sign boundary as the training examples, so four correct labels establish behavior on these four constructed points under the stated threshold, and no more. A responsible report includes the result and this limit. "The model generalized" is too broad. "The trained parameters classified four separately specified sign-pattern fixtures correctly" matches the evidence. A broader performance claim needs a justified sampling process, a task definition, and a larger evaluation.

A held-out set also has a lifespan. Once it guides a choice, whether a rate, a step count, or a decision to keep going, it has become development data, and its next use is no longer independent. Record the change of role when it happens, and build an independent evaluation if the claim requires one. The toy has two roles, training and held-out. The moment you tune anything you need three: training, a development set to tune against, and a held-out set you touch once.

### What a lower loss claims

Lower training loss establishes one thing: the update rule reduced the objective on the pairs it was shown. It does not establish fit to pairs it was not shown, which is what the held-out set is for. And it does not establish that the objective was the right one, which no dataset can establish for you. Suppose, as a constructed hypothetical, that label one means "escalate this message to a person." The binary logistic loss penalizes a missed escalation and a false alarm by how confident the model was in the wrong direction, not by what each error costs you. If a missed escalation is far worse, a lower loss can sit comfortably beside the wrong behavior, and the missing measure is one the gate should have named: the costs of the two errors. Lower loss claims less than "better." Write "training loss decreased" when that is what you measured. "Better" is a claim about the task, and the task is not in the loss.

### Score, probability, and decision are three layers

A probability is not a decision. The score `wx+b` comes from the parameters. The probability comes from the sigmoid. The decision comes from a threshold, here one-half, which you chose and which training never saw. Move the threshold and the decisions move with identical parameters. Record all three layers, and know which one a claim is about.

The constructed data are symmetric: each negative feature with label zero has a positive partner with label one. At the origin the errors sum to zero, so the first bias update is zero, and across training the symmetry keeps the learned bias extremely close to zero in the recorded run. Do not conclude that bias is unnecessary. It shifts the decision boundary whenever the relationship is not centered at zero, and removing one point or changing one label can break the symmetry. The boundary sits where `wx+b = 0`, because sigmoid zero is one-half. With positive w and nearly zero b it lies near x zero, which is why the held-out negative features fall below one-half and the positive ones rise above it.

The held-out probabilities show more than four correct labels: values farther from zero are more extreme under the learned positive weight. That is an observed property of this fitted curve on selected points, not evidence that the confidence is calibrated. Chapter 1's distinction returns here. A model's probability is tied to its mechanism and objective, and whether it matches observed frequencies takes a calibration study on suitable labeled data. Four sign fixtures cannot support that.

## Part 3 — Prediction is not intervention

### Decide what kind of question you are asking

A fitted model arrives with a question attached. The decision that comes before any arithmetic is what kind of question it is. "Which label will this model assign?" asks about the model, and the fitted function answers it. "What would happen if we changed this?" asks about the world, and the function answers a different question.

Make it concrete with an explicit hypothetical, not a study. Suppose x counts the reminder emails a student opened in the first month of a course, y records whether they passed, and a fitted weight comes out positive. Question one: for a student who opened four emails, what label will the model assign? Evaluate the function and you are done. Question two: if we require every student to open the emails, will more of them pass? Evaluate the function at a larger x and you get a larger probability. That number is the model's response to a changed input. It is not the course's response to a changed behavior.

The gap exists because the fitted association has several possible sources. Opening emails might help. Students who are already on track might open more emails, so the arrow runs the other way. A third thing, motivation or free time, might raise both. The sample might contain only students who stayed enrolled. Each is consistent with a positive weight, so the weight cannot tell you which one you have. Acting on a prediction can also change the process that generated the data: a model fit to a period in which nobody acted on its flags can say little about what happens once people do. Our four constructed pairs are not a study at all. They were chosen to make the gradient visible and contain no information about any process in the world, so a causal sentence about them is a story attached to a fixture.

Judea Pearl's ladder gives the three questions names. Association: what goes with what. Intervention: what happens if I do this. Counterfactual: what would have happened to this case had we done otherwise. *Irreducibly Human* builds its Tier 5 chapter on the ladder, and its one-line version is that prediction is not identification: interventional and counterfactual answers generally cannot be recovered from purely observational data without structural assumptions that did not come from the data. I hold this to what the book itself claims. The limit is about information, about what observational data can yield. It is not a proof that no machine architecture could ever reason causally, and the book warns against reaching for that stronger claim. The practical content is narrower and harder to dodge: someone must supply and defend the causal assumptions, more data does not supply them, and neither a person's confident intuition nor a model's fluent explanation does. Nor is the lesson that observational data can never support a causal claim. It can, under assumptions you state and defend.

### What is Claude's here, and what is yours

The division of labor has a sharper edge in this part. Claude can write the notation for a causal diagram, list the confounders it can think of for a given setup, work out what follows if you assume a stated structure, and run the code. It writes fluent paragraphs about confounding because text about confounding is abundant in what such systems learn from, and fluency about causation is not identification of it. What it does not have is your study design, how the data were collected, or the domain facts about your students. It also has nothing riding on the decision. The identification judgment, choosing the variables and asserting the structure you are prepared to defend, stays with the person who will act.

One judgment sits before all of that: deciding whether the question is causal at all. The book's observation is that this decision is itself a causal judgment, since recognizing that a problem demands intervention reasoning is one of the things the ladder describes. I read it as a working rule. Before you hand Claude the algebra, write one sentence saying whether the stakeholder's question is "what will the model say" or "what happens if we act," and who decided. This chapter's report ends with one predictive claim your fixture supports and one intervention claim it does not establish. The pair is the evidence that you drew the line.

## Build It: the baseline that lets you audit

Claude can write sigmoid, loss, and the loop in seconds. You build them first because the update rule is the thing you will be asked to trust, and you cannot audit a gradient you have never computed. This is the same baseline Chapter 1 asked for, at the next size up.

Implement sigmoid and test zero, a large negative input, and a symmetry you can justify. Implement the stable loss and calculate the origin by hand. Implement one gradient step before writing the full loop. Read the [six lesson tests](../lessons/09-training-and-configuration/code/tests/test_main.py) before the reference, and predict the direction and rejection cases; each is a separate question, not "the code works." Add a finite-difference gradient check and a held-out evaluation in your learner artifacts, and do not claim the original demo returns them.

Run the one-step case at rate `0.2` and reconcile `w = 0.15`. If your value differs, inspect averaging, signs, and use of the current parameters. Do not adjust the expected result until the discrepancy is explained: the expected result came from your hand derivation, which is the independent route. Then run 200 steps and preserve the final parameters and the two recorded losses. Label the loss list accurately, and if you add full history, state that your version changed the implementation.

Now write one of the wrong versions your gate promised to catch. Change the update to sum the gradient over the examples instead of averaging. Before running it, predict three things: which of the six lesson tests will fail, how far the first step will land from `0.15`, and whether the final training loss after 200 steps will come out higher or lower than the reference's `0.0215209850`. Then run it. Tests 03 and 04 check only that the loss fell and that the weight is positive, so ask what they can distinguish. The summed version takes a first step four times as large. Whatever you find at step 200, ask what a lower number can tell you about whether the code is right.

## Use It: conduct Claude Code against your gate

Now hand Claude the work it is good at. Open Claude Code in your learner workspace and give it the gate you wrote, with the change, the objective, the held-out list, the stop rule, and your test list, but not your implementation. The lesson's [working prompt](../lessons/09-training-and-configuration/outputs/claude-code-prompt.md) walks you through a guided attempt; this step differs because you are the one holding the specification. Ask for a `train` function and a held-out evaluation that satisfy the gate and pass your tests, then run your tests on what it returns, yourself.

Do three things with the result. First, note which of your tests failed, if any. A failing test is often a gap in your gate that Claude could not see because it had only what you wrote. If it adds early stopping you never asked for, your stop rule had a hole. Second, compare its implementation with your baseline and name one difference in behavior: whether it keeps the held-out points out of training, how it computes the average, whether it records more than two losses. Third, ask Claude to propose a deliberately wrong version that still passes your tests, and check by hand whether it does. If it does, your test list was too weak, and you found out cheaply. Whether your tests are enough cannot be judged by the system they are testing. Preserve the actual transcript: your prompt, the plan, the diff, the commands, and the outputs, with the date and displayed model label. If a session failed or did not run, record that rather than substituting a fixture.

The second task touches Claude's behavior, and it is the place to apply the one-object-at-a-time test from Part 1. Prepare a baseline prompt, a few-shot prompt, and a retrieved-context condition on the same bounded task, and change only one object between conditions. Write your prediction for each first. If you run them, record the actual responses, interface, date, and displayed model label; if you do not, label the design proposed. In either case, state that these conditions change inputs, not Claude's weights.

## Ship It: the comparison report and its sign-off

The [artifact brief](../lessons/09-training-and-configuration/outputs/artifact-brief.md) asks for loss history, before and after parameters, held-out results, and a comparison of parameter learning, prompt changes, and context changes. Preserve the training data and evaluation points. Record the interpreter, step count, rate, initial values, final values, and threshold, and say which results came from the lesson and which from your extension. Add a table with mutable object, mechanism, persistence, evidence, and remaining limits, keeping permissions and tools separate from model parameters. End with one predictive claim supported by your actual toy evaluation and one intervention claim it does not establish, so the report separates mathematical success from decision authority.

**The sign-off.** The last thing the report says is a statement you could put your name to. Claude can draft its words in seconds, and the draft will be fluent, so write it from your record. As in Chapter 2, a pass names the obligation it passed, and no more. This is the template, not a signature:

```text
Sign-off — training versus context report
Checked:      which claims, by which of my own checks (first update by hand,
              finite difference, held-out evaluation, one-object-at-a-time
              comparison)
How:          by hand / by a test I wrote before reading the reference /
              by recomputation / with Claude's help (say which parts)
Not checked:  data beyond the four training and four held-out fixtures; other
              rates, step counts, or starts; calibration of the probabilities;
              any change to Claude itself; any real-world effect of changing x
Not claiming: that the model generalizes, that lower training loss means
              better, that any input causes any outcome
Signed or withheld: ____________  (name, date)
```

Choose the verbs to match the evidence. "Lowered the objective on four pairs" describes what the optimizer did. "Learned" describes a parameter change, and that is accurate here. "Generalizes" needs a criterion you have not run, and "causes" needs assumptions the fixture cannot supply. The "Not checked" line does the work, because it is the one an AI-written sign-off omits: the system that wrote it has no record of what you did not do. If your evidence does not support signing, withholding is an honest result.

### The driver's seat

This is how the chapter's work divided, task by task. Test your own record against it.

| Task | Claude should | You should | Why it stays with you |
| --- | --- | --- | --- |
| Derivation, notation, and the loop | Derive the gradient, write the update, run it, tabulate the output | Reproduce the first step by hand and by finite difference | You cannot audit an update you have never computed |
| Objective, held-out set, stop rule | Challenge them; propose the wrong version that slips through | Write them, first | "Better" is a judgment about the task, and the data hold no opinion |
| Which object changed | List candidates, diff the files, replay the conditions | Choose the object you may change, and run the one-at-a-time test | The change is yours to own and to reverse |
| Prediction or intervention | Draft a diagram, list confounders, compute under a stated model | Decide which kind of question it is; justify the assumptions; get domain evidence | The assumptions are not in the data, and you are the one who acts |
| What the result supports | Flag an overclaim | Choose the verb and sign | Your name is on the claim |

Record in the report one task you delegated and one judgment you retained. If you cannot point to the transcript line or the edit that shows each, the split happened in your head and not in the record.

## Verify and reflect

Run the demo, the lesson tests, your gradient check, and the held-out calculation. Recompute the first update independently, and preserve exact outputs rather than reconstructing them after reading the expected values. Check every use of "history" and "generalization." Two loss values are initial and final, not a full curve. Four designed points are separate fixtures, not evidence of population performance.

Then take four proposed changes, say a rewritten system prompt, a new document in a workspace, a newly enabled tool, and a lowered temperature, and classify each by the object it modifies. For each, say how you would observe the change. If the only evidence is a different output, do not jump to a claim about changed weights. Finally, inspect your strongest causal verb. Did the experiment show association or intervention? Narrow the claim if the data and design cannot support it.

The most useful reflection is local. Which distinction did you originally collapse? Training and context? Lower loss and better? Held-out and representative? Prediction and intervention? Name the calculation or the one-object test that separated them again. Mechanism labels should make evidence easier to inspect; when they hide the mutable object they have become branding. Ask of any change which component changed, who changed it, and what evidence records the transformation. If those stay unanswered, use a narrower description until the mechanism is known.

## Assessments — ungraded practice

These Assessments carry no points. Use the paired lesson's [knowledge check](../lessons/09-training-and-configuration/quiz.json), preserving initial answers before explanations. Write predictions before execution.

### Warm-up

1. **Sigmoid at zero — introductory; objective: calculate a prediction.** Derive one-half from the formula and verify it. Write your prediction first.
2. **Initial loss — introductory; objective: interpret the objective.** Calculate binary loss at probability one-half for each label and explain the average.
3. **Gradient signs — introductory; objective: trace an update.** Complete the four-row error table and predict the direction of w and b before you check.

### Application

4. **One update — intermediate; objective: implement gradient descent.** Reproduce weight `0.15` at rate `0.2`, recording every sum and average. Then write the version that sums instead of averaging, and name the lesson tests that cannot tell the two apart.
5. **Finite difference — intermediate; objective: independently check a gradient.** Approximate the origin gradient and compare within a stated tolerance. State one thing this check would not catch.
6. **Reverse labels — intermediate; objective: predict parameter behavior.** Reverse labels, predict the learned weight sign, then run the bounded experiment.
7. **Separate evaluation — intermediate; objective: assess held-out behavior.** List your evaluation points before training, evaluate them, and state exactly what the result supports.

### Synthesis

8. **Mechanism table — advanced; objective: distinguish system changes.** Compare training, prompting, few-shot examples, retrieval, tools, permissions, and settings by mutable object and evidence. For one pair of rows, design the one-object-at-a-time test that would show which of them caused a behavior change.
9. **Leakage record — advanced; objective: critique evaluation and conduct against a gate.** Add evaluation points to training, explain how their role changes, and redesign the evidence split. Rewrite your gate so the split is stated before training, give it to Claude Code without your implementation, and report which of your tests its version failed, if any.

### Challenge

10. **Loss versus usefulness — stretch; objective: evaluate an objective.** Construct a case where lower training loss does not answer a separate task requirement. State the missing metric and write it into the gate as a second objective.
11. **Prediction versus intervention — stretch; objective: defend a boundary.** Write one supported predictive claim and one unsupported causal claim about a labeled hypothetical application. Name the assumptions needed for the latter, and say who could supply each.

## What you can now explain

You can calculate a sigmoid prediction, stable logistic loss, analytic gradient, and parameter update, and reproduce the first-step values by two routes, the derivative and a finite difference. You can distinguish initial and final training loss from a held-out result, say why four constructed points do not establish real-world generalization, and notice when evaluation data have stopped being held out because they guided a choice. You can trace what changed: training updates learned parameters, prompts, context, tools, permissions, and inference settings change other parts of a system, and behavioral change alone does not identify the mechanism.

And you can say what the three jobs look like at this scale. You conducted: you wrote the change, the objective, the held-out list, and the stop rule before the loop ran, and tested Claude's version against them. You checked: you wrote "training loss decreased" when that was all you measured, and let neither persistence nor a good-looking prompt stand in for training. You drove: you handed Claude the algebra and the loop, kept the question of whether this was a prediction problem or an intervention problem, and signed or withheld.

## Now specify what should change

Once we distinguish mutable objects, we can plan a bounded change without hiding behind fluent prose. Chapter 10 builds a plan with objectives, exclusions, dependencies, evidence, and stopping conditions—and then passes meaningless strings through its structural validator to show why required fields are not enough.

## Irreducibly Human

The relevant companion passage distinguishes predictive association from intervention questions. See [Prediction and intervention](../docs/irreducibly-human.md#prediction-and-intervention). We use its information boundary, not a claim that a particular machine architecture can never represent causal reasoning.

**AI should** inspect calculations, run bounded experiments, tabulate predictions, and challenge assumptions. It can compute consequences under an explicitly stated model, propose candidate confounders, and help draft an evaluation plan, and it should label its assumptions as assumptions instead of presenting a plausible story as established causation.

**Human should** decide whether the task asks for prediction or intervention, justify the outcome and causal assumptions, obtain relevant domain evidence, and own the decision to act. Human intuition is not sufficient causal proof either.

Ask one more question of your intervention claim: what would have to be true about how these data were produced for it to hold? Write the claim with its provisos, in the form "if I change x by doing D, the outcome changes by about this much, provided P, Q, and R." If you can fill in P, Q, and R, you have found the assumptions to defend and the evidence to go and get. If you cannot, you have a prediction. Record the split in the existing report: one predictive claim supported by the executed fixture and one intervention claim it does not establish. Explain why changing x in the fitted Python function measures the model's response, not necessarily the effect of changing a real-world variable, and point to the transcript line or the edit showing that you, not Claude, wrote the sentence that names the assumptions.
