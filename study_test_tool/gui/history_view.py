"""History view — browsable list of past test attempts."""

import threading
import tkinter.messagebox as messagebox

import customtkinter as ctk

from gui.styles import (
    RADIUS_CONTROL,
    RADIUS_ROW,
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
from utils.constants import SCREEN_HOME, SCREEN_RESULTS

HISTORY_COLUMNS = (
    ("Date", 145, 2),
    ("Test Name", 220, 3),
    ("Mode", 90, 1),
    ("Score", 90, 1),
    ("%", 70, 1),
    ("Time", 80, 1),
)


class HistoryViewFrame(ctk.CTkFrame):
    """Displays filterable history of all test attempts."""

    def __init__(self, parent: ctk.CTkFrame, controller) -> None:
        super().__init__(parent, fg_color=get_color("app_bg"))
        self.controller = controller
        self.scoring_service = ScoringService()
        self.test_service = TestService()

        self._all_attempts = []
        self._tests = []

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the history layout."""
        page_header = ctk.CTkFrame(self, **get_header_style("page"))
        page_header.pack(fill="x", padx=SPACE_24, pady=(SPACE_24, SPACE_12))
        page_header.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            page_header,
            text="< Back",
            width=80,
            **get_button_style("secondary"),
            command=lambda: self.controller.show_frame(SCREEN_HOME),
        ).grid(row=0, column=0, padx=(SPACE_16, SPACE_12), pady=SPACE_16)

        title_frame = ctk.CTkFrame(page_header, fg_color="transparent")
        title_frame.grid(row=0, column=1, sticky="ew", pady=SPACE_12)

        ctk.CTkLabel(
            title_frame,
            text="Test History",
            **get_text_style("page_title"),
        ).pack(anchor="w")

        self.header_meta_label = ctk.CTkLabel(
            title_frame,
            text="Loading history",
            **get_text_style("page_subtitle"),
        )
        self.header_meta_label.pack(anchor="w", pady=(SPACE_4, 0))

        filter_frame = ctk.CTkFrame(self, **get_card_style("default"))
        filter_frame.pack(fill="x", padx=SPACE_24, pady=(0, SPACE_12))
        filter_frame.grid_columnconfigure(1, minsize=250)
        filter_frame.grid_columnconfigure(3, minsize=150)
        filter_frame.grid_columnconfigure(4, weight=1)

        ctk.CTkLabel(
            filter_frame,
            text="Test",
            **get_text_style("body"),
        ).grid(row=0, column=0, sticky="w", padx=(SPACE_16, SPACE_8), pady=SPACE_16)

        self.filter_var = ctk.StringVar(value="All Tests")
        self.filter_menu = ctk.CTkOptionMenu(
            filter_frame,
            variable=self.filter_var,
            values=["All Tests"],
            command=self._on_filter_change,
            width=250,
            **self._option_menu_style(),
        )
        self.filter_menu.grid(row=0, column=1, sticky="ew", pady=SPACE_16)

        ctk.CTkLabel(
            filter_frame,
            text="Mode",
            **get_text_style("body"),
        ).grid(row=0, column=2, sticky="w", padx=(SPACE_16, SPACE_8), pady=SPACE_16)

        self.mode_filter_var = ctk.StringVar(value="All Modes")
        self.mode_filter_menu = ctk.CTkOptionMenu(
            filter_frame,
            variable=self.mode_filter_var,
            values=["All Modes", "Test", "Practice"],
            command=self._on_filter_change,
            width=150,
            **self._option_menu_style(),
        )
        self.mode_filter_menu.grid(row=0, column=3, sticky="ew", pady=SPACE_16)

        self.count_label = ctk.CTkLabel(
            filter_frame,
            text="",
            anchor="e",
            **get_text_style("metadata"),
        )
        self.count_label.grid(
            row=0,
            column=4,
            sticky="e",
            padx=(SPACE_16, SPACE_16),
            pady=SPACE_16,
        )

        self.table_header = ctk.CTkFrame(
            self,
            fg_color=get_color("surface_subtle"),
            border_color=get_color("border"),
            border_width=1,
            corner_radius=RADIUS_ROW,
        )
        self.table_header.pack(fill="x", padx=SPACE_24, pady=(0, SPACE_8))
        self._configure_table_columns(self.table_header)

        for column, (text, _, _) in enumerate(HISTORY_COLUMNS):
            ctk.CTkLabel(
                self.table_header,
                text=text,
                anchor="w",
                **get_text_style("metadata"),
            ).grid(
                row=0,
                column=column,
                sticky="ew",
                padx=SPACE_8,
                pady=SPACE_8,
            )

        self.table_body = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=get_color("surface_muted"),
            scrollbar_button_hover_color=get_color("border"),
        )
        self.table_body.pack(
            fill="both",
            expand=True,
            padx=SPACE_24,
            pady=(0, SPACE_24),
        )

        self.loading_state = self._build_state_surface(
            self.table_body,
            "Loading history",
            "Preparing recent attempts.",
        )
        self.empty_state = self._build_state_surface(
            self.table_body,
            "No test history yet",
            "Complete a test or practice session to see attempts here.",
        )

    def _option_menu_style(self) -> dict:
        """Return semantic option-menu styling for History filters."""
        return {
            "fg_color": get_color("surface_subtle"),
            "button_color": get_color("primary"),
            "button_hover_color": get_color("primary_hover"),
            "dropdown_fg_color": get_color("surface"),
            "dropdown_hover_color": get_color("surface_subtle"),
            "dropdown_text_color": get_color("text_primary"),
            "text_color": get_color("text_primary"),
            "corner_radius": RADIUS_CONTROL,
        }

    @staticmethod
    def _configure_table_columns(frame: ctk.CTkFrame) -> None:
        """Apply shared column sizing to headers and attempt rows."""
        for index, (_, min_width, weight) in enumerate(HISTORY_COLUMNS):
            frame.grid_columnconfigure(index, minsize=min_width, weight=weight)

    def _build_state_surface(
        self,
        parent: ctk.CTkFrame,
        title: str,
        helper: str,
    ) -> ctk.CTkFrame:
        """Create an empty/loading state surface."""
        state = ctk.CTkFrame(parent, **get_card_style("default"))

        title_label = ctk.CTkLabel(
            state,
            text=title,
            anchor="center",
            **get_text_style("card_title"),
        )
        title_label.pack(pady=(SPACE_24, SPACE_4))

        helper_label = ctk.CTkLabel(
            state,
            text=helper,
            anchor="center",
            wraplength=520,
            **get_text_style("card_description"),
        )
        helper_label.pack(padx=SPACE_24, pady=(0, SPACE_24))

        state.title_label = title_label
        state.helper_label = helper_label
        return state

    def _show_loading_state(self) -> None:
        """Show the designed loading surface while background data loads."""
        self._clear_table()
        self.empty_state.pack_forget()
        self.loading_state.pack(fill="x", pady=SPACE_24)
        self.header_meta_label.configure(text="Loading history")
        self.count_label.configure(text="Loading...")

    def _show_empty_state(self, title: str, helper: str) -> None:
        """Show the designed empty state with state-specific text."""
        self.loading_state.pack_forget()
        self.empty_state.title_label.configure(text=title)
        self.empty_state.helper_label.configure(text=helper)
        self.empty_state.pack(fill="x", pady=SPACE_24)

    def _hide_state_surfaces(self) -> None:
        """Hide empty and loading surfaces."""
        self.loading_state.pack_forget()
        self.empty_state.pack_forget()

    def _update_attempt_summary(self, visible_count: int) -> None:
        """Update count labels without changing filtering behavior."""
        total_count = len(self._all_attempts)
        if total_count == 0:
            text = "No attempts"
        elif visible_count == total_count:
            text = f"{total_count} attempt{'s' if total_count != 1 else ''}"
        else:
            text = (
                f"Showing {visible_count} of {total_count} "
                f"attempt{'s' if total_count != 1 else ''}"
            )

        self.header_meta_label.configure(text=text)
        self.count_label.configure(text=text)

    def on_show(self, **kwargs) -> None:
        """Load data using a background thread."""
        self._show_loading_state()

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
        self.loading_state.pack_forget()
        self._all_attempts = attempts
        self._tests = tests

        test_names = ["All Tests"] + [t.name for t in tests]
        self.filter_menu.configure(values=test_names)

        self._apply_filters()

    def _on_load_error(self, error: str) -> None:
        """Handle loading errors."""
        self.loading_state.pack_forget()
        self.header_meta_label.configure(text="Unable to load history")
        self.count_label.configure(text="Load failed")
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
            if widget not in (self.empty_state, self.loading_state):
                widget.destroy()

    def _display_attempts(self, attempts) -> None:
        """Render the attempt list as table rows."""
        self._clear_table()
        self._update_attempt_summary(len(attempts))

        if not attempts:
            if self._all_attempts:
                self._show_empty_state(
                    "No matching attempts",
                    "Adjust the History filters to show more attempts.",
                )
            else:
                self._show_empty_state(
                    "No test history yet",
                    "Complete a test or practice session to see attempts here.",
                )
            return

        self._hide_state_surfaces()

        for attempt in attempts:
            self._create_row(attempt)

    def _create_row(self, attempt) -> None:
        """Create one clickable row in the history table."""
        row_style = get_card_style("default")
        row_style["corner_radius"] = RADIUS_ROW
        row = ctk.CTkFrame(self.table_body, cursor="hand2", **row_style)
        row.pack(fill="x", pady=(0, SPACE_8))
        self._configure_table_columns(row)

        self._bind_row_events(row, row, attempt)

        date_str = attempt.completed_at or "N/A"
        if len(date_str) > 16:
            date_str = date_str[:16]

        mode_label = attempt.mode.capitalize() if attempt.mode else "Test"

        values = [
            (date_str, "metadata"),
            (attempt.test_name or "Unknown", "body"),
            (mode_label, "metadata"),
            (f"{attempt.score}/{attempt.total_questions}", "body"),
            (f"{attempt.percentage}%", "body"),
            (self._format_time(attempt.time_taken), "metadata"),
        ]

        for column, (text, text_role) in enumerate(values):
            lbl = ctk.CTkLabel(
                row,
                text=text,
                anchor="w",
                wraplength=220 if column == 1 else 120,
                **get_text_style(text_role),
            )
            lbl.grid(
                row=0,
                column=column,
                sticky="ew",
                padx=SPACE_8,
                pady=SPACE_12,
            )
            self._bind_row_events(lbl, row, attempt)

    def _bind_row_events(self, widget, row: ctk.CTkFrame, attempt) -> None:
        """Attach shared click and hover affordances to a row child."""
        widget.bind("<Button-1>", lambda e, a=attempt: self._on_row_click(a))
        widget.bind(
            "<Enter>",
            lambda e, r=row: r.configure(fg_color=get_color("surface_subtle")),
        )
        widget.bind(
            "<Leave>",
            lambda e, r=row: r.configure(fg_color=get_color("surface")),
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
