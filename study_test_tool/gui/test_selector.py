"""Home screen — test selector with import, create, and test list."""

import json
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

import customtkinter as ctk

from config.settings import (
    COLOR_DANGER,
    COLOR_PRIMARY,
    FONT_FAMILY,
    FONT_SIZE_BODY,
    FONT_SIZE_HEADING,
    FONT_SIZE_SMALL,
    FONT_SIZE_TITLE,
)
from gui.components.mode_dialog import ModeSelectionDialog
from services.import_service import ImportService
from services.test_service import TestService
from utils.constants import (
    IMPORT_FILE_TYPES,
    SCREEN_ANALYTICS,
    SCREEN_EDITOR,
    SCREEN_HISTORY,
    SCREEN_REVIEW,
    SCREEN_TEST_TAKING,
)


class TestSelectorFrame(ctk.CTkFrame):
    """Home screen displaying available tests with actions."""

    def __init__(self, parent: ctk.CTkFrame, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.test_service = TestService()
        self.import_service = ImportService()

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the home screen layout."""
        # Title
        title = ctk.CTkLabel(
            self,
            text="Study Testing Tool",
            font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
        )
        title.pack(pady=(20, 10))

        # Button bar
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=(0, 15))

        ctk.CTkButton(
            btn_frame,
            text="Import Test",
            command=self._on_import,
            width=120,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="New Test",
            command=self._on_new_test,
            width=120,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Analytics",
            command=self._on_analytics,
            width=120,
            fg_color="#6c757d",
            hover_color="#5a6268",
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="View History",
            command=self._on_view_history,
            width=120,
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Review Missed",
            command=self._on_review_missed,
            width=120,
            fg_color="#f0ad4e",
            hover_color="#d9972d",
        ).pack(side="right", padx=5)

        # Scrollable test list
        self.test_list_frame = ctk.CTkScrollableFrame(self)
        self.test_list_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        # Empty state label (shown when no tests)
        self.empty_label = ctk.CTkLabel(
            self.test_list_frame,
            text="No tests available. Import or create one!",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
            text_color="gray",
        )

    def on_show(self, **kwargs) -> None:
        """Refresh the test list when this screen is shown."""
        self._refresh_test_list()

    def _refresh_test_list(self) -> None:
        """Reload and display all tests."""
        # Clear existing cards
        for widget in self.test_list_frame.winfo_children():
            if widget != self.empty_label:
                widget.destroy()

        tests = self.test_service.get_all_tests()

        if not tests:
            self.empty_label.pack(pady=40)
            return

        self.empty_label.pack_forget()

        for test in tests:
            self._create_test_card(test)

    def _create_test_card(self, test) -> None:
        """Create a card widget for a single test."""
        card = ctk.CTkFrame(self.test_list_frame, corner_radius=8)
        card.pack(fill="x", pady=5, padx=5)

        # Info section
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)

        ctk.CTkLabel(
            info_frame,
            text=test.name,
            font=(FONT_FAMILY, FONT_SIZE_HEADING, "bold"),
            anchor="w",
        ).pack(fill="x")

        desc_text = test.description if test.description else "No description"
        ctk.CTkLabel(
            info_frame,
            text=desc_text,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color="gray",
            anchor="w",
        ).pack(fill="x")

        # Question count
        q_count = self.test_service.get_question_count(test.id)
        ctk.CTkLabel(
            info_frame,
            text=f"{q_count} question{'s' if q_count != 1 else ''}",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color="gray",
            anchor="w",
        ).pack(fill="x")

        # Action buttons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(side="right", padx=15, pady=10)

        take_btn = ctk.CTkButton(
            btn_frame,
            text="Take Test",
            width=90,
            command=lambda t=test: self._on_take_test(t),
        )
        take_btn.pack(side="left", padx=3)
        if q_count == 0:
            take_btn.configure(state="disabled")

        ctk.CTkButton(
            btn_frame,
            text="Edit",
            width=70,
            fg_color="gray",
            command=lambda t=test: self._on_edit_test(t),
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            btn_frame,
            text="Delete",
            width=70,
            fg_color=COLOR_DANGER,
            hover_color="#c9302c",
            command=lambda t=test: self._on_delete_test(t),
        ).pack(side="left", padx=3)

    def _on_import(self) -> None:
        """Handle Import Test button click."""
        file_path = filedialog.askopenfilename(
            title="Import Test",
            filetypes=IMPORT_FILE_TYPES,
        )
        if not file_path:
            return

        try:
            if file_path.endswith(".json"):
                test_id = self.import_service.import_from_json(file_path)
            else:
                test_id = self.import_service.import_from_text(file_path)
            messagebox.showinfo("Success", "Test imported successfully!")
            self._refresh_test_list()
        except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
            messagebox.showerror("Import Error", str(e))
        except Exception as e:
            messagebox.showerror("Import Error", f"Unexpected error: {e}")

    def _on_new_test(self) -> None:
        """Navigate to editor for a new test."""
        self.controller.show_frame(SCREEN_EDITOR, test_id=None)

    def _on_view_history(self) -> None:
        """Navigate to history view."""
        self.controller.show_frame(SCREEN_HISTORY)

    def _on_review_missed(self) -> None:
        """Navigate to missed questions review."""
        self.controller.show_frame(SCREEN_REVIEW)

    def _on_analytics(self) -> None:
        """Navigate to analytics view."""
        self.controller.show_frame(SCREEN_ANALYTICS)

    def _on_take_test(self, test) -> None:
        """Show mode dialog, then navigate to test-taking."""
        dialog = ModeSelectionDialog(self.winfo_toplevel())
        mode = dialog.get_mode()
        if mode is None:
            return
        self.controller.show_frame(SCREEN_TEST_TAKING, test_id=test.id, mode=mode)

    def _on_edit_test(self, test) -> None:
        """Navigate to editor for an existing test."""
        self.controller.show_frame(SCREEN_EDITOR, test_id=test.id)

    def _on_delete_test(self, test) -> None:
        """Confirm and delete a test."""
        if messagebox.askyesno(
            "Confirm Delete",
            f'Are you sure you want to delete "{test.name}"?\n\n'
            "This will also delete all questions and attempt history.",
        ):
            self.test_service.delete_test(test.id)
            self._refresh_test_list()
