---
name: shipwright-how
description: "讲清一块代码怎么运作：入口、调用链、状态归属。用于：改陌生代码前。不要用于：问设计原因找 why。"
---

# shipwright-how

何时用：改陌生代码前，或要讲清一块代码怎么运作。
何时不用：问设计原因用 [shipwright-why](../shipwright-why/SKILL.md)。要大白话讲解用 [shipwright-teach](../shipwright-teach/SKILL.md)。要看改动会弄坏什么用 [shipwright-impact](../shipwright-impact/SKILL.md)。

本 skill 只读。不改仓库，不写计划，不开始设计。整理架构事实是为了回答问题或交给规则起草，不写入 `AGENTS.md`、`CLAUDE.md` 或 `REVIEW.md`。

## Steps

1. 收下问题、仓库和版本。范围含糊时先说出理解再查。拿不准就走简单路径。
2. 简单问题（单模块、小工具、一个函数）不派探索者。派一个讲解者，按 [explainer-prompt.md](references/explainer-prompt.md) 去掉 Explorer Findings 一节，自己读代码并写完。然后到第 5 步。
3. 复杂问题（跨多个文件或服务、横切功能、整段架构）拆成 2 到 4 个互不重叠的角度。同一轮派完全部探索者，每人只带自己的角度和 [explorer-prompt.md](references/explorer-prompt.md)。
4. 探索者都回来之后，派一个讲解者，把每份发现填进 [explainer-prompt.md](references/explainer-prompt.md)。讲解者自己核对矛盾，不从头重查。
5. 呈现讲解者的原文。可以做轻量澄清，不要整篇改写。用不上的节删掉：Overview、Key Concepts、How It Works、Where Things Live、Gotchas。

派工方式见 [hosts.md](references/hosts.md)。没有独立执行者时，按同样角色自己顺序做。分工、必须写清的事实和边界见 [procedure.md](references/procedure.md)。

## What to establish

从真实入口跟踪输入、分支、状态、返回值和副作用。跨 API、进程或脚本时核对两端字段、数据归属和失败传播。答案按用户能观察到的行为组织，附 `file:line`。代码推不出的部分写不确定。已有上下文继续用。只有需要新的行为证据时，才在授权范围内运行入口。静态推断不能写成已经跑过。

领域清单不在这里。追调用链和状态归属读 [shipwright-bugs](../shipwright-bugs/SKILL.md)。找现有测试和命令读 [shipwright-test](../shipwright-test/SKILL.md)。找热路径读 [shipwright-perf](../shipwright-perf/SKILL.md)。大段原始输出留在执行者那边。这是共享 principles 目录里的 [guard-the-context-window](../../references/principles/guard-the-context-window.md)。

## Architecture facts

为规则草案整理现有结构时，在调用链之外补齐模块与职责、接口与数据交接、状态归属、约束与未知项。表和正反例在 [architecture-facts.md](references/architecture-facts.md)。没有代码或资料支持的结构标为待确认。不编造目录、接口或已验证结果。输出交给 shipwright-rules，不自动写文件。

## Investigation

只读调查走 [investigation.md](references/investigation.md)。产物是带引用的解释，或带取舍表的建议。吞吐检查点写一行：`throughput checkpoint: n/a, read-only investigation`。不写代码，不开 PR。前提错了要说出来。

## Stop

设计动机交给 shipwright-why。调查之后如果真要改代码，把结论交回，由 shipwright-flow 改路由。本 skill 不调用 shipwright-architect。结果页交给 shipwright-recap。本 skill 不生成 HTML，也不给报告截图。
