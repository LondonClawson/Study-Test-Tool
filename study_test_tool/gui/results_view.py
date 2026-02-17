"""Results view — displays score and question-by-question review."""

from collections import defaultdict

import customtkinter as ctk

from config.settings import (
    COLOR_CORRECT,
    COLOR_INCORRECT,
    COLOR_PRIMARY,
    FONT_FAMILY,
    FONT_SIZE_BODY,
    FONT_SIZE_HEADING,
    FONT_SIZE_SMALL,
    FONT_SIZE_TITLE,
    QUESTION_TYPE_ESSAY,
    QUESTION_TYPE_MC,
)
from services.scoring_service import ScoringService
from services.test_service import TestService
from utils.constants import SCREEN_HOME, SCREEN_TEST_TAKING


class ResultsViewFrame(ctk.CTkFrame):
    """Displays test results with score and per-question review."""

    def __init__(self, parent: ctk.CTkFrame, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.scoring_service = ScoringService()
        self.test_service = TestService()
        self._test_id = None

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the results layout."""
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=30, pady=(20, 10))

        self.score_label = ctk.CTkLabel(
            self.header_frame,
            text="",
            font=(FONT_FAMILY, FONT_SIZE_TITLE + 4, "bold"),
        )
        self.score_label.pack()

        self.details_label = ctk.CTkLabel(
            self.header_frame,
            text="",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
            text_color="gray",
        )
        self.details_label.pack(pady=5)

        # Button bar
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=5)

        ctk.CTkButton(
            btn_frame,
            text="Back to Home",
            width=120,
            command=lambda: self.controller.show_frame(SCREEN_HOME),
        ).pack(side="left", padx=5)

        self.retake_btn = ctk.CTkButton(
            btn_frame,
            text="Retake Test",
            width=120,
            command=self._on_retake,
        )
        self.retake_btn.pack(side="left", padx=5)

        # Scrollable question review
        self.review_frame = ctk.CTkScrollableFrame(self)
        self.review_frame.pack(fill="both", expand=True, padx=30, pady=(5, 20))

    def on_show(
        self,
        attempt_id=None,
        session=None,
        score_data=None,
        **kwargs,
    ) -> None:
        """Show results — from a just-completed test or from history.

        Args:
            attempt_id: The saved attempt ID.
            session: The TestSession (available if coming from test-taking).
            score_data: Score dict (available if coming from test-taking).
        """
        # Clear previous review
        for widget in self.review_frame.winfo_children():
            widget.destroy()

        if session and score_data:
            self._show_from_session(session, score_data)
        elif attempt_id:
            self._show_from_db(attempt_id)

    def _show_from_session(self, session, score_data: dict) -> None:
        """Display results from a just-completed session."""
        self._test_id = session.test_id

        # Header
        score = score_data["score"]
        total = score_data["total"]
        pct = score_data["percentage"]
        time_taken = score_data.get("time_taken", 0)
        essays = score_data.get("essay_questions", 0)

        self.score_label.configure(text=f"{score}/{total} — {pct}%")

        details = f"Time: {self._format_time(time_taken)}"
        if essays > 0:
            details += f"  |  {essays} essay question(s) for self-evaluation"
        self.details_label.configure(text=details)

        # Build question review
        for i, question in enumerate(session.questions, 1):
            user_answer = session.responses.get(question.id)
            response = next(
                (r for r in score_data["responses"] if r.question_id == question.id),
                None,
            )
            is_correct = response.is_correct if response else None
            was_flagged = question.id in session.flagged

            self._create_review_card(
                num=i,
                question_text=question.text,
                question_type=question.type,
                user_answer=user_answer,
                correct_answer=question.correct_answer,
                is_correct=is_correct,
                was_flagged=was_flagged,
                options=question.options,
            )

        # Per-source-test breakdown for mix tests
        if session.is_mix_test:
            self._show_source_breakdown(session, score_data)

    def _show_source_breakdown(self, session, score_data: dict) -> None:
        """Show per-source-test score breakdown for mix tests."""
        # Group questions by source test_id
        grouped: dict = defaultdict(list)
        response_map = {r.question_id: r for r in score_data["responses"]}
        for question in session.questions:
            if question.test_id is not None:
                grouped[question.test_id].append(question)

        if not grouped:
            return

        # Section header
        section = ctk.CTkFrame(self.review_frame, corner_radius=8)
        section.pack(fill="x", pady=(15, 5), padx=5)

        ctk.CTkLabel(
            section,
            text="Score by Source Test",
            font=(FONT_FAMILY, FONT_SIZE_HEADING, "bold"),
            text_color=COLOR_PRIMARY,
        ).pack(anchor="w", padx=15, pady=(10, 5))

        for test_id, questions in grouped.items():
            test = self.test_service.get_test_by_id(test_id)
            test_name = test.name if test else f"Test #{test_id}"

            correct = 0
            mc_total = 0
            for q in questions:
                resp = response_map.get(q.id)
                if resp and resp.is_correct is not None:
                    mc_total += 1
                    if resp.is_correct:
                        correct += 1

            if mc_total > 0:
                pct = round(correct / mc_total * 100, 1)
                line = f"{test_name}: {correct}/{mc_total} ({pct}%)"
            else:
                line = f"{test_name}: {len(questions)} essay question(s)"

            color = COLOR_CORRECT if mc_total > 0 and correct == mc_total else (
                COLOR_INCORRECT if mc_total > 0 and correct < mc_total / 2
                else "gray"
            )

            ctk.CTkLabel(
                section,
                text=line,
                font=(FONT_FAMILY, FONT_SIZE_BODY),
                text_color=color,
                anchor="w",
            ).pack(fill="x", padx=25, pady=2)

        # Bottom padding
        ctk.CTkFrame(section, height=8, fg_color="transparent").pack()

    def _show_from_db(self, attempt_id: int) -> None:
        """Display results loaded from the database."""
        attempt = self.scoring_service.get_attempt_details(attempt_id)
        if not attempt:
            self.score_label.configure(text="Results not found.")
            return

        self._test_id = attempt.test_id

        self.score_label.configure(
            text=f"{attempt.score}/{attempt.total_questions} — {attempt.percentage}%"
        )

        time_str = self._format_time(attempt.time_taken) if attempt.time_taken else "N/A"
        self.details_label.configure(text=f"Time: {time_str}")

        # Load test for question details
        test = self.test_service.get_test_by_id(attempt.test_id)
        if not test:
            return

        q_map = {q.id: q for q in test.questions}

        for i, response in enumerate(attempt.responses, 1):
            question = q_map.get(response.question_id)
            if not question:
                continue

            self._create_review_card(
                num=i,
                question_text=question.text,
                question_type=question.type,
                user_answer=response.user_answer,
                correct_answer=question.correct_answer,
                is_correct=response.is_correct,
                was_flagged=response.was_flagged,
                options=question.options,
            )

    def _create_review_card(
        self,
        num: int,
        question_text: str,
        question_type: str,
        user_answer: str,
        correct_answer: str,
        is_correct: bool,
        was_flagged: bool,
        options=None,
    ) -> None:
        """Create a review card for one question."""
        card = ctk.CTkFrame(self.review_frame, corner_radius=8)
        card.pack(fill="x", pady=5, padx=5)

        # Question header
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(8, 2))

        flag_text = " [Flagged]" if was_flagged else ""
        ctk.CTkLabel(
            header_frame,
            text=f"Q{num}.{flag_text}",
            font=(FONT_FAMILY, FONT_SIZE_BODY, "bold"),
            anchor="w",
        ).pack(side="left")

        # Status indicator
        if is_correct is None:
            status_text = "Essay — Self-evaluate"
            status_color = "gray"
        elif is_correct:
            status_text = "Correct"
            status_color = COLOR_CORRECT
        else:
            status_text = "Incorrect"
            status_color = COLOR_INCORRECT

        ctk.CTkLabel(
            header_frame,
            text=status_text,
            font=(FONT_FAMILY, FONT_SIZE_SMALL, "bold"),
            text_color=status_color,
        ).pack(side="right")

        # Question text
        ctk.CTkLabel(
            card,
            text=question_text,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            wraplength=600,
            justify="left",
            anchor="nw",
        ).pack(fill="x", padx=15, pady=(2, 5))

        if question_type == QUESTION_TYPE_MC:
            # Show user's answer and correct answer
            answer_frame = ctk.CTkFrame(card, fg_color="transparent")
            answer_frame.pack(fill="x", padx=15, pady=(0, 8))

            user_text = user_answer if user_answer else "(No answer)"
            user_color = COLOR_CORRECT if is_correct else COLOR_INCORRECT

            ctk.CTkLabel(
                answer_frame,
                text=f"Your answer: {user_text}",
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                text_color=user_color,
                anchor="w",
            ).pack(fill="x")

            if not is_correct:
                ctk.CTkLabel(
                    answer_frame,
                    text=f"Correct answer: {correct_answer}",
                    font=(FONT_FAMILY, FONT_SIZE_SMALL),
                    text_color=COLOR_CORRECT,
                    anchor="w",
                ).pack(fill="x")
        else:
            # Essay: show side-by-side
            essay_frame = ctk.CTkFrame(card, fg_color="transparent")
            essay_frame.pack(fill="x", padx=15, pady=(0, 8))

            ctk.CTkLabel(
                essay_frame,
                text="Your Answer:",
                font=(FONT_FAMILY, FONT_SIZE_SMALL, "bold"),
                anchor="w",
            ).pack(fill="x")

            ctk.CTkLabel(
                essay_frame,
                text=user_answer if user_answer else "(No answer)",
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                wraplength=600,
                justify="left",
                anchor="nw",
            ).pack(fill="x", pady=(0, 5))

            if correct_answer:
                ctk.CTkLabel(
                    essay_frame,
                    text="Expected Answer:",
                    font=(FONT_FAMILY, FONT_SIZE_SMALL, "bold"),
                    anchor="w",
                ).pack(fill="x")

                ctk.CTkLabel(
                    essay_frame,
                    text=correct_answer,
                    font=(FONT_FAMILY, FONT_SIZE_SMALL),
                    wraplength=600,
                    justify="left",
                    anchor="nw",
                ).pack(fill="x")

    def _on_retake(self) -> None:
        """Navigate to retake the same test."""
        if self._test_id:
            self.controller.show_frame(SCREEN_TEST_TAKING, test_id=self._test_id)

    @staticmethod
    def _format_time(seconds: int) -> str:
        """Format seconds to MM:SS or HH:MM:SS."""
        if not seconds:
            return "00:00"
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        return f"{minutes:02d}:{secs:02d}"
