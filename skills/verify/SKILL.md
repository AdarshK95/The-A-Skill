---
name: verify
description: Run the project's checks, tick the requirements with evidence, diff the build against the approved steps. Nothing is called done without a passing check.
disable-model-invocation: true
---

# /A.verify — prove the build

**Place in the flow:** verify stage; needs something built and, at tiers L and XL, a build review on it (`/A.build.review` — offered first when missing); produces verification evidence; next: Close. See `../core/references/flow.md`.

Runs the spine's **Validate** stage (`../core/SKILL.md`) on the current feature, subject resolved chat-first. Evidence before claims: the checks that cover the change (or the smallest check left behind that fails if the logic breaks), each enumerated failure case exercised, every `## Requirements` line ticked with what satisfied it, the build diffed against the approved steps. **A step that calls a model or a service is verified by what it sends and what it accepts.** At least one test asserts the request content (the question is in the prompt, the fields are in the payload) and one runs a recorded real reply through the parser; a fake that returns a well-formed answer proves only that the code can consume a well-formed answer. And every expected output has a test for its absence: empty, malformed or missing comes back as the named failure state, never as the default conclusion (`build-check.md › Absence is a failure`).

**Verified means verified where users are.** A change to behaviour users see (prompts, routing, answers, UI) is verified through the **deployed** environment's real entry point — the dev app's `/chat`, the real UI — after the change is deployed there, not by a local run against the environment's resources. A local run proves the code on disk; it says nothing about what users get. The report states which: "verified on the deployed dev app (build <id>)" or "verified locally against dev resources — not yet deployed". Results under `## Verification` with commands and output. Then: ready to `/A.close`, or the gaps, in decision shape.
