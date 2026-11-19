---
name: close
description: Finish the current feature: finalize its file, update the project ledgers, move it to Finished. The project stays open.
disable-model-invocation: true
---

# /A.close — finish this topic

**Place in the flow:** needs a verified feature; produces updated ledgers and a Finished row; next: nothing, or the next feature. See `../core/references/flow.md`.

Runs only on the user's word.

1. The feature must be at `Phase: Verified`. Otherwise say which stage it is at and what remains; offer to run Validate first.
2. No row in the shared folder belongs to this feature; release claims, resolve handoffs, withdraw notes first.
3. Every item has `Result:` filled. Every build finding is decided (fixed, moved to a new item or feature, deferred with a row, or left with a reason). Open ones are listed to the user and the close waits.
3a. Append this feature's history line to each element in `### Elements touched`; merge this feature's flow fragments into their flows where the order is unambiguous (leave the rest as fragments for the map); register proposed new elements; set each touched element's state (`stable` unless another open feature touches it); redraw the board's `## Overview` from the registry (`../project-map/SKILL.md › States`); then one line: "Overview updated. Regenerate `docs/map/map.html` too?" — run `.a/scripts/map_build.py` on yes.
3b. Empty `tmp_folder` (`.a/tmp/`) and remove any scratch this feature left under the OS temp folder; list what was removed in the event log.
4. Run `close_updates` from config in order (`../core/references/logging.md` → `/A.close`): implementation log entry; API docs if a contract changed; period ledger if set. Propose constitution wording if a standing rule surfaced; write nothing there yourself. Ask the lesson ladder's question once (`../core/references/logging.md › Drift and lessons`): did this work correct a wrong belief about how the system behaves? If so, the first rung that holds — a check, a standing rule, or a lesson with its retire condition; if not, nothing is written.
5. Header: `Phase: Closed`, `Updated` now. Board: replace the feature block with one row under **Finished** with a one-line result. Overview: the feature's nodes turn green.
6. Say in one line what was updated and that the feature can be continued later with `/A.plan.realign <file>`.

Closing ends this feature, not the project.
