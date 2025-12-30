# GUI Kompatibilitätsproblem - macOS Sequoia

## Problem

Das System-Python 3.9.6 unter macOS Sequoia (26.2) verwendet eine veraltete Tcl/Tk-Version,
die nicht mit macOS 26+ kompatibel ist.

**Fehler:**
```
macOS 26 (2602) or later required, have instead 16 (1602) !
```

## Ursache

- **System-Python**: 3.9.6 (von Apple)
- **Tcl/Tk**: Version 8.5/8.6 (kompiliert für älteres macOS)
- **macOS Sequoia**: Benötigt Tcl/Tk 8.6.13+ oder 9.0+

## Lösungen

### Option 1: Python via Homebrew installieren (Empfohlen)

```bash
# Homebrew installieren (falls noch nicht vorhanden)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 3.12 mit aktueller Tcl/Tk-Version installieren
brew install python@3.12 python-tk@3.12

# Verwende Homebrew-Python
/opt/homebrew/bin/python3 FileInventoryGUI_Lite.py
```

### Option 2: Python.org Distribution

1. Download von [python.org](https://www.python.org/downloads/macos/)
2. Installiere Python 3.12+
3. Diese Version enthält aktuelles Tcl/Tk

```bash
# Nach Installation:
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 FileInventoryGUI_Lite.py
```

### Option 3: Web-basierte GUI (Sofort nutzbar)

Eine Web-basierte Alternative, die im Browser läuft:

```bash
# Installiere Streamlit oder Flask
pip3 install streamlit

# Starte Web-GUI (noch zu erstellen)
streamlit run FileInventoryWeb.py
```

### Option 4: CLI weiter nutzen

Die CLI-Version funktioniert einwandfrei:

```bash
python3 FileInventory.py
```

## Temporärer Workaround

Bis eine der obigen Lösungen umgesetzt ist, nutze die CLI-Version.

## Empfohlene Lösung für dein System

Da du macOS Sequoia (26.2) verwendest, empfehle ich:

1. **Kurzfristig**: Python via Homebrew installieren
2. **Langfristig**: Web-basierte GUI mit Streamlit entwickeln

## Nächste Schritte

Möchtest du:
1. Python via Homebrew installieren? (10 Minuten)
2. Eine Web-basierte GUI mit Streamlit? (Funktioniert sofort mit System-Python)
3. Bei der CLI-Version bleiben?

## Technische Details

### macOS Versionen-Code

| Darwin | macOS |
|--------|-------|
| 16 | High Sierra (10.13) |
| 26 | Sequoia (15.2) |

Die Fehlermeldung ist irreführend - es wird Darwin 16 (High Sierra) statt Darwin 26 (Sequoia) erkannt.

### Tcl/Tk Versionen

| Version | macOS Support |
|---------|---------------|
| 8.5 | Bis Catalina |
| 8.6.0-8.6.12 | Big Sur - Monterey |
| 8.6.13+ | Ventura+ |
| 9.0+ | Sonoma+ |

Dein System-Python hat Tcl/Tk 8.6.x (kompiliert für älteres macOS).
