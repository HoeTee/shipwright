---
name: shipwright-reconcile
description: "对账 plans/：复核 DONE、查 BLOCKED、刷新过期计划。用于：新会话开始、合并之后。不要用于：找新问题用 audit。"
---

# shipwright-reconcile

何时用：新会话开始，或一批变更合并之后，先看 `plans/` 还成不成立。
何时不用：找新问题用 shipwright-audit。本 skill 不删计划文件。

`plans/` 已被别的用途占用时，目录是 `advisor-plans/`。编号只增不减。

## Procedure

1. 读 `plans/README.md` 和每一份计划。用 [reconcile_plans.py](scripts/reconcile_plans.py) 列出状态。BLOCKED 和 IN PROGRESS 会标成需要处理。
2. 按 [reconcile.md](references/reconcile.md) 处理：
   - DONE：只抽查便宜的 done criteria 在当前 HEAD 上是否还成立。成立就在索引里标已复核。
   - BLOCKED：读原因，在代码里看障碍还在不在。做法根本变了就新编号；只是刷新就改原文件。不再做就标 REJECTED，附一行理由。
   - IN PROGRESS 且已经过期：告诉用户，执行者可能中途停了。有 worktree 就去看。
   - TODO：跑 drift check。漂移了就先确认问题还在，再更新 Current state 摘录和 `Planned at`。问题已经没了就标 REJECTED，理由写 fixed independently。
3. 摘录必须来自你自己打开的代码，不抄子代理报告里的行号。
4. 趋势指标（行数、审查轮次、P0/P1/P2、合并后是否返工）有新事实就追加到 Run record。这只是趋势，不说明 skill 省了多少。AI 审查上限仍只由 shipwright-fix 定义，这里不改那个数。

## Stop

报告四件事：哪些 DONE 复核过，哪些计划刷新了，哪些 REJECTED，现在哪些可以执行。不写新的实现，也不开 PR。

## Handoff

下一份要执行的计划交给 shipwright-build。索引格式沿用 [index.md](../shipwright-plan/references/index.md)。
