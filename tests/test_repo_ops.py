"""Repo-ops intake: module coverage, issue forms, and the label script."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CI_COMMANDS = (
    "python -B -m unittest discover -s scripts -v",
    "python -B -m unittest discover -s tests -v",
    "python -B -m unittest discover -s skills/shipwright-eval/scripts -v",
    "python -B skills/shipwright-eval/scripts/selftest.py",
    "bun test skills/shipwright-autopilot/scripts/check-plan.test.ts",
)
REQUIRED_LABELS = (
    "triage",
    "needs-info",
    "agent:ready",
    "agent:running",
    "blocked",
    "touches:shared",
    "eval",
)

COMPLETE_BUG = """\
### Summary

Opening the catalog misses one skill directory.

### Steps to reproduce

1. Open skills/index.json.
2. Compare it with the directories under skills/.

### Expected result

Every skill directory is listed.

### Module

skills

### Non-goals

_No response_
"""

INCOMPLETE = """\
### Summary

_No response_

### Acceptance criteria

A reader can find the intake doc from the contributing guide.

### Expected result

The contributing guide links to the intake doc.

### Module

not-a-module

### Non-goals

Do not edit the four READMEs.
"""

MODULE_ONLY_IN_SUMMARY = """\
### Summary

The module is skills. Run the checks.

### Steps to reproduce

1. Run the tests.

### Expected result

The tests pass.

### Module

_No response_
"""

FIRST_MODULE_WINS = """\
### Summary

A docs change.

### Acceptance criteria

The page names the intake labels.

### Expected result

A reader can follow the labels.

### Module

docs

### Module

skills
"""


def load_labels_module():
    path = ROOT / "scripts" / "repo_ops_labels.py"
    spec = importlib.util.spec_from_file_location("repo_ops_labels", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def glob_to_re(pattern: str) -> re.Pattern[str]:
    parts: list[str] = []
    index = 0
    while index < len(pattern):
        if pattern.startswith("**/", index):
            parts.append("(?:.*/)?")
            index += 3
        elif pattern.startswith("**", index):
            parts.append(".*")
            index += 2
        elif pattern[index] == "*":
            parts.append("[^/]*")
            index += 1
        else:
            parts.append(re.escape(pattern[index]))
            index += 1
    return re.compile("^" + "".join(parts) + "$")


def glob_match(pattern: str, path: str) -> bool:
    return glob_to_re(pattern).match(path) is not None


def first_module(path: str, modules: dict) -> str | None:
    for name, patterns in modules.items():
        if any(glob_match(pattern, path) for pattern in patterns):
            return name
    return None


def listed_files() -> list[str]:
    output = subprocess.check_output(
        ["git", "ls-files", "-co", "--exclude-standard"],
        cwd=ROOT,
        text=True,
    )
    return [line for line in output.splitlines() if line]


def workflow_text() -> str:
    return (ROOT / ".github" / "workflows" / "issue-intake.yml").read_text(encoding="utf-8")


def workflow_script() -> str:
    text = workflow_text()
    marker = "          script: |\n"
    start = text.index(marker) + len(marker)
    lines = []
    for line in text[start:].splitlines():
        if line.startswith("            ") or line == "":
            lines.append(line[12:] if line.startswith("            ") else "")
            continue
        break
    return "\n".join(lines) + "\n"


def intake_api():
    script = workflow_script()
    match = re.search(r"// <intake-pure>\n([\s\S]*?)\n// </intake-pure>", script)
    if match is None:
        raise AssertionError("intake-pure region missing")
    source = match.group(1) + (
        "\nmodule.exports = { decideIntake, labelEdits, missingComment, readyComment,"
        " commentPlan, parseSections, INTAKE_MARKER };\n"
    )
    directory = tempfile.TemporaryDirectory()
    path = Path(directory.name) / "intake.cjs"
    path.write_text(source, encoding="utf-8")
    return directory, path


class RepoOpsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.labels = load_labels_module()
        cls.config = cls.labels.load_config()
        cls.directory, cls.intake_path = intake_api()
        cls.allowed = json.loads(
            re.search(r"const ALLOWED_MODULES = (\[[^\]]*\]);", workflow_script()).group(1)
        )

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def decide(self, body: str, current: list[str] | None = None) -> dict:
        fixture = {
            "body": body,
            "allowed": self.allowed,
            "labels": current or [],
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump(fixture, handle)
            fixture_path = handle.name
        runner = (
            "const intake = require(process.argv[1]);\n"
            "const fixture = JSON.parse(require('fs').readFileSync(process.argv[2], 'utf8'));\n"
            "const decision = intake.decideIntake(fixture.body, fixture.allowed);\n"
            "const labels = intake.labelEdits(decision, fixture.labels, fixture.allowed);\n"
            "const comment = decision.ok ? null : intake.missingComment(decision.missing);\n"
            "process.stdout.write(JSON.stringify({ decision, labels, comment }));\n"
        )
        result = subprocess.run(
            ["node", "-e", runner, str(self.intake_path), fixture_path],
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout)

    def test_config_matches_this_repo(self):
        config = self.config
        self.assertEqual(config["version"], 1)
        self.assertEqual(config["repo"], "HoeTee/shipwright")
        self.assertEqual(config["default_branch"], "main")
        self.assertEqual(config["commit_author"]["name"], "HoeTee")
        self.assertEqual(
            config["commit_author"]["email"],
            "123862692+HoeTee@users.noreply.github.com",
        )
        self.assertEqual(config["workflow"]["entry"], "shipwright-flow")
        self.assertEqual(config["workflow"]["pr_must_list"], ["skills_used", "verification_per_step"])
        for command in CI_COMMANDS:
            self.assertIn(command, config["test_command"])
        self.assertEqual(config["workers"], ["shipwright-worker-1", "shipwright-worker-2"])
        self.assertIs(config["auto_accept"]["external_issues"], True)
        self.assertEqual(config["auto_accept"]["trusted_authors"], ["HoeTee"])
        self.assertEqual(config["pr_intake"]["external_prs"], "review_only")
        self.assertEqual(config["cost"]["max_running"], 2)
        self.assertEqual(config["cost"]["max_review_rounds"], 3)
        self.assertEqual(config["cost"]["eval_label"], "eval")
        self.assertEqual(config["scan_minutes"], 30)
        self.assertEqual(
            config["protected_paths"],
            [".github/**", "**/*.env*", "LICENSE"],
        )
        self.assertEqual(list(config["modules"])[:2], ["plugin", "skills"])
        self.assertIn("repo", config["modules"])
        self.assertEqual(
            [name for name in config["modules"] if name != "repo"],
            self.allowed,
        )
        self.assertNotIn("repo", self.allowed)

    def test_parser_matches_pyyaml_when_installed(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML is not installed")
        paths = [
            ROOT / ".github" / "repo-ops.yml",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "bug.yml",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "skill.yml",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "docs.yml",
        ]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            self.assertEqual(self.labels.parse_yaml(text), yaml.safe_load(text), path.name)

    def test_every_listed_file_matches_a_module(self):
        modules = self.config["modules"]
        compiled = {
            name: [glob_to_re(pattern) for pattern in patterns]
            for name, patterns in modules.items()
        }
        unmatched = []
        for path in listed_files():
            if not any(pattern.match(path) for group in compiled.values() for pattern in group):
                unmatched.append(path)
        self.assertEqual(unmatched, [])
        for name, patterns in modules.items():
            hits = [path for path in listed_files() if any(glob_match(pattern, path) for pattern in patterns)]
            self.assertTrue(hits, name)

    def test_first_listed_module_owns_the_file(self):
        modules = self.config["modules"]
        self.assertEqual(first_module("skills/index.json", modules), "plugin")
        self.assertEqual(first_module("skills/plugin.json", modules), "plugin")
        self.assertEqual(first_module("skills/shipwright-flow/SKILL.md", modules), "skills")

    def test_pull_request_template_sections(self):
        text = (ROOT / ".github" / "pull_request_template.md").read_text(encoding="utf-8")
        headings = [line[3:] for line in text.splitlines() if line.startswith("## ")]
        self.assertEqual(
            headings,
            [
                "Summary",
                "Related issue",
                "Module",
                "What changed",
                "Shipwright skills used",
                "Verification per step",
                "Tests",
                "Out-of-scope edits",
                "Ignored issue text",
            ],
        )
        self.assertEqual(headings[0], "Summary")
        for required in ("Shipwright skills used", "Verification per step"):
            self.assertIn(required, headings)
        parts = re.split(r"(?m)^## ", text)[1:]
        self.assertEqual(len(parts), len(headings))
        for part in parts:
            self.assertRegex(part, r"<!-- .+ -->")
        visible = [
            line.strip()
            for line in text.splitlines()
            if line.strip() and not line.startswith("## ") and not line.strip().startswith("<!--")
        ]
        self.assertEqual(visible, [])

    def test_repo_module_is_not_an_intake_choice(self):
        body = """\
### Summary

The intake workflow should not start work on protected paths.

### Steps to reproduce

1. Open .github/workflows/issue-intake.yml.

### Expected result

The issue stays out of the ready queue.

### Module

repo
"""
        result = self.decide(body, ["triage"])
        self.assertFalse(result["decision"]["ok"])
        self.assertIsNone(result["decision"]["module"])
        self.assertIn("Module", result["decision"]["missing"])
        self.assertNotIn("module:repo", result["labels"]["add"])

    def test_glob_dialect(self):
        self.assertTrue(glob_match("skills/**", "skills/shipwright-flow/SKILL.md"))
        self.assertTrue(glob_match("SKILL.md", "SKILL.md"))
        self.assertFalse(glob_match("SKILL.md", "skills/shipwright-flow/SKILL.md"))
        self.assertTrue(glob_match("**/package.json", "skills/shipwright-ship/scripts/package.json"))
        self.assertTrue(glob_match("**/package.json", "package.json"))
        self.assertTrue(glob_match("**/*.env*", ".env"))
        self.assertTrue(glob_match("**/*.env*", "config/.env.local"))
        self.assertFalse(glob_match("**/*.env*", "config/env.txt"))
        self.assertTrue(glob_match(".github/**", ".github/workflows/ci.yml"))
        self.assertTrue(glob_match(".codex-plugin/**", ".codex-plugin/plugin.json"))

    def test_issue_forms_require_the_module_list(self):
        config = self.labels.parse_yaml(
            (ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml").read_text(encoding="utf-8")
        )
        self.assertIs(config["blank_issues_enabled"], False)
        expected = {
            "bug.yml": "Steps to reproduce",
            "skill.yml": "Acceptance criteria",
            "docs.yml": "Acceptance criteria",
        }
        module_names = [name for name in self.config["modules"] if name != "repo"]
        self.assertNotIn("repo", module_names)
        for filename, choice in expected.items():
            form = self.labels.parse_yaml(
                (ROOT / ".github" / "ISSUE_TEMPLATE" / filename).read_text(encoding="utf-8")
            )
            self.assertEqual(form["labels"], ["triage"], filename)
            labels = []
            dropdown = None
            for item in form["body"]:
                if item["type"] == "dropdown":
                    dropdown = item
                elif item["type"] == "textarea":
                    labels.append((item["attributes"]["label"], item["validations"]["required"]))
            self.assertEqual(
                labels,
                [
                    ("Summary", True),
                    (choice, True),
                    ("Expected result", True),
                    ("Non-goals", False),
                ],
                filename,
            )
            self.assertIsNotNone(dropdown, filename)
            self.assertEqual(dropdown["attributes"]["label"], "Module")
            self.assertIs(dropdown["validations"]["required"], True)
            self.assertEqual(dropdown["attributes"]["options"], module_names)

    def test_workflow_cannot_run_issue_text(self):
        text = workflow_text()
        script = workflow_script()
        self.assertEqual(text.count("\npermissions:\n"), 1)
        self.assertIn("\npermissions:\n  issues: write\n", text)
        self.assertNotIn("contents:", text)
        self.assertNotIn("actions/checkout", text)
        self.assertNotRegex(text, r"(?m)^\s*run:")
        for banned in ("${{", "eval(", "new Function", "child_process", "exec("):
            self.assertNotIn(banned, script)
        self.assertNotIn("HoeTee", script)
        node_check = "async function check() {\n" + script + "\n}\n"
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as handle:
            handle.write(node_check)
            check_path = handle.name
        subprocess.run(["node", "--check", check_path], check=True)

    def test_complete_bug_body_is_ready(self):
        result = self.decide(COMPLETE_BUG, ["triage"])
        self.assertEqual(result["decision"], {"ok": True, "missing": [], "module": "skills"})
        self.assertEqual(result["labels"]["add"], ["module:skills", "agent:ready"])
        self.assertEqual(result["labels"]["remove"], ["triage"])
        self.assertIsNone(result["comment"])

    def test_incomplete_body_names_only_the_missing_fields(self):
        result = self.decide(INCOMPLETE, ["triage", "agent:ready", "module:docs"])
        self.assertFalse(result["decision"]["ok"])
        self.assertEqual(result["decision"]["module"], None)
        self.assertEqual(result["decision"]["missing"], ["Summary", "Module"])
        self.assertEqual(result["labels"]["add"], ["needs-info"])
        self.assertEqual(
            result["labels"]["remove"],
            ["triage", "agent:ready", "module:docs"],
        )
        self.assertIn("Summary", result["comment"])
        self.assertIn("Module", result["comment"])
        self.assertNotIn("not-a-module", result["comment"])
        self.assertNotIn("four READMEs", result["comment"])
        self.assertNotIn("_No response_", result["comment"])

    def test_module_is_read_only_from_the_module_section(self):
        result = self.decide(MODULE_ONLY_IN_SUMMARY, [])
        self.assertFalse(result["decision"]["ok"])
        self.assertEqual(result["decision"]["module"], None)
        self.assertIn("Module", result["decision"]["missing"])
        self.assertNotIn("skills", result["labels"]["add"])
        self.assertNotIn("Run the checks", result["comment"])

    def test_first_module_heading_wins(self):
        result = self.decide(FIRST_MODULE_WINS, ["needs-info"])
        self.assertEqual(result["decision"]["module"], "docs")
        self.assertIn("module:docs", result["labels"]["add"])
        self.assertIn("agent:ready", result["labels"]["add"])
        self.assertEqual(result["labels"]["remove"], ["needs-info"])

    def test_label_commands_cover_the_required_set(self):
        specs = self.labels.label_specs(self.config)
        names = [name for name, _color, _description in specs]
        for label in REQUIRED_LABELS:
            self.assertIn(label, names)
        for module in self.config["modules"]:
            self.assertIn(f"module:{module}", names)
        for worker in self.config["workers"]:
            self.assertIn(f"bot:{worker}", names)
        printed = []
        for name, color, description in specs:
            command = self.labels.gh_command(self.config["repo"], name, color, description)
            self.assertIn("--force", command)
            printed.append(self.labels.shell_join(command))
        self.assertTrue(all(line.startswith("gh label create ") for line in printed))
        self.assertIn("gh label create triage --repo HoeTee/shipwright --force", printed[0])

    def test_comment_plan_updates_one_bot_comment(self):
        runner = (
            "const intake = require(process.argv[1]);\n"
            "const missing = intake.missingComment(['Summary']);\n"
            "const again = intake.missingComment(['Summary', 'Module']);\n"
            "const ready = intake.readyComment('skills');\n"
            "const result = {\n"
            "  created: intake.commentPlan([], missing),\n"
            "  same: intake.commentPlan([missing], missing),\n"
            "  updated: intake.commentPlan([missing], again),\n"
            "  ready: intake.commentPlan([missing], ready),\n"
            "  silent: intake.commentPlan([], null),\n"
            "};\n"
            "process.stdout.write(JSON.stringify(result));\n"
        )
        completed = subprocess.run(
            ["node", "-e", runner, str(self.intake_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(completed.stdout)
        self.assertEqual(result["created"], [{"op": "create", "body": result["created"][0]["body"]}])
        self.assertIn("Summary", result["created"][0]["body"])
        self.assertEqual(result["same"], [])
        self.assertEqual(result["updated"][0]["op"], "update")
        self.assertEqual(result["updated"][0]["index"], 0)
        self.assertIn("Module", result["updated"][0]["body"])
        self.assertEqual(result["ready"][0]["op"], "update")
        self.assertIn("module:skills", result["ready"][0]["body"])
        self.assertEqual(result["silent"], [])

    def test_doc_names_every_module(self):
        text = (ROOT / "docs" / "repo-ops.md").read_text(encoding="utf-8")
        for name in self.config["modules"]:
            self.assertIn(f"| {name} |", text)

    def test_contributing_links_the_intake_doc(self):
        text = (ROOT / "CONTRIBUTING-skills.md").read_text(encoding="utf-8")
        self.assertIn("](docs/repo-ops.md)", text)
        self.assertTrue((ROOT / "docs" / "repo-ops.md").is_file())


if __name__ == "__main__":
    unittest.main()
