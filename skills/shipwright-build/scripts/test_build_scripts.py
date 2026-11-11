"""Tests for the build evidence path and code map."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from code_map import scan
from save_evidence import record


class SaveEvidenceTests(unittest.TestCase):
    def test_names_and_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "shot.png"
            source.write_bytes(b"png")
            dest = record(
                "001",
                "e4f5a6b999",
                "after",
                "order-list",
                source,
                "order list after the fix",
                "open the order list",
                root / "evidence-root",
                aria="heading: Orders",
            )
            self.assertEqual(dest.name, "after-order-list.png")
            self.assertTrue(dest.is_file())
            folder = dest.parent
            self.assertEqual(folder.name, "e4f5a6b")
            self.assertIn("after-order-list.aria.txt", {p.name for p in folder.iterdir()})
            index = (folder / "index.md").read_text(encoding="utf-8")
            self.assertIn("after-order-list.png", index)
            self.assertIn("UTC+8", index)

    def test_rejects_bad_slug(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "a.txt"
            source.write_text("x", encoding="utf-8")
            with self.assertRaises(SystemExit):
                record("001", "abcdef0", "before", "Bad Name", source, "x", "y", root)


class CodeMapTests(unittest.TestCase):
    def test_lists_python_functions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "billing.py").write_text(
                "class Day:\n    def close(self):\n        return 1\n\ndef unused():\n    return 0\n",
                encoding="utf-8",
            )
            text = "\n".join(scan(root))
            self.assertIn("class Day", text)
            self.assertIn("method Day.close", text)
            self.assertIn("function unused", text)


if __name__ == "__main__":
    unittest.main()
