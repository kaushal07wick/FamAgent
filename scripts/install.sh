#!/bin/bash

echo ""
echo "🧠 FamAgent Installer"
echo "----------------------"
echo "This script will clone the FamAgent repository, set up a Python virtual environment,"
echo "and install all required dependencies on your system."
echo ""

# Prompt user for confirmation
read -p "❗ Do you want to continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Installation aborted."
    exit 1
fi

# Clone repo
REPO_URL="https://github.com/kaushal07wick/famagent.git"
INSTALL_DIR="famagent"

echo "📦 Cloning FamAgent repository..."
if ! git clone "$REPO_URL" "$INSTALL_DIR"; then
    echo "❌ Failed to clone the repository."
    exit 1
fi

cd "$INSTALL_DIR" || { echo "❌ Failed to enter directory."; exit 1; }

# Setup virtual environment
echo "🐍 Creating virtual environment..."
if ! python3 -m venv agents; then
    echo "❌ Failed to create virtual environment."
    exit 1
fi

# Activate and install dependencies
echo "📦 Installing dependencies..."
source agents/bin/activate
if ! pip install -r requirements.txt; then
    echo "❌ Failed to install Python packages."
    deactivate
    exit 1
fi

# Final message
echo ""
echo "✅ FamAgent installed successfully!"
echo " Run with: famagent"
