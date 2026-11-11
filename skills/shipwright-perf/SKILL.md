---
name: shipwright-perf
description: "性能：先测量、七条口诀、基准核对、爬坡。用于：慢、负载高。不要用于：流程问题找阶段 skill。"
---

# shipwright-perf

何时用：慢、负载高、要报一个性能数字，或要对着一个指标持续改进。
何时不用：流程怎么推进找对应的阶段 skill。一个人没问题、预期负载下会算错，找 shipwright-bugs 的 Scale。评测 skill 效果找 shipwright-eval。

本 skill 只提供知识。它不路由，不改代码，不合并。

## Rules

1. 先测量再改。读代码不能代替一次运行。
2. 报数字之前写下这个数字要改变的决定，并指出限制因素（原则 [explain-the-number](../../references/principles/explain-the-number.md)）。说不出为什么不是两倍，就还不知道量到了什么。
3. 七条口诀从便宜到贵，前面一条已经达标就停。
4. 选择方案的数字至少交替跑，报告中位数和范围。差距小于各次之间的波动，就是没有可测差异。
5. 没数错误、没确认工作真的发生、一边没按生产配置跑、或说不出限制因素：结论是无法判断，并写明缺什么。
6. 回复写基线数字、修后数字、差值、产物路径。无法判断或量错了表面，不算通过。

原则正文在共享目录，见 [principles](../../references/principles/README.md)。这里不复述。

## Stage checks

### Stage 0 — Understand

沿热路径看数据从哪进、在哪重复算。假设来自调用链，结论来自测量。

### Stage 1 — Discover

按 [Performance checks](references/performance-checks.md) 查 N+1、复杂度、缓存、载荷、同步工作和 CI 缓存。没有模式证据的「可能有 N+1」不是发现。

### Stage 2 — Plan

写下指标、预算、以及什么数字算达标。基线先过 [Benchmark checklist](references/benchmark-checklist.md)。

### Stage 3 — Build

按 [Mantras](references/mantras.md) 从第 1 条试到达标为止。一次修复对应一组前后数字。执行步骤在 shipwright-build 的性能材料里；口诀和停止条件在这里。

### Stage 4 — Review

每个要拿来做决定的数字过七问。快速估数可以只跑一次，仍要核对错误次数和工作是否真的发生，并写明只有一次。在方案之间做选择时，一次不够。

### Stage 5 — Pull request

PR 正文留一个主数字：基线、修后、差值。运行次数、范围和限制因素放在链接的产物里。

### Stage 6 — After merge

对着一个指标持续改进时走 [Hillclimb](references/hillclimb.md)：一次改一处，测完保留或整段回退。目标环境的实测在发布验收里做，数字规则相同。

## Scripts

- [summarize_runs.py](scripts/summarize_runs.py)：中位数、范围、波动，以及是否无法判断。
- [decision_log.py](scripts/decision_log.py)：向仓库外的 `decision.tsv` 追加一行爬坡记录。

## Read next

- [Mantras](references/mantras.md)：七条口诀和回复契约。
- [Benchmark checklist](references/benchmark-checklist.md)：七问全文。
- [Hillclimb](references/hillclimb.md)：爬坡循环全文。
- [Performance checks](references/performance-checks.md)：improve 第 3 类全文。
