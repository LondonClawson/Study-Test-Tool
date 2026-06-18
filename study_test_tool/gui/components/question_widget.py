"""Question widget — displays a question with answer input."""

from typing import Optional

import customtkinter as ctk

from config.settings import (
    QUESTION_TYPE_ESSAY,
    QUESTION_TYPE_MC,
)
from gui.components.formatted_text import FormattedText
from gui.styles import (
    RADIUS_CONTROL,
    SPACE_4,
    SPACE_8,
    SPACE_12,
    SPACE_16,
    get_color,
    get_text_style,
)
from models.question import Question


class QuestionWidget(ctk.CTkFrame):
    """Displays a question and its answer input (radio buttons or textbox)."""

    def __init__(self, parent: ctk.CTkFrame, question: Question, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.question = question
        self._answer_var = ctk.StringVar(value="")
        self._radio_buttons: list = []
        self._option_labels: list = []
        self._option_rows: list = []
        self._essay_textbox: Optional[ctk.CTkTextbox] = None
        self._is_locked = False
        self._checked_user_answer: Optional[str] = None
        self._checked_correct_answer: Optional[str] = None
        self._checked_result: Optional[bool] = None

        self._build_ui()
        self._answer_var.trace_add("write", self._on_answer_changed)
        self._update_option_rows()

    def _build_ui(self) -> None:
        """Build the question display."""
        text_label = FormattedText(
            self,
            text=self.question.text,
            text_role="body",
            background_color=self.cget("fg_color"),
        )
        text_label.pack(fill="x", padx=SPACE_16, pady=(SPACE_16, SPACE_12))

        if self.question.type == QUESTION_TYPE_MC:
            self._build_mc_options()
        else:
            self._build_essay_input()

    def _build_mc_options(self) -> None:
        """Build radio button options for multiple-choice."""
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.pack(fill="x", padx=SPACE_16, pady=(0, SPACE_16))

        for option in self.question.options:
            row = ctk.CTkFrame(
                options_frame,
                fg_color=get_color("surface_subtle"),
                border_color=get_color("border"),
                border_width=1,
                corner_radius=RADIUS_CONTROL,
            )
            row.pack(fill="x", pady=SPACE_4)
            row.grid_columnconfigure(1, weight=1)
            self._bind_option_click(row, option.text)

            rb = ctk.CTkRadioButton(
                row,
                text="",
                variable=self._answer_var,
                value=option.text,
                width=24,
                command=self._update_option_rows,
                fg_color=get_color("primary"),
                hover_color=get_color("primary_hover"),
                border_color=get_color("border"),
            )
            rb.grid(
                row=0,
                column=0,
                sticky="n",
                padx=(SPACE_12, SPACE_8),
                pady=SPACE_12,
            )
            self._radio_buttons.append(rb)

            label = FormattedText(
                row,
                text=option.text,
                text_role="body",
                background_color=get_color("surface_subtle"),
                cursor="hand2",
            )
            label.grid(
                row=0,
                column=1,
                sticky="ew",
                padx=(0, SPACE_12),
                pady=SPACE_12,
            )
            self._bind_option_click(label, option.text)
            self._option_labels.append(label)
            self._option_rows.append(
                {
                    "row": row,
                    "radio": rb,
                    "label": label,
                    "value": option.text,
                }
            )

    def _build_essay_input(self) -> None:
        """Build a textbox for essay answers."""
        ctk.CTkLabel(
            self,
            text="Your Answer:",
            **get_text_style("body"),
        ).pack(anchor="w", padx=SPACE_16, pady=(0, SPACE_4))

        self._essay_textbox = ctk.CTkTextbox(
            self,
            height=132,
            fg_color=get_color("surface_subtle"),
            border_color=get_color("border"),
            border_width=1,
            corner_radius=RADIUS_CONTROL,
            **get_text_style("body"),
        )
        self._essay_textbox.pack(fill="x", padx=SPACE_16, pady=(0, SPACE_16))

    def _select_option(self, option_text: str) -> None:
        """Select an option from any full-row click target."""
        if self._is_locked:
            return
        self._answer_var.set(option_text)

    def _bind_option_click(self, widget, option_text: str) -> None:
        """Bind a CustomTkinter widget and its drawn children to select a row."""
        callback = lambda _event, val=option_text: self._select_option(val)
        if hasattr(widget, "bind_click"):
            widget.bind_click(callback)
            return
        widget.bind("<Button-1>", callback)
        for child_name in ("_canvas", "_label", "_text_label"):
            child = getattr(widget, child_name, None)
            if child is not None:
                child.bind("<Button-1>", callback)

    def _unbind_option_click(self, widget) -> None:
        """Remove option click bindings from a CustomTkinter widget."""
        if hasattr(widget, "unbind_click"):
            widget.unbind_click()
            return
        widget.unbind("<Button-1>")
        for child_name in ("_canvas", "_label", "_text_label"):
            child = getattr(widget, child_name, None)
            if child is not None:
                child.unbind("<Button-1>")

    def _on_answer_changed(self, *_args) -> None:
        """Refresh row styling whenever the selected option changes."""
        self._update_option_rows()

    def _update_option_rows(self) -> None:
        """Apply selected, locked, and checked-result styling to answer rows."""
        if not self._option_rows:
            return

        selected = self._answer_var.get()
        for row_info in self._option_rows:
            option_text = row_info["value"]
            row = row_info["row"]
            label = row_info["label"]
            is_selected = option_text == selected
            is_correct_option = (
                self._checked_correct_answer is not None
                and option_text == self._checked_correct_answer
            )
            is_incorrect_selection = (
                self._checked_result is False
                and self._checked_user_answer is not None
                and option_text == self._checked_user_answer
                and not is_correct_option
            )

            fg_color = get_color("surface_subtle")
            border_color = get_color("border")
            border_width = 1
            text_color = get_color("text_primary")

            if is_correct_option:
                fg_color = get_color("surface")
                border_color = get_color("status_correct")
                border_width = 2
                text_color = get_color("status_correct")
            elif is_incorrect_selection:
                fg_color = get_color("surface")
                border_color = get_color("status_incorrect")
                border_width = 2
                text_color = get_color("status_incorrect")
            elif is_selected:
                fg_color = get_color("surface")
                border_color = get_color("primary")
                border_width = 2
            elif self._is_locked:
                fg_color = get_color("surface_muted")
                border_color = get_color("divider")
                text_color = get_color("text_disabled")

            row.configure(
                fg_color=fg_color,
                border_color=border_color,
                border_width=border_width,
            )
            if hasattr(label, "configure_colors"):
                label.configure_colors(
                    text_color=text_color,
                    background_color=fg_color,
                )
            else:
                label.configure(text_color=text_color)

    def show_checked_state(
        self,
        correct_answer: str,
        user_answer: Optional[str],
        is_correct: Optional[bool],
    ) -> None:
        """Show row-level result styling for a checked multiple-choice answer."""
        if self.question.type != QUESTION_TYPE_MC:
            return
        self._checked_correct_answer = correct_answer
        self._checked_user_answer = user_answer
        self._checked_result = is_correct if isinstance(is_correct, bool) else None
        self._update_option_rows()

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
            self._update_option_rows()
        else:
            self._essay_textbox.delete("1.0", "end")
            self._essay_textbox.insert("1.0", answer)

    def disable(self) -> None:
        """Disable all answer inputs so the answer cannot be changed.

        Used in practice mode after the user clicks "Check Answer" to lock
        in their first attempt.
        """
        if self.question.type == QUESTION_TYPE_MC:
            self._is_locked = True
            for rb in self._radio_buttons:
                rb.configure(state="disabled")
            for label in self._option_labels:
                self._unbind_option_click(label)
                if hasattr(label, "configure_cursor"):
                    label.configure_cursor("arrow")
                else:
                    label.configure(cursor="")
            for row_info in self._option_rows:
                self._unbind_option_click(row_info["row"])
            self._update_option_rows()
        elif self._essay_textbox is not None:
            self._is_locked = True
            self._essay_textbox.configure(
                state="disabled",
                fg_color=get_color("surface_muted"),
                border_color=get_color("border"),
                text_color=get_color("text_secondary"),
            )
