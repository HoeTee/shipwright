#!/usr/bin/env python3
"""Export one revision into a fresh directory with no .git history.

Hidden tests and plans/ are removed so a candidate cannot read the answer
or the commit messages that would leak it.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def export_workspace(repo: str, rev: str, dest: Path, drop: list[str] | None = None) -> Path:
    if dest.exists():
        raise FileExistsError(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    archive = subprocess.run(
        ["git", "-C", repo, "archive", rev],
        check=True,
        capture_output=True,
    )
    dest.mkdir()
    subprocess.run(["tar", "-x", "-C", str(dest)], input=archive.stdout, check=True)
    for rel in drop or []:
        target = dest / rel
        if target.is_dir():
            shutil.rmtree(target)
        elif target.is_file():
            target.unlink()
    plans = dest / "plans"
    if plans.exists():
        shutil.rmtree(plans)
    if (dest / ".git").exists():
        raise RuntimeError("export leaked .git")
    return dest


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a git revision without .git")
    parser.add_argument("repo")
    parser.add_argument("rev")
    parser.add_argument("dest", type=Path)
    parser.add_argument("--drop", action="append", default=[])
    args = parser.parse_args()
    export_workspace(args.repo, args.rev, args.dest, args.drop)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
