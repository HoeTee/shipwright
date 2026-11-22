# Never Block on the Human

When: Use when tempted to ask "should I do X?" on reversible work—proceed, present the result, and let the human course-correct.

The human supervises asynchronously. Agents must stay unblocked. Make reasonable decisions, proceed, and let the human course-correct after the fact. Since code changes are reversible and reviewable, a wrong decision usually costs less than blocking.

- Proceed, then present. Do the work, show the result. Don't ask "should I do X?" Do X, explain why.
- Make the system self-healing. When you notice a problem, log it and fix it in the next round.
- Irreversible actions (force-push, delete production data, send external messages) still require confirmation.
- Reversible actions (write code, edit notes, split tasks) should proceed without blocking.
- Product direction comes from the human. Execution should not block.
- This does not cover a user who explicitly asked to think a requirement or concept through. Follow [clarify.md](../../skills/shipwright-flow/references/clarify.md). own and watch may adopt a recommendation and mark it as an assumption only when the user did not ask for that discussion. Do not treat silence, "continue", or the end of a count as approval.
