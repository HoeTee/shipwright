---
name: shipwright-eval
description: "按需评测 skill 效果：带与不带 skill，或新版与上一版；同一题库、同一盲评评委、同一评分表，只换对照组；出 HTML 报告和判定。用于：想知道 skill 到底有没有用；改了 skill 准备发布；趋势指标变差。不要用于：不在每次改代码或每个 issue 上跑；日常只在 Run record 记趋势指标。"
---

# shipwright-eval

## When to use

想知道 skill 到底有没有用，改了 skill 准备发布，或趋势指标变差。人触发才跑。

## When not to use

不在每次改代码或每个 issue 上跑。日常 AI 审查只在计划的 Run record 记趋势指标：改动行数、tokens、用时、AI 审查轮次、P0/P1/P2 数、合并后是否返工。这行只提示该不该评测，不说 skill 省了多少。

该跑的信号：同一类问题合并后反复返工；AI 审查经常用满上限；改了 skill 之后 tokens 或用时明显上升；P0/P1 到人审或上线后才被发现。

## Modes

两种主模式共用一个题库、一个盲评评委、一张评分表，只换对照组。各组在同一次评测里按题交替，每题每组默认 5 次。

| 模式 | 实验组 | 对照组 | 何时 |
| --- | --- | --- | --- |
| 有无对比 | 装 shipwright | 同一 agent、同一模型和设置，不装任何 skill | 第一次上线、定期复核 |
| 版本对比 | 新版 skill | 上一个发布版 | 改了 skill、准备发布 |
| 一句话对照（可选） | 装 shipwright | 只加一句提示，例如「保持改动最小」 | 怀疑 skill 太重 |
| 多个版本（可选） | 2–4 个改法 | 上一个发布版 | 几种改法同时比 |

发布前用全量题库同时跑新版、上一版、不装 skill 三组。做法见 [iterate.md](references/iterate.md)。

## Steps

1. 先写希望能说的那句话，例如「装 shipwright 后，修 bug 题的隐藏检查通过率不低于不装，tokens 少 20%」。再写什么结果会发布、回退或继续改。
2. 选模式和对照组。写下每题每组次数 N（默认 5）和停止条件。停止条件带最少尝试次数，中途不放宽。
3. 准备题库。第一次用 `scripts/mine_questions.py` 从仓库 git 历史挖题，把 `candidates.md` 给人看一次，删减后冻成 `plans/eval/bank/bank.json`。之后直接复用。规则见 [question-bank.md](references/question-bank.md)。
4. 先校准量具。跑 `scripts/selftest.py`。每题参考答案必须通过隐藏检查，已知坏答案必须被抓住。评委用一好一坏样例自测通过才开始。
5. 搭隔离环境。每次运行一个全新临时目录，用 `scripts/export_workspace.py` 导出修复前的代码。目录里没有 `.git`、`plans/` 和隐藏测试，名字像普通项目。对照组确认没有加载任何 skill。隔离规则见 [blinding.md](references/blinding.md)。
6. 交替跑 N 次。超时、崩溃、没交付照实计入，不丢掉。
7. 盲评并跑隐藏检查。评委来自另一模型家族，只看匿名标签，一次给各组在同一尺度上打分。评分表 3 到 6 条，只给评委。
8. 查运行记录。从实际打开的文件判断有没有按 skill 做，不信自述。只读这次运行的记录，不跨项目翻。
9. 主控读完全部输出，和评委对照。不一致就先查评委或评分表，再下结论。
10. 用 `scripts/stats.py` 按题取中位数，算比值、区间、赢了几题，并过 [numbers.md](references/numbers.md) 的七问。判定为 `improved`、`regressed`、`no-measurable-difference` 或 `inconclusive`。
11. 用 `scripts/render_report.py` 生成 HTML 报告，写到 `plans/reports/<plan-id>-eval-<topic>.html`。判定写进 `plans/<plan-id>-eval-<topic>.md`，`Category` 写 `eval`，并记下结论句、模式、对照组、N 和判定。临时目录交给 shipwright-cleanup。

## Store

```text
plans/<plan-id>-eval-<topic>.md
plans/eval/bank/
plans/reports/<plan-id>-eval-<topic>.html
/tmp/shipwright-eval-<plan-id>/
/tmp/shipwright-eval-<plan-id>/decision.tsv
```

质量没变差且硬指标下降才算赢。tokens 更少但质量更低，不算赢。两组都满分的题单列，不证明差异。

## Hosts

Claude Code、Codex、OpenCode 共用这份说明。派执行组和评委时不写工具名。候选的提示里不出现 eval、test、judge、experiment、rubric、score、compare、benchmark、candidate、arena。
