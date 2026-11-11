"""Tests for question mining and injected-bug strength."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from mine_questions import inject_bug, is_test_path, mine_tasks, test_strength, write_bank


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def _commit(repo: Path, message: str, files: dict[str, str]) -> str:
    for name, body in files.items():
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        _git(repo, "add", name)
    _git(repo, "commit", "-m", message)
    return _git(repo, "rev-parse", "HEAD").strip()


class MineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        _git(self.repo, "init")
        _git(self.repo, "config", "user.email", "test@example.com")
        _git(self.repo, "config", "user.name", "Test")
        self.feature = _commit(
            self.repo,
            "feat: add checkout",
            {"app.py": "def price(n):\n    return n\n", "tests/test_app.py": "def test_price():\n    assert True\n"},
        )
        self.refactor = _commit(
            self.repo,
            "refactor: extract price helper",
            {"app.py": "def price(n):\n    return n * 1\n"},
        )
        self.fix = _commit(
            self.repo,
            "fix: tax rounds the wrong way",
            {
                "app.py": "def price(n):\n    return n\n",
                "tests/test_app.py": "def test_price():\n    assert price(1) == 1\n",
            },
        )
        self.bad = _commit(self.repo, "feat: add util", {"util.py": "def util():\n    return 1\n"})
        _git(self.repo, "revert", "--no-edit", self.bad)
        self.stable = _commit(self.repo, "feat: add stable helper", {"stable.py": "def stable():\n    return 1\n"})

    def tearDown(self):
        self.tmp.cleanup()

    def test_kinds(self):
        tasks = mine_tasks(str(self.repo), limit=20)
        kinds = {(task["kind"], task["raw_subject"]) for task in tasks}
        self.assertIn(("feature", "feat: add checkout"), kinds)
        self.assertIn(("refactor", "refactor: extract price helper"), kinds)
        self.assertIn(("bugfix", "fix: tax rounds the wrong way"), kinds)
        self.assertIn(("review-bad", "feat: add util"), kinds)
        clean = [task for task in tasks if task["kind"] == "review-clean" and task["raw_subject"].startswith("feat: add stable")]
        self.assertTrue(clean)
        self.assertEqual(clean[0]["ci"], "unknown")

    def test_bugfix_shape(self):
        bug = next(task for task in mine_tasks(str(self.repo)) if task["kind"] == "bugfix")
        self.assertEqual(bug["reference"], self.fix)
        self.assertEqual(bug["start_from"], f"{self.fix}^")
        self.assertIn("tests/test_app.py", bug["hidden_tests"])

    def test_sensitive_flag_and_markdown(self):
        _commit(self.repo, "fix: rotate api_key handling", {"tests/test_keys.py": "def test_k():\n    assert True\n", "keys.py": "x = 1\n"})
        dest = self.repo / "out"
        payload = write_bank(str(self.repo), dest, limit=20)
        self.assertTrue(any(task["possible_sensitive"] for task in payload["tasks"]))
        self.assertIn("Question bank candidates", (dest / "candidates.md").read_text(encoding="utf-8"))

    def test_path_heuristic(self):
        self.assertTrue(is_test_path("tests/test_app.py"))
        self.assertFalse(is_test_path("app.py"))


class InjectTests(unittest.TestCase):
    def test_each_mutation_changes_source_and_can_miss(self):
        source = "def clamp(n):\n    if n < 0:\n        return 0\n    if n > 10:\n        return 10\n    return n\n"
        for kind in ("reversed-comparison", "dropped-if", "off-by-one"):
            mutated = inject_bug(source, kind)
            self.assertIsNotNone(mutated)
            self.assertNotEqual(mutated, source)
        self.assertIsNone(inject_bug("def f():\n    return 1\n", "reversed-comparison"))

        def never(_source):
            return False

        report = test_strength(source, never)
        self.assertEqual(report["caught_rate"], 0)
        self.assertEqual(test_strength("def f():\n    return 1\n", never)["caught_rate"], None)


if __name__ == "__main__":
    unittest.main()
