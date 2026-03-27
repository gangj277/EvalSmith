#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/artifact-contract.md",
    "references/evalsmith-method.md",
    "references/forensic-analysis.md",
    "references/research-foundations.md",
    "scripts/bootstrap_evalsmith.py",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the packaged EvalSmith skill folder."
    )
    parser.add_argument(
        "skill_dir",
        nargs="?",
        default="skills/evalsmith",
        help="Path to the packaged skill directory.",
    )
    return parser.parse_args()


def validate_frontmatter(skill_md: Path) -> list[str]:
    errors: list[str] = []
    text = skill_md.read_text()

    if not text.startswith("---\n"):
        return ["SKILL.md must start with YAML frontmatter delimited by ---"]

    try:
        _, frontmatter, _ = text.split("---\n", 2)
    except ValueError:
        return ["SKILL.md frontmatter must contain opening and closing --- markers"]

    if "name:" not in frontmatter:
        errors.append("SKILL.md frontmatter must include name")
    if "description:" not in frontmatter:
        errors.append("SKILL.md frontmatter must include description")
    if "name: evalsmith" not in frontmatter:
        errors.append("SKILL.md frontmatter name must be evalsmith")
    return errors


def main() -> int:
    args = parse_args()
    skill_dir = Path(args.skill_dir).resolve()

    errors: list[str] = []
    if not skill_dir.exists():
        errors.append(f"skill directory does not exist: {skill_dir}")
    else:
        for relative_path in REQUIRED_FILES:
            full_path = skill_dir / relative_path
            if not full_path.exists():
                errors.append(f"missing required file: {full_path}")

        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            errors.extend(validate_frontmatter(skill_md))

    if errors:
        print("Packaged skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Packaged skill is valid: {skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
