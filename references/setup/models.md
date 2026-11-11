# Model settings

Write one model per role. shipwright-setup does this. It does not set the AI review cap. That number lives only in shipwright-fix.

The settings file:

- Claude Code: `~/.claude/rules/shipwright-models.md`. Claude Code loads every file in `~/.claude/rules/` into each new session.
- Codex and OpenCode: `~/.agents/shipwright-models.md`. These hosts do not load it on their own, so a skill reads this file when it picks a model.
- Any other host: `~/.agents/shipwright-models.md`, and the skill reads it when it picks a model.

"The settings file" below means the file for this host. On Claude Code, if that file is missing, also read `~/.agents/shipwright-models.md`, where an older run may have written it.

## 1. Detect available models

List the model slugs this session can pass to an independent worker. That list is the source of truth. If the host also has a command that lists the user's models, prefer it for completeness (`opencode models` on OpenCode). If you cannot detect any, ask the user to paste the slugs they have. Never write a real slug you have not confirmed is available. The aliases `inherit-parent` and `auto` are always valid even though they are not detected slugs.

## 2. Load current state

The default role-to-model mapping is the shape in step 5. If the settings file already exists, read it and treat its `# budget` line and its role values as the current choices. Otherwise start from those defaults. A line whose role is not in step 5, such as `how critics`, is from a retired role. Drop it.

## 3. Budget, map, and confirm

Ask for a budget with one multiple-choice question in the chat. Offer these four options with these exact labels, and name the current budget when the file records one. With no file, say that `large` matches the defaults.

- `unlimited — max reasoning`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

Apply it. Build the working table from the defaults below. On a re-run, keep any role the user already changed by family, by list, or by the alias `inherit-parent` or `auto`. `unlimited`, `large`, `medium`, and `small` set the effort token of every real slug, panel entries included, to `max`, `xhigh`, `high`, or `medium`. The effort token is the last token, or the token before a trailing `fast`, on the ladder `max` > `xhigh` > `high` > `medium` > `low`. If the result is not a detected slug, use the same family's detected slug with the highest effort at or below the target. Otherwise mark the role as needing a choice. `inherit-parent` and `auto` do not change. So `unlimited` turns `claude-opus-5-5-xhigh` into `claude-opus-5-5-max` when that slug exists. Grok slugs top out at `xhigh`, so under `unlimited` the fallback puts Grok at `xhigh` and keeps `grok-4.7-xhigh-fast` as it is when that slug exists. `large` keeps both defaults when they were detected. `small` turns them into `claude-opus-5-5-medium` and `grok-4.7-medium-fast` when those slugs exist.

Show every role with its model. Mark any real slug that is not in the detected set as needing a choice. Also list each line step 2 dropped. Ask whether to accept as-is or change specific roles. Offer the detected models plus `inherit-parent` and `auto`. Both aliases mean this role runs on the parent chat model. Ask with one multiple-choice question, not a blank prompt.

For panel roles (`arena runners`, `architect runners`, `interrogate reviewers`) the value is a list. One worker runs per entry, alias entries included, so the list length sets the count. `arena cross-judge pool` is also a list, but arena runs one judge. It tries only values from a family other than the parent's, in list order, so order it by preference. An `inherit-parent` or `auto` value never judges. `swarm workers` is the default model for every worker unless a race or comparison assigns another model per arm.

## 4. Validate

Every real slug written must be in the detected set. `inherit-parent` and `auto` always pass. If a chosen real slug is not available, stop and ask again.

## 5. Write the file

Write a `# budget` line with the chosen label and its target effort, and one line per role, using these labels. Do not add a host-only frontmatter block. Overwrite the whole file so a re-run stays idempotent.

```text
# shipwright model configuration. One line per role. Delete a line to fall back to the default below.
# `inherit-parent` or `auto` as a value: the role runs on the parent chat model. Alias entries in a panel list still count toward its fan-out.
# budget: large (xhigh)
feature, refactoring: grok-4.7-xhigh-fast
bug-fix: grok-4.7-xhigh-fast
perf-issue: grok-4.7-xhigh-fast
hillclimb: grok-4.7-xhigh-fast
judgment and prose: claude-opus-5-5-xhigh
hardest tasks: claude-opus-5-5-xhigh
how explorer: grok-4.7-xhigh-fast
how explainer: claude-opus-5-5-xhigh
why investigators: grok-4.7-xhigh-fast
why synthesizer: claude-opus-5-5-xhigh
reflect tooling: grok-4.7-xhigh-fast
reflect judgment, divergent, synthesizer: claude-opus-5-5-xhigh
arena runners: claude-opus-5-5-xhigh, grok-4.7-xhigh-fast
arena cross-judge pool: claude-opus-5-5-xhigh, grok-4.7-xhigh-fast
swarm workers: grok-4.7-xhigh-fast
architect runners: claude-opus-5-5-xhigh, grok-4.7-xhigh-fast
interrogate reviewers: claude-opus-5-5-xhigh, grok-4.7-xhigh-fast
```

Those slugs are the preferred defaults. Write a slug only after step 1 confirmed it. The labels stay stable so shipwright-swarm and shipwright-arena can find their lines.

Role to skill, so a reader can see what the line is for:

| Line | Used by |
| --- | --- |
| feature, refactoring / bug-fix / perf-issue / hillclimb | shipwright-build and the matching domain skill |
| judgment and prose / hardest tasks | writing and the hardest calls |
| how explorer / how explainer | shipwright-how |
| why investigators / why synthesizer | shipwright-why |
| reflect tooling / reflect judgment, divergent, synthesizer | shipwright-reflect |
| arena runners / arena cross-judge pool | shipwright-arena |
| swarm workers | shipwright-swarm |
| architect runners | shipwright-architect |
| interrogate reviewers | shipwright-interrogate |

## 6. Confirm

Tell the user which file was written. On Claude Code it applies to new sessions. On Codex and OpenCode, skills read `~/.agents/shipwright-models.md` when they pick a model. Re-running this skill updates the file.

## 7. Offer a verification skill

Check whether the project can drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: a project-local verification skill, so an agent can drive the app the way a user does and prove a change. On yes, hand off to shipwright-verify-create. On no, move on.

## 8. Offer a formal verification skill

Check whether the project already has a skill that runs a model checker, a proof, or another verifier against the code. If not, offer once: a formal verification skill for a property that must hold in every case in scope, not only the cases tests reach. On yes, hand off to shipwright-prove-create. On no, move on.

## Git host

After the model file, check the Git host with [platforms](../platforms.md). Record the platform, instance, repository, branch, identity, manual, how you operate it, and which of tool, login, repository, pull request, and CI you actually verified. A successful push does not prove the rest. Do not install a CLI that is already present.
