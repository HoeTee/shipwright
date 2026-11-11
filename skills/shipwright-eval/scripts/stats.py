#!/usr/bin/env python3
"""Median, geometric-mean ratio, and a 95% bootstrap interval for one eval."""

from __future__ import annotations

import math
import random
import statistics


def median(values: list[float]) -> float:
    return statistics.median(values)


def _spread(values: list[float]) -> float:
    return max(values) - min(values)


def geometric_mean(values: list[float]) -> float:
    return math.exp(statistics.mean(math.log(value) for value in values))


def summarize(per_task: dict, *, lower_is_better: bool = True, seed: int = 0, draws: int = 2000) -> dict:
    """per_task maps a task name to (experiment samples, control samples)."""
    rows = []
    ratios = []
    for name, pair in per_task.items():
        experiment, control = pair
        if not experiment or not control:
            raise ValueError(f"{name} needs samples on both arms")
        experiment_median = median(experiment)
        control_median = median(control)
        row = {
            "task": name,
            "experiment_median": experiment_median,
            "control_median": control_median,
            "experiment_range": (min(experiment), max(experiment)),
            "control_range": (min(control), max(control)),
            "measurable": abs(experiment_median - control_median) > max(_spread(experiment), _spread(control)),
        }
        if control_median == 0:
            row["ratio"] = None
        else:
            row["ratio"] = experiment_median / control_median
            ratios.append(row["ratio"])
        rows.append(row)
    if not ratios:
        return {
            "ratio": None,
            "range95": None,
            "crosses_one": True,
            "better_on": f"0 / {len(rows)}",
            "tasks": rows,
            "undefined": [row["task"] for row in rows],
        }
    generator = random.Random(seed)
    boots = sorted(
        geometric_mean(generator.choices(ratios, k=len(ratios)))
        for _ in range(draws)
    )
    low = int(draws * 0.025)
    high = int(draws * 0.975) - 1
    interval = (boots[low], boots[high])
    if lower_is_better:
        better = sum(ratio < 1 for ratio in ratios)
    else:
        better = sum(ratio > 1 for ratio in ratios)
    return {
        "ratio": geometric_mean(ratios),
        "range95": interval,
        "crosses_one": interval[0] <= 1 <= interval[1],
        "better_on": f"{better} / {len(ratios)}",
        "tasks": rows,
        "undefined": [row["task"] for row in rows if row["ratio"] is None],
    }


def _significant(summary: dict, *, want_below: bool) -> bool:
    if summary["ratio"] is None or summary["crosses_one"]:
        return False
    return summary["ratio"] < 1 if want_below else summary["ratio"] > 1


def decide(
    *,
    quality: dict,
    hard: dict,
    limiter_named: bool,
    settings_match: bool,
    errors_checked: bool,
    work_confirmed: bool,
) -> str:
    """quality is higher-is-better. hard is lower-is-better (tokens, lines, time)."""
    if not all((limiter_named, settings_match, errors_checked, work_confirmed)):
        return "inconclusive"
    quality_down = _significant(quality, want_below=True)
    quality_up = _significant(quality, want_below=False)
    hard_down = _significant(hard, want_below=True)
    hard_up = _significant(hard, want_below=False)
    if quality_down:
        return "regressed"
    if hard_down and not quality_down:
        return "improved"
    if quality_up and not hard_up:
        return "improved"
    if hard_up and not quality_up:
        return "regressed"
    return "no-measurable-difference"


def interleave(arms: list[str], tasks: list[str], repeats: int) -> list[dict]:
    """Alternate arms inside one run so time-of-day drift hits each arm alike."""
    order = []
    for rep in range(repeats):
        for task in tasks:
            for arm in arms:
                order.append({"arm": arm, "task": task, "rep": rep})
    return order
