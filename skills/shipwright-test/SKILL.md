---
name: shipwright-test
description: "测试和验证：分层、TDD、测行为、证据标准；统一证据规则的主人。用于：任何改动。不要用于：真实操作入口找 verify-create。"
---

# shipwright-test

## When to use

任何改动都按这里的分层、TDD 和证据规则验证。本 skill 定规则。build 写测试并执行，ship 把同一条命令放进 CI。

## When not to use

项目还没有像用户一样操作的入口时，交给 shipwright-verify-create。并发、状态机、涉及钱、测试很难碰到的属性，交给 shipwright-prove-create。性能数字交给 shipwright-perf。

## Rules

1. 测调用方、用户或其他服务能观察到的行为。原则 [test-behavior-not-implementation](../../references/principles/test-behavior-not-implementation.md) 见 [共享原则目录](../../references/principles/README.md)。
2. 用这次 commit 的真实产物证明。原则 [prove-it-works](../../references/principles/prove-it-works.md) 见同一目录。
3. 多步改动每一步结束都有可执行检查，通过了再做下一步。原则 [sequence-verifiable-units](../../references/principles/sequence-verifiable-units.md) 见同一目录。
4. 预期来自已确认的契约。把当前实现的输出抄成预期，证明不了正确。
5. 只有单元测试不算验证完成。影响界面或输出的改动，在对应界面实跑并留证。
6. 统一证据规则只写在共享的 [evidence.md](../../references/evidence.md)。shipwright-test 维护那一份。本目录的 [evidence.md](references/evidence.md) 只是指针。

## Layers

分层、验证矩阵、检查范围、外部服务不可达和证据字段见 [layers.md](references/layers.md)。回归不是单独一层。

| 层 | 谁执行 |
| --- | --- |
| Lint 和类型检查 | 项目正在用的工具。本地和 CI 同一条命令 |
| 单元 | bug 先写失败用例。build 写 |
| 特征测试 | 动结构之前钉住现有行为 |
| 接口 / 契约 | 输入、响应、错误、权限、副作用 |
| 集成 | 真实组件的字段、状态、失败传播 |
| 端到端 | `verify-<app>`，按证据规则留截图 |
| 视觉一致 | [visual.md](references/visual.md) |
| 性能 | shipwright-perf |
| 形式化 | shipwright-prove-create / shipwright-prove-maintain |
| UAT | shipwright-signoff、shipwright-deploy |
| 构建与部署适配 | shipwright-deploy |

## TDD

用户明确要求先写失败测试，或这条 bug 有一条便宜、清楚的测试路径时，按 [tdd.md](references/tdd.md)。先看到因预期原因失败，再改产品代码，再看到通过。

路径要大套夹具、脆弱替身、很慢的端到端、只有生产才有的状态，或写完就该删时，不要硬加测试。改用最近的可执行检查，并写明原因。

## Coverage

审计和审查查哪段没测的代码危险时，读 [coverage.md](references/coverage.md)。没有一条命令能知道仓库能不能用，这是风险改动之前的第一项缺口。

## Evidence

目录是 `/tmp/shipwright-<plan-id>/<sha7>/`。文件名 `<kind>-<slug>.<ext>`。种类用 `before`、`after`、`variant-a`、`baseline`、`diff`、`lane01`–`lane10`、`review`。

关键截图和视频先遮挡密钥，再由 shipwright-ship 上传为 PR 附件，链接记进计划的证据附录。没有 PR 时存 `.shipwright/evidence/<plan-id>/<sha7>/`，该目录留在 `.gitignore`。证据不进 Git 历史。

## Hosts

Claude Code、Codex、OpenCode 共用这份说明。正文不写宿主的工具名。浏览器操作用项目已有的方式；没有时用 Playwright。HTML 结果页交给 shipwright-recap。报告、进度页和讲解页本身不截图。
