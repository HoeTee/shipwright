---
name: shipwright-fix
description: "审查-修复循环，派审查子 agent。开 PR 前叫执行/修改，不计数；开 PR 后每次 AI 审查计数，不清零；上限默认 3，只写在本 skill，你可以临时口头改；超了做有界复盘。用于：review 报出阻断项之后。不要用于：你只要报告时不用。"
---

# shipwright-fix

何时用：shipwright-review 报出阻断项，而且授权允许改代码。
何时不用：用户只要报告。本 skill 不合并。

审查上限只写在这里。默认 3。从 PR 打开时起算，不清零。换方法、恢复会话、重开同一任务的 PR，都不重置。开 PR 前的执行和修改叫 Pre-PR iterations，不算 AI 审查。你可以用一句话临时改这次的上限，脚本把新上限写进分母。不要把上限写进 `AGENTS.md`。

## Procedure

1. 用 [review_count.py](scripts/review_count.py) 读写计划 Run record。开 PR 前：`--bump-iteration`。每一次开 PR 之后的 AI 审查：`--bump-review`。口头改上限时加 `--cap N`。计数已到上限时脚本退出，不要开始下一次自动返修。
2. CI 重跑、网络重试、同一版本上的重复事件、人工评论，都不加计数。
3. 修复前核对工作树就是受审版本。审 PR 时，从该 PR 的 head 做隔离 worktree，不改用户原来的工作区。步骤全文在 [loop.md](references/loop.md)。计数和上限只写在本 skill，loop.md 不另写数字。
4. 先查共享根因和调用方，再做最小的完整修改。原则 [fix-root-causes](../../references/principles/fix-root-causes.md) 见 [principles](../../references/principles/README.md)。两次修复基于同一前提却没通过同一检查时，先写下前提并做一次能分辨真假的观察，原则 [attack-the-premise](../../references/principles/attack-the-premise.md)。这不增加审查额度。
5. 哪些证据失效、必须重跑什么，见 [stale-evidence.md](references/stale-evidence.md)。没跑的命令不能写进 Verification evidence。
6. 派独立审查者复审新的 SHA。审查者只读，不能是写这次修复的人。打开 diff、测试断言和证据文件，不只读执行者摘要。一个结论只管一个 SHA。
7. 对一次计划执行的验收用 [verdict.md](references/verdict.md)：重跑 done criteria、核对范围、读完整 diff、读新测试。结论是 APPROVE、REVISE 或 BLOCK。REVISE 最多两轮，然后 BLOCK。这两轮是开 PR 前的执行修改，记入 Pre-PR iterations，不是上面的 AI 审查上限。
8. 领域标签的提交前一节仍读 shipwright-bugs、shipwright-security、shipwright-test、shipwright-structure、shipwright-perf、shipwright-lean。

## Stop

没有阻断项且必需检查通过：交给 shipwright-signoff。不要在这里请人批准合并。

到达上限仍有阻断项：停止自动返修。写一次有界复盘：为什么没收敛，已试过什么，替代做法、影响和验证计划。复盘本身不算新的审查，也不授权第四次审查。需求冲突或超出授权，立刻交给用户，不必等满上限。

## Handoff

把新的候选 SHA、证据目录、未解决的 P0/P1/P2 数量交给下一步。趋势指标只记进行记录，不解释成 skill 省了多少。
