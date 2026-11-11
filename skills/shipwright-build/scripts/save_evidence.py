#!/usr/bin/env python3
"""Store one evidence file under /tmp/shipwright-<plan>/<sha7>/.

The directory is outside the git repo. This script copies a file into the
naming scheme and appends a row to index.md. It does not upload a PR
attachment and it does not commit anything.
"""

from __future__ import annotations

import argparse
import re
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

KINDS = {"before", "after", "variant-a", "variant-b", "baseline", "diff", "review"}
LANE = re.compile(r"lane(0[1-9]|10)\Z")
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
CST = timezone(timedelta(hours=8))


def evidence_dir(plan: str, sha: str, root: Path) -> Path:
    folder = root / f"shipwright-{plan}" / sha[:7]
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def check_kind(kind: str) -> str:
    if kind in KINDS or LANE.fullmatch(kind):
        return kind
    raise SystemExit(f"unknown kind {kind!r}")


def check_slug(slug: str) -> str:
    if SLUG.fullmatch(slug):
        return slug
    raise SystemExit(f"slug must be lowercase english words and hyphens, got {slug!r}")


def record(
    plan: str,
    sha: str,
    kind: str,
    slug: str,
    source: Path,
    proves: str,
    action: str,
    root: Path,
    aria: str | None = None,
) -> Path:
    kind = check_kind(kind)
    slug = check_slug(slug)
    if not source.is_file():
        raise SystemExit(f"source is not a file: {source}")
    folder = evidence_dir(plan, sha, root)
    dest = folder / f"{kind}-{slug}{source.suffix.lower()}"
    shutil.copyfile(source, dest)
    if aria is not None:
        (folder / f"{kind}-{slug}.aria.txt").write_text(aria, encoding="utf-8")
    when = datetime.now(CST).strftime("%Y-%m-%d %H:%M UTC+8")
    index = folder / "index.md"
    if not index.exists():
        index.write_text("# Evidence index\n\n| File | Proves | Action | Time |\n| --- | --- | --- | --- |\n", encoding="utf-8")
    row = f"| `{dest.name}` | {proves.replace('|', '/')} | {action.replace('|', '/')} | {when} |\n"
    with index.open("a", encoding="utf-8") as handle:
        handle.write(row)
    return dest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--sha", required=True)
    parser.add_argument("--kind", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--proves", required=True)
    parser.add_argument("--action", required=True)
    parser.add_argument("--aria-file", type=Path)
    parser.add_argument("--root", type=Path, default=Path("/tmp"))
    args = parser.parse_args()
    aria = args.aria_file.read_text(encoding="utf-8") if args.aria_file else None
    dest = record(args.plan, args.sha, args.kind, args.slug, args.source, args.proves, args.action, args.root, aria)
    print(dest)


if __name__ == "__main__":
    main()
