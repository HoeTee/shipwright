# Teach procedure

Source: pstack `teach`, with the host tooling map removed. shipwright-how and shipwright-why do the digging. This skill blends them into one plain account. It changes nothing.

## What to teach

1. Decide the few things the person should walk away understanding. Choose them from why they are asking (about to change it, reviewing it, debugging it, or new to it) and from what they already know. Read both from the conversation. Do not quiz them. Skip what they plainly already know. Put the depth where their question is.
2. Let shipwright-how and shipwright-why do the work. Read the code only to get oriented, then run those skills. Run them in parallel and combine the results. Match the size to the question. A subsystem needs both. A small change may need one. Keep why narrow by default. Its full sweep is slow. Put the narrowing in the ask itself (a scoped question, git plus a source or two) so why records the skipped categories. Widen it only when the reasons are the point.
3. Start with a plain definition. Name the thing and say what it is in general terms, the way a senior engineer would say it out loud, with its common name if it has one. Then tie it to the case in front of you ("in X, we use this to ...") and build from there: how it works, the deeper reasons, the edge cases. For each part, explain the problem it solves and how it actually works. Walk through what happens as the person does the thing when that is what makes it land. Listing functions and constants is reference, not teaching. Do not print framing labels ("the one idea to hold onto", "the thing to walk away with", "the key insight", "at its core", "TL;DR"). Give the smallest complete answer first, a sentence or two, not a dense paragraph, then stop. Add layers when they ask. Never a wall of text.
4. Keep it a conversation, not a lecture. Offer to go deeper or move on, and follow their lead. No quizzes. Do not print "Pause", do not ask them to say it back, do not announce "the sentence to nail", and do not flag a part as important or hard. When you would pause, stop and let them respond. Running one-shot with no live human, deliver it cleanly and put any offer to go deeper at the end.
5. Show, do not only tell, and build the picture up diagram by diagram. Open the diff, the code, or the debugger when that is the fastest way to land it. Draw when a picture lands faster than words. For anything with three or more moving parts, do not draw one diagram with all of them at once. Draw a short series. Each diagram redraws the last and adds a single part, so the reader watches the system assemble. A single all-at-once diagram, especially one saved for the end, is a reference, not teaching. To teach a flow from A to B to C, draw it three times. First A to B. Then redraw and add C. Then redraw and add the return edge or the next piece. A mermaid diagram fits a flow or structure where the labels carry the meaning. When the idea is spatial (layout, overlap, scroll position, or a before and after), use the host's image tool if it has one, marker-on-whiteboard style with a few short labels, because image models garble long text. If the host has no image tool, use a short series of mermaid or ASCII drawings. Do not settle for describing a spatial idea only in words. The build-up rule holds for generated images too. A single simple point needs no figure.

## Wording

Write the reply the way shipwright-write's wording pass requires: plain spoken language, the way you would explain it to a colleague. Be tight, not terse. Cut filler. Keep why's hedges. Those hedges are findings, not style. State the concrete mechanism, not a metaphor, a framing, or a preview of what is coming. Normal sentence case. No em dashes. Prefer periods over commas. Keep each sentence to one or two commas. If clauses pile up, split them. Give each concept one name and keep it. Avoid mirror sentences ("A without B, or B without A") and tidy closers ("the rest follows", "it all falls out"). The words in these steps are directions, not labels to print.

Target density: "Virtualization runs in two parts, one for rendering and one for loading from disk. When an item scrolls out past the buffer, both its DOM node and its in-memory data are evicted."

## Reply

The explanation itself, never a report about what you did. Lead with the main point, then the plain account of what it is, how it works, and why, and the threads worth chasing with shipwright-how or shipwright-why.

## Docs and DX

A spoken explanation is this skill. Durable docs, a PR description, or a commit message go to shipwright-write. Audit's DX notes live in shipwright-audit's `references/dx.md`. Do not turn the explanation into a docs plan unless the user asks.
