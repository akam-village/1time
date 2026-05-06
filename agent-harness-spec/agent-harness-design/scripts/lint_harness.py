#!/usr/bin/env python3
"""Lint common Agent Harness structure and content issues."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


KEBAB = r"[a-z0-9]+(?:-[a-z0-9]+)*"
LIMITS = {
    "CLAUDE.md": 100,
    ".github/copilot-instructions.md": 500,
}
INSTRUCTION_LIMIT = 200


@dataclass
class Finding:
    severity: str
    path: str
    message: str


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def line_count(path: Path) -> int:
    return len(read(path).splitlines())


def has_frontmatter(text: str) -> bool:
    return text.startswith("---\n") or text.startswith("---\r\n")


def frontmatter_text(text: str) -> str:
    if not has_frontmatter(text):
        return ""
    normalized = text.replace("\r\n", "\n")
    parts = normalized.split("---\n", 2)
    if len(parts) < 3:
        return ""
    return parts[1]


def check_name(path: Path, root: Path, findings: list[Finding]) -> None:
    relative = rel(path, root)
    name = path.name
    checks = [
        (".github/instructions", rf"^{KEBAB}\.instructions\.md$"),
        (".github/prompts", rf"^{KEBAB}\.prompt\.md$"),
        (".github/agents", rf"^{KEBAB}\.agent\.md$"),
    ]
    for prefix, pattern in checks:
        if relative.startswith(prefix + "/") and not re.match(pattern, name):
            findings.append(Finding("error", relative, f"File name should match `{pattern}`."))

    if "/skills/" in relative:
        parts = relative.split("/")
        try:
            idx = parts.index("skills")
            skill_name = parts[idx + 1]
        except (ValueError, IndexError):
            return
        if not re.match(rf"^{KEBAB}$", skill_name):
            findings.append(Finding("error", relative, "Skill directory should use kebab-case."))
        if path.name == "SKILL.md":
            return


def check_frontmatter(path: Path, root: Path, findings: list[Finding]) -> None:
    relative = rel(path, root)
    if not path.suffix == ".md":
        return
    text = read(path)
    fm = frontmatter_text(text)
    if not fm:
        findings.append(Finding("warning", relative, "Markdown harness file has no YAML frontmatter."))
        return

    if path.name == "SKILL.md":
        if "description:" not in fm:
            findings.append(Finding("error", relative, "Skill frontmatter should include `description`."))
        return

    for field in ("description:", "version:", "last_updated:"):
        if field not in fm:
            findings.append(Finding("warning", relative, f"Frontmatter is missing `{field}`."))


def check_size(path: Path, root: Path, findings: list[Finding]) -> None:
    relative = rel(path, root)
    count = line_count(path)
    if relative in LIMITS and count > LIMITS[relative]:
        findings.append(Finding("warning", relative, f"File has {count} lines; soft limit is {LIMITS[relative]}."))
    if relative.startswith(".github/instructions/") and count > INSTRUCTION_LIMIT:
        findings.append(Finding("warning", relative, f"Instruction file has {count} lines; soft limit is {INSTRUCTION_LIMIT}."))


def check_content_smells(path: Path, root: Path, findings: list[Finding]) -> None:
    relative = rel(path, root)
    text = read(path)
    lower = text.lower()

    if relative.startswith(".github/instructions/"):
        if re.search(r"\bstep\s+\d+\b|^#{1,3}\s*steps?\b", lower, re.MULTILINE):
            findings.append(Finding("warning", relative, "Instruction file appears to contain step-by-step procedure; consider a skill."))
        if "temporary" in lower or "until " in lower:
            findings.append(Finding("info", relative, "Instruction file may contain temporary context; verify it is durable policy."))

    if relative.startswith(".github/prompts/"):
        policy_words = ["coding style", "architecture policy", "security requirements", "review policy"]
        if any(word in lower for word in policy_words):
            findings.append(Finding("warning", relative, "Prompt may contain durable policy; consider moving it to instructions."))

    if relative.startswith(".github/agents/"):
        if len(re.findall(r"\bstep\s+\d+\b", lower)) >= 3:
            findings.append(Finding("warning", relative, "Agent file contains many steps; consider moving procedure to a skill."))

    if relative in ("CLAUDE.md", "AGENTS.md"):
        policy_headers = ["coding style", "architecture", "testing policy", "security requirements"]
        if any(header in lower for header in policy_headers) and line_count(path) > 80:
            findings.append(Finding("warning", relative, "Router may be carrying detailed policy; keep routers thin."))


def harness_files(root: Path) -> list[Path]:
    patterns = [
        "CLAUDE.md",
        "AGENTS.md",
        ".github/**/*.md",
        ".claude/**/*.md",
        ".codex/**/*.md",
    ]
    files: list[Path] = []
    for pattern in patterns:
        files.extend(path for path in root.glob(pattern) if path.is_file())
    return sorted(set(files))


def lint(root: Path) -> list[Finding]:
    findings: list[Finding] = []

    if not (root / ".github").exists():
        findings.append(Finding("warning", ".", "No `.github/` canonical harness root found."))
    if not (root / ".github/copilot-instructions.md").exists():
        findings.append(Finding("warning", ".github/copilot-instructions.md", "Top-level instruction file is missing."))

    for path in harness_files(root):
        check_name(path, root, findings)
        check_frontmatter(path, root, findings)
        check_size(path, root, findings)
        check_content_smells(path, root, findings)

    for skill_dir in sorted((root / ".github/skills").glob("*")) if (root / ".github/skills").exists() else []:
        if skill_dir.is_dir() and not (skill_dir / "SKILL.md").exists():
            findings.append(Finding("error", rel(skill_dir, root), "Skill directory is missing `SKILL.md`."))

    if (root / "scripts").exists() and not (root / ".github/skills").exists():
        findings.append(Finding("info", "scripts", "Shared scripts exist but no `.github/skills/` directory was found; ensure scripts are documented."))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Repository root to lint")
    parser.add_argument("--strict", action="store_true", help="Return non-zero for warnings as well as errors")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists() or not root.is_dir():
        parser.error(f"root is not a directory: {root}")

    findings = lint(root)
    if not findings:
        print("No harness lint findings.")
        return 0

    for finding in findings:
        print(f"[{finding.severity}] {finding.path}: {finding.message}")

    has_error = any(finding.severity == "error" for finding in findings)
    has_warning = any(finding.severity == "warning" for finding in findings)
    if has_error or (args.strict and has_warning):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
