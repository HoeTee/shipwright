"""Lane checks stay disabled until the operator passes --enable."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check_lanes.py")
GOOD = """
Tests alone are not sufficient verification.
**Verify, unit.**
**Verify, live.**
**Verify, perf.**
- [ ] Lane 1. Save `/tmp/shipwright-001/e4f5a6b/lane01-checkout.png`.
- [ ] Lane 2. Save `/tmp/shipwright-001/e4f5a6b/lane02-checkout.png`.
- [ ] Lane 3. Save `/tmp/shipwright-001/e4f5a6b/lane03-checkout.png`.
- [ ] Lane 4. Save `/tmp/shipwright-001/e4f5a6b/lane04-checkout.png`.
- [ ] Lane 5. Save `/tmp/shipwright-001/e4f5a6b/lane05-checkout.png`.
- [ ] Lane 6. Save `/tmp/shipwright-001/e4f5a6b/lane06-checkout.png`.
- [ ] Lane 7. Save `/tmp/shipwright-001/e4f5a6b/lane07-checkout.png`.
- [ ] Lane 8. Save `/tmp/shipwright-001/e4f5a6b/lane08-checkout.png`.
- [ ] Lane 9. Save `/tmp/shipwright-001/e4f5a6b/lane09-checkout.png`.
- [ ] Lane 10. Save `/tmp/shipwright-001/e4f5a6b/lane10-checkout.png`.
**Review gate.**
screenshot
video
operator
"""


class LaneTests(unittest.TestCase):
    def test_default_is_disabled(self):
        result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("disabled", result.stdout)

    def test_enable_accepts_ten_lanes(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "plan.md"
            plan.write_text(GOOD, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--enable", str(plan)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("lanes ok", result.stdout)


if __name__ == "__main__":
    unittest.main()
