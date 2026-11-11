# GitHub watcher

`scripts/watch-pr/` is the optional GitHub watcher preserved from the source. It is not a default step on Gitee or plain git, and it does not cover those forges. It needs a local `gh` and the `commander` package declared in `scripts/package.json`. The upstream installer beside it expects a lockfile that was not in the source archive, so do not treat that installer as ready.

When the watcher is not installed, read status with `gh pr checks` and `gh pr view`, then classify a failure with `scripts/classify_ci.py`.

Watcher verdicts used by the babysit procedure:

| Verdict | Meaning |
| --- | --- |
| READY | One PR, or a stack, can merge. Stop. Do not merge here. |
| WAITING / merge-queue | The frontier is merge-ready and waiting on the queue. Stop the watcher. |
| ADVANCE | Someone else merged the frontier. Continue with the new frontier. |
| COMPLETE | Someone else finished the queue. Stop. |

On any other forge, use that forge's mergeability and unresolved threads. Do not invent the four verdicts there.
