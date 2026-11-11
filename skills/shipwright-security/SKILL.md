---
name: shipwright-security
description: "安全：边界校验、权限、注入、密钥处理（截图也要遮挡密钥）。用于：涉及用户输入、权限、密钥。不要用于：流程问题找阶段 skill。"
---

# shipwright-security

何时用：改动或审查涉及用户输入、权限、注入、密钥、上传、Cookie、CORS，或 Ponytail 的 Risk（含数据丢失）。
何时不用：流程怎么推进找对应的阶段 skill。正确性和负载行为找 shipwright-bugs。

本 skill 只提供知识。它不路由，不改代码，不写计划。

## Rules

1. 只报有代码证据的问题。模式、生产影响、修复写在发现里。
2. 安全发现描述更安全的 API 或校验边界。不给可运行的演示字符串，不写逐步误用步骤。计划停在代码、配置和测试。
3. 密钥只写 `file:line` 和类型。修复包含轮换，不只是从文件里删掉。已提交的密钥视为已经泄露。
4. 截图、证据、计划和回复里不出现密钥值和个人数据。上传前先遮挡。
5. 校验放在系统边界（原则 `boundary-discipline`）。边界以内信任已经校验过的类型。
6. `shortcut:` 或旧的 `ponytail:` 不能豁免安全、数据完整性或项目必需要求。容量上限仍然成立时，保留该决定，安全问题另行报告。
7. 依赖审计只读运行，只报告影响到可达运行代码或构建发布路径的 critical / high。用 [filter_advisories.py](scripts/filter_advisories.py) 过滤，不安装包，不拉取利用细节。

原则正文在共享目录，见 [principles](../../references/principles/README.md)。这里不复述。

## Stage checks

### Stage 0 — Understand

读 ADR 和决策文档里已经记下的取舍。文档与代码不一致时，报告决策漂移。文档不能用来压掉漂移。

### Stage 1 — Discover

按 [Security checks](references/security-checks.md) 和 [Risk](references/risk.md) 查。没有代码位置的猜测不进发现表。标准平台约定（例如代理环境变量、本地开发工具调用已配置的包管理器）本身不是发现。

### Stage 2 — Plan

把校验放在边界：解析外部数据、核对身份和归属、限制上传的类型和大小。计划里的密钥修复写明轮换和更安全的配置来源。

### Stage 3 — Build

信任边界上的校验、防止数据丢失的错误处理、安全相关分支，不因为精简而删掉。shipwright-lean 的 never cut 清单在这里生效。搬动或合并代码时，原有的校验和错误处理跟着走。

### Stage 4 — Review

安全是正确性之后的第二优先。核对用户输入、权限、密钥、写入顺序和事务。高风险或有争议的设计，知识上需要对手用运行结果证明问题（shipwright-interrogate 的场合）。

### Stage 5 — Pull request

安全项进入人工终审包，由人看过。分流机器人评论时，不因为描述里已经有截图就自动驳回安全评论。

### Stage 6 — After merge

同一类安全错误出现两次，用类型、lint 或构建失败把它固定下来（shipwright-prevent）。只在说明里加一句提醒不算完成。

## Read next

- [Security checks](references/security-checks.md)：improve 第 2 类全文。
- [Risk](references/risk.md)：Ponytail Risk，以及注释不能豁免安全的规则。
