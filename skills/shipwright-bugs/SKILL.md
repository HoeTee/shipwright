---
name: shipwright-bugs
description: "正确性和可靠性：每个阶段查什么、防什么。用于：任务带 bugs 标签。不要用于：流程问题找阶段 skill。"
---

# shipwright-bugs

何时用：任务带 bugs 标签，或这一阶段要核对正确性、并发、重试和状态归属。
何时不用：流程怎么推进找对应的阶段 skill。测得出来的慢找 shipwright-perf。权限、注入和密钥找 shipwright-security。

本 skill 只提供知识。它不路由，不改代码，不写计划，不出审查结论。

## Rules

1. 每条发现都要有具体输入和错误结果，并指到 `file:line`。没有案例就不是发现。
2. 先修共享根因，再核对调用方。症状处打补丁会把证据盖住（原则 `fix-root-causes`）。
3. 会重试的写操作，重复执行和中途崩溃都要收敛到同一终态（原则 `make-operations-idempotent`）。
4. 多个执行者可能写同一份状态时，先去掉共享写（原则 `separate-before-serializing-shared-state`）。
5. 两次修复共享同一个前提、又没通过同一道检查：先把前提写下来并直接验证（原则 `attack-the-premise`）。
6. 密钥只写位置和类型。界面证据的路径和遮挡规则在共享 `references/evidence.md`。

原则正文在共享目录，见 [principles](../../references/principles/README.md)。这里不复述。

## Stage checks

### Stage 0 — Understand

追调用链和状态归属：数据从哪进、存在哪、从哪出，谁可以写。重启后才出现的失败，先看持久化状态（配置、缓存、锁、序列化结果）。

### Stage 1 — Discover

全仓或指定范围按 [Correctness checks](references/correctness.md) 查。改动或仓库的行为按 [Bug and scale](references/bug-and-scale.md) 的 Bug 与 Scale 两条给具体案例。诊断在真实界面复现，这一阶段只读。

### Stage 2 — Plan

计划写明停止条件：哪条命令、哪种界面状态算修好。先定数据形状，让不该出现的状态写不出来。队列、webhook 和多步写入写清幂等三问。

### Stage 3 — Build

先改共享代码里的根因，再改被带坏的调用方。保留原有的错误处理和失败断言。用户能看到的缺陷，修复前后在同一界面、同一步骤留证。

### Stage 4 — Review

按 Bug 与 Scale 核对这次改动。签名、返回值或行为变了，核对接得到的每一个调用方。一个人没问题、预期负载下会错的，记在 Scale，并写明你假定的负载。

### Stage 5 — Pull request

阻断项的审查次数和上限只在 shipwright-fix 里定义。CI 失败先分类再重跑，分类在 shipwright-ship。本 skill 只要求：失败日志能对上 Bug 或 Scale 里的哪一条。

### Stage 6 — After merge

运行日志按原因分流（shipwright-recover 的知识）。同一类错误第二次出现，按 shipwright-prevent 改结构。同一前提的修复再次失败，先验证前提。

## Read next

- [Correctness checks](references/correctness.md)：improve 第 1 类清单全文。
- [Bug and scale](references/bug-and-scale.md)：Ponytail 的 Bug 与 Scale，含改动和全仓两种表述。
