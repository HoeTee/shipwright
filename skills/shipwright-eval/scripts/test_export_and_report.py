"""Tests for a git-free workspace export and the HTML report."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from export_workspace import export_workspace
from render_report import render_html, render_plan


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


class ExportTests(unittest.TestCase):
    def test_export_has_no_git_and_drops_hidden_tests(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            _git(repo, "init")
            _git(repo, "config", "user.email", "test@example.com")
            _git(repo, "config", "user.name", "Test")
            (repo / "app.py").write_text("x = 1\n", encoding="utf-8")
            (repo / "plans").mkdir()
            (repo / "plans" / "secret.md").write_text("answer\n", encoding="utf-8")
            (repo / "tests").mkdir()
            (repo / "tests" / "test_app.py").write_text("assert False\n", encoding="utf-8")
            _git(repo, "add", ".")
            _git(repo, "commit", "-m", "feat: seed")
            sha = _git(repo, "rev-parse", "HEAD").strip()
            dest = Path(tmp) / "order-service"
            export_workspace(str(repo), sha, dest, drop=["tests/test_app.py"])
            self.assertFalse((dest / ".git").exists())
            self.assertFalse((dest / "plans").exists())
            self.assertFalse((dest / "tests" / "test_app.py").exists())
            self.assertEqual((dest / "app.py").read_text(encoding="utf-8"), "x = 1\n")
            with self.assertRaises(FileExistsError):
                export_workspace(str(repo), sha, dest)


class ReportTests(unittest.TestCase):
    def test_html_escapes_and_plan_stores_the_verdict(self):
        report = {
            "title": "review <skill>",
            "claim": "tokens & quality",
            "verdict": "improved",
            "plan": "012",
            "mode": "with-without",
            "control": "no skill",
            "n": 5,
            "questions": [{"question": "Did it even happen?", "answer": "yes <log>"}],
            "tasks": [],
            "both_perfect": [],
            "limitations": [],
            "quality": {"ratio": 1},
            "hard": {"ratio": 0.8},
        }
        page = render_html(report)
        self.assertIn("review &lt;skill&gt;", page)
        self.assertNotIn("<skill>", page)
        self.assertIn("<h2>Verdict</h2>", page)
        plan = render_plan(report)
        self.assertIn("**Category**: eval", plan)
        self.assertIn("**Verdict**: improved", plan)
        json.dumps(report)


if __name__ == "__main__":
    unittest.main()
