# HTML packet

The human-review packet is both a chat message and an HTML page. The page is a report. Do not screenshot it.

The renderer stays at `scripts/render_html.mjs` in the repository root. This skill does not move or copy it. The legacy skill still calls that path.

```sh
python skills/shipwright-signoff/scripts/render_signoff.py --draft-only --draft /tmp/packet.md --sha <sha>
node scripts/render_html.mjs render /tmp/packet.md -o plans/reports/<slug>.html --no-open
```

`render_signoff.py` finds the renderer three directories above its own `scripts/` folder. If Node.js is missing or the renderer fails, say what is missing and still deliver the chat packet.

Draft shape, sheet / blueprint / light, and the footer switch are in `references/html-explainer.md`. Page checks are in `references/progress-interaction.md`. Check the exit code, the HTML file, the candidate SHA, the findings, and the evidence links. Do not open a browser to accept the page.

Write the report to the plan's Report path and update that same file on the next pass. Embed key product screenshots in the page. Raw screenshots stay in `/tmp/shipwright-<plan>/<sha7>/`.
