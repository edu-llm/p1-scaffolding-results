# Worked Examples With Faded Scaffolds

Source: Research context assembled for this experiment.

## Definition

Worked examples with faded scaffolds show a complete, step-by-step solved problem instead of an unsolved one and then gradually strip steps out across a problem sequence.
The learner receives less handholding over time.

## Evidence

### Sweller and Cooper (1985) and Sweller (1988)

The origin study found that algebra students who studied fully worked solutions learned faster than students who solved problems unaided.
They also performed better on transfer problems, ruling out a simple memorization explanation.
The theory is that novices working toward a fixed goal must keep the current state, goal state, gap between them, and a subgoal stack in working memory simultaneously.
That process overloads working memory.

Sweller's PRISM model offered a computational account of the load difference.
A goal-specific solver for a three-step problem needed four productions, five cycles, and 29 conditions matched.
A nonspecific goal solver needed one production, three cycles, and 17 conditions matched.
This is a concrete measure of how much less machinery goal-free solving requires.

In a key dual-task experiment with 24 trigonometry students, goal-specific and goal-free groups solved the main task equally well and equally quickly.
The goal-free group recalled significantly more structural problem elements afterward, without an advantage on irrelevant details.
This supports the interpretation that freed capacity is spent building a schema.

### Barbieri et al. Meta-analysis

This meta-analysis combined 55 studies and 181 results selected from more than 8,000 candidates to test whether worked examples outperform solving alone in mathematics.
Its headline effect was g = 0.48 with a 95% confidence interval from 0.36 to 0.60.
The analysis used robust variance estimation to avoid overcounting studies that reported multiple correlated effects.
It checked publication bias using a funnel plot and Egger's test, finding some bias.
Trim-and-fill correction barely changed the estimate from 0.48 to 0.44.
The fail-safe N was approximately 13,915 hidden null studies, which would be required to erase the result and is implausibly large.

The average conceals substantial genuine variation, with I² = 93.7%.
Correct-only examples beat incorrect or mixed-correctness examples.
Self-explanation prompts hurt rather than helped, likely because they elicited shallow self-explanations or repetition.
Timing, such as a new topic versus practice, did not matter.

The evidence does not fully transfer directly to P1.
The comparisons are across studies rather than from a single controlled experiment, so they are suggestive rather than causal proof of a particular design choice.
The outcomes are test accuracy, not token or compute efficiency.
There is no dosage curve for the amount of worked-example exposure.
The expected baseline is a real-world effect around g = 0.48, but P1 should directly measure token efficiency, dosage scaling, and isolated design choices.

### Xwin-Math and GAIR-Abel

This is an LLM-specific comparison of step-by-step chain-of-thought solutions against terse final-answer-only responses.
The core lever is the quantity of step-by-step data.
Starting from real GSM8K and MATH training questions, GPT-4 Turbo generated new questions with a verification pass that solved and checked each question before it was retained.
It then generated a full worked chain-of-thought solution for each question.

Scaling from 7.5K real examples to 960K synthetic GSM8K examples and 480K synthetic MATH examples moved LLaMA-2 7B from 50.2% to 82.6% on GSM8K and from 8.4% to 40.6% on MATH.
The reported results showed no sign of saturation at the tested scales.
The paper distinguishes Pass@256, whether a correct answer appears in any of 256 samples and therefore a ceiling-capability measure, from PassRatio@256, the fraction of the 256 generations that are correct and therefore a reliability measure.
Scaling worked-solution data mostly improved reliability.
The capability ceiling was already high with little data.
In other words, more worked examples made the model more consistently correct rather than enabling it to solve entirely new harder problems.
The paper decomposes errors into reasoning versus calculation errors and finds that calculation errors are corrected faster than reasoning errors as data scales.

### Understanding the Effect of Noise in LLM Training Data with Algorithmic Chains of Thought (arXiv:2402.04004)

The authors fine-tuned a pretrained Pythia 410M model on 20,000 synthetic arithmetic and median problems.
The direct arm learned from final answers only.
The algorithmic chain-of-thought arm learned from verified intermediate states and final answers.

| Task | Final answer only | Verified algorithmic trace |
| --- | ---: | ---: |
| Five-digit multiplication | 39.6% | 90.7% |
| Ten-number median | 30.6% | 97.0% |
| Mixed arithmetic | 60.4% | 95.8% |

### Distilling Algorithmic Reasoning from LLMs via Explaining Solution Programs

This experiment operates in algorithmic programming.
An Explainer annotates explanations from a problem and solution pair.
A Reasoner learns to reason from problem and explanation pairs.
A Coder implements the solution from the reasoning.
The Explainer is a frontier model, GPT-4.
The Reasoner can be a closed model, GPT-3.5-Turbo, or an open model, DeepSeek Coder 7B.
The Coder is the same model as the Reasoner without fine-tuning.

## Current Evidence Assessment

### Strong findings

- Sweller and Cooper showed that worked examples benefit transfer as well as memorization.
- There is a plausible, quantified mechanism in cognitive-load and working-memory conservation.
- PRISM provides a concrete accounting: 4 productions, 5 cycles, and 29 condition matches for a goal-directed solver versus 1, 3, and 17 for a goal-free solver.
- The dual-task recall experiment indicates that freed capacity is spent on structural schema elements rather than irrelevant surface detail.
- The Barbieri meta-analysis gives a replicated, medium effect with g ≈ 0.48 and a confidence interval clearly above zero.
- The result survives publication-bias correction and has a high fail-safe N.
- Xwin-Math and GAIR-Abel provide a direct LLM-specific scaling result for step-by-step worked solutions.
- The Xwin-Math evidence is closest in this bundle to direct evidence that the effect can transfer to LLM training corpora.

### Conflicts and issues

- The human literature disagrees about supplementary design features.
- The Barbieri meta-analysis found self-explanation prompts harmful on average, with β = −0.24, despite other literature suggesting self-explanation can help.
- The high I² = 93.7% indicates that much of this variation is genuine rather than sampling noise.
- The mechanism does not cleanly match between human and LLM evidence.
- Sweller's account is about freed working memory enabling schema building, while Xwin-Math frames its result as higher PassRatio@256 rather than higher Pass@256.
- It is unclear whether human schema building and LLM reliability improvement are the same phenomenon or distinct mechanisms that look similar in benchmark outcomes.
- The importance of correctness and fading specifically is unresolved.
- The meta-analysis supports correct-only examples over incorrect or mixed examples, but this evidence bundle does not isolate faded scaffolds against static worked examples at equal data volume.
- The evidence supports worked examples generally and makes fading a plausible learning analogy, but does not prove fading as an independent lever.

### Weak evidence

- There is no dosage-response curve that identifies whether returns are linear, log-linear, or plateau at a scale relevant to a 1B model.
- Xwin-Math only establishes no saturation at the studied scale, not where saturation begins.
- Neither the human evidence nor Xwin-Math measures the token or compute efficiency that P1 uses as its currency.
- Fading itself is untested in the cited bundle.
- Error-type decomposition was measured under chain-of-thought volume scaling, not a fading manipulation.
- The error decomposition is a metric template, not evidence about fading.

## Hypotheses

### Null hypothesis

At a fixed total continued-pretraining token budget, complete or faded worked solutions produce the same held-out problem-solving accuracy as bare problem-answer pairs, which can fit more distinct problems and repetitions into the same budget.

### Alternative hypothesis

At the same fixed token budget, complete and/or faded worked solutions produce higher held-out accuracy than bare problem-answer pairs.
This is the claim that depth beats breadth per token.

## Proposed Experiment

Continually pretrain an early checkpoint on matched procedural or mathematics problem families.
Each family shares an underlying skill.
Split trainable and held-out instances by family in the same manner used by the QA augmentation lever's Ptrain and Ptest split.

### Main arms

1. **Bare problem-answer pairs, control.**
   Each training document contains a problem followed only by its final answer, with no intermediate steps or general expository text.
2. **Complete worked solutions.**
   Each training document contains a problem, a complete step-by-step solution, and its final answer.
3. **Ordered faded completions.**
   Each problem family appears repeatedly under a preregistered sequence of decreasing scaffold lengths.
   The shown scaffold is context, and the omitted continuation is the training target.
4. **Shuffled-fade control.**
   This arm uses the same problem instances, scaffold-length multiset, and loss masking as Arm 3.
   It randomizes scaffold lengths within each family instead of presenting them from most to least support.

All arms use the same preregistered problem-family roster and the same trainable and held-out split.
For Arms 2, 3, and 4, each family appears the same preregistered number of times under the same distinct-instance policy.
Arm 2 presents complete solutions on those appearances.
Arm 3 applies the fixed fading schedule.
Arm 4 presents the identical scaffold-length multiset in randomized within-family order.

### Training-data validation

Validate worked solutions and scaffolds before continual pretraining.
Where a deterministic or symbolic verifier is available, verify every final answer and intermediate step.
For items that cannot be automatically checked, conduct a preregistered, blinded audit sampled across problem families and scaffold lengths.
Validate that every shown scaffold is a correct prefix of the complete solution and that its omitted continuation completes the same valid solution.
Regenerate or remove every failing example before main training runs.

### Coverage versus compute

The same problem families, problem counts, and held-out/trainable split are used across arms.
This holds coverage fixed, not compute.
Worked solutions contain substantially more tokens per problem than bare answers.
Using the same problems and counts would cause worked-solution arms to run longer if every arm traversed its full problem set once.

Match compute by assigning every arm the same fixed total token budget, such as equal training steps multiplied by batch size.
The bare-answer arm uses its budget by cycling through more distinct real problems and/or repetitions from the same pool used by the solution arms.
Do not pad it with filler text.
Mixing unrelated exposition would confound lack of steps with content type and prevent attribution of any difference to the intended intervention.
The bare-answer arm will naturally encounter more distinct problems and/or repetitions during the fixed budget.
This is expected because coverage is not the matched resource.

Log every arm's accuracy as a curve across training, checkpointed at regular token intervals.
This tests efficiency by estimating both final accuracy at the common budget and tokens needed to reach target levels.

## What to Measure

### Primary metric

Measure unscaffolded accuracy on held-out problem instances from trained-on families.
At evaluation, provide only the bare problem and no supplied steps or scaffold.
Score each item as the fraction of N sampled generations that are correct by verifier checking or exact match.
This tests whether worked examples or fading help models solve new instances without continued assistance.

### Secondary metrics

1. **Transfer.**
   Measure accuracy on problem families never seen in training.
   This distinguishes schema learning from surface pattern matching and is the LLM analog of Sweller and Cooper's transfer test.
2. **Ceiling versus reliability.**
   Sample N generations for each held-out problem.
   Report Pass@N, whether any generation is correct, and PassRatio@N, the fraction correct.
   This separates solving harder problems from producing correct answers more consistently.
3. **Error type.**
   Classify incorrect answers as reasoning versus calculation errors.
   This tests whether a gain reduces reasoning failures rather than only arithmetic slip-ups.

## Decision Rules

Reject the null if Arm 2 and/or Arm 3 beats Arm 1 with non-overlapping 95% confidence intervals.
Only conclude that fading adds value if Arm 3 beats Arm 2.
Beating Arm 1 alone is insufficient to establish a fading effect.
Calculate confidence intervals by bootstrapping the held-out set 1,000 times per arm.
Treat arms as significantly different only when their 95% confidence intervals do not overlap.

## Follow-up Experiment if the Null Is Rejected

If Arm 2 and/or Arm 3 beats bare-answer control, sweep fading schedules to identify the best pace.

1. Fast fading removes steps after 1-2 exposures.
2. Slow fading removes steps gradually over many exposures.
3. Fixed 50% steps permanently shows half the steps without further fading.

The schedule with the best held-out accuracy wins.
This step is required because neither the human literature nor the cited LLM literature establishes an optimal fading pace.

## Success Criteria for the Fading Schedule Sweep

1. The schedule matches or beats the best main-experiment result.
   Its accuracy is not statistically significantly worse than the best single Arm 2 or Arm 3 result.
2. The schedule uses the same token budget.
   It uses no more solution tokens per problem family than Arm 2, so any gain comes from pacing rather than additional content.
3. The mechanism is more than reliability alone.
   It shows a real shift in Pass@N or in reasoning-error rate, not solely in PassRatio@N.
