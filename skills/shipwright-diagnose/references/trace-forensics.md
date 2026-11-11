# Trace forensics

Source: pstack `playbooks/trace-forensics.md`. Distinct from [runtime-forensics.md](runtime-forensics.md), which instruments the live process. Here the capture already exists. The artifact is a fixed dataset. Read it. Do not re-run it.

Keep tooling generic. A DevTools or trace parser for a cpuprofile and a `.json.gz`. A text editor for a spindump. The repo's heap tool for a heapsnapshot. `scripts/trace_to_sqlite.py` loads a Chrome trace or a cpuprofile JSON into sqlite so the queries below have a table to run against.

1. Identify the format and load it with the right tool. Parse a large artifact in an independent worker and keep the reduced finding in the main thread. That is principle `guard-the-context-window`.
2. Transform the raw artifact into a form you can query. Dump the trace or heap snapshot into sqlite, one row per sample, frame, or node. Reach the queryable shape before you read.
3. Narrow to the cause. Query for the frames that hold the most time and walk the call tree to the hot path. For a leak, follow the retainer chain from the leaked object to a GC root. For a spindump, find the thread stuck on-CPU or blocked and its wait reason.
4. Attribute to source. Map the hot frame to file, symbol, and line via the artifact's own symbols. A frame with no source mapping is not yet a diagnosis. Resolve the symbols, or say plainly that the artifact does not carry them.
5. If you have a paired capture, diff the before and after artifacts to confirm. Otherwise, mark the finding as the strongest hypothesis the artifact supports, not a confirmed cause.
6. Hand back a cited diagnosis. No fix unless asked. Route to shipwright-build once the cause is known. The throughput checkpoint stays one line: `throughput checkpoint: n/a, read-only forensics`.

**Reply:** the artifact and format, the reduced finding, the source location, the artifact paths, and whether a paired capture confirmed it.
