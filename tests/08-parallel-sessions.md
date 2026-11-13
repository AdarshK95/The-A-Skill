# 08 — Two sessions, one file

**Setup:** two chats on the same project. Session A is implementing feature 7 and has a claim on `lib/range.ts:normalizeRange`. Session B starts feature 8 which needs to change `lib/range.ts:parseRange` and later needs A's finished `normalizeRange`.

**Pass when all hold:**
- [ ] B, in a fresh chat, reports the shared folder first: A's claim, in plain words.
- [ ] B claims `parseRange` only and does not touch `normalizeRange`, even though a half-written line inside it looks malformed.
- [ ] B writes a `waiting on` handoff for `normalizeRange` and continues with its other steps.
- [ ] When A finishes and writes `done`, B's next step pick-up removes both rows and B continues.
- [ ] A's claim is released when its step's check passes; neither session leaves rows behind at close; `/A.close` refuses while a row remains.
- [ ] `/A.status` in a third chat lists the live claim and wait before the board.
