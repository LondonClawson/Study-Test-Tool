"""Import preview dialog with optional group assignment."""

from typing import List, Optional, Tuple

import customtkinter as ctk

from config.settings import (
    COLOR_DANGER,
    COLOR_PRIMARY,
    FONT_FAMILY,
    FONT_SIZE_BODY,
    FONT_SIZE_HEADING,
    FONT_SIZE_SMALL,
)
from services.import_preview_service import ImportPreview


class ImportPreviewDialog(ctk.CTkToplevel):
    """Modal confirmation dialog shown before committing imported tests."""

    def __init__(self, parent, previews: List[ImportPreview]) -> None:
        super().__init__(parent)
        self.title("Import Preview")
        self.geometry("620x560")
        self.resizable(False, False)

        self._previews = previews
        self._result: Optional[Tuple[bool, str]] = None
        self._group_entry: Optional[ctk.CTkEntry] = None

        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - 620) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - 560) // 2
        self.geometry(f"+{x}+{y}")

    def _build_ui(self) -> None:
        importable = [preview for preview in self._previews if not preview.errors]
        skipped = [preview for preview in self._previews if preview.errors]
        total_questions = sum(preview.question_count for preview in importable)

        ctk.CTkLabel(
            self,
            text="Import Preview",
            font=(FONT_FAMILY, FONT_SIZE_HEADING, "bold"),
        ).pack(pady=(15, 4))

        ctk.CTkLabel(
            self,
            text=(
                f"{len(importable)} test(s), {total_questions} question(s) ready. "
                f"{len(skipped)} skipped."
            ),
            font=(FONT_FAMILY, FONT_SIZE_BODY),
            text_color="gray",
        ).pack(pady=(0, 10))

        group_frame = ctk.CTkFrame(self, fg_color="transparent")
        group_frame.pack(fill="x", padx=25, pady=(0, 10))
        ctk.CTkLabel(
            group_frame,
            text="Group:",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
        ).pack(side="left", padx=(0, 8))
        self._group_entry = ctk.CTkEntry(group_frame)
        self._group_entry.pack(side="left", fill="x", expand=True)

        existing_groups = sorted({p.group_name for p in importable if p.group_name})
        if len(existing_groups) == 1:
            self._group_entry.insert(0, existing_groups[0])

        scroll = ctk.CTkScrollableFrame(self, height=350)
        scroll.pack(fill="both", expand=True, padx=25, pady=5)

        for preview in self._previews:
            self._add_preview_row(scroll, preview)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=25, pady=(10, 15))

        import_button = ctk.CTkButton(
            btn_frame,
            text="Import",
            width=120,
            fg_color=COLOR_PRIMARY,
            command=self._on_import,
        )
        import_button.pack(side="left", padx=5, expand=True)
        if not importable:
            import_button.configure(state="disabled")

        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=100,
            fg_color="gray",
            command=self._on_cancel,
        ).pack(side="right", padx=5, expand=True)

    def _add_preview_row(self, parent, preview: ImportPreview) -> None:
        row = ctk.CTkFrame(parent)
        row.pack(fill="x", pady=5, padx=3)

        status = "Skipped" if preview.errors else "Ready"
        color = COLOR_DANGER if preview.errors else COLOR_PRIMARY
        ctk.CTkLabel(
            row,
            text=f"{status}: {preview.test_name}",
            font=(FONT_FAMILY, FONT_SIZE_BODY, "bold"),
            text_color=color,
            anchor="w",
        ).pack(fill="x", padx=10, pady=(8, 2))

        ctk.CTkLabel(
            row,
            text=f"{preview.source_name} - {preview.question_count} question(s)",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color="gray",
            anchor="w",
        ).pack(fill="x", padx=10)

        messages = preview.errors or preview.warnings
        if messages:
            text = "\n".join(f"- {message}" for message in messages[:4])
            if len(messages) > 4:
                text += f"\n- {len(messages) - 4} more message(s)"
            ctk.CTkLabel(
                row,
                text=text,
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                text_color=COLOR_DANGER if preview.errors else "gray",
                anchor="w",
                justify="left",
                wraplength=560,
            ).pack(fill="x", padx=10, pady=(4, 8))
        else:
            ctk.CTkLabel(
                row,
                text="No warnings.",
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                text_color="gray",
                anchor="w",
            ).pack(fill="x", padx=10, pady=(4, 8))

    def _on_import(self) -> None:
        group_name = self._group_entry.get().strip() if self._group_entry else ""
        self._result = (True, group_name)
        self.destroy()

    def _on_cancel(self) -> None:
        self._result = (False, "")
        self.destroy()

    def get_result(self) -> Optional[Tuple[bool, str]]:
        """Return ``(confirmed, group_name)`` after the dialog closes."""
        self.wait_window()
        return self._result
