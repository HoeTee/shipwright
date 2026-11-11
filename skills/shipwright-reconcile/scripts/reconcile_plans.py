#!/usr/bin/env python3
"""Read plans/README.md and report each plan's status.

This does not delete plan files and does not edit them. DONE still needs a
spot check. BLOCKED and stale IN PROGRESS are listed for the operator.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROW = re.compile(r"^\|\s*(\d+)\s*\|")
STATUSES = ("TODO", "IN PROGRESS", "DONE", "BLOCKED", "REJECTED")


def status_from_row(line: str) -> str | None:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    if len(cells) < 2:
        return None
    for cell in reversed(cells):
        for name in STATUSES:
            if cell.upper().startswith(name):
                return name
    return None


def scan(plans: Path) -> list[tuple[str, str, str]]:
    index = plans / "README.md"
    if not index.is_file():
        raise SystemExit(f"missing index: {index}")
    rows: list[tuple[str, str, str]] = []
    for line in index.read_text(encoding="utf-8").splitlines():
        if not ROW.match(line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        status = status_from_row(line) or "UNKNOWN"
        rows.append((cells[0], cells[1] if len(cells) > 1 else "", status))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plans", type=Path, default=Path("plans"))
    args = parser.parse_args()
    rows = scan(args.plans)
    attention = [row for row in rows if row[2] in {"BLOCKED", "IN PROGRESS", "UNKNOWN"}]
    print(f"plans {len(rows)}")
    for number, title, status in rows:
        print(f"{number}\t{status}\t{title}")
    if attention:
        print("attention")
        for number, _title, status in attention:
            print(f"{number}\t{status}")
    return None


if __name__ == "__main__":
    sys.exit(main())
