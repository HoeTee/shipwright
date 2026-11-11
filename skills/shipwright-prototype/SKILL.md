---
name: shipwright-prototype
description: "用一次性原型回答哪种做法更好；视觉决策每个方案留截图。用于：有实验能回答的分歧。不要用于：纯偏好问题直接问你。"
---

# shipwright-prototype

何时用：有一个实验能回答的分歧，包括布局、交互、密度、行为或时序。
何时不用：没有要做的决定。纯偏好、跑实验也分不出高下，直接问对方，并给出选项。一两处改动做法已经明显，交给 shipwright-build。

原型是一次性的仪器。真正的实现走 shipwright-build。选定的方向还要定形状时走 [shipwright-architect](../shipwright-architect/SKILL.md)。

## Steps

1. 先写明这个原型要决定什么。没有决定，就不做原型。
2. 设计空间还开着时，先找已有做法，收一版主题、配色和布局的参照，让对方选方向再动手。方向已经定了就跳过。
3. 在生产源码之外的临时目录里做。用 `/tmp/shipwright-<plan-id>/prototype/`。视觉决策用最轻的 HTML、CSS 和 JS。行为或时序决策用能碰到问题的最小脚本。不用生产框架，不写测试，不做抽象。
4. 比较多个方案时，放在同一个开关后面，每个方案有标签。至少给出对方没点名的一个变体。这是原则 `exhaust-the-design-space`。
5. 在对应界面上验证。视觉决策每个方案一张截图，路径 `/tmp/shipwright-<plan-id>/<sha7>/variant-<letter>-<slug>.png`，并实际操作。行为或时序决策记下时间、输出或画面。这里的观察就是测试，不是断言。无法判断或拍错界面不算通过。密钥先遮挡。
6. 给出方案、取舍和推荐。有计划文件时，把分支、SHA 和截图链接记进计划的证据附录。然后停。

细则在 [procedure.md](references/procedure.md)。原则 `experience-first`：先在扔掉的原型里做决定，不在生产代码里做。

## Stop

回复写明探索了哪些方案、证据、取舍、推荐和临时目录，并明说原型是扔掉的。不把原型合并进仓库，不把它当成可发布的代码。结果页交给 shipwright-recap。原型截图是产品界面，可以进证据。讲解页本身不截图。
