#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
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
        description="Validate the packaged EvalSmith distribution artifacts."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to the repository root or packaged skill directory.",
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


def resolve_repo_and_skill(path: Path) -> tuple[Path | None, Path]:
    if (path / "skills" / "evalsmith" / "SKILL.md").exists():
        return path, path / "skills" / "evalsmith"

    if (path / "SKILL.md").exists() and (path / "agents" / "openai.yaml").exists():
        if path.name == "evalsmith" and path.parent.name == "skills":
            return path.parents[1], path
        return None, path

    return path, path / "skills" / "evalsmith"


def validate_skill_dir(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    if not skill_dir.exists():
        return [f"skill directory does not exist: {skill_dir}"]

    for relative_path in REQUIRED_FILES:
        full_path = skill_dir / relative_path
        if not full_path.exists():
            errors.append(f"missing required file: {full_path}")

    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        errors.extend(validate_frontmatter(skill_md))

    return errors


def load_json(path: Path) -> tuple[dict[str, object] | None, list[str]]:
    try:
        return json.loads(path.read_text()), []
    except FileNotFoundError:
        return None, [f"missing required file: {path}"]
    except json.JSONDecodeError as exc:
        return None, [f"invalid JSON in {path}: {exc}"]


def validate_plugin_manifest(repo_root: Path) -> tuple[list[str], dict[str, object] | None]:
    manifest_path = repo_root / ".claude-plugin" / "plugin.json"
    manifest, errors = load_json(manifest_path)
    if manifest is None:
        return errors, None

    if manifest.get("name") != "evalsmith":
        errors.append(f"{manifest_path} name must be evalsmith")

    for field in ["description", "version", "homepage", "repository", "license"]:
        if field not in manifest:
            errors.append(f"{manifest_path} must include {field}")

    return errors, manifest


def validate_marketplace(repo_root: Path, manifest: dict[str, object] | None) -> list[str]:
    marketplace_path = repo_root / ".claude-plugin" / "marketplace.json"
    marketplace, errors = load_json(marketplace_path)
    if marketplace is None:
        return errors

    if marketplace.get("name") != "evalsmith":
        errors.append(f"{marketplace_path} name must be evalsmith")

    owner = marketplace.get("owner")
    if not isinstance(owner, dict) or "name" not in owner:
        errors.append(f"{marketplace_path} must include owner.name")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        errors.append(f"{marketplace_path} must include at least one plugin entry")
        return errors

    first_plugin = plugins[0]
    if not isinstance(first_plugin, dict):
        errors.append(f"{marketplace_path} first plugin entry must be an object")
        return errors

    if first_plugin.get("name") != "evalsmith":
        errors.append(f"{marketplace_path} plugin name must be evalsmith")
    if first_plugin.get("source") != "./":
        errors.append(f"{marketplace_path} plugin source must be ./")

    if manifest is not None and first_plugin.get("version") != manifest.get("version"):
        errors.append(
            f"{marketplace_path} plugin version must match .claude-plugin/plugin.json"
        )

    return errors


def main() -> int:
    args = parse_args()
    path = Path(args.path).resolve()
    repo_root, skill_dir = resolve_repo_and_skill(path)

    errors = validate_skill_dir(skill_dir)
    if repo_root is not None:
        plugin_errors, manifest = validate_plugin_manifest(repo_root)
        errors.extend(plugin_errors)
        errors.extend(validate_marketplace(repo_root, manifest))

    if errors:
        print("Packaged skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    if repo_root is not None:
        print(f"Packaged skill and Claude marketplace are valid: {repo_root}")
    else:
        print(f"Packaged skill is valid: {skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
