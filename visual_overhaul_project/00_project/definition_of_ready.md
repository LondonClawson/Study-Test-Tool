# Definition Of Ready

Use this gate before assigning work to junior developers. A task is not ready
just because a file exists or a dependency is named. It is ready when the next
agent can complete the assignment without making project-management decisions or
rediscovering broad code context.

## Research Task Ready

A research task is ready to assign when all of these are true:

- The output summary file is named.
- Required inputs are listed.
- Source files, screens, or workflows to inspect are listed.
- Research steps are bounded and do not include implementation.
- The task says what must not be changed.
- Done criteria explain how the PM or reviewer will judge the summary.
- The task is listed on the status board and dependency map.

## Context Summary Ready

A context summary is ready for implementation use when all of these are true:

- The producing research task is named.
- Source files and screens inspected are listed.
- Important UI states and workflows are mapped.
- Visual findings are separated from recommendations.
- Behavior constraints are explicit.
- Implementation risks and fragile interactions are called out.
- Open questions are listed instead of guessed.
- The summary recommends any needed story splits.
- Context index and status board state are updated.

## Implementation Story Ready

An implementation story is ready to assign when all of these are true:

- Every required context summary is Ready.
- The scope is one major screen, one shared component family, or one clear
  foundation decision.
- Likely files are listed.
- In-scope and out-of-scope work are concrete.
- Implementation steps are included.
- Acceptance criteria are observable, not only qualitative.
- Verification lists exact screens, states, smoke checks, and test commands or
  a reason tests are not required.
- Handoff requirements say what evidence the developer must provide.
- The story status is Ready on the status board.

## Two-Agent Flow

Use this project as a two-agent pipeline:

1. Dev 1 completes the research task and writes the context summary.
2. The PM or reviewer marks the summary Ready only if it passes this gate.
3. Dev 2 reads the story and required summary, then implements the story without
   repeating broad exploration.

If Dev 2 finds missing or stale context, pause implementation, update or create
the linked research task, and return the implementation story to Blocked.

## Not Ready Examples

- A story says the pilot area will be chosen during sprint planning.
- A story covers multiple unrelated screens without a shared component reason.
- Acceptance criteria say only "polished" or "easy to scan" without named states
  or verification.
- A summary lists files but does not identify workflows, states, risks, and
  behavior constraints.
