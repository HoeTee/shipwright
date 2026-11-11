"""patch-id survives a rebase that does not change the patch."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("patch_id.py")


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True)
    return result.stdout.strip()


class PatchIdTests(unittest.TestCase):
    def test_same_patch_and_code_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.check_call(["git", "init", "-q", str(repo)])
            git(repo, "config", "user.email", "shipwright@example.com")
            git(repo, "config", "user.name", "shipwright")
            (repo / "app.py").write_text("VALUE = 1\n", encoding="utf-8")
            git(repo, "add", "app.py")
            git(repo, "commit", "-q", "-m", "base")
            (repo / "app.py").write_text("VALUE = 2\n", encoding="utf-8")
            git(repo, "commit", "-q", "-am", "change")
            first = git(repo, "rev-parse", "HEAD")
            git(repo, "checkout", "-q", "-b", "replay", "HEAD~1")
            (repo / "app.py").write_text("VALUE = 2\n", encoding="utf-8")
            git(repo, "commit", "-q", "-am", "replay")
            second = git(repo, "rev-parse", "HEAD")
            same = subprocess.run(
                [sys.executable, str(SCRIPT), first, second, "--repo", str(repo)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(same.returncode, 0, same.stderr)
            self.assertIn("SAME", same.stdout)
            (repo / "app.py").write_text("VALUE = 3\n", encoding="utf-8")
            git(repo, "commit", "-q", "-am", "other")
            third = git(repo, "rev-parse", "HEAD")
            changed = subprocess.run(
                [sys.executable, str(SCRIPT), first, third, "--repo", str(repo)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(changed.returncode, 1)
            self.assertIn("DIFFERENT", changed.stdout)


if __name__ == "__main__":
    unittest.main()
