# Dependencies and migrations

Source: improve audit playbook, category 6, plus the migration-entry table from lifecycle `execution-efficiency.md`. The rest of that lifecycle file belongs to shipwright-fix and shipwright-ship. Domain checklists for bugs, security, performance, tests, and structure are those skills, not this file.

## What to look for

- Major-version lag on a core framework or runtime. Not every minor bump. The ones with a real cost to staying behind: end of life, security-fix cutoffs, ecosystem incompatibility.
- Deprecated APIs in use that have announced removal timelines.
- Abandoned dependencies (no release in years, archived repos) on critical paths.
- Duplicate dependencies solving the same problem (two date libraries, two HTTP clients).
- Lockfile or manifest drift, and version pinning inconsistencies across a monorepo.
- For each migration candidate, estimate blast radius (files touched). That drives effort and whether to recommend it at all. The consumer check itself is shipwright-impact.

## Migration entries

When a directory, module, resource, or test-discovery path moves, build a short map: old location, new location, consumer, verification entry. Separate the move, what stays, and a thin compatibility entry. Check the files git is tracking now. Historical archives keep their original time and meaning.

| Entry | Must check | Verification |
| --- | --- | --- |
| Source dependency | import, dynamic module name, relative resource root | a real install or load, and the callers |
| Command and process | CLI, background job, subprocess, admin and acceptance scripts | the command unchanged; run it from outside the repo when that is how it is used |
| Tests and CI | discovery directory, registration list, CI path | the actual executed count is non-zero; an exit code alone is not enough |
| Build and delivery | package discovery, module manifest, resource copy, protect or package choice | what is actually in the final artifact, and that startup consumes it |
| Deploy and config | host path, container path, config consumer | a redacted fixture parse; a real run when it is required |
| Current docs | links, commands in code blocks and tables, preconditions | a link existing and a command running are separate checks |

Search the affected area for the same kind of reference and handle every confirmed instance in one pass. A link that still exists is not a command that still works. Do not turn an old test directory into another directory with no assertions.

Positive: after tests move next to the component, fix the discovery config, CI, and the README command, run the documented command, and record the count.
Negative: the first pass fixes source imports, the second discovers the build manifest, and the third discovers that the README runs zero tests. Each pass fixes only the line that was named.

## Hand off

A migration plan is shipwright-plan. The plan estimates the surface and splits the work into verifiable steps. Principle [migrate-callers-then-delete-legacy-api](../../../references/principles/migrate-callers-then-delete-legacy-api.md) is in the shared principles directory: move callers, then delete the old API. This file does not implement the move.
