---
name: build-review
description: Review what was built, after the build. Fresh reviewers check the code against the user's own words to find shallow work, loopholes, wrong fixes and decisions taken without the user. Output is a verdict with evidence, never a fix.
disable-model-invocation: true
---

# /A.build.review — is it really built, and is it what was asked

**Place in the flow:** after the build, before verify; needs something built; produces a verdict (Sound · Sound once fixed · Shallow · Off target) with evidence; next: Verify, or the fixes as a new item at Gate. See `../core/references/flow.md`.

Runs the spine (`../core/SKILL.md`) with `../core/references/build-review.md` as its method — read it whole, it is the skill. Subject resolved chat-first (Start step 0): the feature built in this conversation, else a diff or code the user pointed at, else board features at Implement or Realign, offered by name. A word in the request sets the depth ("at L", "xl"); otherwise the tier is recomputed from what the build touched, never below M.

This file is this command's **Evaluate** step, and nothing more: run `build-review.md` §1–§7 in order, then its *Gate*, *Resolution and rounds* and *Without a plan* sections. `/A.review` reviews a plan; this reviews the build, and they are not interchangeable.
