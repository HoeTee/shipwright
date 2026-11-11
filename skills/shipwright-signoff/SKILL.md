---
name: shipwright-signoff
description: "准备人工终审包（P0–P2、关键片段、explainer、证据）；改了交互的附截图和 30–60 秒视频；记录你的结论。用于：技术检查都过了、合并前。不要用于：修问题找 fix。"
---

# shipwright-signoff

何时用：必需检查通过，阻断项已经清除，合并前要人做最后一次判断。
何时不用：还有要修的阻断项时回到 shipwright-fix。本 skill 不合并，也不部署。

人工终审和 HTML 页面都保留。页面是报告，不截图。产品界面的截图可以嵌进页面。

## Procedure

1. 按 [packet.md](references/packet.md) 准备一页材料：对象、目标与范围、P0/P1/P2 未解决数量和逐项发现、关键片段和 explainer 七问、技术证据、业务结果、需要人决定的问题。零发现也写 `P0: 0 · P1: 0 · P2: 0`。沉默和「看到了」不是通过。用户只同意方案，不等于验收了实现。
2. 聊天里给同一份结论。HTML 用仓库根的 `scripts/render_html.mjs` 生成，不要把渲染器搬进本目录。草稿和命令见 [html.md](references/html.md)，内容模型见 [html-explainer.md](../../references/html-explainer.md)，页面检查见 [progress-interaction.md](../../references/progress-interaction.md)。也可以用 [render_signoff.py](scripts/render_signoff.py) 写草稿再调用那个渲染器。Node 缺失或渲染失败时说明缺项，聊天结果照常给出。
3. 改了交互的，按 [interaction-gate.md](references/interaction-gate.md) 附上这次候选的关键截图和 30–60 秒视频，遮挡密钥后放进 PR，并写入计划的证据附录。没有 PR 时写到 `.shipwright/evidence/<计划编号>/<commit 前 7 位>/`，该目录保持 gitignore。停在可合并，等结论。
4. 真实业务任务的数量没定过，就只问一次「这次真实验收要跑几个任务？」证据字段见 [business-tasks.md](references/business-tasks.md)。发布后才做的检查标成待验收，不标成已经通过，也不拿它替换合并前的必需检查。
5. 把人的原话、PR、commit 和证据记进 Run record 的 Human verdict。有授权时写到 PR，并标明是代记，不冒充别人的 Approve。平台要求有资格的人审批时，由那个人在平台上完成。

## Stop

人要求修改：回到 shipwright-fix，沿用原来的审查计数。人给出通过，而且授权里有合并：交给 shipwright-land。没有合并授权：停在可合并。

通过不自动变成发布或部署授权。
