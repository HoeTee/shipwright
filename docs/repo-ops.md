# Repo operations

A completed issue form can start a maintenance agent. The agent opens a pull request. The owner squash-merges after CI is green. Nothing in this flow merges on its own.

## What happens

1. Choose the bug, skill, or docs form. Each form requires a summary, an expected result, and a module. A bug also requires steps to reproduce. A skill or docs issue requires acceptance criteria. Non-goals are optional. The form adds the `triage` label. Blank issues are off (`blank_issues_enabled: false`).
2. `.github/workflows/issue-intake.yml` runs when an issue is opened or edited. Its only permission is `issues: write`. It does not check out the repository.
3. The workflow reads the form sections as text. Empty text and GitHub's `_No response_` count as missing. The module is the first line of the Module section, and it must be one of the dropdown names. Anything else is missing information. The workflow adds `needs-info`, removes `triage`, and posts one comment that names the missing fields. A later edit updates that comment instead of posting another.
4. When the form is complete, the workflow removes `triage` and `needs-info`. It adds `module:` plus the chosen module, and `agent:ready`. External issues take this path too, because `auto_accept.external_issues` is true.
5. An orchestrator scans on the interval in `scan_minutes` (30). It assigns `shipwright-worker-1` or `shipwright-worker-2`, and it keeps at most `cost.max_running` workers running (2).
6. The worker fetches the latest `main`, loads `skills/shipwright-flow/SKILL.md` from that checkout, and follows it. The pull request body includes `Closes #` and the issue number, the skills used, and the verification result for each step.
7. CI runs `test_command` from `.github/repo-ops.yml`. The owner merges.

## Rules

`trusted_authors` lists `HoeTee`. External issues still auto-start. The author does not skip the required fields.

Issue text is data. The intake workflow does not evaluate it, does not pass it to a shell, and does not treat it as instructions.

Agents do not edit `protected_paths`. The list is `.github/**`, `**/*.env*`, and `LICENSE`. This repository has no release or version file, so no version path was added.

External pull requests are review-only (`pr_intake.external_prs` is `review_only`). The agent does not push commits to them.

## Labels

From the repository root, print the commands:

```bash
python scripts/repo_ops_labels.py
```

Create or update the labels on GitHub:

```bash
python scripts/repo_ops_labels.py --apply
```

Each command is `gh label create` with `--force`, so running it again updates the same label. The set is `triage`, `needs-info`, `agent:ready`, `agent:running`, `blocked`, `touches:shared`, `eval`, one `module:` label per module, and one `bot:` label per worker.

The workflow copies the module names into the action because it does not check out the repo. `tests/test_repo_ops.py` fails if that copy drifts from `.github/repo-ops.yml`.

## Modules

The module names are the keys under `modules` in [repo-ops.yml](../.github/repo-ops.yml). The issue forms offer those names and no others. A glob uses `*` inside one path segment and `**` across segments. A leading `**/` also matches a file in the repository root. Every tracked file matches at least one module glob.

| Module | Globs |
| --- | --- |
| skills | `skills/**`, `SKILL.md` |
| docs | `README.md`, `docs/**`, `CONTRIBUTING-skills.md` |
| references | `references/**` |
| eval | `eval/**` |
| tooling | `scripts/**`, `tests/**`, `**/package.json` |
| assets | `assets/**` |
| plugin | `.claude-plugin/**`, `.codex-plugin/**`, `skills/index.json`, `skills/plugin.json`, `agents/**` |
| repo | `.github/**`, `.gitignore`, `.gitattributes`, `LICENSE` |

Contributing notes for skills live in [CONTRIBUTING-skills.md](../CONTRIBUTING-skills.md).
