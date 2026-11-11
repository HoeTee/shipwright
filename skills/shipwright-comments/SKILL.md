---
name: shipwright-comments
description: "清理坏注释，约束性注释改成类型、测试或 lint。用于：送审前。不要用于：写文档找 write。"
---

# shipwright-comments

何时用：送审之前，清掉叙述性注释、注释掉的废代码，以及用注释代替结构的回避。
何时不用：给人读的文档用 shipwright-write。本 skill 不扩大功能范围。

## Procedure

1. 范围用调用方给的文件或 diff。没有就用相对基线的当前 diff，含工作区。
2. 派一个独立工作者，提示词用 [comment-sicko.md](references/comment-sicko.md) 全文，再附上范围。步骤和拒绝规则见 [procedure.md](references/procedure.md)。Codex 用 subagent 或云端代理，Claude Code 用 Agent 工具，OpenCode 用 task，子代理类型 general。没有子代理就自己按那份提示词另过一遍，并写明。
3. 检查它的报告。拒绝它改产品逻辑、越界、删掉有例外保护的注释、写错的 MUST KILL。对含糊的 `IMPORTANT` 或 `do not remove`，先读 [shipwright-how](../shipwright-how/SKILL.md) 或 [shipwright-why](../shipwright-why/SKILL.md)。被驳回的报告点名原因重跑一次。
4. 接受的小问题直接删死代码、去掉无用参数或改用真实 API。需要改形状时，让 shipwright-architect 只出草图，然后在范围内做最小的根因修改。原则 [fix-root-causes](../../references/principles/fix-root-causes.md) 和 [redesign-from-first-principles](../../references/principles/redesign-from-first-principles.md) 只指导意图，不授权扩大范围。见 [principles](../../references/principles/README.md)。
5. 约束性注释（不要删、不要改措辞、改之前问某人）能改成类型、测试或 lint 时，先给出最便宜的方案并等待同意。未同意就删掉注释、把约束记为未落实，并写出范围外的草图。无人值守时，没有事先同意就不编码。
6. 报告删除数量、恢复的注释、REVIEW 保留项、重跑、草图、已做的修改和仍开放的约束。

## Stop

注释清理完就停。不在这里做功能审查，也不开 PR。
