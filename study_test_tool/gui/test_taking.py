"""Test-taking screen — the core test experience."""

import tkinter.messagebox as messagebox

import customtkinter as ctk

from config.settings import (
    COLOR_FLAGGED,
    COLOR_WARNING,
    FONT_FAMILY,
    FONT_SIZE_BODY,
    FONT_SIZE_HEADING,
    FONT_SIZE_TITLE,
)
from gui.components.progress_bar import ProgressBar
from gui.components.question_widget import QuestionWidget
from gui.components.timer_widget import TimerWidget
from services.question_service import QuestionService
from services.scoring_service import ScoringService
from services.test_service import TestService
from services.test_session import TestSession
from utils.constants import SCREEN_HOME, SCREEN_RESULTS


class TestTakingFrame(ctk.CTkFrame):
    """Screen for taking a test with timer, navigation, and flagging."""

    def __init__(self, parent: ctk.CTkFrame, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.test_service = TestService()
        self.question_service = QuestionService()
        self.scoring_service = ScoringService()

        self._session = None
        self._question_widget = None
        self._progress_bar = None

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the test-taking layout."""
        # Top bar
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=20, pady=(15, 5))

        self.test_name_label = ctk.CTkLabel(
            self.top_frame,
            text="",
            font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
        )
        self.test_name_label.pack(side="left")

        self.timer_widget = TimerWidget(self.top_frame)
        self.timer_widget.pack(side="right", padx=10)

        # Progress text
        self.progress_label = ctk.CTkLabel(
            self.top_frame,
            text="",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
        )
        self.progress_label.pack(side="right", padx=20)

        # Flag button
        self.flag_btn = ctk.CTkButton(
            self.top_frame,
            text="Flag",
            width=70,
            fg_color="gray",
            command=self._on_flag,
        )
        self.flag_btn.pack(side="right", padx=5)

        # Center: question area
        self.question_area = ctk.CTkFrame(self)
        self.question_area.pack(fill="both", expand=True, padx=30, pady=10)

        # Bottom: nav buttons + progress bar
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=20, pady=(5, 10))

        nav_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        nav_frame.pack(fill="x", pady=(0, 5))

        self.prev_btn = ctk.CTkButton(
            nav_frame,
            text="< Previous",
            width=100,
            command=self._on_previous,
        )
        self.prev_btn.pack(side="left", padx=5)

        self.next_btn = ctk.CTkButton(
            nav_frame,
            text="Next >",
            width=100,
            command=self._on_next,
        )
        self.next_btn.pack(side="left", padx=5)

        self.finish_btn = ctk.CTkButton(
            nav_frame,
            text="Finish Test",
            width=120,
            fg_color="#d9534f",
            hover_color="#c9302c",
            command=self._on_finish,
        )
        self.finish_btn.pack(side="right", padx=5)

        # Progress bar container
        self.progress_container = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        self.progress_container.pack(fill="x", pady=5)

    def on_show(self, test_id=None, **kwargs) -> None:
        """Initialize the test-taking session."""
        if test_id is None:
            return

        test = self.test_service.get_test_by_id(test_id)
        if not test:
            messagebox.showerror("Error", "Test not found.")
            self.controller.show_frame(SCREEN_HOME)
            return

        questions = self.question_service.get_questions_for_test(
            test_id, randomize=True
        )
        if not questions:
            messagebox.showwarning("No Questions", "This test has no questions.")
            self.controller.show_frame(SCREEN_HOME)
            return

        self.test_name_label.configure(text=test.name)
        self._session = TestSession(test_id, questions)
        self._session.start()

        # Rebuild progress bar
        for widget in self.progress_container.winfo_children():
            widget.destroy()

        self._progress_bar = ProgressBar(
            self.progress_container,
            total=len(questions),
            on_click=self._on_progress_click,
        )
        self._progress_bar.pack()

        self.timer_widget.start()
        self._display_question()

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
            self.flag_btn.configure(fg_color=COLOR_FLAGGED, text="Unflag")
        else:
            self.flag_btn.configure(fg_color="gray", text="Flag")

        # Update nav buttons
        self.prev_btn.configure(
            state="normal" if idx > 0 else "disabled"
        )
        self.next_btn.configure(
            state="normal" if idx < total - 1 else "disabled"
        )

        # Rebuild question widget
        for widget in self.question_area.winfo_children():
            widget.destroy()

        self._question_widget = QuestionWidget(
            self.question_area, question
        )
        self._question_widget.pack(fill="both", expand=True)

        # Restore saved answer
        saved = self._session.responses.get(question.id)
        if saved:
            self._question_widget.set_answer(saved)

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
            self.flag_btn.configure(fg_color=COLOR_FLAGGED, text="Unflag")
        else:
            self.flag_btn.configure(fg_color="gray", text="Flag")

        self._update_progress_bar()

    def _on_finish(self) -> None:
        """Confirm and finish the test."""
        if self._session is None:
            return

        self._save_current_answer()

        unanswered = self._session.get_unanswered_count()
        flagged = self._session.get_flagged_count()

        msg = "Are you sure you want to finish this test?"
        if unanswered > 0:
            msg += f"\n\n{unanswered} question(s) unanswered."
        if flagged > 0:
            msg += f"\n{flagged} question(s) flagged."

        if not messagebox.askyesno("Finish Test", msg):
            return

        # Score and save
        self.timer_widget.stop()
        self._session.finish_test()

        score_data = self.scoring_service.score_test(self._session)
        attempt_id = self.scoring_service.save_attempt(
            self._session.test_id, score_data
        )

        self.controller.show_frame(
            SCREEN_RESULTS,
            attempt_id=attempt_id,
            session=self._session,
            score_data=score_data,
        )
