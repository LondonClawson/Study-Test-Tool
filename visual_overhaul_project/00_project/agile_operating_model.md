# Agile Operating Model

## Method

Use a lightweight Scrum-style process. The project should move in short sprints,
but the documentation is optimized for asynchronous agents who may receive only
one task at a time.

The preferred execution model is a two-agent pipeline. A Research Agent first
produces a focused context summary. An Implementation Agent later reads the
story and summary, then completes the visual change without repeating broad
codebase discovery.

## Roles

- Product Owner: the repository owner or user making product decisions.
- Project Manager: maintains backlog, sprint sequencing, context requirements,
  and acceptance criteria.
- Research Agent: collects bounded context and writes summaries to
  `01_context/summaries/`.
- Implementation Agent: completes one story using the linked summaries.
- Review Agent: verifies acceptance criteria, visual checks, regression risk,
  and handoff quality.

One human or agent may hold multiple roles in a sprint, but the role distinction
keeps outputs clear.

## Sprint Cadence

Use 1-week sprints by default. If a sprint is run by intermittent agents, treat
the sprint as a batch of related stories rather than a calendar commitment.

Recommended sprint order:

- Sprint 0: context and visual audit.
- Sprint 1: visual foundation and home screen.
- Sprint 2: test-taking and results.
- Sprint 3: editor, history, analytics, review, and dialogs.
- Sprint 4: light/dark validation, minimum-size pass, and MVP closeout.

## Ceremonies

- Sprint Planning: choose stories from the backlog and confirm context summaries
  exist, pass the Definition of Ready, or are scheduled as research tasks.
- Daily Check-in: update story status and blockers. For async agents, this can
  be a short handoff note.
- Backlog Refinement: split any story that requires more than one screen or one
  component family.
- Sprint Review: compare work against screenshots and acceptance criteria.
- Retrospective: record process improvements in the sprint file or a handoff.

## Artifact Rules

- Every story must name required context summaries.
- Research tasks must write or update a specific summary file.
- Implementation stories should avoid fresh broad code exploration unless the
  assigned summaries are missing or stale.
- Implementation stories are not assignable to junior developers until they pass
  `00_project/definition_of_ready.md`.
- A story is too broad if it touches more than one major screen without a shared
  component reason.
- A summary is stale when the source files it describes changed after the
  summary date or the story needs states not covered by the summary.

## Status Terms

- Proposed: documented but not ready for work.
- Ready: the item passes the relevant Definition of Ready gate.
- In Progress: actively owned by an agent.
- Blocked: cannot proceed without a decision, missing dependency, or environment
  issue.
- Done: completed and handed off with verification notes.

For context summaries, use the expanded status terms in
`00_project/status_board.md`: Missing, Placeholder, Seeded, Ready, In Progress,
Blocked, Done, and Stale.
