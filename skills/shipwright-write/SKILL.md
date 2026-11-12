---
name: shipwright-write
description: "文档、PR 描述、commit 信息、去掉 AI 腔。用于：写给人看的文字。不要用于：代码注释找 comments。项目 README 找 shipwright-readme。"
---

# shipwright-write

## When to use

何时用：文档、RFC、PR 描述、commit 信息，以及任何要给人看的说明。也用于去掉 AI 腔。项目 README 整页交给 shipwright-readme。

何时不用：代码里的注释。那是 shipwright-comments。项目 README 的版式、证据和图不在这里写。

## Procedure

四层都过，再过一遍用词。英文写作的层和禁用词在 [Technical writing](../../references/write/technical-writing.md) 与 [Unslop](../../references/write/unslop.md)。中文和审核材料的组织、语言优先顺序在 [Lifecycle technical writing](../../references/write/lifecycle-technical-writing.md) 与 [Calibrate the wording](../../references/write/lifecycle-unslop.md)。

1. 先定体裁：教程、操作步骤、参考，或解释。一种页面不混几种体裁，除非小节标题写明。
2. 结论或任务放在前面。一段一个意思。动作用祈使步骤。概念在细节之前。对照用表，顺序用列表。
3. 缩写第一次出现时定义。命令放进可复制的块。前提单独写。不可逆的步骤点明。旗标写默认值和范围。
4. 读一遍。删掉不开工的套话。每句论断对着代码或界面核对。路径读仓库确认，不编造目录树。
5. 再扫 AI 腔。英文材料用 unslop 的编号规则，删了的编号留空，不重新编号。中文材料用校准一节：句子写谁对什么做了什么，分清已完成、已验证、待确认、失败和未执行，保留否定、条件、例外和风险。不要把英文禁词表套到中文语法上。

## Language

用户对这份产物指定了语言，就用那个语言。其次用项目对这类材料的要求。其余沿用对话语言。同一任务可以中文解释、英文 PR 描述。命令、标识符、路径、字段和错误信息保留原文。

PR 描述写最终问题和行为变化，不记整段聊天。人工审核材料写清哪些已经验证、哪些检查会漏、哪些要用户决定。图和 HTML 帮助理解，不代替证据。

## Do not

校准用词不授权改代码、改结论，或删掉未解决的问题。不要为了短而删掉失败条件。没跑的检查不要写成通过。发现新的空话模式时提出来，不要在任务中途悄悄改本 skill。改 skill 交给 shipwright-skillsmith。
