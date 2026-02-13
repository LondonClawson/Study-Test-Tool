#!/bin/bash
# Study Test Tool — One-Time Installer for macOS
#
# Usage:  bash install.sh
#
# What this does:
#   1. Installs Homebrew (if needed)
#   2. Installs Python 3 via Homebrew (if needed)
#   3. Clones the repo to ~/StudyTestTool
#   4. Creates a virtual environment & installs dependencies
#   5. Places a "Study Test Tool" app on the Desktop
#
# After install, just double-click "Study Test Tool" on the Desktop.

set -e

# ── Configuration ─────────────────────────────────────────────
# Change this to your GitHub repo URL before running on her machine
REPO_URL="https://github.com/LondonClawson/Study-Test-Tool.git"
INSTALL_DIR="$HOME/StudyTestTool"
APP_NAME="Study Test Tool"
DESKTOP_APP="$HOME/Desktop/${APP_NAME}.app"
# ──────────────────────────────────────────────────────────────

# Support both Apple Silicon and Intel Homebrew paths
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

info()  { printf "\n\033[1;34m→ %s\033[0m\n" "$1"; }
ok()    { printf "\033[1;32m  ✓ %s\033[0m\n" "$1"; }
fail()  { printf "\033[1;31m  ✗ %s\033[0m\n" "$1"; exit 1; }

# ── Preflight ─────────────────────────────────────────────────

if [ "$REPO_URL" = "CHANGE_ME" ]; then
    fail "Edit install.sh and set REPO_URL to your GitHub repo URL first."
fi

# ── Xcode Command Line Tools (needed for git) ────────────────

info "Checking for Xcode Command Line Tools..."
if xcode-select -p &>/dev/null; then
    ok "Already installed"
else
    info "Installing Xcode Command Line Tools (you may see a system prompt)..."
    xcode-select --install 2>/dev/null || true
    echo "    Waiting for installation to finish..."
    until xcode-select -p &>/dev/null; do
        sleep 5
    done
    ok "Installed"
fi

# ── Homebrew ──────────────────────────────────────────────────

info "Checking for Homebrew..."
if command -v brew &>/dev/null; then
    ok "Already installed"
else
    info "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # Add to PATH for this session
    if [ -f /opt/homebrew/bin/brew ]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    ok "Installed"
fi

# ── Python 3 (python.org install required for tkinter) ───────
# Homebrew Python does NOT include tkinter, which this app needs.
# The python.org installer bundles tkinter and works out of the box.

info "Checking for python.org Python (>= 3.9)..."

PYTHON_BIN=""
# Check python.org framework versions from newest to oldest
for ver_dir in /Library/Frameworks/Python.framework/Versions/3.*; do
    candidate="$ver_dir/bin/python3"
    if [ -x "$candidate" ]; then
        minor=$("$candidate" -c "import sys; print(sys.version_info.minor)" 2>/dev/null)
        if [ -n "$minor" ] && [ "$minor" -ge 9 ]; then
            PYTHON_BIN="$candidate"
        fi
    fi
done

if [ -z "$PYTHON_BIN" ]; then
    fail "Python >= 3.9 from python.org not found.

    This app requires the python.org installer (Homebrew Python
    doesn't include tkinter, which the GUI needs).

    Download it from:  https://www.python.org/downloads/

    Then re-run this installer."
fi

ok "Using $PYTHON_BIN ($($PYTHON_BIN --version 2>&1))"

# ── Clone Repository ──────────────────────────────────────────

info "Setting up the application..."
if [ -d "$INSTALL_DIR/.git" ]; then
    ok "Repository already exists at $INSTALL_DIR"
    cd "$INSTALL_DIR"
    git pull -q
else
    if [ -d "$INSTALL_DIR" ]; then
        fail "$INSTALL_DIR exists but is not a git repo. Remove it first."
    fi
    git clone "$REPO_URL" "$INSTALL_DIR"
    ok "Cloned to $INSTALL_DIR"
fi

# ── Navigate into the code directory ──────────────────────────

CODE_DIR="$INSTALL_DIR/study_test_tool"
cd "$CODE_DIR"

# ── Virtual Environment & Dependencies ────────────────────────

info "Setting up Python environment..."
if [ ! -d "venv" ]; then
    "$PYTHON_BIN" -m venv venv
    ok "Virtual environment created"
else
    ok "Virtual environment already exists"
fi

source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
ok "Dependencies installed"

# ── Create Desktop App ────────────────────────────────────────

info "Creating desktop launcher..."

LAUNCH_SCRIPT="$CODE_DIR/scripts/launch.sh"
chmod +x "$LAUNCH_SCRIPT"

# Build a real .app via AppleScript — no Terminal window opens
osacompile -o "$DESKTOP_APP" <<EOF
do shell script "/bin/bash \"$LAUNCH_SCRIPT\""
EOF

ok "Created \"$APP_NAME\" on Desktop"

# ── Done ──────────────────────────────────────────────────────

printf "\n\033[1;32m════════════════════════════════════════════\033[0m\n"
printf "\033[1;32m  Installation complete!\033[0m\n"
printf "\033[1;32m  Double-click \"$APP_NAME\" on the Desktop.\033[0m\n"
printf "\033[1;32m════════════════════════════════════════════\033[0m\n\n"
