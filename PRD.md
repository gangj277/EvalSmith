
---

# PRD: Coding-Agent Skill for Grounded Prompt Evaluation and Optimization

## 1. Product Overview

We are building an open-source **coding-agent-native skill** that helps developers debug and improve prompt-driven LLM features inside real products.

The skill is designed to be invoked by coding agents operating directly in a codebase. Instead of merely suggesting generic prompt improvements, it will:

* inspect the repository and infer the LLM workflow
* identify prompts, system instructions, tool flows, and evaluation surfaces
* generate a benchmark and testing strategy grounded in the product’s actual behavior
* install or scaffold the necessary evaluation infrastructure
* run evaluations against the current implementation
* analyze failures by stage, not just by final output
* propose concrete prompt and workflow changes backed by measured findings

This product turns prompt engineering from a manual, intuition-heavy process into a more rigorous engineering loop.

In simple terms:

> The coding agent should be able to enter an LLM product repo and say:
> “I understand how this feature works, I created the right eval plan, I ran it, here is where it fails, and here are the highest-leverage changes to improve it.”

---

## 2. Problem

Teams building LLM products routinely write long, complicated prompts and multi-step workflows, but they lack a systematic way to improve them.

Today, the workflow usually looks like this:

* change the prompt
* manually test a few examples
* hope the behavior improved
* accidentally regress something else
* repeat

This is painful for several reasons.

First, prompts are rarely isolated. They live inside larger workflows involving retrieval, formatting, tool usage, state management, and output parsing. When the behavior degrades, teams often do not know whether the problem is the prompt itself, the surrounding scaffolding, the examples, the retrieval context, or the evaluation criteria.

Second, evaluation is underspecified. Teams often do not know:

* what “good” means for this feature
* how to generate representative test cases
* how to score outputs consistently
* how to catch regressions before shipping

Third, the debugging process is expensive in human time. The hardest part is not merely running a model. It is defining the benchmark, designing the test strategy, interpreting the failures, and deciding what to change next.

Coding agents are now capable enough to help with implementation work, but they still lack a **reliable skill for prompt/system evaluation engineering**.

That gap is the product.

---

## 3. Product Thesis

The most valuable thing we can build is not a generic “prompt optimizer.”

It is a **skill for coding agents that converts prompt and workflow iteration into a grounded, repeatable evaluation loop**.

The product wins if it can do five things well:

1. **Understand the workflow**
   It must infer how the LLM feature actually operates in the repository.

2. **Create the right evaluation plan**
   It must propose meaningful benchmarks, failure modes, and scoring criteria based on the workflow and product intent.

3. **Set up runnable infrastructure**
   It must scaffold the necessary eval files, fixtures, configs, and runners directly into the codebase.

4. **Diagnose failures with structure**
   It must identify where the system is breaking and why.

5. **Recommend high-confidence improvements**
   It must propose prompt and workflow changes tied to measured outcomes, not intuition.

---

## 4. Product Definition

### Product type

An open-source **skill/package/instructional runtime** for coding agents.

### Primary environment

* Claude Code
* Codex-style coding agents
* agentic coding environments that can inspect files, edit code, run commands, and produce artifacts

### Core function

Enable a coding agent to perform **workflow-aware eval engineering** for LLM features.

### What it is not

* not a Chrome extension
* not a no-code prompt playground
* not a generic dashboard product
* not a pure SaaS observability platform
* not a fake “automatic best prompt generator”

---

## 5. Target Users

### Primary users

Engineers and technical founders building products that contain:

* prompt-based features
* RAG flows
* tool-calling flows
* agentic workflows
* structured generation features
* classification or recommendation steps powered by LLMs

### Secondary users

* AI product engineers
* applied AI teams
* startups shipping LLM features quickly
* OSS builders who want to improve their prompt quality systematically

### User context

These users already have:

* a repository
* some LLM feature that “kind of works”
* frustration around iteration speed, regression risk, and evaluation ambiguity

---

## 6. Jobs to Be Done

When a developer invokes this skill inside a repo, they want the coding agent to:

* understand how this LLM feature works
* identify the relevant prompts and workflow stages
* propose what should be tested and how
* generate eval cases and rubric definitions
* wire those evals into the project
* run the evals against the current implementation
* explain where the failures are coming from
* recommend prompt or workflow changes with evidence
* optionally implement the changes and rerun the evaluation

---

## 7. Product Principles

### 1. Grounded over magical

The system should never pretend to know the “best prompt” abstractly. It should reason from the actual repository, workflow, and observed failures.

### 2. Workflow-aware, not prompt-only

The product must treat prompts as part of a larger execution system.

### 3. Evidence before optimization

Prompt recommendations should come after benchmark definition and evaluation results, not before.

### 4. Coding-agent-native

Everything should be designed so an agent can inspect, scaffold, run, compare, and patch with minimal friction.

### 5. Human-auditable

All generated eval plans, rubrics, and changes must be visible and editable by humans.

### 6. Incremental adoption

The first useful outcome should arrive quickly, even if the repository is messy or incomplete.

---

## 8. Core User Flow

### Flow A: Repo analysis

The user asks the coding agent to improve an LLM feature.
The skill scans the repository and identifies:

* where prompts live
* where model calls are made
* how inputs are transformed
* what the outputs are expected to do
* whether there are tool calls, retrieval, memory, or structured outputs
* where existing tests or fixtures already exist

**Output:** a workflow map plus a recommended evaluation plan.

### Flow B: Benchmark and rubric generation

The skill generates:

* representative benchmark cases
* failure mode categories
* eval criteria
* assertions and rubrics
* optional judge prompts for nuanced scoring
* baseline metrics to track

**Output:** machine-readable eval spec files committed into the repo.

### Flow C: Harness setup

The skill scaffolds:

* eval config
* fixture directories
* adapters for the relevant LLM function or route
* runner scripts
* report generation

**Output:** a runnable local evaluation harness.

### Flow D: Execution

The skill runs the benchmark and produces:

* pass/fail results
* rubric scores
* cost and latency measurements where relevant
* failure clustering
* regression comparison if prior runs exist

**Output:** report artifacts plus actionable diagnosis.

### Flow E: Optimization

The skill proposes prompt and workflow changes, explains why they are likely to help, optionally patches the code, and reruns the evaluation.

**Output:** measured before/after improvement loop.

---

## 9. Functional Requirements

## 9.1 Repository and Workflow Understanding

The skill must be able to:

* inspect the codebase for model invocation points
* detect prompt templates, system prompts, few-shot examples, and prompt assembly logic
* identify workflow type:

  * single-call prompt feature
  * structured output generation
  * RAG pipeline
  * tool-calling flow
  * multi-stage agentic flow
* locate relevant APIs, functions, tests, and sample inputs
* infer probable user-facing intent from code, docs, comments, schemas, and endpoint names

The system should produce a **workflow map** that identifies:

* input sources
* intermediate transformations
* model calls
* tools or retrieval layers
* output contracts
* likely evaluation surfaces

---

## 9.2 Evaluation Strategy Synthesis

The skill must generate an evaluation strategy tailored to the workflow.

This includes:

* what to test
* what good looks like
* what typical failures matter
* what benchmark distribution is needed
* which stages need direct evaluation

It should support:

* exact-match assertions
* schema/format correctness checks
* rule-based assertions
* rubric-based scoring
* LLM-as-judge scoring where appropriate
* pairwise comparisons
* regression testing against prior prompt versions
* stage-level evaluation for multi-step workflows

It should also categorize likely failure modes, for example:

* instruction-following failure
* hallucination or unsupported claim
* over-verbosity or under-specification
* tone mismatch
* compliance/policy deviation
* retrieval misuse
* tool misuse
* formatting or schema breakage

---

## 9.3 Benchmark Generation

The skill must be able to create benchmark datasets from available context.

Sources may include:

* existing fixtures
* logs or stored examples if available
* docs and product specs
* hardcoded examples in code
* API contracts
* generated edge cases derived from workflow analysis

Benchmark cases should support labels such as:

* happy path
* edge case
* adversarial case
* ambiguity case
* safety/compliance case
* regression case

Each case should include:

* input
* expected properties
* scoring method
* optional rationale
* optional tags for filtering

---

## 9.4 Harness Scaffolding

The skill must scaffold infrastructure into the repository, such as:

* `/evals/specs/...`
* `/evals/cases/...`
* `/evals/rubrics/...`
* `/evals/reports/...`
* runner scripts
* config files
* adapters to call the relevant feature entrypoint

The scaffolding should be lightweight, understandable, and easy to modify manually.

The skill should prefer adding infrastructure that feels native to the repo’s stack rather than imposing a rigid framework.

---

## 9.5 Evaluation Execution

The skill must run evaluations and produce structured outputs.

Minimum outputs:

* case-level results
* aggregate score summary
* category breakdown
* failure clusters
* regression comparison
* prompt/version comparison
* optional cost and latency statistics

The runner should support:

* local execution
* repeated sampling for stochasticity analysis
* versioned result artifacts
* filtering by benchmark tag
* deterministic replay where possible

---

## 9.6 Failure Interpretation

This is one of the most important features.

The skill must interpret results in a way that is useful to engineers. It should not just say “score dropped.”

It should explain:

* what kinds of cases are failing
* which stage appears responsible
* whether the issue is prompt wording, context assembly, retrieval pollution, tool misuse, or output formatting
* whether failures are systematic or stochastic
* which metrics are most concerning
* what change is most likely to improve results with minimal downside

---

## 9.7 Prompt and Workflow Optimization Proposals

The skill should propose changes such as:

* prompt restructuring
* better instruction ordering
* clearer constraints
* better few-shot examples
* more explicit output contracts
* decomposition of a single large prompt into staged prompts
* retrieval filtering or context restructuring
* stage-specific assertions
* fallback handling for common failure patterns

Important: these should be **proposals backed by observed evidence**, not generic advice.

In MVP, changes should be recommendation-first.
Auto-patching can be supported as an optional mode.

---

## 10. Skill Interface

The skill should expose a clean agent-facing interface. The exact syntax may vary by coding agent, but conceptually the skill should support the following operations:

### `analyze_workflow`

Scans the repo and produces a workflow map plus candidate eval surfaces.

### `propose_eval_plan`

Generates a recommended benchmark and scoring strategy.

### `scaffold_evals`

Creates the necessary specs, fixtures, configs, and runners.

### `run_evals`

Executes the benchmark and stores results.

### `interpret_results`

Analyzes failures and summarizes the likely causes.

### `propose_optimizations`

Suggests grounded prompt or workflow improvements.

### `apply_patch_and_rerun`

Optionally edits the prompt/workflow and reruns evaluations.

This interface should feel like a **capability skill**, not merely a library.

---

## 11. System Architecture

The product should consist of the following logical components.

### A. Repo Analyzer

Understands the codebase structure and finds LLM-related workflows.

### B. Workflow Modeler

Builds an internal representation of the feature pipeline and identifies evaluation surfaces.

### C. Eval Planner

Generates benchmark strategy, metrics, rubrics, and failure mode hypotheses.

### D. Spec Generator

Writes machine-readable eval specs and fixture templates.

### E. Runner Adapters

Connects the eval system to the actual feature implementation inside the repo.

### F. Result Analyzer

Clusters failures, compares runs, and identifies likely root causes.

### G. Optimization Engine

Produces recommended prompt/workflow changes based on observed results.

### H. Report Generator

Outputs human-readable markdown and machine-readable JSON reports for the agent and developer.

---

## 12. Output Artifacts

Each run should leave behind durable artifacts in the repo.

Minimum artifacts:

* workflow analysis report
* eval plan
* benchmark case files
* rubric definitions
* run report
* comparison report against prior runs
* optimization proposal report

These artifacts are important because they make the skill auditable, forkable, and collaborative in open-source settings.

---

## 13. MVP Scope

The MVP should focus on a narrow but powerful slice.

### In scope

* identify prompt/model call sites in common code patterns
* generate a workflow map
* create a first-pass eval plan
* scaffold benchmark spec files
* support small benchmark execution
* produce pass/fail and rubric summary
* interpret results
* recommend prompt edits

### Initially supported workflow types

* single prompt feature
* structured output generation
* RAG-like single retrieval + generation workflow
* simple multi-stage prompt chains

### Out of scope for MVP

* full autonomous optimization loops without review
* deep support for arbitrary multi-agent graphs
* production observability ingestion
* hosted dashboard
* enterprise collaboration features

---

## 14. Success Metrics

### Product effectiveness

* time from invocation to first runnable eval harness
* percentage of repos where the skill successfully identifies the primary workflow
* percentage of recommended eval plans accepted with minor edits
* measurable quality lift after one optimization cycle
* reduction in manual prompt iteration time

### OSS adoption

* stars
* forks
* benchmark/example contributions
* integrations with major coding-agent workflows
* number of external repositories using generated eval structure

### Quality of trust

* low rate of obviously wrong workflow inference
* high editability of generated artifacts
* low perception of “AI slop” in reports and proposals

---

## 15. Risks

### 1. Overclaiming intelligence

If the skill pretends it understands the repo perfectly when it does not, trust collapses.

### 2. Generic eval slop

If the generated eval plans look like shallow boilerplate, the product loses credibility.

### 3. Framework lock-in

If the harness feels too opinionated or invasive, adoption will drop.

### 4. Prompt-only thinking

If the skill ignores retrieval, tools, or workflow composition, it will diagnose the wrong problem.

### 5. No measurable loop

If it cannot show before/after evidence, it becomes just another advisory tool.

---

## 16. Key Design Decisions

### Decision 1: Skill-first, not UI-first

The primary product surface is the coding agent’s capability, not a dashboard.

### Decision 2: Repository-grounded analysis

All reasoning begins from the codebase and surrounding artifacts.

### Decision 3: Evaluation artifacts live in the repo

This is essential for transparency, versioning, and collaboration.

### Decision 4: Recommendation-first optimization

The system should earn trust before taking autonomous patching actions.

### Decision 5: Workflow-aware evaluation

Evaluation should attach to the actual execution chain, not just final outputs.

---

## 17. Example Positioning

A strong positioning sentence for the open-source project is:

> An open-source coding-agent skill that turns prompt and agent workflow iteration into a grounded evaluation loop.

A sharper, more GitHub-friendly version is:

> Your coding agent can now inspect an LLM feature, generate the right eval harness, run it, diagnose failures, and propose prompt fixes backed by evidence.

---

## 18. Final Product Definition

This project should be understood as:

**a coding-agent-native eval engineering skill for LLM products**

It is not merely a prompt optimizer.
It is not merely an eval framework.
It is not merely a testing library.

It is the layer that lets coding agents do the hard part of LLM improvement work:

* understand the workflow
* define what should be tested
* build the evaluation infrastructure
* run the tests
* interpret the failures
* improve the prompt or workflow based on grounded findings

That is the product.

---