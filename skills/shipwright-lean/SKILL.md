---
name: shipwright-lean
description: "精简：最小完整改动，不加没要求的东西，shortcut: 约定。用于：写任何代码（默认常驻）。不要用于：你说 stop lean 时关闭。"
---

# shipwright-lean

何时用：正在写代码。默认开着，级别是 full，直到你说 `stop lean`、`stop ponytail` 或 `normal mode`。
何时不用：你说停之后。只读的理解、审计和审查可以读本 skill 的检查清单，但不会因此改代码。

本 skill 是写法知识。它不决定阶段，不合并，不代替审查报告。

## Rules

1. 用最小的完整改动做完这件事。没人要的功能、选项和灵活性点名后跳过。
2. 按六步梯子取第一件能完整工作的做法：不做、仓库里已有、标准库或平台、已经安装的依赖、一眼能看懂的一行、否则最少的代码。见 [Smallest complete change](references/smallest-change.md)。
3. 懒的是方案，不是改动本身。调用方、测试和夹具被带坏的部分要一起做完。
4. 这些不能为了变短而删：信任边界上的校验、防止数据丢失的错误处理、安全、无障碍、真机校准、你明确要的东西。
5. 有已知上限的捷径写成 `shortcut: <ceiling>, <when-to-upgrade>`。旧代码里的 `ponytail:` 同样算。上限仍成立是决定，不是发现；实际负载已经超过上限，要报告具体后果。注释不能豁免安全、数据完整性或项目必需要求。
6. 级别保持到你改口：`lean lite`、`lean full`、`lean ultra`（旧说法 `ponytail lite|full|ultra` 同样有效）。交给独立执行者时，把这些规则写进简报。

原则 [laziness-protocol](../../references/principles/laziness-protocol.md) 在共享目录，见 [principles](../../references/principles/README.md)。梯子以本 skill 为准。

## Stage checks

### Stage 0 — Understand

只读。精简不改写法。先看清改动必须到达的调用方、测试、夹具、配置和导出。

### Stage 1 — Discover

快速审计时列出可删的死代码、没人设的选项、只有一个实现的抽象、必须一起改的近似副本。清单在 [Lean checks](references/lean-checks.md)。带上限的 `shortcut:` 先交给 shipwright-debt，不重复当成缺陷。

### Stage 2 — Plan

把这次不做的事写进范围外，并各用一行说明为什么不做。

### Stage 3 — Build

默认 full。lite 先按要求做，并用一行写出更小的做法让你选。ultra 在动手前对没有依据的部分提出异议。新的非平凡逻辑留下一个小测试或自检。搬动代码时，校验和错误处理跟着走。

### Stage 4 — Review

按 [Lean checks](references/lean-checks.md) 的「一次改动」清单看。按职责拆，不按行数拆。没有实际缺陷的精简建议标成非阻断建议。

### Stage 5 — Pull request

返修保持最小完整改动：补上这次必须到达的调用方和测试，不借返修加没要求的层。

### Stage 6 — After merge

`shortcut:` 由 shipwright-debt 收成账本。没有升级条件的标记会静默烂掉，账本里标 `no-trigger`。

## Read next

- [Smallest complete change](references/smallest-change.md)：六步梯子、never cut、三级行为。
- [Lean checks](references/lean-checks.md)：改动和全仓两份精简清单，以及 shortcut 规则。
