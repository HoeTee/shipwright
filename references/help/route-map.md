# Route map

Help does not start the work. Answer, then hand back a prompt the user can send. If the user already asked you to do the work, say once that shipwright-flow is the entry, and stop.

Do not invent a chat channel, a repository id, or a model slug. Do not start a hosted worker or a browser session on a help-only turn.

## Find the need

Infer from the message. If it is unclear, ask one multiple-choice question: Get set up / Start a task / Pick a skill / Models and autonomy / Writing and review / Something else.

## Shipwright routes

- Setup and models → shipwright-setup. Project rule files → shipwright-rules.
- Start the work → shipwright-flow.
- How a piece runs → shipwright-how. Why it is shaped this way → shipwright-why. Teach me → shipwright-teach.
- Design before code → shipwright-architect. Several candidates → shipwright-arena. Adversarial review → shipwright-interrogate.
- Fan-out → shipwright-swarm. Catch me up on this chat → shipwright-recap. An earlier session → shipwright-recall.
- A real-app verification skill → shipwright-verify-create or shipwright-verify-maintain. A formal proof → shipwright-prove-create or shipwright-prove-maintain.
- Prose → shipwright-write. Comments in code → shipwright-comments.
- A personal mode skill → shipwright-skillsmith, [automate me](../skillsmith/automate-me.md).
- Decision trail → shipwright-trail. Reflect → shipwright-reflect.
- Prompt shape → [prompting](prompting.md), [recipes](recipes.md), [sharpen](sharpen.md).
- Levels → [ponytail card](ponytail-card.md), applied by shipwright-lean.

## Reply shape

1. Direct answer in plain words.
2. A copy-paste prompt the user can send next, unless they already asked you to run it.
3. The skill or reference the answer came from.

## Source route text

The poteto-help route follows. Read it as the original map. Prefer the shipwright names in the table above when you answer.

# Poteto Help

Answer questions about pstack / poteto-mode: how to set up, which skill or playbook to use, and what prompt to send. For pure help questions, **do not start the work**—hand back a ready-to-send prompt. If the user asks to *do* work with pstack, follow **poteto-mode** instead and mention once that a Custom Mode can keep it on.

Details live in sibling skills and `references/`. Read the file you route to before quoting it. Prefer installed local paths over remote plugin URLs; if you cite upstream, use the public GitHub copy only when it matches what is installed.

## Find the need

Infer from the message. If unclear, ask one multiple-choice: Get set up / Start a task with poteto-mode / Pick a skill or playbook / Models & autonomy / Writing & review / Something else.

## Route map (read then answer)

- **Setup / models** → **setup-pstack**; point at harness settings files it writes.
- **Style / principles / playbooks** → **poteto-mode** + the named `playbooks/*.md`.
- **How does X work** → **how**. **Why shaped this way** → **why**. **Teach me** → **teach**.
- **Design before code** → **architect** / **arena**. **Adversarial review** → **interrogate**.
- **Fan-out** → **swarm**. **Catch me up** → **ketchup** / **ketchup-video**.
- **Verification skills** → create/maintain verification or formal-verification skills.
- **Prose** → **unslop**, **technical-writing**, **no-comments**.
- **Personal mode skill** → **automate-me**, now shipwright-skillsmith. Follow the host-neutral authoring notes. Do not call a host-only update command.
- **Decision trails** → **show-me-your-work**. **Reflect learnings** → **reflect**.
- Prompt recipes and phrasing: `references/prompting.md`, `references/recipes.md`.

## Reply shape

1. Direct answer in plain words.
2. A copy-paste prompt the user can send next (unless they already asked you to run it).
3. The skill/playbook file the answer came from.

Do not invent chat-channel or repository IDs. Do not start a hosted worker or a browser session for a help-only turn.
