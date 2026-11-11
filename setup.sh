#!/bin/bash
# ==============================================================================
# SPDX-License-Identifier: MIT
#
# AI-Generated Code Notice:
# Generated with: Gemini (Google)
# Date: 2026-11-11
# Human Review: Reviewed, adapted, and verified by Guzz-T
#
# Disclaimer:
# This script is provided "AS IS", without warranty of any kind. Review before
# execution in your local or production environment.
#
# Description:
# Script to install everything needed for development and set up the pre-commit hook.
# The script:
# - creates a .venv environment if one does not already exist
# - installs all development dependencies within the .venv environment
# - configures the pre-commit hook so that the cache is stored in the .venv folder
# - sets up the pre-commit hook (including for external Git clients such as TortoiseGit)
#
# ==============================================================================
set -e

echo "Starting project setup..."

# 1. Find the appropriate Python executable (Windows vs. Linux/macOS)
if command -v py &> /dev/null; then
    PYTHON_CMD="py"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

# 2. Create virtual environment (.venv) if it does not exist yet
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment (.venv)..."
    $PYTHON_CMD -m venv .venv
fi

# 3. Determine path to the venv Python executable (Windows uses Scripts/, Linux uses bin/)
if [ -f ".venv/Scripts/python.exe" ]; then
    VENV_PYTHON=".venv/Scripts/python.exe"
else
    VENV_PYTHON=".venv/bin/python"
fi

# 4. Define cache path inside the venv and enforce UTF-8 mode for Windows
CACHE_DIR="$(pwd)/.venv/.pre-commit-cache"
export PRE_COMMIT_HOME="$CACHE_DIR"
export PYTHONUTF8=1

# 5. Install project including dev dependencies (from pyproject.toml)
echo "Installing dependencies..."
"$VENV_PYTHON" -m pip install --upgrade pip
"$VENV_PYTHON" -m pip install -e ".[dev]"

# 6. Activate pre-commit Git hooks (overwrite any broken hook file)
echo "Installing pre-commit Git hooks..."
"$VENV_PYTHON" -m pre_commit install --overwrite

# 7. Inject cache path and UTF-8 setting directly into .git/hooks/pre-commit as Bash commands
HOOK_FILE=".git/hooks/pre-commit"
if [ -f "$HOOK_FILE" ]; then
    echo "Configuring Git hook for external Git clients..."
    "$VENV_PYTHON" -c "
import pathlib

hook_path = pathlib.Path('$HOOK_FILE')
content = hook_path.read_text(encoding='utf-8')
lines = content.splitlines()

# Inject valid Bash export commands right after the shebang (first line)
injection = [
    'export PRE_COMMIT_HOME=\"$CACHE_DIR\"',
    'export PYTHONUTF8=1'
]

if 'PRE_COMMIT_HOME' not in content and lines:
    lines = [lines[0]] + injection + lines[1:]
    hook_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
"
fi

# 8. Pre-build pre-commit environments inside the venv cache
echo "Pre-building pre-commit environments in venv cache..."
"$VENV_PYTHON" -m pre_commit install-hooks

echo "Setup completed successfully! Cache is located at: .venv/.pre-commit-cache"
