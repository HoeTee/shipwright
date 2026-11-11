# Guard the Context Window

When: Use when context is filling up (large outputs, long files, repeated reads, fan-out)—route bulk to subagents and keep summaries in the main thread.

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.
