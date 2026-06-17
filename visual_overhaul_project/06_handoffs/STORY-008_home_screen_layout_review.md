# STORY-008 Home Screen Layout Review

Story/Task:
`STORY-008_home_screen_layout.md`

Status:
Done. Accepted by PM/reviewer on 2026-06-16 after resubmission.

Review Summary:
The Home shell/layout implementation is accepted. The initial review withheld
acceptance because the minimum populated screenshots were captured with the Home
list already scrolled down. The resubmitted evidence now shows the top of the
minimum-window Home list cleanly in both light and dark mode.

Findings:
- The prior minimum populated evidence blocker is resolved. Both refreshed
  minimum-window screenshots show the header, toolbar, group header, first card,
  and active card actions without top clipping.
- The remaining roughness is in card internals/action hierarchy, especially the
  disabled Take Test treatment and action-row density. That work is explicitly
  reserved for `STORY-009_home_test_cards_and_actions.md` and does not block
  acceptance of the Home shell/layout story.

Acceptance Decision:
Accepted. `STORY-008_home_screen_layout.md` is Done. `STORY-009` can move to
Ready after its story file is tightened with concrete screenshot and smoke
check expectations.

Evidence Reviewed:
- `visual_overhaul_project/01_context/screenshots/after/STORY-008/light/light_home_expanded_cards.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-008/light/light_home_empty_state.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-008/light/light_home_minimum_empty.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-008/light/light_home_minimum_populated.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-008/dark/dark_home_minimum_populated.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-008/dark/dark_home_empty_state.png`

Verification Run By PM:
- `PYTHONPATH=study_test_tool python3 -m py_compile study_test_tool/gui/test_selector.py study_test_tool/gui/components/collapsible_group.py study_test_tool/gui/styles.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/styles.py study_test_tool/gui/test_selector.py study_test_tool/gui/components/collapsible_group.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --states home_populated_grouped home_expanded_cards home_expanded_archived_cards home_empty_state home_minimum_populated home_minimum_empty --output visual_overhaul_project/01_context/screenshots/after/STORY-008`
- `git diff --check`

Verification Result:
All commands passed. Screenshot validation covered the 12 light/dark Home files
submitted for `STORY-008`.

Follow-up:
`STORY-009_home_test_cards_and_actions.md` was later accepted. The current
implementation path is active `STORY-013`, while `STORY-012` waits on a
targeted changes-requested fix. Keep later Home follow-up behind those lanes
unless PM opens new capacity.
