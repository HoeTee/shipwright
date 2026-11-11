---
name: shipwright-recall
description: "开工或接手前找回之前的进度和决定。用于：新会话续做。不要用于：当前会话进度找 recap。"
---

# shipwright-recall

何时用：新会话要续做，或开工前要找回最近的进度和决定。
何时不用：当前会话的进度页用 shipwright-recap。要把习惯写成个人 skill 用 shipwright-skillsmith。

本 skill 只读。它重建上下文，不改仓库，不重做已经做完的工作。

## Steps

1. 先分类。要续的是某一个先前会话，走 [session-pickup.md](references/session-pickup.md)，不要走下面的广搜。用户已经给了完整状态（路径、分支、改动）就直接用，不再翻记录。
2. 搜索前钉死范围：时间窗（「最近」默认 7 天）、话题、工作区（默认当前这一个）。把范围说回去。不许悄悄把「全部」收成「最近 N 条」。不读其他项目的会话，除非对方明确要求。
3. 在自己的会话记录里分片并行查找。按修改时间排序，不按 UUID 名字。先搜话题，再只读命中的会话和相关段落。跳过当前会话，以及执行者、评测和测试会话。每段返回同一格式：话题、用户目标、决定、未完成的线、卡住和被纠正的地方、产物（PR、工单、分支），并引用会话 id。只有一两个会话时自己搜，不派工。原文留在执行者那边。会话文件的位置和查找脚本见 [procedure.md](references/procedure.md)，命令是 [find_sessions.py](scripts/find_sessions.py)。
4. 话题点名了功能、文件、子系统、区域或 bug 时，同时扫共享记录。这是默认，不是可选项。「我在 X 上做的」也不能免。交给 shipwright-why 的调查者，问题改成：现在是什么状态、试过什么没站住、用户还在报什么。来源剧本照 why 的用。和会话查找并行。没有接上的来源记为缺口。只有「这周我做了什么」这种纯活动回忆才跳过这一步。
5. 用 `git` 和宿主的 git 客户端核对挖出来的 PR、分支和工单。答案取决于当时实际跑了什么时，读完整会话，不读裁过的副本。
6. 按下面的契约写简报。按线分组。停在点名的话题上。

派工见 [hosts.md](../shipwright-how/references/hosts.md)。恢复审查或交接时，先有当前事实，再补历史，步骤在 [method.md](references/method.md)。

## Output

- **Capsule.** 最多 5 条。这件工作是什么，整体停在哪。
- **Threads.** 每条线一行，且只有一个状态标签：`[merged #N]`、`[open PR #N]`、`[in flight <branch>]`、`[verified, uncommitted]`、`[reverted #N]`、`[planned, not started]`。没有标签就不算写完。
- **Problems.** 最多 5 条反复出现的问题。包括用户还在报的症状，以及已经发布又被回滚的修复。
- **Next move.** 一个最有用的下一步，要具体。

不相关的功能和工单不写，除非它挡住这一件。篇幅不够时先砍细节，不砍线。会话发现用会话 id 引用，共享记录用 PR 号、工单号、聊天链接或错误跟踪编号引用。公开输出前去掉私人上下文。

## Stop

简报交回 shipwright-flow，由它路由剩下的工作。恢复会话不重置审查计数，也不扩大授权。旧报告只是线索。不重跑上一轮的复现，不重做已完成的步骤。继承来的结论要在真实产物上核对，原则是 [prove-it-works](../../references/principles/prove-it-works.md)。一份先前的自述通过不算证明。
