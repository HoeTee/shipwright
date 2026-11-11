# Project working notes

> 这是输出结构模板。生成时将各段写成有依据的项目内容并移除此提示；未知内容明确写“待确认”或“拟议”，不得编造路径、命令与通过状态。已有等价来源优先引用。

## Goal and scope

说明服务谁、要完成什么、主要输入输出、怎样算可接受；列明确非目标。链接权威需求及其适用范围。

## Status and constraints

说明当前项目阶段、已确认决定和重要假设。把已有实现、目标与计划分开。

## Modules and responsibilities

列实际模块、入口、交接关系及来源；只有想法时写拟议结构。详细设计链接维护中的资料。

## Implementer conventions

写本项目有效的编码、数据、配置、状态、副作用及失败行为约定。复用已有 AGENTS.md 等来源，不复制出矛盾规则。

## Verification entry points

| Object | Command or entry | Environment and dependencies | When it runs | Pass bar and status |
|---|---|---|---|---|
| 按项目事实填写完整条目 | 命令未建立则明确待建立 | 标明不可达部分 | 必需或按影响触发 | 记录本次是否实际执行 |

说明类型、语法与行为检查的边界，链接完整验证矩阵。不能用模板行当作已有有效检查。

## Platform and review

记录所选平台/手册及操作绑定入口、作者和审查任务的加载方式、人工关口、版本绑定和 AI 往返规则。详细 PR 操作链接项目流程。

## Deployment and delivery

摘要已确认部署画像：管理方式、必要运行时、目标环境、产物/传递、执行者、验收及恢复入口。首次或变化确认，未定则明列。分列开发、CI、发布和目标验收，凭据只引用。

## Maintenance

列权威需求、设计、验证、审查与部署资料。实现、规则或环境变化时更新受影响来源，保留必要证据。
