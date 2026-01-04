# Plattform-Unterstützung

FileInventory unterstützt Windows 11, macOS 15+ (Sequoia) und Linux mit automatischer Plattformerkennung.

## Unterstützte Plattformen

### ✅ Windows 11
- **Automatische Erkennung:** OneDrive Personal & Business
- **Standard-Pfade:**
  - Quelle: `%OneDriveCommercial%` oder `%OneDrive%` oder `%USERPROFILE%\Documents`
  - Ziel: `%USERPROFILE%\LLM`
- **Besonderheiten:**
  - Verwendet `msvcrt` für Tastatureingabe-Erkennung
  - UTF-8 Encoding (Windows 11 Standard)
  - Tesseract Installation: `winget install UB-Mannheim.TesseractOCR`

### ✅ macOS 15+ (Sequoia)
- **Automatische Erkennung:** OneDrive in iCloud Storage
- **Standard-Pfade:**
  - Quelle: `~/Library/CloudStorage/OneDrive-*` oder `~/OneDrive` (Legacy)
  - Ziel: `~/LLM`
- **Besonderheiten:**
  - Verwendet `select()` für Tastatureingabe-Erkennung
  - UTF-8 Encoding
  - Tesseract Installation: `brew install tesseract tesseract-lang`
  - Unterstützt Apple Silicon (M1/M2/M3) und Intel Macs

### ✅ Linux (Ubuntu, Debian, Fedora, etc.)
- **Standard-Pfade:**
  - Quelle: `~/Documents`
  - Ziel: `~/LLM`
- **Besonderheiten:**
  - Verwendet `select()` für Tastatureingabe-Erkennung
  - UTF-8 Encoding
  - Tesseract Installation: `sudo apt-get install tesseract-ocr tesseract-ocr-deu`

## Konfiguration

Die Plattform-Konfiguration erfolgt automatisch über `platform_config.py`.

### Manuelle Anpassung

Wenn Sie die Standard-Pfade ändern möchten, bearbeiten Sie `platform_config.py`:

```python
# Beispiel: Eigene Pfade für Windows
if self.system == 'Windows':
    self.default_src = r'C:\MeineDaten\OneDrive'
    self.default_dst = r'C:\MeineDaten\LLM'
```

### Kommandozeilen-Parameter

Sie können die Pfade auch per Kommandozeile überschreiben:

```bash
# Windows
python FileInventory.py --src "C:\MeineDaten" --dst "C:\Output"

# macOS/Linux
python3 FileInventory.py --src ~/Dokumente --dst ~/Ausgabe
```

## Plattform-Informationen anzeigen

```bash
python3 platform_config.py
```

Ausgabe:
```
=== Plattform-Konfiguration ===
Plattform: macOS
System: Darwin 25.2.0
Python: 3.12.0
Standard Quellverzeichnis: /Users/username/Library/CloudStorage/OneDrive-Personal
Standard Zielverzeichnis: /Users/username/LLM
Tesseract OCR: /opt/homebrew/bin/tesseract
```

## Plattformspezifische Features

### Tastatureingabe während Verarbeitung

**Windows:** Verwendet `msvcrt.kbhit()` für nicht-blockierende Eingabe

**macOS/Linux:** Verwendet `select.select()` für nicht-blockierende Eingabe

### OneDrive-Erkennung

**Windows:**
- Prüft `OneDriveCommercial` (Business) und `OneDrive` (Personal) Umgebungsvariablen
- Fallback auf `Documents` Ordner

**macOS:**
- Sucht in `~/Library/CloudStorage/` nach `OneDrive-*` Ordnern
- Unterstützt neue macOS Sequoia CloudStorage-Struktur
- Fallback auf Legacy-Pfade (`~/OneDrive`)

**Linux:**
- OneDrive ist optional (via rclone)
- Standard: `~/Documents`

## Entwickler-Hinweise

### Plattform-Check in Code

```python
from platform_config import is_windows, is_macos, is_linux

if is_windows():
    # Windows-spezifischer Code
    pass
elif is_macos():
    # macOS-spezifischer Code
    pass
else:
    # Linux-spezifischer Code
    pass
```

### Zugriff auf Plattform-Konfiguration

```python
from platform_config import PLATFORM

print(f"Plattform: {PLATFORM.platform_name}")
print(f"Standard-Quelle: {PLATFORM.default_src}")
print(f"Tesseract-Pfad: {PLATFORM.find_tesseract()}")
```

## Bekannte Einschränkungen

- **Linux:** OneDrive-Unterstützung erfordert manuelle Installation (z.B. via rclone)
- **macOS < 15:** Legacy OneDrive-Pfade werden unterstützt, aber neue CloudStorage-Struktur wird bevorzugt
- **Windows < 11:** Nicht getestet, sollte aber funktionieren (Windows 10 mit UTF-8 Support)

## Changelog

### Version 1.19.0 (2026-01-04)
- ✨ Plattformübergreifende Unterstützung (Windows 11, macOS 15+, Linux)
- ✨ Automatische Plattformerkennung und Pfad-Konfiguration
- ✨ Plattformspezifische OneDrive-Erkennung
- ✨ Plattformspezifische Tastatureingabe (msvcrt vs. select)
- ✨ Neue `platform_config.py` für zentrale Konfiguration
- 🔧 GUI-Kompatibilität für alle Plattformen
