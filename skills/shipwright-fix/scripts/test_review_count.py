"""The AI review cap is counted from PR open and is not reset."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("review_count.py")
PLAN = """# Plan 001: Example

## Run record

- **Pre-PR iterations**: 2
- **AI reviews since PR**: 0 / 3
"""


class ReviewCountTests(unittest.TestCase):
    def run_script(self, plan: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(plan), *args],
            capture_output=True,
            text=True,
        )

    def test_pre_pr_iteration_does_not_touch_the_review_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "001.md"
            plan.write_text(PLAN, encoding="utf-8")
            result = self.run_script(plan, "--bump-iteration")
            self.assertEqual(result.returncode, 0, result.stderr)
            text = plan.read_text(encoding="utf-8")
            self.assertIn("**Pre-PR iterations**: 3", text)
            self.assertIn("**AI reviews since PR**: 0 / 3", text)

    def test_cap_stops_the_fourth_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "001.md"
            plan.write_text(PLAN.replace("0 / 3", "3 / 3"), encoding="utf-8")
            result = self.run_script(plan, "--bump-review")
            self.assertEqual(result.returncode, 2)
            self.assertIn("cap reached", result.stderr)
            self.assertIn("**AI reviews since PR**: 3 / 3", plan.read_text(encoding="utf-8"))

    def test_verbal_override_raises_the_denominator(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "001.md"
            plan.write_text(PLAN.replace("0 / 3", "3 / 3"), encoding="utf-8")
            result = self.run_script(plan, "--bump-review", "--cap", "4")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("**AI reviews since PR**: 4 / 4", plan.read_text(encoding="utf-8"))

    def test_count_increments_and_keeps_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "001.md"
            plan.write_text(PLAN, encoding="utf-8")
            first = self.run_script(plan, "--bump-review")
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertIn("1 / 3", plan.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
