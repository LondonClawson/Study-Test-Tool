#!/usr/bin/env python3
"""Capture visual-overhaul baseline screenshots with seeded app data.

This is a development-only harness. It creates an isolated SQLite database,
drives the CustomTkinter app through its frame controller, and captures named
screenshots for the visual overhaul audit. It does not touch the user's normal
application database.
"""

from __future__ import annotations

import argparse
import colorsys
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = REPO_ROOT / "study_test_tool"
DEFAULT_OUTPUT_DIR = (
    REPO_ROOT / "visual_overhaul_project" / "01_context" / "screenshots" / "baseline"
)
GROUPS = (
    "all",
    "home",
    "dialogs",
    "editor",
    "test-taking",
    "results",
    "data",
    "empty",
)

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

try:
    from PIL import Image, ImageStat
except ImportError as exc:  # pragma: no cover - environment guard
    missing = exc.name or "required dependency"
    raise SystemExit(f"Missing {missing}. Install app requirements first.") from exc

try:
    import customtkinter as ctk
except ImportError:  # pragma: no cover - validate-only can run without GUI deps
    ctk = None

try:
    import Quartz
except ImportError:  # pragma: no cover - validate-only can run without Quartz
    Quartz = None

import config.database as database_config
import config.settings as settings
from config.database import initialize_database
from database.db_manager import DatabaseManager
from models.question import Question, QuestionOption
from models.test_result import QuestionResponse, TestAttempt
from services.scoring_service import ScoringService
from services.test_session import TestSession
from utils.constants import (
    MODE_PRACTICE,
    MODE_TEST,
    SCREEN_ANALYTICS,
    SCREEN_EDITOR,
    SCREEN_HISTORY,
    SCREEN_HOME,
    SCREEN_RESULTS,
    SCREEN_REVIEW,
    SCREEN_TEST_TAKING,
)

App = None
MixTestDialog = None
ModeSelectionDialog = None


def ensure_gui_modules() -> None:
    """Load GUI modules only when capture mode needs them."""
    global App, MixTestDialog, ModeSelectionDialog

    if ctk is None:
        raise RuntimeError("customtkinter is required for capture.")
    if App is not None:
        return

    from gui.components.mix_test_dialog import MixTestDialog as ImportedMixTestDialog
    from gui.components.mode_dialog import (
        ModeSelectionDialog as ImportedModeSelectionDialog,
    )
    from gui.main_window import App as ImportedApp

    App = ImportedApp
    MixTestDialog = ImportedMixTestDialog
    ModeSelectionDialog = ImportedModeSelectionDialog


@dataclass
class SeedData:
    """IDs and objects needed to drive screenshot states."""

    db_path: Path
    active_test_id: int
    second_test_id: int
    essay_test_id: int
    archived_test_id: int
    empty_attempt_id: int
    partial_attempt_id: int
    high_attempt_id: int
    questions_by_test: Dict[int, List[Question]]


@dataclass(frozen=True)
class CaptureState:
    """A named visual state the harness can capture."""

    name: str
    group: str
    source: str
    action: Callable[
        ["App", Optional[SeedData], "ScreenshotHarness"],
        Optional[Callable[[], None]],
    ]


@dataclass
class ValidationResult:
    """Validation outcome for one screenshot."""

    path: Path
    ok: bool
    reason: str = ""


class ScreenshotHarness:
    """Drive app states and capture screenshots."""

    def __init__(self, app: App, output_dir: Path, mode: str) -> None:
        self.app = app
        self.output_dir = output_dir
        self.mode = mode

    def capture(self, name: str) -> None:
        """Capture the current app window."""
        self._settle()
        target = self.output_dir / self.mode / f"{self.mode}_{name}.png"
        target.parent.mkdir(parents=True, exist_ok=True)
        bounds = self._find_app_bounds()
        if bounds is None:
            raise RuntimeError("Could not find the Study Testing Tool window.")
        rect = self._screencapture_rect(bounds)
        subprocess.run(
            [
                "screencapture",
                "-x",
                "-R",
                f"{rect[0]},{rect[1]},{rect[2]},{rect[3]}",
                str(target),
            ],
            check=True,
        )
        print(f"captured {target.relative_to(REPO_ROOT)}")

    def show_frame(self, screen_name: str, **kwargs) -> None:
        """Raise an app frame and wait for Tk to render it."""
        self.app.show_frame(screen_name, **kwargs)
        self._settle()

    def show_history_sync(self) -> None:
        """Raise history and load table data without its background thread."""
        self.app._current_screen = SCREEN_HISTORY
        frame = self.app.frames[SCREEN_HISTORY]
        frame.tkraise()
        frame.loading_label.pack(pady=10)
        frame._clear_table()
        attempts = frame.scoring_service.get_all_attempts()
        tests = frame.test_service.get_all_tests()
        frame._on_data_loaded(attempts, tests)
        self._settle()

    def _settle(self) -> None:
        """Let Tk and the macOS compositor catch up before capture."""
        self.app.update_idletasks()
        self.app.update()
        time.sleep(0.25)
        self.app.update_idletasks()
        self.app.update()

    def _find_app_bounds(self) -> Optional[Dict[str, int]]:
        """Return CoreGraphics bounds for the main app window."""
        if Quartz is None:
            raise RuntimeError(
                "PyObjC Quartz is required for capture. Install "
                "pyobjc-framework-Quartz."
            )
        windows = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListOptionOnScreenOnly,
            Quartz.kCGNullWindowID,
        )
        if not windows:
            return None

        candidates = []
        for window in windows:
            owner = window.get("kCGWindowOwnerName")
            bounds = window.get("kCGWindowBounds") or {}
            if owner != "Python":
                continue
            if bounds.get("Width", 0) < 700 or bounds.get("Height", 0) < 500:
                continue
            candidates.append(bounds)

        if not candidates:
            return None
        return max(candidates, key=lambda b: b.get("Width", 0) * b.get("Height", 0))

    def _screencapture_rect(self, bounds: Dict[str, int]) -> tuple[int, int, int, int]:
        """Convert CoreGraphics point bounds into screencapture pixels."""
        scale = self._display_scale(bounds)
        x = int(bounds["X"] * scale)
        y = int(bounds["Y"] * scale)
        width = int(bounds["Width"] * scale)
        height = int(bounds["Height"] * scale)
        return x, y, width, height

    def _display_scale(self, bounds: Dict[str, int]) -> float:
        """Find the backing scale for the display containing the window."""
        displays = Quartz.CGGetActiveDisplayList(16, None, None)[1]
        center_x = bounds["X"] + bounds["Width"] / 2
        center_y = bounds["Y"] + bounds["Height"] / 2

        for display_id in displays:
            display_bounds = Quartz.CGDisplayBounds(display_id)
            if (
                display_bounds.origin.x
                <= center_x
                <= display_bounds.origin.x + display_bounds.size.width
                and display_bounds.origin.y
                <= center_y
                <= display_bounds.origin.y + display_bounds.size.height
            ):
                pixel_width = Quartz.CGDisplayPixelsWide(display_id)
                return pixel_width / display_bounds.size.width
        return 1.0


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Capture seeded baseline screenshots for the visual overhaul."
    )
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Appearance mode to capture.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Screenshot output root.",
    )
    parser.add_argument(
        "--keep-db",
        action="store_true",
        help="Keep the temporary seeded database for debugging.",
    )
    parser.add_argument(
        "--states",
        nargs="*",
        help="Optional list of state names to capture. Takes precedence over --group.",
    )
    parser.add_argument(
        "--group",
        choices=GROUPS,
        default="all",
        help="Capture a named group of states.",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate expected screenshots without launching the GUI.",
    )
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip post-capture screenshot validation.",
    )
    return parser.parse_args()


def configure_database(db_path: Path) -> None:
    """Point app services at an isolated database."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    initialize_database(str(db_path))
    settings.DB_PATH = db_path
    database_config.DB_PATH = db_path


def add_question(
    db: DatabaseManager,
    test_id: int,
    text: str,
    correct_answer: str,
    category: str,
    options: Optional[List[str]] = None,
) -> int:
    """Insert a multiple-choice or essay question."""
    if options is None:
        question = Question(
            test_id=test_id,
            text=text,
            type=settings.QUESTION_TYPE_ESSAY,
            correct_answer=correct_answer,
            category=category,
        )
    else:
        question = Question(
            test_id=test_id,
            text=text,
            type=settings.QUESTION_TYPE_MC,
            correct_answer=correct_answer,
            category=category,
            options=[
                QuestionOption(text=option, is_correct=option == correct_answer)
                for option in options
            ],
        )
    return db.add_question(question)


def save_attempt(
    db: DatabaseManager,
    test_id: int,
    responses: Iterable[QuestionResponse],
    score: int,
    total_questions: int,
    percentage: float,
    mode: str = MODE_TEST,
    time_taken: int = 420,
) -> int:
    """Insert an attempt and its responses."""
    attempt_id = db.save_attempt(
        TestAttempt(
            test_id=test_id,
            score=score,
            total_questions=total_questions,
            percentage=percentage,
            time_taken=time_taken,
            mode=mode,
        )
    )
    for response in responses:
        response.attempt_id = attempt_id
        db.save_response(response)
    return attempt_id


def seed_database(db_path: Path) -> SeedData:
    """Create representative app data for visual capture."""
    db_path.unlink(missing_ok=True)
    configure_database(db_path)
    db = DatabaseManager(str(db_path))

    active_test_id = db.create_test(
        settings_test(
            "Cardiology Board Review",
            "High-yield practice set with categories and mixed question types.",
            "Clinical Medicine",
        )
    )
    second_test_id = db.create_test(
        settings_test(
            "Pharmacology Quick Drill",
            "Medication mechanism and safety review.",
            "Clinical Medicine",
        )
    )
    essay_test_id = db.create_test(
        settings_test(
            "Pathophysiology Essays",
            "Short-answer prompts for explaining mechanisms.",
            "",
        )
    )
    archived_test_id = db.create_test(
        settings_test(
            "Archived Anatomy Final",
            "Older final exam prep set retained for reference.",
            "Archived Courses",
        )
    )

    active_questions = [
        add_question(
            db,
            active_test_id,
            "Which finding most strongly supports acute decompensated heart failure?",
            "Bilateral pulmonary crackles with elevated BNP",
            "Cardiology",
            [
                "Normal jugular venous pressure",
                "Bilateral pulmonary crackles with elevated BNP",
                "Isolated wheezing after exercise",
                "Low serum creatinine",
            ],
        ),
        add_question(
            db,
            active_test_id,
            "A patient with atrial fibrillation needs stroke-risk counseling. Which score is commonly used?",
            "CHA2DS2-VASc",
            "Cardiology",
            ["CURB-65", "Wells", "CHA2DS2-VASc", "APACHE II"],
        ),
        add_question(
            db,
            active_test_id,
            "Explain why loop diuretics can cause hypokalemia.",
            "Increased distal sodium delivery promotes potassium secretion.",
            "Renal",
            None,
        ),
    ]
    second_questions = [
        add_question(
            db,
            second_test_id,
            "Which medication class is first-line for anaphylaxis?",
            "Epinephrine",
            "Emergency",
            ["Diphenhydramine", "Epinephrine", "Albuterol", "Prednisone"],
        ),
        add_question(
            db,
            second_test_id,
            "Which adverse effect is most associated with aminoglycosides?",
            "Ototoxicity",
            "Pharmacology",
            ["Ototoxicity", "Hyperkalemia", "Photosensitivity", "Sedation"],
        ),
    ]
    essay_questions = [
        add_question(
            db,
            essay_test_id,
            "Compare preload and afterload in one concise paragraph.",
            "Preload reflects ventricular filling; afterload reflects ejection resistance.",
            "Physiology",
            None,
        )
    ]
    archived_questions = [
        add_question(
            db,
            archived_test_id,
            "Which structure passes through the foramen magnum?",
            "Medulla oblongata",
            "Anatomy",
            ["Optic nerve", "Medulla oblongata", "Facial nerve", "Carotid artery"],
        )
    ]
    db.archive_test(archived_test_id)

    partial_attempt_id = save_attempt(
        db,
        active_test_id,
        [
            QuestionResponse(
                active_questions[0], "Normal jugular venous pressure", False, True, 65
            ),
            QuestionResponse(active_questions[1], "CHA2DS2-VASc", True, False, 44),
            QuestionResponse(
                active_questions[2],
                "Loop diuretics increase sodium delivery downstream.",
                None,
                False,
                120,
            ),
        ],
        score=1,
        total_questions=3,
        percentage=50.0,
        mode=MODE_TEST,
    )
    high_attempt_id = save_attempt(
        db,
        second_test_id,
        [
            QuestionResponse(second_questions[0], "Epinephrine", True, False, 35),
            QuestionResponse(second_questions[1], "Ototoxicity", True, False, 42),
        ],
        score=2,
        total_questions=2,
        percentage=100.0,
        mode=MODE_PRACTICE,
    )
    empty_attempt_id = save_attempt(
        db,
        essay_test_id,
        [
            QuestionResponse(
                essay_questions[0],
                "Preload is filling; afterload is resistance.",
                None,
                False,
                95,
            )
        ],
        score=0,
        total_questions=1,
        percentage=0.0,
        mode=MODE_TEST,
    )

    return SeedData(
        db_path=db_path,
        active_test_id=active_test_id,
        second_test_id=second_test_id,
        essay_test_id=essay_test_id,
        archived_test_id=archived_test_id,
        empty_attempt_id=empty_attempt_id,
        partial_attempt_id=partial_attempt_id,
        high_attempt_id=high_attempt_id,
        questions_by_test={
            active_test_id: DatabaseManager(str(db_path)).get_questions_for_test(
                active_test_id
            ),
            second_test_id: DatabaseManager(str(db_path)).get_questions_for_test(
                second_test_id
            ),
            essay_test_id: DatabaseManager(str(db_path)).get_questions_for_test(
                essay_test_id
            ),
            archived_test_id: DatabaseManager(str(db_path)).get_questions_for_test(
                archived_test_id
            ),
        },
    )


def settings_test(name: str, description: str, group_name: str):
    """Create a Test model without importing it at module top for readability."""
    from models.test import Test

    return Test(name=name, description=description, group_name=group_name)


def create_results_session(seed: SeedData) -> tuple[TestSession, dict]:
    """Create an unsaved session with flagged, incorrect, and essay responses."""
    questions = seed.questions_by_test[seed.active_test_id]
    session = TestSession(seed.active_test_id, questions, mode=MODE_TEST)
    session.start()
    session.save_response(questions[0].id, "Normal jugular venous pressure")
    session.save_response(questions[1].id, "CHA2DS2-VASc")
    session.save_response(questions[2].id, "Increased distal sodium delivery.")
    session.flag_question(questions[0].id)
    score_data = ScoringService(str(seed.db_path)).score_test(session)
    score_data["time_taken"] = 540
    return session, score_data


def create_mix_questions(seed: SeedData) -> List[Question]:
    """Return questions from multiple tests for mix-test screenshots."""
    return (
        seed.questions_by_test[seed.active_test_id][:2]
        + seed.questions_by_test[seed.second_test_id][:2]
    )


def capture_dialog(
    app: App,
    harness: ScreenshotHarness,
    factory: Callable[[], ctk.CTkToplevel],
) -> Callable[[], None]:
    """Open a CTk dialog and return a cleanup callback."""
    dialog = factory()
    app.update_idletasks()
    app.update()

    def cleanup() -> None:
        dialog.destroy()
        app.update_idletasks()
        app.update()

    return cleanup


def show_home(app: App, seed: Optional[SeedData], harness: ScreenshotHarness) -> None:
    """Show the populated home screen."""
    harness.show_frame(SCREEN_HOME)


def show_mode_dialog(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> Callable[[], None]:
    """Show the mode selection dialog."""
    harness.show_frame(SCREEN_HOME)
    return capture_dialog(app, harness, lambda: ModeSelectionDialog(app))


def show_mix_dialog(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> Callable[[], None]:
    """Show the mix-test dialog."""
    tests_with_counts = [
        (DatabaseManager(str(seed.db_path)).get_test_by_id(seed.active_test_id), 3),
        (DatabaseManager(str(seed.db_path)).get_test_by_id(seed.second_test_id), 2),
        (DatabaseManager(str(seed.db_path)).get_test_by_id(seed.essay_test_id), 1),
    ]
    harness.show_frame(SCREEN_HOME)
    return capture_dialog(app, harness, lambda: MixTestDialog(app, tests_with_counts))


def show_editor_new(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the new-test editor state."""
    harness.show_frame(SCREEN_EDITOR, test_id=None)


def show_editor_existing(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the existing-test editor state."""
    harness.show_frame(SCREEN_EDITOR, test_id=seed.active_test_id)


def show_test_unanswered(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show an unanswered test-taking question."""
    harness.show_frame(SCREEN_TEST_TAKING, test_id=seed.active_test_id, mode=MODE_TEST)


def show_test_answered_flagged(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show an answered and flagged test-taking question."""
    harness.show_frame(SCREEN_TEST_TAKING, test_id=seed.active_test_id, mode=MODE_TEST)
    frame = app.frames[SCREEN_TEST_TAKING]
    question = frame._session.get_current_question()
    frame._question_widget.set_answer(question.correct_answer)
    frame._save_current_answer()
    frame._session.flag_question(question.id)
    frame._display_question()


def show_practice_feedback(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show practice-mode incorrect feedback."""
    harness.show_frame(
        SCREEN_TEST_TAKING, test_id=seed.active_test_id, mode=MODE_PRACTICE
    )
    frame = app.frames[SCREEN_TEST_TAKING]
    frame._question_widget.set_answer("Normal jugular venous pressure")
    frame._on_check_answer()


def show_essay_question(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show an essay question in the test-taking screen."""
    harness.show_frame(SCREEN_TEST_TAKING, test_id=seed.active_test_id, mode=MODE_TEST)
    frame = app.frames[SCREEN_TEST_TAKING]
    essay_index = next(
        index
        for index, question in enumerate(frame._session.questions)
        if question.type == settings.QUESTION_TYPE_ESSAY
    )
    frame._session.go_to_question(essay_index)
    frame._display_question()


def show_mix_test(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show a mixed test-taking session."""
    harness.show_frame(
        SCREEN_TEST_TAKING,
        mode=MODE_TEST,
        questions=create_mix_questions(seed),
        mix_test_name="Mixed Clinical Review",
    )


def show_results_session(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show just-completed results with partial score, essay, and flag data."""
    session, score_data = create_results_session(seed)
    harness.show_frame(SCREEN_RESULTS, session=session, score_data=score_data)


def show_results_history(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show results loaded from persisted history."""
    harness.show_frame(SCREEN_RESULTS, attempt_id=seed.partial_attempt_id)


def show_history(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show history with data loaded synchronously."""
    harness.show_history_sync()


def show_analytics(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show analytics with populated data."""
    harness.show_frame(SCREEN_ANALYTICS)


def show_review(app: App, seed: Optional[SeedData], harness: ScreenshotHarness) -> None:
    """Show missed-question review."""
    harness.show_frame(SCREEN_REVIEW)


def show_empty_home(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the empty home state."""
    harness.show_frame(SCREEN_HOME)


def show_empty_history(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the empty history state."""
    harness.show_history_sync()


def show_empty_analytics(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the analytics no-data state."""
    harness.show_frame(SCREEN_ANALYTICS)


def show_empty_review(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the empty review state."""
    harness.show_frame(SCREEN_REVIEW)


CAPTURE_STATES = [
    CaptureState("home_populated_grouped", "home", "seeded", show_home),
    CaptureState("mode_selection_dialog", "dialogs", "seeded", show_mode_dialog),
    CaptureState("mix_test_dialog", "dialogs", "seeded", show_mix_dialog),
    CaptureState("editor_new_test", "editor", "seeded", show_editor_new),
    CaptureState(
        "editor_existing_test_with_questions",
        "editor",
        "seeded",
        show_editor_existing,
    ),
    CaptureState(
        "test_taking_unanswered", "test-taking", "seeded", show_test_unanswered
    ),
    CaptureState(
        "test_taking_answered_flagged",
        "test-taking",
        "seeded",
        show_test_answered_flagged,
    ),
    CaptureState(
        "test_taking_practice_incorrect_feedback",
        "test-taking",
        "seeded",
        show_practice_feedback,
    ),
    CaptureState(
        "test_taking_essay_question", "test-taking", "seeded", show_essay_question
    ),
    CaptureState("test_taking_mix_test", "test-taking", "seeded", show_mix_test),
    CaptureState(
        "results_partial_score_essay_flagged",
        "results",
        "seeded",
        show_results_session,
    ),
    CaptureState(
        "results_loaded_from_history", "results", "seeded", show_results_history
    ),
    CaptureState("history_populated", "data", "seeded", show_history),
    CaptureState("analytics_populated", "data", "seeded", show_analytics),
    CaptureState("review_missed_questions", "data", "seeded", show_review),
    CaptureState("home_empty_state", "empty", "empty", show_empty_home),
    CaptureState("history_empty_state", "empty", "empty", show_empty_history),
    CaptureState("analytics_no_data", "empty", "empty", show_empty_analytics),
    CaptureState("review_empty_state", "empty", "empty", show_empty_review),
]


def selected_capture_states(args: argparse.Namespace) -> List[CaptureState]:
    """Return states selected by --states or --group."""
    if args.states:
        known = {state.name: state for state in CAPTURE_STATES}
        missing = sorted(set(args.states) - set(known))
        if missing:
            raise SystemExit(f"Unknown capture state(s): {', '.join(missing)}")
        return [known[name] for name in args.states]
    if args.group == "all":
        return list(CAPTURE_STATES)
    return [state for state in CAPTURE_STATES if state.group == args.group]


def capture_state_group(
    app: App,
    seed: Optional[SeedData],
    harness: ScreenshotHarness,
    states: Sequence[CaptureState],
) -> None:
    """Capture states for one database source."""
    for state in states:
        cleanup = state.action(app, seed, harness)
        try:
            harness.capture(state.name)
        finally:
            if cleanup is not None:
                cleanup()


def create_app(mode: str) -> App:
    """Create the app and force the requested appearance mode."""
    if ctk is None:
        raise RuntimeError("customtkinter is required for capture.")
    app = App()
    ctk.set_appearance_mode(mode)
    app.geometry("1000x700+80+80")
    app.update_idletasks()
    app.update()
    return app


def selected_modes(mode: str) -> List[str]:
    """Expand a mode argument into concrete appearance modes."""
    return ["light", "dark"] if mode == "both" else [mode]


def expected_screenshot_paths(
    output_dir: Path,
    modes: Sequence[str],
    states: Sequence[CaptureState],
) -> List[Path]:
    """Return expected screenshot paths for modes and states."""
    return [
        output_dir / mode / f"{mode}_{state.name}.png"
        for mode in modes
        for state in states
    ]


def validate_screenshot(path: Path) -> ValidationResult:
    """Validate one screenshot file."""
    if not path.exists():
        return ValidationResult(path, False, "missing")

    try:
        with Image.open(path) as image:
            image = image.convert("RGB")
            width, height = image.size
            if width < 900 or height < 600:
                return ValidationResult(path, False, f"too small: {width}x{height}")

            stat = ImageStat.Stat(image)
            if max(stat.stddev) < 2.0:
                return ValidationResult(path, False, "near-uniform image")

            if looks_desktop_only(image):
                return ValidationResult(path, False, "looks like desktop-only capture")
    except Exception as exc:
        return ValidationResult(path, False, f"unreadable: {exc}")

    return ValidationResult(path, True)


def looks_desktop_only(image: Image.Image) -> bool:
    """Heuristically detect wallpaper-only captures."""
    sample = image.resize((80, 80))
    if hasattr(sample, "get_flattened_data"):
        pixels = list(sample.get_flattened_data())
    else:
        pixels = list(sample.getdata())
    saturated_purple_blue = 0
    neutral = 0

    for red, green, blue in pixels:
        hue, saturation, value = colorsys.rgb_to_hsv(
            red / 255,
            green / 255,
            blue / 255,
        )
        hue_degrees = hue * 360
        if 220 <= hue_degrees <= 320 and saturation > 0.45 and value > 0.2:
            saturated_purple_blue += 1
        if saturation < 0.18 and value > 0.08:
            neutral += 1

    total = len(pixels)
    return saturated_purple_blue / total > 0.55 and neutral / total < 0.12


def validate_screenshots(paths: Sequence[Path]) -> bool:
    """Validate screenshot files and print a concise summary."""
    results = [validate_screenshot(path) for path in paths]
    failures = [result for result in results if not result.ok]

    if failures:
        print(f"validation failed: {len(failures)} of {len(results)} file(s)")
        for failure in failures:
            try:
                rel_path = failure.path.relative_to(REPO_ROOT)
            except ValueError:
                rel_path = failure.path
            print(f"- {rel_path}: {failure.reason}")
        return False

    print(f"validation passed: {len(results)} screenshot(s)")
    return True


def run_capture(args: argparse.Namespace) -> None:
    """Seed data, launch the app, and capture requested states."""
    tmp_dir = Path(tempfile.mkdtemp(prefix="study-test-tool-visual-"))
    db_path = tmp_dir / "visual_seed.db"
    modes = selected_modes(args.mode)
    states = selected_capture_states(args)
    seeded_states = [state for state in states if state.source == "seeded"]
    empty_states = [state for state in states if state.source == "empty"]
    expected_paths = expected_screenshot_paths(args.output, modes, states)

    if args.validate_only:
        if not validate_screenshots(expected_paths):
            raise SystemExit(1)
        return

    ensure_gui_modules()

    app = None
    try:
        for mode in modes:
            if seeded_states:
                seed = seed_database(db_path)
                app = create_app(mode)
                harness = ScreenshotHarness(app, args.output, mode)
                capture_state_group(app, seed, harness, seeded_states)
                app.destroy()
                app = None

            if empty_states:
                empty_db_path = tmp_dir / f"visual_empty_{mode}.db"
                configure_database(empty_db_path)
                app = create_app(mode)
                harness = ScreenshotHarness(app, args.output, mode)
                capture_state_group(app, None, harness, empty_states)
                app.destroy()
                app = None
    finally:
        if app is not None:
            app.destroy()
        if args.keep_db:
            print(f"kept seeded database: {db_path}")
        else:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    if not args.no_validate and not validate_screenshots(expected_paths):
        raise SystemExit(1)


def main() -> None:
    """CLI entrypoint."""
    args = parse_args()
    run_capture(args)


if __name__ == "__main__":
    main()
