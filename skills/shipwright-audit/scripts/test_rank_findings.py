"""rank_findings.py orders by the audit rubric, not by input order."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("rank_findings.py")

SAMPLE = """### [P2][structure] Rename a helper
- **Evidence**: `src/a.py:1` — name
- **Impact**: LOW cosmetic
- **Effort**: S
- **Risk**: LOW
- **Confidence**: HIGH
- **Domain**: structure

### [P1][security] Check the download owner
- **Evidence**: `api/orders.py:88` — no owner check
- **Impact**: HIGH other users can download
- **Effort**: S
- **Risk**: LOW
- **Confidence**: HIGH
- **Domain**: security

### [P1][test] Add a verification baseline
- **Evidence**: `package.json:1` — no test script
- **Impact**: HIGH nothing can be checked
- **Effort**: M
- **Risk**: LOW
- **Confidence**: HIGH
- **Domain**: test
- **Unblocks**: yes
"""


class RankFindingsTests(unittest.TestCase):
    def test_unblocked_security_beats_a_cosmetic_fix(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "findings.md"
            path.write_text(SAMPLE, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        titles = [line.split("  ")[0] for line in result.stdout.splitlines()]
        self.assertTrue(titles[0].endswith("Add a verification baseline") or "verification baseline" in titles[0])
        self.assertLess(result.stdout.index("download owner"), result.stdout.index("Rename a helper"))
        self.assertLess(result.stdout.index("verification baseline"), result.stdout.index("download owner"))


if __name__ == "__main__":
    unittest.main()
