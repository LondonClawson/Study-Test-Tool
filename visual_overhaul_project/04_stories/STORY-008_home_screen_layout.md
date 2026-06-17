# STORY-008: Home Screen Layout

## Status

Done.

## Readiness

- Blocked by: None.
- CTX-HOME is Ready from `R-003_home_screen_context.md`.
- Unblocked by: accepted completion of the Home/Test Selector button hierarchy
  pilot.

CTX-FOUNDATION and `STORY-004_shared_style_entrypoints.md` are Done.
`STORY-005` has accepted Home button role evidence. This story is Ready for Dev
2 assignment.

## Sprint

Target sprint: Sprint 1.

## User Story

As a user, I want the home screen to feel like a polished study dashboard so that
available tests and study actions are immediately clear.

## Goal

Polish the home screen shell: page title, toolbar, sort/filter row, scrollable
content area, group spacing, and empty state.

## Required Context

- `visual_overhaul_project/01_context/summaries/home_screen_context.md`.
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- `VISUAL_OVERHAUL_PLAN.md`.
- Research task if CTX-HOME becomes stale:
  `visual_overhaul_project/02_research_tasks/R-003_home_screen_context.md`.

## Scope

In:

- Home layout composition.
- Toolbar spacing and action grouping.
- Sort/collapse control presentation.
- Empty state.
- Group area spacing.

Out:

- Test-card internal redesign, unless required for layout fit.
- Import/export behavior changes.
- Dialog redesign.

## Likely Files

- `study_test_tool/gui/test_selector.py`.
- Shared style entry points from earlier stories.

## Implementation Steps

1. Read CTX-HOME, CTX-FOUNDATION, and the Dev 2 Quick Start notes.
2. Inspect only the home layout regions named by CTX-HOME.
3. Polish the page shell, toolbar grouping, sort/collapse row, group spacing,
   scroll area, and empty state.
4. Preserve all home actions and expanded/collapsed behavior.
5. Verify populated, grouped/collapsed, archived, empty, light, dark, and
   minimum-window states.
6. Document card-specific follow-up work for STORY-009.

## Acceptance Criteria

- The home screen no longer reads as default framework output.
- Import, New Test, Mix Test, Review Missed, View History, and Analytics have
  clear visual grouping and hierarchy.
- Empty state is intentional and concise.
- Groups remain functional and preserve expanded/collapsed behavior.
- Layout remains usable at the minimum window size.

## Verification

- Screenshot evidence is required under
  `visual_overhaul_project/01_context/screenshots/after/STORY-008/`.
- Capture or document a blocker for light and dark Home states covering
  populated expanded groups, archived content, empty state, and minimum-window
  layout.
- Navigation smoke check for home toolbar actions.
- Run relevant tests if behavior-bearing changes are made.

## Dev 2 Assignment Notes

- Do not redesign test-card internals unless required for layout fit and noted
  in the handoff.
- Do not change import/export, archive, delete, restore, mix, review, history,
  analytics, or take-test behavior.
- If CTX-HOME is missing or stale, stop and assign R-003.

## Handoff Requirements

- List home states checked.
- Include before/after screenshot references if available.
- List card-specific follow-up work for STORY-009.
