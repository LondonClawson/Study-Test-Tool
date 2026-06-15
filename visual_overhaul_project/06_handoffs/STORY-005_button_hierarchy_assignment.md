# STORY-005 Button Hierarchy Assignment

Assignment:
Apply the MVP button hierarchy to the Home/Test Selector target area.

Story:
`visual_overhaul_project/04_stories/STORY-005_button_hierarchy.md`

Status:
Ready for Dev 2 assignment.

Required context:
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/01_context/summaries/style_inventory.md`
- `visual_overhaul_project/01_context/summaries/home_screen_context.md`
- `visual_overhaul_project/06_handoffs/STORY-004_shared_style_entrypoints_handoff.md`

Target area:
Home/Test Selector only, implemented in `study_test_tool/gui/test_selector.py`.

In scope:
- Top action bar buttons: Import, New Test, Mix Test, Analytics, View History,
  and Review Missed.
- Active test-card buttons: Take Test, disabled Take Test for zero-question
  tests, Edit, Export, Archive, and Delete.
- Archived test-card buttons: Unarchive and Delete.
- Group header Archive Group button.
- Use accepted `gui.styles` button role helpers where practical.

Out of scope:
- Home layout redesign, card surface redesign, group header pattern redesign,
  dialog polish, copy changes, callback changes, navigation changes, and
  app-wide button migration.

Implementation notes:
- Preserve all existing `command=` callbacks and service calls.
- Keep Mix Test as the accepted special workflow role.
- Keep Delete as danger and visually lower-frequency than the primary workflow.
- Treat Edit, Export, Archive, Analytics, View History, and group archive as
  secondary or utility unless the foundation explicitly says otherwise.
- Do not change native file dialog or messagebox behavior.

Required verification:
- Smoke check Home/Test Selector in light and dark mode.
- Verify Import, New Test, Mix Test, Analytics, View History, and Review Missed
  still trigger the same routes/dialogs.
- Verify Take Test still launches the same mode flow and disabled Take Test
  remains disabled for zero-question tests.
- Verify Edit, Export, Archive, Delete, Unarchive, and Archive Group keep their
  existing callback and confirmation behavior.
- Run pytest only if behavior-bearing code changes; otherwise document why it
  was not run.

Handoff requirements:
- List changed buttons by final role.
- List unresolved role questions.
- List screens intentionally not migrated.
- Include light/dark smoke notes and callback-preservation notes.
