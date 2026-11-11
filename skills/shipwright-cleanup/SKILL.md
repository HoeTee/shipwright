---
name: shipwright-cleanup
description: "清理已合并的 worktree、分支、临时实例和草稿；任务结束（PR 合并或关闭）后再清截图临时目录。删除 worktree 和分支前列清单等你确认。用于：任务结束，或工作区堆积。不要用于：任务没结束时不删证据；计划文件永不删。"
---

# shipwright-cleanup

## When to use

何时用：任务已经结束，或工作区里堆了 worktree、模拟器和缓存。

何时不用：任务还没结束。那时不删证据。`plans/` 里的计划永远不删，做完也不删。

## Worktrees

先审计，再给人确认，然后才删。步骤全文在 [Worktree cleanup](../../references/cleanup/worktree-cleanup.md)。脚本只读，自己不删东西：

```sh
references/cleanup/worktree-audit.sh [-b <pr-base-ref>] [repo-path]
```

路径相对 shipwright 仓库根目录。PR 不是合进默认分支时加上 `-b`。

1. 记下 `df -h /`，跑脚本。分类来自 `git worktree list`，不要手打路径。
2. 桶只是建议。用户钉住的和还在进行的会话优先。脚本把仍被钉住的 worktree 标成 safe 时，以钉住的为准。
3. `verify-recent-chat` 和拿不准的，派独立 worker 读会话记录，确认是否还在用。
4. `wip:N` 先给 diff，等决定。未提交的改动删了就没了。`scratch:N` 可以丢，但要说出文件名。
5. 删除 worktree 和分支之前，列出清单，等用户确认。确认后 `git worktree remove --force <path>`，目录还在就清掉忽略的构建产物，再 `git worktree prune`。分支引用还在，提交不会丢。删分支是另一次确认。
6. 用户点名的模拟器克隆和包缓存可以清。没点名的缓存不动。

回复写清清理前后的磁盘、收回多少、删了哪些、每个留下的一行原因。

## Evidence

任务进行中，验证用的清理只删这次拉起的实例和草稿。按进程名乱杀不行。删完要确认证据还在。规则在 [Evidence retention](../../references/cleanup/evidence-retention.md)。

任务结束是 PR 合并，或任务关闭。那时删除整个 `/tmp/shipwright-<plan-id>/`，以及评测的 `/tmp/shipwright-eval-<plan-id>/`。

不删 PR 附件，不删没有 PR 时放在 `.shipwright/evidence/` 里的关键截图，不删 `plans/` 和已经内嵌了截图的 HTML 结果页。

云端会话的 `/tmp` 会随会话消失。关键截图要在那之前上传并内嵌。这不改变「任务没结束不主动删」的规则。
