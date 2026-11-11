#!/usr/bin/env python3
"""Find this workspace's transcript without scanning other projects.

Known layouts: Claude Code's project slug directory, Codex rollout files
whose first line names this workspace, and an optional OpenCode directory
passed with --extra-dir.
"""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path


def claude_slug(workspace: Path) -> str:
    return "".join(character if character.isalnum() else "-" for character in str(workspace.resolve()))


def first_text(path: Path, limit: int = 40) -> str:
    chunks: list[str] = []
    with path.open(encoding="utf-8", errors="replace") as handle:
        for _ in range(limit):
            line = handle.readline()
            if not line:
                break
            chunks.append(line)
    return "".join(chunks)


def json_objects(text: str) -> list[object]:
    rows: list[object] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def opening_text(path: Path) -> str:
    blob = first_text(path)
    parts: list[str] = [blob]
    for row in json_objects(blob):
        parts.extend(_strings(row))
    return "\n".join(parts)


def _strings(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        found: list[str] = []
        for item in value.values():
            found.extend(_strings(item))
        return found
    if isinstance(value, list):
        found = []
        for item in value:
            found.extend(_strings(item))
        return found
    return []


def codex_cwd(path: Path) -> str:
    first = ""
    with path.open(encoding="utf-8", errors="replace") as handle:
        first = handle.readline()
    try:
        row = json.loads(first)
    except json.JSONDecodeError:
        return ""
    payload = row.get("payload") if isinstance(row, dict) else None
    if isinstance(payload, dict) and isinstance(payload.get("cwd"), str):
        return payload["cwd"]
    if isinstance(row, dict) and isinstance(row.get("cwd"), str):
        return row["cwd"]
    return ""


def claude_candidates(workspace: Path, home: Path) -> list[Path]:
    root = home / ".claude" / "projects" / claude_slug(workspace)
    if not root.is_dir():
        return []
    return sorted(root.glob("*.jsonl"), key=lambda item: item.stat().st_mtime, reverse=True)


def codex_candidates(workspace: Path, home: Path, *, scan_limit: int) -> list[Path]:
    root = home / ".codex" / "sessions"
    if not root.is_dir():
        return []
    wanted = str(workspace.resolve())
    files = sorted(root.glob("**/rollout-*.jsonl"), key=lambda item: item.stat().st_mtime, reverse=True)
    matched: list[Path] = []
    for path in files[:scan_limit]:
        cwd = codex_cwd(path)
        if cwd and str(Path(cwd).resolve()) == wanted:
            matched.append(path)
    return matched


def extra_candidates(extra_dir: Path) -> list[Path]:
    if not extra_dir.is_dir():
        return []
    return sorted(extra_dir.glob("*.jsonl"), key=lambda item: item.stat().st_mtime, reverse=True)


def matching(paths: list[Path], prompt: str) -> list[Path]:
    if not prompt:
        return paths
    return [path for path in paths if prompt in opening_text(path)]


def find_transcripts(
    workspace: Path,
    prompt: str,
    *,
    home: Path,
    extra_dir: Path | None,
    scan_limit: int,
) -> list[Path]:
    found: list[Path] = []
    found.extend(matching(claude_candidates(workspace, home), prompt))
    found.extend(matching(codex_candidates(workspace, home, scan_limit=scan_limit), prompt))
    if extra_dir is not None:
        found.extend(matching(extra_candidates(extra_dir), prompt))
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in found:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(resolved)
    return unique


def self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp) / "home"
        workspace = Path(tmp) / "proj"
        workspace.mkdir()
        other = Path(tmp) / "other"
        other.mkdir()
        prompt = "shipwright reflect unique opening"
        slug = claude_slug(workspace)
        good = home / ".claude" / "projects" / slug
        good.mkdir(parents=True)
        (good / "sess.jsonl").write_text(
            json.dumps({"message": {"content": [{"text": prompt}]}}) + "\n",
            encoding="utf-8",
        )
        foreign = home / ".claude" / "projects" / claude_slug(other)
        foreign.mkdir(parents=True)
        (foreign / "nope.jsonl").write_text(
            json.dumps({"message": {"content": [{"text": prompt}]}}) + "\n",
            encoding="utf-8",
        )
        day = home / ".codex" / "sessions" / "2026" / "11" / "11"
        day.mkdir(parents=True)
        (day / "rollout-a.jsonl").write_text(
            json.dumps({"payload": {"cwd": str(workspace.resolve())}}) + "\n" + json.dumps({"text": prompt}) + "\n",
            encoding="utf-8",
        )
        (day / "rollout-b.jsonl").write_text(
            json.dumps({"payload": {"cwd": str(other.resolve())}}) + "\n" + json.dumps({"text": prompt}) + "\n",
            encoding="utf-8",
        )
        extra = Path(tmp) / "opencode"
        extra.mkdir()
        (extra / "s.jsonl").write_text(json.dumps({"text": prompt}) + "\n", encoding="utf-8")
        rows = find_transcripts(workspace, prompt, home=home, extra_dir=extra, scan_limit=20)
        names = {path.name for path in rows}
        assert names == {"sess.jsonl", "rollout-a.jsonl", "s.jsonl"}, names
        assert claude_slug(Path("/tmp/My Proj")) == "-tmp-My-Proj"
    print("find_transcript self-test ok")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Find this workspace's session transcript.")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--prompt", default="", help="Opening user prompt to confirm the file")
    parser.add_argument("--extra-dir", help="OpenCode (or other host) session directory for this workspace only")
    parser.add_argument("--home", default=str(Path.home()))
    parser.add_argument("--scan-limit", type=int, default=200)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    workspace = Path(args.workspace).resolve()
    extra = Path(args.extra_dir).resolve() if args.extra_dir else None
    rows = find_transcripts(
        workspace,
        args.prompt,
        home=Path(args.home).expanduser(),
        extra_dir=extra,
        scan_limit=args.scan_limit,
    )
    if not rows:
        print("No transcript matched this workspace. Pass a tight digest of the session.")
        return 2
    for path in rows:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
