#!/usr/bin/env python3
"""Install SKILL.md-bearing folders from a repo into ~/.claude/skills/.

Discovers every top-level folder under the given repo that contains a
SKILL.md with valid YAML frontmatter (name + description), and installs
each one into the Claude skills directory as either a symlink (default,
so `git pull` in the repo updates installed skills in place) or a copy.

Idempotent: existing targets are skipped unless --force is passed.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Literal

import yaml  # pip install pyyaml

InstallMode = Literal["symlink", "copy"]
Action = Literal["linked", "copied", "replaced", "skipped"]


@dataclass(frozen=True)
class SkillSource:
    """A folder on disk that contains a valid SKILL.md."""

    path: Path
    name: str
    description: str


@dataclass(frozen=True)
class InstallResult:
    skill: SkillSource
    target: Path
    action: Action


def _parse_frontmatter(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError("missing YAML frontmatter")
    try:
        _, frontmatter, _ = text.split("---", 2)
    except ValueError as exc:
        raise ValueError("unterminated frontmatter block") from exc
    data = yaml.safe_load(frontmatter) or {}
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a mapping")
    return data


def _is_nested_skill(skill_md: Path, root: Path) -> bool:
    """True if skill_md lives inside another SKILL.md's folder tree."""
    ancestor = skill_md.parent.parent
    while ancestor != root and ancestor != ancestor.parent:
        if (ancestor / "SKILL.md").exists():
            return True
        ancestor = ancestor.parent
    return False


def discover_skills(root: Path) -> Iterator[SkillSource]:
    for skill_md in sorted(root.rglob("SKILL.md")):
        if _is_nested_skill(skill_md, root):
            continue
        try:
            fm = _parse_frontmatter(skill_md)
            name = str(fm["name"]).strip()
            description = str(fm["description"]).strip()
        except (KeyError, ValueError) as exc:
            print(f"skip  {skill_md.relative_to(root)}: {exc}", file=sys.stderr)
            continue
        if not name or not description:
            print(
                f"skip  {skill_md.relative_to(root)}: empty name/description",
                file=sys.stderr,
            )
            continue
        yield SkillSource(path=skill_md.parent, name=name, description=description)


def install(
    skill: SkillSource,
    dest_root: Path,
    *,
    mode: InstallMode,
    force: bool,
) -> InstallResult:
    target = dest_root / skill.name
    existed = target.exists() or target.is_symlink()
    if existed and not force:
        return InstallResult(skill, target, "skipped")
    if existed:
        if target.is_symlink() or target.is_file():
            target.unlink()
        else:
            shutil.rmtree(target)
    if mode == "symlink":
        target.symlink_to(skill.path.resolve(), target_is_directory=True)
    else:
        shutil.copytree(skill.path, target)
    return InstallResult(skill, target, "replaced" if existed else mode_to_action(mode))


def mode_to_action(mode: InstallMode) -> Action:
    return "linked" if mode == "symlink" else "copied"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path, help="Path to a cloned skills repo")
    parser.add_argument(
        "--dest",
        type=Path,
        default=Path.home() / ".claude" / "skills",
        help="Claude skills directory (default: ~/.claude/skills)",
    )
    parser.add_argument(
        "--mode",
        choices=("symlink", "copy"),
        default="symlink",
        help="symlink (default) tracks the repo on git pull; copy is portable",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing skills with the same name",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List what would happen without touching the filesystem",
    )
    args = parser.parse_args(argv)

    repo: Path = args.repo.resolve()
    if not repo.is_dir():
        print(f"error: {repo} is not a directory", file=sys.stderr)
        return 2

    dest: Path = args.dest
    if not args.dry_run:
        dest.mkdir(parents=True, exist_ok=True)

    skills = list(discover_skills(repo))
    if not skills:
        print(f"no skills found under {repo}")
        return 0

    results: list[InstallResult] = []
    for skill in skills:
        if args.dry_run:
            print(f"would  {skill.name:<30}  <-  {skill.path.relative_to(repo)}")
            continue
        result = install(skill, dest, mode=args.mode, force=args.force)
        results.append(result)
        print(f"{result.action:<8} {skill.name:<30}  {skill.path.relative_to(repo)}")

    if not args.dry_run:
        summary = {
            action: sum(1 for r in results if r.action == action)
            for action in ("linked", "copied", "replaced", "skipped")
        }
        kept = ", ".join(f"{k}={v}" for k, v in summary.items() if v)
        print(f"\ndone -> {dest}  ({kept})")
    return 0


if __name__ == "__main__":
    sys.exit(main())