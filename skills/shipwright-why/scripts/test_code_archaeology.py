"""code_archaeology.py runs read-only git searches against a temp repo."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("code_archaeology.py")


def run(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo", str(repo), *args],
        capture_output=True,
        text=True,
        check=False,
    )


class CodeArchaeologyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.repo = Path(self.directory.name)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "a@example.com"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Arch"], cwd=self.repo, check=True)
        source = self.repo / "billing.py"
        source.write_text("limit = 50\n# TODO: clamp\n", encoding="utf-8")
        note = self.repo / "docs" / "adr" / "0001.md"
        note.parent.mkdir(parents=True)
        note.write_text("architecture decision: clamp at 50\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "clamp at 50"], cwd=self.repo, check=True)
        source.write_text("limit = 100\n# TODO: clamp\n", encoding="utf-8")
        subprocess.run(["git", "commit", "-aq", "-m", "raise the clamp"], cwd=self.repo, check=True)

    def tearDown(self) -> None:
        self.directory.cleanup()

    def test_follow_and_pickaxe_see_the_change(self):
        follow = run(self.repo, "follow", "billing.py")
        self.assertEqual(follow.returncode, 0, follow.stderr)
        self.assertIn("raise the clamp", follow.stdout)
        pickaxe = run(self.repo, "pickaxe", "--text", "limit = 100", "billing.py")
        self.assertEqual(pickaxe.returncode, 0, pickaxe.stderr)
        self.assertIn("raise the clamp", pickaxe.stdout)

    def test_blame_and_hints(self):
        blame = run(self.repo, "blame", "--start", "1", "--end", "2", "billing.py")
        self.assertEqual(blame.returncode, 0, blame.stderr)
        self.assertIn("limit = 100", blame.stdout)
        hints = run(self.repo, "hints", "--symbol", "limit", "billing.py")
        self.assertEqual(hints.returncode, 0, hints.stderr)
        self.assertIn("0001.md", hints.stdout)
        self.assertIn("TODO", hints.stdout)

    def test_refuses_a_revision_with_spaces(self):
        result = run(self.repo, "show", "HEAD; rm -rf /")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("refusing revision", result.stderr)

    def test_refuses_a_non_repo(self):
        with tempfile.TemporaryDirectory() as empty:
            result = run(Path(empty), "follow", "billing.py")
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
