"""find_sessions.py stays inside one workspace and orders by mtime."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("find_sessions.py")


class FindSessionsTests(unittest.TestCase):
    def test_lists_this_workspace_and_skips_another(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            workspace = Path(tmp) / "proj"
            other = Path(tmp) / "other"
            workspace.mkdir()
            other.mkdir()
            slug = "".join(character if character.isalnum() else "-" for character in workspace.resolve().as_posix())
            claude_dir = home / ".claude" / "projects" / slug
            claude_dir.mkdir(parents=True)
            older = claude_dir / "old.jsonl"
            newer = claude_dir / "new.jsonl"
            older.write_text("{}\n", encoding="utf-8")
            newer.write_text("{}\n", encoding="utf-8")
            os.utime(older, (1_700_000_000, 1_700_000_000))
            os.utime(newer, (1_700_000_100, 1_700_000_100))
            other_slug = "".join(character if character.isalnum() else "-" for character in other.resolve().as_posix())
            other_dir = home / ".claude" / "projects" / other_slug
            other_dir.mkdir(parents=True)
            (other_dir / "secret.jsonl").write_text("{}\n", encoding="utf-8")

            codex = home / ".codex" / "sessions" / "2026" / "11" / "11"
            codex.mkdir(parents=True)
            match = codex / "rollout-match.jsonl"
            match.write_text(json.dumps({"payload": {"cwd": str(workspace.resolve())}}) + "\n", encoding="utf-8")
            miss = codex / "rollout-miss.jsonl"
            miss.write_text(json.dumps({"payload": {"cwd": str(other.resolve())}}) + "\n", encoding="utf-8")
            now = time.time()
            os.utime(match, (now, now))
            os.utime(miss, (now, now))

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--home",
                    str(home),
                    "--workspace",
                    str(workspace),
                    "--all-time",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("new.jsonl", result.stdout)
            self.assertIn("rollout-match.jsonl", result.stdout)
            self.assertNotIn("secret.jsonl", result.stdout)
            self.assertNotIn("rollout-miss.jsonl", result.stdout)
            self.assertLess(result.stdout.index("rollout-match.jsonl"), result.stdout.index("new.jsonl"))
            self.assertIn("3 session files", result.stderr)


if __name__ == "__main__":
    unittest.main()
