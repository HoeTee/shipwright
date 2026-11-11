---
name: shipwright-architect
description: "跨函数边界的设计：先写调用方用法，再定类型和接口，至少两种方案。用于：新模块、新接口。不要用于：小改动或做法已定。"
---

# shipwright-architect

何时用：新模块、新接口，或跳进代码会把错误的形状定死。
何时不用：小改动，或做法已经定了。只读地整理现有结构用 [shipwright-how](../shipwright-how/SKILL.md)，不走本流程。

本 skill 产出类型、签名和取舍。`plan` 模式停在草图。`change` 模式才按草图填代码，并且要有本地修改授权。

## Phase A. Ground

先弄清新代码会碰到的每个系统。对相关子系统跑 shipwright-how，产出它规定的架构说明。只点一个文件名不算接地。设计会改掉归属或分层时，再跑 shipwright-why，让已有理由变成约束，而不是猜测。真正的绿地、周围没有要接入的系统时，可以跳过这一相。

## Phase B. Sketch

先写调用方怎么用：README 式的用法，加两三处真实调用。类型从用法推出来，两边不一致时改类型。然后交给 shipwright-arena，每个候选的提示词用 [runner-prompt.md](references/runner-prompt.md)。至少两个结构上不同的方案，即使第一个看起来已经够用。这是原则 [exhaust-the-design-space](../../references/principles/exhaust-the-design-space.md)。合成前用 [design-red-flags.md](references/design-red-flags.md) 筛每一份。比较接口深度，优先把复杂度藏在更小的公开面上。持续的结构检查在 shipwright-structure，这份清单是设计这一步用的筛子。

## Phase C. Agree

默认不设人工关口，直接往下。对方明确说「先给我看再写」时，交出合成结果并停。对方否定形状时，把反对当作 Phase A 的新证据，重做 Phase B，然后再写代码。想在写之前加压，用 shipwright-interrogate。

## Phase D. Implement

用代码替换 `not implemented`，用逻辑替换伪代码。草图是合同。偏离要说出来，不悄悄吸收。`plan` 模式不进入这一相，把草图和理由交给 shipwright-plan。

## Phase E. Scrap

实现反复产生草图吸收不了的摩擦时，扔掉草图，不在错误设计上打补丁。信号是反复出现的模式，不是单个边界。判据、重做顺序和原则名在 [procedure.md](references/procedure.md)。

## Output

小改动一份类型和签名。大改动再加模块图。理由按 [rationale-template.md](references/rationale-template.md)，包含用法和合成决定。完整分相、arena 要额外遵守的约束，都在 [procedure.md](references/procedure.md)。

## Stop

没有两个不同的方案，就不合成。红旗没过，就不进入实现。模式是 `plan` 时不写产品代码。结果页交给 shipwright-recap。
