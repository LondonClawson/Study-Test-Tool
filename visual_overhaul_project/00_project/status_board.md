# Visual Overhaul Status Board

Use this board as the fast project scan. Update it when a research task,
summary, story, or sprint changes state.

## Status Terms

- Missing: expected artifact does not exist yet.
- Placeholder: artifact exists but is not ready for implementation use.
- Seeded: artifact has initial context and may be useful, but should be refreshed
  when source files change or screenshots become available.
- Ready: artifact passes the relevant Definition of Ready gate.
- In Progress: actively owned.
- Submitted For Review: assigned work is complete from the agent side and is
  waiting for reviewer or PM acceptance.
- Blocked: waiting on a dependency, decision, or environment.
- Done: complete and handed off.
- Stale: artifact exists but source changes or new requirements make it unsafe
  to rely on without refresh.

Use `00_project/definition_of_ready.md` before marking any research task,
context summary, or implementation story Ready.
Use `00_project/status_transition_rules.md` when moving items between statuses.

## Summary Status

| Summary | Status | Unblocks |
| --- | --- | --- |
| `gui_architecture_summary.md` | Seeded | Most stories |
| `screen_inventory.md` | Seeded | Most stories |
| `current_visual_state_seed.md` | Seeded | Sprint 0 research |
| `baseline_visual_audit.md` | Blocked | `STORY-003`, validation stories; app launch and bare `tkinter.Tk()` both exit `-1` before any window appears in this shell |
| `style_inventory.md` | Ready | `STORY-003`, `STORY-004` |
| `home_screen_context.md` | Ready | `STORY-008`, `STORY-009` |
| `test_taking_context.md` | Ready | `STORY-010`, `STORY-011` |
| `results_context.md` | Ready | `STORY-012` |
| `editor_context.md` | Ready | `STORY-013` |
| `history_analytics_review_context.md` | Ready | `STORY-014`, `STORY-015` |
| `dialog_context.md` | Missing | `STORY-015` |
| `visual_foundation_decisions.md` | Placeholder | `STORY-004` through `STORY-017` |

## Research Task Status

| Task | Status | Output | Assignment Gate |
| --- | --- | --- | --- |
| `R-001_baseline_visual_audit.md` | Blocked | `baseline_visual_audit.md` | None (GUI capture blocked: `python3 main.py` stops after font-registry startup noise and a minimal `tkinter.Tk()` probe also exits `-1` before window creation) |
| `R-002_component_style_inventory.md` | Done | `style_inventory.md` | None |
| `R-003_home_screen_context.md` | Done | `home_screen_context.md` | R-002 Done |
| `R-004_test_taking_context.md` | Done | `test_taking_context.md` | R-002 Done |
| `R-005_results_context.md` | Done | `results_context.md` | R-002 Done |
| `R-006_editor_context.md` | Done | `editor_context.md` | R-002 Done |
| `R-007_history_analytics_review_context.md` | Done | `history_analytics_review_context.md` | R-002 Done |
| `R-008_dialog_context.md` | Blocked | `dialog_context.md` | R-001 Done |

## Story Status

| Story | Status | Blocked By |
| --- | --- | --- |
| `STORY-001_context_batch_one.md` | Submitted For Review | None |
| `STORY-002_baseline_visual_audit.md` | Blocked | R-001 GUI capture environment |
| `STORY-003_visual_foundation_spec.md` | Blocked | CTX-AUDIT-BASELINE |
| `STORY-004_shared_style_entrypoints.md` | Blocked | CTX-FOUNDATION |
| `STORY-005_button_hierarchy.md` | Blocked | CTX-FOUNDATION |
| `STORY-006_card_and_list_patterns.md` | Blocked | CTX-FOUNDATION, named pilot area |
| `STORY-007_page_header_pattern.md` | Blocked | CTX-FOUNDATION |
| `STORY-008_home_screen_layout.md` | Blocked | CTX-FOUNDATION |
| `STORY-009_home_test_cards_and_actions.md` | Blocked | CTX-FOUNDATION |
| `STORY-010_test_taking_shell.md` | Blocked | CTX-TEST-TAKING, CTX-FOUNDATION |
| `STORY-011_answer_rows_and_practice_feedback.md` | Blocked | CTX-TEST-TAKING, CTX-FOUNDATION |
| `STORY-012_results_summary_and_review_cards.md` | Blocked | CTX-FOUNDATION |
| `STORY-013_editor_layout.md` | Blocked | CTX-FOUNDATION |
| `STORY-014_history_and_analytics_polish.md` | Blocked | CTX-FOUNDATION, story split |
| `STORY-015_review_and_dialog_polish.md` | Blocked | CTX-DIALOGS, CTX-FOUNDATION, story split |
| `STORY-016_light_dark_and_min_size_validation.md` | Blocked | Core MVP screen stories |
| `STORY-017_mvp_visual_regression_pass.md` | Blocked | Sprint 4 validation |

## Next Recommended Work

1. Complete `R-001_baseline_visual_audit.md` on a GUI-capable runner to produce
   missing light/dark baseline screenshots.
2. Review completed screen-specific context summaries as needed for sprint
   planning; R-003 through R-007 are now Done.
3. Review `baseline_visual_audit.md` against the Definition of Ready.
4. Use `baseline_visual_audit.md` and `style_inventory.md` to unblock
   `STORY-003_visual_foundation_spec.md`.
