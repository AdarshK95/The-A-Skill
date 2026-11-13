# 06 — Plain-English report and conclusive answer

**Setup:** any fixture; run scenario 01's prompt through to the report.

**Pass when all hold:**
- [ ] The chat report opens with what this means for the user, not with files or findings.
- [ ] No path or symbol appears in chat that the user did not ask for; the chat says which file holds the detail.
- [ ] Options come with trade-offs and one line on which way the agent leans and why.
- [ ] The chat ends with the next step and what the user has to do.
- [ ] A five-line progress update appeared at each stage move before the report.
- [ ] The activity file's Summary has the five plain-language points filled; the event log has one timed `E<n>` line per step with the ask quoted as E1.
- [ ] Ask "why did you choose that?" after a correction: the agent appends an event-log line that corrects the earlier one by reference and leaves the earlier line unchanged.
