"""Entry point for the Study Testing Tool application."""

import sys
from pathlib import Path

# Ensure the project root is on the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config.database import initialize_database
from config.settings import ensure_directories
from database.migrations import run_migrations
from gui.main_window import App


def main() -> None:
    """Initialize and launch the application."""
    ensure_directories()
    initialize_database()
    run_migrations()
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
