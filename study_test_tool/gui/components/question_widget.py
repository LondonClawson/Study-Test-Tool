"""Question widget — displays a question with answer input."""

from typing import Optional

import customtkinter as ctk

from config.settings import (
    FONT_FAMILY,
    FONT_SIZE_BODY,
    FONT_SIZE_HEADING,
    QUESTION_TYPE_ESSAY,
    QUESTION_TYPE_MC,
)
from models.question import Question


class QuestionWidget(ctk.CTkFrame):
    """Displays a question and its answer input (radio buttons or textbox)."""

    def __init__(self, parent: ctk.CTkFrame, question: Question, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.question = question
        self._answer_var = ctk.StringVar(value="")

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the question display."""
        # Question text
        text_label = ctk.CTkLabel(
            self,
            text=self.question.text,
            font=(FONT_FAMILY, FONT_SIZE_BODY),
            wraplength=600,
            justify="left",
            anchor="nw",
        )
        text_label.pack(fill="x", padx=15, pady=(15, 10))

        if self.question.type == QUESTION_TYPE_MC:
            self._build_mc_options()
        else:
            self._build_essay_input()

    def _build_mc_options(self) -> None:
        """Build radio button options for multiple-choice."""
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.pack(fill="x", padx=30, pady=5)

        for option in self.question.options:
            ctk.CTkRadioButton(
                options_frame,
                text=option.text,
                variable=self._answer_var,
                value=option.text,
                font=(FONT_FAMILY, FONT_SIZE_BODY),
            ).pack(anchor="w", pady=4)

    def _build_essay_input(self) -> None:
        """Build a textbox for essay answers."""
        ctk.CTkLabel(
            self,
            text="Your Answer:",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
        ).pack(anchor="w", padx=15, pady=(5, 2))

        self._essay_textbox = ctk.CTkTextbox(self, height=120)
        self._essay_textbox.pack(fill="x", padx=15, pady=(0, 10))

    def get_answer(self) -> Optional[str]:
        """Get the current answer.

        Returns:
            The selected option text (MC) or typed text (essay), or None if empty.
        """
        if self.question.type == QUESTION_TYPE_MC:
            val = self._answer_var.get()
            return val if val else None
        else:
            val = self._essay_textbox.get("1.0", "end-1c").strip()
            return val if val else None

    def set_answer(self, answer: Optional[str]) -> None:
        """Restore a previously saved answer.

        Args:
            answer: The answer text to restore.
        """
        if not answer:
            return
        if self.question.type == QUESTION_TYPE_MC:
            self._answer_var.set(answer)
        else:
            self._essay_textbox.delete("1.0", "end")
            self._essay_textbox.insert("1.0", answer)
