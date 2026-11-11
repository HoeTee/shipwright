#!/usr/bin/env python3
"""Fail when a rule table is enforced only by prose.

The prevent skill keeps a markdown table with English headings
`Rule` and `Enforcement`. Docs, comments, and reminders do not count.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PROSE = re.compile(
    r"^(docs?|prose|instruction|instructions|comment|comments|reminder|reminders|"
    r"text|documentation|agent rules?|note|notes|none|n/a|—|-|\(none\))$",
    re.IGNORECASE,
)


def split_row(line: str) -> list[str]:
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|"):
        text = text[:-1]
    return [cell.strip() for cell in text.split("|")]


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def find_weak_rows(markdown: str) -> list[str]:
    lines = markdown.splitlines()
    weak: list[str] = []
    index = 0
    while index < len(lines):
        cells = split_row(lines[index]) if lines[index].strip().startswith("|") else []
        if cells and "Rule" in cells and "Enforcement" in cells and index + 1 < len(lines):
            separator = split_row(lines[index + 1])
            if is_separator(separator):
                rule_at = cells.index("Rule")
                enforce_at = cells.index("Enforcement")
                index += 2
                while index < len(lines) and lines[index].strip().startswith("|"):
                    row = split_row(lines[index])
                    if len(row) > max(rule_at, enforce_at):
                        rule = row[rule_at]
                        enforcement = row[enforce_at]
                        if rule and (not enforcement or PROSE.fullmatch(enforcement)):
                            weak.append(f"{rule} → {enforcement or '(empty)'}")
                    index += 1
                continue
        index += 1
    return weak


def self_test() -> int:
    sample = """
# Rules

| Rule | Enforcement |
| --- | --- |
| One owner for order status | import of order.internal fails the build |
| Remember to check auth | docs |

| Other | Columns |
| --- | --- |
| skip | docs |
"""
    weak = find_weak_rows(sample)
    assert weak == ["Remember to check auth → docs"], weak
    assert find_weak_rows("| Rule | Enforcement |\n| --- | --- |\n| Typed ids | UserId is not OrderId |\n") == []
    print("check_rule_table self-test ok")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Flag rule-table rows enforced only by prose.")
    parser.add_argument("path", nargs="?", help="Markdown file. Default: stdin")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    markdown = sys.stdin.read() if not args.path else Path(args.path).read_text(encoding="utf-8")
    weak = find_weak_rows(markdown)
    if not weak:
        print("Rule table: every listed rule names a structural enforcement.")
        return 0
    print("Prose-only rules:")
    for item in weak:
        print(f"- {item}")
    print("Encode these at a higher level, or drop them from the table.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
