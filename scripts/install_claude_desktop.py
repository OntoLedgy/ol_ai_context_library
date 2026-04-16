#!/usr/bin/env python3
"""Package every SKILL.md-bearing folder in a repo as an uploadable .zip.

For each discovered skill, produces <out>/<skill-name>.zip whose archive
root is the skill folder itself (the layout Claude Desktop's
Customize > Skills uploader expects).

Stdlib only: no PyYAML, no third-party deps. Frontmatter is parsed just
enough to extract `name` and `description` for validation.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


# --- Types ------------------------------------------------------------------

@dataclass(frozen=True)
class SkillSource:
    path: Path
    name: str
    description: str


@dataclass(frozen=True)
class PackageResult:
    skill: SkillSource
    archive: Path


# --- Frontmatter ------------------------------------------------------------

_KV = re.compile(r"^\s*([A-Za-z_][\w-]*)\s*:\s*(.+?)\s*$")


def _strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def _read_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError("missing frontmatter")
    rest = text[3:]
    end = rest.find("\n---")
    if end < 0:
        raise ValueError("unterminated frontmatter block")
    fields: dict[str, str] = {}
    for line in rest[:end].splitlines():
        match = _KV.match(line)
        if match:
            fields[match.group(1)] = _strip_quotes(match.group(2))
    return fields


# --- Discovery --------------------------------------------------------------

def _is_nested(skill_md: Path, root: Path) -> bool:
    ancestor = skill_md.parent.parent
    while ancestor != root and ancestor != ancestor.parent:
        if (ancestor / "SKILL.md").exists():
            return True
        ancestor = ancestor.parent
    return False


def discover_skills(root: Path) -> Iterator[SkillSource]:
    for skill_md in sorted(root.rglob("SKILL.md")):
        if _is_nested(skill_md, root):
            continue
        try:
            fm = _read_frontmatter(skill_md)
            name = fm["name"].strip()
            description = fm["description"].strip()
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


# --- Packaging --------------------------------------------------------------

def package(skill: SkillSource, out_dir: Path, *, force: bool) -> PackageResult | None:
    archive = out_dir / f"{skill.name}.zip"
    if archive.exists() and not force:
        print(f"skip     {skill.name:<32}  (already packaged)")
        return None
    if archive.exists():
        archive.unlink()

    # shutil.make_archive places `base_dir` at the archive root, which is
    # exactly what the Claude Desktop uploader expects.
    produced = shutil.make_archive(
        base_name=str(out_dir / skill.name),
        format="zip",
        root_dir=str(skill.path.parent),
        base_dir=skill.path.name,
    )
    return PackageResult(skill=skill, archive=Path(produced))


# --- Main -------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path, help="Path to a cloned skills repo")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path.cwd() / "skill-zips",
        help="Output directory for .zip files (default: ./skill-zips)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Rebuild archives that already exist",
    )
    args = parser.parse_args(argv)

    repo: Path = args.repo.resolve()
    if not repo.is_dir():
        print(f"error: {repo} is not a directory", file=sys.stderr)
        return 2

    out: Path = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)

    skills = list(discover_skills(repo))
    if not skills:
        print(f"no skills found under {repo}")
        return 0

    packaged: list[PackageResult] = []
    for skill in skills:
        result = package(skill, out, force=args.force)
        if result is None:
            continue
        packaged.append(result)
        print(f"packaged {skill.name:<32}  -> {result.archive.name}")

    print(f"\n{len(packaged)} archive(s) in {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())