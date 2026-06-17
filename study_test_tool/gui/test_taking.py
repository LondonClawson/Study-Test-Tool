"""Test-taking screen — the core test experience."""

import tkinter.messagebox as messagebox
from typing import List, Optional

import customtkinter as ctk
from gui.components.progress_bar import ProgressBar
from gui.components.question_widget import QuestionWidget
from gui.components.timer_widget import TimerWidget
from gui.styles import (
    RADIUS_CARD,
    RADIUS_CONTROL,
    SPACE_4,
    SPACE_8,
    SPACE_12,
    SPACE_16,
    SPACE_24,
    get_button_style,
    get_card_style,
    get_color,
    get_header_style,
    get_text_style,
)
from services.question_service import QuestionService
from services.review_service import ReviewService
from services.scoring_service import ScoringService
from services.test_service import TestService
from services.test_session import TestSession
from utils.constants import MODE_PRACTICE, MODE_TEST, SCREEN_HOME, SCREEN_RESULTS


class TestTakingFrame(ctk.CTkFrame):
    """Screen for taking a test with timer, navigation, and flagging."""

    def __init__(self, parent: ctk.CTkFrame, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.test_service = TestService()
        self.question_service = QuestionService()
        self.scoring_service = ScoringService()
        self.review_service = ReviewService()

        self._session: Optional[TestSession] = None
        self._question_widget: Optional[QuestionWidget] = None
        self._progress_bar: Optional[ProgressBar] = None
        self._mode: str = MODE_TEST
        self._feedback_frame: Optional[ctk.CTkFrame] = None
        self._is_mix_test: bool = False

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the test-taking layout."""
        self.configure(fg_color=get_color("app_bg"))

        # Top bar
        self.top_frame = ctk.CTkFrame(self, **get_header_style("page"))
        self.top_frame.pack(fill="x", padx=SPACE_24, pady=(SPACE_24, SPACE_12))
        self.top_frame.grid_columnconfigure(0, weight=1)

        title_frame = ctk.CTkFrame(self.top_frame, fg_color="transparent")
        title_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=SPACE_24,
            pady=(SPACE_16, SPACE_16),
        )

        self.test_name_label = ctk.CTkLabel(
            title_frame,
            text="",
            anchor="w",
            wraplength=470,
            justify="left",
            **get_text_style("page_title"),
        )
        self.test_name_label.pack(fill="x", anchor="w")

        self.mix_subtitle_label = ctk.CTkLabel(
            title_frame,
            text="",
            anchor="w",
            wraplength=470,
            justify="left",
            **get_text_style("metadata"),
        )
        self.mix_subtitle_label.pack(fill="x", anchor="w", pady=(SPACE_4, 0))

        status_frame = ctk.CTkFrame(self.top_frame, fg_color="transparent")
        status_frame.grid(
            row=0,
            column=1,
            sticky="e",
            padx=(SPACE_8, SPACE_24),
            pady=(SPACE_16, SPACE_16),
        )
        status_frame.grid_columnconfigure((0, 1), weight=1)

        self.timer_widget = TimerWidget(
            status_frame,
            fg_color=get_color("surface_subtle"),
            text_color=get_color("text_primary"),
            corner_radius=RADIUS_CONTROL,
        )
        self.timer_widget.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, SPACE_8),
            pady=(0, SPACE_8),
        )

        # Progress text
        self.progress_label = ctk.CTkLabel(
            status_frame,
            text="",
            fg_color=get_color("surface_subtle"),
            corner_radius=RADIUS_CONTROL,
            **get_text_style("body"),
        )
        self.progress_label.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(0, 0),
            pady=(0, SPACE_8),
        )

        # Flag button
        self.flag_btn = ctk.CTkButton(
            status_frame,
            text="Flag",
            width=172,
            height=34,
            command=self._on_flag,
            **get_button_style("tertiary"),
        )
        self.flag_btn.grid(row=1, column=0, columnspan=2, sticky="ew")

        # Center: question area
        self.question_area = ctk.CTkScrollableFrame(
            self,
            fg_color=get_color("surface_subtle"),
            border_color=get_color("border"),
            border_width=1,
            corner_radius=RADIUS_CARD,
            scrollbar_button_color=get_color("secondary"),
            scrollbar_button_hover_color=get_color("secondary_hover"),
        )
        self.question_area.pack(
            fill="both",
            expand=True,
            padx=SPACE_24,
            pady=(0, SPACE_12),
        )

        # Bottom: nav buttons + progress bar
        bottom_frame = ctk.CTkFrame(
            self,
            fg_color=get_color("surface"),
            border_color=get_color("border"),
            border_width=1,
            corner_radius=RADIUS_CARD,
        )
        bottom_frame.pack(fill="x", padx=SPACE_24, pady=(0, SPACE_24))

        # Progress bar container
        self.progress_container = ctk.CTkFrame(
            bottom_frame,
            fg_color=get_color("surface_subtle"),
            corner_radius=RADIUS_CONTROL,
        )
        self.progress_container.pack(
            fill="x",
            padx=SPACE_16,
            pady=(SPACE_16, SPACE_8),
        )

        nav_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        nav_frame.pack(fill="x", padx=SPACE_16, pady=(SPACE_4, SPACE_16))

        navigation_actions = ctk.CTkFrame(nav_frame, fg_color="transparent")
        navigation_actions.pack(side="left")

        completion_actions = ctk.CTkFrame(nav_frame, fg_color="transparent")
        completion_actions.pack(side="right")

        self.prev_btn = ctk.CTkButton(
            navigation_actions,
            text="< Previous",
            width=110,
            height=36,
            command=self._on_previous,
            **get_button_style("secondary"),
        )
        self.prev_btn.pack(side="left", padx=(0, SPACE_8))

        self.next_btn = ctk.CTkButton(
            navigation_actions,
            text="Next >",
            width=110,
            height=36,
            command=self._on_next,
            **get_button_style("secondary"),
        )
        self.next_btn.pack(side="left")

        # Check Answer button (practice mode only, hidden by default)
        self.check_btn = ctk.CTkButton(
            completion_actions,
            text="Check Answer",
            width=130,
            height=36,
            command=self._on_check_answer,
            **get_button_style("primary"),
        )
        self.check_btn.grid(row=0, column=0, padx=(0, SPACE_8))
        self.check_btn.grid_remove()

        self.finish_btn = ctk.CTkButton(
            completion_actions,
            text="Finish Test",
            width=130,
            height=36,
            command=self._on_finish,
            **get_button_style("primary"),
        )
        self.finish_btn.grid(row=0, column=1)

    def on_show(
        self,
        test_id: Optional[int] = None,
        mode: str = MODE_TEST,
        review_question_ids: Optional[List[int]] = None,
        questions: Optional[List] = None,
        mix_test_name: Optional[str] = None,
        mix_test_subtitle: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Initialize the test-taking session.

        Args:
            test_id: The test to take.
            mode: "test" or "practice".
            review_question_ids: Specific question IDs for review sessions.
            questions: Pre-selected questions (for mix tests).
            mix_test_name: Display name for mix tests.
            mix_test_subtitle: Scope summary for mix tests.
        """
        self._mode = mode

        # Configure UI for mode
        if mode == MODE_PRACTICE:
            self.check_btn.grid()
            self._enable_check_answer()
            self.finish_btn.configure(text="Finish Practice")
        else:
            self.check_btn.grid_remove()
            self.finish_btn.configure(text="Finish Test")

        # Mix test: questions already provided
        if questions is not None:
            self._is_mix_test = True
            self.test_name_label.configure(
                text=mix_test_name if mix_test_name else "Mix Test"
            )
            self.mix_subtitle_label.configure(text=mix_test_subtitle or "")
            self._session = TestSession(
                None,
                questions,
                mode=mode,
                mix_name=mix_test_name,
                mix_subtitle=mix_test_subtitle,
            )
        elif review_question_ids:
            self._is_mix_test = False
            self.mix_subtitle_label.configure(text="")
            loaded = self._load_review_questions(review_question_ids)
            if not loaded:
                messagebox.showwarning(
                    "No Questions", "Could not load review questions."
                )
                self.controller.show_frame(SCREEN_HOME)
                return
            # Use the test_id from the first question if not provided
            if test_id is None:
                test_id = loaded[0].test_id
            self.test_name_label.configure(text="Review Session")
            self._session = TestSession(test_id, loaded, mode=mode)
        else:
            self._is_mix_test = False
            self.mix_subtitle_label.configure(text="")
            if test_id is None:
                return

            test = self.test_service.get_test_by_id(test_id)
            if not test:
                messagebox.showerror("Error", "Test not found.")
                self.controller.show_frame(SCREEN_HOME)
                return

            loaded = self.question_service.get_questions_for_test(
                test_id, randomize=True
            )
            if not loaded:
                messagebox.showwarning("No Questions", "This test has no questions.")
                self.controller.show_frame(SCREEN_HOME)
                return

            self.test_name_label.configure(text=test.name)
            self._session = TestSession(test_id, loaded, mode=mode)

        self._session.start()

        # Rebuild progress bar
        for widget in self.progress_container.winfo_children():
            widget.destroy()

        self._progress_bar = ProgressBar(
            self.progress_container,
            total=len(self._session.questions),
            on_click=self._on_progress_click,
        )
        self._progress_bar.pack(anchor="center", pady=SPACE_8)

        self.timer_widget.start()
        self._display_question()

    def _load_review_questions(self, question_ids: List[int]):
        """Load specific questions by ID for review sessions."""
        return self.review_service.create_review_session_questions(question_ids)

    def _display_question(self) -> None:
        """Show the current question."""
        if self._session is None:
            return

        question = self._session.get_current_question()
        if question is None:
            return

        # Update progress text
        idx = self._session.current_index
        total = self._session.total_questions
        self.progress_label.configure(text=f"Question {idx + 1} of {total}")

        # Update flag button
        if self._session.is_question_flagged:
            self.flag_btn.configure(text="Unflag", **get_button_style("warning"))
        else:
            self.flag_btn.configure(text="Flag", **get_button_style("tertiary"))

        # Update nav buttons
        self.prev_btn.configure(state="normal" if idx > 0 else "disabled")
        self.next_btn.configure(state="normal" if idx < total - 1 else "disabled")

        # Rebuild question widget
        for widget in self.question_area.winfo_children():
            widget.destroy()
        self._feedback_frame = None

        self._question_widget = QuestionWidget(
            self.question_area,
            question,
            **get_card_style("default"),
        )
        self._question_widget.pack(
            fill="x",
            expand=True,
            padx=SPACE_12,
            pady=SPACE_12,
        )

        # Reset scroll to top for the new question
        self.question_area._parent_canvas.yview_moveto(0.0)

        # Restore saved answer
        saved = self._session.responses.get(question.id)
        if saved:
            self._question_widget.set_answer(saved)

        # In practice mode, re-apply the lock and feedback if this question
        # was already checked.
        if self._mode == MODE_PRACTICE:
            if question.id in self._session.checked_responses:
                checked_answer = self._session.checked_responses[question.id]
                self._question_widget.set_answer(checked_answer)
                is_correct = self.scoring_service.score_question(
                    question, checked_answer if checked_answer else None
                )
                self._question_widget.show_checked_state(
                    question.correct_answer,
                    checked_answer if checked_answer else None,
                    is_correct,
                )
                self._question_widget.disable()
                self._show_feedback(
                    question,
                    checked_answer if checked_answer else None,
                    is_correct,
                )
                self._disable_check_answer()
            else:
                self._enable_check_answer()

        # Update progress bar
        self._update_progress_bar()

    def _save_current_answer(self) -> None:
        """Save the current question's answer to the session."""
        if self._session is None or self._question_widget is None:
            return

        question = self._session.get_current_question()
        if question is None:
            return

        answer = self._question_widget.get_answer()
        self._session.save_response(question.id, answer if answer else "")

    def _update_progress_bar(self) -> None:
        """Update progress bar colors."""
        if self._progress_bar is None or self._session is None:
            return

        question_ids = [q.id for q in self._session.questions]
        answered_ids = set(self._session.responses.keys())
        self._progress_bar.update_status(
            self._session.current_index,
            answered_ids,
            self._session.flagged,
            question_ids,
        )

    def _on_check_answer(self) -> None:
        """Check the current answer (practice mode).

        The first answer the user submits via this button is locked in for
        scoring. The answer widget is then disabled so it cannot be changed.
        """
        if self._session is None or self._question_widget is None:
            return

        question = self._session.get_current_question()
        if question is None:
            return

        # If already checked, do nothing — the answer is locked.
        if question.id in self._session.checked_responses:
            return

        self._save_current_answer()
        user_answer = self._session.responses.get(question.id)

        # Lock the answer for scoring (first-write-wins).
        self._session.save_checked_response(
            question.id, user_answer if user_answer else ""
        )

        is_correct = self.scoring_service.score_question(question, user_answer)
        self._question_widget.show_checked_state(
            question.correct_answer,
            user_answer,
            is_correct,
        )
        self._question_widget.disable()
        self._show_feedback(question, user_answer, is_correct)

        # Visually lock the answer input and disable the Check Answer button.
        self._disable_check_answer()

    def _enable_check_answer(self) -> None:
        """Restore Check Answer to the active primary action style."""
        self.check_btn.configure(state="normal", **get_button_style("primary"))

    def _disable_check_answer(self) -> None:
        """Show Check Answer as unavailable after a practice answer is locked."""
        self.check_btn.configure(
            state="disabled",
            fg_color=get_color("surface_muted"),
            hover_color=get_color("surface_muted"),
            text_color=get_color("text_disabled"),
            border_color=get_color("border"),
            border_width=1,
        )

    def _show_feedback(self, question, user_answer, is_correct) -> None:
        """Display practice feedback below the question widget."""
        # Remove existing feedback if any
        if self._feedback_frame is not None:
            self._feedback_frame.destroy()

        if is_correct is None:
            title = "Essay response"
            message = "Compare your response with the expected answer."
            status_color = get_color("status_neutral")
            title_color = get_color("text_secondary")
        elif is_correct:
            title = "Correct"
            message = "Your answer matches the correct answer."
            status_color = get_color("status_correct")
            title_color = status_color
        else:
            title = "Incorrect"
            message = "Review the correct answer before moving on."
            status_color = get_color("status_incorrect")
            title_color = status_color

        self._feedback_frame = ctk.CTkFrame(
            self.question_area,
            fg_color=get_color("surface"),
            border_color=status_color,
            border_width=1,
            corner_radius=RADIUS_CARD,
        )
        self._feedback_frame.pack(fill="x", padx=SPACE_12, pady=(0, SPACE_12))

        content_frame = ctk.CTkFrame(self._feedback_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=SPACE_16, pady=SPACE_12)

        ctk.CTkLabel(
            content_frame,
            text=title,
            anchor="w",
            **self._feedback_text_style("section_title", title_color),
        ).pack(fill="x")

        ctk.CTkLabel(
            content_frame,
            text=message,
            wraplength=620,
            justify="left",
            anchor="w",
            **get_text_style("body"),
        ).pack(fill="x", pady=(SPACE_4, 0))

        if is_correct is None:
            if question.correct_answer:
                self._add_feedback_detail(
                    content_frame,
                    "Expected answer",
                    question.correct_answer,
                    title_color,
                )
        elif not is_correct:
            if user_answer:
                self._add_feedback_detail(
                    content_frame,
                    "Your answer",
                    user_answer,
                    get_color("status_incorrect"),
                )
            if question.correct_answer:
                self._add_feedback_detail(
                    content_frame,
                    "Correct answer",
                    question.correct_answer,
                    get_color("status_correct"),
                )

        if question.explanation:
            self._add_feedback_detail(
                content_frame,
                "Explanation",
                question.explanation,
            )
        self._scroll_feedback_into_view()

    def _scroll_feedback_into_view(self) -> None:
        """Scroll the practice feedback surface into the visible question area."""
        self.question_area.update_idletasks()
        self.question_area._parent_canvas.yview_moveto(1.0)

    def _feedback_text_style(self, role: str, text_color=None):
        """Return a text style with an optional feedback status color."""
        style = get_text_style(role)
        if text_color is not None:
            style["text_color"] = text_color
        return style

    def _add_feedback_detail(
        self,
        parent: ctk.CTkFrame,
        label: str,
        text: str,
        label_color=None,
    ) -> None:
        """Add a labeled feedback detail row."""
        detail_frame = ctk.CTkFrame(
            parent,
            fg_color=get_color("surface_subtle"),
            border_color=get_color("divider"),
            border_width=1,
            corner_radius=RADIUS_CONTROL,
        )
        detail_frame.pack(fill="x", pady=(SPACE_8, 0))

        ctk.CTkLabel(
            detail_frame,
            text=label,
            anchor="w",
            **self._feedback_text_style(
                "metadata",
                label_color or get_color("text_secondary"),
            ),
        ).pack(fill="x", padx=SPACE_12, pady=(SPACE_8, SPACE_4))

        ctk.CTkLabel(
            detail_frame,
            text=text,
            wraplength=620,
            justify="left",
            anchor="nw",
            **get_text_style("body"),
        ).pack(fill="x", padx=SPACE_12, pady=(0, SPACE_8))

    def _on_previous(self) -> None:
        """Navigate to the previous question."""
        self._save_current_answer()
        if self._session.previous_question():
            self._display_question()

    def _on_next(self) -> None:
        """Navigate to the next question."""
        self._save_current_answer()
        if self._session.next_question():
            self._display_question()

    def _on_progress_click(self, index: int) -> None:
        """Jump to a specific question from the progress bar."""
        self._save_current_answer()
        if self._session.go_to_question(index):
            self._display_question()

    def _on_flag(self) -> None:
        """Toggle flag on the current question."""
        if self._session is None:
            return

        question = self._session.get_current_question()
        if question is None:
            return

        is_flagged = self._session.flag_question(question.id)
        if is_flagged:
            self.flag_btn.configure(text="Unflag", **get_button_style("warning"))
        else:
            self.flag_btn.configure(text="Flag", **get_button_style("tertiary"))

        self._update_progress_bar()

    def _on_finish(self) -> None:
        """Confirm and finish the test."""
        if self._session is None:
            return

        self._save_current_answer()

        unanswered = self._session.get_unanswered_count()
        flagged = self._session.get_flagged_count()

        label = "practice" if self._mode == MODE_PRACTICE else "test"
        msg = f"Are you sure you want to finish this {label}?"
        if unanswered > 0:
            msg += f"\n\n{unanswered} question(s) unanswered."
        if flagged > 0:
            msg += f"\n{flagged} question(s) flagged."

        title = "Finish Practice" if self._mode == MODE_PRACTICE else "Finish Test"
        if not messagebox.askyesno(title, msg):
            return

        # Score and save
        self.timer_widget.stop()
        self._session.finish_test()

        score_data = self.scoring_service.score_test(self._session)

        if self._is_mix_test:
            self.scoring_service.save_mixed_attempt(
                score_data, self._session.questions, mode=self._mode
            )
            self.controller.show_frame(
                SCREEN_RESULTS,
                attempt_id=None,
                session=self._session,
                score_data=score_data,
            )
        else:
            attempt_id = self.scoring_service.save_attempt(
                self._session.test_id, score_data, mode=self._mode
            )
            self.controller.show_frame(
                SCREEN_RESULTS,
                attempt_id=attempt_id,
                session=self._session,
                score_data=score_data,
            )
