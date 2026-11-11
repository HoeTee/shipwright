# Authoring or modifying a skill

You own the skill's voice.

1. Follow the Agent Skills format: YAML frontmatter with `name` and `description`, then the body. https://agentskills.io . On Claude Code, use that host's skill-authoring guidance when it is present. Do not call a host-only update command, and do not depend on one vendor's creator tool.
2. Validate the skill. Frontmatter has `name` and `description`. Referenced files exist. Cross-skill links resolve.
3. Add test cases when the change is structural. Skip them when the change is subjective.
4. A behavior change that must be shown to work is handed to shipwright-eval. Do not claim the skill is better without that run. Authoring itself does not run the eval.
5. Open the pull request through shipwright-ship when the user has authorized that.

When in doubt, delete. Keep only prose that changes a decision. Tell it to do the thing and skip the reason. Explain only when the rule is confusing without one. Match tone to scope. Point at structural sources (types, READMEs, config) per [encode lessons in structure](../principles/encode-lessons-in-structure.md). Delegate to other skills by path. Do not restate them. A workflow you keep hitting that is not captured yet becomes a proposal for a new skill, not a silent edit of an unrelated one.

A skill that breaks in the middle of a task is fixed in its own pull request. Do not silently work around it inside the task.

Reply with a summary of the skill, the key design decisions, and the validation notes.

Shipwright constraints that sit on top of the source playbook:

- The body is Chinese, about 120 lines. The bulk lives in `references/`.
- Directory names, file names, path placeholders, and structural headings are English.
- Instructions name Codex, Claude Code, and OpenCode by what they share. They do not name a host tool.
- A new file under `skills/<name>/` has to be reflected in `skills/index.json` by `python scripts/build_opencode_index.py`. Do not hand-edit the catalog.
