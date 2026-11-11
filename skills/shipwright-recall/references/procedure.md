# Recall procedure

Source: pstack `recall`, with the host tooling map removed. One specific prior chat is [session-pickup.md](session-pickup.md), not this procedure. The review-shaped companion is [method.md](method.md). Locating transcript files is `scripts/find_sessions.py`.

Before starting or resuming work, rebuild the recent working context and hand back a tight capsule of where things stand and what to do next. Read only what the in-scope threads need, then stop.

## Two records

Your own chat history holds what you did and decided. The shared record holds what happened around the same code under other names: symptoms users keep reporting, fixes that shipped and got reverted, errors still firing in production. That second record is what shipwright-why searches. A feature with a long bug tail keeps most of its story there. Do not reconstruct it from transcripts alone.

## Where transcripts live

This plugin targets Codex, Claude Code, and OpenCode. Cursor and Pi paths stay so a transcript found there is not ignored. Each transcript file is JSONL, except OpenCode which stores JSON. Find the active workspace's directory. If you cannot tell the host, check which of these exist. Do not glob across every project's directory.

- **Claude Code:** `~/.claude/projects/<slug>/<session-id>.jsonl`. `<slug>` is the workspace path with every character that is not a letter or digit turned into `-` (`/Users/you/proj` becomes `-Users-you-proj`).
- **Codex:** `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`, not grouped by workspace. Keep only files whose first line has `payload.cwd` equal to the workspace path.
- **OpenCode:** `~/.local/share/opencode/storage/`. Sessions are JSON files under `session/<project-id>/`, with messages under `message/` and `part/`. Open a session only when its metadata names this workspace.
- **Cursor:** `~/.cursor/projects/<slug>/agent-transcripts/<uuid>/<uuid>.jsonl`. `<slug>` is the workspace path with the leading slash dropped and each `/` turned into `-`.
- **Pi:** `~/.pi/agent/sessions/--<slug>--/<timestamp>_<id>.jsonl`. `<slug>` drops the leading slash and turns each `/` into `-`, and the directory is wrapped in `--`.

`scripts/find_sessions.py` prints matching paths and modification times. It does not print transcript bodies.

## Steps

1. Classify, then route. One specific prior chat to resume is [session-pickup.md](session-pickup.md). Turning habits into a durable personal skill is shipwright-skillsmith. A human-readable summary of the work is a different task. Recall loads working context across recent chats before you act. If the user already gave a full state capsule (paths, branch, the change), use it and skip the mining.
2. Lock the scope before searching. Pin the window ("recent" is a real range, default the last 7 days), the topic if named, and the workspace (default the active one). Never read another project's transcripts without being asked. State the scope back. Never quietly turn "all" into "recent N".
3. Fan out across chat history. Dispatch parallel workers on a fast model, each taking a slice. Order candidates by modification time, never by UUID name. Search the topic first, then read only the matching chats and only their relevant regions. Skip the current chat and obvious noise (worker, eval, and test chats). Each returns the same schema, one block per chat: topic, the user's goal, decisions, open threads, struggles and corrections, and artifacts (PRs, tickets, branches), each citing the chat id. For one or two chats, skip the fan-out and search directly. Raw transcripts stay with the workers. The main thread gets only their findings. That is principle `guard-the-context-window`.
4. Sweep the shared record whenever the topic names a feature, file, subsystem, area, or bug. This is the default, not a judgment call, and "my work on X" does not exempt it. Hand it to shipwright-why's investigators, but steer the question from "why was this built this way" to "what is the current state, what has been tried and did not hold, and what are users still reporting". Reuse its per-source playbooks. Run the investigators in parallel with the chat mining. Inherit its posture: one investigator per source, null results are findings, skip an unavailable connector and say so. Fold what comes back into the brief. Skip this step only for pure activity recall with no named target ("what did I do this week"), where your own history and live state are the entire answer.
5. Verify against live state. Check the PRs, branches, and tickets with `git` and the host's git client. When the answer hinges on what an agent actually did (the tools it ran, files it read, errors it hit), read the full transcript, not a trimmed copy.
6. Write the brief to the contract below. Group by thread. Stay on the named topic.

## Output contract

Lead with the capsule, then the thread status, then the problems, then the next move. Deeper detail goes below or gets cut.

- **Capsule.** At most 5 bullets. What this work is and where it stands overall.
- **Threads.** One line each, prefixed with exactly one status tag: `[merged #N]`, `[open PR #N]`, `[in flight <branch>]`, `[verified, uncommitted]`, `[reverted #N]`, or `[planned, not started]`. A thread with no tag is not done yet, so tag it.
- **Problems.** At most 5, the recurring ones. Include the symptoms users keep reporting and any fix that shipped and was reverted, so the next attempt starts where the last one failed.
- **Next move.** The single most useful next action, concrete.

An adjacent feature or ticket stays out unless it blocks this one. When the capsule and thread lines outgrow a screen, cut detail before you cut threads. Cite chat findings by id and shared-record findings by their source (PR number, ticket id, chat permalink, error-tracker issue). Sanitize private context before any public output. Run the wording pass in shipwright-write.

## Review use

[method.md](method.md) applies when the task is to resume a review or a handoff. Current facts come first. History fills context. Restoring a session does not reset review counts or widen authorization. An old report is a lead. Compare its version, environment, and inputs with the current ones.

## Reply

The brief, to the contract above. Current session progress is shipwright-recap, not this skill.
