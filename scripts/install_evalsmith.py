#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_SOURCE = REPO_ROOT / "skills" / "evalsmith"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Install the packaged EvalSmith skill into a Codex or standalone Claude Code skills directory. "
            "For Claude marketplace installation, use the repo's plugin marketplace instead."
        )
    )
    parser.add_argument(
        "--target",
        required=True,
        choices=["codex", "claude", "both"],
        help="Which direct-install client to install the skill for.",
    )
    parser.add_argument(
        "--dest-base",
        help="Base home directory to install under. Defaults to the current user's home directory.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing installation.",
    )
    return parser.parse_args()


def destination_roots(dest_base: Path, target: str) -> list[Path]:
    mapping = {
        "codex": dest_base / ".codex" / "skills" / "evalsmith",
        "claude": dest_base / ".claude" / "skills" / "evalsmith",
    }
    if target == "both":
        return [mapping["codex"], mapping["claude"]]
    return [mapping[target]]


def ensure_installable() -> None:
    required = [
        SKILL_SOURCE / "SKILL.md",
        SKILL_SOURCE / "agents" / "openai.yaml",
        SKILL_SOURCE / "references" / "forensic-analysis.md",
        SKILL_SOURCE / "scripts" / "bootstrap_evalsmith.py",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        joined = "\n".join(f"- {path}" for path in missing)
        raise FileNotFoundError(f"packaged skill is incomplete:\n{joined}")


def install_one(destination: Path, force: bool) -> None:
    if destination.exists():
        if not force:
            raise FileExistsError(f"destination already exists: {destination}")
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SKILL_SOURCE, destination)


def main() -> int:
    args = parse_args()
    base = Path(args.dest_base).expanduser().resolve() if args.dest_base else Path.home()

    try:
        ensure_installable()
        for destination in destination_roots(base, args.target):
            install_one(destination, force=args.force)
            print(destination)
    except (FileNotFoundError, FileExistsError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
