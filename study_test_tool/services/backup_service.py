"""Local database backup helpers."""

import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

from config.settings import BACKUPS_DIR, DB_PATH


class BackupService:
    """Create local backups of the SQLite database."""

    def __init__(
        self,
        db_path: Optional[str] = None,
        backups_dir: Path = BACKUPS_DIR,
    ) -> None:
        self._db_path = Path(db_path) if db_path else DB_PATH
        self._backups_dir = backups_dir

    def create_database_backup(self) -> Optional[Path]:
        """Create a timestamped copy of the current SQLite database if it exists."""
        if not self._db_path.exists():
            return None

        self._backups_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        backup_path = (
            self._backups_dir / f"{self._db_path.stem}_{timestamp}{self._db_path.suffix}"
        )
        shutil.copy2(self._db_path, backup_path)
        return backup_path
