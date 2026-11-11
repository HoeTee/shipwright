# Fan out

Four adversaries. Each gets the same scope and the same intent, and a different worktree. Copy uncommitted changes into each worktree. A finding survives only when that adversary's command is rerun and the output still breaks the intent.

## Seats

Use the models shipwright-setup recorded for review. When the host can run two model families, split the four seats across those families. When it cannot, say that the adversaries shared a family. Do not invent a model slug.

Give each adversary its own output directory: a git worktree when possible, otherwise `/tmp/shipwright-<plan>/<sha7>/worker-<n>/`.

## Spawn

Spawn all four in one step when the host allows parallel workers. Each prompt contains the scope, the intent, the output path, and the brief in [brief.md](brief.md). The brief replaces a design rationale. An adversary that returns nothing is a dropout. Continue with the rest and record the dropout.

## Verify

Rerun each finding's command. Keep it when the output shows the failure and the failure breaks the intent. Drop style, naming, and risks that need a future change to matter. Merge findings that share a root cause. Do not pick one adversary's list and discard the others. Do not apply fixes.

No verified findings is a valid result.
