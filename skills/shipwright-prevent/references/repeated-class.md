<!--
Lifecycle rule for a repeated defect class.
Sources, kept in full:
- code-review-lifecycle `references/verification.md` section 同类缺陷重复出现
- one sentence from `references/pr-workflow.md` (同类缺陷检查本次影响范围)
- one sentence from `references/execution-efficiency.md` (一次处理已确认实例)
- the behavior row from `references/validation-scenarios.md`
- the sentence from `assets/REVIEW.template.md`
The rest of those files belongs to shipwright-fix, shipwright-ship,
shipwright-test, and shipwright-rules.
-->

# Repeated defect class

## From verification

审查记录或已确认修复表明同一类错误至少出现两次时，核对现有检查为何没有拦住。只读审查给出证据与修复建议；已有返修授权时，在本次范围内优先消除共享根因，或补合适的类型、lint 或行为回归检查。选择最小有效办法，不自动扩大为架构重写。

让检查在真实的旧错误或等价坏输入上失败、修复后通过，复用既有验证入口；适合 CI 的稳定检查接入同一清单。仅增加文字提醒不算防止复发，检查仍不能证明的部分要保留限制。项目既定必需检查照常满足。

正例：不同接口重复漏掉归属校验，修复共享授权入口并用无权限用户访问他人记录的用例验证拒绝结果。反例：只在文档增加“注意权限”，或增加一条错误实现也能通过的测试。

## Same class inside this change

作者先核实意见，再修复或附依据处理误报。风格交给已有工具，避免无价值改写。同类缺陷检查本次影响范围内的其他实例，复用原线程；无新证据不重复报告已处理事项。

先搜索本次影响内同类引用，一次处理全部已确认实例。不能把“链接仍存在”当成“命令执行有效”，也不能把旧测试目录机械改成另一个无断言的目录。

真实问题复现或核证后修复，误报附理由；同类检查其他受影响实例。同一问题复用原线程，无新证据不重复报告。

## Expected behavior

同类缺陷至少出现两次：在授权范围内修根因，或补上有效检查。坏行为必须失败，修复后通过。只增加文字提醒，或检查拦不住旧错误，都不算完成。

一次性的缺陷交给 shipwright-fix。这里只处理已经重复的类。
