#!/usr/bin/env python3
"""Classify one CI failure before any retry.

Rules from the babysit procedure:

- A flake or infrastructure failure gets one fresh build, not a job retry.
- The same failure a second time is not a flake.
- A failure outside the diff is a stale base when the target is not an ancestor
  of HEAD. Do not spend the retry on it.
- Only a failure in the diff's own code gets a commit.
"""

from __future__ import annotations

import argparse
import json


def classify(touches_diff: bool, repeat: bool, infrastructure: bool, ancestor: str) -> dict[str, str]:
    if ancestor not in {"yes", "no", "unknown"}:
        raise SystemExit("ancestor must be yes, no, or unknown")
    if repeat:
        return {
            "class": "not-flake",
            "action": "read the child logs and reclassify; do not retry the same failure again",
        }
    if not touches_diff:
        if ancestor == "no":
            return {
                "class": "stale-base",
                "action": "report the branch that needs a rebase; do not retry and do not commit",
            }
        if ancestor == "yes":
            return {
                "class": "outside-diff",
                "action": "the failing code is not in this diff and the base is current; do not commit a speculative fix",
            }
        return {
            "class": "unknown",
            "action": "run git merge-base --is-ancestor on the target before calling this a flake",
        }
    if infrastructure:
        return {
            "class": "retry-once",
            "action": "one fresh build only; a second identical failure is not a flake",
        }
    return {
        "class": "fix-in-diff",
        "action": "the failure is in the diff; fix it with a commit after reading the log",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--touches-diff", choices=("yes", "no"), required=True)
    parser.add_argument("--repeat", choices=("yes", "no"), default="no")
    parser.add_argument("--infrastructure", choices=("yes", "no"), default="no")
    parser.add_argument("--ancestor", choices=("yes", "no", "unknown"), default="unknown")
    args = parser.parse_args()
    result = classify(
        args.touches_diff == "yes",
        args.repeat == "yes",
        args.infrastructure == "yes",
        args.ancestor,
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
