#!/bin/bash
# FileInventory GUI - Setup-Script für macOS
# ==========================================

echo "================================"
echo "FileInventory GUI Setup"
echo "================================"
echo ""

# Prüfe Python-Version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python Version: $PYTHON_VERSION"

# Erstelle Virtual Environment (optional aber empfohlen)
if [ ! -d ".venv" ]; then
    echo ""
    echo "Erstelle Virtual Environment..."
    python3 -m venv .venv
    echo "✓ Virtual Environment erstellt"
fi

# Aktiviere venv
echo ""
echo "Aktiviere Virtual Environment..."
source .venv/bin/activate
echo "✓ Virtual Environment aktiviert"

# Installiere Dependencies
echo ""
echo "Installiere Python-Pakete..."
pip install --upgrade pip
pip install -r requirements-gui.txt

echo ""
echo "================================"
echo "✓ Setup abgeschlossen!"
echo "================================"
echo ""
echo "GUI starten mit:"
echo "  source .venv/bin/activate"
echo "  python3 FileInventoryGUI.py"
echo ""
