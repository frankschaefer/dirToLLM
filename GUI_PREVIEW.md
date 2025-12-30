# FileInventory GUI - Vorschau

## Hauptfenster

```
╔════════════════════════════════════════════════════════════════════════════╗
║  📁  FileInventory - Dokumenten-Analyse                                    ║
║      Version 1.19.0 (2025-12-30) - KI-gestützte Dokumenten-Zusammenfassung ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │  Quellverzeichnis:                                                 │  ║
║  │  ┌──────────────────────────────────────────────┐  ┌──────────┐   │  ║
║  │  │ ~/OneDrive - Marc König Unternehmensberatung │  │Durchsuchen│  │  ║
║  │  └──────────────────────────────────────────────┘  └──────────┘   │  ║
║  │                                                                     │  ║
║  │  Ausgabeverzeichnis:                                               │  ║
║  │  ┌──────────────────────────────────────────────┐  ┌──────────┐   │  ║
║  │  │ ~/LLM                                        │  │Durchsuchen│  │  ║
║  │  └──────────────────────────────────────────────┘  └──────────┘   │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │  Optionen                                                          │  ║
║  │                                                                     │  ║
║  │  ☑ DSGVO-Klassifizierung durchführen                              │  ║
║  │  ☑ Existierende Dateien überspringen                              │  ║
║  │  ☐ Kombinierte Datenbank erstellen                                │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │  Verarbeitungslog                           [Log löschen]         │  ║
║  │  ┌──────────────────────────────────────────────────────────────┐ │  ║
║  │  │ [12:34:56] === Verarbeitung gestartet ===                    │ │  ║
║  │  │ [12:34:56] Quelle: ~/OneDrive - Marc König ...               │ │  ║
║  │  │ [12:34:56] Ziel: ~/LLM                                       │ │  ║
║  │  │ [12:34:57] Sammle Dateien...                                 │ │  ║
║  │  │ [12:34:58] Gefunden: 1,234 Dateien                           │ │  ║
║  │  │ [12:34:59] [1/1234] Analyse_Q4_2024.pdf                      │ │  ║
║  │  │ [12:35:00] [2/1234] Präsentation_Kunde_A.pptx                │ │  ║
║  │  │ [12:35:01] [3/1234] Vertrag_Mustervertrag.docx               │ │  ║
║  │  │ [12:35:02] ⚠️  DSGVO [Gehaltsabrechnung.pdf]: GEHALTS...    │ │  ║
║  │  │ [12:35:03] [4/1234] Budget_2025.xlsx                         │ │  ║
║  │  │                                                               │ │  ║
║  │  │                                                               │ │  ║
║  │  └──────────────────────────────────────────────────────────────┘ │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌──────────────────┐  ┌──────────┐                                      ║
║  │ ▶ Verarbeitung   │  │ ■ Stoppen│                                      ║
║  │   starten        │  │          │    Gesamt: 1234 | Verarbeitet: 234  ║
║  └──────────────────┘  └──────────┘    Übersprungen: 50 | Fehler: 2     ║
║                                                                            ║
║  [██████████████████░░░░░░░░░░░░░░░░░░░░░░░░] 19%                        ║
╚════════════════════════════════════════════════════════════════════════════╝
```

## Design-Features

### 🎨 Farb-Schema

**Light Mode (macOS):**
- Hintergrund: Weiß (#FFFFFF)
- Primär: macOS Blau (#007AFF)
- Text: Schwarz (#000000)
- Rahmen: Hellgrau (#E5E5E5)

**Dark Mode (macOS):**
- Hintergrund: Dunkelgrau (#1E1E1E)
- Primär: macOS Blau (#0A84FF)
- Text: Weiß (#FFFFFF)
- Rahmen: Mittelgrau (#3A3A3C)

**Windows 11 Mode:**
- Hintergrund: System-Standard
- Primär: Windows Blau (#0078D4)
- Akzent: Automatisch vom System
- Mica-Material-Effekt (wenn verfügbar)

### 📐 Layout

**Hauptbereiche:**
1. **Header** (15% Höhe): Titel, Version, Icon
2. **Content** (65% Höhe): Pfade, Optionen, Log
3. **Footer** (20% Höhe): Buttons, Stats, Progress

**Responsive Design:**
- Min-Breite: 800px
- Min-Höhe: 600px
- Bevorzugt: 1200x800px

### 🔘 Button-Zustände

**Start-Button:**
```
Normal:    [▶ Verarbeitung starten]  (Grün)
Hover:     [▶ Verarbeitung starten]  (Dunkelgrün, Cursor: Pointer)
Disabled:  [▶ Verarbeitung starten]  (Grau)
```

**Stop-Button:**
```
Normal:    [■ Stoppen]  (Rot)
Hover:     [■ Stoppen]  (Dunkelrot, Cursor: Pointer)
Disabled:  [■ Stoppen]  (Grau)
```

### 📊 Progress Bar

```
Idle:      [░░░░░░░░░░░░░░░░░░░░░░░░░] 0%
Running:   [████████████░░░░░░░░░░░░░] 50%
Complete:  [█████████████████████████] 100%
```

Farben:
- Fortschritt: Blau (macOS), System-Akzent (Windows)
- Hintergrund: Hellgrau
- Animation: Smooth Transitions

### 📝 Log-Farben

```
INFO:     Weiß/Schwarz (je nach Theme)
SUCCESS:  Grün (#4CAF50)
WARNING:  Orange (#FF9800)
ERROR:    Rot (#F44336)
```

### ⚡ Animationen

1. **Button-Hover**: Smooth color transition (200ms)
2. **Progress Bar**: Linear fill animation
3. **Log-Scroll**: Auto-scroll zu neuesten Einträgen
4. **Window-Resize**: Smooth element repositioning

## Tastenkombinationen

| Kürzel | Funktion |
|--------|----------|
| `Cmd/Ctrl + Q` | Beenden |
| `Cmd/Ctrl + O` | Ordner öffnen |
| `Cmd/Ctrl + L` | Log löschen |
| `Cmd/Ctrl + R` | Verarbeitung starten |
| `Esc` | Verarbeitung stoppen |

## Interaktive Elemente

### Folder-Browser
```
┌─────────────────────────────────────┐
│  Ordner auswählen                   │
├─────────────────────────────────────┤
│  📁 Dokumente                       │
│  📁 OneDrive                        │
│  ▸📁 Marc König Unternehmensberatung│
│    📁 Projekte                      │
│    📁 Kunden                        │
│    📁 Internes                      │
│                                     │
│  [Abbrechen]           [Auswählen] │
└─────────────────────────────────────┘
```

### Options-Checkboxes
```
☑ DSGVO-Klassifizierung durchführen
  ↳ Analysiert Dokumente auf personenbezogene Daten

☑ Existierende Dateien überspringen
  ↳ Spart Zeit bei erneutem Durchlauf

☐ Kombinierte Datenbank erstellen
  ↳ Erstellt große JSON-Datenbanken
```

## Statusanzeige

### Statistik-Zeile
```
┌────────────────────────────────────────────────────────────┐
│ Gesamt: 1,234 | Verarbeitet: 234 | Übersprungen: 50 | ❌ 2 │
└────────────────────────────────────────────────────────────┘
```

**Live-Updates:**
- Aktualisierung alle 100ms
- Keine UI-Blockierung
- Thread-Safe via Queue

### Log-Format
```
[HH:MM:SS] [LEVEL] Nachricht
[12:34:56] [INFO]  Dokument verarbeitet
[12:34:57] [✓]     Erfolgreich gespeichert
[12:34:58] [⚠️]     DSGVO-Warnung: Sensible Daten erkannt
[12:34:59] [❌]     Fehler beim Lesen
```

## Plattform-Spezifische Features

### macOS
- Native Titlebar mit Traffic Lights
- System-Font (SF Pro)
- Retina-optimiert
- Touch Bar Support (zukünftig)

### Windows 11
- Rounded Corners
- Mica Material (wenn verfügbar)
- System-Font (Segoe UI Variable)
- Snap Layouts kompatibel

## Accessibility

- ✅ Tastatur-Navigation
- ✅ Hoher Kontrast-Modus
- ✅ Screen Reader kompatibel
- ✅ Skalierbar (125%, 150%, 200%)

---

**Design inspiriert von:**
- macOS Big Sur / Sonoma Design Guidelines
- Windows 11 Fluent Design System
- Material Design 3 (Google)
