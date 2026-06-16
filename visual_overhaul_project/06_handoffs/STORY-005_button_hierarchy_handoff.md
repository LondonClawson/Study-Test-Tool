# STORY-005 Button Hierarchy Handoff

Story/Task:
`STORY-005_button_hierarchy.md`

Status:
Submitted For Review. Implementation is complete and waiting for PM/reviewer
acceptance.

Summary:
Applied the MVP button hierarchy to the Home/Test Selector target area by using
the shared `gui.styles.get_button_style()` role helper for assigned buttons.
No callback, navigation, dialog, service, copy, or layout behavior was changed.

Files changed:
- `study_test_tool/gui/test_selector.py`
- `study_test_tool/gui/components/collapsible_group.py`
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/04_stories/STORY-005_button_hierarchy.md`
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
- Code-level callback preservation checked for Import, New Test, Mix Test,
  Analytics, View History, Review Missed, Take Test, Edit, Export, Archive,
  Delete, Unarchive, and Archive Group.
- Disabled Take Test remains configured through the existing zero-question
  branch.

Tests run:
- `PYTHONPATH=study_test_tool python3 -m py_compile study_test_tool/gui/test_selector.py study_test_tool/gui/components/collapsible_group.py`
- `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 study_test_tool/main.py`
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
- Do not refactor the repeated inline `get_button_style("...")` calls yet.
  A local helper could reduce repetition, but it would hide the explicit role
  decisions that this pilot is meant to prove. Revisit after the PM/reviewer
  accepts the Home/Test Selector role mapping or after a second screen repeats
  the same pattern.

Risks:
- `CollapsibleGroup` now imports `get_button_style()` for the Home-rendered
  Archive Group button. This is scoped today because the component is only used
  by Home/Test Selector, but future reuse should confirm the secondary role is
  still appropriate.
- Light/dark readability was smoke-checked by startup only; no screenshot pass
  was captured in this chunk.

Follow-up backlog items:
- After `STORY-005` is accepted, select a named pilot area for
  `STORY-006_card_and_list_patterns.md`.
- Use this role mapping as the starting point for blocked screen stories that
  depend on button hierarchy.
