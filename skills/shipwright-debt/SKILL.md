---
name: shipwright-debt
description: "把 shortcut: 注释汇成技术债账本。用于：盘点故意留下的捷径。不要用于：找新问题用 audit。"
---

# shipwright-debt

何时用：盘点故意留下的捷径，或你要看 `shortcut:` / `ponytail:` 现在有多少。
何时不用：找新的缺陷、安全问题或结构问题。那是 shipwright-audit 和对应的领域 skill。改写法找 shipwright-lean。

本 skill 只读。它不改代码，除非你同意把账本写进文件。

## Steps

1. 在仓库根运行 [scan_shortcuts.py](scripts/scan_shortcuts.py)。它用 `git grep --no-index --exclude-standard`，跳过 `.git` 和 `.gitignore` 覆盖的文件，仍然看得到未跟踪文件。
2. 你指定了别的标记词（例如 `TODO`）时，加 `--marker TODO`。堆栈还有别的注释前缀时，加 `--prefix`。
3. 每一命中是一行。注释前缀把只是提到这个约定的散文排除在外。你再丢掉不是延期的命中，例如键盘快捷键说明。
4. 从注释里取出上限和升级条件，写成：`<file>:<line>, <简化了什么>. ceiling: <上限>. upgrade: <何时再看>.` 「简化了什么」来自你读过的那行代码。
5. 需要负责人时加 `--blame`。
6. 没有升级条件或触发条件的标记标 `no-trigger`。这些会静默烂掉。
7. 结尾写 `<N> markers, <M> with no trigger.` 没有命中时写 `No shortcut debt. Clean ledger.`

## Boundaries

上限仍然成立的标记是决定，不是新发现，除非预期负载已经越过上限。越过之后报告具体后果，规则在 shipwright-lean。注释不能豁免安全或数据完整性。

默认不写文件。要留下账本时先问。仓库已有 `plans/` 时写 `plans/shortcut-debt.md`；否则可以写 `PONYTAIL-DEBT.md`。你同意之后才写。

Codex、Claude Code、OpenCode 都用上面这条命令。用宿主的文件工具读代码，用宿主的 shell 跑脚本。

## Read next

[Shortcut ledger](references/ledger.md) 是 ponytail-debt 的全文。
