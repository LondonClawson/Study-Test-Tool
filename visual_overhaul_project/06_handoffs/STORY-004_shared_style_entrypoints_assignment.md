# STORY-004 Shared Style Entry Points Assignment

Assignment: Create the shared visual style entry points.
Role: Dev 2 Implementation Agent

Primary file:
`visual_overhaul_project/04_stories/STORY-004_shared_style_entrypoints.md`

Read these context summaries first:
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/01_context/summaries/style_inventory.md`
- `visual_overhaul_project/01_context/summaries/gui_architecture_summary.md`

Do this:
- Create the smallest practical shared styling structure needed by upcoming
  visual stories.
- Prefer semantic role names from `visual_foundation_decisions.md`.
- Support CustomTkinter light/dark tuple colors where the foundation requires
  light/dark-specific values.
- Keep compatibility with existing `config.settings` conventions.
- Migrate only this proof-of-use target:
  `study_test_tool/gui/components/progress_bar.py`.
- Use that target to prove compact typography, radius, and question-progress
  status roles can come from the shared style entry points.
- Document which areas are intentionally not migrated yet.

Do not do this:
- Do not redesign any screen.
- Do not restyle every button, card, row, or header in the app.
- Do not add a design-system framework or dependency.
- Do not change navigation, service calls, database access, import/export,
  scoring, review selection, mix-test behavior, or session behavior.
- Do not replace native dialogs or file dialogs.

Expected output:
- Shared visual constants or helper functions for semantic roles.
- A narrow proof-of-use migration in
  `study_test_tool/gui/components/progress_bar.py`.
- Updated `STORY-004` status and a completion handoff.

Required verification:
- Run the relevant subset of tests if behavior-bearing code paths are touched.
- Launch the app or inspect a test-taking screen enough to confirm no startup
  error and no broken progress-button rendering.
- Record light/dark smoke-check notes for the progress buttons if helpers
  include theme tuples.
- Run `git diff --check`.

Handoff location:
Use `visual_overhaul_project/06_handoffs/handoff_template.md` and save the
completed handoff as:
`visual_overhaul_project/06_handoffs/STORY-004_shared_style_entrypoints_handoff.md`

Notes:
- CTX-FOUNDATION is Ready as of PM review on 2026-06-15.
- The proof target is deliberately `ProgressBar`, not the full test-taking
  screen. Do not move button placement, navigation behavior, progress-click
  behavior, or question status semantics.
- If implementation discovers incomplete foundation roles, stop and document the
  missing decision instead of guessing.
- After this story is Done, PM should select a narrow target area for
  `STORY-005_button_hierarchy.md`.
