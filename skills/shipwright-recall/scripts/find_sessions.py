#!/usr/bin/env python3
"""List session files for the active workspace. Does not print their bodies.

Paths follow shipwright-recall's procedure. Codex, Claude Code, and OpenCode
are the hosts this plugin targets. Cursor and Pi directories are included so
a transcript stored there is not ignored.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


def cursor_slug(workspace: Path) -> str:
    text = workspace.resolve().as_posix()
    if text.startswith("/"):
        text = text[1:]
    return text.replace("/", "-")


def claude_slug(workspace: Path) -> str:
    return re.sub(r"[^A-Za-z0-9]", "-", workspace.resolve().as_posix())


def roots(home: Path, workspace: Path) -> list[tuple[str, Path]]:
    cursor = cursor_slug(workspace)
    claude = claude_slug(workspace)
    return [
        ("claude", home / ".claude" / "projects" / claude),
        ("codex", home / ".codex" / "sessions"),
        ("opencode", home / ".local" / "share" / "opencode" / "storage" / "session"),
        ("cursor", home / ".cursor" / "projects" / cursor / "agent-transcripts"),
        ("pi", home / ".pi" / "agent" / "sessions" / f"--{cursor}--"),
    ]


def codex_matches(path: Path, workspace: Path) -> bool:
    try:
        first = path.open(encoding="utf-8").readline()
    except OSError:
        return False
    try:
        payload = json.loads(first).get("payload", {})
    except json.JSONDecodeError:
        return False
    cwd = payload.get("cwd")
    if not isinstance(cwd, str):
        return False
    return Path(cwd).resolve() == workspace.resolve()


def opencode_matches(path: Path, workspace: Path) -> bool:
    try:
        header = path.read_text(encoding="utf-8")[:4096]
    except OSError:
        return False
    try:
        data = json.loads(header)
    except json.JSONDecodeError:
        data = {}
    wanted = workspace.resolve().as_posix()
    if isinstance(data, dict):
        for key in ("cwd", "path", "directory", "workspace"):
            value = data.get(key)
            if isinstance(value, str) and Path(value).resolve().as_posix() == wanted:
                return True
    return wanted in header


def collect(home: Path, workspace: Path, harness: str, days: int | None) -> list[tuple[str, Path, float]]:
    cutoff = None if days is None else datetime.now(timezone.utc) - timedelta(days=days)
    found: list[tuple[str, Path, float]] = []
    for name, root in roots(home, workspace):
        if harness not in ("auto", name) or not root.is_dir():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if name == "codex" and not codex_matches(path, workspace):
                continue
            if name == "opencode" and path.suffix != ".json":
                continue
            if name == "opencode" and not opencode_matches(path, workspace):
                continue
            if name in ("claude", "cursor", "pi") and path.suffix != ".jsonl":
                continue
            modified = path.stat().st_mtime
            if cutoff is not None:
                when = datetime.fromtimestamp(modified, timezone.utc)
                if when < cutoff:
                    continue
            found.append((name, path, modified))
    found.sort(key=lambda item: item[2], reverse=True)
    return found


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--harness", default="auto", choices=["auto", "claude", "codex", "opencode", "cursor", "pi"])
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--all-time", action="store_true")
    args = parser.parse_args(argv)
    workspace = args.workspace.resolve()
    rows = collect(args.home, workspace, args.harness, None if args.all_time else args.days)
    for name, path, modified in rows:
        stamp = datetime.fromtimestamp(modified, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        print(f"{stamp}\t{name}\t{path}")
    print(f"{len(rows)} session files", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
