---
name: shipwright-help
description: "速查卡和可直接发送的提示词，不开工。用于：问怎么用、该用哪个。不要用于：要真干活找 flow。"
---

# shipwright-help

## When to use

何时用：用户问怎么用、该用哪个 skill，或要一条可以直接发送的提示词。

何时不用：用户要真的开工。开工交给 shipwright-flow。本 skill 不改仓库、不派 worker、不写计划。

## Reply

1. 先判断问题属于哪一类。不清楚就只问一个选择题：安装和模型、开工、选 skill、写作和审查、其他。
2. 读对应参考再回答。不要编造频道、仓库编号或模型 slug。
3. 回复三块：白话答案、一条可复制的下一条提示词（用户已经要求执行时不附）、答案来自哪份参考。
4. 只回答用法。不要打开浏览器，不要创建云端任务。

## Card

精简级别在 shipwright-lean：lite 先做所求并点出更小的做法，full 是默认的最小完整改动，ultra 先质疑请求。级别保持到用户改口。说 stop lean 就关掉。对照表在 [Ponytail card](../../references/help/ponytail-card.md)。

| 用户要 | 打开 |
| --- | --- |
| 不知道从哪开始 | shipwright-flow |
| 本机模型和 Git 平台 | shipwright-setup |
| 仓库缺规则或规则冲突 | shipwright-rules |
| 代码怎么跑，或为什么这样 | shipwright-how，shipwright-why；要讲清楚用 shipwright-teach |
| 接上一会话 | shipwright-recall |
| 追赶这次对话 | shipwright-recap |
| 按切片并行 | shipwright-swarm |
| 同一任务多份候选 | shipwright-arena |
| 长任务决策日志 | shipwright-trail |
| 给人看的文字 | shipwright-write |
| 项目 README | shipwright-readme |
| 新写或修改 skill | shipwright-skillsmith |
| 工作区堆积或任务结束 | shipwright-cleanup |

完整路由、提示词配方，以及「把任务改深而不是改大」的四问，在参考里。把任务改深时：先说专业人士会多做哪一步、从什么原材料开始、用什么方法、用什么外部结果证明做对了，然后改写提示词，把该用户决定的选择留空。

## References

- [Route map](../../references/help/route-map.md)
- [Prompting](../../references/help/prompting.md)
- [Recipes](../../references/help/recipes.md)
- [Sharpen](../../references/help/sharpen.md)
