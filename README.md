# FileInventory - OneDrive Dokumenten-Zusammenfassung (macOS)

**Version:** 1.9.0
**Datum:** 2025-12-28
**Lizenz:** Proprietär

## Übersicht

FileInventory ist ein intelligentes Python-Tool zur automatischen Analyse und Zusammenfassung von Dokumenten in OneDrive-Verzeichnissen. Das System nutzt lokale Large Language Models (LLM) über LM Studio, um kompakte, aussagekräftige Zusammenfassungen von verschiedenen Dateiformaten zu erstellen.

### Hauptfunktionen

- **Multiformat-Unterstützung**: PDF, Word (.docx/.doc), Excel (.xlsx/.xls/.xlsm/.xltx), PowerPoint (.pptx/.ppt), Text, Markdown und Bilder
- **OCR-Unterstützung**: Automatische Texterkennung für gescannte PDFs mit Tesseract OCR
- **RAG-Optimierung**: Wissensextraktion für semantische Suche mit Schlüsselbegriffen und strukturierter Zusammenfassung
- **Kombinierte Datenbank**: Erstellt durchsuchbare JSON-Datenbanken für ChatGPT/Claude (NEU in v1.9.0)
- **macOS-optimiert**: Native macOS-Unterstützung mit OneDrive-Integration
- **LLM-basierte Analyse**: Intelligente Zusammenfassungen mit RAG-optimierten, dateityp-spezifischen Prompts
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
- **mistralai/ministral-3-14b-reasoning** (empfohlen, getestet - 262k Tokens Context, hohe Präzision)
- **ministral-3-3b-instruct** (leichtgewichtig, schnell)
- **Mistral-7B-Instruct** (ausgewogen)
- **Llama-3-8B-Instruct** (hochwertig)
- **Qwen-2.5-14B** (sehr gut für deutsche Texte, 32k Tokens Context)

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

# Modell Context-Länge (maximale Anzahl Tokens)
# Passen Sie dies an Ihr Modell an:
# - Kleinere Modelle (z.B. Llama 3 8B): 8192
# - Größere Modelle (z.B. Qwen 2.5 14B): 32768
# - Reasoning-Modelle (z.B. mistralai/ministral-3-14b-reasoning): 262144
MAX_CONTEXT_TOKENS = 262144
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

### Kommandozeilenparameter

FileInventory unterstützt folgende Kommandozeilenparameter:

```bash
# Hilfe anzeigen
python3 FileInventory.py -h
python3 FileInventory.py --help

# Version anzeigen
python3 FileInventory.py --version

# Mit benutzerdefinierten Verzeichnissen
python3 FileInventory.py --src ~/Documents --dst ~/Summaries

# Kleineres Modell mit 8k Token Context
python3 FileInventory.py --max-tokens 8192

# Vollständig benutzerdefiniert
python3 FileInventory.py --src ~/Docs --dst ~/Summaries --max-tokens 32768

# Kombinierte Datenbank erstellen (empfohlen für ChatGPT/Claude)
python3 FileInventory.py --create-database

# Datenbank mit benutzerdefinierter Größe
python3 FileInventory.py --create-database --max-database-size 50

# Datenbank in benutzerdefiniertem Verzeichnis
python3 FileInventory.py --create-database --database-output ~/MyDatabase

# Standard-Verzeichnisse und -Einstellungen verwenden
python3 FileInventory.py
```

**Verfügbare Parameter:**

| Parameter | Beschreibung | Standard |
|-----------|--------------|----------|
| `-h`, `--help` | Zeigt Hilfe und alle verfügbaren Optionen | - |
| `--version` | Zeigt Versionsinformation | - |
| `--src VERZEICHNIS` | Quellverzeichnis für Dokumente | `~/OneDrive - Marc König Unternehmensberatung` |
| `--dst VERZEICHNIS` | Zielverzeichnis für JSON-Dateien | `~/LLM` |
| `--max-tokens TOKENS` | Maximale Context-Länge des Modells in Tokens | `262144` |
| `--create-database` | Erstellt kombinierte JSON-Datenbank aus allen einzelnen JSON-Dateien | - |
| `--database-output DIR` | Ausgabeverzeichnis für Datenbank-Dateien | `~/LLM/database` |
| `--max-database-size MB` | Maximale Größe pro Datenbank-Datei in MB | `30` |

### Basis-Ausführung

```bash
cd ~/Library/CloudStorage/Dropbox/Frank/Code/MKU

# Mit virtueller Umgebung
source .venv/bin/activate
python3 FileInventory.py

# Ohne virtuelle Umgebung
python3 FileInventory.py

# Mit benutzerdefinierten Verzeichnissen
python3 FileInventory.py --src ~/Documents --dst ~/Summaries
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

### Kombinierte Datenbank erstellen (NEU in v1.9.0)

Nach der Verarbeitung Ihrer Dokumente können Sie eine kombinierte JSON-Datenbank erstellen, die alle Zusammenfassungen in wenigen großen Dateien zusammenfasst. Dies ist ideal für die Verwendung mit ChatGPT oder Claude.

#### Datenbank erstellen

```bash
# Aktiviere virtuelle Umgebung
source .venv/bin/activate

# Erstelle Datenbank mit Standard-Einstellungen (max 30 MB pro Datei)
python3 FileInventory.py --create-database
```

#### Ausgabe

Die Datenbank wird standardmäßig im Verzeichnis `~/LLM/database/` erstellt:

```
~/LLM/database/
  ├── file_database_001.json  (10.19 MB, 6,283 Dokumente)
```

#### Datenbankstruktur

Jede Datenbank-Datei enthält Metadaten und alle Dokumente:

```json
{
  "metadata": {
    "created": "2025-12-28T19:18:03.965074",
    "source_directory": "/Users/fs_mku/OneDrive - Marc König Unternehmensberatung",
    "json_directory": "/Users/fs_mku/LLM",
    "script_version": "1.9.0",
    "script_date": "2025-12-28",
    "batch_number": 1,
    "documents_in_batch": 6283,
    "max_size_mb": 30
  },
  "documents": [
    {
      "path": "Projekte/Kunde_A/Beispieldokument.pdf",
      "ext": ".pdf",
      "size": 1048576,
      "summary": "...",
      "keywords": ["Projekt", "Kunde A", "..."]
    },
    ...
  ]
}
```

#### Verwendung mit ChatGPT/Claude

1. **Lade die Datenbank-Datei hoch** zu ChatGPT oder Claude
2. **Stelle Fragen** über Ihre Dokumente:
   - "Suche alle Projekte mit dem Kunden X"
   - "Welche Dokumente erwähnen digitale Transformation?"
   - "Finde alle PDFs von Marc König"
   - "Liste alle Dokumente mit dem Keyword 'Innovation' auf"

#### Erweiterte Optionen

```bash
# Kleinere Dateien (z.B. 5 MB für bessere Uploads)
python3 FileInventory.py --create-database --max-database-size 5

# Benutzerdefiniertes Ausgabeverzeichnis
python3 FileInventory.py --create-database --database-output ~/Desktop/Datenbank

# Mit benutzerdefinierten Quell-Verzeichnissen
python3 FileInventory.py --dst ~/Summaries --create-database
```

#### Vorteile der Datenbank

- **Schnellere Uploads**: Eine große Datei statt tausende kleine
- **Bessere Durchsuchbarkeit**: ChatGPT/Claude kann alle Dokumente auf einmal durchsuchen
- **Metadaten**: Enthält Versionsinformationen und Verarbeitungsdetails
- **Flexible Größe**: Automatische Aufteilung bei Überschreitung der max. Größe

### Ausgabeformat (Einzelne JSON-Dateien)

Für jede verarbeitete Datei wird eine JSON-Datei erstellt:

```json
{
  "path": "Projekte/Kunde_A/Beispieldokument.pdf",
  "ext": ".pdf",
  "size": 1048576,
  "created": "2025-01-15T10:30:00",
  "modified": "2025-01-20T14:45:00",
  "chars": 15420,
  "summary": "Projektübersicht für Kunde A mit Marc König als Projektleiter. Beschreibt Meilensteine Q1-Q4 2025 mit Fokus auf digitale Transformation und Prozessoptimierung.",
  "keywords": [
    "Projektübersicht",
    "Marc König",
    "Meilensteine 2025",
    "Digitale Transformation",
    "Prozessoptimierung",
    "Q1-Q4"
  ],
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
| `path` | Relativer Pfad zur Quelldatei (inkl. Dateiname) |
| `ext` | Dateierweiterung |
| `size` | Dateigröße in Bytes |
| `created` | Erstellungszeitpunkt (ISO 8601) |
| `modified` | Letzte Änderung (ISO 8601) |
| `chars` | Anzahl extrahierter Zeichen |
| `summary` | KI-generierte Zusammenfassung (max. 1000 Zeichen, RAG-optimiert, auf Deutsch) |
| `keywords` | **Array:** Extrahierte Schlüsselbegriffe als Liste für schnelle Kategorisierung |
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

### RAG-optimierte Wissensextraktion

Das System verwendet einen spezialisierten RAG-Ansatz (Retrieval-Augmented Generation) für maximale Auffindbarkeit:

**Prompt-Struktur:**
- Sachliche, informationsdichte Zusammenfassungen ohne Meta-Kommentare
- Beibehaltung wichtiger Fachbegriffe, Zahlen, Technologien und Personennamen
- Beschreibung von Zweck, Inhalt, Kontext und Besonderheiten
- Strukturierte Darstellung: Was? Wozu? Welche Inhalte? Was ist besonders?
- **Kommagetrennte Schlüsselbegriff-Liste** am Ende jeder Zusammenfassung

**Dateityp-spezifische Schwerpunkte:**
- **PDF/DOCX/DOC**: Dokumenteninhalt, Kernaussagen, Personen und ihre Rollen
- **PPTX/PPT**: Präsentationsthemen, Kernbotschaften, Folienstruktur
- **XLSX/XLS/XLSM/XLTX**: Datenarten, Kategorien, Zahlen, Automatisierung
- **TXT/MD**: Textinhalt, Dokumentstruktur, technische Details
- **PNG/JPG/JPEG**: Bildinhalte, sichtbarer Text, Diagramme, Personen

**Vorteile für semantische Suche:**
- Maximale Informationsdichte (bis zu 1000 Zeichen)
- **Separates Keywords-Array** für schnelle Kategorisierung und Filterung
- Automatische Extraktion der Schlüsselbegriffe aus der LLM-Antwort
- Keine ablenkenden Formatierungen oder Füllwörter
- Optimiert für Vektorsuche und RAG-Systeme
- Keywords ermöglichen effiziente Volltextsuche und Indexierung

### Adaptive Context-Verwaltung

Das System berechnet automatisch die optimale Textlänge basierend auf `MAX_CONTEXT_TOKENS`:

**Beispiel für MAX_CONTEXT_TOKENS = 262144 (ministral-3-14b-reasoning):**
```
Versuch 1: 1.044.576 Zeichen (~261.000 Tokens) - Nutzt fast vollen Context
Versuch 2:   699.666 Zeichen (~175.000 Tokens) - 67% des Max-Context
Versuch 3:   490.951 Zeichen (~123.000 Tokens) - 47% des Max-Context
Versuch 4:   344.710 Zeichen  (~86.000 Tokens) - 33% des Max-Context
Versuch 5:   208.915 Zeichen  (~52.000 Tokens) - 20% des Max-Context
Versuch 6:     3.000 Zeichen     (~750 Tokens) - Minimum-Fallback
```

**Beispiel für MAX_CONTEXT_TOKENS = 8192 (kleinere Modelle):**
```
Versuch 1: 28.768 Zeichen (~7.200 Tokens)
Versuch 2: 19.274 Zeichen (~4.800 Tokens)
Versuch 3: 13.520 Zeichen (~3.400 Tokens)
Versuch 4:  9.493 Zeichen (~2.400 Tokens)
Versuch 5:  5.753 Zeichen (~1.400 Tokens)
Versuch 6:  3.000 Zeichen   (~750 Tokens)
```

**Annahme**: ~4 Zeichen pro Token (konservativ für deutsche Texte)

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
"max_tokens": 400,       # Limitiert auf ~1000 Zeichen Output
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
# In get_prompt_for_filetype() - Basis-Prompt:
"Maximal 1000 Zeichen"  # Auf gewünschte Länge anpassen

# In summarize_with_lmstudio():
"max_tokens": 400,  # Entsprechend anpassen (~2.5 Zeichen pro Token)
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

# Suche nach Personennamen in der Zusammenfassung
results = [s for s in summaries if "Marc König" in s.get("summary", "")]

# Suche nach Keywords
keyword_results = [s for s in summaries if "Digitale Transformation" in s.get("keywords", [])]

# Kombinierte Suche
combined = [s for s in summaries
            if any(kw in ["Projekt", "Transformation"] for kw in s.get("keywords", []))]

# Gruppierung nach Keywords
from collections import Counter
all_keywords = []
for s in summaries:
    all_keywords.extend(s.get("keywords", []))
top_keywords = Counter(all_keywords).most_common(10)

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

### Version 1.9.0 (2025-12-28)
- **Neu**: `--create-database` Parameter zum Erstellen kombinierter JSON-Datenbanken
- **Neu**: Automatische Aufteilung in mehrere Dateien basierend auf Größenlimit
- **Neu**: `--database-output DIR` zur Angabe eines benutzerdefinierten Ausgabeverzeichnisses
- **Neu**: `--max-database-size MB` zur Kontrolle der maximalen Datenbankdateigröße
- **Neu**: Metadaten in Datenbank-Dateien (Version, Zeitstempel, Quellverzeichnisse)
- **Neu**: Fortschrittsanzeige während der Datenbank-Erstellung
- **Neu**: Detaillierte Statistiken nach Datenbank-Erstellung
- **Verbessert**: Optimiert für ChatGPT/Claude-Integration
- **Verbessert**: JSON-Struktur mit separaten Metadaten und Dokumenten-Arrays
- **Dokumentiert**: Neue Sektion in README mit Beispielen und Best Practices

### Version 1.8.0 (2025-12-25)
- **Neu**: Alphabetische Sortierung von Verzeichnissen und Dateien während der Verarbeitung
- **Neu**: Zeitstempelprüfung beim Überspringen existierender JSON-Dateien
- **Verbessert**: Automatische Neuverarbeitung wenn `created` oder `modified` Zeitstempel geändert wurden
- **Verbessert**: Konsistente Verarbeitungsreihenfolge durch Sortierung
- **Fix**: Verhindert übersprungene Updates bei Dateiänderungen

### Version 1.7.4 (2025-12-25)
- **Debug**: Erweiterte Fehlerausgaben bei Context/Token-Fehlern
- **Debug**: Zeigt geschätzte Token-Anzahl und tatsächliche LLM-Fehlermeldung
- **Verbessert**: Bessere Diagnose von Context-Problemen für Fehlersuche
- **Hilfe**: Ermöglicht Identifikation von LM Studio Konfigurationsproblemen

### Version 1.7.3 (2025-12-25)
- **Verbessert**: Breitere erste Spalte in Dateiendungen-Statistik (18 statt 10 Zeichen)
- **Fix**: Lange Dateiendungen wie ".herunterladen" werden jetzt korrekt dargestellt
- **Optimiert**: Tabellenbreite auf 80 Zeichen erweitert für bessere Lesbarkeit

### Version 1.7.2 (2025-12-25)
- **Fix**: Intelligente retry_lengths - berücksichtigt jetzt tatsächliche Textlänge
- **Optimiert**: Vermeidet unnötige Retry-Versuche mit zu großen Textlängen
- **Verbessert**: Entfernt Duplikate aus retry_lengths für effizientere Verarbeitung
- **Beispiel**: 23k Zeichen Text → nur 2 Versuche statt 6

### Version 1.7.1 (2025-12-25)
- **Neu**: `--max-tokens TOKENS` Parameter für dynamische Context-Länge
- **Verbessert**: MAX_CONTEXT_TOKENS kann per Kommandozeile überschrieben werden
- **Verbessert**: Erweiterte Hilfe mit Beispielen für verschiedene Modellgrößen
- **Optimiert**: Flexible Anpassung an verschiedene LLM-Modelle ohne Code-Änderung

### Version 1.7.0 (2025-12-25)
- **Neu**: Professionelle Kommandozeilenparameter-Unterstützung mit argparse
- **Neu**: `-h` / `--help` zeigt Hilfe und alle verfügbaren Optionen
- **Neu**: `--version` zeigt Versionsinformation an
- **Neu**: `--src VERZEICHNIS` für benutzerdefiniertes Quellverzeichnis
- **Neu**: `--dst VERZEICHNIS` für benutzerdefiniertes Zielverzeichnis
- **Verbessert**: Detaillierte Hilfe mit Beispielen und Konfigurationshinweisen
- **Dokumentiert**: Alle Parameter in der README mit Beispielen

### Version 1.6.8 (2025-12-25)
- **Neu**: Konfigurierbare MAX_CONTEXT_TOKENS für unterschiedliche Modellgrößen
- **Neu**: Automatische Berechnung der retry_lengths basierend auf Modell-Context
- **Verbessert**: Unterstützung für große Context-Fenster (bis 262k Tokens)
- **Getestet**: Erfolgreich mit mistralai/ministral-3-14b-reasoning (262k Tokens)
- **Optimiert**: Bessere Nutzung der verfügbaren Context-Länge

### Version 1.6.7 (2025-12-25)
- **Neu**: OCR-Funktionalitätsprüfung beim Programmstart mit detailliertem Status
- **Neu**: Prüfung ob Tesseract installiert ist und deutsche Sprache verfügbar ist
- **Fix**: OCR_AVAILABLE als globale Variable - behebt "name 'ocr_available' is not defined" Fehler
- **Verbessert**: Klare Warnung beim Start wenn OCR nicht verfügbar ist
- **Verbessert**: Anzeige der Tesseract-Version und Sprachunterstützung

### Version 1.6.6 (2025-12-25)
- **Verbessert**: Deutlich verbesserte Fehlermeldung für gescannte PDFs ohne OCR-Unterstützung
- **Verbessert**: Zeigt Installationsanweisungen für Tesseract OCR an (macOS, Linux, Python)
- **Verbessert**: Klar abgegrenzte Warnung mit Erklärung warum Datei übersprungen wird
- **Fix**: Benutzer werden jetzt direkt informiert dass OCR-Installation benötigt wird

### Version 1.6.5 (2025-12-25)
- **Fix**: Keyword-Extraktion funktioniert jetzt korrekt mit "Schlüsselbegriffe:", "Keywords:" Markern
- **Verbessert**: Robuste Regex-basierte Keyword-Erkennung mit mehreren Fallback-Optionen
- **Verbessert**: Keywords werden auch bei längeren Zeilen (>200 Zeichen) korrekt extrahiert
- **Verbessert**: Automatisches Entfernen der Keyword-Zeile aus der Zusammenfassung

### Version 1.6.4 (2025-12-25)
- **Fix**: OCR-Zähler funktioniert jetzt auch bei übersprungenen (bereits verarbeiteten) Dateien
- **Verbessert**: Prompts optimiert - kein Markdown, keine Meta-Begriffe wie "Zusammenfassung" oder "Diese Datei enthält"
- **Verbessert**: System-Prompt fordert reinen Fließtext ohne Formatierung
- **Verbessert**: Direkter Einstieg in Inhalte ohne Einleitungen

### Version 1.6.3 (2025-12-25)
- **Fix**: OCR-Zähler wird jetzt korrekt aktualisiert (auch bei bereits verarbeiteten Dateien)
- **Fix**: OCR-Warnung "nicht verfügbar" erscheint nur einmal pro PDF statt bei jeder Seite
- **Verbessert**: OCR-Import-Check erfolgt einmal zu Beginn der PDF-Verarbeitung
- **Verbessert**: OCR-Statistik aus existierenden JSON-Dateien wird korrekt gelesen

### Version 1.6.2 (2025-12-25)
- **Optimiert**: Redundantes `name` Feld aus JSON-Struktur entfernt
- **Verbessert**: Dateiname ist bereits im `path` Feld enthalten
- **Optimiert**: Schlankere JSON-Dateien durch reduzierten Speicherbedarf

### Version 1.6.1 (2025-12-25)
- **Neu**: Separates `keywords` Feld in JSON-Struktur
- **Neu**: Automatische Extraktion der Schlüsselbegriffe aus LLM-Antwort
- **Verbessert**: Keywords als Array für einfache Filterung und Suche
- **Verbessert**: Zusammenfassung und Keywords werden getrennt gespeichert
- **Optimiert**: README mit erweiterten Integration-Beispielen

### Version 1.6.0 (2025-12-25)
- **Neu**: RAG-optimierte Prompt-Struktur für semantische Suche
- **Neu**: Kommagetrennte Schlüsselbegriff-Liste in jeder Zusammenfassung
- **Verbessert**: Zusammenfassungslänge auf 1000 Zeichen erhöht
- **Verbessert**: Informationsdichte durch strukturierte Wissensextraktion
- **Verbessert**: System-Prompt fokussiert auf Fakten, Zahlen und Fachbegriffe
- **Verbessert**: max_tokens auf 400 erhöht für längere Ausgaben
- **Optimiert**: Prompts ohne Meta-Kommentare und Füllwörter
- **Optimiert**: Bessere Auffindbarkeit durch strukturierte Darstellung (Was? Wozu? Welche Inhalte? Besonderheiten?)

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
