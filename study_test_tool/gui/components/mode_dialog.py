"""Mode selection dialog for choosing between Test and Practice modes."""

import customtkinter as ctk

from config.settings import FONT_FAMILY, FONT_SIZE_BODY, FONT_SIZE_HEADING
from utils.constants import MODE_PRACTICE, MODE_TEST


class ModeSelectionDialog(ctk.CTkToplevel):
    """Dialog for selecting test-taking mode."""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.title("Select Mode")
        self.geometry("360x220")
        self.resizable(False, False)

        self._mode = None

        # Make modal
        self.transient(parent)
        self.grab_set()

        self._build_ui()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - 360) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - 220) // 2
        self.geometry(f"+{x}+{y}")

    def _build_ui(self) -> None:
        """Build the dialog layout."""
        ctk.CTkLabel(
            self,
            text="Choose Mode",
            font=(FONT_FAMILY, FONT_SIZE_HEADING, "bold"),
        ).pack(pady=(20, 15))

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=5)

        ctk.CTkButton(
            btn_frame,
            text="Test Mode",
            width=130,
            height=50,
            command=self._select_test,
        ).pack(side="left", padx=10, expand=True)

        ctk.CTkButton(
            btn_frame,
            text="Practice Mode",
            width=130,
            height=50,
            fg_color="#2fa572",
            hover_color="#258a5e",
            command=self._select_practice,
        ).pack(side="right", padx=10, expand=True)

        ctk.CTkLabel(
            self,
            text="Practice mode shows instant answer feedback",
            font=(FONT_FAMILY, FONT_SIZE_BODY - 2),
            text_color="gray",
        ).pack(pady=(10, 5))

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
