"""Behavior tests for check_plan.py, ported from pstack check-plan.test.ts."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECKER = Path(__file__).with_name("check_plan.py")
RULE = (
    "Tests alone are not sufficient verification. "
    "A PR is verified only when its unit, live, and perf boxes are all checked."
)
LANES = "\n".join(
    f"- [ ] Lane {index}. Save `lane-{index}.png`. Pass when evidence exists."
    for index in range(1, 11)
)
VALID = f"""# Demo

## How to read this
One box is one unit of work and names the evidence. Check a box only when its evidence exists. See shipwright-autopilot.
{RULE}

## Program checklist
### Arm the program
### Spawn owners
### PR mechanics
### Verdict and merge
### Boot recipe
`git show origin/main:` one-hour cadence status message

## PR 1
**Depends on.** None.
**Files.**
- [ ] Do the thing.
**Build.**
- [ ] Do the thing.
**You see.**
- [ ] Do the thing.
**Verify, unit.** {RULE}
- [ ] Check the thing.
**Verify, live.** {RULE} Ten lanes on `example-model` at the PR head
{LANES}
**Verify, perf.** {RULE}
- [ ] Metric. Recorded.
- [ ] Probe. Recorded.
- [ ] Baseline. Recorded.
- [ ] Rule. Recorded.
**Review gate.** None.
**Merge.**
- [ ] Merge when approved.

## Close the program
Close.

## Appendix Prototype evidence
Recorded.
"""


def run_plan(example: str) -> subprocess.CompletedProcess[str]:
    directory = tempfile.mkdtemp(prefix="check-plan-test-")
    path = Path(directory) / "plan.md"
    path.write_text(VALID + example, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(CHECKER), str(path)],
        capture_output=True,
        text=True,
        check=False,
    )


class CheckPlanTests(unittest.TestCase):
    def test_accepts_ordinary_indented_and_longer_closing_fences(self):
        for indent in ["", " ", "  ", "   "]:
            result = run_plan(f"{indent}```markdown\n## Example only\n{indent}```\n")
            self.assertEqual(result.returncode, 0, result.stderr)
        result = run_plan("```markdown\n## Example only\n````\n")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_accepts_nested_backticks_and_tilde_info_strings(self):
        result = run_plan("````markdown\n```markdown\n## Example only\n```\n````\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        result = run_plan("~~~markdown `info`\n## Example only\n ~~~\n")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_keeps_mismatched_shorter_and_suffixed_closers_inside_the_fence(self):
        result = run_plan("````markdown\n~~~\n## Example only\n````\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        result = run_plan("````markdown\n```\n## Example only\n````\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        result = run_plan("````markdown\n``` info\n## Example only\n````\n")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_headings_and_prose_outside_a_proper_close(self):
        for suffix in ["  ", "\t"]:
            result = run_plan(f"```markdown\n## Example only\n```{suffix}\n## Example only\n")
            self.assertEqual(result.returncode, 1)
            self.assertIn('"## Example only" after Close the program is not an appendix', result.stderr)
        result = run_plan(
            "```markdown\nThis prose has a mid-sentence colon: inside code\n```\n"
            "This prose has a mid-sentence colon: bad.\n"
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("mid-sentence colon", result.stderr)

    def test_rejects_backtick_info_strings_containing_a_backtick(self):
        result = run_plan("```markdown `invalid`\n## Example only\n```\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn('"## Example only" after Close the program is not an appendix', result.stderr)

    def test_ignores_prose_punctuation_inside_matching_multi_backtick_spans(self):
        for count in [2, 3, 4]:
            delimiter = "`" * count
            result = run_plan(f"Use {delimiter}echo `x`: “quoted” — example{delimiter}.\n")
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_checks_prose_following_a_multi_backtick_span_and_unmatched_delimiters(self):
        outside = run_plan("Use ``echo `x`: y``. Bad: prose.\n")
        self.assertEqual(outside.returncode, 1)
        self.assertIn("mid-sentence colon", outside.stderr)
        unmatched = run_plan("Use ``unclosed: bad` here.\n")
        self.assertEqual(unmatched.returncode, 1)
        self.assertIn("mid-sentence colon", unmatched.stderr)

    def test_usage(self):
        result = subprocess.run([sys.executable, str(CHECKER)], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
