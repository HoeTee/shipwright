"""Contract checks for the five skill-rule changes.

These tests read the skill files. They do not call a model. shipwright-eval's
paid comparison was not run. A passing test is a static rule check, not a
measured-model-behavior guarantee.
"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

CLARIFY = SKILLS / "shipwright-flow/references/clarify.md"
CONTRACT = SKILLS / "shipwright-lean/references/worker-contract.md"
FLOW = SKILLS / "shipwright-flow/SKILL.md"
PLAN = SKILLS / "shipwright-plan/SKILL.md"
PLAN_RULES = SKILLS / "shipwright-plan/references/writing-rules.md"
ARCHITECT = SKILLS / "shipwright-architect/SKILL.md"
PROCEDURE = SKILLS / "shipwright-architect/references/procedure.md"
RATIONALE = SKILLS / "shipwright-architect/references/rationale-template.md"
LEAN = SKILLS / "shipwright-lean/SKILL.md"
DISPATCH = SKILLS / "shipwright-build/references/dispatch.md"
FEATURE = SKILLS / "shipwright-build/references/feature.md"
AUTOPILOT = SKILLS / "shipwright-autopilot/SKILL.md"
NEVER_BLOCK = ROOT / "references/principles/never-block-on-the-human.md"
FIX = SKILLS / "shipwright-fix/SKILL.md"

CAP_PHRASES = (
    "最多三轮",
    "at most 3",
    "of at most 3",
    "Stop asking new rounds",
    "Do not ask more than three rounds",
    "Round 1 of at most",
    "即使第一个看起来已经够用",
    "even when the first looks sufficient",
)

CLARIFY_PATHS = (
    CLARIFY,
    FLOW,
    PLAN,
    PLAN_RULES,
    AUTOPILOT,
    NEVER_BLOCK,
)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class DecisionContractTests(unittest.TestCase):
    def test_static_check_is_not_a_model_measurement(self):
        note = Path(__file__).read_text(encoding="utf-8")
        self.assertIn("not a measured-model-behavior guarantee", note)
        self.assertIn("do not call a model", note.lower())

    def test_no_old_clarify_runtime(self):
        self.assertFalse((SKILLS / "shipwright-clarify").exists())
        self.assertFalse((ROOT / "references/process.md").exists())
        self.assertTrue(CLARIFY.is_file())

    def test_rounds_past_three_are_not_cut_or_silently_approved(self):
        clarify = text(CLARIFY)
        self.assertIn("没有固定轮次上限", clarify)
        self.assertIn("不在第三轮截断", clarify)
        self.assertIn("不批准未答", clarify)
        self.assertIn("沉默", clarify)
        self.assertIn("「继续」", clarify)
        self.assertIn("轮次用尽", clarify)
        for path in CLARIFY_PATHS:
            body = text(path)
            for phrase in CAP_PHRASES:
                self.assertNotIn(phrase, body, f"{path.name} contains {phrase}")
        self.assertIn("另一道关口", clarify)
        self.assertIn("默认 3", text(FIX))

    def test_deep_mode_waits_for_shared_understanding(self):
        clarify = text(CLARIFY)
        for phrase in ("已定", "未决", "非目标", "共享理解"):
            self.assertIn(phrase, clarify)
        self.assertIn("不能声称整项已获确认", clarify)
        self.assertIn("真正不依赖未决项的工作可以做", clarify)
        self.assertIn("hook、脚本", clarify)
        self.assertIn("确认共享理解", text(FLOW))
        self.assertIn("confirm the shared understanding", text(PLAN_RULES))

    def test_ordinary_tasks_are_not_forced_into_deep_mode(self):
        clarify = text(CLARIFY)
        self.assertIn("明确任务直接执行", clarify)
        self.assertIn("普通任务只问关键开放决策", clarify)
        self.assertIn("不因此进入深入讨论", clarify)
        self.assertIn("不是默认一问一答", clarify)
        self.assertNotIn("有歧义就问一个问题", text(FLOW))
        self.assertNotIn("一次只问一个问题", text(PLAN))
        self.assertNotIn("Ask one question at a time, each with a recommended answer", text(PLAN_RULES))

    def test_own_and_watch_do_not_override_explicit_deep_discussion(self):
        clarify = text(CLARIFY)
        self.assertIn("own", clarify)
        self.assertIn("watch", clarify)
        self.assertIn("标成假设", clarify)
        self.assertIn("不覆盖用户显式的深入讨论", clarify)
        self.assertIn("clarify.md", text(NEVER_BLOCK))
        self.assertIn("不按本条采用未答决策", text(AUTOPILOT))
        self.assertIn("labeled assumption", text(PLAN_RULES))

    def test_worker_contract_is_complete_and_not_the_two_line_summary(self):
        contract = text(CONTRACT)
        for phrase in (
            "first option that fully works",
            "callers, tests, fixtures, config, and exports",
            "validation at trust boundaries",
            "error handling that prevents data loss",
            "security",
            "accessibility",
            "anything the user asked for",
            "shortcut: <the limit>, <when to upgrade>",
            "does not exempt security, data integrity",
            "not a substitute",
            "only when dispatching",
        ):
            self.assertIn(phrase, contract)
        self.assertIn("laziness-protocol", contract)
        self.assertIn("worker-contract.md", text(LEAN))
        self.assertIn("worker-contract.md", text(FLOW))
        self.assertIn("worker-contract.md", text(DISPATCH))
        self.assertIn("does not exempt security or data integrity", text(SKILLS / "shipwright-lean/references/smallest-change.md"))
        for rel in (
            "shipwright-build/references/feature.md",
            "shipwright-build/references/bugfix.md",
            "shipwright-build/references/perf.md",
            "shipwright-build/references/refactor.md",
            "shipwright-perf/references/hillclimb.md",
        ):
            self.assertIn("worker-contract.md", text(SKILLS / rel), rel)

    def test_small_tasks_skip_architect_exploration(self):
        architect = text(ARCHITECT)
        procedure = text(PROCEDURE)
        self.assertIn("真实结构取舍", architect)
        self.assertIn("第一件完全够用", architect)
        self.assertIn("不因为任务存在就调用", architect)
        self.assertIn("不是每个任务的必经步骤", architect)
        self.assertNotIn("即使第一个看起来已经够用", architect)
        self.assertIn("real structural tradeoff", procedure)
        self.assertIn("Skip shipwright-arena", procedure)
        self.assertNotIn("even when the first looks sufficient", procedure)
        self.assertIn("Do not call it for every feature", text(FEATURE))
        self.assertNotIn("no skip-with-reason escape", text(FEATURE))
        structure = text(SKILLS / "shipwright-structure/SKILL.md")
        self.assertNotIn("至少两种方案", structure)
        self.assertIn("有真实结构取舍时才比较方案", structure)

    def test_adr_is_gated_and_not_the_architect_rationale(self):
        clarify = text(CLARIFY)
        for phrase in ("难撤销", "缺背景会令人困惑", "实质取舍", "可以是零"):
            self.assertIn(phrase, clarify)
        self.assertIn("rationale 不是 ADR", clarify)
        self.assertIn("仅咨询", clarify)
        self.assertIn("不写文件", clarify)
        self.assertIn("docs/adr/", clarify)
        self.assertIn("docs/adrs/", clarify)
        self.assertIn("docs/decisions/", clarify)
        self.assertIn("Supersedes", clarify)
        self.assertIn("rationale 不是 ADR", text(ARCHITECT))
        self.assertIn("is not an ADR", text(RATIONALE))
        self.assertIn("is not an ADR", text(PROCEDURE))


if __name__ == "__main__":
    unittest.main()
