---
name: verify
description: Run the project's checks, tick the requirements with evidence, diff the build against the approved steps. Nothing is called done without a passing check.
disable-model-invocation: true
---

# /A.verify — prove the build

**Place in the flow:** verify stage; needs something built; produces verification evidence; next: Close. See `../core/references/flow.md`.

Runs the spine's **Validate** stage (`../core/SKILL.md`) on the current feature, subject resolved chat-first. Evidence before claims: the checks that cover the change (or the smallest check left behind that fails if the logic breaks), each enumerated failure case exercised, every `## Requirements` line ticked with what satisfied it, the build diffed against the approved steps. Results under `## Verification` with commands and output. Then: ready to `/A.close`, or the gaps, in decision shape.
