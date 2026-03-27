# EvalSmith

<p align="center">
  <img src=".github/readme/evalsmith-hero-web.png" alt="EvalSmith forensic evaluation workflow banner" width="100%">
</p>

<p align="center">
  Grounded forensic evaluation for prompts, context, retrieval, tools, and multi-stage LLM workflows.
</p>

EvalSmith is an open-source coding-agent skill for grounded prompt and workflow evaluation inside real LLM product repositories.

Instead of giving generic prompt advice, EvalSmith is designed to help an agent:

- inspect the repository and infer the real LLM workflow
- map evaluation surfaces across prompts, retrieval, tools, and output contracts
- scaffold repo-native eval artifacts
- run or wire up a benchmark loop
- diagnose failures by stage
- perform attribution-driven forensic analysis across traces, prompt clauses, context blocks, tools, and parsers
- propose evidence-backed prompt or workflow changes

## Why This Exists

Most teams still improve LLM features with ad hoc prompt edits and a few manual spot checks. That breaks down once the feature depends on retrieval, tools, structured outputs, or multi-stage orchestration.

EvalSmith exists to make prompt iteration look more like engineering:

1. Understand the workflow.
2. Define what good looks like.
3. Scaffold runnable evals.
4. Run them.
5. Diagnose failures.
6. Change the system with evidence.

For serious workflows, that means more than a benchmark score. EvalSmith is designed to force:

- exact trace capture
- component inventories for prompts and context
- controlled ablations and counterfactual reruns
- component-to-behavior attribution ledgers
- optimization only after the attribution evidence is strong enough

## Repository Layout

```text
.
├── SKILL.md
├── PRD.md
├── agents/
│   └── openai.yaml
├── .github/
│   ├── readme/
│   │   └── evalsmith-hero-web.png
│   └── workflows/
│       └── ci.yml
├── docs/
│   └── plans/
├── references/
│   ├── artifact-contract.md
│   ├── evalsmith-method.md
│   ├── forensic-analysis.md
│   └── research-foundations.md
├── scripts/
│   └── bootstrap_evalsmith.py
└── tests/
    └── test_bootstrap_evalsmith.py
```

## Quick Start

Use the repository root as the skill root.

Example invocation:

```text
Use $evalsmith to inspect this repo's LLM feature, create the right eval plan, scaffold repo-native evals, and propose evidence-backed prompt fixes.
```

If you want a starter artifact layout in a target repository:

```bash
python scripts/bootstrap_evalsmith.py /path/to/target-repo \
  --feature-name "Support Copilot" \
  --workflow-type rag
```

That command creates a first-pass `/evals/` tree with workflow, spec, cases, rubric, reports, and runs placeholders.
It also scaffolds forensic artifacts for component inventory, ablation planning, traces, and attribution reports.

## Research Basis

EvalSmith is grounded in primary sources rather than prompt folklore. The bundled references synthesize:

- OpenAI eval design, graders, and trace grading guidance
- Anthropic evaluation design guidance
- APE, OPRO, Self-Refine, DSPy, and TextGrad
- G-Eval and MT-Bench / Chatbot Arena judge reliability work
- Ragas for retrieval-augmented generation evaluation
- ProSA for prompt sensitivity
- Context-faithful Prompting for context adherence

See [references/research-foundations.md](references/research-foundations.md).

## Status

This repository currently packages the first OSS-ready skill definition, method references, bootstrap tooling, and README visuals for the EvalSmith concept described in [PRD.md](PRD.md).
