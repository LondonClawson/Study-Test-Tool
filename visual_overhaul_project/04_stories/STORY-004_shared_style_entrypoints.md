# STORY-004: Shared Style Entry Points

## Status

Submitted For Review.

## Readiness

- Blocked by: None.
- Unblocked by: `STORY-003_visual_foundation_spec.md`.

CTX-FOUNDATION is Ready as of PM review on 2026-06-15.

## Sprint

Target sprint: Sprint 1.

## User Story

As a maintainer, I want shared style entry points so that screen files stop
duplicating visual constants and inline role colors.

## Goal

Create the smallest practical shared styling structure needed for MVP screens.

## Required Context

- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- `visual_overhaul_project/01_context/summaries/style_inventory.md`.
- `visual_overhaul_project/01_context/summaries/gui_architecture_summary.md`.

## Scope

In:

- Shared constants or helper functions for semantic visual roles.
- Compatibility with existing `config.settings` conventions.
- A narrow migration of only the roles needed by upcoming stories, using
  `study_test_tool/gui/components/progress_bar.py` as the proof target.

Out:

- Large design-system framework.
- Screen redesign.
- New dependency.
- Behavior changes.

## Likely Files

- `study_test_tool/config/settings.py`.
- Possible new or existing helper under `study_test_tool/gui/components/`.
- `study_test_tool/gui/components/progress_bar.py` as the required proof target.

## Implementation Steps

1. Read CTX-FOUNDATION, CTX-STYLE-INVENTORY, and CTX-GUI-ARCH.
2. Identify the minimum shared style entry points needed by upcoming stories.
3. Add or adjust shared constants/helpers using existing project conventions.
4. Migrate only `study_test_tool/gui/components/progress_bar.py` to prove the
   entry points.
5. Smoke check app startup and the touched validation area.
6. Document entry points, intentionally unmigrated areas, and follow-up stories.

## Acceptance Criteria

- Shared style entry points are named by purpose, not by one-off screen.
- They support light and dark CustomTkinter values where needed.
- Existing app startup and navigation remain unchanged.
- No unrelated visual refactor is bundled into this story.
- `ProgressBar` still renders one clickable button per question and preserves
  current, flagged, answered, and unanswered status behavior.

## Verification

- Run the relevant subset of tests if behavior-bearing files are touched.
- Launch the app or inspect a test-taking screen enough to confirm no startup
  error and no broken progress-button rendering.
- Record light/dark smoke-check notes for the progress buttons if helpers
  include theme tuples.

## Dev 2 Assignment Notes

- Do not redesign screens while creating shared style entry points.
- Do not move or redesign the test-taking shell; `ProgressBar` is only a compact
  proof target for shared style entry points.
- Do not add a broad design-system framework or dependency.
- If CTX-FOUNDATION is not Ready, including Submitted For Review or stale, stop
  and return this story to Blocked.

## Handoff Requirements

- List new or changed style entry points.
- List files intentionally not migrated yet.
- List follow-up stories that should use the entry points.
