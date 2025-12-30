#!/bin/bash
# FileInventory - macOS App Bundle Build Script
# ==============================================

set -e  # Exit on error

echo "========================================"
echo "FileInventory macOS App Bundle Builder"
echo "========================================"
echo ""

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Cleanup alte Builds
echo -e "${YELLOW}[1/5]${NC} Cleanup alte Builds..."
if [ -d "build" ]; then
    rm -rf build
    echo "  ✓ build/ entfernt"
fi
if [ -d "dist" ]; then
    rm -rf dist
    echo "  ✓ dist/ entfernt"
fi

# Prüfe Python-Version
echo ""
echo -e "${YELLOW}[2/5]${NC} Prüfe Python-Version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "  ✓ Python $PYTHON_VERSION"

# Prüfe Dependencies
echo ""
echo -e "${YELLOW}[3/5]${NC} Prüfe Dependencies..."

check_package() {
    python3 -c "import $1" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "  ✓ $1"
    else
        echo -e "  ${RED}✗ $1 nicht installiert${NC}"
        return 1
    fi
}

check_package "customtkinter" || exit 1
check_package "py2app" || exit 1
check_package "FileInventory" || exit 1

# Build App Bundle
echo ""
echo -e "${YELLOW}[4/5]${NC} Baue macOS App Bundle..."
python3 setup.py py2app

if [ $? -eq 0 ]; then
    echo -e "  ${GREEN}✓ App Bundle erfolgreich erstellt${NC}"
else
    echo -e "  ${RED}✗ Build fehlgeschlagen${NC}"
    exit 1
fi

# Prüfe Output
echo ""
echo -e "${YELLOW}[5/5]${NC} Prüfe Output..."
if [ -d "dist/FileInventory.app" ]; then
    APP_SIZE=$(du -sh dist/FileInventory.app | awk '{print $1}')
    echo -e "  ${GREEN}✓ FileInventory.app erstellt ($APP_SIZE)${NC}"

    # Zeige App-Info
    echo ""
    echo "App-Bundle Details:"
    echo "  Pfad: $(pwd)/dist/FileInventory.app"
    echo "  Größe: $APP_SIZE"
    echo "  Bundle ID: com.marckonig.fileinventory"

    # Signierung-Info
    echo ""
    echo -e "${YELLOW}Hinweis:${NC} Die App ist NICHT signiert."
    echo "Beim ersten Start erscheint eine Sicherheitswarnung."
    echo "Lösung: Systemeinstellungen > Sicherheit > 'Trotzdem öffnen'"
else
    echo -e "  ${RED}✗ App Bundle nicht gefunden${NC}"
    exit 1
fi

# Erfolg
echo ""
echo "========================================"
echo -e "${GREEN}✓ Build erfolgreich abgeschlossen!${NC}"
echo "========================================"
echo ""
echo "App starten:"
echo "  open dist/FileInventory.app"
echo ""
echo "App in Applications kopieren:"
echo "  cp -r dist/FileInventory.app /Applications/"
echo ""
