# Claude Marketplace Packaging Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Package EvalSmith as a Claude Code marketplace plugin while preserving the existing Codex installable skill layout.

**Architecture:** Keep `skills/evalsmith/` as the Codex-ready skill package, add a repo-level Claude marketplace catalog at `.claude-plugin/marketplace.json`, and add a plugin package under `plugins/evalsmith/` that contains its own `.claude-plugin/plugin.json` plus a plugin-local `skills/` tree and supporting references/scripts. Extend validation and tests to cover both distributions.

**Tech Stack:** Markdown skill packaging, JSON plugin manifests, Python installer/validation scripts, `unittest`, GitHub Actions

---

### Task 1: Inspect current packaging and define the Claude plugin source of truth

**Files:**
- Modify: `README.md`
- Modify: `scripts/install_evalsmith.py`
- Modify: `scripts/validate_packaged_skill.py`
- Test: `tests/test_install_evalsmith.py`

**Step 1: Record the packaging contract**

Document that:
- `skills/evalsmith/` remains the direct-install skill for Codex
- `plugins/evalsmith/` becomes the Claude marketplace plugin root
- `.claude-plugin/marketplace.json` becomes the marketplace catalog

**Step 2: Run existing verification before refactor**

Run: `python -m unittest discover -s tests -v`
Expected: current tests pass before edits start

### Task 2: Add Claude marketplace structure

**Files:**
- Create: `.claude-plugin/marketplace.json`
- Create: `plugins/evalsmith/.claude-plugin/plugin.json`
- Create: `plugins/evalsmith/skills/evalsmith/SKILL.md`
- Create: `plugins/evalsmith/skills/evalsmith/agents/openai.yaml`
- Create: `plugins/evalsmith/skills/evalsmith/references/artifact-contract.md`
- Create: `plugins/evalsmith/skills/evalsmith/references/evalsmith-method.md`
- Create: `plugins/evalsmith/skills/evalsmith/references/forensic-analysis.md`
- Create: `plugins/evalsmith/skills/evalsmith/references/research-foundations.md`
- Create: `plugins/evalsmith/skills/evalsmith/scripts/bootstrap_evalsmith.py`

**Step 1: Create the marketplace catalog**

Add a valid Claude marketplace manifest that points to `./plugins/evalsmith`.

**Step 2: Create the plugin manifest**

Add a minimal but production-ready `.claude-plugin/plugin.json` with name, description, version, author, repository, homepage, and license metadata.

**Step 3: Copy the skill package into the plugin**

Mirror the EvalSmith skill files inside `plugins/evalsmith/skills/evalsmith/` so Claude installs a self-contained plugin without outside path dependencies.

### Task 3: Extend install and validation tooling

**Files:**
- Modify: `scripts/install_evalsmith.py`
- Modify: `scripts/validate_packaged_skill.py`
- Test: `tests/test_install_evalsmith.py`

**Step 1: Add plugin-aware validation**

Teach the validation script to verify:
- `skills/evalsmith/` contains the canonical skill assets
- `.claude-plugin/marketplace.json` exists
- `plugins/evalsmith/.claude-plugin/plugin.json` exists
- plugin-local skill files are present

**Step 2: Decide installer scope**

Keep direct skill installation for Codex and standalone Claude skills. Do not replace it with plugin installation, but update help text and README to distinguish direct install from marketplace install.

**Step 3: Add tests**

Add tests for marketplace and plugin package integrity alongside existing install tests.

### Task 4: Update user-facing docs and verify

**Files:**
- Modify: `README.md`
- Modify: `.github/workflows/ci.yml` if needed

**Step 1: Document Claude marketplace installation**

Add the official install flow:
- `/plugin marketplace add gangj277/EvalSmith`
- `/plugin install evalsmith@evalsmith`

**Step 2: Clarify naming and invocation**

Explain that Claude marketplace installs a plugin, while Codex installs the raw skill folder.

**Step 3: Run full verification**

Run:
- `python scripts/validate_packaged_skill.py`
- `python -m unittest discover -s tests -v`

Expected: validation passes and all tests pass.
