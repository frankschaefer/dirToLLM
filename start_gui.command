#!/bin/bash
# FileInventory GUI Starter
# Doppelklick auf diese Datei startet die GUI

# Wechsle ins Projektverzeichnis
cd "$(dirname "$0")"

# Aktiviere venv
source .venv/bin/activate

# Starte GUI
python3 FileInventoryGUI_Lite.py

# Halte Terminal offen bei Fehler
if [ $? -ne 0 ]; then
    echo ""
    echo "Fehler beim Start. Drücke Enter zum Beenden..."
    read
fi
