# 02 — Root cause with a shared caller

**Setup:** fixture where helper `H` is called from modules `A` and `B`; `A` shows a wrong result because `H` mishandles an empty input.

**Prompt:** `/A.rootcause the list in A shows a wrong total when the filter matches nothing`

**Pass when all hold:**
- [ ] The trace runs from the symptom in `A` back to `H`, hop by hop, with the state at each hop.
- [ ] The root cause is one sentence, with one sentence on why not the nearer symptom.
- [ ] The caller inventory lists `B` as a caller of `H`, found by search.
- [ ] The tier is at least M, with "shared callers" named as a signal.
- [ ] The four boxes (symptom, expectation, the user's insights, what they want) are written before any code is read.
- [ ] The reverse lane stops at the origin in `H`, not at the first plausible line in `A`; the chain `H → A` is recorded.
- [ ] A prediction and test confirm it (e.g. `B` shows the same wrong total on empty input) → CONFIRMED.
- [ ] The report names no fix; it hands off to `/A.plan` at `H`.
- [ ] `/A.plan` then plans the change in `H`, with a check that fails if the cause returns, and states what changes for `B`.
