# Project working notes

> 输出结构模板。根据当前仓库及已确认要求填写，移除此提示。未知内容标为待确认，拟议要求单列；不编造路径、命令或通过结果。完整草案经用户确认后再写入。

## Purpose and boundaries

说明当前仓库服务的用户、主要输入输出和已确认约束。引用权威需求或已有 `AGENTS.md` 等资料，不重复另一份完整规则。

## Modules, interfaces, and state

| Module or entry, with source | Responsibility | Inputs, outputs, and handoff | State owner and failure handling |
|---|---|---|---|
| 按已核实路径填写 | 写实际任务 | 核对接口或字段和真实消费方 | 谁修改、清理及传播错误 |

保留相关权限、兼容性与共享状态约束。没有依据的设计理由标为未知，详细说明链接维护中的来源。

## Working agreements

记录适用于本仓库的实现与审查约定，明确范围和来源。区分当前行为、已确认要求和待采用建议，不能因代码现状如此就认定它正确。

## Verification entry points

| What is checked | Command and location | Preconditions and dependencies | Trigger, pass bar, and run status |
|---|---|---|---|
| 按项目行为填写 | 未有命令则标待建立 | 标明实际环境或不可达部分 | 分清已通过、失败、未执行和待确认 |

链接已有测试与 CI 清单，不把模板行当作已存在的检查。

## Review and maintenance sources

引用 `REVIEW.md`、实际规则加载入口及其他权威资料。说明哪些事实和要求仍待确认，代码或约定变化时更新对应来源。
