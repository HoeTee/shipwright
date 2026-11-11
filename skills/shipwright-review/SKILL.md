---
name: shipwright-review
description: "对固定版本给出已核实的发现，只读不改。用于：提交前、PR 中、复审。不要用于：全仓体检找 audit；要修找 fix。"
---

# shipwright-review

何时用：提交前、PR 中、或对上一轮发现做复审。对象是 flow 已经固定的候选和基线。
何时不用：全仓体检用 shipwright-audit。要改代码用 shipwright-fix。本 skill 只读，不改产品代码。

## Procedure

1. 规则从可信基线读，不从候选里的新规则读。步骤见 [rules-baseline.md](references/rules-baseline.md)。缺规则时交给 shipwright-rules 起草，确认前不写入。候选版本怎么选定写在共享 `references/scope.md`；本轮沿用 flow 已经固定的基线、候选和范围，不另选。
2. 分支审查的范围和 `introduced` / `pre-existing` 标签见 [branch.md](references/branch.md)。
3. 按 [adversarial.md](references/adversarial.md) 做独立审查。顺序是正确性、安全、实际负载、有效测试、性能、必要复杂度。共享接口、状态、配置或产物变了，再读 [shipwright-impact](../shipwright-impact/SKILL.md)。
4. 报告句子用 [ponytail-review.md](references/ponytail-review.md) 的四句：这是什么、问题、修法、不修会怎样。级别只用 P0 / P1 / P2，定义在 [packet.md](../shipwright-signoff/references/packet.md)。没有实际缺陷的建议另列非阻断建议，不写成 P2。
5. 每条发现都要有具体输入和具体错误结果。打开被引用的代码。三类常见误报见 [vet.md](references/vet.md)：设计如此、证据指错位置、重复。否决的写进计划索引的 Findings considered and rejected。
6. 领域标签指向哪份就读哪份的提交前一节：[bugs](../shipwright-bugs/SKILL.md)、[security](../shipwright-security/SKILL.md)、[test](../shipwright-test/SKILL.md)、[structure](../shipwright-structure/SKILL.md)、[perf](../shipwright-perf/SKILL.md)、[lean](../shipwright-lean/SKILL.md)。`shortcut:` 或旧 `ponytail:` 注释在记录的限度内仍成立时，不把那个限度再报成缺陷；实际使用已经超限才报告后果。注释不能豁免安全或数据要求。
7. 复审比较上一次受审版本和新版本，核对原发现和相关影响。基线或影响面变了就重读完整 diff。静态依据和运行证据分开写。没有发现是有效结果。

## Platforms

有独立审查者时，审查者不能是写这份代码的人，而且只读这个候选 SHA。Codex 用 subagent，Claude Code 用 Agent 工具，OpenCode 用 task。没有子代理时自己再读一遍，报告里写明这不是独立审查。结论只对当前 SHA 有效。

## Stop

发现列表、疑点和已排除项交回。不在这里修。AI 审查计数只由 shipwright-fix 增加，本 skill 不写上限。

## Handoff

有阻断项且用户要修：交给 shipwright-fix，附上候选 SHA 和每条发现的证据。只要报告：停在这里，并由 shipwright-recap 出 HTML。HTML 报告本身不截图。
