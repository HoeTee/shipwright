#!/usr/bin/env python3
"""Prove the eval instruments before any paid run.

A reference answer must pass its hidden check. A known-bad answer must be
caught. The three injected bugs must be visible to a suite that actually
asserts the boundary.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mine_questions import inject_bug, test_strength
from stats import decide, summarize


FIXTURE = """
def score(n):
    if n < 0:
        return 0
    return n - 1
"""


def hidden_check(source: str) -> bool:
    namespace: dict = {}
    exec(source, namespace)
    fn = namespace["score"]
    return fn(-1) == 0 and fn(0) == -1 and fn(2) == 1


def suite_fails(source: str) -> bool:
    return not hidden_check(source)


def main() -> int:
    if not hidden_check(FIXTURE):
        print("selftest: reference answer failed its hidden check", file=sys.stderr)
        return 1
    broken = inject_bug(FIXTURE, "reversed-comparison")
    if broken is None or hidden_check(broken):
        print("selftest: known-bad answer was not caught", file=sys.stderr)
        return 1
    strength = test_strength(FIXTURE, suite_fails)
    if strength["caught_rate"] != 1:
        print(f"selftest: injected bugs were not all caught: {strength}", file=sys.stderr)
        return 1
    quality = summarize(
        {"clamp": ([1, 1, 1, 1, 1], [1, 1, 1, 1, 1])},
        lower_is_better=False,
        seed=1,
    )
    hard = summarize(
        {"clamp": ([8, 9, 8, 8, 10], [16, 15, 17, 16, 16])},
        lower_is_better=True,
        seed=1,
    )
    verdict = decide(
        quality=quality,
        hard=hard,
        limiter_named=True,
        settings_match=True,
        errors_checked=True,
        work_confirmed=True,
    )
    if verdict != "improved":
        print(f"selftest: expected improved, got {verdict}", file=sys.stderr)
        return 1
    missing = decide(
        quality=quality,
        hard=hard,
        limiter_named=False,
        settings_match=True,
        errors_checked=True,
        work_confirmed=True,
    )
    if missing != "inconclusive":
        print(f"selftest: missing limiter should be inconclusive, got {missing}", file=sys.stderr)
        return 1
    print("selftest: all instruments valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
