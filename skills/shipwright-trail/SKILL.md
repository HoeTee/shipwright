---
name: shipwright-trail
description: "决策日志 TSV，交付前换一个模型复查。用于：长任务或无人值守。不要用于：短任务不用。"
---

# shipwright-trail

## When to use

何时用：长任务或无人值守，需要一份以后能核对的决策日志。

何时不用：短任务。不要为了几步操作另起一份日志。

## Log

只保留一份 TSV。一行一个决定。单元格单行。evidence 列是指针，不是一段话。表头在 [decision-log-template.tsv](../../references/trail/decision-log-template.tsv)。列是 `ts`、`phase`、`decision`、`why`、`evidence`、`result`。

用仓库里的脚本追加，它会写时间、补表头，并挡掉会被表格软件当成公式的开头：

```sh
references/trail/log.sh <logfile> <phase> <decision> <why> <evidence> <result>
```

路径相对 shipwright 仓库根目录。只记分叉、做完并验证的一步、转向或回退、阻塞、修好的门禁。循环一轮一行。显而易见的动作不记。

默认不提交。放在工作目录的 `decisions.tsv`，多件事并行时放 `.audit/<task-slug>.tsv`，并排除出 git。只有审阅者必须靠这份日志才能信任结果时才提交。截图不进 git，evidence 列指向 [Evidence](../../references/evidence.md) 里的路径或 PR 附件。

只追加。写错了就新加一行取代它，不改旧行。

一次对话是一轮。接手续做或新开会话是新的一轮。接到已有日志时，第一行的 phase 是 `start`，写明前面哪些时间范围不是本轮写的。`start` 不用于别的意思。

格式、例子和会话目录在 [Decision log](../../references/trail/decision-log.md)。

## Before handoff

交回前对照本轮会话记录核对日志。只读本工作区的会话目录，不跨项目去翻。每一行对得上真实决定，证据打得开，而且确实证明那一行所说的。漏记的分叉补上一行。核对只追加，不删行。

然后换一个不同模型家族的 worker 读日志和会话记录，标出证据弱、验证被跳过、事后看有风险的选择，以及扫一眼会漏掉的缺口。回复末尾用 Attention 一节：第一行是 `reviewed by <model>`，然后每条指向具体行。没有问题就写 No flags。模型名不能省。

其他 skill 要决策日志时引用本 skill，不要另造列。
