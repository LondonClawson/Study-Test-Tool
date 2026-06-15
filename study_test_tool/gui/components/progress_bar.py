"""Progress bar — row of clickable question indicators."""

from typing import Callable, Set

import customtkinter as ctk

from gui.styles import FONT_COMPACT, PROGRESS_STATUS_COLORS, RADIUS_ROW


class ProgressBar(ctk.CTkFrame):
    """Row of small buttons representing each question's status."""

    def __init__(
        self,
        parent: ctk.CTkFrame,
        total: int,
        on_click: Callable[[int], None],
        **kwargs,
    ) -> None:
        super().__init__(parent, **kwargs)
        self._total = total
        self._on_click = on_click
        self._buttons = []
        self._build_ui()

    def _build_ui(self) -> None:
        """Create one button per question."""
        for i in range(self._total):
            btn = ctk.CTkButton(
                self,
                text=str(i + 1),
                width=32,
                height=28,
                corner_radius=RADIUS_ROW,
                fg_color=PROGRESS_STATUS_COLORS["unanswered"],
                font=FONT_COMPACT,
                command=lambda idx=i: self._on_click(idx),
            )
            btn.pack(side="left", padx=1, pady=2)
            self._buttons.append(btn)

    def update_status(
        self,
        current_index: int,
        answered: Set[int],
        flagged: Set[int],
        question_ids: list,
    ) -> None:
        """Update all button colors based on current state.

        Args:
            current_index: Index of the currently displayed question.
            answered: Set of question IDs that have been answered.
            flagged: Set of question IDs that are flagged.
            question_ids: Ordered list of question IDs matching button indices.
        """
        for i, btn in enumerate(self._buttons):
            q_id = question_ids[i] if i < len(question_ids) else None
            if i == current_index:
                color = PROGRESS_STATUS_COLORS["current"]
            elif q_id in flagged:
                color = PROGRESS_STATUS_COLORS["flagged"]
            elif q_id in answered:
                color = PROGRESS_STATUS_COLORS["answered"]
            else:
                color = PROGRESS_STATUS_COLORS["unanswered"]
            btn.configure(fg_color=color)
