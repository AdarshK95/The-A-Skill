# Elements

_The system's parts and what has been done to them. One section per element; the id is stable, `Names` collects every name the project has used, `History` is append-only. Maintained by the `/A.*` commands at Report, Decision and Close; assembled into the map by `/A.project.map`. Rules: the skill's `core/references/elements.md`._

## Flows

_Named sequences of elements in the order they run. One numbered line per step: `N. <element-id> · <what happens here>`, then `Sources:`. Fragments from passes go under the flow's name as `### <flow> (fragment, F<n>)`; the map merges them._

<!--
### chat-turn · a user sends a message and gets an answer
1. chat-renderer · the browser posts /chat
2. chat-reception · stamps the record, opens the turn
Sources: F<n>
-->

<!--
## <element-id>
Names: <current name> · <older name> · <alias>
Layer: entry | api | orchestration | agents | stores | platform
Part of: <element-id, or none>
Purpose: <one line>
Code: <path (symbols)> · <path>
Interfaces: <routes, events, contracts>
Area: <one of the project's areas>
Depends on: <element-id> · <element-id>
Used by: <element-id>
Sources: <documents that describe it, with dates>
State: stable | in change | planned | unwired | untouched | superseded
Note: <optional, why the state or anything a reader should know>
History:
- <date> · F<n> <title> (<type>) · <decisions> · <one-line result>
-->
