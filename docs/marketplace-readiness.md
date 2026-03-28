# EvalSmith Marketplace Readiness

EvalSmith is packaged for two different distribution surfaces because Claude Code and Codex do not expose the same install model today.

## Claude Code

Claude Code distributes shared extensions as plugins, not raw skill folders.
The live marketplace package for EvalSmith is:

- plugin manifest: `.claude-plugin/plugin.json`
- marketplace catalog: `.claude-plugin/marketplace.json`
- plugin payload: repo root with `skills/evalsmith/`

### Current public install flow

```text
/plugin marketplace add gangj277/EvalSmith
/plugin install evalsmith@evalsmith
```

Explicit invocation after install:

```text
/evalsmith:evalsmith
```

### Team rollout

If you want a repository to prompt teammates to install the marketplace and enable EvalSmith by default, start from `examples/claude-settings.evalsmith.json` and merge it into `.claude/settings.json`.

### Official Anthropic marketplace submission

The self-hosted marketplace above is already live. Listing in Anthropic's official marketplace is a separate manual step done through Anthropic's in-app submission forms:

- Claude.ai: `https://claude.ai/settings/plugins/submit`
- Console: `https://platform.claude.com/plugins/submit`

### Validation checklist

Run before every release:

```bash
claude plugin validate .
python scripts/validate_packaged_skill.py
python /Users/gangjimin/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/evalsmith
python -m unittest discover -s tests -v
```

Release discipline:

- keep `.claude-plugin/plugin.json` on semantic versioning
- update `.claude-plugin/marketplace.json` when the published plugin ref changes
- tag the repo with the plugin version for stable marketplace installs

## Codex

Codex currently has a native GitHub skill installation path for `SKILL.md` packages. EvalSmith is already shaped for that path at `skills/evalsmith/`.

Recommended public install command:

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
python "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo gangj277/EvalSmith \
  --path skills/evalsmith
```

This repository does not claim a public Codex marketplace listing because that is not a distribution surface I can verify from current official OpenAI documentation. The native, verified path is GitHub skill installation.
