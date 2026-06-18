"""Results view — displays score and question-by-question review."""

from collections import defaultdict

import customtkinter as ctk

from config.settings import QUESTION_TYPE_MC
from gui.components.formatted_text import FormattedText
from gui.styles import (
    FONT_BODY_BOLD,
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
        self._mode = None
        self._mix_questions = None
        self._mix_name = None
        self._mix_subtitle = None

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the results layout."""
        self.configure(fg_color=get_color("app_bg"))

        # Header
        self.header_frame = ctk.CTkFrame(self, **get_header_style("page"))
        self.header_frame.pack(fill="x", padx=SPACE_24, pady=(SPACE_24, SPACE_12))
        self.header_frame.grid_columnconfigure(0, weight=1)

        summary_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        summary_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=SPACE_24,
            pady=SPACE_16,
        )

        ctk.CTkLabel(
            summary_frame,
            text="Results",
            anchor="w",
            **get_text_style("page_title"),
        ).pack(fill="x")

        score_row = ctk.CTkFrame(summary_frame, fg_color="transparent")
        score_row.pack(fill="x", pady=(SPACE_8, SPACE_4))

        self.score_label = ctk.CTkLabel(
            score_row,
            text="",
            anchor="w",
            **get_text_style("page_score"),
        )
        self.score_label.pack(side="left")

        self.percentage_label = ctk.CTkLabel(
            score_row,
            text="",
            fg_color=get_color("surface_subtle"),
            corner_radius=RADIUS_CONTROL,
            **get_text_style("section_title"),
        )
        self.percentage_label.pack(side="left", padx=(SPACE_12, 0), ipadx=SPACE_12)

        self.metrics_frame = ctk.CTkFrame(summary_frame, fg_color="transparent")
        self.metrics_frame.pack(fill="x", pady=(SPACE_8, 0))

        btn_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        btn_frame.grid(
            row=0,
            column=1,
            sticky="ne",
            padx=(SPACE_8, SPACE_24),
            pady=SPACE_16,
        )

        ctk.CTkButton(
            btn_frame,
            text="Back to Home",
            width=120,
            command=lambda: self.controller.show_frame(SCREEN_HOME),
            **get_button_style("secondary"),
        ).pack(fill="x", pady=(0, SPACE_8))

        self.retake_btn = ctk.CTkButton(
            btn_frame,
            text="Retake Test",
            width=120,
            command=self._on_retake,
            **get_button_style("primary"),
        )
        self.retake_btn.pack(fill="x")

        # Scrollable question review
        self.review_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=get_color("surface_subtle"),
            border_color=get_color("border"),
            border_width=1,
            corner_radius=RADIUS_CARD,
            scrollbar_button_color=get_color("secondary"),
            scrollbar_button_hover_color=get_color("secondary_hover"),
        )
        self.review_frame.pack(
            fill="both",
            expand=True,
            padx=SPACE_24,
            pady=(0, SPACE_24),
        )

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
        self._reset_retake_state()

        # Clear previous review
        for widget in self.review_frame.winfo_children():
            widget.destroy()

        if session and score_data:
            self._show_from_session(session, score_data)
        elif attempt_id:
            self._show_from_db(attempt_id)
        self._reset_review_scroll()

    def _reset_retake_state(self) -> None:
        """Clear retained retake routing before loading a new result payload."""
        self._test_id = None
        self._mode = None
        self._mix_questions = None
        self._mix_name = None
        self._mix_subtitle = None

    def _show_from_session(self, session, score_data: dict) -> None:
        """Display results from a just-completed session."""
        self._test_id = session.test_id
        self._mode = session.mode
        if session.is_mix_test:
            self._mix_questions = session.questions
            self._mix_name = session.mix_name
            self._mix_subtitle = session.mix_subtitle
        else:
            self._mix_questions = None
            self._mix_name = None
            self._mix_subtitle = None

        # Header
        score = score_data["score"]
        total = score_data["total"]
        pct = score_data["percentage"]
        time_taken = score_data.get("time_taken", 0)
        essays = score_data.get("essay_questions", 0)

        metrics = [("Time", self._format_time(time_taken))]
        metrics.append(("Scored", f"{total} question{'s' if total != 1 else ''}"))
        if essays > 0:
            metrics.append(("Essays", f"{essays} self-evaluate"))
        self._set_score_summary(score, total, pct, metrics)

        # Build question review
        self._add_review_section_title("Question Review")
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
                explanation=question.explanation,
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
        section = ctk.CTkFrame(self.review_frame, **get_card_style("default"))
        section.pack(fill="x", pady=(SPACE_16, SPACE_8), padx=SPACE_12)

        ctk.CTkLabel(
            section,
            text="Score by Source Test",
            anchor="w",
            **get_text_style("section_title"),
        ).pack(fill="x", padx=SPACE_16, pady=(SPACE_16, SPACE_8))

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
                detail = f"{correct}/{mc_total}"
                summary = f"{pct}%"
            else:
                detail = f"{len(questions)} essay question(s)"
                summary = "Essay"

            if mc_total > 0 and correct == mc_total:
                status_color = get_color("status_correct")
            elif mc_total > 0 and correct < mc_total / 2:
                status_color = get_color("status_incorrect")
            else:
                status_color = get_color("status_neutral")

            self._add_source_row(section, test_name, detail, summary, status_color)

        ctk.CTkFrame(section, height=SPACE_8, fg_color="transparent").pack()

    def _show_from_db(self, attempt_id: int) -> None:
        """Display results loaded from the database."""
        attempt = self.scoring_service.get_attempt_details(attempt_id)
        if not attempt:
            self._show_missing_results()
            return

        self._test_id = attempt.test_id
        self._mode = attempt.mode

        time_str = (
            self._format_time(attempt.time_taken) if attempt.time_taken else "N/A"
        )
        self._set_score_summary(
            attempt.score,
            attempt.total_questions,
            attempt.percentage,
            [("Time", time_str)],
        )

        # Load test for question details
        test = self.test_service.get_test_by_id(attempt.test_id)
        if not test:
            self._add_empty_review_message("The test for this attempt is unavailable.")
            return

        q_map = {q.id: q for q in test.questions}

        self._add_review_section_title("Question Review")
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
                explanation=question.explanation,
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
        explanation: str,
        is_correct: bool,
        was_flagged: bool,
        options=None,
    ) -> None:
        """Create a review card for one question."""
        card = ctk.CTkFrame(self.review_frame, **get_card_style("default"))
        card.pack(fill="x", pady=SPACE_8, padx=SPACE_12)

        # Question header
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=SPACE_16, pady=(SPACE_16, SPACE_8))

        ctk.CTkLabel(
            header_frame,
            text=f"Q{num}",
            fg_color=get_color("surface_subtle"),
            corner_radius=RADIUS_CONTROL,
            **get_text_style("metadata"),
        ).pack(side="left", ipadx=SPACE_8, ipady=SPACE_4)

        # Status indicator
        if is_correct is None:
            status_text = "Essay"
            status_color = get_color("status_neutral")
        elif is_correct:
            status_text = "Correct"
            status_color = get_color("status_correct")
        else:
            status_text = "Incorrect"
            status_color = get_color("status_incorrect")

        if was_flagged:
            self._build_status_badge(
                header_frame, "Flagged", get_color("warning")
            ).pack(
                side="left",
                padx=(SPACE_8, 0),
            )

        self._build_status_badge(header_frame, status_text, status_color).pack(
            side="right"
        )

        # Question text
        FormattedText(
            card,
            text=question_text,
            text_role="body",
            background_color=get_color("surface"),
        ).pack(fill="x", padx=SPACE_16, pady=(0, SPACE_12))

        if question_type == QUESTION_TYPE_MC:
            # Show user's answer and correct answer
            answer_frame = ctk.CTkFrame(card, fg_color="transparent")
            answer_frame.pack(fill="x", padx=SPACE_16, pady=(0, SPACE_16))

            user_text = user_answer if user_answer else "(No answer)"
            user_color = (
                get_color("status_correct")
                if is_correct
                else get_color("status_incorrect")
            )
            self._add_answer_panel(
                answer_frame,
                "Your answer",
                user_text,
                user_color,
            )

            self._add_answer_panel(
                answer_frame,
                "Correct answer",
                correct_answer,
                get_color("status_correct"),
            )
        else:
            # Essay: show side-by-side
            essay_frame = ctk.CTkFrame(card, fg_color="transparent")
            essay_frame.pack(fill="x", padx=SPACE_16, pady=(0, SPACE_16))

            self._add_answer_panel(
                essay_frame,
                "Your answer",
                user_answer if user_answer else "(No answer)",
                get_color("status_neutral"),
            )

            if correct_answer:
                self._add_answer_panel(
                    essay_frame,
                    "Expected answer",
                    correct_answer,
                    get_color("status_neutral"),
                )

        if explanation:
            explanation_frame = ctk.CTkFrame(card, fg_color="transparent")
            explanation_frame.pack(fill="x", padx=SPACE_16, pady=(0, SPACE_16))

            self._add_answer_panel(
                explanation_frame,
                "Explanation",
                explanation,
                get_color("text_secondary"),
            )

    def _set_score_summary(self, score, total, percentage, metrics) -> None:
        """Update score summary and metric chips."""
        self.score_label.configure(text=f"{score}/{total}")
        self.percentage_label.configure(text=f"{percentage}%")
        for widget in self.metrics_frame.winfo_children():
            widget.destroy()
        for label, value in metrics:
            self._add_metric(label, value)

    def _add_metric(self, label: str, value: str) -> None:
        """Add a compact metric to the score summary."""
        metric = ctk.CTkFrame(
            self.metrics_frame,
            fg_color=get_color("surface_subtle"),
            corner_radius=RADIUS_CONTROL,
        )
        metric.pack(side="left", padx=(0, SPACE_8), pady=(0, SPACE_4))

        ctk.CTkLabel(
            metric,
            text=label,
            **get_text_style("metadata"),
        ).pack(side="left", padx=(SPACE_12, SPACE_4), pady=SPACE_8)

        ctk.CTkLabel(
            metric,
            text=value,
            font=FONT_BODY_BOLD,
            text_color=get_color("text_primary"),
        ).pack(side="left", padx=(0, SPACE_12), pady=SPACE_8)

    def _add_review_section_title(self, text: str) -> None:
        """Add a section title inside the review scroll area."""
        ctk.CTkLabel(
            self.review_frame,
            text=text,
            anchor="w",
            **get_text_style("section_title"),
        ).pack(fill="x", padx=SPACE_16, pady=(SPACE_16, SPACE_4))

    def _build_status_badge(self, parent, text: str, color) -> ctk.CTkLabel:
        """Build a compact status badge."""
        return ctk.CTkLabel(
            parent,
            text=text,
            fg_color=color,
            corner_radius=RADIUS_CONTROL,
            text_color=get_color("text_inverse"),
            font=FONT_BODY_BOLD,
        )

    def _add_answer_panel(
        self,
        parent: ctk.CTkFrame,
        label: str,
        text: str,
        label_color,
    ) -> None:
        """Add a labeled answer comparison panel."""
        panel = ctk.CTkFrame(
            parent,
            fg_color=get_color("surface_subtle"),
            border_color=get_color("divider"),
            border_width=1,
            corner_radius=RADIUS_CONTROL,
        )
        panel.pack(fill="x", pady=(0, SPACE_8))

        ctk.CTkLabel(
            panel,
            text=label,
            anchor="w",
            **self._answer_panel_label_style(label_color),
        ).pack(fill="x", padx=SPACE_12, pady=(SPACE_8, SPACE_4))

        FormattedText(
            panel,
            text=text if text else "(No answer)",
            text_role="body",
            background_color=get_color("surface_subtle"),
        ).pack(fill="x", padx=SPACE_12, pady=(0, SPACE_8))

    def _add_source_row(
        self,
        parent: ctk.CTkFrame,
        test_name: str,
        detail: str,
        summary: str,
        status_color,
    ) -> None:
        """Add one mixed-source breakdown row."""
        row = ctk.CTkFrame(
            parent,
            fg_color=get_color("surface_subtle"),
            border_color=get_color("divider"),
            border_width=1,
            corner_radius=RADIUS_CONTROL,
        )
        row.pack(fill="x", padx=SPACE_16, pady=(0, SPACE_8))
        row.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            row,
            text=test_name,
            anchor="w",
            **get_text_style("body"),
        ).grid(row=0, column=0, sticky="ew", padx=SPACE_12, pady=SPACE_12)

        ctk.CTkLabel(
            row,
            text=detail,
            **get_text_style("metadata"),
        ).grid(row=0, column=1, padx=SPACE_12, pady=SPACE_12)

        self._build_status_badge(row, summary, status_color).grid(
            row=0,
            column=2,
            padx=(0, SPACE_12),
            pady=SPACE_12,
        )

    def _answer_panel_label_style(self, text_color) -> dict:
        """Return a card-title style with a custom semantic color."""
        style = get_text_style("card_title")
        style["text_color"] = text_color
        return style

    def _show_missing_results(self) -> None:
        """Show a calm missing-results state."""
        self.score_label.configure(text="Results unavailable")
        self.percentage_label.configure(text="")
        for widget in self.metrics_frame.winfo_children():
            widget.destroy()
        self._add_empty_review_message("This saved result could not be loaded.")

    def _add_empty_review_message(self, message: str) -> None:
        """Add an empty/error state inside the review area."""
        frame = ctk.CTkFrame(self.review_frame, **get_card_style("default"))
        frame.pack(fill="x", padx=SPACE_12, pady=SPACE_16)
        ctk.CTkLabel(
            frame,
            text=message,
            anchor="center",
            **get_text_style("body"),
        ).pack(fill="x", padx=SPACE_24, pady=SPACE_24)

    def _reset_review_scroll(self) -> None:
        """Reset CTkScrollableFrame after rebuilding result content."""
        self.update_idletasks()
        canvas = getattr(self.review_frame, "_parent_canvas", None)
        if canvas is not None:
            canvas.yview_moveto(0.0)

    def _on_retake(self) -> None:
        """Navigate to retake the same test (mix or regular)."""
        if self._mix_questions is not None:
            self.controller.show_frame(
                SCREEN_TEST_TAKING,
                mode=self._mode,
                questions=self._mix_questions,
                mix_test_name=self._mix_name,
                mix_test_subtitle=self._mix_subtitle,
            )
        elif self._test_id:
            self.controller.show_frame(
                SCREEN_TEST_TAKING,
                test_id=self._test_id,
                mode=self._mode,
            )

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
