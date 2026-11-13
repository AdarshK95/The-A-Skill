# Lean — least code, most capability, nothing duplicated, nothing hardcoded

The standard every proposal and every build is held to. Fewer lines is never bought with lost capability; the same capability with fewer lines, fewer files and fewer special cases always wins.

## The ladder — before proposing anything new

Stop at the first rung that holds, after Read is complete:

1. **Does it need to exist?** A need the ask does not evidence is skipped and said so in one line.
2. **Already here?** The reuse search below has run and found it → reuse or extend it.
3. **Standard library does it?** Use it. Two options of the same size → the one correct on edge cases.
4. **Platform does it?** A native input over a widget library; a DB constraint over app code; a framework feature over a wrapper.
5. **An installed dependency does it?** Use it. A new dependency for what a few lines do is not lean.
6. **One line?** One line.
7. **Only then:** the minimum code that works, in the fewest files.

The ladder shortens the solution, never the reading.

**The ladder applies to anything you hand the user, not only to code.** A check, a script, a procedure or a tool you are about to write for them is climbed the same way: does an existing tool already answer the question (`git status` is a file comparison; a diff is a review; a folder listing is an inventory)? If it does, name the tool and the one command, and write nothing. A custom script that reproduces `git status` is the same failure as a custom cache that reproduces the standard library.

## Reuse search — mandatory in Evaluate

Duplicate *purpose* is the risk, not duplicate text: agents re-implement rather than copy. Before any new function, endpoint, component, query, helper or config path is proposed:

1. **Index.** Read the codebase map (`map_folder`) if present: the contracts say what each directory already provides. Read the artifacts ledger: it says what has already been measured, so nothing is probed twice.
2. **Search.** By meaning and by text: the verb and noun of the need (`export csv`, `format date`, `fetch orders`), the shape of the data, the route or table involved, sibling files of where the change would land. Use a semantic search tool when the host has one; grep otherwise. Search the whole repository, tests and scripts included.
3. **Categorize** each candidate: **exact** (does this already) · **close** (same domain, slightly different operation) · **pattern** (same shape, different domain) · **none**.
4. **Decide**, and write it in the report under *Reuse candidates*:

   | Need | Candidate (`path:symbol`) | Match | Decision |
   | --- | --- | --- | --- |
   | export rows as CSV | `lib/export.ts:toCsv` | close | extend with column selection |

   Exact → use it. Close → extend it, in place, for all callers. Pattern → follow it, so the codebase has one way. None → new, with one line on why nothing fit; three *none*s in one feature is a signal that a shared module is missing.

An empty *Reuse candidates* section means the search was not run; the self-check fails.

## Modularity — how new code plugs in

- **One path per purpose.** Two routes that fetch the same thing, two helpers that format the same value, two places that call the same endpoint: one is deleted or made to call the other. A second parallel path is never added to get one more field.
- **Nothing hardcoded that varies.** A URL, key name, limit, path, label, feature switch or environment detail lives in config or is passed in; code reads it. A literal that appears twice is already a parameter.
- **Accept dependencies, don't create them.** A function receives the client, the store, the clock; it does not construct them. That is what makes it testable and swappable.
- **Deep modules.** A small interface with the work behind it. One adapter means a hypothetical seam — don't build the seam until a second adapter exists. The deletion test: imagine deleting the module; if complexity vanishes it was a pass-through, if it reappears across callers it was earning its place.
- **Deletion over addition.** When a fix can remove code and still meet the ask, remove.
- **Fewest files.** A new file needs a reason a reader would accept; a new folder needs two.
- **Boring over clever.** Clever is what someone decodes at three in the morning.

## When not to be lean

Never simplified away: validation at a trust boundary (anything from a user, a network, a file); error handling that prevents data loss or a silent wrong answer; authentication, authorization, secrets handling; accessibility basics; anything the user explicitly asked for. When the user insists on the full version, build it without re-arguing, and log the decision.

## Marked simplifications

Every deliberate shortcut carries a one-line comment naming its ceiling and its upgrade path, in the project's comment style (for example `// lean: single global lock; per-account locks if throughput matters`). Simple then reads as intent, not oversight. `/A.drift` lists these markers so ceilings are revisited.

## Duplication and complexity check — at Realign

Over what this feature added or changed, answer with citations:

1. **Same purpose twice?** Any new symbol whose purpose an existing symbol already serves (re-run the reuse search over the *new* code).
2. **Parallel paths?** The same endpoint, table, file or service reached by two routes; the same data fetched or computed twice in one flow.
3. **Hardcoded?** Literals that exist in config or appear more than once.
4. **Pass-throughs?** Abstractions with one implementation, wrappers that only forward, interfaces nobody else uses.
5. **Dead or defensive?** Unreachable branches, checks the types already guarantee, commented-out code, comments that restate the code.
6. **Simplify pass** (behaviour-preserving, over recently modified code only): flatten nesting with early returns; split dense chains into named steps; inline single-use helpers; consolidate duplicates into the shared place; remove the dead and the defensive. **Balance:** never trade clarity for brevity — no nested ternaries, no dense one-liners, keep an abstraction that organizes; a change that would alter behaviour is a build finding, not a simplification. Each cut is proven by the existing check before the next.

Findings become Realign simplifications (applied when they need no decision) or decisions for the user. `/A.simplify` runs step 6 on demand over whatever was recently modified.

## One runnable check

Lean code without its check is unfinished. Non-trivial logic leaves the smallest check that fails if it breaks. Trivial one-liners need none; the ladder applies to tests too.
