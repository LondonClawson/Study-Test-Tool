"""Application settings and constants."""

from pathlib import Path

# Application
APP_NAME = "Study Testing Tool"
APP_VERSION = "1.0.0"

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_DIR = DATA_DIR / "database"
DB_PATH = DB_DIR / "study_tool.db"
TESTS_DIR = DATA_DIR / "tests"
BACKUPS_DIR = DATA_DIR / "backups"
ASSETS_DIR = PROJECT_ROOT / "assets"
SCHEMA_PATH = PROJECT_ROOT / "database" / "schema.sql"

# Window
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

# Colors
COLOR_PRIMARY = "#1f6aa5"
COLOR_SUCCESS = "#2fa572"
COLOR_DANGER = "#d9534f"
COLOR_WARNING = "#f0ad4e"
COLOR_ANSWERED = "#1f6aa5"
COLOR_FLAGGED = "#f0ad4e"
COLOR_UNANSWERED = "#6c757d"
COLOR_CURRENT = "#2fa572"
COLOR_CORRECT = "#2fa572"
COLOR_INCORRECT = "#d9534f"

# Fonts
FONT_FAMILY = "Helvetica"
FONT_SIZE_TITLE = 24
FONT_SIZE_HEADING = 18
FONT_SIZE_BODY = 14
FONT_SIZE_SMALL = 12

# Question types
QUESTION_TYPE_MC = "multiple_choice"
QUESTION_TYPE_ESSAY = "essay"

# Topic health colors
COLOR_TOPIC_WEAK = "#d9534f"
COLOR_TOPIC_MODERATE = "#f0ad4e"
COLOR_TOPIC_STRONG = "#2fa572"

# Weak topic threshold
WEAK_TOPIC_THRESHOLD = 70.0

# Default values
DEFAULT_OPTIONS_COUNT = 4


def ensure_directories() -> None:
    """Create required data directories if they don't exist."""
    for directory in [DATA_DIR, DB_DIR, TESTS_DIR, BACKUPS_DIR, ASSETS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
