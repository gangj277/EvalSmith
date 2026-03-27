# EvalSmith Forensic Analysis Protocol

Use this file when the task requires attribution, not just evaluation.

## Objective

Determine which specific parts of the current pipeline are producing which behaviors, with enough evidence to justify a prompt, context, retrieval, tool, or parser change.

## What Counts As Forensic Analysis

Forensic analysis is not:

- reading aggregate benchmark scores
- clustering failures without reading traces
- giving generic prompt advice
- editing multiple prompt sections at once and hoping scores improve

Forensic analysis is:

1. capturing exact traces
2. decomposing the system into atomic components
3. reading failures case-by-case
4. contrasting them against passes
5. testing causal hypotheses with controlled manipulations
6. recording confidence and uncertainty explicitly

## Required Inputs

- workflow map
- eval spec
- benchmark cases
- exact or near-exact traces
- component inventory
- rubric results

If trace capture is incomplete, state the missing fields and lower confidence.

## Componentization Rules

Do not treat “the prompt” as one blob.

Componentize at least:

- role framing
- task objective
- guardrails and refusal policy
- formatting instructions
- ranking priorities
- few-shot examples
- retrieved chunks or context classes
- tool descriptions
- tool parameter schemas
- parser or post-processing constraints

Give each component a stable ID.

## Case Reading Workflow

For each failure:

1. read the user input
2. read the assembled system prompt
3. read all injected context
4. read tool schemas, calls, and outputs
5. read the final output and parsed output
6. mark the exact point where behavior diverges from the intended contract
7. tag the likely responsible components

Then read a contrast sample of passes with similar inputs.

Questions to answer:

- What did the model have available at the moment it failed?
- Which instruction or context block likely dominated the outcome?
- Which relevant signal was present but ignored?
- Which irrelevant signal may have overpowered the correct one?
- Would a smaller change isolate the issue better than a full rewrite?

## Attribution Ladder

Use the strongest applicable evidence:

1. trace correlation
2. repeated correlation across similar cases
3. contrastive evidence from passing cases
4. controlled one-component ablation
5. controlled one-component rewrite or substitution
6. rerun on the same slice after the fix

Do not describe level 1 or 2 evidence as proof.

## Controlled Manipulation Patterns

### Prompt clause ablation

- remove one clause
- rerun same cases
- observe whether the failure disappears, improves, worsens, or remains unchanged

### Context ablation

- remove one retrieved chunk class or metadata block
- hold the rest fixed

### Context substitution

- swap in a more relevant or conflicting context block
- test whether behavior follows the context or ignores it

### Order-only change

- keep instruction content constant
- change ordering only
- test priority effects

### Example swap

- replace one few-shot example while keeping instruction text stable
- test anchoring effects

## Confidence Labels

Use one of:

- `low`: correlation only or incomplete trace capture
- `medium`: repeated pattern plus contrastive evidence
- `high`: repeated pattern plus controlled manipulation or rerun evidence

Never use `high` without either ablation evidence or same-slice rerun evidence.

## Optimization Gate

A production-ready recommendation must satisfy all of:

- exact component IDs are named
- expected mechanism is stated
- supporting cases are listed
- a counterexample check was performed
- downside risk is stated
- the rerun plan is defined

## Output Format

The final forensic report should include:

1. benchmark slice
2. failure clusters
3. component influence ledger
4. ablation evidence
5. high-confidence recommendations
6. low-confidence ideas intentionally rejected
