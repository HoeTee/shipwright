---
name: shipwright-structure
description: "架构和技术债：模块深浅、分层、重复、删减。用于：重构、新模块、技术债。不要用于：具体设计动作找 architect。"
---

# shipwright-structure

何时用：重构、新模块、分层、重复实现、死代码、技术债。
何时不用：具体设计动作（先写调用方、至少两种方案、综合成一份设计）找 shipwright-architect。故意留下的 `shortcut:` 账本找 shipwright-debt。

本 skill 只提供知识。它不路由，不改代码，不写计划。

## Rules

1. 先看读者要跨几层、要记住多少隐藏状态（原则 `minimize-reader-load`）。行数和圈复杂度只是代理指标。
2. 先定数据形状，再写逻辑（原则 `foundational-thinking`、`model-the-domain`）。非法状态用类型写不出来（原则 `type-system-discipline`）。
3. 先删后加（原则 `subtract-before-you-add`）。新需求按「从一开始就有这条要求」重新想一遍，再分成可验证的小步交付（原则 `redesign-from-first-principles`）。
4. 换内部 API 时，先迁调用方，再在同一次改动里删掉旧 API（原则 `migrate-callers-then-delete-legacy-api`）。没有外部兼容包袱时才适用。
5. 校验和解析放在边界，不把传输类型重新导出（原则 `boundary-discipline`）。
6. 每个状态一个写入者，每件任务一条做法。内部实现从模块外导入就会让构建失败。

原则正文在共享目录，见 [principles](../../references/principles/README.md)。这里不复述。

## Stage checks

### Stage 0 — Understand

查设计理由和当时的约束。理由不清楚时，先把现在的数据形状和所有权画出来，再谈拆分。

### Stage 1 — Discover

按 [Tech debt and architecture](references/tech-debt.md) 查重复、分层、死代码、三种并存的做法、只有一个实现的抽象。候选形状用 [Design red flags](references/design-red-flags.md) 过一遍。故意留下的捷径交给 shipwright-debt 汇成账本，不在这里当成新缺陷。

### Stage 2 — Plan

跨函数边界的设计至少两种方案，每种先过红旗筛查。范围外写明这次不搬的模块。迁移按调用方切成可验证的小步，最后一步删除旧入口。

### Stage 3 — Build

重构先钉住现有行为，再删后加。大改用新旧输出比对或界面冒烟证明行为没变。调用方迁完才删旧 API。测试改为断言新契约，删掉只保护旧实现细节的测试。

### Stage 4 — Review

看这次改动有没有把模块变浅、把内部决定泄漏到多个调用方、或留下第二条做法。送审前的坏注释按 shipwright-comments 处理：能变成类型、测试或 lint 的，不留在注释里。

### Stage 5 — Pull request

结构和债本身不增加提交检查。该在审查前处理的红旗，不留到合并说明里用文字补救。

### Stage 6 — After merge

`shortcut:` 账本由 shipwright-debt 更新。同一类结构错误出现两次，按 shipwright-prevent 改成构建或类型会失败。任务结束后的工作区清理不删计划，也不提前删证据。

## Read next

- [Tech debt and architecture](references/tech-debt.md)：improve 第 5 类全文。
- [Design red flags](references/design-red-flags.md)：八条红旗全文。
