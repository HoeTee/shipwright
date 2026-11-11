---
name: shipwright-why
description: "查设计原因和历史，分确证、推断、猜测。用于：想知道为什么这样写。不要用于：怎么运作找 how。"
---

# shipwright-why

何时用：想知道为什么这样写，包括设计取舍、回归考古、阈值和历史决定。
何时不用：问怎么运作用 [shipwright-how](../shipwright-how/SKILL.md)。要合成讲解用 [shipwright-teach](../shipwright-teach/SKILL.md)。

本 skill 只读。调查者不写产品代码。综合者引用并抽查，不提交、不改外部状态。

## Steps

1. 框定问题：谁的决定、哪一个界面、这里的「为什么」是历史、约束、事故还是取舍。先用当前代码钉住行为和符号，避免查错版本。
2. 从 [source-playbook.md](references/source-playbook.md) 选来源。每个来源一份剧本，在 [sources/](references/sources/)。只查已经接上的系统。源码历史必查。代码看起来在防御（空值、重试、超时、限流、开关、出口守卫、内存耗尽）时，加上 [incident-postmortem.md](references/sources/incident-postmortem.md)。仓库内的 git 查询用 [code_archaeology.py](scripts/code_archaeology.py)。
3. 每个来源派一个独立调查者，提示词用 [investigator-prompt.md](references/investigator-prompt.md)，附上那一份剧本。同一轮派完。调查者只收集，不下结论。连接不上或未授权的来源记为缺口，不编造。
4. 综合者先读完 [epistemics.md](references/epistemics.md)，再用 [synthesizer-prompt.md](references/synthesizer-prompt.md)。先写证据最强的动机，再列竞争假说。两处记载冲突时两处都留下。
5. 输出先给短答案，再给带来源的证据，最后给未知项。保留表示不确定的措辞。不发明组织历史。

派工见 [hosts.md](../shipwright-how/references/hosts.md)。完整姿势、五级置信度和审查用法见 [procedure.md](references/procedure.md)。审查场景的中文步骤在 [method.md](references/method.md)。

## Confidence

每句判断带上等级。五级都要留，不能收成一句「大概是」。

| 等级 | 回复里的说法 | 要求 |
| --- | --- | --- |
| Direct | 确证 | 作者写过原因，紧挨着引用 |
| Supported | 有支持 | 多条间接证据收敛，逐条引用 |
| Inferred | 推断 | 记录里没写，用「看起来」「可能」并写出推理链 |
| Speculative | 猜测 | 证据很薄，和其他解释一样说得通 |
| Unknown | 未知 | 写清搜了什么、在哪、没找到什么 |

代码只能说明它做什么，不能当作「作者当时想要什么」的证据。用户夹在问题里的猜测只是候选，要单独核对。

## Stop

把带引用的答案交回。不写代码，不开计划，不开始设计。过去的理由不等于现在仍该如此，也不等于用户提出了新目标。要改方案时回到 shipwright-flow。结果页交给 shipwright-recap。
