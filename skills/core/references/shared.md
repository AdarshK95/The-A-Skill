# Shared folder — how parallel sessions coordinate without colliding

Several sessions (same agent or different agents) may work on the same project at once. They never read each other's conversations; they talk through one small folder, `shared_folder` in config (default `.a/shared/`). Its single rule: **it holds only what is live.** Finished things move to their proper home (the activity file, the board, the decisions log) and leave the folder. An empty shared folder means nothing is in flight. A non-empty one at the start of a session means something is in flight and must be read before anything else.

## Session identity

At Start, every session writes a `Session:` tag into its feature header and uses it in every shared entry: `<host>-<feature number>-<date time>`, for example `claude-7-13 Nov 26 04:15 PM`. There is no other way to tell sessions apart.

## Three files

| File | Holds | Entry lifetime |
| --- | --- | --- |
| `claims.md` | Who is editing what, right now | From just before the first edit to the moment the edits are verified or abandoned |
| `handoffs.md` | What one session is waiting for from another, and notices that it is done | From the wait or the completion until the receiving session has acted on it |
| `notes.md` | Short warnings between sessions: "don't touch X", "file Y is mid-rewrite, lines 40–90 look broken, leave them", "I changed the shape of Z, re-read it" | Until the addressed session acknowledges, or the writer withdraws it |

Each entry is one table row, written by one session, with the session tag and a time. A session edits only its own rows, except to remove a row addressed to it that it has acted on.

## Claims — before any edit

1. **Re-read `claims.md`** immediately before editing a file.
2. Another session claims the same file → read its row. If its claim covers the symbols or lines you need, **do not edit them**: write a `handoffs.md` row (`waiting on <session> for <file>:<symbols>`), tell the user in one line, and work on another step until the claim is released. If the claim covers other parts of the file, you may edit your part: write your own claim naming the exact symbols or line ranges, and never reformat, reorder or "fix" anything inside the other session's range — a region under construction may look malformed and is not yours to repair.
3. No conflicting claim → write your row: `| <session> | <file> | <symbols or line ranges> | <feature.item step> | <since> | <expected release> |`. Claim narrowly: the symbols you will touch, not the whole file, unless you truly need the whole file.
4. **Release** the row as soon as the edits to that file are verified (the step's check passed) or abandoned. A claim that lives past its step is a bug.

A claim whose `since` is older than `claim_stale_hours` (config, default 4) and whose session has no newer board or header update is **stale**: the other session may take it over after writing a `notes.md` row saying so, and the user is told.

## Handoffs — dependencies between sessions

- **Waiting:** session B needs something session A is building. B writes `| <B> | waiting on | <A> | <feature.item or file:symbol> | <what B needs, in one line> | <time> |`, sets its own header `Status: waiting on <A>`, tells the user, and continues with unblocked steps or stops.
- **Done:** when A finishes the thing, A writes `| <A> | done | <B> | <the same reference> | <where the result is: file, symbol, commit> | <time> |`. A also updates its own board row and header as usual — the handoff row is a signal, not the record.
- **Pick-up:** B re-reads `handoffs.md` at every stage move and before every step. On seeing A's `done`, B removes **both** rows (its own wait and A's done), logs the pick-up in its event log, and continues. If B's session was cut off, the next session that resumes B's feature finds the rows and does the same.

The folder is emptied by the receiver acting, never by the sender assuming.

## Notes — warnings and requests

Short, addressed, dated: `| <from> | <to or all> | <note> | <time> |`. Typical: "don't touch `lib/range.ts` until I release it", "I changed `Order.total` from number to string — re-read before you use it", "lines 40–90 of `api/index.ts` are mid-rewrite". The addressed session removes the row once it has read and acted on it; `all` notes are removed by the writer when no longer true.

## When sessions touch the same file anyway

- Prefer **partition by symbol**: each session claims different functions, and neither reformats the file.
- If both need the same symbol, the second to arrive waits (handoff) — it does not merge by hand.
- Never resolve a conflict by deleting or rewriting a region another session claims, even when it looks wrong. Note it; let its owner fix it.
- After any edit to a shared file, re-read your own symbol before the next edit; the other session may have saved.

## Reading the folder

Every session reads all three files at Start, at every stage move, and before every step of Implement; that is cheap because the folder is small. At Start in a fresh conversation, a non-empty folder is reported to the user in plain words before anything else: who is working on what, who is waiting on whom, what is in flight — and whether any of it is this session's to resume.

## What never goes here

Plans, reports, decisions, findings, results, logs. Those have homes; the shared folder points at them when needed and is otherwise empty. `/A.status` shows the live entries; `/A.close` refuses to close a feature that still has rows here.
