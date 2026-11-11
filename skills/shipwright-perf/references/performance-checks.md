<!--
Adapted from improve `references/audit-playbook.md` section 3 (MIT).
Copyright (c) 2026 shadcn
https://github.com/shadcn/improve
-->

# Performance checks

Look for the algorithmic and architectural wins, not micro-optimizations.

- N+1 patterns: a query or fetch per item inside loops or per list-row rendering; missing batching or a dataloader.
- Wrong complexity: nested scans over the same collection, repeated `find` or `filter` inside hot loops where a map keyed lookup belongs.
- Caching gaps: identical expensive computations or fetches repeated per request or render; missing memoization at clear function boundaries; no HTTP or data-layer caching on stable data.
- Payload size: over-fetching (selecting every column, full objects where ids suffice), missing pagination on unbounded lists, large JSON shipped to clients.
- Frontend, when the repo has one: bundle composition (heavyweight dependencies for trivial use), missing code-splitting on rarely-hit routes, unoptimized images or fonts, client-side fetching for data available at render time, render waterfalls. For React or Next.js, defer to the repo's framework conventions and any installed best-practices guidelines.
- Backend: synchronous work that belongs in a queue, missing indexes implied by query patterns (flag for verification; do not claim an index is missing without schema evidence), connection-per-request patterns where pooling exists.
- Build and CI: slow CI from missing caching, redundant pipeline steps, test suites that could parallelize.

A Scale finding (correct for one user, wrong for many) belongs to shipwright-bugs. This list is for work that is correct and costs too much. Both can be true of the same loop; report each with its own evidence.

Ponytail's Speed item, for one change and for a whole repo: big slowdowns are problems. Small wins (work repeated in a hot loop) are suggestions; some software counts every millisecond. A suggestion stays off the blocking list unless a project rule says otherwise.

Every number on this list still goes through [Benchmark checklist](benchmark-checklist.md) before it is used to choose a fix.
