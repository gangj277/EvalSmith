---
name: evalsmith
description: Grounded forensic evaluation engineering for LLM product repositories. Use when a coding agent needs to inspect an existing codebase, infer the workflow behind a prompt feature, structured output flow, RAG pipeline, tool-calling path, or simple multi-stage chain, then design repo-native evals, capture exact traces, attribute behaviors to prompt or context components, and propose evidence-backed prompt or workflow improvements.
---

# EvalSmith

## Overview

Turn prompt iteration into a grounded evaluation loop inside the repository that actually ships the feature.

Do not optimize prompts from intuition alone. First understand the workflow, then define what good looks like, then create or run evals, then diagnose the failures, and only then propose changes.

## Non-Negotiables

1. Ground every claim in repository evidence, runnable results, or an explicit assumption.
2. Evaluate the workflow, not only the final answer. Prompts, retrieval, tools, parsers, and intermediate transforms are all valid failure surfaces.
3. Prefer the simplest reliable grader. Use code-based checks first, then calibrated LLM grading, then human review when nuance demands it.
4. Keep artifacts human-auditable and easy to edit by hand.
5. Do forensic attribution before optimization. Do not jump from aggregate benchmark scores to prompt edits.
6. Recommend the smallest high-confidence change set before suggesting broad rewrites.
7. Reuse existing fixtures, tests, schemas, and logs before inventing synthetic infrastructure.

## Forensic Standard

An EvalSmith run is not complete when it has only produced a benchmark score. It is only complete when it can explain, with evidence, which parts of the current system are producing which behaviors.

Minimum forensic protocol:

1. Capture exact traces for each evaluated case.
   Store the assembled system prompt, user input, few-shot examples, retrieved context, tool schemas, tool calls, tool outputs, intermediate model outputs when available, and final parsed result.
2. Build a component inventory.
   Assign stable IDs to atomic prompt clauses, context blocks, examples, tool descriptions, and post-processing constraints.
3. Read all failing cases end-to-end.
   Do not rely only on aggregate metrics or cluster labels.
4. Read a contrast sample of passing cases.
   You need contrastive evidence, not only failures.
5. Write explicit causal hypotheses.
   Example: `SP3 causes over-refusal when paired with retrieval chunk class C2`.
6. Run controlled manipulations.
   Use ablations, substitutions, re-orderings, or context swaps that change one meaningful component at a time while holding the rest fixed as much as the stack allows.
7. Separate correlation from causal evidence.
   A repeated co-occurrence is not enough by itself.
8. Do not patch until the evidence threshold is met.

Evidence threshold for a “high-confidence” optimization:

- supported by multiple benchmark cases, not one anecdote
- backed by exact trace inspection
- strengthened by at least one controlled manipulation or comparison
- checked against a counterexample or non-failing contrast case
- rerun on the same benchmark slice after the change

## Operating Sequence

### 1. Scope the feature

- Identify the user-facing LLM feature the request is about.
- Find the likely entrypoints: routes, services, prompts, adapters, tests, fixtures, schemas, and docs.
- State the probable product intent and any unresolved assumptions.
- If the repo has multiple candidate workflows, rank them and explain which one you are optimizing first.

### 2. Build a workflow map

- Trace inputs, intermediate transforms, model calls, retrieval, tool calls, structured outputs, and output contracts.
- Identify where nondeterminism enters the system.
- Mark evaluation surfaces at both the stage level and the final-output level.
- Build a component inventory for prompt clauses, context sources, examples, tool descriptions, and parser constraints.
- Use [references/artifact-contract.md](references/artifact-contract.md) for the required workflow report sections.

### 3. Design the eval plan

- Define success criteria that are specific, measurable, and relevant to the feature.
- Choose a benchmark mix that includes happy-path, edge, adversarial, ambiguity, and regression cases.
- Choose grading methods in this order:
  - Code or schema checks for deterministic requirements
  - Rule-based assertions for constrained semantics
  - LLM-as-judge only for nuanced judgment with explicit rubrics and calibration
  - Human review for high-stakes or unresolved disagreement
- Decide what exact trace data must be persisted so later forensic attribution is possible.
- Design ablation and counterfactual tests before running the first serious benchmark.
- Load [references/research-foundations.md](references/research-foundations.md) when deciding tradeoffs.
- Load [references/evalsmith-method.md](references/evalsmith-method.md) when writing the plan.
- Load [references/forensic-analysis.md](references/forensic-analysis.md) when you need the attribution protocol.

### 4. Scaffold repo-native artifacts

- Prefer a lightweight `/evals/` tree over a new framework.
- Keep file names tied to the feature slug.
- If the target repo has no eval structure yet, use `python scripts/bootstrap_evalsmith.py <target-repo> --feature-name "<Feature Name>" --workflow-type <type>` to create a first-pass layout.
- Adapt the generated files to the repo’s stack instead of forcing a generic harness.

### 5. Execute and record results

- Run the smallest eval slice that can falsify the current approach.
- Record case-level outputs, aggregate scores, failure buckets, and latency or cost when relevant.
- Persist exact traces so you can reconstruct how every output was produced.
- Repeat stochastic calls when variance matters.
- Preserve before/after comparability by keeping the benchmark slice fixed across iterations.

### 6. Diagnose failures structurally

- Group failures by type before editing prompts.
- Read every failing case and at least a representative sample of passing cases.
- Build an influence ledger mapping components to observed behaviors and confidence levels.
- Distinguish:
  - prompt wording failures
  - context assembly failures
  - retrieval failures
  - tool selection or tool argument failures
  - parser or schema failures
  - stochastic instability
- Explain which stage is most likely responsible and what evidence supports that judgment.

### 7. Run attribution tests

- Use one-component-at-a-time ablations where possible.
- Use pairwise differential reruns to compare current and manipulated traces on the same cases.
- Use context substitutions or chunk removals for RAG when prompt text alone is not the real cause.
- Reject optimization ideas that are only weakly correlated with the failure.

### 8. Propose optimizations

- Tie every recommendation to observed failure patterns.
- Prefer interventions in this order:
  - clarify success criteria or rubrics
  - fix context assembly or retrieval pollution
  - tighten output contracts and schema checks
  - improve instruction ordering and constraint wording
  - add or replace few-shot examples
  - split overloaded prompts into stages
- For each proposed change, state:
  - target component IDs
  - expected causal mechanism
  - evidence supporting the change
  - downside risk
- Do not claim a change helped unless the same eval slice was rerun.

### 9. Apply patches only when trust is earned

- Recommendation-first is the default mode.
- Auto-patching is opt-in for low-risk, auditable changes.
- If you patch, rerun the benchmark slice and compare the same metrics.
- If the patch alters more than one causal hypothesis at once, call that out and lower confidence.

## Required Artifacts

Each serious EvalSmith run should leave behind:

- a workflow analysis report
- an eval plan or spec
- benchmark cases
- rubric definitions
- a component inventory
- an ablation or counterfactual plan
- exact or near-exact trace artifacts
- a forensic analysis report
- a run report
- a comparison report if a prior run exists
- an optimization proposal

Follow the exact contracts in [references/artifact-contract.md](references/artifact-contract.md).

## Anti-Patterns

- Do not start with “improve the prompt” before understanding the repo.
- Do not hide uncertainty. State assumptions explicitly.
- Do not rely on one generic score for a multi-stage system.
- Do not use judge-only evals when deterministic checks are available.
- Do not confuse benchmark generation with benchmark validity.
- Do not make causal claims from aggregate benchmark deltas alone.
- Do not collapse all context into one opaque block. Componentize it.
- Do not ship “prompt improvements” that were never isolated against counterfactuals or reruns.
- Do not let the eval become a dashboard exercise detached from the codebase.

## Reference Loading Guide

- Read [references/research-foundations.md](references/research-foundations.md) when you need evidence for method choices.
- Read [references/evalsmith-method.md](references/evalsmith-method.md) when you need the detailed repo-analysis, eval-design, diagnosis, and optimization playbook.
- Read [references/forensic-analysis.md](references/forensic-analysis.md) when you need the attribution-first workflow.
- Read [references/artifact-contract.md](references/artifact-contract.md) when you are creating or reviewing eval artifacts.
