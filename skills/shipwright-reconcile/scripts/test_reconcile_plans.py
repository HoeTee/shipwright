"""The reconcile report keeps every status and flags blocked work."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("reconcile_plans.py")
INDEX = """# Plans

| Plan | Title | Priority | Effort | Depends on | Domains | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 001 | Close the day | P1 | S | — | bugs | DONE |
| 002 | Refresh excerpts | P2 | S | 001 | bugs | TODO |
| 003 | Stuck migration | P1 | M | — | structure | BLOCKED |
"""


class ReconcileTests(unittest.TestCase):
    def test_lists_statuses(self):
        with tempfile.TemporaryDirectory() as tmp:
            plans = Path(tmp)
            (plans / "README.md").write_text(INDEX, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--plans", str(plans)],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("001\tDONE\tClose the day", result.stdout)
            self.assertIn("003\tBLOCKED\tStuck migration", result.stdout)
            self.assertIn("attention", result.stdout)


if __name__ == "__main__":
    unittest.main()
