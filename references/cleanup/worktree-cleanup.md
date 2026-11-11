# Worktree and instance cleanup

This is the playbook that deletes user state with no code review to catch a slip. The gates below are the review.

1. Snapshot and audit. Record `df -h /`, then run `references/cleanup/worktree-audit.sh` from the shipwright repository root:

   ```sh
   references/cleanup/worktree-audit.sh [-b <pr-base-ref>] [repo-path]
   ```

   The script is read-only. It never deletes. Without `-b` it checks `MERGED` against `origin/HEAD`, so pass `-b origin/<branch>` when pull requests target another branch. It reads paths from `git worktree list`, never from a hand-typed path, because a typed `myrepo-worktrees/x` misses a worktree that lives somewhere else. See [encode lessons in structure](../principles/encode-lessons-in-structure.md). It classifies each worktree by size, age, merge state, uncommitted work, pull-request state, and the newest chat that touched it, then suggests a bucket. The transcript scan is slow, so run it in the background. See [build the lever](../principles/build-the-lever.md).

   The script looks for transcripts under Claude Code's project directory and under two other hosts' session directories that group by project. Codex and OpenCode do not group sessions by project, so the script does not search them. For those hosts, ask the user which chats are still pinned or active instead of guessing from a global scan.

2. The bucket is advice, not permission. The pinned and active chats are the real artifact. See [prove it works](../principles/prove-it-works.md). Get that set from the user and cross-check every candidate. The script has marked `safe` a worktree the user had pinned, so the pinned set wins.

3. Verify usage before deleting. For every `verify-recent-chat` row, or anything you doubt, send independent workers to read the transcripts and report whether the chat is pinned or ongoing and which worktrees it touches. Transcripts are bulk. See [guard the context window](../principles/guard-the-context-window.md). A pinned chat can spawn extra worktrees that are in use even when their names never appear in the sidebar. Pick each worker's model from the shipwright model settings.

4. Pause on irreversible loss. `wip:N` is N tracked uncommitted edits. Show the diff and get a decision first. Removing a clean worktree is recoverable from its branch. Uncommitted work is gone. `scratch:N` is untracked throwaway, safe to drop, but name the files. Clean, merged, and not-in-use may proceed. `wip` and in-use pause.

5. Prune the confirmed set. Show the list and wait for the user to confirm before you delete a worktree or a branch. Per confirmed path, `git worktree remove --force <path>`. If the directory survives on ignored build artifacts, remove that directory, then `git worktree prune`. Branch refs survive that, so no commits are lost. Deleting a branch is a separate confirmation. Confirm with `df -h /` and list the worktrees again.

6. Simulators and other reclaimers. Simulators are often the next largest win, on a machine that has them: `xcrun simctl --set testing delete all` (cloned test devices), `xcrun simctl delete unavailable`, and `xcrun simctl runtime list` then `runtime delete <id>` for old runtimes. More when the user asks: Xcode `DerivedData` and `iOS DeviceSupport`, a host's local state backup that the user names, and package caches (pnpm, uv, brew, yarn). Clear only caches the user has not said to keep.

Reply with `df -h /` before and after, the space reclaimed, the worktrees pruned, and a one-line reason for each one held back (in use by which chat, or uncommitted work).

## What this playbook does not delete

- Anything under `plans/`. Finished plans stay.
- Evidence the task still needs. See [evidence retention](evidence-retention.md).
