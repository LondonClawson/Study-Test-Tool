# STORY-009 Home Test Cards And Actions Readiness Review

Story/Task:
`STORY-009_home_test_cards_and_actions.md`

Status:
Ready after PM readiness review on 2026-06-16.

Purpose:
Clear the Home card/action story after `STORY-008_home_screen_layout.md` was
accepted, while keeping the next developer away from already accepted Home
shell/layout work.

Decision:
`STORY-009_home_test_cards_and_actions.md` is Ready. CTX-HOME and
CTX-FOUNDATION are Ready, `STORY-006_card_and_list_patterns.md` is accepted,
and the accepted `STORY-008` shell gives the card/action work a stable Home
surface.

Scope Confirmation:
- Keep the story limited to active test cards, archived test cards, metadata
  hierarchy, disabled Take Test treatment, and card action hierarchy.
- Preserve sorting, grouping, expanded/collapsed behavior, archive/delete
  confirmations, import/export behavior, and navigation callbacks.
- Do not redesign the Home header, toolbar, scroll surface, group shell, or
  empty state accepted in `STORY-008`.

Required Screenshot Evidence:
Capture under `visual_overhaul_project/01_context/screenshots/after/STORY-009/`
or document exact blockers in the handoff.

Required states:
- Populated expanded active cards in light and dark mode.
- Grouped/collapsed cards in light and dark mode.
- Expanded archived cards in light and dark mode.
- Zero-question disabled Take Test treatment in light and dark mode.
- Minimum-window populated layout in light and dark mode.

Verification Expectations:
- Smoke check Take Test, Edit, Export, Archive, Delete, Unarchive, and Archive
  Group still call the same workflows.
- Run focused GUI syntax/format checks for any touched files.
- Run relevant pytest tests only if behavior-bearing service, persistence,
  session, import/export, or callback logic changes.

Priority:
This priority note is superseded by the 2026-06-16 PM acceptance pass:
`STORY-009` and `STORY-011` are Done, `STORY-012` is Changes Requested for the
retake-state fix, and `STORY-013` is the active implementation lane. Do not pull
developers into lower-priority Sprint 3 polish stories unless another lane is
intentionally opened.

Files Updated:
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/04_stories/STORY-009_home_test_cards_and_actions.md`
- `visual_overhaul_project/06_handoffs/STORY-009_home_test_cards_and_actions_readiness_review.md`

Tests:
Not run. This readiness review was PM tracker/documentation work only; no
application code changed.
