# Blast radius procedure

Source: pstack `blast-radius`, with the host tooling map removed. The review-shaped companion is [method.md](method.md). Dispatch is `skills/shipwright-how/references/hosts.md`.

Find what a change breaks somewhere else, before it ships. Use for "blast radius of X", "what could this break", or a small diff you do not trust yet.

shipwright-how tells you what the code does. shipwright-why tells you why it is shaped that way. This skill tells you what it breaks somewhere else.

Listing the callers is not the job. Those can be searched in a second. The job is the breakage a search will not show.

## Do not trust your own writeup

A blast-radius writeup that sounds right is worthless. It reads as convincing whether or not it is true. Do not hand back the writeup alone. Find the one or two facts the whole thing depends on and prove them by running code.

### How sure are you

For each fact the change's safety depends on, get it as far down this list as is cheap, and say where it stopped.

1. You said so. Worthless on its own.
2. You pointed at the line. A real `file:line`, or the library's own source.
3. You showed the bad case cannot happen. You walked the failure step by step and it does not reach.
4. You ran it. A script or test that calls the real code and fails loud if you are wrong.
5. You reproduced it in the running app.

Step 4 is usually one small script that imports the same library the app ships and calls the exact function you are worried about. The script is written for this change. It is not a checker that ships inside the plugin. Save its output under `/tmp/shipwright-<plan-id>/<sha7>/` as a `.txt` or `.json`. A new head needs a new run.

## Steps

1. Read the change. The diff, the symbols it adds, changes, and deletes, and what it now does differently, including the part the diff does not spell out. Use shipwright-why's source step to pull the PR and the commits when the motive matters.
2. Find the one fact it is safe because of. Most changes that look risky are safe because of a single fact, like "this call only drops already-dead cache entries and does nothing else". Find that fact. If it holds, most risky cases are cleared at once. Spend the time here, not on a long list of maybes.
3. Look where search stops. Read the source of the library you call, and check its pinned version and any local patch. Work out when things run: microtasks, unmount and teardown, and which UI runtime. Follow what a symbol search misses: the JSON an API returns, a database column, a wire format, another language reading the same bytes, a feature flag, code three hops downstream.
4. Be honest about each risk. Give it a real chance of happening and a real cost if it does. Keep the risks you confirmed. List the ones you checked and cleared separately. Same rules as shipwright-why. Cite a real `file:line`. A search that finds nothing is still an answer. Never make up a caller or an API.
5. Prove the one fact. Write a script or test that runs the real code, run it, and paste what happened.
6. For a big or wide change, run it as shipwright-arena. Ask more than one model the same question and merge the answers. Different models catch different real bugs. Do not copy arena's procedure into this file.

## What to hand back

- **What it does.** What changed, including the part that is not obvious.
- **The one fact it is safe because of.** State it, say which step you got it to, and show the proof. If you could not prove it, write unproven.
- **Risks.** Each names how it breaks, the `file:line`, how likely and how bad, and how to check. Paste the proof for the ones that matter.
- **Cleared.** What you checked and why it is fine.
- **Before you merge.** The cheapest test or repro that catches the real bug, including the script you wrote.

Run the wording pass in shipwright-write. Cite real code. Strip anything private before it goes anywhere public.

## Review use

[method.md](method.md) is the same job inside a review: shared interfaces, persisted data, config, state, concurrency, and delivered artifacts. Follow producers and consumers out to behavior a user can observe. Also check serialization, the database, when config takes effect, old versions reading new data, errors, and cleanup. A premise you did not run is not "reproduced". A new product direction found during the check does not become a repair on its own. Hand it back.

## Domain

Correctness of the callers is shipwright-bugs. Whether a migration's consumers were actually updated is the dependency pass in shipwright-audit's `references/deps.md`, then this skill. Do not paste those checklists here.

**Reply:** the writeup above, with the one safety fact either proven or marked unproven.
