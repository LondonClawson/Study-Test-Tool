#!/bin/bash
# Study Test Tool — Launcher
# Called each time the app is opened. Pulls latest code, then runs the app.

set -e

# Support both Apple Silicon and Intel Homebrew paths
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

REPO_DIR="$HOME/StudyTestTool"
APP_DIR="$REPO_DIR/study_test_tool"
DESKTOP_APP="$HOME/Desktop/Study Test Tool.app"

cd "$REPO_DIR"

# Pull latest updates silently (non-fatal if offline)
git pull -q 2>/dev/null || true

# Activate virtual environment, sync dependencies, and launch
cd "$APP_DIR"
source venv/bin/activate
pip install -q -r requirements.txt 2>/dev/null || true

if [ -d "$DESKTOP_APP" ] && [ -f "$APP_DIR/assets/logo.png" ]; then
    python3 "$APP_DIR/scripts/app_icon.py" "$APP_DIR/assets/logo.png" "$DESKTOP_APP" 2>/dev/null || true
fi

python3 main.py
