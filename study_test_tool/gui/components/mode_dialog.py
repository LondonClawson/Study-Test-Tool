"""Mode selection dialog for choosing between Test and Practice modes."""

from typing import Callable

import customtkinter as ctk

from gui.styles import (
    SPACE_12,
    SPACE_16,
    SPACE_24,
    SPACE_4,
    SPACE_8,
    get_button_style,
    get_card_style,
    get_color,
    get_text_style,
)
from utils.constants import MODE_PRACTICE, MODE_TEST


class ModeSelectionDialog(ctk.CTkToplevel):
    """Dialog for selecting test-taking mode."""

    DIALOG_WIDTH = 500
    DIALOG_HEIGHT = 320

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.title("Select Mode")
        self.geometry(f"{self.DIALOG_WIDTH}x{self.DIALOG_HEIGHT}")
        self.resizable(False, False)
        self.configure(fg_color=get_color("app_bg"))

        self._mode = None

        # Make modal
        self.transient(parent)
        self.grab_set()

        self._build_ui()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - self.DIALOG_WIDTH) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.DIALOG_HEIGHT) // 2
        self.geometry(f"+{x}+{y}")

    def _build_ui(self) -> None:
        """Build the dialog layout."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=SPACE_16, pady=SPACE_16)

        shell = ctk.CTkFrame(container, **get_card_style("default"))
        shell.pack(fill="both", expand=True)

        ctk.CTkLabel(
            shell,
            text="Choose a Study Mode",
            **get_text_style("section_title"),
        ).pack(pady=(SPACE_24, SPACE_4))

        ctk.CTkLabel(
            shell,
            text="Select how this session should score answers and show feedback.",
            wraplength=410,
            justify="center",
            **get_text_style("card_description"),
        ).pack(padx=SPACE_24, pady=(0, SPACE_16))

        options_frame = ctk.CTkFrame(shell, fg_color="transparent")
        options_frame.pack(fill="x", padx=SPACE_24, pady=(0, SPACE_24))
        options_frame.grid_columnconfigure((0, 1), weight=1, uniform="mode_options")

        self._build_mode_card(
            options_frame,
            0,
            "Test Mode",
            "Answer every question first, then submit once for a final score.",
            "Start Test",
            "primary",
            self._select_test,
        )
        self._build_mode_card(
            options_frame,
            1,
            "Practice Mode",
            "Check answers as you go with feedback during the session.",
            "Start Practice",
            "secondary",
            self._select_practice,
        )

    def _build_mode_card(
        self,
        parent,
        column: int,
        title: str,
        description: str,
        button_text: str,
        button_role: str,
        command: Callable[[], None],
    ) -> None:
        """Create one mode option card."""
        card = ctk.CTkFrame(parent, width=206, height=142, **get_card_style("default"))
        card.grid(row=0, column=column, sticky="nsew", padx=SPACE_8)
        card.grid_propagate(False)

        ctk.CTkLabel(
            card,
            text=title,
            anchor="w",
            **get_text_style("card_title"),
        ).pack(fill="x", padx=SPACE_12, pady=(SPACE_12, SPACE_4))

        ctk.CTkLabel(
            card,
            text=description,
            wraplength=174,
            justify="left",
            anchor="w",
            **get_text_style("card_description"),
        ).pack(fill="x", padx=SPACE_12)

        ctk.CTkButton(
            card,
            text=button_text,
            height=34,
            command=command,
            **get_button_style(button_role),
        ).pack(side="bottom", fill="x", padx=SPACE_12, pady=SPACE_12)

    def _select_test(self) -> None:
        """Select test mode."""
        self._mode = MODE_TEST
        self.destroy()

    def _select_practice(self) -> None:
        """Select practice mode."""
        self._mode = MODE_PRACTICE
        self.destroy()

    def get_mode(self) -> str:
        """Return the selected mode after dialog closes.

        Returns:
            The selected mode string, or None if dialog was closed.
        """
        self.wait_window()
        return self._mode
