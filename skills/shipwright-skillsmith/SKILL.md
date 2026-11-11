---
name: shipwright-skillsmith
description: "新写或修改 skill（含本插件和项目 skill）；要证明改动有效时交给 shipwright-eval。用于：要新增或修 skill。不要用于：从对话提炼经验先用 reflect；跑分找 eval。"
---

# shipwright-skillsmith

## When to use

何时用：要新写或修改一个 skill，包括本插件和项目自己的 skill，也包括按用户习惯生成的个人 mode skill。

何时不用：先从这次对话里提炼经验。那是 shipwright-reflect，用户同意后才改 skill。要跑分比较，直接用 shipwright-eval。

## Author

按 [Authoring](../../references/skillsmith/authoring.md) 写。

1. Frontmatter 有 `name` 和 `description`。格式见 https://agentskills.io 。Claude Code 上如果已有它自己的写作说明，就遵循那份说明。不要调用只存在于某一家的更新命令。
2. 正文用中文，大约 120 行。细则放 `references/`。目录、文件名、路径占位符和结构性标题用英文。
3. 引用的文件必须存在。能用路径指向别的 skill 或原则时，不要把它们再抄一遍。
4. 只保留会改变决定的句子。拿不准就删。
5. 结构有变化时补可核对的检查。纯偏好的措辞不用配测试。
6. 在 `skills/` 下增删文件后，运行 `python scripts/build_opencode_index.py`，提交生成的 `skills/index.json`。不要手改目录。

任务做到一半发现 skill 坏了：在单独的 PR 里修，不要在当前任务里悄悄绕过去。

## Personal mode

用户要一份跟着自己习惯走的 `-mode` skill 时，走 [Automate me](../../references/skillsmith/automate-me.md)：先找已有的，再只挖本工作区的会话，用选择题问缺口，按证据写小节，用 shipwright-write 收散文，在 worktree 里提交。不要把一次对话里的偏好写成规则。不要把 shipwright-flow 的内容抄进用户的 mode。

## Prove it

要证明这次 skill 改动真的改变了结果时，把改前和改后交给 shipwright-eval。本 skill 不自己跑评测，也不把用户的主观「像不像我」说成评测通过。主观 mode 可以在用户点头后交付。用户要的是效果证明时，仍然交给 shipwright-eval。
