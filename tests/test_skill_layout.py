"""Validate the shipwright skill skeleton: frontmatter, links, and catalog."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

EXPECTED = {
    "shipwright-flow",
    "shipwright-help",
    "shipwright-setup",
    "shipwright-rules",
    "shipwright-how",
    "shipwright-why",
    "shipwright-teach",
    "shipwright-recall",
    "shipwright-audit",
    "shipwright-roadmap",
    "shipwright-diagnose",
    "shipwright-impact",
    "shipwright-plan",
    "shipwright-architect",
    "shipwright-prototype",
    "shipwright-build",
    "shipwright-autopilot",
    "shipwright-review",
    "shipwright-fix",
    "shipwright-interrogate",
    "shipwright-comments",
    "shipwright-ship",
    "shipwright-signoff",
    "shipwright-land",
    "shipwright-deploy",
    "shipwright-recover",
    "shipwright-reconcile",
    "shipwright-debt",
    "shipwright-prevent",
    "shipwright-reflect",
    "shipwright-cleanup",
    "shipwright-verify-create",
    "shipwright-verify-maintain",
    "shipwright-prove-create",
    "shipwright-prove-maintain",
    "shipwright-bugs",
    "shipwright-security",
    "shipwright-test",
    "shipwright-structure",
    "shipwright-perf",
    "shipwright-lean",
    "shipwright-swarm",
    "shipwright-arena",
    "shipwright-trail",
    "shipwright-recap",
    "shipwright-write",
    "shipwright-readme",
    "shipwright-skillsmith",
    "shipwright-eval",
}

PRINCIPLES = [
    "attack-the-premise",
    "boundary-discipline",
    "build-the-lever",
    "encode-lessons-in-structure",
    "exhaust-the-design-space",
    "experience-first",
    "explain-the-number",
    "fix-root-causes",
    "foundational-thinking",
    "guard-the-context-window",
    "laziness-protocol",
    "make-operations-idempotent",
    "migrate-callers-then-delete-legacy-api",
    "minimize-reader-load",
    "model-the-domain",
    "never-block-on-the-human",
    "outcome-oriented-execution",
    "prove-it-works",
    "redesign-from-first-principles",
    "separate-before-serializing-shared-state",
    "sequence-verifiable-units",
    "subtract-before-you-add",
    "test-behavior-not-implementation",
    "type-system-discipline",
]

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
CODE_FENCE = re.compile(r"^```[^\n]*\n.*?^```\s*$", re.M | re.S)
INLINE_CODE = re.compile(r"`([^`\n]*)`")
PLACEHOLDER = re.compile(r"<([^>\n]*)>")
NON_ASCII = re.compile(r"[^\x00-\x7F]")


def placeholders_in_code(text: str) -> list[str]:
    """Return <placeholder> tokens inside fenced blocks and inline code spans."""
    tokens = []
    for match in CODE_FENCE.finditer(text):
        tokens.extend(PLACEHOLDER.findall(match.group(0)))
    without_fences = CODE_FENCE.sub("", text)
    for match in INLINE_CODE.finditer(without_fences):
        tokens.extend(PLACEHOLDER.findall(match.group(1)))
    return tokens


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("frontmatter is not closed")
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
            value = value[1:-1].replace('\\"', '"')
        data[key.strip()] = value
    return data, text[end + 5 :]


class SkillLayoutTests(unittest.TestCase):
    def test_exactly_the_49_skills(self):
        found = {path.parent.name for path in SKILLS.glob("shipwright-*/SKILL.md")}
        self.assertEqual(found, EXPECTED)
        extra = {path.name for path in SKILLS.iterdir() if path.is_dir()} - EXPECTED
        self.assertEqual(extra, set())

    def test_frontmatter_links_and_references(self):
        for name in sorted(EXPECTED):
            skill = SKILLS / name
            text = (skill / "SKILL.md").read_text(encoding="utf-8")
            meta, body = parse_frontmatter(text)
            self.assertEqual(meta.get("name"), name, name)
            self.assertTrue(meta.get("description"), name)
            self.assertTrue(body.strip(), name)
            for match in LINK.finditer(text):
                target = match.group(1).strip()
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                path_part, _, _anchor = target.partition("#")
                if not path_part:
                    continue
                resolved = (skill / "SKILL.md").parent.joinpath(path_part).resolve()
                self.assertTrue(resolved.exists(), f"{name} links to missing {target}")

    def test_plan_templates_and_principle_directory(self):
        template = (SKILLS / "shipwright-plan/references/template.md").read_text(encoding="utf-8")
        index = (SKILLS / "shipwright-plan/references/index.md").read_text(encoding="utf-8")
        for phrase in ("Self-contained context", "Domains", "Run record", "## Evidence appendix", "Copyright (c) 2026 shadcn"):
            self.assertIn(phrase, template)
        for phrase in ("Execution order", "Domains", "Findings considered and rejected"):
            self.assertIn(phrase, index)
        readme = (ROOT / "references/principles/README.md").read_text(encoding="utf-8")
        for slug in PRINCIPLES:
            self.assertIn(f"{slug}.md", readme)
        self.assertEqual(len(PRINCIPLES), 24)

    def test_repo_paths_and_code_placeholders_are_ascii(self):
        bad_paths = []
        for path in ROOT.rglob("*"):
            if ".git" in path.parts:
                continue
            relative = path.relative_to(ROOT).as_posix()
            if NON_ASCII.search(relative):
                bad_paths.append(relative)
        self.assertEqual(bad_paths, [])

        bad_tokens = []
        for path in ROOT.rglob("*.md"):
            if ".git" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            for token in placeholders_in_code(text):
                if NON_ASCII.search(token):
                    bad_tokens.append(f"{path.relative_to(ROOT).as_posix()}: <{token}>")
        self.assertEqual(bad_tokens, [])

    def test_opencode_catalog_matches_skill_files(self):
        script = ROOT / "scripts/build_opencode_index.py"
        spec = importlib.util.spec_from_file_location("build_opencode_index", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result = subprocess.run([sys.executable, str(script), "--check"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        catalog = json.loads((SKILLS / "index.json").read_text(encoding="utf-8"))
        self.assertEqual({item["name"] for item in catalog["skills"]}, EXPECTED)
        for item in catalog["skills"]:
            skill = SKILLS / item["name"]
            on_disk = module.skill_files(skill)
            self.assertEqual(item["files"], on_disk, item["name"])
            self.assertEqual(item["version"], module.content_version(skill, on_disk), item["name"])
            self.assertIn("SKILL.md", item["files"])
            for rel in item["files"]:
                self.assertFalse(rel.startswith(("/", "..")), rel)
                self.assertNotIn("/../", f"/{rel}/")
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "demo-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text("one", encoding="utf-8")
            files = ["SKILL.md"]
            before = module.content_version(skill, files)
            (skill / "SKILL.md").write_text("two", encoding="utf-8")
            after = module.content_version(skill, files)
            self.assertNotEqual(before, after)

    def test_host_manifests_discover_the_49_skills(self):
        claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        codex = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        # Claude Code loads skills/<name>/SKILL.md when plugin.json omits "skills".
        # A skills entry has to be a directory that itself contains SKILL.md, so
        # pointing it at the parent directory would hide the 49 skills.
        self.assertNotIn("skills", claude)
        self.assertEqual(codex["skills"], "./skills/")
        plugin = marketplace["plugins"][0]
        self.assertEqual(plugin["name"], claude["name"])
        self.assertEqual(plugin["source"], "./")
        found = {path.parent.name for path in (ROOT / "skills").glob("shipwright-*/SKILL.md")}
        self.assertEqual(found, EXPECTED)

    def test_one_copy_of_shared_rules(self):
        structure = (SKILLS / "shipwright-structure/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("../shipwright-architect/references/design-red-flags.md", structure)
        self.assertFalse((SKILLS / "shipwright-structure/references/design-red-flags.md").exists())
        template = (SKILLS / "shipwright-plan/references/template.md").read_text(encoding="utf-8")
        self.assertIn("| eval", template)
        pointer = (SKILLS / "shipwright-test/references/evidence.md").read_text(encoding="utf-8")
        self.assertIn("../../../references/evidence.md", pointer)
        self.assertLess(len(pointer.splitlines()), 12)
        self.assertFalse((SKILLS / "shipwright-ship/scripts/bootstrap.ts").exists())
        bootstrap = SKILLS / "shipwright-ship/scripts/bootstrap.py"
        source = bootstrap.read_text(encoding="utf-8")
        self.assertTrue(bootstrap.is_file())
        self.assertIn("npm", source)
        self.assertNotIn("frozen-lockfile", source)
        watcher = (SKILLS / "shipwright-ship/scripts/watch-pr/watch-pr").read_text(encoding="utf-8")
        self.assertIn("bootstrap.py", watcher)
        self.assertNotIn("bootstrap.ts", watcher)

    def test_parallel_batch_and_review_cap_have_one_home(self):
        self.assertTrue((SKILLS / "shipwright-land/references/batch-ci.md").is_file())
        for rel in (
            "shipwright-land/SKILL.md",
            "shipwright-land/references/shipping.md",
            "shipwright-swarm/SKILL.md",
            "shipwright-autopilot/references/stack.md",
            "shipwright-prevent/references/repeated-class.md",
        ):
            text = (SKILLS / rel).read_text(encoding="utf-8")
            self.assertIn("batch-ci.md", text, rel)
        fix = (SKILLS / "shipwright-fix/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("默认 3", fix)
        for name in EXPECTED - {"shipwright-fix"}:
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertNotIn("默认 3", text, name)

    def test_template_headings_are_not_cjk(self):
        cjk = re.compile(r"[\u3400-\u9fff\u3040-\u30ff\uac00-\ud7af]")
        bad = []
        for path in list(ROOT.rglob("*template*.md")) + [SKILLS / "shipwright-plan/references/index.md"]:
            if not path.is_file() or ".git" in path.parts:
                continue
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if line.startswith("#") and cjk.search(line):
                    bad.append(f"{path.relative_to(ROOT).as_posix()}:{number}:{line}")
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
