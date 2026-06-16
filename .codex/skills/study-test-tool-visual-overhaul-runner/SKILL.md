---
name: study-test-tool-visual-overhaul-runner
description: Use when the user asks to advance, choose, complete, hand off, update, or automate a task in this repository's visual_overhaul_project workflow. This skill is specific to Study-Test-Tool and its visual overhaul tracker, research tasks, stories, context summaries, status board, and handoff process.
---

# Study-Test-Tool Visual Overhaul Runner

Use this skill to advance exactly one safe unit of work in
`visual_overhaul_project/` while preserving the tracker/handoff process. By
default, act as the assigned agent, not as reviewer or PM, unless the user
explicitly asks for review, acceptance, or PM status changes.

## Core Workflow

1. Read the tracker sources before choosing work:
   - `visual_overhaul_project/00_project/status_board.md`
   - `visual_overhaul_project/00_project/status_transition_rules.md`
   - `visual_overhaul_project/00_project/definition_of_ready.md`
   - `visual_overhaul_project/00_project/screenshot_evidence_policy.md`
   - `visual_overhaul_project/01_context/context_index.md`
   - Relevant task, story, summary, and handoff files.
2. Pick one safe task:
   - Prefer Ready research or tracker-cleanup tasks that can be completed from
     existing code/docs.
   - Avoid GUI screenshot work if Tk/CustomTkinter is blocked in the current
     shell.
   - Avoid implementation stories unless every required context summary is
     Ready and the story itself is Ready.
3. State the chosen task and why.
4. Mark the task `In Progress` before doing the scoped work.
5. Complete only the selected task's scope.
6. Create or update the handoff in `visual_overhaul_project/06_handoffs/`.
7. Mark the final task status according to `status_transition_rules.md`. For
   agent-completed research tasks and implementation stories, use
   `Submitted For Review` unless the user explicitly asked you to act as the
   reviewer/PM or accept completed work.
8. Update `status_board.md`, `context_index.md`, and the task/story file when
   required by the transition rules.
9. If "Next Recommended Work" names the completed task, update that note.
10. Run `git diff --check`.

## Selection Rules

- Treat `status_board.md` as the fast source of truth, then confirm against the
  owning task/story file and `context_index.md`.
- If multiple tasks are Ready, choose the smallest one that unblocks later work
  or removes stale tracker state.
- Do not choose `R-001_baseline_visual_audit.md` unless a GUI-capable runtime is
  available for baseline screenshots.
- Do not choose `R-008_dialog_context.md` while it is blocked on R-001.
- Do not start blocked stories by bypassing missing `CTX-FOUNDATION`,
  `CTX-AUDIT-BASELINE`, or `CTX-DIALOGS`.

## Handoff Requirements

Use `visual_overhaul_project/06_handoffs/handoff_template.md` for every completed
or blocked task. Keep the handoff factual and include:

- Task/story name and submitted, blocked, or accepted status.
- Summary of completed work.
- Files changed.
- Definition of Ready or acceptance notes.
- Context summaries read or updated.
- Screens/states checked.
- Screenshot evidence or capture blocker, following
  `visual_overhaul_project/00_project/screenshot_evidence_policy.md`.
- Tests run, or why tests were not run.
- Risks and follow-up backlog items.

For docs-only tracker work, note that pytest was not run because no application
code changed.

## Guardrails

- Do not change application code for research or tracker-cleanup tasks.
- Do not overwrite unrelated dirty work; inspect `git status --short` before
  editing and keep changes scoped.
- Preserve the project's status vocabulary: Missing, Placeholder, Seeded, Ready,
  In Progress, Submitted For Review, Blocked, Done, and Stale.
- Preserve the two-agent flow unless the user explicitly asks to collapse it:
  Dev 1 research produces summaries and handoffs; reviewer/PM marks summaries
  Ready or tasks Done.
- Do not mark research tasks or stories `Done` unless the user explicitly asked
  you to review or accept completed work, or the current task is clearly a
  reviewer/PM acceptance pass.
- If a task cannot be completed because required runtime states, screenshots, or
  product decisions are unavailable, mark it Blocked and document the blocker in
  the handoff and tracker.

## Final Response

Report:

- The task chosen and submitted/proposed status, including whether reviewer/PM
  acceptance is still required.
- The tracker and handoff files changed.
- Verification performed, especially `git diff --check`.
- Tests not run and why.
