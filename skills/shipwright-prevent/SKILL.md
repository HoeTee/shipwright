---
name: shipwright-prevent
description: "同类错误出现两次，就改结构让它不能再犯。用于：同一类问题反复被纠正。不要用于：一次性 bug 用 fix。"
---

# shipwright-prevent

何时用：同一类错误至少出现两次，或你又一次纠正了同一个错误。
何时不用：一次性缺陷找 shipwright-fix。起草仓库的 `AGENTS.md`、`CLAUDE.md`、`REVIEW.md` 找 shipwright-rules。从对话里提炼 skill 改动找 shipwright-reflect，写 skill 找 shipwright-skillsmith。

本 skill 改仓库结构，让下一个只打开了邻近文件的人无法再犯。它不重写整个架构。

## Steps

1. 读最近的提交、回滚、审查评论、代理说明文件，以及解释变通做法的注释。把错误分成类。同一类要有两次才算。
2. 选能生效的最高一层，从高到低：架构、类型、lint 或 CI、行为测试、文档。文档只留给需要判断的事。见 [Make the mistake impossible](references/correct.md)。
3. 同一类在本次影响范围内的其他实例一次处理完。规则原文在 [Repeated defect class](references/repeated-class.md)。
4. 最常见的类现在就修，一类一个提交。新检查要在真实的旧错误或等价坏输入上失败，修复后通过。本地和 CI 跑同一条命令。
5. 例外写在出错的那一行：理由、到期日、以及人的批准。
6. 在代理说明文件里保留规则表，英文表头 `Rule` 和 `Enforcement`。跑 [check_rule_table.py](scripts/check_rule_table.py)。只靠文档、注释或提醒拦住的行，脚本会失败。
7. 你再次纠正时，先修这次的错误，再补规则。规则已经写过但没有强制手段，就是复发，同一次改动里把它升到更高一层。某类错误已经不可能发生时，删掉对应规则。

原则 `encode-lessons-in-structure` 在共享目录，见 [principles](../../references/principles/README.md)。能用结构拦住时，只留结构，不另加一段提醒。

## Reply

每一类写：证据、选中的层、更高一层为什么做不到。

## Platforms

Codex、Claude Code、OpenCode 用同一梯子。检查接进仓库已经在跑的 lint、类型或测试命令。
