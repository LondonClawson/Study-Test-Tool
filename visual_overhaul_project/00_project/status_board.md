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
| `gui_architecture_summary.md` | Ready | Most stories |
| `screen_inventory.md` | Ready | Most stories |
| `current_visual_state_seed.md` | Seeded | Sprint 0 research |
| `baseline_visual_audit.md` | Ready | `STORY-003`, validation stories; 42 scripted light/dark screenshots validate, with remaining uncaptured states documented |
| `style_inventory.md` | Ready | `STORY-003`, `STORY-004` |
| `home_screen_context.md` | Ready | `STORY-008`, `STORY-009` |
| `test_taking_context.md` | Ready | `STORY-010`, `STORY-011` |
| `results_context.md` | Ready | `STORY-012` |
| `editor_context.md` | Ready | `STORY-013` |
| `history_analytics_review_context.md` | Ready | `STORY-014`, `STORY-015A` |
| `dialog_context.md` | Ready | `STORY-015B`, `STORY-015C`, `STORY-015D`, `STORY-015E` |
| `visual_foundation_decisions.md` | Ready | `STORY-004` through `STORY-017`; accepted for MVP implementation sequencing |

## Research Task Status

| Task | Status | Output | Assignment Gate |
| --- | --- | --- | --- |
| `R-001_baseline_visual_audit.md` | Done | `baseline_visual_audit.md` | None |
| `R-002_component_style_inventory.md` | Done | `style_inventory.md` | None |
| `R-003_home_screen_context.md` | Done | `home_screen_context.md` | R-002 Done |
| `R-004_test_taking_context.md` | Done | `test_taking_context.md` | R-002 Done |
| `R-005_results_context.md` | Done | `results_context.md` | R-002 Done |
| `R-006_editor_context.md` | Done | `editor_context.md` | R-002 Done |
| `R-007_history_analytics_review_context.md` | Done | `history_analytics_review_context.md` | R-002 Done |
| `R-008_dialog_context.md` | Done | `dialog_context.md` | R-001 Done |

## Story Status

| Story | Status | Blocked By |
| --- | --- | --- |
| `STORY-001_context_batch_one.md` | Done | None |
| `STORY-002_baseline_visual_audit.md` | Done | None |
| `STORY-003_visual_foundation_spec.md` | Done | None |
| `STORY-004_shared_style_entrypoints.md` | Done | None |
| `STORY-005_button_hierarchy.md` | Submitted For Review | None |
| `STORY-006_card_and_list_patterns.md` | Blocked | named pilot area |
| `STORY-007_page_header_pattern.md` | Blocked | named pilot screen/path |
| `STORY-008_home_screen_layout.md` | Blocked | `STORY-005` |
| `STORY-009_home_test_cards_and_actions.md` | Blocked | `STORY-006`, `STORY-008` |
| `STORY-010_test_taking_shell.md` | Blocked | `STORY-005` |
| `STORY-011_answer_rows_and_practice_feedback.md` | Blocked | `STORY-010` |
| `STORY-012_results_summary_and_review_cards.md` | Blocked | `STORY-006` or shared card/badge entry points |
| `STORY-013_editor_layout.md` | Blocked | Foundation implementation stories |
| `STORY-014_history_and_analytics_polish.md` | Blocked | Foundation implementation stories, story split |
| `STORY-015_review_and_dialog_polish.md` | Done | split into child stories |
| `STORY-015A_review_screen_polish.md` | Blocked | `STORY-005`, `STORY-006`, `STORY-007` |
| `STORY-015B_mode_dialog_polish.md` | Blocked | `STORY-005` |
| `STORY-015C_mix_dialog_polish.md` | Blocked | `STORY-005`, list/card pattern guidance |
| `STORY-015D_import_preview_dialog_polish.md` | Blocked | `STORY-005`, list/card pattern guidance |
| `STORY-015E_native_dialog_inventory_followup.md` | Blocked | PM post-MVP decision |
| `STORY-016_light_dark_and_min_size_validation.md` | Blocked | Core MVP screen stories |
| `STORY-017_mvp_visual_regression_pass.md` | Blocked | Sprint 4 validation |

## Next Recommended Work

1. Review `STORY-005_button_hierarchy.md` for acceptance.
2. After `STORY-005` is Done, select a named pilot area for
   `STORY-006_card_and_list_patterns.md`.
3. Keep `STORY-015` child stories blocked until the named foundation
   implementation stories land.
