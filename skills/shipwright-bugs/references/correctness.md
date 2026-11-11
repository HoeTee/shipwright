<!--
Adapted from improve `references/audit-playbook.md` section 1 (MIT).
Copyright (c) 2026 shadcn
https://github.com/shadcn/improve
The finding-format and priority rubric at the bottom of that playbook
belong to the shared [finding.md](../../../references/finding.md). They are not copied here.
-->

# Correctness checks

What to look for. A finding is only a finding with evidence. "Probably races somewhere" is not a finding; `orders/api.ts:142 reads the row, then writes it, with no transaction` is.

The highest-trust category: real bugs found by reading, not speculation.

- Error handling: swallowed exceptions, empty catch blocks, `catch (e) { console.log(e) }` on critical paths, missing error states in UI code.
- Async hazards: unawaited promises, race conditions on shared state, missing cancellation/cleanup (stale closures in React effects, listeners never removed).
- Null/undefined flows: non-null assertions (`!`) on values that can be null, optional chaining hiding a value that must exist, unchecked array indexing.
- Boundary conditions: off-by-one, empty-collection handling, timezone/locale assumptions, integer overflow in counters/IDs.
- State machines: impossible-state combinations representable in types, status enums with unhandled branches (look for `default:` that silently no-ops).
- Concurrency: check-then-act on shared resources, missing transactions around multi-write operations, idempotency of retried operations (webhooks, queues).
- Type escape hatches: `any` / `as` casts / `@ts-ignore` clusters. Each one is a place the compiler was overruled.
- Resource leaks: unclosed handles, connections, subscriptions; missing `finally`.
