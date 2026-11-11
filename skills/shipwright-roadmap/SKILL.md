---
name: shipwright-roadmap
description: "有仓库证据的功能方向建议。用于：下一步做什么功能。不要用于：找 bug 找 audit。"
---

# shipwright-roadmap

何时用：问下一步做什么功能，或请求里有 `next`、`features`、`roadmap`。
何时不用：找 bug、安全问题和债用 [shipwright-audit](../shipwright-audit/SKILL.md)。做法已经要落成计划用 [shipwright-plan](../shipwright-plan/SKILL.md)。

本 skill 只读。它给有仓库证据的选项，不决定战略，不写代码。

## Steps

1. 先侦察。意图文档优先于从代码猜出来的方向。侦察清单在共享的 `references/recon.md`（另写）。决策文档已经否决的，不提出来，只记下矛盾。
2. 只查方向这一类，而且比普通审计更深。依据规则和五类信号在 [direction.md](references/direction.md)。每条建议必须引用仓库里的证据。换成任何同类项目都成立的句子（「加暗色模式」「加 AI」）不是发现。
3. `next` / `features` / `roadmap` 给 4 到 6 条。普通审计交过来的方向最多 2 到 4 条，放在缺陷表之后，不和 bug 混排。
4. 每条写证据、取舍和粗的工作量，并说明工作量是粗的。Impact 写谁需要、为什么是现在。Confidence 写证据有多扎实，不写「这肯定是对的产品决定」。
5. 对方选中的条目交给 shipwright-plan，通常写成设计或探测计划：调查、原型、定接口、列出未决问题。不是一份把功能全部做完的计划。有实验能回答的分歧先走 shipwright-prototype。新模块或新接口走 shipwright-architect。

取舍碰到「实现省事」和「用的人更顺」时，选后者。原则名是 `experience-first`，在共享 principles 目录，不在这里复述。

## Stop

停在选项和对方的选择上。不把方向写成 P0/P1/P2 缺陷。不开始实现。结果页交给 shipwright-recap。
