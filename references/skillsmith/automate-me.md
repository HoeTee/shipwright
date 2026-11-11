# Automate me

A guided flow for turning the user's working conventions into a skill agents will follow. The output is one `-mode` skill tailored to them, for example `jay-mode` or `priya-mode`.

This flow uses three pieces: the mining pass in step 1, [authoring](authoring.md), and shipwright-write for the prose. It sequences them. It does not replace them.

## Flow

### 0. Check for an existing skill

Look recursively for `*-mode/SKILL.md` matching the user's handle.

Project folders:

- Claude Code: `.claude/skills/`
- Codex and OpenCode: `.agents/skills/`
- If the repo already keeps skills in one of these, use that one.

User folders:

- Claude Code: `~/.claude/skills/`
- Codex: `~/.codex/skills/`
- OpenCode: `~/.config/opencode/skills/`
- Shared: `~/.agents/skills/`

A mode skill can live in a personal category directory (`<skills>/<handle>/`), not only at the top level. If one exists, confirm intent with one multiple-choice question in the chat, unless they already said "update my skill" or similar:

- Update the existing skill (default for a repeat run)
- Start fresh (rare; ask why before doing it)

Update mode changes the rest of the flow:

- Step 1 mines only history since the skill was last edited (`git log -1 --format=%cI <path>`).
- Step 2 asks what changed or what is missing, not what to capture from zero.
- Step 4 edits the existing file in place. Preserve sections the user has not contradicted. Revise ones with new evidence. Add a section only for a genuinely new rule.

### 1. Mine their history

Locate this workspace's transcripts before fanning out. Use only that workspace's directory. Do not search every project's directory. That reads private chats from unrelated projects.

- Claude Code: `~/.claude/projects/<slug>/*.jsonl`, where `<slug>` is the workspace path with every character that is not a letter or digit turned into `-`.
- Codex: `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`. Keep only files whose first line has `payload.cwd` equal to the workspace path.
- OpenCode: this workspace's session directory. If the host does not isolate it, do not scan other projects. Mine the current conversation and say the history was limited.
- Another host: the session directory that host names for this workspace.

Survey recent conversations in that scope for recurring patterns. Run several parallel workers across slices of history (for example the last 2 to 4 weeks, split into 3 slices so each has enough material). Pick each worker's model from the shipwright model settings. Each slice reads transcripts from the path the parent provides, looks for the signals below, and returns a short structured list of patterns with evidence pointers.

Default signals:

- Response preferences (length, tone, format, "dumb it down" corrections)
- Delegation habits (workers, models, specialized workflows, parallelism)
- Verification posture (what "done" means, unit tests versus a live repro, reviewers)
- Code and prose discipline (style, principles cited, lint and format tools)
- Process conventions (worktrees, commits, pull requests, review and merge)
- Meta preferences (fixing skills mid-task, proposing new ones)

Cross-check across slices before elevating a signal. A pattern seen in 2 or more slices is high-confidence. A lone signal is weak and usually dropped.

### 2. Ask the user directly

Mining misses intent that has not come up yet. Ask with one or two multiple-choice questions in the chat, not a blank page. If you need a free-form catch, ask one after the choices.

Shape: one or two questions with 4 to 6 options each. Allow several selections for a category question. Start broad ("Which areas matter most?"), then follow up on the selected areas. After those rounds, one free-form question catches anything the options missed.

Do not dump 20 questions.

### 3. Cluster findings

Group the combined signals into sections. Use only what applies:

- **Response style**: length, tone, format.
- **Autonomy**: how much to do without asking.
- **Understand first**: which skills to reach for when scoping or investigating a change.
- **Workers**: default, parallelism, model-to-task, specialized workflows.
- **Prose and code discipline**: principles, lint tools, style guides.
- **Review and verify**: repro posture, verification skills, live checks.
- **Process**: git worktrees, commits, pull requests, review and merge.
- **Skills**: authoring habits, fix-the-skill-first, proposing new skills.

shipwright-flow shows the shape of a standing style. Read it for granularity. Do not copy its content. The user's rules are not the same as the plugin's.

### 4. Draft the skill

Author it with [authoring](authoring.md). Placement:

- Path: preserve an existing mode skill's category. For a new mode, use `<skills>/<handle>/<handle>-mode/SKILL.md` when the repo has an established personal category for that handle. Otherwise default to `<skills>/<handle>-mode/SKILL.md` in the project, or the user-level skill folder if the user prefers a personal skill. `<skills>` is the folder from step 0.
- Handle: the user's first name or chosen identifier.
- Frontmatter `description`: trigger on their name, `/<handle>-mode`, and "work in their style". Do not trigger on generic keywords like "write code" or "review PR".
- Keep `description` as one YAML scalar. Quote it, or use `description: >-` with indented continuation lines, when punctuation or wrapping requires it.
- `disable-model-invocation: true` by default. Opt out only if the user explicitly wants the mode on every turn.

### 5. Iterate on the prose

Apply shipwright-write to every line.

Show the draft and take feedback. Expect several iterations. Cut hard. A mode skill is not a manual.

### 6. Land it

Work in a worktree off the default branch. Commit and open a pull request through shipwright-ship when that is authorized. Do not push to the default branch directly.

To prove a change in the mode skill changes behavior, hand the before and after to shipwright-eval. A vibe check with the user is the subjective bar below. It is not a substitute when the user asked for proof.

## Guardrails

- Do not overfit to one conversation. A preference stated once and contradicted later is noise. Require several instances before writing it down.
- Do not be clever. Restating other skills, inventing metaphors, or writing poetic prose for an agent reader costs and does not help. Keep it operational.
- Reference, do not inline. Other skills the user relies on appear as paths, not pasted excerpts. Same for principle files.
- Keep sections minimal. Add a section only when the user has a specific, non-default rule there. "Communicate clearly" is not a section. "Short paragraphs. Tables when comparing options. Bullets only when items are genuinely parallel." is.
- Name the person "the user" or "the human" in imperatives, not the author's first name.
- Do not force symmetry. If the user has no process rules worth writing, skip the Process section.

## Evaluation

A `-mode` skill is subjective. A benchmark loop is not useful here. Vibe-check with the user: does it read like them, and did it miss anything? Then ship.

Run a description-tuning loop only if the trigger turns out to fire on the wrong requests.

When the user wants proof that the skill changes results, that run is shipwright-eval, not this vibe check.

## When not to use

- The user wants a task-specific skill, not working conventions. Use [authoring](authoring.md) alone. No mining.
- The user wants one narrow workflow, such as "how I write commit messages". That is a regular skill, not a mode skill.
