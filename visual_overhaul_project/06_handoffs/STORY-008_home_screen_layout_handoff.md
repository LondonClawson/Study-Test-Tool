Story/Task:
`STORY-008_home_screen_layout.md`

Status:
Done. Accepted by PM/reviewer on 2026-06-16 after the PM-requested minimum
populated screenshot refresh; see
`visual_overhaul_project/06_handoffs/STORY-008_home_screen_layout_review.md`.

Summary:
Polished the Home/Test Selector shell around the accepted header, button, and
card pilots. The Home screen now uses semantic app/background surfaces, a
designed sort/collapse toolbar, an intentional scrollable content surface,
semantic group header containers, and a surfaced empty state with Import and
New Test actions. Home workflows, service calls, sorting values,
expanded/collapsed behavior, archive/delete confirmations, and navigation
callbacks were preserved.

Files changed:
- `study_test_tool/gui/test_selector.py`
- `study_test_tool/gui/components/collapsible_group.py`
- `study_test_tool/gui/styles.py`
- `visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/04_stories/STORY-008_home_screen_layout.md`
- `visual_overhaul_project/06_handoffs/STORY-008_home_screen_layout_handoff.md`
- `visual_overhaul_project/01_context/screenshots/after/STORY-008/`

Definition of Ready checked:
Yes. `STORY-008` was Ready and unblocked, CTX-HOME and CTX-FOUNDATION were
Ready, and the PM readiness pass named `STORY-008` as the next primary Dev 2
assignment.

Context summaries read:
- `visual_overhaul_project/01_context/summaries/home_screen_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/01_context/summaries/baseline_visual_audit.md`
- `visual_overhaul_project/01_context/summaries/style_inventory.md`
- `VISUAL_OVERHAUL_PLAN.md`
- Accepted handoffs for `STORY-004`, `STORY-005`, `STORY-006`, and `STORY-007`
- `visual_overhaul_project/06_handoffs/PM_readiness_pass_2026-06-16.md`

Context summaries created/updated:
None.

Screens/states checked:
- Home populated grouped/collapsed in light and dark mode.
- Home expanded active cards in light and dark mode.
- Home expanded archived cards in light and dark mode.
- Home empty state in light and dark mode.
- Home populated minimum-window layout in light and dark mode.
- Home empty minimum-window layout in light and dark mode.
- Focused Home navigation smoke for New Test, View History, Review Missed, and
  Analytics using an isolated temporary database.
- Resubmission check: refreshed Home populated minimum-window layout in light
  and dark mode after resetting the Home scrollable list to the top before
  capture.

Screenshot evidence:
- `visual_overhaul_project/01_context/screenshots/after/STORY-008/light/light_home_populated_grouped.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-008/light/light_home_expanded_cards.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-008/light/light_home_expanded_archived_cards.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-008/light/light_home_empty_state.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-008/light/light_home_minimum_populated.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-008/light/light_home_minimum_empty.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-008/dark/dark_home_populated_grouped.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-008/dark/dark_home_expanded_cards.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-008/dark/dark_home_expanded_archived_cards.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-008/dark/dark_home_empty_state.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-008/dark/dark_home_minimum_populated.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-008/dark/dark_home_minimum_empty.png`

Tests run:
- `python3 -m compileall -q study_test_tool/gui/styles.py study_test_tool/gui/test_selector.py study_test_tool/gui/components/collapsible_group.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/styles.py study_test_tool/gui/test_selector.py study_test_tool/gui/components/collapsible_group.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states home_populated_grouped home_expanded_cards home_expanded_archived_cards home_empty_state home_minimum_populated home_minimum_empty --output visual_overhaul_project/01_context/screenshots/after/STORY-008`
- Focused Home navigation smoke with a temporary SQLite database for New Test,
  View History, Review Missed, and Analytics.

Tests not run and why:
Full pytest was not run because this story changed GUI layout/style and the
development screenshot harness only. No service, database, scoring, import,
export, persistence, or session behavior changed.

Acceptance criteria notes:
- The Home screen no longer uses the default gray scroll box as the primary
  content area; header, toolbar, group list, and empty state now use accepted
  semantic surfaces and borders.
- Import, New Test, Mix Test, Review Missed, View History, and Analytics remain
  grouped in workflow/navigation rows with the accepted button roles.
- The empty state is a designed surface with concise copy and existing Import
  and New Test callbacks.
- Groups preserve expand/collapse and Archive Group behavior.
- Minimum-window evidence was captured at the documented 800x600 size.

Scope-adjacent notes for PM review:
- `capture_baseline_screenshots.py` now has `home_minimum_populated` and
  `home_minimum_empty` states, resets default geometry before each capture
  state, and allows 800x600 minimum-window screenshots to validate on non-retina
  displays. This was needed for repeatable STORY-008 evidence.
- Resubmission update: `home_minimum_populated` now resets the Home scrollable
  list to the top before capture, and the refreshed light/dark screenshots show
  the top of the Home list cleanly at the documented minimum window size.
- The screenshot harness now brings the app window to the front before each
  capture so overlapping development windows do not obscure evidence.
- Home card action frames are packed before info frames and button widths/gaps
  were tightened so the existing horizontal action row does not clip at the
  minimum supported window size. No callback or card data behavior changed.

Risks:
- `CollapsibleGroup` now uses semantic card styling. It is currently a Home
  component; if reused elsewhere later, confirm the Home group-header treatment
  still fits that screen.
- The Home card action-row tightening is a layout-fit exception. PM should
  decide whether to accept it now or ask for a narrower/different follow-up in
  `STORY-009`.

Follow-up backlog items:
- `STORY-009_home_test_cards_and_actions.md`: revisit Home card internals,
  including metadata hierarchy, action-row responsiveness, disabled Take Test
  affordance, archived-card details, and any further utility/danger action
  treatment.
