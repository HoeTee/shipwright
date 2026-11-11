#!/usr/bin/env python3
"""Collect shortcut: and ponytail: comments into a debt ledger.

Read-only. Uses git grep --no-index --exclude-standard so .gitignore applies
and untracked files are still visible.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path

DEFAULT_PATTERN = r"(#|//|/\*) ?(shortcut|ponytail):"


def git_grep(repo: Path, pattern: str) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), "grep", "--no-index", "--exclude-standard", "-nE", pattern],
        capture_output=True,
        text=True,
    )
    if result.returncode not in (0, 1):
        message = result.stderr.strip() or f"git grep failed ({result.returncode})"
        raise SystemExit(message)
    return [line for line in result.stdout.splitlines() if line.strip()]


def parse_hit(line: str, pattern: re.Pattern[str]) -> dict[str, object] | None:
    match = re.match(r"^(.*):(\d+):(.*)$", line)
    if not match:
        return None
    path, lineno, text = match.group(1), int(match.group(2)), match.group(3)
    found = pattern.search(text)
    if not found:
        return None
    comment = text[found.end() :].strip().rstrip("*/").strip()
    return {"path": path, "line": lineno, "text": text.strip(), "comment": comment}


def split_ceiling(comment: str) -> tuple[str, str | None]:
    if "," not in comment:
        return comment.strip(), None
    ceiling, upgrade = comment.split(",", 1)
    upgrade = upgrade.strip()
    return ceiling.strip(), upgrade or None


def blame(repo: Path, path: str, line: int) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "blame", "-L", f"{line},{line}", "--porcelain", "--", path],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return "unknown"
    for row in result.stdout.splitlines():
        if row.startswith("author "):
            return row[len("author ") :]
    return "unknown"


def collect(repo: Path, pattern: str, *, with_blame: bool) -> list[dict[str, object]]:
    compiled = re.compile(pattern)
    rows: list[dict[str, object]] = []
    for line in git_grep(repo, pattern):
        hit = parse_hit(line, compiled)
        if hit is None:
            continue
        if with_blame:
            hit["owner"] = blame(repo, str(hit["path"]), int(hit["line"]))
        rows.append(hit)
    return rows


def render(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "No shortcut debt. Clean ledger."
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["path"])].append(row)
    lines: list[str] = []
    no_trigger = 0
    for path in sorted(grouped):
        for row in grouped[path]:
            ceiling, upgrade = split_ceiling(str(row["comment"]))
            if upgrade is None:
                no_trigger += 1
                upgrade_text = "(none)"
                tag = " no-trigger"
            else:
                upgrade_text = upgrade
                tag = ""
            owner = f" owner: {row['owner']}." if row.get("owner") else ""
            lines.append(
                f"{path}:{row['line']}, {row['text']}. ceiling: {ceiling}. upgrade: {upgrade_text}.{owner}{tag}"
            )
    lines.append(f"{len(rows)} markers, {no_trigger} with no trigger.")
    return "\n".join(lines)


def self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        (root / ".gitignore").write_text("secret.py\n", encoding="utf-8")
        (root / "app.py").write_text(
            "\n".join(
                [
                    "def run():",
                    "    # shortcut: one process, add a lock when two writers share the file",
                    "    pass",
                    "    # ponytail: in-memory list",
                    "    # this prose mentions shortcut: but is not a marker",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        (root / "secret.py").write_text("# shortcut: ignored, never\n", encoding="utf-8")
        subprocess.run(["git", "add", "app.py", ".gitignore"], cwd=root, check=True)
        text = render(collect(root, DEFAULT_PATTERN, with_blame=False))
        assert "secret.py" not in text, text
        assert "app.py:2" in text and "one process" in text, text
        assert "app.py:4" in text and "no-trigger" in text, text
        assert "prose mentions" not in text, text
        assert text.endswith("2 markers, 1 with no trigger."), text
    ceiling, upgrade = split_ceiling("one process, add a lock")
    assert ceiling == "one process" and upgrade == "add a lock"
    print("scan_shortcuts self-test ok")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Collect shortcut comments into a debt ledger.")
    parser.add_argument("repo", nargs="?", default=".", help="Repository root")
    parser.add_argument("--marker", help="Search this word instead of shortcut and ponytail")
    parser.add_argument("--prefix", action="append", default=[], help="Extra git-grep extended pattern")
    parser.add_argument("--blame", action="store_true", help="Add the git blame author on each row")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.marker:
        pattern = rf"(#|//|/\*) ?{re.escape(args.marker)}:"
    else:
        pattern = DEFAULT_PATTERN
    if args.prefix:
        pattern = "(?:" + "|".join([pattern, *args.prefix]) + ")"
    repo = Path(args.repo).resolve()
    print(render(collect(repo, pattern, with_blame=args.blame)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
