# Root cause — the method

Diagnosis is a stage of its own, before planning. Its output is a cause, with the evidence and the confidence, never a fix. Treating a symptom is not an acceptable outcome; "not found, and here is what would find it" is.

## 1. Understand, and compartmentalize

Capture the user's account verbatim, then keep four boxes apart for the whole investigation:

| Box | Holds | Rule |
| --- | --- | --- |
| **Symptom** | What they saw, exactly | The thing to explain |
| **Expectation** | What they expected instead | Defines "wrong" |
| **Their insights** | Suspicions, hunches, "I think it's because…", context only they have | Hypotheses to test — never ignored, never assumed true. Each gets a verdict in the report |
| **What they want next** | The fix they have in mind, the behaviour they want | Parked for the plan stage; it does not steer the diagnosis, and the diagnosis may show it is not the cure |

## 2. Observe

Get the artifacts, not the description of them: outputs, logs, traces, stored records, request and response bodies. For a model or retrieval system: the question as sent, what was retrieved, the prompt as rendered, the model output, the parameters. Reproduce when possible; when not, say what prevents it. A diagnosis built on one pasted answer is a HYPOTHESIS by definition.

## 3. Three lanes, in parallel, each blind to the others

| Lane | Starts from | Moves | Stops at |
| --- | --- | --- | --- |
| **Reverse** | the symptom | backward, hop by hop (`tracing.md` trace table): where does correct input first become wrong output? | an **origin** (below) — not the first plausible candidate |
| **Forward** | the entry point | forward through every stage: under what conditions could *this* error arise here? Continues past the first candidate — a later stage can produce the same symptom | the output |
| **Zoom-out** | the design | what is this part for; what was it designed to do (element history, lineage, decisions); when did the behaviour start (git); is this a design gap, a regression, a data gap, a configuration gap, or a misuse? | a verdict on kind, with its evidence |

**Origin rule.** A lane stops only at something the system *received* rather than *produced*: an input, a configuration value, data content, a design decision, a code path that exists by choice. Anything between symptom and origin is a **cascade**, recorded as a chain `origin → effect → … → symptom`. A candidate that is itself produced by an earlier step is a link, not the cause.

Each lane returns: its candidates with evidence (`path:symbol`, log line, record id), the chain it followed, and a **coverage statement**: the segments, components and layers it examined. At depth S the agent runs the lanes itself, one after another, writing each lane's result before starting the next (blindness by discipline). At M and above each lane is a fresh subagent (`hosts.md`).

## 4. Coverage check — before any reconciliation

Draw the **path map**: entry → every stage → output, plus the layer beneath each stage. Mark each segment *examined by* (which lanes) or *not examined*. Gaps have three directions:

- **Along the path** — the stretch between where the forward lane reached and where the reverse lane reached, when they did not meet.
- **Lateral** — components that share state, configuration, data, timing or a session with the path: another tab, a cache, a queue, a concurrent writer.
- **Vertical** — the layer beneath: network, authentication, the model or provider, storage, environment differences (dev vs prod, versions, flags).

Every gap that could carry the error gets a **targeted pass** (parallel where independent). Repeat until the map has no unexamined segment that could carry the error. Record the map in the report; it is the proof of coverage.

## 5. Reconcile

Merge the lanes' candidates:

- Implicated by two or more lanes, at an origin → **root cause candidate**.
- In a cascade chain → ordered; the origin is the cause, the rest are effects (and places where the symptom could be *masked*, which is different from fixing it).
- Implicated by one lane only → **contributing** or **ruled out**, with the evidence that rules it out.
- The user's insights → each one **confirmed / refuted / untested**, with why.
- Several surviving candidates → they go to step 6 as separate predictions.

## 6. Confirm — what a person does, and the step most diagnoses skip

Every surviving candidate gets a **falsifiable prediction** and a **test**: *if this is the cause, then <doing X> makes the symptom <appear / disappear>*. X is one change: toggle the configuration, swap the input, replay with the other variant or data, simulate the condition, bisect the change, run with the suspected component stubbed. Run it.

| Outcome | Then |
| --- | --- |
| Prediction holds | **CONFIRMED** |
| Test cannot be run here (needs production data, a credential, a device) | **LIKELY** — say exactly what test would confirm it and what it needs |
| Prediction fails | The candidate is demoted; the new fact goes back to steps 4–5; loop, bounded by the depth |
| Every candidate fails | **Not found.** Report what was ruled out, the coverage map, and the evidence that would find it. Never report a symptom treatment as a cause |

At XL, a fresh reviewer runs the **critic** lens on the confirmed cause: "assume this is wrong — where else could the symptom come from, given this evidence?" An unanswerable critic finding reopens step 4.

## 7. Report

Plain words first: what went wrong, why, how sure, what it is not. Then: the cause (CONFIRMED / LIKELY) with its condition — *when* the error happens — and its chain; contributing causes; ruled out, with evidence; the user's insights with verdicts; the coverage map; the test that confirmed it. No fix. The last line hands off: "Next: `/A.plan` to plan the fix at <origin>, where both lanes converged." A root cause that is only HYPOTHESIS does not hand off; it says what would raise it.

## Depth

Chosen from signals, escalated mid-way when a shallower pass does not close; the user may force `.m` `.l` `.xl`.

| Depth | Runs | Enough when |
| --- | --- | --- |
| **S** | Understand, observe, reverse lane only, confirm | One element, reproducible, the reverse lane reaches an origin in one or two hops and the test holds |
| **M** | + forward lane, coverage check, rule-outs | More than one hop, or the first candidate is a link not an origin |
| **L** | + zoom-out lane (element history, lineage, git tipping point), lateral and vertical gaps, environment and data checks | More than one element, intermittent, data- or environment-dependent, a regression |
| **XL** | + fresh reviewers for the lanes and a critic on the confirmed cause; experiments between surviving candidates | Seen in production, a user hypothesis the lanes cannot confirm or refute, or the cause still open after L |

Raising signals: the cause is unknown after the reverse lane; more than one element implicated; intermittent; depends on data or environment; seen in production; the user's hypothesis survives untested.
