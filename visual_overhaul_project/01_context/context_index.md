# Context Index

Use this index to find the summary required by a story. If a story needs context
that is not represented here, create a research task or add the missing summary
before implementation.

Only mark a summary Ready after it passes
`00_project/definition_of_ready.md`.

Status terms match `00_project/status_board.md`: Missing, Placeholder, Seeded,
Ready, In Progress, Submitted For Review, Blocked, Done, and Stale.

| Context ID | Summary | Source Scope | Status | Refresh Trigger | Research Task |
| --- | --- | --- | --- | --- | --- |
| CTX-GUI-ARCH | `summaries/gui_architecture_summary.md` | `main_window.py`, screen constants, GUI file inventory | Ready | Any navigation, screen registration, or frame lifecycle change | `02_research_tasks/R-002_component_style_inventory.md` |
| CTX-SCREEN-INV | `summaries/screen_inventory.md` | Major GUI screens and components | Ready | New screen/component or renamed GUI file | `02_research_tasks/R-002_component_style_inventory.md` |
| CTX-VISUAL-SEED | `summaries/current_visual_state_seed.md` | Early static visual read of GUI code and visual plan; superseded for implementation planning by CTX-AUDIT-BASELINE and CTX-FOUNDATION | Seeded | Major style refactor or contradiction with accepted audit/foundation context | `02_research_tasks/R-001_baseline_visual_audit.md` |
| CTX-AUDIT-BASELINE | `summaries/baseline_visual_audit.md` | 42 validated scripted light/dark baseline screenshots of major screens, custom dialogs, test-taking variants, data views, and empty states; remaining uncaptured states are documented | Ready | Refresh if screenshots or source UI change before implementation comparison | `02_research_tasks/R-001_baseline_visual_audit.md` |
| CTX-STYLE-INVENTORY | `summaries/style_inventory.md` | Inline colors, fonts, widgets, repeated surfaces | Ready | Required before visual foundation spec | `02_research_tasks/R-002_component_style_inventory.md` |
| CTX-HOME | `summaries/home_screen_context.md` | Home/test selector, groups, cards, dialogs launched from home | Ready | Home layout, card data, action set, grouping, archive behavior, or import/mix launch flow changes | `02_research_tasks/R-003_home_screen_context.md` |
| CTX-TEST-TAKING | `summaries/test_taking_context.md` | Test-taking screen, question widget, timer, progress, practice feedback | Ready | Test-taking shell, question widget, timer, progress, practice feedback, session behavior, scoring handoff, or foundation token changes | `02_research_tasks/R-004_test_taking_context.md` |
| CTX-RESULTS | `summaries/results_context.md` | Results view, score summary, review cards, mix breakdown | Ready | Results view, scoring handoff, history result navigation, mix source attribution, or foundation token changes | `02_research_tasks/R-005_results_context.md` |
| CTX-EDITOR | `summaries/editor_context.md` | Test editor layout, question list, form states | Ready | Editor layout, question list, form state, option row, group autocomplete, validation, or foundation token changes | `02_research_tasks/R-006_editor_context.md` |
| CTX-DATA-VIEWS | `summaries/history_analytics_review_context.md` | History, analytics, review, charts, data states | Ready | Required before secondary screen stories | `02_research_tasks/R-007_history_analytics_review_context.md` |
| CTX-DIALOGS | `summaries/dialog_context.md` | Mode, mix, import/error/confirmation dialogs | Ready | Required before dialog polish; refresh if custom dialog styling, import preview behavior, messagebox usage, or file dialog flows change | `02_research_tasks/R-008_dialog_context.md` |
| CTX-FOUNDATION | `summaries/visual_foundation_decisions.md` | Accepted MVP visual tokens and component rules | Ready | Refresh if implementation discovers incomplete rules or PM changes foundation decisions | `04_stories/STORY-003_visual_foundation_spec.md` |
