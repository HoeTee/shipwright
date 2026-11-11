# Runtime forensics

Source: pstack `playbooks/runtime-forensics.md`. Use this when a live process is the evidence. The deliverable is a cited diagnosis, not a fix.

You own the diagnosis. Instrument the live process. Do not theorize from source alone.

1. Capture the live signal on the matching surface. A CPU profile for a spinning process, a heap snapshot for a leak, a DevTools trace for a visual glitch. A real artifact, not a guess. Save it under `/tmp/shipwright-<plan-id>/<sha7>/`.
2. Reduce the artifact to the smoking gun: the function on the hot path, the retainer chain from the leaked object to a GC root, the loop firing without input. Parse a large artifact in an independent worker. Keep the reduced finding in the main thread. That is principle [guard-the-context-window](../../../references/principles/guard-the-context-window.md). A trace or heap dump that is JSON can be loaded with `scripts/trace_to_sqlite.py` before it is queried.
3. Prove the mechanism before believing it. Inject instrumentation on the running process, or hotfix the live code without reloading, to confirm the hypothesis cheaply. Read-only means the hotfix is not committed and the worktree is restored when the check is done. If you cannot touch the live code without a write grant, say the mechanism is unproven and stop.
4. Map the finding back to source: file, symbol, the line that allocates or schedules.
5. The throughput checkpoint stays one line: `throughput checkpoint: n/a, read-only forensics`.

**Reply:** the signal captured, the reduced finding, how you proved the mechanism, the source location, and the artifact paths. No fix unless asked. Hand back to shipwright-build once the cause is known. A performance number's limits are shipwright-perf, principle [explain-the-number](../../../references/principles/explain-the-number.md).
