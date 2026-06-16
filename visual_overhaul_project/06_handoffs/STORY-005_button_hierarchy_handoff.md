# STORY-005 Button Hierarchy Handoff

Story/Task:
`STORY-005_button_hierarchy.md`

Status:
Submitted For Review. Evidence pass is complete from the implementation side
and waiting for PM/reviewer acceptance.

Summary:
Applied the MVP button hierarchy to the Home/Test Selector target area by using
the shared `gui.styles.get_button_style()` role helper for assigned buttons.
No callback, navigation, dialog, service, copy, or layout behavior was changed.

Files changed:
- `study_test_tool/gui/test_selector.py`
- `study_test_tool/gui/components/collapsible_group.py`
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/04_stories/STORY-005_button_hierarchy.md`
- `visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `visual_overhaul_project/01_context/screenshots/after/STORY-005/light/light_home_expanded_cards.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-005/light/light_home_expanded_archived_cards.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-005/dark/dark_home_expanded_cards.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-005/dark/dark_home_expanded_archived_cards.png`
- `visual_overhaul_project/06_handoffs/STORY-005_button_hierarchy_assignment.md`
- `visual_overhaul_project/06_handoffs/STORY-005_button_hierarchy_handoff.md`

Definition of Ready checked:
Yes. `CTX-FOUNDATION`, `CTX-STYLE-INVENTORY`, and `CTX-HOME` were Ready before
implementation, and `STORY-004_shared_style_entrypoints.md` was Done.

Context summaries read:
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/01_context/summaries/style_inventory.md`
- `visual_overhaul_project/01_context/summaries/home_screen_context.md`
- `visual_overhaul_project/06_handoffs/STORY-004_shared_style_entrypoints_handoff.md`

Context summaries created/updated:
None.

Screens/states checked:
- Home/Test Selector startup smoke check reached the GUI main loop with no
  immediate console error.
- Captured expanded Home active-card actions in light and dark mode:
  `home_expanded_cards`.
- Captured expanded Home archived-card actions in light and dark mode:
  `home_expanded_archived_cards`.
- Visual evidence includes active-card Take Test, disabled Take Test on a
  zero-question seeded test, Edit, Export, Archive, active Delete, archived
  Unarchive, and archived Delete.
- Code-level callback preservation checked for Import, New Test, Mix Test,
  Analytics, View History, Review Missed, Take Test, Edit, Export, Archive,
  Delete, Unarchive, and Archive Group.
- Disabled Take Test remains configured through the existing zero-question
  branch.

Tests run:
- `PYTHONPATH=study_test_tool python3 -m py_compile study_test_tool/gui/test_selector.py study_test_tool/gui/components/collapsible_group.py`
- `PYTHONPATH=study_test_tool python3 -m py_compile visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 study_test_tool/main.py`
- `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states home_expanded_cards home_expanded_archived_cards --output visual_overhaul_project/01_context/screenshots/after/STORY-005`
- `git diff --check`

Tests not run and why:
Full pytest was not run because this implementation only changed GUI style
kwargs/imports. No service, database, scoring, import, session, or navigation
behavior changed.

Acceptance criteria notes:
- Primary role: New Test and active-card Take Test.
- Special role: Mix Test.
- Warning role: Review Missed.
- Secondary role: Import, Analytics, View History, Archive, Unarchive, and
  Archive Group.
- Tertiary role: Collapse/Expand All, Edit, and Export.
- Danger role: active and archived Delete.
- Success role intentionally unused; Export is no longer styled as success.
- Home/Test Selector remains the only migrated screen.

PM review notes:
- Reviewed on 2026-06-16. Scope stayed limited to Home/Test Selector button
  hierarchy and callback wiring appears preserved, but acceptance is withheld
  pending visual evidence for the full touched button set. The subsequent
  STORY-007 Home screenshots cover the main header and toolbar button roles, but
  they do not show expanded cards, card action buttons, or disabled Take Test.

PM requested changes:
- Capture or add reviewable visual evidence for expanded Home cards in light and
  dark mode.
- Evidence must include active card action buttons: Take Test, Edit, Export,
  Archive, and Delete.
- Evidence must include archived card actions: Unarchive and Delete.
- Evidence must include a zero-question active card showing disabled Take Test.
- Resubmit with screenshot paths or a documented capture blocker. Startup smoke
  and code-level callback inspection are not sufficient for this visual story.
- Do not refactor the repeated inline `get_button_style("...")` calls yet.
  A local helper could reduce repetition, but it would hide the explicit role
  decisions that this pilot is meant to prove. Revisit after the PM/reviewer
  accepts the Home/Test Selector role mapping or after a second screen repeats
  the same pattern.

Implementation update:
- Added `home_expanded_cards` and `home_expanded_archived_cards` capture states
  to the visual screenshot harness.
- Added a STORY-005-only zero-question Home fixture named "Empty Intake
  Template" so the disabled Take Test state is visible in repeatable review
  evidence without changing unrelated seeded screenshot states.
- Captured and validated the requested light/dark screenshots under
  `visual_overhaul_project/01_context/screenshots/after/STORY-005/`.

Risks:
- `CollapsibleGroup` now imports `get_button_style()` for the Home-rendered
  Archive Group button. This is scoped today because the component is only used
  by Home/Test Selector, but future reuse should confirm the secondary role is
  still appropriate.
- The screenshot harness now uses the CustomTkinter scrollable frame's internal
  canvas to position the archived-card evidence state. That is acceptable for
  development-only visual evidence, but it should not be copied into app code.

Follow-up backlog items:
- After `STORY-005` is accepted, use this role mapping as the starting point for
  blocked screen stories that depend on button hierarchy.
