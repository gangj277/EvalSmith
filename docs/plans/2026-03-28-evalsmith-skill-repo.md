# EvalSmith Skill Repo Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Turn `EvalSmith/` into an OSS-ready GitHub repository containing a research-backed Codex skill for grounded LLM prompt and workflow evaluation.

**Architecture:** Keep the repository root as the skill root so the project is immediately publishable and directly invokable. Combine a concise `SKILL.md`, compact research references, and one deterministic bootstrap script that scaffolds eval artifacts into a target repo.

**Tech Stack:** Markdown, YAML, Python 3 standard library, `unittest`, Git

---

### Task 1: Scaffold The Repository

**Files:**
- Create: `README.md`
- Create: `LICENSE`
- Create: `.gitignore`
- Create: `agents/openai.yaml`
- Modify: `PRD.md`

**Step 1: Define the public repo contract**

Document the repository as:
- a publishable GitHub repo
- a Codex skill rooted at repository top-level
- a research-backed implementation of the PRD

**Step 2: Create the repo metadata files**

Add:
- `README.md` with positioning, usage, and repo layout
- `LICENSE` with a permissive OSS license
- `.gitignore` for Python and macOS noise
- `agents/openai.yaml` with display metadata and a default invocation prompt

**Step 3: Verify repository structure**

Run: `find . -maxdepth 2 -type f | sort`
Expected: repo metadata files appear alongside `SKILL.md`, `references/`, `scripts/`, and `tests/`

### Task 2: Author The Skill

**Files:**
- Create: `SKILL.md`
- Create: `references/research-foundations.md`
- Create: `references/evalsmith-method.md`
- Create: `references/artifact-contract.md`

**Step 1: Write the skill contract**

`SKILL.md` must:
- describe exactly when `$evalsmith` should trigger
- define the operating sequence from workflow analysis through optimization
- enforce evidence-first behavior and anti-slop guardrails
- point to reference files only when needed

**Step 2: Capture research-backed guidance**

`references/research-foundations.md` should summarize primary-source findings on:
- task-specific eval design
- trace or stage-level grading
- LLM-as-judge reliability and its limits
- automated prompt optimization methods and failure modes
- RAG-specific evaluation decomposition

**Step 3: Define durable artifact contracts**

`references/artifact-contract.md` should specify the recommended `/evals/...` tree and the required sections for workflow maps, specs, cases, rubrics, and reports.

### Task 3: Build Deterministic Bootstrap Tooling

**Files:**
- Create: `tests/test_bootstrap_evalsmith.py`
- Create: `scripts/bootstrap_evalsmith.py`

**Step 1: Write the failing test**

Test that the bootstrap script creates:
- `evals/workflows/<slug>.md`
- `evals/specs/<slug>.yaml`
- `evals/cases/<slug>/cases.jsonl`
- `evals/rubrics/<slug>.md`
- `evals/reports/.gitkeep`
- `evals/runs/.gitkeep`

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_bootstrap_evalsmith.py -v`
Expected: FAIL because `scripts/bootstrap_evalsmith.py` does not exist yet

**Step 3: Write minimal implementation**

Implement a standard-library CLI that:
- accepts `target_dir`, `--feature-name`, `--slug`, and `--workflow-type`
- creates the eval directory layout
- writes starter templates
- refuses to overwrite files unless `--force` is supplied

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_bootstrap_evalsmith.py -v`
Expected: PASS

### Task 4: Validate The Skill

**Files:**
- Verify: `SKILL.md`
- Verify: `agents/openai.yaml`
- Verify: `scripts/bootstrap_evalsmith.py`
- Verify: `tests/test_bootstrap_evalsmith.py`

**Step 1: Validate the skill metadata**

Run: `python /Users/gangjimin/.codex/skills/.system/skill-creator/scripts/quick_validate.py .`
Expected: validation passes

**Step 2: Run the unit tests**

Run: `python -m unittest discover -s tests -v`
Expected: PASS

**Step 3: Inspect git status**

Run: `git status --short`
Expected: only intended new files are present
