#!/usr/bin/env python3
"""Check a multi-PR lane plan. Disabled unless --enable is passed.

The upstream checker is scripts/check-plan.mjs. It stays off the default
path because it expects the upstream wording, including a host wake command.
This script checks the shipwright rules: ten live lanes, unit/live/perf
boxes, and a review gate. Passing it does not authorize a merge.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RULE = "Tests alone are not sufficient verification."
LANE = re.compile(r"Lane (\d+)\. ")
BOX = re.compile(r"^\s*- \[[ x]\] (.*)$")


def problems(text: str) -> list[str]:
    found: list[str] = []
    if RULE not in text:
        found.append("missing the unit/live/perf verification sentence")
    numbers = sorted(int(match) for match in LANE.findall(text))
    if numbers != list(range(1, 11)):
        found.append(f"lanes are {numbers}, expected 1 through 10")
    for label in ("Verify, unit.", "Verify, live.", "Verify, perf."):
        if label not in text:
            found.append(f"missing {label}")
    if "/tmp/shipwright-" not in text:
        found.append("live lanes must store screenshots under /tmp/shipwright-<plan>/<sha7>/")
    if "Review gate." not in text:
        found.append("missing Review gate.")
    elif "None." not in text.split("Review gate.", 1)[1][:80]:
        gate = text.split("Review gate.", 1)[1]
        for word in ("screenshot", "video", "operator"):
            if word not in gate:
                found.append(f"review gate lacks {word}")
    if not any(BOX.match(line) for line in text.splitlines()):
        found.append("no evidence boxes")
    return found


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, nargs="?")
    parser.add_argument("--enable", action="store_true")
    args = parser.parse_args()
    if not args.enable:
        print("disabled: multi-PR lane checks stay off unless the operator enables them (--enable)")
        return
    if args.plan is None:
        raise SystemExit("pass the plan file")
    found = problems(args.plan.read_text(encoding="utf-8"))
    if found:
        for item in found:
            print(item, file=sys.stderr)
        raise SystemExit(1)
    print("lanes ok")


if __name__ == "__main__":
    main()
