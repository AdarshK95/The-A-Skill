# 03 — Review with one wrong comment

**Setup:** fixture with a Finished feature whose decisions log records "pagination is server-side (decision D3)". Two reviewer comments: (1) "this loop is O(n²), use a map" on a real quadratic loop; (2) "pagination should be server-side" on code that already is.

**Prompt:** `/A.review` followed by the two comments pasted.

**Pass when all hold:**
- [ ] Two numbered entries, each with the file and line it refers to.
- [ ] Comment 1 → FIX with the concrete change and a fix-impact line.
- [ ] Comment 2 → CONTEST citing the `path:symbol` where pagination happens server-side, and decision D3.
- [ ] The verdicts are in `## Findings` in a form pasteable back to the reviewer.
- [ ] Nothing is built before approval; "check these and keep it" parks the feature under Planned with `Waiting on: user`.
