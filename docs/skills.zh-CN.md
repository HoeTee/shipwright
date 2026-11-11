# Skill 列表

[English](skills.md) · [日本語](skills.ja.md) · [한국어](skills.ko.md)

[README](README.zh-CN.md) 展示八个核心 skill。
本页列出全部 48 个 skill。
每一行是一件事。

shipwright-autopilot、shipwright-swarm、shipwright-arena 和 shipwright-eval 在你要求之前保持关闭。

## 开始

| Skill | 做什么 |
| --- | --- |
| [shipwright-flow](../skills/shipwright-flow/SKILL.md) | 选择阶段、范围，以及你允许的操作。 |
| [shipwright-help](../skills/shipwright-help/SKILL.md) | 显示速查卡和提示。它不开始工作。 |
| [shipwright-setup](../skills/shipwright-setup/SKILL.md) | 设置每个角色的模型，以及 Git 平台。 |
| [shipwright-rules](../skills/shipwright-rules/SKILL.md) | 起草项目规则文件。你同意之后才写入。 |

## 理解

| Skill | 做什么 |
| --- | --- |
| [shipwright-how](../skills/shipwright-how/SKILL.md) | 说明一块代码如何运作。 |
| [shipwright-why](../skills/shipwright-why/SKILL.md) | 说明代码为什么是这样。 |
| [shipwright-teach](../skills/shipwright-teach/SKILL.md) | 把 how 和 why 合成一份直白说明。 |
| [shipwright-recall](../skills/shipwright-recall/SKILL.md) | 找回之前的进度和决定。 |

## 发现

| Skill | 做什么 |
| --- | --- |
| [shipwright-audit](../skills/shipwright-audit/SKILL.md) | 审计仓库或指定范围，并按收益排序。 |
| [shipwright-roadmap](../skills/shipwright-roadmap/SKILL.md) | 根据仓库证据建议下一个功能。 |
| [shipwright-diagnose](../skills/shipwright-diagnose/SKILL.md) | 复现 bug 并找到原因。它不改代码。 |
| [shipwright-impact](../skills/shipwright-impact/SKILL.md) | 检查一处改动会在别处弄坏什么。 |

## 计划

| Skill | 做什么 |
| --- | --- |
| [shipwright-plan](../skills/shipwright-plan/SKILL.md) | 在 plans/ 写一份新代理可以执行的计划。 |
| [shipwright-architect](../skills/shipwright-architect/SKILL.md) | 跨函数边界做设计。从调用方开始。 |
| [shipwright-prototype](../skills/shipwright-prototype/SKILL.md) | 用一次性原型比较做法。 |

## 构建

| Skill | 做什么 |
| --- | --- |
| [shipwright-build](../skills/shipwright-build/SKILL.md) | 完成改动，并带回证据。 |
| [shipwright-autopilot](../skills/shipwright-autopilot/SKILL.md) | 长时间无人值守地循环推进。它不合并。 |

## 审查

| Skill | 做什么 |
| --- | --- |
| [shipwright-review](../skills/shipwright-review/SKILL.md) | 对一个版本报告已核实的发现。它不改代码。 |
| [shipwright-fix](../skills/shipwright-fix/SKILL.md) | 修复阻断项。它持有 AI 审查上限。 |
| [shipwright-interrogate](../skills/shipwright-interrogate/SKILL.md) | 用几方对立检查。每方用一次运行来证明。 |
| [shipwright-comments](../skills/shipwright-comments/SKILL.md) | 在审查前清掉坏注释。 |

## 交付

| Skill | 做什么 |
| --- | --- |
| [shipwright-ship](../skills/shipwright-ship/SKILL.md) | 打开 pull request 并跟进 CI。它不合并。 |
| [shipwright-signoff](../skills/shipwright-signoff/SKILL.md) | 为一个人准备审查包。 |
| [shipwright-land](../skills/shipwright-land/SKILL.md) | 在非作者验证并且你允许之后，合并那个版本。 |

## 合并之后

| Skill | 做什么 |
| --- | --- |
| [shipwright-deploy](../skills/shipwright-deploy/SKILL.md) | 发布改动，并检查目标环境。 |
| [shipwright-recover](../skills/shipwright-recover/SKILL.md) | 读故障日志，并打开一个新的修复 pull request。 |
| [shipwright-reconcile](../skills/shipwright-reconcile/SKILL.md) | 检查 plans/ 里已完成、受阻和过期的计划。 |
| [shipwright-debt](../skills/shipwright-debt/SKILL.md) | 把 shortcut 注释收成账本。 |
| [shipwright-prevent](../skills/shipwright-prevent/SKILL.md) | 改结构，使反复出现的错误不能再犯。 |
| [shipwright-reflect](../skills/shipwright-reflect/SKILL.md) | 提出 skill 改动。你同意之后才编辑。 |
| [shipwright-cleanup](../skills/shipwright-cleanup/SKILL.md) | 在你确认之后，清掉已合并的 worktree 和分支。 |

## 验证

| Skill | 做什么 |
| --- | --- |
| [shipwright-verify-create](../skills/shipwright-verify-create/SKILL.md) | 创建在真实产品上操作的项目 skill。 |
| [shipwright-verify-maintain](../skills/shipwright-verify-maintain/SKILL.md) | 产品变化之后，更新那个 skill。 |
| [shipwright-prove-create](../skills/shipwright-prove-create/SKILL.md) | 为代价最高的属性加上形式化证明。 |
| [shipwright-prove-maintain](../skills/shipwright-prove-maintain/SKILL.md) | 被证明的代码变化之后，更新证明。 |

## 领域知识

| Skill | 做什么 |
| --- | --- |
| [shipwright-bugs](../skills/shipwright-bugs/SKILL.md) | 写出一项任务的正确性检查。 |
| [shipwright-security](../skills/shipwright-security/SKILL.md) | 写出输入、权限和密钥的检查。 |
| [shipwright-test](../skills/shipwright-test/SKILL.md) | 写出如何测试行为，以及如何存放证据。 |
| [shipwright-structure](../skills/shipwright-structure/SKILL.md) | 写出模块、分层和删除的检查。 |
| [shipwright-perf](../skills/shipwright-perf/SKILL.md) | 写出在改速度之前如何测量。 |
| [shipwright-lean](../skills/shipwright-lean/SKILL.md) | 让每处改动保持小而完整。 |

## 额外工具

| Skill | 做什么 |
| --- | --- |
| [shipwright-swarm](../skills/shipwright-swarm/SKILL.md) | 运行并行 worker，并交回一份报告。 |
| [shipwright-arena](../skills/shipwright-arena/SKILL.md) | 比较做同一件事的候选，并保留强的部分。 |
| [shipwright-trail](../skills/shipwright-trail/SKILL.md) | 保留决策日志，并请另一个模型复查。 |
| [shipwright-recap](../skills/shipwright-recap/SKILL.md) | 为每个结果渲染一份 HTML 页面。 |
| [shipwright-write](../skills/shipwright-write/SKILL.md) | 写文档、pull request 文字和 commit 信息。 |
| [shipwright-skillsmith](../skills/shipwright-skillsmith/SKILL.md) | 编写或修改一个 skill。 |
| [shipwright-eval](../skills/shipwright-eval/SKILL.md) | 只在你要求时测量一个 skill。 |
