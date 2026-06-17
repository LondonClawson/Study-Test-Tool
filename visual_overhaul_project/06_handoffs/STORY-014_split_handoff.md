# STORY-014 Split Handoff

Story/Task:
`STORY-014_history_and_analytics_polish.md`

Status:
Done. Parent story split by PM on 2026-06-16.

Summary:
Split the broad history/analytics polish placeholder into three narrow child
stories: History list and filters, Analytics chart shell, and Analytics weak
topics/no-data states. The parent story should not be assigned for
implementation. While updating the dependency map, also normalized the existing
`STORY-015` split rows so the map points developers at child stories instead of
the broad parent.

Files changed:
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/03_backlog/backlog_index.md`
- `visual_overhaul_project/03_backlog/dependency_map.md`
- `visual_overhaul_project/04_stories/STORY-014_history_and_analytics_polish.md`
- `visual_overhaul_project/04_stories/STORY-014A_history_list_and_filters.md`
- `visual_overhaul_project/04_stories/STORY-014B_analytics_chart_shell.md`
- `visual_overhaul_project/04_stories/STORY-014C_analytics_weak_topics_and_no_data.md`
- `visual_overhaul_project/06_handoffs/STORY-014_split_handoff.md`

Definition of Ready checked:
Yes. Each child story names required context, narrow scope, likely files,
behavior constraints, observable acceptance criteria, screenshot evidence
requirements, smoke checks, and test expectations.

Context summaries read:
- `visual_overhaul_project/01_context/summaries/history_analytics_review_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`

Context summaries created/updated:
None.

Screens/states checked:
Static PM documentation review only. Child stories name the runtime states Dev 2
must verify.

Screenshot evidence:
Not applicable for this PM split. Child stories require after evidence under:
- `visual_overhaul_project/01_context/screenshots/after/STORY-014A/`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014B/`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014C/`

Tests run:
`git diff --check`.

Tests not run and why:
Pytest was not run because this is PM documentation and tracker work only. No
application code changed.

Acceptance criteria notes:
The parent `STORY-014` is no longer a large implementation assignment. History,
analytics chart shell, and analytics weak-topic/no-data work now have separate
scoped story files and are Ready on the status board.

Risks:
The screenshot harness currently exposes `history_populated`,
`history_empty_state`, `analytics_populated`, and `analytics_no_data`, but may
not land on every analytics tab or weak-topic grouping state. Child story
handoffs must either include manual evidence for those states or document the
exact capture blocker.

Follow-up backlog items:
None. Keep the new child stories behind active `STORY-013` unless additional
capacity opens.
