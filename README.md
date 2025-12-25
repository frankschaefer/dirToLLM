# FileInventory - OneDrive Dokumenten-Zusammenfassung (macOS)

**Version:** 1.5.1
**Datum:** 2025-12-25
**Lizenz:** Proprietär

## Übersicht

FileInventory ist ein intelligentes Python-Tool zur automatischen Analyse und Zusammenfassung von Dokumenten in OneDrive-Verzeichnissen. Das System nutzt lokale Large Language Models (LLM) über LM Studio, um kompakte, aussagekräftige Zusammenfassungen von verschiedenen Dateiformaten zu erstellen.

### Hauptfunktionen

- **Multiformat-Unterstützung**: PDF, Word (.docx/.doc), Excel (.xlsx/.xls/.xlsm/.xltx), PowerPoint (.pptx/.ppt), Text, Markdown und Bilder
- **OCR-Unterstützung**: Automatische Texterkennung für gescannte PDFs mit Tesseract OCR
- **macOS-optimiert**: Native macOS-Unterstützung mit OneDrive-Integration
- **LLM-basierte Analyse**: Intelligente Zusammenfassungen mit dateityp-spezifischen Prompts
- **Vision-Fähigkeit**: Bildanalyse und -beschreibung mittels multimodaler Modelle
- **Icon-Filter**: Automatisches Überspringen kleiner Bilder (<10 KB)
- **Validierung**: Automatische Überprüfung und Neuerstellung fehlerhafter JSON-Ausgaben
- **Fortschrittsüberwachung**: Detaillierte Zeitschätzungen und Statistiken mit Dateiendungs-Übersicht und OCR-Zähler
- **Interaktive Steuerung**: Pause/Resume-Funktionalität während der Verarbeitung
- **Professionelle Fehlerbehandlung**: Intelligente LM Studio-Fehlerbehandlung mit Benutzerabfragen
- **Legacy-Format-Support**: Unterstützung für alte Office-Formate (.doc, .ppt, .xls)

---

## Systemanforderungen

### Betriebssystem
- **macOS**: Version 10.15 (Catalina) oder höher
- Getestet auf macOS 26.2

### Software
- **Python**: Version 3.8 oder höher (Python 3.12+ empfohlen)
- **LM Studio**: Aktuelle Version mit laufendem lokalem Server
- **OneDrive**: OneDrive App für macOS installiert und synchronisiert

### Hardware-Empfehlungen
- **RAM**: Mindestens 8 GB (16 GB empfohlen)
- **GPU**: Optional, beschleunigt LLM-Inferenz erheblich (Apple Silicon bevorzugt)
- **Festplatte**: Ausreichend Speicherplatz für JSON-Ausgaben

---

## Installation

### 1. Python Installation auf macOS

#### Option A: Homebrew (Empfohlen)
```bash
# Installieren Sie Homebrew falls noch nicht vorhanden
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Installieren Sie Python
brew install python@3.12
```

#### Option B: Python.org
1. Besuchen Sie [python.org/downloads](https://www.python.org/downloads/)
2. Laden Sie Python 3.12.x für macOS herunter
3. Installieren Sie das .pkg-Paket

#### Verifizierung
```bash
python3 --version
# Erwartete Ausgabe: Python 3.12.x
```

### 2. Python-Bibliotheken installieren

Öffnen Sie Terminal und führen Sie folgende Befehle aus:

```bash
# Navigieren Sie zum Skript-Verzeichnis
cd ~/Library/CloudStorage/Dropbox/Frank/Code/MKU

# Optional: Erstellen Sie eine virtuelle Umgebung
python3 -m venv .venv
source .venv/bin/activate

# Installieren Sie alle erforderlichen Bibliotheken
pip install -r requirements.txt
```

#### Einzelne Bibliotheken (zur Referenz)

| Bibliothek | Zweck | Version |
|------------|-------|---------|
| `pdfplumber` | PDF-Textextraktion | 0.11.4 |
| `python-docx` | Word-Dokumentenverarbeitung | 1.1.2 |
| `python-pptx` | PowerPoint-Analyse | 1.0.2 |
| `openpyxl` | Excel-Datenextraktion | 3.1.5 |
| `requests` | HTTP-Kommunikation mit LM Studio | 2.32.3 |
| `pytesseract` | OCR für gescannte PDFs | 0.3.13 |
| `Pillow` | Bildverarbeitung für OCR | 12.0.0 |

### 3. LM Studio Installation und Konfiguration

#### Installation
1. Laden Sie LM Studio für macOS herunter: [lmstudio.ai](https://lmstudio.ai/)
2. Installieren Sie die Anwendung
3. Laden Sie ein LLM-Modell herunter (Empfehlungen siehe unten)

#### Modell-Empfehlungen

##### Für Textverarbeitung (Standard)
- **ministral-3-14b-reasoning** (optimiert für präzise Zusammenfassungen)
- **ministral-3-3b-instruct** (leichtgewichtig, schnell)
- **Mistral-7B-Instruct** (ausgewogen)
- **Llama-3-8B-Instruct** (hochwertig)

##### Für Bildverarbeitung (Vision-Modelle)
- **LLaVA-v1.6-Mistral-7B**
- **BakLLaVA-1**
- **Obsidian-3B-Multimodal**

#### Server-Konfiguration
1. Öffnen Sie LM Studio
2. Laden Sie das gewünschte Modell
3. Wechseln Sie zur "Local Server" Ansicht
4. Starten Sie den Server auf Port **1234** (Standard)
5. Notieren Sie den "Model Name" (wird in `FileInventory.py` benötigt)

#### Konfiguration im Skript
Öffnen Sie `FileInventory.py` und passen Sie bei Bedarf an:

```python
LMSTUDIO_API_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "local-model"  # Ersetzen Sie mit dem Namen aus LM Studio
```

### 4. Tesseract OCR Installation (für gescannte PDFs)

#### Installation auf macOS

```bash
# Installation via Homebrew (empfohlen)
brew install tesseract

# Deutsche Sprachdaten installieren
brew install tesseract-lang
```

#### Alternative Installation

```bash
# Oder nur deutsche Sprachdaten
brew install tesseract
# Die deutschen Sprachdaten werden automatisch mitinstalliert
```

#### Verifizierung

```bash
tesseract --version
# Erwartete Ausgabe: tesseract 5.x.x

# Prüfe verfügbare Sprachen
tesseract --list-langs
# Sollte 'deu' (Deutsch) enthalten
```

#### Hinweise zur OCR-Funktionalität

- **Automatische Erkennung**: Das System erkennt automatisch gescannte PDFs (Seiten mit <10 Zeichen extrahiertem Text)
- **Hohe Auflösung**: OCR verwendet 300 DPI für optimale Texterkennung
- **Deutsch-Optimiert**: Verwendet 'deu' Sprachmodell für deutsche Texte
- **Fortschrittsanzeige**: Bei mehrseitigen gescannten PDFs wird der OCR-Fortschritt angezeigt
- **Statistik**: OCR-verarbeitete Dokumente werden in den Berichten separat gezählt
- **Optional**: Wenn Tesseract nicht installiert ist, werden gescannte PDFs übersprungen (mit Warnung)

---

## Konfiguration

### Verzeichnispfade anpassen

Öffnen Sie `FileInventory.py` und passen Sie die Pfade an:

```python
# Quellverzeichnis (OneDrive)
SRC_ROOT = os.path.expanduser("~/OneDrive - Marc König Unternehmensberatung")

# Zielverzeichnis für JSON-Ausgaben
DST_ROOT = os.path.expanduser("~/LLM")
```

### Dateitypen konfigurieren

Standardmäßig werden folgende Formate verarbeitet:

```python
EXTENSIONS = {
    ".pdf",                                    # PDF-Dokumente
    ".docx", ".doc",                          # Word-Dokumente (neu und alt)
    ".pptx", ".ppt",                          # PowerPoint-Präsentationen (neu und alt)
    ".xlsx", ".xls", ".xlsm", ".xltx",       # Excel-Dateien (neu, alt, Makro, Vorlagen)
    ".txt", ".md",                            # Textdateien
    ".png", ".jpg", ".jpeg"                   # Bilddateien
}
```

**Anpassung**: Entfernen oder ergänzen Sie Dateitypen nach Bedarf.

### Minimale Bildgröße anpassen

```python
# Minimale Dateigröße für Bilddateien (in Bytes) - ignoriere kleine Icons
MIN_IMAGE_SIZE = 10 * 1024  # 10 KB
```

---

## Verwendung

### Basis-Ausführung

```bash
cd ~/Library/CloudStorage/Dropbox/Frank/Code/MKU

# Mit virtueller Umgebung
source .venv/bin/activate
python3 FileInventory.py

# Ohne virtuelle Umgebung
python3 FileInventory.py
```

### Interaktive Steuerung während der Ausführung

#### Pause/Resume
- **Pause**: Drücken Sie Enter während der Verarbeitung
- **Fortsetzen**: Wählen Sie `J` (Ja)
- **Abbrechen**: Wählen Sie `N` (Nein)

#### Fehlerbehandlung (NEU in v1.4.0)
Beim ersten LM Studio-Fehler werden Sie gefragt:

```
================================================================================
FEHLER BEI DER VERARBEITUNG
================================================================================

Datei: beispiel.pdf
Fehler: Netzwerkfehler bei der Zusammenfassung: Connection timeout

--------------------------------------------------------------------------------

Wie möchten Sie fortfahren?

  [A] Abbrechen - Verarbeitung sofort beenden
  [W] Weiter ohne Fehlerabfragen - Weitere Fehler stillschweigend überspringen
  [F] Weiter mit Fehlerabfragen - Bei jedem Fehler erneut nachfragen

--------------------------------------------------------------------------------
Bitte wählen Sie (A/W/F):
```

**Optionen:**
- **A**: Programm wird sofort beendet
- **W**: Fehlerhafte Dateien werden übersprungen, keine weiteren Abfragen
- **F**: Bei jedem Fehler erfolgt eine erneute Abfrage

### Ausgabeformat

Für jede verarbeitete Datei wird eine JSON-Datei erstellt:

```json
{
  "name": "Beispieldokument.pdf",
  "path": "Projekte/Kunde_A/Beispieldokument.pdf",
  "ext": ".pdf",
  "size": 1048576,
  "created": "2025-01-15T10:30:00",
  "modified": "2025-01-20T14:45:00",
  "chars": 15420,
  "summary": "Projektübersicht für Kunde A mit Marc König als Projektleiter. Beschreibt Meilensteine Q1-Q4 2025 mit Fokus auf digitale Transformation und Prozessoptimierung...",
  "ocr_info": {
    "used_ocr": true,
    "ocr_pages": 15,
    "total_pages": 20,
    "ocr_chars": 12350
  }
}
```

#### Feldübersicht

| Feld | Beschreibung |
|------|--------------|
| `name` | Dateiname |
| `path` | Relativer Pfad zur Quelldatei |
| `ext` | Dateierweiterung |
| `size` | Dateigröße in Bytes |
| `created` | Erstellungszeitpunkt (ISO 8601) |
| `modified` | Letzte Änderung (ISO 8601) |
| `chars` | Anzahl extrahierter Zeichen |
| `summary` | KI-generierte Zusammenfassung (max. 650 Zeichen, reiner Fließtext, auf Deutsch) |
| `ocr_info` | **Optional:** OCR-Metadaten (nur bei gescannten PDFs) |
| `ocr_info.used_ocr` | Boolean - ob OCR verwendet wurde |
| `ocr_info.ocr_pages` | Anzahl der Seiten, die mit OCR verarbeitet wurden |
| `ocr_info.total_pages` | Gesamtzahl der PDF-Seiten |
| `ocr_info.ocr_chars` | Anzahl der via OCR extrahierten Zeichen |

---

## Funktionsweise

### Verarbeitungspipeline

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Dateiscan mit Live-Fortschrittsanzeige                  │
│    └─> Rekursive Durchsuchung des OneDrive-Verzeichnisses  │
│    └─> Statistik nach Dateiendungen                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. LM Studio-Verbindungscheck                               │
│    └─> Prüfung auf erreichbaren Server                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Dateizugriffsprüfung                                     │
│    └─> OneDrive-Dateien sind direkt verfügbar auf macOS    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Bildgrößenfilter (für PNG/JPG/JPEG)                     │
│    └─> Überspringt Dateien < 10 KB (Icons)                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Textextraktion                                           │
│    ├─> PDF: pdfplumber + OCR-Fallback (Tesseract)         │
│    │   └─> Automatische OCR-Erkennung bei <10 Zeichen/Seite│
│    │   └─> 300 DPI Auflösung für optimale Texterkennung    │
│    ├─> DOCX/DOC: python-docx                               │
│    ├─> PPTX/PPT: python-pptx                               │
│    ├─> XLSX/XLS/XLSM/XLTX: openpyxl (Werte, keine Formeln)│
│    ├─> TXT/MD: UTF-8 + Latin-1 Fallback                   │
│    └─> PNG/JPG: Base64 + Vision API                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. LLM-Zusammenfassung                                      │
│    ├─> Dateityp-spezifische Prompts (AUF DEUTSCH)         │
│    ├─> Adaptive Textkürzung (30k → 3k Zeichen)            │
│    ├─> Context/Token-Overflow Handling mit Retry           │
│    └─> Professionelle Fehlerbehandlung mit Benutzerabfrage │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. JSON-Ausgabe                                             │
│    ├─> Validierung vorhandener Dateien                     │
│    └─> Speicherung unter DST_ROOT                          │
└─────────────────────────────────────────────────────────────┘
```

### Dateityp-spezifische Prompts

Das System verwendet optimierte Prompts für jeden Dateityp:

- **PDF/DOCX/DOC**: Fokus auf Inhalte, Themen und Kernaussagen mit Personennamen
- **PPTX/PPT**: Hauptthemen, Folieninhalte und zentrale Botschaften
- **XLSX/XLS/XLSM/XLTX**: Art der Daten, Kategorien und Zweck der Tabelle
- **TXT**: Wichtigste Informationen und Zweck
- **MD**: Struktur, Hauptthemen und Inhalte
- **PNG/JPG/JPEG**: Bildbeschreibung, visuelle Elemente, Text und Diagramme

**Besonderheit**: Alle Prompts fordern explizit **reinen Fließtext ohne Markdown-Formatierung** an und priorisieren die Nennung von Personennamen mit ihrem Kontext.

### Adaptive Context-Verwaltung

Bei Context/Token-Overflow-Fehlern reduziert das System automatisch die Textlänge:

```
Versuch 1: 30.000 Zeichen (~7.500 Tokens)
Versuch 2: 20.000 Zeichen (~5.000 Tokens)
Versuch 3: 14.000 Zeichen (~3.500 Tokens)
Versuch 4: 10.000 Zeichen (~2.500 Tokens)
Versuch 5:  6.000 Zeichen (~1.500 Tokens)
Versuch 6:  3.000 Zeichen (~750 Tokens)
```

**Verbesserte Fehlerkennung**: Das System erkennt Context-Fehler anhand der Keywords "context", "token" oder "length" in der Fehlermeldung.

---

## Fehlerbehandlung

### Professionelle LM Studio-Fehlerbehandlung (NEU in v1.4.0)

Beim ersten LM Studio-Fehler (Netzwerk, Validierung, Typ-Fehler) wird der Benutzer gefragt, wie fortgefahren werden soll:

1. **Abbrechen**: Programm wird sofort beendet
2. **Weiter ohne Fehlerabfragen**: Fehlerhafte Dateien werden stillschweigend übersprungen
3. **Weiter mit Fehlerabfragen**: Bei jedem Fehler erfolgt eine erneute Abfrage

Diese Einstellung gilt für den gesamten Durchlauf und wird beim nächsten Programmstart zurückgesetzt.

### Häufige Probleme und Lösungen

#### LM Studio Connection Error
```
FEHLER: LM Studio ist nicht erreichbar!
```

**Lösung:**
1. Stellen Sie sicher, dass LM Studio läuft
2. Prüfen Sie, ob der Server auf Port 1234 aktiv ist
3. Verifizieren Sie die `LMSTUDIO_API_URL` im Skript
4. Überprüfen Sie, ob ein Modell geladen ist

#### Context/Token Overflow
```
  → Context/Token-Fehler (30000 Zeichen), versuche mit weniger...
```

**Lösung:**
- Automatisch gelöst durch adaptive Textkürzung
- Bei persistierenden Problemen: Kleineres Modell oder größeres Context-Fenster verwenden
- Erwägen Sie ein Reasoning-Modell (ministral-3-14b-reasoning)

#### Vision API Error (Bildanalyse)
```
Vision-Analyse fehlgeschlagen: [Error]
```

**Lösung:**
- Laden Sie ein multimodales Modell (LLaVA, BakLLaVA)
- Aktualisieren Sie LM Studio auf die neueste Version
- Prüfen Sie, ob das Modell Vision-Funktionen unterstützt

#### Legacy Office Format Warnings
```
[.doc-Datei - Textextraktion nicht vollständig möglich...]
```

**Hinweis:**
- .doc, .ppt, .xls Dateien verwenden alte Binärformate
- Für vollständige Unterstützung: Konvertierung zu .docx/.pptx/.xlsx empfohlen
- Oder Installation von LibreOffice/antiword für erweiterte Unterstützung

---

## Performance-Optimierung

### Empfohlene Einstellungen

| Aspekt | Empfehlung | Begründung |
|--------|-----------|------------|
| **Modellgröße** | 3B-14B Parameter | Balance zwischen Qualität und Geschwindigkeit |
| **GPU-Offloading** | 100% (Apple Silicon) | 10-50x schnellere Verarbeitung |
| **Batch-Größe** | 1 (Standard) | Sequentielle Verarbeitung mit Validierung |
| **Context-Länge** | 8192+ Tokens | Vermeidet häufige Textkürzungen |

### Geschwindigkeitsoptimierung

```python
# In summarize_with_lmstudio():
"temperature": 0.3,      # Niedrig = deterministischer, schneller
"max_tokens": 250,       # Limitiert auf ~650 Zeichen Output
```

**Erwartete Verarbeitungsgeschwindigkeit (Apple M1/M2):**
- Text-Dateien: 1-3 Sekunden pro Datei
- PDF (mit Text): 3-8 Sekunden pro Datei
- PDF (gescannt, OCR): 10-30 Sekunden pro Datei (abhängig von Seitenzahl)
- DOCX/XLSX/PPTX: 3-8 Sekunden pro Datei
- Bilder (Vision): 8-25 Sekunden pro Datei

**macOS-Optimierungen:**
- Native Apple Silicon-Unterstützung durch LM Studio
- OneDrive-Dateien sind direkt verfügbar (kein Download nötig)
- Effiziente Speicherverwaltung durch Python 3.12+
- Tesseract OCR mit optimierter Performance auf Apple Silicon

---

## Erweiterte Nutzung

### Skript-Parameter anpassen

#### Zusammenfassungslänge ändern
```python
# In get_prompt_for_filetype():
"...in maximal 650 Zeichen..."  # Auf gewünschte Länge anpassen

# In summarize_with_lmstudio():
"max_tokens": 250,  # Entsprechend anpassen (~2.6 Zeichen pro Token)
```

#### Retry-Strategie modifizieren
```python
# In summarize_with_lmstudio():
retry_lengths = [30000, 20000, 14000, 10000, 6000, 3000]  # Anpassen nach Bedarf
```

#### Bildgröße-Filter ändern
```python
MIN_IMAGE_SIZE = 20 * 1024  # 20 KB - strengerer Filter
# oder
MIN_IMAGE_SIZE = 5 * 1024   # 5 KB - weniger streng
```

### Integration in andere Workflows

Das JSON-Ausgabeformat ermöglicht einfache Integration:

```python
# Beispiel: JSON-Dateien einlesen und durchsuchen
import json
import glob

summaries = []
for json_file in glob.glob(os.path.expanduser("~/LLM/**/*.json"), recursive=True):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        summaries.append(data)

# Suche nach Personennamen
results = [s for s in summaries if "Marc König" in s.get("summary", "")]

# Weitere Verarbeitung...
```

---

## Sicherheit und Datenschutz

### Lokale Verarbeitung
- **Alle Daten bleiben lokal**: Keine Cloud-API-Aufrufe
- **OneDrive-Dateien**: Lokal synchronisiert und verarbeitet
- **LLM-Inferenz**: Vollständig offline über LM Studio

### Datensicherheit
- JSON-Ausgaben enthalten nur Metadaten und Zusammenfassungen
- Originaldateien bleiben unverändert
- Keine Übertragung sensibler Informationen
- Keine Telemetrie oder Analytics

---

## Versionsverlauf

### Version 1.5.1 (2025-12-25)
- **Neu**: OCR-Statistiken und -Berichterstattung
- **Neu**: OCR-Dokumentenzähler in Fortschrittsberichten
- **Neu**: Detaillierte OCR-Informationen in JSON-Ausgabe
- **Neu**: OCR-Zähler im Abschlussbericht
- **Verbessert**: Besseres Error-Handling mit Traceback bei Fehlern
- **Fix**: Robuste Tuple-Unpacking-Logik für extract_text()

### Version 1.5.0 (2025-12-25)
- **Neu**: OCR-Unterstützung für gescannte PDFs mit Tesseract
- **Neu**: Automatische Erkennung von Scan-PDFs (<10 Zeichen pro Seite)
- **Neu**: 300 DPI Auflösung für optimale OCR-Qualität
- **Neu**: Fortschrittsanzeige für mehrseitige OCR-Verarbeitung
- **Neu**: Deutsche Sprachunterstützung für OCR (lang='deu')
- **Neu**: OCR-Metadaten in Rückgabewerten (used_ocr, ocr_pages, total_pages, ocr_chars)
- **Verbessert**: Detaillierte OCR-Ergebnisausgabe

### Version 1.4.2 (2025-12-25)
- **Neu**: Erzwinge deutsche Sprache in allen LLM-Zusammenfassungen ("AUF DEUTSCH")
- **Neu**: Zeige nur erste 100 Zeichen der Zusammenfassung
- **Verbessert**: Berechne Durchschnittszeit nur für verarbeitete Dateien (nicht übersprungene)

### Version 1.4.1 (2025-12-25)
- **Fix**: Akzeptiere J/N Eingaben in Groß- und Kleinschreibung
- **Fix**: Fehlende Zusammenfassungs-Ausgabe wiederhergestellt

### Version 1.4.0 (2025-12-25)
- **Neu**: Professionelle Fehlerbehandlung mit interaktiven Benutzerabfragen
- **Neu**: Fehlerbehandlungsmodus (Abbrechen/Weiter ohne Fragen/Weiter mit Fragen)
- **Neu**: Globaler ERROR_HANDLING_MODE für konsistentes Verhalten
- **Verbessert**: ask_on_lmstudio_error() mit professionellem Layout
- **Verbessert**: Detaillierte Fehlerberichterstattung

### Version 1.3.9 (2025-12-25)
- **Verbessert**: Robuste Token/Context-Fehlerkennung
- **Fix**: Erkennung von "token", "context", "length" in Fehlermeldungen
- **Fix**: HTTP 400 Fallback auch bei JSON-Parse-Fehlern

### Version 1.3.8 (2025-12-25)
- **Neu**: LM Studio Connection Check vor Verarbeitung
- **Neu**: Minimale Bildgröße (10 KB) - ignoriert Icons
- **Verbessert**: Fehlermeldungen bei nicht erreichbarem LM Studio

### Version 1.3.7 (2025-12-25)
- **Neu**: Unterstützung für .doc, .ppt, .xls, .xlsm, .xltx
- **Neu**: Dateityp-spezifische Extraktionsfunktionen
- **Verbessert**: Fallback-Mechanismen für alte Office-Formate

### Version 1.3.6 (2025-12-25)
- **Neu**: Dateiendungs-Statistik nach Verzeichnisscan
- **Neu**: Markierung welche Dateitypen analysiert werden
- **Verbessert**: Übersichtlichere Darstellung mit Anzahl, Größe, Durchschnitt

### Version 1.3.5 (2025-12-25)
- **Fix**: Fortschrittsbalken überschreibt nun korrekt längere Zeilen
- **Verbessert**: last_line_length tracking für saubere Terminal-Ausgabe

### Version 1.3.0 (2025-12-25)
- **macOS-Portierung**: Vollständige Anpassung für macOS
- **Neu**: select() statt msvcrt für Tastatureingabe
- **Entfernt**: Windows-spezifische OneDrive Download-Logik
- **Neu**: Fortschrittsbalken beim Verzeichnisscan
- **Verbessert**: Terminal-Ausgabe mit \r für überschreibende Updates

### Version 1.2.0 (2025-12-23)
- **Neu**: Adaptive Textkürzung mit 6 Retry-Stufen
- **Neu**: Verbesserte Context-Overflow-Erkennung
- **Verbessert**: Reasoning-Model-Kompatibilität

### Version 1.1.0 (2025-12-22)
- **Neu**: Unterstützung für TXT, MD, PNG, JPG/JPEG
- **Neu**: Dateityp-spezifische Prompts für bessere Zusammenfassungen
- **Neu**: Vision API-Integration für Bildanalyse
- **Verbessert**: Text-Encoding mit UTF-8/Latin-1 Fallback

### Version 1.0.0 (2025-12-22)
- Initiale Version (Windows)
- Unterstützung für PDF, DOCX, PPTX, XLSX
- OneDrive-Integration
- Adaptive Context-Verwaltung
- JSON-Validierung
- Pause/Resume-Funktionalität

---

## Support und Feedback

### Technischer Support
Bei Problemen oder Fragen:

1. Überprüfen Sie die [Fehlerbehandlung](#fehlerbehandlung)
2. Validieren Sie Ihre [Konfiguration](#konfiguration)
3. Prüfen Sie die LM Studio Logs
4. Überprüfen Sie Terminal-Ausgaben auf Hinweise
5. Kontaktieren Sie den Entwickler mit detaillierten Fehlerprotokollen

### Feature-Requests
Vorschläge für neue Funktionen sind willkommen. Bitte spezifizieren Sie:
- Gewünschte Funktionalität
- Anwendungsfall
- Priorität
- Plattform (macOS/Windows)

---

## Lizenz und Urheberrecht

**Copyright © 2025 - Alle Rechte vorbehalten**

Dieses Tool ist proprietäre Software für den internen Gebrauch. Vervielfältigung, Weitergabe oder kommerzielle Nutzung ohne ausdrückliche Genehmigung ist untersagt.

---

## Technische Spezifikationen

### Architektur
- **Sprache**: Python 3.8+ (optimiert für 3.12+)
- **Paradigma**: Prozedural mit funktionaler Extraktion
- **Threading**: Single-threaded (sequentielle Verarbeitung)
- **Encoding**: UTF-8 (Standard), Latin-1 (Fallback)
- **Plattform**: macOS (native Unterstützung)

### API-Kompatibilität
- **LM Studio**: OpenAI-kompatibles Chat Completion API
- **HTTP-Protokoll**: POST-Requests mit JSON-Payload
- **Timeout**: 300 Sekunden (5 Minuten) pro Request
- **Vision API**: Base64-kodierte Bilder mit multimodalen Modellen

### Ressourcenverbrauch (macOS)
- **RAM**: ~200-500 MB (Skript) + LLM-Modell (3-14 GB)
- **CPU**: Niedrig (Hauptlast auf Apple Neural Engine/GPU für LLM)
- **Netzwerk**: Nur für OneDrive-Synchronisation
- **Festplatte**: ~1-5 KB pro JSON-Ausgabe

### macOS-spezifische Features
- **Non-blocking Input**: select.select() für Tastatureingabe
- **Path Expansion**: os.path.expanduser() für ~ Pfade
- **OneDrive**: Direkte Verarbeitung synchronisierter Dateien
- **Terminal**: ANSI-kompatible Fortschrittsanzeige

---

**Entwickelt mit Präzision für effiziente Dokumentenanalyse auf macOS**
