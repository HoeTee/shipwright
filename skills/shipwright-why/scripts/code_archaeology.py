#!/usr/bin/env python3
"""Read-only git archaeology for shipwright-why.

Wraps the searches in references/sources/code-archaeology.md. It does not
commit, checkout, or change the worktree.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REV = re.compile(r"^[A-Za-z0-9_./^{}~-]+$")


def git(repo: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def require_repo(path: Path) -> Path:
    repo = path.resolve()
    probe = git(repo, ["rev-parse", "--is-inside-work-tree"])
    if probe.returncode != 0 or probe.stdout.strip() != "true":
        raise SystemExit(f"{repo} is not a git worktree")
    return repo


def rev(value: str) -> str:
    if not REV.fullmatch(value):
        raise SystemExit(f"refusing revision {value!r}")
    return value


def emit(result: subprocess.CompletedProcess[str]) -> int:
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return result.returncode


def build(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--repo", type=Path, default=Path("."))
    sub = parser.add_subparsers(dest="command", required=True)

    follow = sub.add_parser("follow", help="history through renames")
    follow.add_argument("path")

    pickaxe = sub.add_parser("pickaxe", help="commits that add or remove this exact text")
    pickaxe.add_argument("--text", required=True)
    pickaxe.add_argument("path")

    regex = sub.add_parser("regex", help="commits that touch lines matching a regex")
    regex.add_argument("--pattern", required=True)
    regex.add_argument("path")

    blame = sub.add_parser("blame", help="who wrote a line range")
    blame.add_argument("--start", type=int, required=True)
    blame.add_argument("--end", type=int, required=True)
    blame.add_argument("path")

    show = sub.add_parser("show", help="one commit's full diff")
    show.add_argument("commit")

    span = sub.add_parser("range", help="commits between two points affecting a path")
    span.add_argument("--old", required=True)
    span.add_argument("--new", required=True)
    span.add_argument("path")

    hints = sub.add_parser("hints", help="ADR names, nearby TODO markers, related tests")
    hints.add_argument("--symbol", default="")
    hints.add_argument("path", nargs="?", default="")
    return parser


def main(argv: list[str]) -> int:
    args = build(argparse.ArgumentParser(description=__doc__)).parse_args(argv)
    repo = require_repo(args.repo)
    if args.command == "follow":
        result = git(repo, ["log", "--follow", "--oneline", "--", args.path])
    elif args.command == "pickaxe":
        result = git(repo, ["log", "-S", args.text, "--oneline", "--", args.path])
    elif args.command == "regex":
        result = git(repo, ["log", "-G", args.pattern, "--oneline", "--", args.path])
    elif args.command == "blame":
        if args.start < 1 or args.end < args.start:
            raise SystemExit("blame range must be a positive start..end")
        result = git(repo, ["blame", "-L", f"{args.start},{args.end}", "--", args.path])
    elif args.command == "show":
        result = git(repo, ["show", "--stat", "--format=fuller", rev(args.commit)])
    elif args.command == "range":
        result = git(repo, ["log", "--oneline", f"{rev(args.old)}..{rev(args.new)}", "--", args.path])
    elif args.command == "hints":
        chunks = [
            git(repo, ["grep", "-l", "-i", "-e", "architecture.decision", "--", "*.md"]),
        ]
        if args.path:
            chunks.append(
                git(
                    repo,
                    ["grep", "-n", "-E", r"(TODO|FIXME|HACK|XXX|NOTE)", "--", args.path],
                )
            )
        if args.symbol:
            chunks.append(git(repo, ["grep", "-l", "-e", args.symbol, "--", "*test*"]))
        code = 0
        for chunk in chunks:
            sys.stdout.write(chunk.stdout)
            if chunk.returncode not in (0, 1):
                sys.stderr.write(chunk.stderr)
                code = chunk.returncode
        return code
    else:
        raise SystemExit(f"unknown command {args.command}")
    return emit(result)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
