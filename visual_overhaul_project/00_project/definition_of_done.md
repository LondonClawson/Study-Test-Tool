# Definition Of Done

## Story Done

A visual overhaul story is done when all of these are true:

- The story passed the Definition of Ready before implementation began, or the
  handoff explains why the work proceeded under PM direction.
- The assigned story scope is complete and no unrelated screens or behaviors
  were changed.
- Required context summaries were read before implementation.
- Any stale or missing context discovered during work was updated in
  `01_context/summaries/`.
- Acceptance criteria in the story file are satisfied.
- Current workflows still behave the same.
- Relevant automated tests were run when behavior-bearing files were touched.
- Visual verification was recorded, including light/dark notes when relevant.
- A handoff note was written or the story file was updated with verification,
  changed files, remaining risks, and follow-up backlog items.

## Research Task Done

A research task is done when all of these are true:

- The required source files or screens were inspected.
- The specified summary file was created or updated.
- The summary includes source paths, observed states, risks, and open questions.
- The context index was updated if a new summary was added.
- Any blocked screenshot or runtime step is called out with the reason.

## Visual Implementation Done

Visual implementation is done when all of these are true:

- Primary, secondary, tertiary, danger, warning, success, and muted roles are
  applied consistently for the touched area.
- Text hierarchy is intentional and readable.
- Spacing, padding, radius, and borders match the current visual foundation.
- Empty/loading/error states in the touched area are not plain unstyled text
  unless explicitly out of scope.
- Minimum window size remains usable.
- Light and dark mode remain readable.

## MVP Done

The MVP visual overhaul is done when:

- Every screen listed in the charter has passed before/after visual review.
- Shared visual foundation is documented and used by major screens.
- Button hierarchy, cards, list rows, status badges, page headers, and empty
  states are consistent.
- No core workflow, scoring, import/export, database, or session behavior changed.
- Full relevant test suite has been run or skipped only with a documented reason.
