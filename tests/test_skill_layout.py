"""Validate the shipwright skill skeleton: frontmatter, links, and catalog."""

from __future__ import annotations

import json
import re
import subprocess
import sys
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
    def test_exactly_the_48_skills(self):
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
        result = subprocess.run([sys.executable, str(script), "--check"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        catalog = json.loads((SKILLS / "index.json").read_text(encoding="utf-8"))
        self.assertEqual({item["name"] for item in catalog["skills"]}, EXPECTED)
        flow = next(item for item in catalog["skills"] if item["name"] == "shipwright-flow")
        self.assertIn("SKILL.md", flow["files"])


if __name__ == "__main__":
    unittest.main()
