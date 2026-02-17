"""Autocomplete entry widget — a text entry with a filtered dropdown."""

from typing import List, Optional

import customtkinter as ctk


class AutocompleteEntry(ctk.CTkFrame):
    """Entry with a dropdown that filters suggestions as the user types.

    Exposes .get(), .delete(), .insert() to match CTkEntry's interface.
    """

    def __init__(
        self,
        master,
        width: int = 200,
        placeholder_text: str = "",
        values: Optional[List[str]] = None,
        max_dropdown_items: int = 8,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._values: List[str] = values or []
        self._max_items = max_dropdown_items
        self._dropdown_visible = False

        self._entry = ctk.CTkEntry(
            self, width=width, placeholder_text=placeholder_text
        )
        self._entry.pack(fill="x")

        self._entry.bind("<KeyRelease>", self._on_key)
        self._entry.bind("<FocusIn>", self._on_focus_in)
        self._entry.bind("<Escape>", lambda e: self._close_dropdown())

        # Dropdown frame — placed as overlay below the entry
        self._dropdown_frame: Optional[ctk.CTkFrame] = None

    # ── Public interface (mirrors CTkEntry) ───────────────────

    def get(self) -> str:
        """Return the current entry text."""
        return self._entry.get()

    def delete(self, first, last=None) -> None:
        """Delete text from the entry."""
        self._entry.delete(first, last)

    def insert(self, index, text: str) -> None:
        """Insert text into the entry."""
        self._entry.insert(index, text)

    def configure(self, **kwargs):
        """Forward configuration to the inner entry."""
        self._entry.configure(**kwargs)

    def set_values(self, values: List[str]) -> None:
        """Update the list of autocomplete suggestions."""
        self._values = values

    # ── Grid geometry forwarding ──────────────────────────────

    def grid(self, **kwargs):
        """Forward grid call so the widget can be placed with grid."""
        super().grid(**kwargs)

    # ── Dropdown logic ────────────────────────────────────────

    def _on_key(self, event) -> None:
        """Handle key release — filter and show/hide dropdown."""
        if event.keysym in ("Escape", "Return", "Tab"):
            self._close_dropdown()
            return
        self._show_dropdown()

    def _on_focus_in(self, event) -> None:
        """Show dropdown when the entry gains focus (delayed to avoid click conflict)."""
        self.after(50, self._show_dropdown)

    def _get_filtered(self) -> List[str]:
        """Return values matching the current text (case-insensitive)."""
        text = self._entry.get().strip().lower()
        if not text:
            return self._values[: self._max_items]
        return [
            v for v in self._values if text in v.lower()
        ][: self._max_items]

    def _show_dropdown(self) -> None:
        """Display or refresh the dropdown below the entry."""
        matches = self._get_filtered()
        if not matches:
            self._close_dropdown()
            return

        # Destroy old dropdown so we rebuild with fresh items
        if self._dropdown_frame is not None:
            self._dropdown_frame.destroy()
            self._dropdown_frame = None

        # Use the top-level window for overlay placement
        toplevel = self.winfo_toplevel()

        # Calculate absolute position of the entry within the toplevel
        self.update_idletasks()
        entry_x = self._entry.winfo_rootx() - toplevel.winfo_rootx()
        entry_y = self._entry.winfo_rooty() - toplevel.winfo_rooty()
        entry_h = self._entry.winfo_height()
        entry_w = self._entry.winfo_width()

        item_height = 30
        dropdown_height = min(len(matches) * item_height + 10, self._max_items * item_height + 10)

        self._dropdown_frame = ctk.CTkFrame(
            toplevel,
            width=entry_w,
            height=dropdown_height,
            corner_radius=4,
        )
        self._dropdown_frame.place(
            x=entry_x, y=entry_y + entry_h + 2
        )
        # Raise above other widgets
        self._dropdown_frame.lift()

        for value in matches:
            btn = ctk.CTkButton(
                self._dropdown_frame,
                text=value,
                anchor="w",
                height=item_height,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray80", "gray30"),
                command=lambda v=value: self._select(v),
            )
            btn.pack(fill="x", padx=2, pady=1)

        self._dropdown_visible = True

        # Close dropdown when clicking elsewhere
        toplevel.bind("<Button-1>", self._on_click_outside, add="+")

    def _select(self, value: str) -> None:
        """Fill the entry with the selected value and close dropdown."""
        self._entry.delete(0, "end")
        self._entry.insert(0, value)
        self._close_dropdown()

    def _close_dropdown(self) -> None:
        """Remove the dropdown overlay."""
        if self._dropdown_frame is not None:
            self._dropdown_frame.place_forget()
            self._dropdown_frame.destroy()
            self._dropdown_frame = None
        self._dropdown_visible = False
        try:
            self.winfo_toplevel().unbind("<Button-1>")
        except Exception:
            pass

    def _is_click_inside(self, widget, x_root: int, y_root: int) -> bool:
        """Check if root coordinates fall within a widget's bounding box."""
        try:
            wx = widget.winfo_rootx()
            wy = widget.winfo_rooty()
            ww = widget.winfo_width()
            wh = widget.winfo_height()
            return wx <= x_root <= wx + ww and wy <= y_root <= wy + wh
        except Exception:
            return False

    def _on_click_outside(self, event) -> None:
        """Close dropdown if the click is outside the dropdown and entry."""
        if not self._dropdown_visible:
            return
        # Check if click landed inside the entry or dropdown by coordinates
        if self._is_click_inside(self._entry, event.x_root, event.y_root):
            return
        if self._dropdown_frame is not None:
            if self._is_click_inside(self._dropdown_frame, event.x_root, event.y_root):
                return
        self._close_dropdown()
