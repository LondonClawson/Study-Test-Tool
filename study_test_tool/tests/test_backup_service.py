"""Tests for local database backup helpers."""

from services.backup_service import BackupService


def test_create_database_backup_copies_existing_database(tmp_path):
    db_path = tmp_path / "study_tool.db"
    backups_dir = tmp_path / "backups"
    db_path.write_text("db contents", encoding="utf-8")

    backup_path = BackupService(
        db_path=str(db_path),
        backups_dir=backups_dir,
    ).create_database_backup()

    assert backup_path is not None
    assert backup_path.exists()
    assert backup_path.parent == backups_dir
    assert backup_path.read_text(encoding="utf-8") == "db contents"


def test_create_database_backup_missing_database_is_noop(tmp_path):
    db_path = tmp_path / "missing.db"
    backups_dir = tmp_path / "backups"

    backup_path = BackupService(
        db_path=str(db_path),
        backups_dir=backups_dir,
    ).create_database_backup()

    assert backup_path is None
    assert not backups_dir.exists()
