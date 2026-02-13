"""History view — browsable list of past test attempts."""

import threading
import tkinter.messagebox as messagebox

import customtkinter as ctk

from config.settings import (
    FONT_FAMILY,
    FONT_SIZE_BODY,
    FONT_SIZE_HEADING,
    FONT_SIZE_SMALL,
    FONT_SIZE_TITLE,
)
from services.scoring_service import ScoringService
from services.test_service import TestService
from utils.constants import SCREEN_HOME, SCREEN_RESULTS


class HistoryViewFrame(ctk.CTkFrame):
    """Displays filterable history of all test attempts."""

    def __init__(self, parent: ctk.CTkFrame, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.scoring_service = ScoringService()
        self.test_service = TestService()

        self._all_attempts = []
        self._tests = []

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the history layout."""
        # Top bar
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(20, 10))

        ctk.CTkButton(
            top_frame,
            text="< Back",
            width=80,
            fg_color="gray",
            command=lambda: self.controller.show_frame(SCREEN_HOME),
        ).pack(side="left")

        ctk.CTkLabel(
            top_frame,
            text="Test History",
            font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
        ).pack(side="left", padx=20)

        # Filter row
        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.pack(fill="x", padx=30, pady=(0, 10))

        ctk.CTkLabel(
            filter_frame,
            text="Filter by test:",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
        ).pack(side="left", padx=(0, 10))

        self.filter_var = ctk.StringVar(value="All Tests")
        self.filter_menu = ctk.CTkOptionMenu(
            filter_frame,
            variable=self.filter_var,
            values=["All Tests"],
            command=self._on_filter_change,
            width=250,
        )
        self.filter_menu.pack(side="left")

        ctk.CTkLabel(
            filter_frame,
            text="Mode:",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
        ).pack(side="left", padx=(20, 10))

        self.mode_filter_var = ctk.StringVar(value="All Modes")
        self.mode_filter_menu = ctk.CTkOptionMenu(
            filter_frame,
            variable=self.mode_filter_var,
            values=["All Modes", "Test", "Practice"],
            command=self._on_filter_change,
            width=150,
        )
        self.mode_filter_menu.pack(side="left")

        # Loading indicator
        self.loading_label = ctk.CTkLabel(
            self,
            text="Loading...",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
            text_color="gray",
        )

        # Table header
        self.table_header = ctk.CTkFrame(self, fg_color="transparent")
        self.table_header.pack(fill="x", padx=30)

        headers = [
            ("Date", 160),
            ("Test Name", 200),
            ("Mode", 80),
            ("Score", 80),
            ("%", 60),
            ("Time", 70),
        ]
        for text, width in headers:
            ctk.CTkLabel(
                self.table_header,
                text=text,
                font=(FONT_FAMILY, FONT_SIZE_SMALL, "bold"),
                width=width,
                anchor="w",
            ).pack(side="left", padx=5)

        # Scrollable table body
        self.table_body = ctk.CTkScrollableFrame(self)
        self.table_body.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        # Empty state
        self.empty_label = ctk.CTkLabel(
            self.table_body,
            text="No test history yet.",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
            text_color="gray",
        )

    def on_show(self, **kwargs) -> None:
        """Load data using a background thread."""
        self.loading_label.pack(pady=10)
        self._clear_table()

        thread = threading.Thread(target=self._load_data, daemon=True)
        thread.start()

    def _load_data(self) -> None:
        """Fetch attempts and tests from the DB (runs in background thread)."""
        try:
            attempts = self.scoring_service.get_all_attempts()
            tests = self.test_service.get_all_tests()
            self.after(0, lambda: self._on_data_loaded(attempts, tests))
        except Exception as e:
            self.after(0, lambda: self._on_load_error(str(e)))

    def _on_data_loaded(self, attempts, tests) -> None:
        """Update the UI with loaded data (runs on main thread)."""
        self.loading_label.pack_forget()
        self._all_attempts = attempts
        self._tests = tests

        # Update filter menu
        test_names = ["All Tests"] + [t.name for t in tests]
        self.filter_menu.configure(values=test_names)

        self._apply_filters()

    def _on_load_error(self, error: str) -> None:
        """Handle loading errors."""
        self.loading_label.pack_forget()
        messagebox.showerror("Error", f"Failed to load history: {error}")

    def _on_filter_change(self, value: str) -> None:
        """Apply all active filters."""
        self._apply_filters()

    def _apply_filters(self) -> None:
        """Filter attempts by test name and mode."""
        filtered = self._all_attempts

        test_filter = self.filter_var.get()
        if test_filter != "All Tests":
            filtered = [a for a in filtered if a.test_name == test_filter]

        mode_filter = self.mode_filter_var.get()
        if mode_filter != "All Modes":
            mode_val = mode_filter.lower()
            filtered = [a for a in filtered if a.mode == mode_val]

        self._display_attempts(filtered)

    def _clear_table(self) -> None:
        """Remove all rows from the table."""
        for widget in self.table_body.winfo_children():
            if widget != self.empty_label:
                widget.destroy()

    def _display_attempts(self, attempts) -> None:
        """Render the attempt list as table rows."""
        self._clear_table()

        if not attempts:
            self.empty_label.pack(pady=40)
            return

        self.empty_label.pack_forget()

        for attempt in attempts:
            self._create_row(attempt)

    def _create_row(self, attempt) -> None:
        """Create one clickable row in the history table."""
        row = ctk.CTkFrame(self.table_body, corner_radius=4, cursor="hand2")
        row.pack(fill="x", pady=2)

        # Make the whole row clickable
        row.bind(
            "<Button-1>",
            lambda e, a=attempt: self._on_row_click(a),
        )

        date_str = attempt.completed_at or "N/A"
        if len(date_str) > 16:
            date_str = date_str[:16]

        mode_label = attempt.mode.capitalize() if attempt.mode else "Test"

        values = [
            (date_str, 160),
            (attempt.test_name or "Unknown", 200),
            (mode_label, 80),
            (f"{attempt.score}/{attempt.total_questions}", 80),
            (f"{attempt.percentage}%", 60),
            (self._format_time(attempt.time_taken), 70),
        ]

        for text, width in values:
            lbl = ctk.CTkLabel(
                row,
                text=text,
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                width=width,
                anchor="w",
            )
            lbl.pack(side="left", padx=5, pady=5)
            lbl.bind(
                "<Button-1>",
                lambda e, a=attempt: self._on_row_click(a),
            )

    def _on_row_click(self, attempt) -> None:
        """Navigate to the detailed results view for this attempt."""
        self.controller.show_frame(SCREEN_RESULTS, attempt_id=attempt.id)

    @staticmethod
    def _format_time(seconds) -> str:
        """Format seconds to MM:SS."""
        if not seconds:
            return "N/A"
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"
