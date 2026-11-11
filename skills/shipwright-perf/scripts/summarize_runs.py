#!/usr/bin/env python3
"""Median, range, and noise check for alternating before/after runs.

Question 5 of the benchmark checklist: a gap smaller than the run-to-run
variation is no measurable difference. Missing error or work counts make
the verdict inconclusive (questions 4 and 7).
"""

from __future__ import annotations

import argparse
import json
from statistics import median


def _spread(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    return max(values) - min(values)


def summarize(
    before: list[float],
    after: list[float],
    *,
    errors_before: int | None = None,
    errors_after: int | None = None,
    work_before: int | None = None,
    work_after: int | None = None,
    lower_is_better: bool = True,
) -> dict[str, object]:
    if not before or not after:
        raise SystemExit("both sides need at least one sample")
    med_before = float(median(before))
    med_after = float(median(after))
    variation = max(_spread(before), _spread(after))
    gap = abs(med_after - med_before)
    one_run = len(before) < 2 or len(after) < 2
    improved = med_after < med_before if lower_is_better else med_after > med_before
    blocking: list[str] = []
    notes: list[str] = []
    if errors_before is None or errors_after is None:
        blocking.append("error counts missing")
    elif errors_before or errors_after:
        notes.append(f"errors before={errors_before} after={errors_after}")
    if work_before is None or work_after is None:
        blocking.append("work counts missing")
    elif work_before <= 0 or work_after <= 0:
        blocking.append("work count is zero")
    if blocking:
        verdict = "inconclusive"
    elif gap <= variation:
        verdict = "no measurable difference"
    elif improved:
        verdict = "faster"
    else:
        verdict = "slower"
    delta = med_before - med_after if lower_is_better else med_after - med_before
    return {
        "median_before": med_before,
        "median_after": med_after,
        "range_before": [min(before), max(before)],
        "range_after": [min(after), max(after)],
        "variation": variation,
        "gap": gap,
        "delta": delta,
        "runs_before": len(before),
        "runs_after": len(after),
        "one_run": one_run,
        "lower_is_better": lower_is_better,
        "verdict": verdict,
        "reasons": blocking + notes,
    }


def _load_numbers(path: str) -> list[float]:
    values: list[float] = []
    for line in open(path, encoding="utf-8"):
        text = line.strip()
        if not text or text.startswith("#"):
            continue
        values.append(float(text.split()[0]))
    return values


def render(result: dict[str, object]) -> str:
    lines = [
        f"verdict: {result['verdict']}",
        f"median: {result['median_before']} → {result['median_after']}",
        f"delta: {result['delta']}",
        f"range before: {result['range_before'][0]} .. {result['range_before'][1]} ({result['runs_before']} runs)",
        f"range after: {result['range_after'][0]} .. {result['range_after'][1]} ({result['runs_after']} runs)",
        f"variation: {result['variation']}",
        "direction: lower is better" if result["lower_is_better"] else "direction: higher is better (faster means the after side is higher)",
    ]
    if result["one_run"]:
        lines.append("note: one side has a single run; say so if you report it as a ballpark.")
    for reason in result["reasons"]:
        lines.append(f"reason: {reason}")
    return "\n".join(lines)


def self_test() -> int:
    quiet = summarize([10, 11, 9, 10, 12], [10.2, 9.8, 10.1, 10.4, 9.9], errors_before=0, errors_after=0, work_before=5, work_after=5)
    assert quiet["verdict"] == "no measurable difference", quiet
    faster = summarize([40, 42, 39, 41, 40], [30, 31, 29, 32, 30], errors_before=0, errors_after=0, work_before=5, work_after=5)
    assert faster["verdict"] == "faster", faster
    missing = summarize([40, 42, 39], [30, 31, 29])
    assert missing["verdict"] == "inconclusive", missing
    zero_work = summarize([40, 42], [30, 31], errors_before=0, errors_after=0, work_before=0, work_after=3)
    assert zero_work["verdict"] == "inconclusive", zero_work
    higher = summarize([10, 11, 12], [20, 21, 19], errors_before=0, errors_after=0, work_before=1, work_after=1, lower_is_better=False)
    assert higher["verdict"] == "faster", higher
    print("summarize_runs self-test ok")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare alternating benchmark samples.")
    parser.add_argument("--before", help="File of before samples, one number per line")
    parser.add_argument("--after", help="File of after samples, one number per line")
    parser.add_argument("--json", dest="payload", help="JSON object with before, after, and optional counts")
    parser.add_argument("--higher-is-better", action="store_true")
    parser.add_argument("--errors-before", type=int)
    parser.add_argument("--errors-after", type=int)
    parser.add_argument("--work-before", type=int)
    parser.add_argument("--work-after", type=int)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    errors_before = args.errors_before
    errors_after = args.errors_after
    work_before = args.work_before
    work_after = args.work_after
    if args.payload:
        data = json.loads(args.payload)
        before = [float(item) for item in data["before"]]
        after = [float(item) for item in data["after"]]
        errors_before = data.get("errors_before", errors_before)
        errors_after = data.get("errors_after", errors_after)
        work_before = data.get("work_before", work_before)
        work_after = data.get("work_after", work_after)
    elif args.before and args.after:
        before = _load_numbers(args.before)
        after = _load_numbers(args.after)
    else:
        parser.error("pass --before and --after, or --json")
        return 2
    result = summarize(
        before,
        after,
        errors_before=errors_before,
        errors_after=errors_after,
        work_before=work_before,
        work_after=work_after,
        lower_is_better=not args.higher_is_better,
    )
    print(render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
