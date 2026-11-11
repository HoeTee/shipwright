---
name: shipwright-interrogate
description: "几个对手各自用运行结果证明问题。用于：高风险或有争议的设计。不要用于：普通改动用 review。"
---

# shipwright-interrogate

何时用：高风险或有争议的设计，普通审查之外还要有人用运行结果来证伪。
何时不用：普通改动用 shipwright-review。本 skill 只报告，不改代码。

## Procedure

1. 范围用用户点名的对象。没有点名时，用相对默认分支合并点的分支差异，加上工作区。用自己的话写下意图。意图不清楚就问一个问题。
2. 按 [fan-out.md](references/fan-out.md) 派四个对手。每个对手一份 worktree，简报用 [brief.md](references/brief.md) 里的原文。没跑出来的不算发现。
3. 你亲自重跑每条发现的命令。输出仍显示失败，而且这个失败破坏意图，才保留。同一根因合并成一条。丢掉的写出条数和原因。
4. 没有核实发现是有效结果。不为了填满报告制造问题。

## Platforms

Codex 用 subagent 或云端代理，Claude Code 用 Agent 工具，OpenCode 用 task，子代理类型 general。不能并行时按同一简报逐个做，并写明。模型用 shipwright-setup 记下的审查角色；能分两个模型家族就分开，不能分就说明他们是同一家族。

## Stop

证据目录用 `/tmp/shipwright-<计划编号>/<commit 前 7 位>/worker-<n>/`。不把对手的复现改合并进产品分支。

## Handoff

回复意图、保留的发现（命令、输出、破坏了哪条意图、谁发现的）、每个对手丢掉的条数。要修才交给 shipwright-fix。
