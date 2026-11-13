# 02 — Bugfix with a shared caller

**Setup:** fixture where helper `H` is called from modules `A` and `B`; `A` shows a wrong result because `H` mishandles an empty input.

**Prompt:** `/A.bugfix the list in A shows a wrong total when the filter matches nothing`

**Pass when all hold:**
- [ ] The trace runs from the symptom in `A` back to `H`, hop by hop, with the state at each hop.
- [ ] The root cause is one sentence, with one sentence on why not the nearer symptom.
- [ ] The caller inventory lists `B` as a caller of `H`, found by search.
- [ ] The tier is at least M, with "shared callers" named as a signal.
- [ ] The proposed fix is in `H`, not in `A`.
- [ ] *Impact* states what changes for `B` and whether the fix moves or removes the cause.
- [ ] The last step is a check that fails if the bug returns.
- [ ] No code changes before approval.
