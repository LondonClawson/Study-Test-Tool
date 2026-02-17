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
from gui.components.mix_test_dialog import MixTestDialog
from gui.components.mode_dialog import ModeSelectionDialog
from services.export_service import ExportService
from services.import_service import ImportService
from services.mix_service import MixService
from services.question_service import QuestionService
from services.test_service import TestService
from utils.constants import (
    EXPORT_FILE_TYPES,
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
        self.question_service = QuestionService()
        self.import_service = ImportService()
        self.export_service = ExportService()
        self.mix_service = MixService()

        self._sort_by = "Last Updated"

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
            text="Mix Test",
            command=self._on_mix_test,
            width=120,
            fg_color="#7b2d8e",
            hover_color="#5e2270",
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

        # Sort toolbar
        sort_frame = ctk.CTkFrame(self, fg_color="transparent")
        sort_frame.pack(fill="x", padx=30, pady=(0, 5))

        ctk.CTkLabel(
            sort_frame,
            text="Sort by:",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
        ).pack(side="left", padx=(0, 5))

        self._sort_menu = ctk.CTkOptionMenu(
            sort_frame,
            values=[
                "Last Updated",
                "Name (A-Z)",
                "Name (Z-A)",
                "Date Created",
                "Group",
            ],
            width=150,
            command=self._on_sort_changed,
        )
        self._sort_menu.set(self._sort_by)
        self._sort_menu.pack(side="left")

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

    def _on_sort_changed(self, value: str) -> None:
        """Handle sort dropdown change."""
        self._sort_by = value
        self._refresh_test_list()

    def _sort_tests(self, tests):
        """Sort the test list based on current sort selection."""
        if self._sort_by == "Name (A-Z)":
            return sorted(tests, key=lambda t: t.name.lower())
        if self._sort_by == "Name (Z-A)":
            return sorted(tests, key=lambda t: t.name.lower(), reverse=True)
        if self._sort_by == "Date Created":
            return sorted(tests, key=lambda t: t.created_at or "", reverse=True)
        if self._sort_by == "Group":
            return sorted(
                tests, key=lambda t: (t.group_name or "", t.name.lower())
            )
        # Default: "Last Updated" — already sorted by DB query
        return tests

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

        tests = self._sort_tests(tests)

        if self._sort_by == "Group":
            current_group = None
            for test in tests:
                group = test.group_name if test.group_name else "Ungrouped"
                if group != current_group:
                    current_group = group
                    header = ctk.CTkLabel(
                        self.test_list_frame,
                        text=current_group,
                        font=(FONT_FAMILY, FONT_SIZE_HEADING, "bold"),
                        anchor="w",
                        text_color=COLOR_PRIMARY,
                    )
                    header.pack(fill="x", padx=5, pady=(12, 4))
                self._create_test_card(test)
        else:
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

        # Question count and group
        q_count = self.test_service.get_question_count(test.id)
        detail_parts = [f"{q_count} question{'s' if q_count != 1 else ''}"]
        if test.group_name:
            detail_parts.append(test.group_name)
        ctk.CTkLabel(
            info_frame,
            text="  |  ".join(detail_parts),
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
            text="Export",
            width=70,
            fg_color="#5cb85c",
            hover_color="#449d44",
            command=lambda t=test: self._on_export_test(t),
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

    def _on_mix_test(self) -> None:
        """Open mix test dialog, then start a mixed test."""
        tests = self.test_service.get_all_tests()
        tests_with_counts = []
        for test in tests:
            q_count = self.test_service.get_question_count(test.id)
            if q_count > 0:
                tests_with_counts.append((test, q_count))

        if not tests_with_counts:
            messagebox.showinfo(
                "No Tests",
                "No tests with questions available for mixing.",
            )
            return

        dialog = MixTestDialog(self.winfo_toplevel(), tests_with_counts)
        result = dialog.get_result()
        if result is None:
            return

        test_ids, count = result

        # Show mode selection
        mode_dialog = ModeSelectionDialog(self.winfo_toplevel())
        mode = mode_dialog.get_mode()
        if mode is None:
            return

        questions = self.mix_service.select_questions(test_ids, count)
        if not questions:
            messagebox.showwarning(
                "No Questions", "Could not load questions from selected tests."
            )
            return

        # Build display name from selected test names
        selected_tests = [t for t, _ in tests_with_counts if t.id in test_ids]
        name_parts = [t.name for t in selected_tests]
        mix_name = "Mix: " + ", ".join(name_parts)

        self.controller.show_frame(
            SCREEN_TEST_TAKING,
            mode=mode,
            questions=questions,
            mix_test_name=mix_name,
        )

    def _on_take_test(self, test) -> None:
        """Show mode dialog, then navigate to test-taking."""
        # Check for questions with no correct answer set
        questions = self.question_service.get_questions_for_test(test.id)
        missing = [q for q in questions if not q.correct_answer]
        if missing:
            proceed = messagebox.askyesno(
                "Missing Answers",
                f"{len(missing)} question(s) have no correct answer set. "
                "Scoring may not work correctly for those questions.\n\n"
                "Do you want to continue anyway?",
            )
            if not proceed:
                return

        dialog = ModeSelectionDialog(self.winfo_toplevel())
        mode = dialog.get_mode()
        if mode is None:
            return
        self.controller.show_frame(SCREEN_TEST_TAKING, test_id=test.id, mode=mode)

    def _on_edit_test(self, test) -> None:
        """Navigate to editor for an existing test."""
        self.controller.show_frame(SCREEN_EDITOR, test_id=test.id)

    def _on_export_test(self, test) -> None:
        """Validate and export a test to a JSON file."""
        try:
            warnings = self.export_service.validate_test(test.id)
        except ValueError as e:
            messagebox.showerror("Export Error", str(e))
            return

        if warnings:
            msg = "The following issues were found:\n\n"
            msg += "\n".join(f"  - {w}" for w in warnings)
            msg += "\n\nDo you want to export anyway?"
            if not messagebox.askyesno("Export Warnings", msg):
                return

        file_path = filedialog.asksaveasfilename(
            title="Export Test",
            defaultextension=".json",
            filetypes=EXPORT_FILE_TYPES,
            initialfile=f"{test.name}.json",
        )
        if not file_path:
            return

        try:
            self.export_service.export_to_json(test.id, file_path)
            messagebox.showinfo("Success", "Test exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Error", f"Unexpected error: {e}")

    def _on_delete_test(self, test) -> None:
        """Confirm and delete a test."""
        if messagebox.askyesno(
            "Confirm Delete",
            f'Are you sure you want to delete "{test.name}"?\n\n'
            "This will also delete all questions and attempt history.",
        ):
            self.test_service.delete_test(test.id)
            self._refresh_test_list()
