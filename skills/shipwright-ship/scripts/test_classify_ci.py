"""CI classification: one retry, then a real cause."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("classify_ci.py")


def run(**kwargs: str) -> dict[str, str]:
    args = [sys.executable, str(SCRIPT)]
    for key, value in kwargs.items():
        args.extend(["--" + key.replace("_", "-"), value])
    result = subprocess.run(args, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


class ClassifyTests(unittest.TestCase):
    def test_infrastructure_retries_once(self):
        self.assertEqual(run(touches_diff="yes", infrastructure="yes")["class"], "retry-once")

    def test_second_failure_is_not_a_flake(self):
        self.assertEqual(run(touches_diff="yes", infrastructure="yes", repeat="yes")["class"], "not-flake")

    def test_untouched_code_with_a_moved_base_is_stale(self):
        self.assertEqual(run(touches_diff="no", ancestor="no")["class"], "stale-base")

    def test_diff_failure_gets_a_commit(self):
        self.assertEqual(run(touches_diff="yes", ancestor="yes")["class"], "fix-in-diff")


if __name__ == "__main__":
    unittest.main()
