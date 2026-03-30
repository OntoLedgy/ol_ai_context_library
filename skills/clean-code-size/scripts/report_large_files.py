#!/usr/bin/env python3
"""Report oversized source files using simple language-aware thresholds."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path


SUPPORTED_LANGUAGES = {
    "python": {".py"},
    "javascript": {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"},
    "csharp": {".cs"},
    "rust": {".rs"},
}

DEFAULT_THRESHOLDS = {
    "python": 500,
    "javascript": 300,
    "csharp": 250,
    "rust": 250,
    "unknown": 300,
}

SKIP_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "target",
    "__pycache__",
}


@dataclass(frozen=True)
class FileSizeReport:
    path: str
    language: str
    total_lines: int
    nonblank_lines: int
    threshold: int
    over_by: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report source files that exceed language-aware size thresholds."
    )
    parser.add_argument("target_path", help="File or directory to scan.")
    parser.add_argument(
        "--language",
        choices=("auto", "python", "javascript", "csharp", "rust"),
        default="auto",
        help="Restrict scanning to one language. Defaults to auto.",
    )
    parser.add_argument(
        "--max-lines",
        type=int,
        help="Override the default non-blank line threshold.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Maximum number of oversized files to print.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    return parser.parse_args()


def detect_language(path: Path) -> str | None:
    for language, extensions in SUPPORTED_LANGUAGES.items():
        if path.suffix.lower() in extensions:
            return language

    return None


def iter_candidate_files(target_path: Path, selected_language: str) -> list[Path]:
    if target_path.is_file():
        return [target_path]

    candidates: list[Path] = []
    for path in target_path.rglob("*"):
        if path.is_dir():
            if path.name in SKIP_DIRECTORIES:
                continue
            continue

        if any(part in SKIP_DIRECTORIES for part in path.parts):
            continue

        detected_language = detect_language(path)
        if detected_language is None:
            continue

        if selected_language != "auto" and detected_language != selected_language:
            continue

        candidates.append(path)

    return sorted(candidates)


def count_lines(path: Path) -> tuple[int, int]:
    total_lines = 0
    nonblank_lines = 0

    with path.open("r", encoding="utf-8", errors="ignore") as file_handle:
        for line in file_handle:
            total_lines += 1
            if line.strip():
                nonblank_lines += 1

    return total_lines, nonblank_lines


def build_reports(
    files: list[Path],
    max_lines: int | None,
    base_directory: Path,
) -> list[FileSizeReport]:
    reports: list[FileSizeReport] = []

    for file_path in files:
        detected_language = detect_language(file_path) or "unknown"
        threshold = max_lines or DEFAULT_THRESHOLDS[detected_language]
        total_lines, nonblank_lines = count_lines(file_path)

        if nonblank_lines <= threshold:
            continue

        reports.append(
            FileSizeReport(
                path=str(file_path.relative_to(base_directory)),
                language=detected_language,
                total_lines=total_lines,
                nonblank_lines=nonblank_lines,
                threshold=threshold,
                over_by=nonblank_lines - threshold,
            )
        )

    return sorted(
        reports,
        key=lambda report: (report.over_by, report.nonblank_lines, report.path),
        reverse=True,
    )


def render_markdown(
    reports: list[FileSizeReport],
    scanned_file_count: int,
    top_n: int,
) -> str:
    header_lines = [
        "## Large File Report",
        "",
        f"Scanned files: {scanned_file_count}",
        f"Oversized files: {len(reports)}",
        "",
    ]

    if not reports:
        return "\n".join(header_lines + ["No files exceeded the configured threshold."])

    table_lines = [
        "| Rank | File | Language | Total lines | Non-blank lines | Threshold | Over by |",
        "|------|------|----------|-------------|-----------------|-----------|---------|",
    ]

    for index, report in enumerate(reports[:top_n], start=1):
        table_lines.append(
            f"| {index} | `{report.path}` | {report.language} | {report.total_lines} | "
            f"{report.nonblank_lines} | {report.threshold} | {report.over_by} |"
        )

    if len(reports) > top_n:
        table_lines.extend(
            [
                "",
                f"Showing top {top_n} oversized files out of {len(reports)}.",
            ]
        )

    return "\n".join(header_lines + table_lines)


def main() -> int:
    args = parse_args()
    target_path = Path(args.target_path).resolve()

    if not target_path.exists():
        raise SystemExit(f"Target path does not exist: {target_path}")

    base_directory = target_path if target_path.is_dir() else target_path.parent
    candidate_files = iter_candidate_files(target_path, args.language)
    reports = build_reports(candidate_files, args.max_lines, base_directory)

    if args.format == "json":
        print(
            json.dumps(
                {
                    "scanned_files": len(candidate_files),
                    "oversized_files": len(reports),
                    "items": [asdict(report) for report in reports[: args.top]],
                },
                indent=2,
            )
        )
        return 0

    print(render_markdown(reports, len(candidate_files), args.top))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
