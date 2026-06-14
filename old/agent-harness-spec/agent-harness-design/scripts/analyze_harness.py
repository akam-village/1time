#!/usr/bin/env python3
"""Summarize Agent Harness files in a repository."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


HARNESS_PATTERNS = {
    "routers": ["CLAUDE.md", "AGENTS.md"],
    "canonical_top": [".github/copilot-instructions.md"],
    "instructions": [".github/instructions/*.instructions.md"],
    "prompts": [".github/prompts/*.prompt.md"],
    "agents": [".github/agents/*.agent.md"],
    "skills": [".github/skills/*/SKILL.md"],
    "root_scripts": ["scripts/*"],
    "claude_adapters": [".claude/**/*"],
    "codex_adapters": [".codex/**/*"],
}


@dataclass
class FileInfo:
    path: Path
    lines: int
    bytes_: int


def count_lines(path: Path) -> int:
    try:
        return len(path.read_text(encoding="utf-8", errors="replace").splitlines())
    except OSError:
        return 0


def collect(root: Path, pattern: str) -> list[FileInfo]:
    matches: list[FileInfo] = []
    for path in sorted(root.glob(pattern)):
        if path.is_file():
            matches.append(
                FileInfo(
                    path=path.relative_to(root),
                    lines=count_lines(path),
                    bytes_=path.stat().st_size,
                )
            )
    return matches


def render(root: Path) -> str:
    sections: dict[str, list[FileInfo]] = {}
    for category, patterns in HARNESS_PATTERNS.items():
        found: list[FileInfo] = []
        for pattern in patterns:
            found.extend(collect(root, pattern))
        sections[category] = sorted(found, key=lambda item: str(item.path))

    total_files = sum(len(items) for items in sections.values())
    total_lines = sum(item.lines for items in sections.values() for item in items)

    lines = [
        "# Agent Harness Analysis",
        "",
        f"Root: `{root}`",
        f"Files discovered: {total_files}",
        f"Total harness lines: {total_lines}",
        "",
        "## Categories",
        "",
        "| Category | Files | Lines |",
        "|---|---:|---:|",
    ]

    for category, items in sections.items():
        lines.append(f"| {category} | {len(items)} | {sum(item.lines for item in items)} |")

    lines.extend(["", "## Files", ""])
    for category, items in sections.items():
        lines.append(f"### {category}")
        if not items:
            lines.append("")
            lines.append("_None found._")
            lines.append("")
            continue
        lines.append("")
        lines.append("| Path | Lines | Bytes |")
        lines.append("|---|---:|---:|")
        for item in items:
            lines.append(f"| `{item.path.as_posix()}` | {item.lines} | {item.bytes_} |")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Repository root to analyze")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists() or not root.is_dir():
        parser.error(f"root is not a directory: {root}")

    print(render(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
