#!/usr/bin/env python3
"""Compare git patch-id for two commits.

A verdict covers a patch. A rebase can move the SHA without changing the
patch. Exit 0 when the stable patch-ids match, 1 when they differ.
`--allow-noise` still exits 1 for a code change, and exits 0 when the only
files that differ between the two patches are tests, docs, or lint config.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

NOISE_PARTS = {
    "test",
    "tests",
    "docs",
    "doc",
    "__snapshots__",
}
NOISE_NAMES = {
    ".editorconfig",
    ".prettierrc",
    ".prettierrc.json",
    "ruff.toml",
    "pyproject.toml",
    "eslint.config.js",
    "eslint.config.mjs",
}


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout


def patch_id(repo: Path, commit: str) -> str:
    diff = subprocess.run(
        ["git", "-C", str(repo), "show", "--pretty=", "--binary", commit],
        capture_output=True,
        text=True,
    )
    if diff.returncode != 0:
        raise SystemExit(diff.stderr.strip() or f"git show {commit} failed")
    hashed = subprocess.run(
        ["git", "-C", str(repo), "patch-id", "--stable"],
        input=diff.stdout,
        capture_output=True,
        text=True,
    )
    if hashed.returncode != 0 or not hashed.stdout.strip():
        raise SystemExit(hashed.stderr.strip() or f"no patch-id for {commit}")
    return hashed.stdout.split()[0]


def names(repo: Path, commit: str) -> set[str]:
    text = git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", commit)
    return {line for line in text.splitlines() if line}


def noise_only(paths: set[str]) -> bool:
    if not paths:
        return True
    for path in paths:
        name = Path(path).name
        parts = set(Path(path).parts)
        if name in NOISE_NAMES or parts & NOISE_PARTS or name.startswith("eslint") or name.endswith(".md"):
            continue
        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("commit_a")
    parser.add_argument("commit_b")
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--allow-noise", action="store_true")
    args = parser.parse_args()
    left = patch_id(args.repo, args.commit_a)
    right = patch_id(args.repo, args.commit_b)
    same = left == right
    changed = names(args.repo, args.commit_a) ^ names(args.repo, args.commit_b)
    print(f"patch-id {args.commit_a} {left}")
    print(f"patch-id {args.commit_b} {right}")
    if same:
        print("SAME")
        return
    if args.allow_noise and noise_only(changed):
        print("NOISE")
        for path in sorted(changed):
            print(f"noise-file {path}")
        return
    print("DIFFERENT")
    for path in sorted(changed):
        print(f"changed-file {path}")
    raise SystemExit(1)


if __name__ == "__main__":
    sys.exit(main())
