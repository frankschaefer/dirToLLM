# FileInventory - OneDrive Dokumenten-Zusammenfassung

**Version:** 1.1.0
**Datum:** 2025-12-22
**Lizenz:** Proprietär

## Übersicht

FileInventory ist ein intelligentes Python-Tool zur automatischen Analyse und Zusammenfassung von Dokumenten in OneDrive-Verzeichnissen. Das System nutzt lokale Large Language Models (LLM) über LM Studio, um kompakte, aussagekräftige Zusammenfassungen von verschiedenen Dateiformaten zu erstellen.

### Hauptfunktionen

- **Multiformat-Unterstützung**: PDF, Word, Excel, PowerPoint, Text, Markdown und Bilder
- **OneDrive-Integration**: Automatischer Download von "nur online verfügbaren" Dateien
- **LLM-basierte Analyse**: Intelligente Zusammenfassungen mit dateityp-spezifischen Prompts
- **Vision-Fähigkeit**: Bildanalyse und -beschreibung mittels multimodaler Modelle
- **Validierung**: Automatische Überprüfung und Neuerstellung fehlerhafter JSON-Ausgaben
- **Fortschrittsüberwachung**: Detaillierte Zeitschätzungen und Statistiken
- **Interaktive Steuerung**: Pause/Resume-Funktionalität während der Verarbeitung

---

## Systemanforderungen

### Betriebssystem
- Windows 10/11 (erforderlich für OneDrive-Integration)

### Software
- **Python**: Version 3.8 oder höher
- **LM Studio**: Aktuelle Version mit laufendem lokalem Server

### Hardware-Empfehlungen
- **RAM**: Mindestens 8 GB (16 GB empfohlen)
- **GPU**: Optional, beschleunigt LLM-Inferenz erheblich
- **Festplatte**: Ausreichend Speicherplatz für JSON-Ausgaben

---

## Installation

### 1. Python Installation

#### Option A: Microsoft Store (Empfohlen für Windows)
```powershell
# Öffnen Sie den Microsoft Store und suchen Sie nach "Python 3.12"
# oder verwenden Sie den direkten Link:
# ms-windows-store://pdp/?productid=9NCVDN91XZQP
```

#### Option B: Python.org
1. Besuchen Sie [python.org/downloads](https://www.python.org/downloads/)
2. Laden Sie Python 3.12.x herunter
3. **Wichtig**: Aktivieren Sie "Add Python to PATH" während der Installation

#### Verifizierung
```cmd
python --version
# Erwartete Ausgabe: Python 3.12.x
```

### 2. Python-Bibliotheken installieren

Öffnen Sie eine Kommandozeile (CMD oder PowerShell) und führen Sie folgende Befehle aus:

```cmd
# Navigieren Sie zum Skript-Verzeichnis
cd "D:\Dropbox\Frank\Code\MKU"

# Installieren Sie alle erforderlichen Bibliotheken
pip install pdfplumber python-docx python-pptx openpyxl requests
```

#### Einzelne Bibliotheken (zur Referenz)

| Bibliothek | Zweck | Installation |
|------------|-------|--------------|
| `pdfplumber` | PDF-Textextraktion | `pip install pdfplumber` |
| `python-docx` | Word-Dokumentenverarbeitung | `pip install python-docx` |
| `python-pptx` | PowerPoint-Analyse | `pip install python-pptx` |
| `openpyxl` | Excel-Datenextraktion | `pip install openpyxl` |
| `requests` | HTTP-Kommunikation mit LM Studio | `pip install requests` |

### 3. LM Studio Installation und Konfiguration

#### Installation
1. Laden Sie LM Studio herunter: [lmstudio.ai](https://lmstudio.ai/)
2. Installieren Sie die Anwendung
3. Laden Sie ein LLM-Modell herunter (Empfehlungen siehe unten)

#### Modell-Empfehlungen

##### Für Textverarbeitung (Standard)
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

---

## Konfiguration

### Verzeichnispfade anpassen

Öffnen Sie `FileInventory.py` und passen Sie die Pfade an:

```python
# Quellverzeichnis (OneDrive)
SRC_ROOT = r"C:\Users\frank\OneDrive - Marc König Unternehmensberatung"

# Zielverzeichnis für JSON-Ausgaben
DST_ROOT = r"D:\LLM"
```

### Dateitypen konfigurieren

Standardmäßig werden folgende Formate verarbeitet:

```python
EXTENSIONS = {".pdf", ".docx", ".pptx", ".xlsx", ".txt", ".md", ".png", ".jpg", ".jpeg"}
```

**Anpassung**: Entfernen oder ergänzen Sie Dateitypen nach Bedarf.

---

## Verwendung

### Basis-Ausführung

```cmd
cd "D:\Dropbox\Frank\Code\MKU"
python FileInventory.py
```

### Interaktive Steuerung während der Ausführung

- **Pause**: Drücken Sie eine beliebige Taste während der Verarbeitung
- **Fortsetzen**: Wählen Sie `J` (Ja)
- **Abbrechen**: Wählen Sie `N` (Nein)

### Ausgabeformat

Für jede verarbeitete Datei wird eine JSON-Datei erstellt:

```json
{
  "name": "Beispieldokument.pdf",
  "path": "Projekte\\Kunde_A\\Beispieldokument.pdf",
  "ext": ".pdf",
  "size": 1048576,
  "created": "2025-01-15T10:30:00",
  "modified": "2025-01-20T14:45:00",
  "chars": 15420,
  "summary": "Projektübersicht für Kunde A mit Meilensteinen Q1-Q4 2025..."
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
| `summary` | KI-generierte Zusammenfassung (max. 500 Zeichen) |

---

## Funktionsweise

### Verarbeitungspipeline

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Dateiscan                                                │
│    └─> Rekursive Durchsuchung des OneDrive-Verzeichnisses  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. OneDrive-Download                                        │
│    └─> Prüfung auf "nur online" + automatischer Download   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Textextraktion                                           │
│    ├─> PDF: pdfplumber                                     │
│    ├─> DOCX: python-docx                                   │
│    ├─> PPTX: python-pptx                                   │
│    ├─> XLSX: openpyxl (Werte, keine Formeln)              │
│    ├─> TXT/MD: UTF-8 + Latin-1 Fallback                   │
│    └─> PNG/JPG: Base64 + Vision API                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. LLM-Zusammenfassung                                      │
│    ├─> Dateityp-spezifische Prompts                        │
│    ├─> Adaptive Textkürzung (14k → 1.5k Zeichen)          │
│    └─> Context-Overflow Handling mit automatischem Retry   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. JSON-Ausgabe                                             │
│    ├─> Validierung vorhandener Dateien                     │
│    └─> Speicherung unter DST_ROOT                          │
└─────────────────────────────────────────────────────────────┘
```

### Dateityp-spezifische Prompts

Das System verwendet optimierte Prompts für jeden Dateityp:

- **PDF/DOCX**: Fokus auf Inhalte, Themen und Kernaussagen
- **PPTX**: Hauptthemen, Folieninhalte und zentrale Botschaften
- **XLSX**: Art der Daten, Kategorien und Zweck der Tabelle
- **TXT**: Wichtigste Informationen und Zweck
- **MD**: Struktur, Hauptthemen und Inhalte
- **PNG/JPG**: Bildbeschreibung, visuelle Elemente, Text und Diagramme

### Adaptive Context-Verwaltung

Bei Context-Overflow-Fehlern reduziert das System automatisch die Textlänge:

```
Versuch 1: 14.000 Zeichen (~3.500 Tokens)
Versuch 2: 10.000 Zeichen (~2.500 Tokens)
Versuch 3:  6.000 Zeichen (~1.500 Tokens)
Versuch 4:  3.000 Zeichen (~750 Tokens)
Versuch 5:  1.500 Zeichen (~375 Tokens)
```

---

## Fehlerbehandlung

### Häufige Probleme und Lösungen

#### LM Studio Connection Error
```
HTTPConnectionPool(host='localhost', port=1234): Connection refused
```

**Lösung:**
1. Stellen Sie sicher, dass LM Studio läuft
2. Prüfen Sie, ob der Server auf Port 1234 aktiv ist
3. Verifizieren Sie die `LMSTUDIO_API_URL` im Skript

#### Context Overflow
```
Trying to keep the first 4509 tokens when context overflows...
```

**Lösung:**
- Automatisch gelöst durch adaptive Textkürzung
- Bei persistierenden Problemen: Kleineres Modell oder größeres Context-Fenster verwenden

#### OneDrive Download Timeout
```
Timeout beim Herunterladen von [Datei]
```

**Lösung:**
1. Prüfen Sie Ihre Internetverbindung
2. Erhöhen Sie `max_wait` in `download_onedrive_file()` (Standard: 60 Sekunden)
3. Laden Sie große Dateien manuell herunter

#### Vision API Error (Bildanalyse)
```
Vision-Analyse fehlgeschlagen: [Error]
```

**Lösung:**
- Laden Sie ein multimodales Modell (LLaVA, BakLLaVA)
- Aktualisieren Sie LM Studio auf die neueste Version
- Prüfen Sie, ob das Modell Vision-Funktionen unterstützt

---

## Performance-Optimierung

### Empfohlene Einstellungen

| Aspekt | Empfehlung | Begründung |
|--------|-----------|------------|
| **Modellgröße** | 3B-7B Parameter | Balance zwischen Qualität und Geschwindigkeit |
| **GPU-Offloading** | 100% (falls verfügbar) | 10-50x schnellere Verarbeitung |
| **Batch-Größe** | 1 (Standard) | Sequentielle Verarbeitung mit Validierung |
| **Context-Länge** | 4096+ Tokens | Vermeidet häufige Textkürzungen |

### Geschwindigkeitsoptimierung

```python
# In summarize_with_lmstudio():
"temperature": 0.3,      # Niedrig = deterministischer, schneller
"max_tokens": 200,       # Limitiert auf ~500 Zeichen Output
```

**Erwartete Verarbeitungsgeschwindigkeit:**
- Text-Dateien: 2-5 Sekunden pro Datei
- PDF/DOCX: 5-10 Sekunden pro Datei
- Bilder (Vision): 10-30 Sekunden pro Datei

---

## Erweiterte Nutzung

### Skript-Parameter anpassen

#### Zusammenfassungslänge ändern
```python
# In get_prompt_for_filetype():
"...in maximal 500 Zeichen..."  # Auf gewünschte Länge anpassen

# In summarize_with_lmstudio():
if len(summary) > 500:  # Entsprechend anpassen
    summary = summary[:497] + "..."
```

#### Retry-Strategie modifizieren
```python
# In summarize_with_lmstudio():
retry_lengths = [14000, 10000, 6000, 3000, 1500]  # Anpassen nach Bedarf
```

### Integration in andere Workflows

Das JSON-Ausgabeformat ermöglicht einfache Integration:

```python
# Beispiel: JSON-Dateien einlesen
import json
import glob

summaries = []
for json_file in glob.glob("D:/LLM/**/*.json", recursive=True):
    with open(json_file, 'r', encoding='utf-8') as f:
        summaries.append(json.load(f))

# Weitere Verarbeitung...
```

---

## Sicherheit und Datenschutz

### Lokale Verarbeitung
- **Alle Daten bleiben lokal**: Keine Cloud-API-Aufrufe
- **OneDrive-Dateien**: Werden lokal heruntergeladen und verarbeitet
- **LLM-Inferenz**: Vollständig offline über LM Studio

### Datensicherheit
- JSON-Ausgaben enthalten nur Metadaten und Zusammenfassungen
- Originaldateien bleiben unverändert
- Keine Übertragung sensibler Informationen

---

## Versionsverlauf

### Version 1.1.0 (2025-12-22)
- **Neu**: Unterstützung für TXT, MD, PNG, JPG/JPEG
- **Neu**: Dateityp-spezifische Prompts für bessere Zusammenfassungen
- **Neu**: Vision API-Integration für Bildanalyse
- **Verbessert**: Text-Encoding mit UTF-8/Latin-1 Fallback

### Version 1.0.0 (2025-12-22)
- Initiale Version
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
4. Kontaktieren Sie den Entwickler mit detaillierten Fehlerprotokollen

### Feature-Requests
Vorschläge für neue Funktionen sind willkommen. Bitte spezifizieren Sie:
- Gewünschte Funktionalität
- Anwendungsfall
- Priorität

---

## Lizenz und Urheberrecht

**Copyright © 2025 - Alle Rechte vorbehalten**

Dieses Tool ist proprietäre Software für den internen Gebrauch. Vervielfältigung, Weitergabe oder kommerzielle Nutzung ohne ausdrückliche Genehmigung ist untersagt.

---

## Technische Spezifikationen

### Architektur
- **Sprache**: Python 3.8+
- **Paradigma**: Prozedural mit funktionaler Extraktion
- **Threading**: Single-threaded (sequentielle Verarbeitung)
- **Encoding**: UTF-8 (Standard), Latin-1 (Fallback)

### API-Kompatibilität
- **LM Studio**: OpenAI-kompatibles Chat Completion API
- **HTTP-Protokoll**: POST-Requests mit JSON-Payload
- **Timeout**: 300 Sekunden (5 Minuten) pro Request

### Ressourcenverbrauch
- **RAM**: ~200-500 MB (Skript) + LLM-Modell (3-8 GB)
- **CPU**: Niedrig (Hauptlast auf GPU für LLM)
- **Netzwerk**: Nur für OneDrive-Downloads
- **Festplatte**: ~1-5 KB pro JSON-Ausgabe

---

**Entwickelt mit Präzision für effiziente Dokumentenanalyse**
