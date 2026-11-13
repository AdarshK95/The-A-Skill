---
name: resume
description: Continue a feature from the exact place work stopped. Reads the board and the feature's pointer; never guesses.
disable-model-invocation: true
---

# /A.resume — pick up where we left off

**Place in the flow:** needs a feature with a pointer; produces continuation at that pointer; next: whatever stage the pointer is in. See `../core/references/flow.md`.

**Input:** optional — a feature number, title or file. With none, this is also what "where did we leave off, let's continue" means.

1. **Read the shared folder** first: a handoff addressed to this feature, or a claim left by a cut-off session, changes where to resume; report it. Then **read the board** (`project_board`). Reminders, one line, if due.
   - A target was given → that feature.
   - One feature in progress → that one.
   - Several → list each in one line: `7 · CSV export › 7.2 › 3/5 — next: wire route in api/index.ts`. Ask which. "Where did we leave off" with no pick is answered by this list.
   - None in progress → say so; list Planned features; offer to start one.
2. **Open the feature file.** Read the header (`Phase`, `Pointer`, `Last done`, `Next`) and `## Context`. Nothing else yet.
3. **Open the item** the pointer names: its mini header, its step list, its lines in `## Changes`, build findings marked awaiting, the last five `## Log` lines.
4. **Verify the pointer against reality.** The files `Last done` names must contain the change it describes: read them; use `git status` / `git diff` where available. The previous session may have died mid-write. Any mismatch is reported before anything else happens, with what you found.
5. **Announce**, one short block:
   ```
   Resuming 7 · CSV export › 7.2 null range on empty filter (bugfix) › step 3/5
   Last done: step 2 — guard added in lib/range.ts:normalizeRange (13 Nov 26, 05:31 PM)
   Next: add route handler in api/index.ts calling exportCsv; then run npm test
   Awaiting you: 1 build finding (7.2-BF1)
   ```
6. **Continue from `Next`, in the item's current stage**, under the spine (`../core/SKILL.md`). `Phase: Gate` means wait for approval, not build. `Implement` means step k continues. `Verified` means offer `/A.close`.
7. **Update** `Updated`, the header and the board block at the first change.

Never pick a different item than the pointer names. Never start a step the pointer does not name. If `Next` is vague ("continue implementing"), say so, derive the concrete next action from the step list and `## Changes`, write it into `Next`, then proceed.
