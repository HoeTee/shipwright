#!/usr/bin/env python3
"""Rank vetted audit findings by leverage.

Leverage is impact ÷ effort, discounted by confidence and by the risk of the
fix. Tiebreakers follow the audit rubric: unblockers first, then HIGH-confidence
security findings, then a clean verification story, then the score.

Impact, when it is a sentence, counts as MED unless it starts with HIGH, MED,
or LOW. The script says so on stderr.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

IMPACT = {"HIGH": 3.0, "MED": 2.0, "LOW": 1.0}
EFFORT = {"S": 1.0, "M": 2.0, "L": 3.0}
CONFIDENCE = {"HIGH": 1.0, "MED": 0.6, "LOW": 0.3}
RISK = {"LOW": 1.0, "MED": 0.7, "HIGH": 0.4}
HEADING = re.compile(r"^###\s+(.*)$")
FIELD = re.compile(r"^-\s+\*\*([^*]+)\*\*:\s*(.*)$")
LEVEL = re.compile(r"^(HIGH|MED|LOW)\b", re.IGNORECASE)


def parse(text: str) -> list[dict]:
    findings: list[dict] = []
    current: dict | None = None
    for line in text.splitlines():
        heading = HEADING.match(line)
        if heading:
            if current:
                findings.append(current)
            current = {"title": heading.group(1).strip(), "fields": {}}
            continue
        if current is None:
            continue
        field = FIELD.match(line)
        if field:
            current["fields"][field.group(1).strip().lower()] = field.group(2).strip()
    if current:
        findings.append(current)
    return findings


def level(value: str, table: dict[str, float], default: str) -> tuple[str, bool]:
    match = LEVEL.match(value.strip())
    token = match.group(1).upper() if match else default
    if token not in table:
        token = default
    return token, match is None


def score(finding: dict, notes: list[str]) -> tuple:
    fields = finding["fields"]
    impact, impact_defaulted = level(fields.get("impact", ""), IMPACT, "MED")
    if impact_defaulted:
        notes.append(f"{finding['title']}: impact has no HIGH/MED/LOW prefix, counted as MED")
    effort_token = fields.get("effort", "M").split()[0].upper().strip(".,")
    if effort_token not in EFFORT:
        effort_token = "M"
        notes.append(f"{finding['title']}: effort missing, counted as M")
    confidence_token = fields.get("confidence", "MED").split()[0].upper().strip(".,")
    if confidence_token not in CONFIDENCE:
        confidence_token = "MED"
    risk_token = fields.get("risk", "MED").split()[0].upper().strip(".,")
    if risk_token not in RISK:
        risk_token = "MED"
    value = (IMPACT[impact] / EFFORT[effort_token]) * CONFIDENCE[confidence_token] * RISK[risk_token]
    domain = fields.get("domain", "").split(",")[0].strip().lower()
    title = finding["title"].lower()
    if not domain and "security" in title:
        domain = "security"
    unblocks = fields.get("unblocks", "").lower().startswith("y")
    clean = fields.get("verification", "").lower().startswith("clean")
    security_high = domain == "security" and confidence_token == "HIGH"
    return (
        (0 if unblocks else 1, 0 if security_high else 1, 0 if clean else 1, -value),
        value,
        impact,
        effort_token,
        confidence_token,
        risk_token,
        domain,
    )


def rank(text: str) -> tuple[list[str], list[str]]:
    notes: list[str] = []
    ranked = []
    for finding in parse(text):
        key, value, impact, effort, confidence, risk, domain = score(finding, notes)
        ranked.append((key, value, finding["title"], impact, effort, confidence, risk, domain))
    ranked.sort(key=lambda item: item[0])
    lines = []
    for index, item in enumerate(ranked, start=1):
        _, value, title, impact, effort, confidence, risk, domain = item
        lines.append(
            f"{index}. {title}  score={value:.2f}  impact={impact}  effort={effort}  "
            f"confidence={confidence}  risk={risk}  domain={domain or '-'}"
        )
    return lines, notes


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path)
    args = parser.parse_args(argv)
    text = args.path.read_text(encoding="utf-8") if args.path else sys.stdin.read()
    lines, notes = rank(text)
    for note in notes:
        print(note, file=sys.stderr)
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
