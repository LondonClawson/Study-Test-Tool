1. Open Terminal (Cmd+Space, type "Terminal")
  2. Paste this one line:
  bash -c "$(curl -fsSL https://raw.githubusercontent.com/LondonClawson/Study-Test-Tool/main/study_test_tool/scripts/install.sh)"
  3. Wait for it to finish, close Terminal

  From then on:
  - "Study Test Tool" app sits on her Desktop — double-click to open, like any app
  - It silently pulls your latest code each launch
  - No Terminal window, no updates to manage

## Local Data And Safe Updates

Study Test Tool keeps user study data separate from tracked application code.
Imported tests, the SQLite database, and local backups live under
`study_test_tool/data/`, which is ignored by git. Local source documents can be
kept in `test_source_data/`, which is also ignored by git.

Safe local folders:

- `study_test_tool/data/database/` - the local SQLite database.
- `study_test_tool/data/backups/` - automatic and manual database backups.
- `study_test_tool/data/tests/` - user-local test artifacts.
- `test_source_data/` - PDFs, DOCX files, text files, or other private source
  documents used for imports.

App updates and `git pull` should not overwrite these ignored folders. Before a
large folder import, the app creates a timestamped database backup in
`study_test_tool/data/backups/`. For a manual backup, copy
`study_test_tool/data/database/study_tool.db` somewhere safe. To restore, close
the app and replace that file with the backup copy.

Avoid storing personal study materials or generated import files in tracked repo
folders. Keeping local data in ignored folders prevents merge noise and makes
future updates safer.
