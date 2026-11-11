#!/usr/bin/env python3
"""Mine an eval question bank from a git repository.

The list is shown to a person once. This script does not rewrite subjects
into a user's voice and does not drop commits on its own.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

MUTATIONS = ("reversed-comparison", "dropped-if", "off-by-one")
_SENSITIVE = re.compile(r"password|secret|token|api[_-]?key", re.I)
_REVERT = re.compile(r"reverts commit ([0-9a-f]{7,40})", re.I)


def git(repo: str, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def is_test_path(path: str) -> bool:
    name = path.replace("\\", "/").lower()
    base = name.rsplit("/", 1)[-1]
    return (
        "/tests/" in f"/{name}"
        or "/test/" in f"/{name}"
        or name.startswith("tests/")
        or name.startswith("test/")
        or base.startswith("test_")
        or base.endswith("_test.py")
        or ".test." in base
        or ".spec." in base
    )


def is_source_path(path: str) -> bool:
    if is_test_path(path):
        return False
    name = path.replace("\\", "/").lower()
    if name.endswith((".md", ".txt", ".rst", ".png", ".svg", ".lock")):
        return False
    return True


def _subject_kind(subject: str) -> str | None:
    text = subject.strip().lower()
    if text.startswith(("fix", "bug")):
        return "bugfix"
    if any(word in text for word in ("refactor", "rename", "extract", "restructure")):
        return "refactor"
    if text.startswith(("feat", "feature", "add ")):
        return "feature"
    return None


def _changed_files(repo: str, sha: str) -> list[str]:
    out = git(repo, "show", "--name-only", "--pretty=format:", sha)
    return [line for line in out.splitlines() if line.strip()]


def _commits(repo: str, limit: int) -> list[dict]:
    raw = git(repo, "log", "--no-merges", f"-{limit}", "--pretty=%H%x1f%s%x1f%b%x1e")
    commits = []
    for record in raw.split("\x1e"):
        record = record.strip("\n")
        if not record.strip():
            continue
        sha, subject, body = (record.split("\x1f", 2) + ["", ""])[:3]
        commits.append({"sha": sha.strip(), "subject": subject.strip(), "body": body})
    return commits


def mine_bugfix_tasks(repo: str, limit: int = 300):
    """找出“修 bug 且改了测试”的提交，作为候选题。任务描述之后要改写成用户口吻。"""
    for task in mine_tasks(repo, limit):
        if task["kind"] == "bugfix":
            yield task


def mine_tasks(repo: str, limit: int = 300) -> list[dict]:
    commits = _commits(repo, limit)
    # git log is newest first. "Later" means a smaller index.
    files_of: list[list[str]] = []
    for commit in commits:
        files_of.append(_changed_files(repo, commit["sha"]))
    later_paths: set[str] = set()
    tasks: list[dict] = []
    reverted: dict[str, str] = {}
    for commit in commits:
        match = _REVERT.search(commit["body"])
        if match:
            reverted[match.group(1)] = commit["sha"]

    for index, commit in enumerate(commits):
        files = files_of[index]
        # Paths touched by newer commits (already recorded) make this one stale.
        untouched = not any(path in later_paths for path in files)
        for path in files:
            later_paths.add(path)
        tests = [path for path in files if is_test_path(path)]
        sources = [path for path in files if is_source_path(path)]
        label = _subject_kind(commit["subject"])
        sensitive = bool(_SENSITIVE.search(commit["subject"]) or _SENSITIVE.search(commit["body"]))
        base = {
            "start_from": f"{commit['sha']}^",
            "reference": commit["sha"],
            "hidden_tests": tests,
            "raw_subject": commit["subject"],
            "possible_sensitive": sensitive,
        }
        full = commit["sha"]
        subject_lower = commit["subject"].lower()
        is_revert_commit = subject_lower.startswith("revert") or bool(_REVERT.search(commit["body"]))
        is_reverted = any(full.startswith(prefix) or prefix.startswith(full) for prefix in reverted)
        if is_reverted:
            tasks.append({**base, "kind": "review-bad", "reason": "reverted", "confidence": "high"})
        if is_revert_commit:
            continue
        if label == "bugfix" and tests:
            tasks.append({**base, "kind": "bugfix", "confidence": "high"})
        elif label == "feature" and tests and sources:
            tasks.append({**base, "kind": "feature", "confidence": "high"})
        elif tests and sources and label is None:
            tasks.append({**base, "kind": "feature", "confidence": "prune"})
        elif sources and not tests and (label == "refactor" or label is None):
            tasks.append(
                {
                    **base,
                    "kind": "refactor",
                    "confidence": "high" if label == "refactor" else "prune",
                }
            )
        if untouched and files and not (label == "bugfix" and tests) and not is_reverted:
            tasks.append(
                {
                    **base,
                    "kind": "review-clean",
                    "ci": "unknown",
                    "confidence": "prune",
                }
            )
    return tasks


def inject_bug(source: str, kind: str) -> str | None:
    """Return source with one small bug, or None when this source has no site."""
    if kind == "reversed-comparison":
        for old, new in ((" == ", " != "), (" < ", " > "), (" > ", " < ")):
            if old in source:
                return source.replace(old, new, 1)
        return None
    if kind == "dropped-if":
        match = re.search(r"(?m)^(?P<indent>[ \t]*)if .+:[ \t]*$", source)
        if not match:
            return None
        line = match.group(0)
        return source.replace(line, f"{match.group('indent')}if True:", 1)
    if kind == "off-by-one":
        for old, new in ((" - 1", " - 2"), (" + 1", " + 2"), (" > ", " >= "), (" < ", " <= ")):
            if old in source:
                return source.replace(old, new, 1)
        return None
    raise ValueError(kind)


def test_strength(source: str, caught) -> dict:
    """caught(mutated_source) is true when the suite fails, which means it caught the bug."""
    report = {}
    for kind in MUTATIONS:
        mutated = inject_bug(source, kind)
        if mutated is None:
            report[kind] = "no-site"
        else:
            report[kind] = "caught" if caught(mutated) else "missed"
    scored = [item for item in report.values() if item != "no-site"]
    report["caught_rate"] = (scored.count("caught") / len(scored)) if scored else None
    return report


def render_bank_markdown(tasks: list[dict]) -> str:
    lines = [
        "# Question bank candidates",
        "",
        "看一次。删掉敏感、过时或太简单的题，再冻成 bank.json。确认 CI 之前不要用 review-clean。",
        "",
    ]
    for index, task in enumerate(tasks, start=1):
        lines.append(
            f"{index}. `{task['kind']}` {task['raw_subject']} "
            f"(`{task['reference'][:7]}`, {task.get('confidence', 'high')})"
        )
        if task.get("possible_sensitive"):
            lines.append("   - possible_sensitive: leave this out unless you explicitly keep it")
        if task.get("ci") == "unknown":
            lines.append("   - ci: unknown until a green run is confirmed")
    lines.append("")
    return "\n".join(lines)


def write_bank(repo: str, dest: Path, limit: int = 300) -> dict:
    tasks = mine_tasks(repo, limit)
    dest.mkdir(parents=True, exist_ok=True)
    payload = {"tasks": tasks}
    (dest / "candidates.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (dest / "candidates.md").write_text(render_bank_markdown(tasks), encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Mine eval tasks from git history")
    parser.add_argument("repo")
    parser.add_argument("--limit", type=int, default=300)
    parser.add_argument("--dest", type=Path, required=True)
    args = parser.parse_args()
    write_bank(args.repo, args.dest, args.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
