---
name: shipwright-plan
description: "写 plans/NNN 计划并维护索引；临时 PR 审查也开一个编号。用于：发现之后、动手之前。不要用于：一两处改动且做法明显，直接 build。"
---

# shipwright-plan

何时用：发现已经选定，动手之前，要把做法写成一份别人能独立执行的计划。临时 PR 审查也要编号。
何时不用：一两处改动而且做法明显，直接交给 shipwright-build，并说一声为什么不写计划。

本 skill 只写 `plans/`。`plans/` 已被别的用途占用时改用 `advisor-plans/`，并说明。不改源码，不提交，不合并。

## Steps

1. 记下 `git rev-parse --short HEAD`。摘录必须来自你自己打开的代码，不来自工人的报告。编号只增不减。已有索引就接着编，不重复，不把已否决的发现再写成计划。
2. 选定要写的条目。审计没选定时不要写 30 份。无人可选时，写收益最高的 3 到 5 条，并在索引里记下这个默认。`plan <description>` 跳过审计，先从仓库消除歧义，剩下的一次只问一个问题，并给出推荐答案。
3. 每一份计划按 [template.md](references/template.md) 写，文件名 `plans/<NNN>-<slug>.md`。索引按 [index.md](references/index.md) 写成 `plans/README.md`。写给一个没见过这次对话的执行者。自包含、每步有命令和期望结果、写明停止条件。细则在 [writing-rules.md](references/writing-rules.md)。一份真实样例在 [example.md](references/example.md)，那是历史样本，不要执行它。
4. `Domains` 写 `bugs`、`security`、`test`、`structure`、`perf`、`lean` 里的一个或多个。临时 PR 审查的 Category 写 `review`，同样登记进索引。Run record 和证据附录从模板抄，不另建记录文件。证据附录记分支、SHA 和链接，截图不进 git。
5. 审一份已有计划用 `review-plan`。对照模板收紧。如果这份计划是本会话写的，再派一个没有这份对话的执行者冷读，报告含糊处。
6. 用户明确加上 `--issues` 时才发工单。公开仓库要先警告并得到确认。步骤在 [issues.md](references/issues.md)。
7. 没有更窄的 skill 能套上的大任务，先做 [figure-it-out.md](references/figure-it-out.md) 的框定和阶段设计，把阶段清单交出去，不在这里执行。

多 PR 节目默认不启用。只有用户明确要一个多 PR 节目时才读 [multi-pr.md](references/multi-pr.md)，并用 [check_plan.py](scripts/check_plan.py) 检查那份清单。普通计划不跑这个脚本。

## Hand off

计划写完就停。执行交给 shipwright-build。无人值守交给 shipwright-autopilot。跨函数边界的形状先交给 [shipwright-architect](../shipwright-architect/SKILL.md)。有实验能回答的分歧先交给 [shipwright-prototype](../shipwright-prototype/SKILL.md)。方向类条目来自 [shipwright-roadmap](../shipwright-roadmap/SKILL.md)，通常写成探测计划，不是把功能做完的计划。

原则名记在这里，原文在共享 principles 目录，不抄进计划：`sequence-verifiable-units`、`build-the-lever`、`outcome-oriented-execution`。

## Stop

不派执行者改代码，不合并，不推送。对方要求直接实现时，拒绝，并指向已经写好的计划。结果页交给 shipwright-recap。
