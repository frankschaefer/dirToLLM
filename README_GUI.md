# FileInventory GUI

Moderne grafische Oberfläche für FileInventory mit nativem macOS- und Windows 11-Design.

## Features

### 🎨 Modernes Design
- **CustomTkinter**: Natives Aussehen für macOS und Windows 11
- **Dark/Light Mode**: Automatische Anpassung an System-Theme
- **Responsive Layout**: Skaliert mit Fenstergröße

### 📊 Funktionen
- ✅ Visuelle Pfad-Auswahl mit Folder-Browser
- ✅ Live-Fortschrittsanzeige während Verarbeitung
- ✅ Detailliertes Logging mit Timestamps
- ✅ Statistik-Übersicht (Verarbeitet, Übersprungen, Fehler)
- ✅ DSGVO-Klassifizierung optional
- ✅ Multi-Threading für responsive UI

### 🖥️ Plattform-Unterstützung
- **macOS** (primär): Getestet auf macOS 12+
- **Windows 11**: Voll kompatibel
- **Linux**: Funktioniert ebenfalls (mit GTK)

## Installation

### Automatische Installation (macOS)

```bash
# Setup-Script ausführen
./setup_gui.sh
```

Das Script:
- Erstellt ein Virtual Environment (`.venv`)
- Installiert alle Dependencies
- Aktiviert das Environment

### Manuelle Installation

```bash
# Virtual Environment erstellen (optional)
python3 -m venv .venv
source .venv/bin/activate

# Dependencies installieren
pip install -r requirements-gui.txt
```

### Windows 11

```powershell
# Virtual Environment erstellen
python -m venv .venv
.venv\Scripts\activate

# Dependencies installieren
pip install -r requirements-gui.txt
```

## Verwendung

### GUI starten

```bash
# Mit Virtual Environment
source .venv/bin/activate
python3 FileInventoryGUI.py
```

### Erste Schritte

1. **Quellverzeichnis auswählen**
   - Klicke auf "Durchsuchen" bei Quellverzeichnis
   - Wähle dein OneDrive/Dokumente-Ordner

2. **Ausgabeverzeichnis festlegen**
   - Standard: `~/LLM`
   - Kann angepasst werden

3. **Optionen konfigurieren**
   - ✓ DSGVO-Klassifizierung durchführen
   - ✓ Existierende Dateien überspringen
   - ✓ Kombinierte Datenbank erstellen (optional)

4. **Verarbeitung starten**
   - Klicke auf "▶ Verarbeitung starten"
   - Beobachte Fortschritt im Log-Bereich
   - Stoppen mit "■ Stoppen" möglich

## Architektur

### UI-Komponenten

```
FileInventoryApp
├── Header (Titel, Version)
├── Main Content
│   ├── Path Section (Quelle/Ziel)
│   ├── Options (Checkboxes)
│   └── Log Section (Textbox)
└── Footer
    ├── Buttons (Start/Stop)
    ├── Statistics
    └── Progress Bar
```

### Threading-Modell

```
Main Thread (UI)
    │
    ├─> Message Queue ←─── Worker Thread (Processing)
    │
    └─> Queue Check (100ms) → Update UI
```

**Vorteile**:
- UI bleibt responsive während Verarbeitung
- Keine Freezes
- Saubere Thread-Kommunikation via Queue

## Tastenkombinationen

| Tastenkombination | Aktion |
|-------------------|--------|
| `Cmd/Ctrl + Q` | Beenden |
| `Cmd/Ctrl + ,` | Einstellungen (zukünftig) |

## Screenshot-Tour

### Hauptfenster
```
┌─────────────────────────────────────────────────┐
│ 📁  FileInventory - Dokumenten-Analyse         │
│     Version 1.19.0 - KI-gestützte Analyse      │
├─────────────────────────────────────────────────┤
│ Quellverzeichnis:                               │
│ [~/OneDrive - Marc König...]  [Durchsuchen]    │
│                                                 │
│ Ausgabeverzeichnis:                             │
│ [~/LLM]                        [Durchsuchen]    │
├─────────────────────────────────────────────────┤
│ Optionen:                                       │
│ ☑ DSGVO-Klassifizierung  ☑ Existierende skip  │
├─────────────────────────────────────────────────┤
│ Verarbeitungslog                  [Log löschen]│
│ ╔═══════════════════════════════════════════╗ │
│ ║ [12:34:56] Verarbeitung gestartet...      ║ │
│ ║ [12:34:57] Gefunden: 1,234 Dateien        ║ │
│ ║ [12:34:58] [1/1234] Dokument1.pdf         ║ │
│ ╚═══════════════════════════════════════════╝ │
├─────────────────────────────────────────────────┤
│ [▶ Verarbeitung starten] [■ Stoppen]           │
│ Gesamt: 1234 | Verarbeitet: 123 | Fehler: 0    │
│ [████████████░░░░░░░░░] 10%                    │
└─────────────────────────────────────────────────┘
```

## Technische Details

### Dependencies

- **customtkinter** (5.2.0+): Modernes UI-Framework
- **darkdetect**: System-Theme-Erkennung
- Alle FileInventory-Dependencies (siehe requirements-gui.txt)

### Kompatibilität

| OS | Version | Status |
|----|---------|--------|
| macOS | 12+ | ✅ Voll unterstützt |
| Windows | 11 | ✅ Voll unterstützt |
| Windows | 10 | ✅ Kompatibel |
| Linux | Ubuntu 22+ | ✅ Funktioniert |

### Performance

- **Start-Zeit**: < 2 Sekunden
- **UI-Responsiveness**: 60 FPS (kein Blocking)
- **Memory**: ~50-100 MB (ohne File-Processing)

## Erweiterte Konfiguration

### Theme anpassen

In `FileInventoryGUI.py`:

```python
# Dark Mode erzwingen
ctk.set_appearance_mode("Dark")

# Light Mode erzwingen
ctk.set_appearance_mode("Light")

# System-Theme verwenden (Standard)
ctk.set_appearance_mode("System")
```

### Farb-Theme ändern

```python
# Blau (Standard)
ctk.set_default_color_theme("blue")

# Grün
ctk.set_default_color_theme("green")

# Dunkelblau
ctk.set_default_color_theme("dark-blue")
```

## Fehlerbehandlung

### GUI startet nicht?

1. **Python-Version prüfen**:
   ```bash
   python3 --version  # Mindestens 3.9
   ```

2. **CustomTkinter installiert?**:
   ```bash
   python3 -c "import customtkinter"
   ```

3. **Virtual Environment aktiviert?**:
   ```bash
   source .venv/bin/activate
   ```

### macOS Sicherheitswarnung?

Beim ersten Start kann macOS warnen:
- System-Einstellungen > Sicherheit > "Trotzdem öffnen"

## Roadmap

### Version 1.20.0 (geplant)
- [ ] Einstellungs-Dialog
- [ ] Datei-Filter konfigurierbar
- [ ] Export-Optionen (CSV, Excel)
- [ ] Mehrsprachigkeit (EN/DE)

### Version 1.21.0 (geplant)
- [ ] Drag & Drop für Ordner
- [ ] Favoriten/Presets speichern
- [ ] Dark Mode Toggle-Button
- [ ] Notification bei Abschluss

### Version 2.0.0 (Vision)
- [ ] Integrierter Viewer für Dokumente
- [ ] Such-Funktion in verarbeiteten Daten
- [ ] Visualisierung (Charts, Statistiken)
- [ ] Cloud-Integration

## Support

Bei Problemen oder Fragen:
1. Prüfe die [FAQ](#fehlerbehandlung)
2. Schaue in die Logs im Log-Bereich
3. Erstelle ein Issue auf GitHub

## Lizenz

Wie FileInventory - Proprietär

---

**Made with ❤️ using CustomTkinter**
