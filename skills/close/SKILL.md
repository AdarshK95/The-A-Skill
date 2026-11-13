---
name: close
description: Finish the current feature: finalize its file, update the project ledgers, move it to Finished. The project stays open.
disable-model-invocation: true
---

# /A.close — finish this topic

Aliases: `/A.done`, `/A.finish`. Runs only on the user's word.

1. The feature must be at `Phase: Verified`. Otherwise say which stage it is at and what remains; offer to run Validate first.
2. No row in the shared folder belongs to this feature; release claims, resolve handoffs, withdraw notes first.
3. Every item has `Result:` filled. Every build finding is decided (fixed, moved to a new item or feature, deferred with a row, or left with a reason). Open ones are listed to the user and the close waits.
4. Run `close_updates` from config in order (`../core/references/logging.md` → `/A.close`): implementation log entry; API docs if a contract changed; period ledger if set. Propose constitution wording if a standing rule surfaced; write nothing there yourself.
5. Header: `Phase: Closed`, `Updated` now. Board: replace the feature block with one row under **Finished** with a one-line result. Overview: the feature's nodes turn green.
6. Say in one line what was updated and that the feature can be continued later with `/A.reopen <file>`.

Closing ends this feature, not the project.
