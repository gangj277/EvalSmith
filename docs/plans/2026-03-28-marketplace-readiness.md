# Marketplace Readiness Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make EvalSmith submission-ready for the official Claude Code marketplace flow while documenting the real native install path for Codex.

**Architecture:** Keep the repo root as the Claude plugin and marketplace root, keep `skills/evalsmith/` as the Codex-ready skill payload, and add submission/readiness documentation plus team-install examples that match current platform behavior instead of inventing unsupported marketplace mechanics.

**Tech Stack:** Claude plugin manifests, marketplace metadata, Markdown docs, Python validation, `unittest`

---

### Task 1: Encode the current platform constraints

**Files:**
- Create: `docs/marketplace-readiness.md`
- Modify: `README.md`

**Step 1: Document Claude’s real install and submission flow**

Cover:
- plugin install unit vs bare skill folders
- `/plugin marketplace add` and `/plugin install`
- in-app submission forms for the official Anthropic marketplace
- local validation with `claude plugin validate .`

**Step 2: Document Codex’s real distribution model**

Cover:
- GitHub skill install from `skills/evalsmith/`
- no public Codex marketplace claim unless verified

### Task 2: Tighten plugin metadata and team rollout guidance

**Files:**
- Modify: `.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`
- Create: `examples/claude-settings.evalsmith.json`
- Modify: `tests/test_install_evalsmith.py`
- Modify: `scripts/validate_packaged_skill.py`

**Step 1: Improve metadata**

Add richer author metadata and validate semver/version consistency.

**Step 2: Add team rollout example**

Provide an example `.claude/settings.json` snippet with `extraKnownMarketplaces` and enabled plugin configuration.

**Step 3: Extend tests and validator**

Verify the new metadata fields and example file exist.

### Task 3: Verify and publish

**Files:**
- Modify: `.github/workflows/ci.yml` only if verification coverage changes

**Step 1: Run validation**

Run:
- `claude plugin validate .`
- `python scripts/validate_packaged_skill.py`
- `python /Users/gangjimin/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/evalsmith`
- `python -m unittest discover -s tests -v`

**Step 2: Publish**

Commit with a neutral message, push to `main`, and report the live install commands.
