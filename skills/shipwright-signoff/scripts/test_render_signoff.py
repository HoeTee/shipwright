"""The signoff draft is HTML input and does not require a screenshot."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("render_signoff.py")


class RenderSignoffTests(unittest.TestCase):
    def test_draft_contains_the_packet_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            draft = Path(tmp) / "packet.md"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--draft-only",
                    "--draft",
                    str(draft),
                    "--sha",
                    "e4f5a6b",
                    "--findings",
                    "P0: 0 · P1: 1 · P2: 0",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            text = draft.read_text(encoding="utf-8")
            self.assertIn("## A Decision", text)
            self.assertIn("e4f5a6b", text)
            self.assertIn("P0: 0 · P1: 1 · P2: 0", text)
            self.assertIn("template: sheet", text)


if __name__ == "__main__":
    unittest.main()
