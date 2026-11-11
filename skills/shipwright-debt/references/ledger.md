<!--
Adapted from ponytail-debt (MIT).
https://github.com/DietrichGebert/ponytail
The host-specific paragraph is replaced with a host-neutral scan.
-->

# Shortcut ledger

Every deliberate shortcut is marked with a `shortcut:` comment naming its ceiling and upgrade path. Older code may say `ponytail:`. This collects them into one ledger so a deferral cannot quietly become permanent.

Codex, Claude Code, and OpenCode run the same read-only scan. Reply in the user's language. The summary lines below stay in this wording so the ledger is stable.

## Scan

Search the repo for comment markers, skipping `.git` and everything the `.gitignore` files ignore:

```bash
python skills/shipwright-debt/scripts/scan_shortcuts.py
```

The script runs:

`git grep --no-index --exclude-standard -nE '(#|//|/\*) ?(shortcut|ponytail):'`

Add other comment prefixes with `--prefix` when the stack uses them (for example a second pattern for `--` comments). If the user names their own marker word (for example `TODO`), pass `--marker TODO` and the script searches for that word instead.

Each hit is one ledger row. The comment prefix keeps prose that merely mentions the convention out of the ledger. Skip hits that are not a deferral, like a note about a keyboard shortcut. The script prints every regex hit; you drop the non-deferrals before you call the ledger done.

## Output

One row per marker, grouped by file:

`<file>:<line>, <what was simplified>. ceiling: <the limit named>. upgrade: <the trigger to revisit>.`

The convention is `shortcut: <ceiling>, <upgrade path>`, so pull the ceiling and the trigger straight from the comment. The script's `ceiling:` and `upgrade:` fields are that split. You write `<what was simplified>` from the code the comment is attached to, not from a guess about a file you did not open.

For an owner per row, pass `--blame`. The script adds `git blame -L<line>,<line>`.

Flag the rot risk: any marker comment that names no upgrade path or trigger gets a `no-trigger` tag. Those are the ones that silently rot.

End with `<N> markers, <M> with no trigger.` Nothing found: `No shortcut debt. Clean ledger.`

## Boundaries

Reads and reports only. Changes nothing. To persist the ledger, ask first, then write it through the normal edit path. In a repo that already uses `plans/`, `plans/shortcut-debt.md` is the shipwright place. Otherwise a root file such as `PONYTAIL-DEBT.md` matches the older name. Do not write the file until the user agrees.

A marker whose ceiling still holds is a decision, not a new defect. shipwright-lean owns that rule. This skill only collects the markers.
