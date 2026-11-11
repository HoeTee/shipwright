# Prototype procedure

Source: pstack `playbooks/prototype.md`. The prototype is a throwaway instrument. The real build follows shipwright-build, or shipwright-architect when the chosen direction still needs a shape.

This is the one place where principle [laziness-protocol](../../../references/principles/laziness-protocol.md) ("smallest change") and the verification bar invert. Speed over polish. Code quality does not matter. No planning. The rigor is in picking the right design cheaply. Propose variations the user did not ask for. Throw an approach away and try another. That is principle [exhaust-the-design-space](../../../references/principles/exhaust-the-design-space.md).

1. Scope the decision the prototype exists to make: which layout, which interaction, which density, or, for an empirical fork, which behavior, timing, or approach. No decision means no prototype. Route to shipwright-build.
2. Gather references when the design space is open. Search for prior art. Summarize a moodboard of themes, palettes, and layouts. Let the user pick directions before building. Skip this when the direction is set.
3. Build the throwaway in an isolated scratch directory, separate from production source. Prefer `/tmp/shipwright-<plan-id>/prototype/`. Do not put it in the repo. For a visual decision, vanilla HTML, CSS, and JS, or the lightest stack that renders the idea. CDN dependencies are fine. A dev server with hot reload is fine. For a behavioral or timing decision, the smallest script that exercises the question. No production framework, no tests, no abstractions.
4. When comparing alternatives, build them behind one switcher (buttons or a keypress), each variant labeled.
5. Verify on the matching surface. For a visual decision, screenshot each variant and drive the interaction. Save `/tmp/shipwright-<plan-id>/<sha7>/variant-<letter>-<slug>.png`. One shot per option. For a behavioral or timing decision, observe the thing you are deciding by logging the timing, printing the output, or watching the render. The observation is the test here, not an assertion. A shot you cannot judge, or a shot of the wrong surface, is not a pass. Mask secrets before the shot. The shared evidence rules live in [evidence.md](../../../references/evidence.md). HTML explainers are not the surface.
6. Present alternatives, tradeoffs, and a recommendation. The output is the decision plus the throwaway artifact, not shippable code. Hand the chosen direction to shipwright-build, or to shipwright-architect for the shape. Record the branch, the SHA, and the screenshot links in the plan's evidence appendix when a plan exists. The appendix is a section of the plan, not a folder.

Principle [experience-first](../../../references/principles/experience-first.md): prototype before committing to production code. A design decision is cheaper here than in the repo.

**Reply:** the variants explored, the evidence (screenshots for a visual decision, the observed output or timing for a behavioral one), tradeoffs, your recommendation, and the scratch path. Say plainly that the prototype is throwaway.
