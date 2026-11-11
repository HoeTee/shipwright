#!/usr/bin/env python3
"""Update AI-review accounting on one plan file.

The default cap is 3. It is defined only in shipwright-fix. Counting starts
when the PR is opened and never resets. Pre-PR iterations are a different
counter. A verbal override is `--cap N` on this task's plan file.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DEFAULT_CAP = 3
ITER = re.compile(r"^(- \*\*Pre-PR iterations\*\*:\s*)(\d+)\s*$", re.M)
REVIEWS = re.compile(r"^(- \*\*AI reviews since PR\*\*:\s*)(\d+)\s*/\s*(\d+)\s*$", re.M)


def read_plan(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"plan not found: {path}")
    return path.read_text(encoding="utf-8")


def status(text: str) -> tuple[int, int, int]:
    iterations = ITER.search(text)
    reviews = REVIEWS.search(text)
    if not iterations or not reviews:
        raise SystemExit("plan is missing Pre-PR iterations or AI reviews since PR")
    return int(iterations.group(2)), int(reviews.group(2)), int(reviews.group(3))


def write_status(text: str, iterations: int, count: int, cap: int) -> str:
    text, n1 = ITER.subn(rf"\g<1>{iterations}", text, count=1)
    text, n2 = REVIEWS.subn(rf"\g<1>{count} / {cap}", text, count=1)
    if n1 != 1 or n2 != 1:
        raise SystemExit("failed to update the Run record counters")
    return text


def bump_iteration(path: Path) -> str:
    text = read_plan(path)
    iterations, count, cap = status(text)
    text = write_status(text, iterations + 1, count, cap)
    path.write_text(text, encoding="utf-8")
    return f"pre-pr-iterations {iterations + 1}; ai-reviews {count} / {cap}"


def bump_review(path: Path, cap_override: int | None) -> str:
    text = read_plan(path)
    iterations, count, cap = status(text)
    if cap_override is not None:
        if cap_override < 1:
            raise SystemExit("cap must be at least 1")
        cap = cap_override
    if count >= cap:
        path.write_text(write_status(text, iterations, count, cap), encoding="utf-8")
        raise SystemExit(
            f"cap reached: {count} / {cap}. Stop the automatic fix loop and write the bounded retrospective. "
            "A further review needs an explicit new plan and a new authorization. "
            f"The default cap is {DEFAULT_CAP} and lives only in shipwright-fix."
        )
    text = write_status(text, iterations, count + 1, cap)
    path.write_text(text, encoding="utf-8")
    return f"pre-pr-iterations {iterations}; ai-reviews {count + 1} / {cap}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--show", action="store_true")
    parser.add_argument("--bump-iteration", action="store_true")
    parser.add_argument("--bump-review", action="store_true")
    parser.add_argument("--cap", type=int, help="verbal override for this task; recorded as the denominator")
    args = parser.parse_args()
    chosen = sum(bool(flag) for flag in (args.show, args.bump_iteration, args.bump_review))
    if chosen != 1:
        parser.error("choose one of --show, --bump-iteration, --bump-review")
    if args.show:
        iterations, count, cap = status(read_plan(args.plan))
        if args.cap is not None:
            cap = args.cap
        print(f"pre-pr-iterations {iterations}; ai-reviews {count} / {cap}; default-cap {DEFAULT_CAP}")
        return
    if args.cap is not None and not args.bump_review:
        parser.error("--cap is only valid with --bump-review or --show")
    if args.bump_iteration:
        print(bump_iteration(args.plan))
        return
    try:
        print(bump_review(args.plan, args.cap))
    except SystemExit as exc:
        if exc.code not in (None, 0):
            print(exc.code, file=sys.stderr)
            raise SystemExit(2) from None
        raise


if __name__ == "__main__":
    main()
