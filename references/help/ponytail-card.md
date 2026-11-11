
# Ponytail card

The levels below are shipwright-lean. The card is read-only: change no mode and persist nothing. Show it in the user's language.

| Ponytail name | Shipwright |
| --- | --- |
| ponytail lite / full / ultra | shipwright-lean, same three levels. Full is the default. The level sticks until the user changes it. |
| ponytail | shipwright-lean |
| ponytail-review | shipwright-review |
| ponytail-audit | shipwright-audit |
| ponytail-debt | shipwright-debt |
| ponytail-help | shipwright-help |
| stop ponytail / normal mode | the user says stop lean |

Source text, with the host menu line rewritten:

# Ponytail Help

Source: [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) (MIT).

Show this reference card, in the user's language. One-shot: change no mode and persist nothing.

## Levels

| Level | Say | What changes |
|-------|-----|--------------|
| **Lite** | `ponytail lite` | Build what was asked, name the smaller option in one line. |
| **Full** | `ponytail` | The smallest complete change, a check where the logic needs one, and a reply that names what was skipped and any risk. Default. |
| **Ultra** | `ponytail ultra` | Also questions the request and pushes back before building. |

The level sticks for the conversation until changed.

## Skills

| Skill | What it does |
|-------|--------------|
| **ponytail** | Lazy mode itself: least new code, clear replies that name skipped work and risks. |
| **ponytail-review** | Quality review of a diff or PR: bugs, security, load, missing tests, speed, what to cut. Each finding says what goes wrong and how to fix it. |
| **ponytail-audit** | The same quality review for the whole repo, ranked. |
| **ponytail-debt** | Harvest `shortcut:` comments into a debt ledger. |
| **ponytail-help** | This card. |

On Claude Code, Codex, and OpenCode, name the shipwright skill in the prompt. Do not depend on a host-only slash menu.

## Deactivate

Say "stop ponytail" or "normal mode". Resume anytime with `ponytail`.

Full docs: https://github.com/DietrichGebert/ponytail
