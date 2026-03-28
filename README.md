# EvalSmith

<p align="center">
  <img src=".github/readme/evalsmith-hero-web.png" alt="EvalSmith forensic evaluation workflow banner" width="100%">
</p>

<p align="center">
  Grounded forensic evaluation for prompts, context, retrieval, tools, and multi-stage LLM workflows.
</p>

EvalSmith is an open-source coding-agent skill for grounded prompt and workflow evaluation inside real LLM product repositories.

The canonical direct-install skill package lives at `skills/evalsmith/`.
The repository root is also packaged as a Claude Code plugin and marketplace.

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
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
├── SKILL.md
├── agents/
│   └── openai.yaml
├── .github/
│   ├── readme/
│   │   └── evalsmith-hero-web.png
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── marketplace-readiness.md
│   └── plans/
├── examples/
│   └── claude-settings.evalsmith.json
├── PRD.md
├── README.md
├── references/
│   ├── artifact-contract.md
│   ├── evalsmith-method.md
│   ├── forensic-analysis.md
│   └── research-foundations.md
├── scripts/
│   ├── bootstrap_evalsmith.py
│   ├── install_evalsmith.py
│   └── validate_packaged_skill.py
├── skills/
│   └── evalsmith/
│       ├── SKILL.md
│       ├── agents/
│       ├── references/
│       └── scripts/
└── tests/
    ├── test_bootstrap_evalsmith.py
    └── test_install_evalsmith.py
```

## Install

### Claude Code Marketplace

Recommended install path:

```text
/plugin marketplace add gangj277/EvalSmith
/plugin install evalsmith@evalsmith
```

This repo publishes a marketplace named `evalsmith` and a plugin named `evalsmith`.
After install, Claude Code can auto-invoke the skill when the task matches, and you can explicitly test it with `/evalsmith:evalsmith`.
The repository is also prepared for Anthropic's official plugin submission flow. Details and the submission links are in [docs/marketplace-readiness.md](docs/marketplace-readiness.md).

### Codex

Native public install path:

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
python "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo gangj277/EvalSmith \
  --path skills/evalsmith
```

Clone-based fallback:

```bash
python scripts/install_evalsmith.py --target codex
```

This installs the packaged skill into `~/.codex/skills/evalsmith`.
This repository does not claim a public Codex marketplace listing; the native verified path is GitHub skill installation.

### Claude Code

If you want a direct standalone skill install instead of the marketplace plugin:

```bash
python scripts/install_evalsmith.py --target claude
```

This installs the packaged skill into `~/.claude/skills/evalsmith`.

Claude Code also supports project-local skills at `.claude/skills/<skill-name>/SKILL.md` and personal skills at `~/.claude/skills/<skill-name>/SKILL.md`. This repo packages the exact folder you would copy there: `skills/evalsmith/`.
For local plugin development, you can also point Claude Code directly at this repo root:

```bash
claude --plugin-dir /path/to/EvalSmith
```

For team-wide rollout, start from [examples/claude-settings.evalsmith.json](examples/claude-settings.evalsmith.json) and merge it into your repository's `.claude/settings.json`.

## Use

Example invocation:

```text
Use $evalsmith to inspect this repo's LLM feature, create the right eval plan, scaffold repo-native evals, and propose evidence-backed prompt fixes.
```

If you want a starter artifact layout in a target repository after installation:

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

This repository now supports two distribution paths for the same EvalSmith capability:

- direct GitHub skill installation from `skills/evalsmith/` for Codex and standalone Claude skills
- Claude Code marketplace installation from the repo-level `.claude-plugin/marketplace.json`

That keeps the packaging native to both platforms without pretending they share the same marketplace model.
