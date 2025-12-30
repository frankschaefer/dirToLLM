# Tkinter für pyenv Python aktivieren

## Problem
Dein pyenv Python 3.12.1 wurde ohne Tkinter-Support kompiliert.

## Lösung: Python mit Tkinter neu installieren

### Schritt 1: Tcl/Tk via Homebrew installieren

```bash
# Installiere Tcl/Tk
brew install tcl-tk

# Zeige Installationspfad
brew info tcl-tk
```

### Schritt 2: Python mit Tkinter neu kompilieren

```bash
# Setze Umgebungsvariablen für pyenv
export PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I$(brew --prefix tcl-tk)/include' --with-tcltk-libs='-L$(brew --prefix tcl-tk)/lib -ltcl8.6 -ltk8.6'"

# Installiere Python 3.12.1 neu
pyenv install 3.12.1 --force

# Oder installiere neueste Version
pyenv install 3.12.7
pyenv local 3.12.7
```

### Schritt 3: Neues venv erstellen

```bash
# Altes venv löschen
rm -rf .venv

# Neues venv mit Tkinter-Python erstellen
python3 -m venv .venv

# Aktivieren
source .venv/bin/activate

# Teste Tkinter
python3 -c "import tkinter; print('✓ Tkinter funktioniert!')"
```

### Schritt 4: Dependencies installieren

```bash
pip install -r requirements-gui.txt
```

### Schritt 5: GUI starten

```bash
python3 FileInventoryGUI_Lite.py
```

## Alternative: Homebrew Python verwenden (Schneller!)

Wenn du nicht neu kompilieren möchtest:

```bash
# Installiere Homebrew Python (hat Tkinter bereits)
brew install python@3.12

# Erstelle venv mit Homebrew Python
rm -rf .venv
/opt/homebrew/bin/python3.12 -m venv .venv

# Aktivieren und testen
source .venv/bin/activate
python3 -c "import tkinter; print('✓ Tkinter funktioniert!')"

# Dependencies
pip install -r requirements-gui.txt

# GUI starten
python3 FileInventoryGUI_Lite.py
```

## Welche Lösung?

**Empfehlung**: Homebrew Python verwenden (Option 2)
- ✅ Schneller (kein Neu-Kompilieren)
- ✅ Tkinter bereits dabei
- ✅ Gut gewartet

**pyenv neu kompilieren**: Nur wenn du unbedingt pyenv nutzen willst
