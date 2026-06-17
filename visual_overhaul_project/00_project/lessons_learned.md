# Lessons Learned

Date: 2026-06-17.

This retrospective records process lessons from the Study Testing Tool visual
overhaul. It is meant for future agent-led projects where a developer and PM or
reviewer work in parallel.

## Executive Summary

The project worked because it treated documentation as operating infrastructure,
not as a passive record. The best artifacts made the next action obvious:
status board, dependency map, context summaries, assignment packets, handoffs,
review notes, screenshot evidence, and closeout classification.

The biggest improvement for future projects is to start with the mature version
of that system on day one. Some of the strongest practices, especially
assignment packets, strict evidence review, post-MVP classification, and quiet
PM polling intervals, became clear only after the project had already produced
friction.

## What Worked Well

### One Fast Source Of Truth

`00_project/status_board.md` was the right front door. It let the PM quickly
answer:

- What is Done?
- What is Ready?
- What is Blocked?
- What is Submitted For Review?
- What should happen next?

The board was most effective when it was paired with the owning story and
handoff. The board alone should summarize state; the story and handoff should
carry scope, evidence, and verification detail.

### Explicit Status Transitions

The status vocabulary helped prevent ambiguous progress claims. `Ready`,
`In Progress`, `Submitted For Review`, `Changes Requested`, `Blocked`, and
`Done` each carried a different operational meaning.

The important lesson is that a status change is a project-management event, not
an incidental file edit. Future projects should keep the rule that status
changes update the board, owning story, and handoff together.

### Research Before Implementation

The two-agent pipeline was useful:

1. Research agent writes bounded context.
2. PM or reviewer accepts the context.
3. Developer implements from the story plus accepted context.

This reduced broad rediscovery and kept implementation stories from becoming
open-ended exploration. It worked best when context summaries named specific
files, workflows, visual states, behavior constraints, and risks.

### Narrow Stories And Late Splits

Splitting broad parent stories into child stories was a good call. The work
became easier to assign, review, and accept when each story was one screen, one
dialog, or one component family.

For future projects, do this earlier. Parent stories can remain as planning
containers, but implementation should happen through small child stories from
the beginning.

### Assignment Packets

Assignment packets were valuable because they gave the developer a task-specific
contract:

- read these files first;
- do this;
- do not do this;
- produce this handoff;
- run these checks.

They worked especially well for validation and closeout stories because they
kept the developer from turning review work into an unbounded fix-it pass.

### Handoffs And Review Notes

The handoff/review split worked well. Developer handoffs documented what was
done and what evidence was provided. PM review notes documented whether that
evidence was accepted, rejected, or accepted with follow-up classification.

This created an audit trail that was useful at closeout. The PM could inspect
the chain of evidence instead of relying on memory.

### Screenshot Evidence As A Quality Gate

The screenshot harness was one of the strongest quality tools in the project.
It made visual review concrete, repeatable, and comparable across light mode,
dark mode, and minimum-size states.

The best evidence had three qualities:

- named screen states;
- light/dark coverage where relevant;
- validation commands and counts.

Manual visual impressions were not enough by themselves. They became defensible
only when tied to screenshot paths, harness states, and acceptance criteria.

### Critical PM Review

The project benefited when the PM stayed critical and asked whether evidence was
strong enough, not just whether a developer said a story was complete.

Changes-requested moments were useful. They improved the final result by making
the developer fix acceptance gaps such as missing minimum-window evidence,
retake-state behavior, or contaminated screenshots.

### Post-MVP Classification

The final closeout was stronger because remaining issues were classified as:

- MVP blocker;
- post-MVP follow-up;
- accepted limitation.

This prevented two failure modes: shipping with hidden known issues, and
reopening completed MVP scope for every non-critical imperfection.

## What Did Not Work As Well

### Some Documentation Matured Too Late

The project documentation improved over time, but some useful artifacts appeared
after the team had already felt their absence. Assignment packets, review notes,
and final classification language should exist from the start in future
projects.

### Early Stories Were Sometimes Too Broad

Broad parent stories were useful for planning, but not for assignment. Stories
that covered multiple unrelated screens created unnecessary PM decisions during
implementation. Splitting helped, but future projects should split earlier.

### Evidence Gaps Appeared Late

The closeout found representative coverage, not exhaustive long-content stress
coverage. That was acceptable for MVP, but it should have been called out as a
known validation dimension earlier.

Future screenshot harnesses should include stress fixtures from the beginning:
long names, long descriptions, long prompts, long answers, dense lists, and
larger dialogs.

### Status Drift Was A Constant Risk

The board, story files, and handoffs could diverge if they were not updated
together. This was manageable, but it required repeated PM discipline.

Future projects should consider a lightweight checklist in every review:

- board status updated;
- owning story status updated;
- handoff status updated;
- Next Recommended Work updated;
- acceptance or changes-request note added.

### PM Polling Needed Restraint

The PM role worked best when it checked the board after meaningful intervals
instead of constantly rereading context while the developer was actively
working.

The better pattern is:

1. assign the task clearly;
2. wait unless the developer asks for input;
3. check the board after a quiet interval;
4. review only if something is submitted or blocked.

This reduces context churn and avoids interrupting active implementation.

### Native Dialog Decisions Should Happen Earlier

Native messageboxes and file dialogs became an explicit accepted MVP limitation
late in the project. That decision was reasonable, but future projects should
classify platform-native exceptions earlier so developers do not waste time
guessing whether they are blockers.

## Documentation Style Lessons

### Good Documentation Is Operational

The best project docs did not explain the project in broad terms. They told the
next agent what to do next, what not to do, and how completion would be judged.

Future docs should prefer:

- exact file paths;
- exact screen states;
- exact commands;
- named dependencies;
- explicit in-scope and out-of-scope bullets;
- observable acceptance criteria.

Avoid vague phrases like "make polished", "improve UI", or "review quality"
unless they are paired with concrete evidence requirements.

### Keep Files Small And Purpose-Specific

The directory split worked:

- `00_project/` for operating rules and governance;
- `01_context/` for reusable research summaries;
- `03_backlog/` for sequencing and acceptance;
- `04_stories/` for assignable work;
- `06_handoffs/` for completion and review evidence.

This made it possible for an agent to read only the needed layer instead of the
entire project every time.

### Handoffs Need Evidence, Not Narration

A good handoff should answer:

- What changed?
- What files changed?
- What states were checked?
- What evidence proves it?
- What tests ran?
- What risks remain?
- What should happen next?

Long explanations were less useful than precise evidence and clear residual
risk classification.

### Reviews Should Lead With Acceptance Or Required Changes

PM review notes should state the decision first, then evidence. The useful
shape was:

- accepted, changes requested, or blocked;
- evidence reviewed;
- verification performed;
- acceptance notes;
- risks and follow-ups.

This kept review notes actionable instead of becoming another progress report.

## Developer And PM Collaboration Lessons

### The Parallel Model Worked

Parallel developer and PM work was effective when the developer owned the active
story and the PM owned the board, quality gate, scope decisions, and acceptance.

The PM should not micromanage an `In Progress` story. The PM should intervene
when:

- the developer asks for input;
- work is submitted for review;
- evidence reveals a quality gap;
- a blocker is real and needs a decision;
- project documentation needs clarification independent of active coding.

### The PM Must Be Willing To Say No

Quality improved when PM acceptance was not automatic. Accepting a story should
mean the evidence is strong enough, not that the implementation looks plausible.

Future PMs should be explicit about confidence level and should request changes
when evidence is missing, screenshots are weak, behavior checks are absent, or
scope has drifted.

### Developers Need Clear Stop Conditions

Developers moved better when stories said what completion looked like and when
not to continue. Validation stories in particular need stop conditions so the
developer reports findings instead of starting broad redesign.

### Product Decisions Should Be Documented Where They Are Made

The `STORY-015E` native-dialog decision was useful because it turned an
ambiguous visual mismatch into an accepted MVP limitation. Future projects
should record product decisions immediately in the story, board, and handoff.

## Recommended Future Project Setup

Before assigning implementation work, create these artifacts:

1. `status_board.md` with status vocabulary and Next Recommended Work.
2. `status_transition_rules.md`.
3. `definition_of_ready.md`.
4. `definition_of_done.md`.
5. `screenshot_evidence_policy.md` or equivalent evidence policy.
6. `dependency_map.md`.
7. `acceptance_matrix.md`.
8. `assignment_packet_template.md`.
9. `handoff_template.md`.
10. `review_checklist.md`.
11. A closeout story with blocker/follow-up/accepted-limitation categories.
12. A post-MVP recommendation queue.

For visual projects, also create the screenshot harness early and expand it with
each story. Do not wait until closeout to discover that important states are not
capturable.

## Future Operating Rules

- Assign one narrow story at a time.
- Require accepted context before implementation.
- Keep parent stories as containers; assign child stories.
- Use assignment packets for every implementation, validation, and closeout
  story.
- Treat screenshot evidence as a first-class deliverable for visual work.
- Run focused tests for touched behavior and full tests at closeout.
- Update board, story, and handoff together on every status transition.
- PM should wait during active work and review only on submission, blocker, or
  explicit request.
- PM acceptance should document evidence reviewed and verification performed.
- Close every project with explicit MVP blockers, post-MVP follow-ups, and
  accepted limitations.

## What I Would Do Differently Next Time

Start with the final operating model. In this project, the system became strong
as we used it. Next time, create the stronger system before implementation:
assignment packets from the first story, screenshot stress fixtures from the
first harness pass, explicit post-MVP classification from the first validation
story, and a PM polling rhythm that gives developers quiet work windows.

The core project result was good. The process lesson is that agent-led projects
need tighter upfront operating rules than human-only projects because each agent
turn may have limited context. Clear artifacts are not overhead in that model;
they are the mechanism that keeps quality and momentum aligned.

## Developer Perspective Addendum

This section records the developer-side lessons from the same project. It is
intentionally narrower than the PM retrospective above: the focus is what made
implementation easier, what made it riskier, and what a future developer agent
would need on day one.

### What Helped The Developer Most

The strongest implementation support came from having durable project docs that
could survive chat context loss. The developer could recover state by reading
the status board, transition rules, context index, current story, assignment
packet, and handoff history. That mattered because the project lasted across
many turns and had multiple PM decisions.

The most useful developer inputs were:

- a single fast status board;
- clear role rules saying the developer submits and the PM marks Done;
- accepted context summaries before implementation;
- story files with exact scope and out-of-scope boundaries;
- assignment packets that named what to read first;
- screenshot policy and repeatable harness commands;
- handoff templates with evidence and test expectations;
- PM review notes that explained acceptance or changes requested.

The developer work became much safer once the rule was explicit: `Submitted For
Review` is not Done. That prevented premature closure and made waiting for PM
acceptance part of the workflow instead of a special case.

### What Made Implementation Harder

The hardest part was not the app code. It was keeping the project record
coherent while many documents changed in parallel. A normal implementation task
often required checking or updating the board, story file, handoff, screenshot
folder, acceptance matrix, and sometimes PM review notes. That audit trail was
valuable, but the coordination overhead was real.

The second source of friction was broad or qualitative story language. A
developer can implement "make the screen polished" only after the PM or context
docs translate that into named states, expected hierarchy, screenshots, and
tests. Future projects should not assign broad polish stories until that
translation is complete.

The third issue was evidence arriving incrementally. The screenshot harness
became excellent, but some fixtures were added only when needed. That left final
closeout with representative evidence rather than full stress coverage for long
user-authored text.

### Developer/PM Collaboration Lessons

The two-agent model worked when each side had a different job:

- The PM owned priority, readiness, acceptance, and scope decisions.
- The developer owned implementation, evidence collection, focused tests,
  handoff writing, and commits.

The model was weakest when the developer had to infer PM intent from scattered
notes. It was strongest when the PM created a current assignment packet with
"do this", "do not do this", expected evidence, and required verification.

Waiting after submission was also important. If the board had no ready developer
work, the right behavior was to sleep, re-check the tracker, and continue only
after PM action. That kept the developer from inventing scope.

### Screenshot And Verification Lessons

For a visual project, the screenshot harness should be treated like a test
suite. The developer needs named states, stable seed data, validation-only
commands, and expected screenshot counts. The final closeout was credible
because it could cite both baseline and after evidence with validation counts.

Focused tests were the right default during visual implementation. Running the
full test suite on every visual-only change would have slowed the project down,
but running the relevant service/session/review/analytics tests protected
behavior. The full suite belonged at closeout, where it proved there was no
known core behavior regression.

### Documentation Improvements For Future Developers

Future projects should add these before implementation starts:

- `active_assignment.md`: one PM-owned file for the current developer task.
- Tracker consistency check: board status, story status, handoff status, and
  review status should agree.
- Screenshot manifest check: expected states and counts per story.
- Long-content stress fixtures from the first screenshot harness pass.
- A source-of-truth order that identifies stale docs explicitly.
- A commit policy: developer commits submitted packages; PM commits acceptance
  or changes-requested decisions.

### Developer Rules To Keep

- Read the tracker before claiming work.
- Do not claim blocked or stale work.
- Make the smallest scoped change that satisfies the story.
- Preserve existing app behavior unless the story explicitly changes it.
- Collect screenshot evidence for visual changes.
- Run focused tests for touched behavior.
- Use `git diff --check` before submitting.
- Commit submitted packages.
- Never mark developer work Done.
- If no work is available after submission, wait and re-check the tracker.

### Developer Bottom Line

The process worked because the project treated documentation as part of the
runtime for agent collaboration. The developer could move quickly only when the
docs were precise enough to answer scope, evidence, and acceptance questions
without another chat round. Future projects should preserve that rigor while
reducing friction through smaller stories, one active assignment file, and
automated checks for tracker and screenshot consistency.
