import os
import pathlib
import requests
import pdfplumber
import docx
from pptx import Presentation
from openpyxl import load_workbook
import time
import json
from datetime import datetime
import select
import sys
import warnings

# Unterdrücke openpyxl Warnungen für nicht unterstützte Excel-Features
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

# Version und Metadaten
VERSION = "1.3.8"
VERSION_DATE = "2025-12-25"
SCRIPT_NAME = "FileInventory - OneDrive Dokumenten-Zusammenfassung (macOS)"

# macOS Pfade - expandiere ~ zum Home-Verzeichnis
SRC_ROOT = os.path.expanduser("~/OneDrive - Marc König Unternehmensberatung")
DST_ROOT = os.path.expanduser("~/LLM")

LMSTUDIO_API_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "local-model"  # in LM Studio unter Model-Name des laufenden Servers schauen

# Alternativ: Falls LM Studio auf einem anderen Port läuft:
# LMSTUDIO_API_URL = "http://localhost:8080/v1/chat/completions"
# oder prüfen Sie in LM Studio unter "Local Server" welcher Port verwendet wird

# Minimale Dateigröße für Bilddateien (in Bytes) - ignoriere kleine Icons
MIN_IMAGE_SIZE = 10 * 1024  # 10 KB

# Welche Dateitypen sollen verarbeitet werden?
EXTENSIONS = {
    ".pdf",                                    # PDF-Dokumente
    ".docx", ".doc",                          # Word-Dokumente (neu und alt)
    ".pptx", ".ppt",                          # PowerPoint-Präsentationen (neu und alt)
    ".xlsx", ".xls", ".xlsm", ".xltx",       # Excel-Dateien (neu, alt, Makro, Vorlagen)
    ".txt", ".md",                            # Textdateien
    ".png", ".jpg", ".jpeg"                   # Bilddateien
}

def extract_text_pdf(path):
    texts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            texts.append(page.extract_text() or "")
    return "\n\n".join(texts)

def extract_text_docx(path):
    """Extrahiert Text aus Word-Dokumenten (.docx)."""
    doc = docx.Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_text_doc(path):
    """
    Extrahiert Text aus alten Word-Dokumenten (.doc).
    Hinweis: .doc-Format wird nicht nativ unterstützt.
    Als Workaround wird versucht, mit python-docx zu öffnen (funktioniert manchmal).
    """
    try:
        # python-docx kann manchmal auch .doc öffnen (wenn es eigentlich .docx ist)
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception as e:
        # Fallback: Rückgabe mit Hinweis
        return f"[.doc-Datei - Textextraktion nicht vollständig möglich. Benötigt LibreOffice/antiword für vollständige Konvertierung]"

def extract_text_pptx(path):
    """Extrahiert Text aus PowerPoint-Dateien (.pptx)."""
    texts = []
    try:
        prs = Presentation(path)
        for slide_num, slide in enumerate(prs.slides, 1):
            slide_texts = []
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    slide_texts.append(shape.text)
            if slide_texts:
                texts.append(f"Folie {slide_num}:\n" + "\n".join(slide_texts))
        return "\n\n".join(texts)
    except Exception as e:
        print(f"Warnung bei PPTX-Extraktion: {e}")
        return ""

def extract_text_ppt(path):
    """
    Extrahiert Text aus alten PowerPoint-Dateien (.ppt).
    Hinweis: .ppt-Format wird nicht nativ unterstützt.
    Als Workaround wird versucht, mit python-pptx zu öffnen (funktioniert manchmal).
    """
    try:
        # python-pptx kann manchmal auch .ppt öffnen (wenn es eigentlich .pptx ist)
        prs = Presentation(path)
        texts = []
        for slide_num, slide in enumerate(prs.slides, 1):
            slide_texts = []
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    slide_texts.append(shape.text)
            if slide_texts:
                texts.append(f"Folie {slide_num}:\n" + "\n".join(slide_texts))
        return "\n\n".join(texts)
    except Exception as e:
        # Fallback: Rückgabe mit Hinweis
        return f"[.ppt-Datei - Textextraktion nicht vollständig möglich. Benötigt LibreOffice für vollständige Konvertierung]"

def extract_text_xlsx(path):
    """Extrahiert Text (keine Formeln) aus Excel-Dateien (.xlsx, .xlsm, .xltx)."""
    texts = []
    try:
        wb = load_workbook(path, data_only=True)  # data_only=True gibt Werte statt Formeln
        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            sheet_texts = []

            for row in sheet.iter_rows(values_only=True):
                # Filtere None-Werte und konvertiere zu String
                row_texts = [str(cell).strip() for cell in row if cell is not None and str(cell).strip()]
                if row_texts:
                    sheet_texts.append(" | ".join(row_texts))

            if sheet_texts:
                texts.append(f"Arbeitsblatt '{sheet_name}':\n" + "\n".join(sheet_texts))

        wb.close()
        return "\n\n".join(texts)
    except Exception as e:
        print(f"Warnung bei Excel-Extraktion: {e}")
        return ""

def extract_text_xls(path):
    """
    Extrahiert Text aus alten Excel-Dateien (.xls).
    Hinweis: .xls-Format wird von openpyxl nicht unterstützt.
    Benötigt xlrd-Bibliothek für vollständige Unterstützung.
    """
    try:
        # Versuche mit openpyxl (funktioniert nur wenn Datei fälschlicherweise .xls heißt)
        wb = load_workbook(path, data_only=True)
        texts = []
        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            sheet_texts = []
            for row in sheet.iter_rows(values_only=True):
                row_texts = [str(cell).strip() for cell in row if cell is not None and str(cell).strip()]
                if row_texts:
                    sheet_texts.append(" | ".join(row_texts))
            if sheet_texts:
                texts.append(f"Arbeitsblatt '{sheet_name}':\n" + "\n".join(sheet_texts))
        wb.close()
        return "\n\n".join(texts)
    except Exception as e:
        # Fallback: Rückgabe mit Hinweis
        return f"[.xls-Datei - Textextraktion nicht möglich. Benötigt xlrd-Bibliothek oder LibreOffice für Konvertierung]"

def extract_text_txt(path):
    """Extrahiert Text aus TXT-Dateien."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Fallback für andere Encodings
        try:
            with open(path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            print(f"Warnung bei TXT-Extraktion: {e}")
            return ""
    except Exception as e:
        print(f"Warnung bei TXT-Extraktion: {e}")
        return ""

def extract_text_md(path):
    """Extrahiert Text aus Markdown-Dateien."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            print(f"Warnung bei MD-Extraktion: {e}")
            return ""
    except Exception as e:
        print(f"Warnung bei MD-Extraktion: {e}")
        return ""

def extract_text_image(path):
    """Für Bilddateien wird ein Platzhalter zurückgegeben - das Bild wird per Vision API analysiert."""
    # Der eigentliche Text wird später vom LLM extrahiert, das die Bilddatei direkt analysiert
    return f"[IMAGE_FILE:{path}]"

def extract_text(path):
    ext = path.suffix.lower()
    if ext == ".pdf":
        return extract_text_pdf(path)
    elif ext == ".docx":
        return extract_text_docx(path)
    elif ext == ".doc":
        return extract_text_doc(path)
    elif ext == ".pptx":
        return extract_text_pptx(path)
    elif ext == ".ppt":
        return extract_text_ppt(path)
    elif ext in {".xlsx", ".xlsm", ".xltx"}:
        return extract_text_xlsx(path)
    elif ext == ".xls":
        return extract_text_xls(path)
    elif ext == ".txt":
        return extract_text_txt(path)
    elif ext == ".md":
        return extract_text_md(path)
    elif ext in {".png", ".jpg", ".jpeg"}:
        return extract_text_image(path)
    else:
        return ""

def is_file_accessible(file_path):
    """
    Prüft, ob eine Datei zugänglich ist.
    Auf macOS sind OneDrive-Dateien normalerweise direkt verfügbar.
    """
    try:
        return os.path.exists(file_path) and os.access(file_path, os.R_OK)
    except Exception as e:
        print(f"Warnung: Konnte Dateizugriff nicht prüfen für {file_path}: {e}")
        return False

def get_prompt_for_filetype(file_ext):
    """Gibt einen dateityp-spezifischen Prompt zurück."""
    prompts = {
        ".pdf": "Erstelle eine präzise Zusammenfassung dieses PDF-Dokuments in maximal 650 Zeichen als reinen Fließtext ohne Markdown-Formatierung. Bevorzuge die Nennung von Personennamen mit ihrem Kontext (Rolle, Funktion, Beziehung). Erfasse wichtigste Inhalte, Themen und Kernaussagen. Verwende keine Aufzählungszeichen, Sternchen, Hashtags oder andere Formatierungszeichen.",
        ".docx": "Erstelle eine präzise Zusammenfassung dieses Word-Dokuments in maximal 650 Zeichen als reinen Fließtext ohne Markdown-Formatierung. Bevorzuge die Nennung von Personennamen mit ihrem Kontext (Rolle, Funktion, Beziehung). Erfasse wichtigste Inhalte, Themen und Kernaussagen. Verwende keine Aufzählungszeichen, Sternchen, Hashtags oder andere Formatierungszeichen.",
        ".doc": "Erstelle eine präzise Zusammenfassung dieses Word-Dokuments in maximal 650 Zeichen als reinen Fließtext ohne Markdown-Formatierung. Bevorzuge die Nennung von Personennamen mit ihrem Kontext (Rolle, Funktion, Beziehung). Erfasse wichtigste Inhalte, Themen und Kernaussagen. Verwende keine Aufzählungszeichen, Sternchen, Hashtags oder andere Formatierungszeichen.",
        ".pptx": "Erstelle eine präzise Zusammenfassung dieser PowerPoint-Präsentation in maximal 650 Zeichen als reinen Fließtext ohne Markdown-Formatierung. Bevorzuge die Nennung von Personennamen mit ihrem Kontext (Rolle, Funktion). Erfasse Hauptthemen, wichtigste Folieninhalte und zentrale Botschaften. Verwende keine Aufzählungszeichen, Sternchen, Hashtags oder andere Formatierungszeichen.",
        ".ppt": "Erstelle eine präzise Zusammenfassung dieser PowerPoint-Präsentation in maximal 650 Zeichen als reinen Fließtext ohne Markdown-Formatierung. Bevorzuge die Nennung von Personennamen mit ihrem Kontext (Rolle, Funktion). Erfasse Hauptthemen, wichtigste Folieninhalte und zentrale Botschaften. Verwende keine Aufzählungszeichen, Sternchen, Hashtags oder andere Formatierungszeichen.",
        ".xlsx": "Erstelle eine präzise Zusammenfassung dieser Excel-Datei in maximal 650 Zeichen als reinen Fließtext ohne Markdown-Formatierung. Nenne relevante Personennamen falls vorhanden (mit Kontext). Beschreibe die Art der Daten, wichtige Kategorien und den Zweck der Tabelle. Verwende keine Aufzählungszeichen, Sternchen, Hashtags oder andere Formatierungszeichen.",
        ".xls": "Erstelle eine präzise Zusammenfassung dieser Excel-Datei in maximal 650 Zeichen als reinen Fließtext ohne Markdown-Formatierung. Nenne relevante Personennamen falls vorhanden (mit Kontext). Beschreibe die Art der Daten, wichtige Kategorien und den Zweck der Tabelle. Verwende keine Aufzählungszeichen, Sternchen, Hashtags oder andere Formatierungszeichen.",
        ".xlsm": "Erstelle eine präzise Zusammenfassung dieser Excel-Datei mit Makros in maximal 650 Zeichen als reinen Fließtext ohne Markdown-Formatierung. Nenne relevante Personennamen falls vorhanden (mit Kontext). Beschreibe die Art der Daten, wichtige Kategorien und den Zweck der Tabelle. Verwende keine Aufzählungszeichen, Sternchen, Hashtags oder andere Formatierungszeichen.",
        ".xltx": "Erstelle eine präzise Zusammenfassung dieser Excel-Vorlage in maximal 650 Zeichen als reinen Fließtext ohne Markdown-Formatierung. Nenne relevante Personennamen falls vorhanden (mit Kontext). Beschreibe die Art der Daten, wichtige Kategorien und den Zweck der Vorlage. Verwende keine Aufzählungszeichen, Sternchen, Hashtags oder andere Formatierungszeichen.",
        ".txt": "Erstelle eine präzise Zusammenfassung dieser Textdatei in maximal 650 Zeichen als reinen Fließtext ohne Markdown-Formatierung. Bevorzuge die Nennung von Personennamen mit ihrem Kontext (Rolle, Funktion, Beziehung). Erfasse wichtigste Informationen und den Zweck des Dokuments. Verwende keine Aufzählungszeichen, Sternchen, Hashtags oder andere Formatierungszeichen.",
        ".md": "Erstelle eine präzise Zusammenfassung dieses Markdown-Dokuments in maximal 650 Zeichen als reinen Fließtext ohne Markdown-Formatierung. Bevorzuge die Nennung von Personennamen mit ihrem Kontext. Erfasse Struktur, Hauptthemen und wichtigste Inhalte. Verwende keine Aufzählungszeichen, Sternchen, Hashtags oder andere Formatierungszeichen.",
        ".png": "Beschreibe dieses Bild in maximal 650 Zeichen als reinen Fließtext ohne Markdown-Formatierung. Nenne sichtbare Personennamen oder Personen mit ihrem Kontext. Erfasse was zu sehen ist, den Zweck des Bildes und wichtige Details wie Text, Diagramme oder Grafiken. Verwende keine Aufzählungszeichen, Sternchen, Hashtags oder andere Formatierungszeichen.",
        ".jpg": "Beschreibe dieses Foto/Bild in maximal 650 Zeichen als reinen Fließtext ohne Markdown-Formatierung. Nenne sichtbare Personennamen oder abgebildete Personen mit ihrem Kontext. Erfasse was zu sehen ist, den Kontext und wichtige visuelle Elemente. Verwende keine Aufzählungszeichen, Sternchen, Hashtags oder andere Formatierungszeichen.",
        ".jpeg": "Beschreibe dieses Foto/Bild in maximal 650 Zeichen als reinen Fließtext ohne Markdown-Formatierung. Nenne sichtbare Personennamen oder abgebildete Personen mit ihrem Kontext. Erfasse was zu sehen ist, den Kontext und wichtige visuelle Elemente. Verwende keine Aufzählungszeichen, Sternchen, Hashtags oder andere Formatierungszeichen."
    }
    return prompts.get(file_ext, "Erstelle eine präzise Zusammenfassung in maximal 650 Zeichen als reinen Fließtext ohne Markdown-Formatierung. Bevorzuge die Nennung von Personennamen mit ihrem Kontext. Verwende keine Aufzählungszeichen, Sternchen, Hashtags oder andere Formatierungszeichen.")

def summarize_image_with_lmstudio(image_path, file_ext):
    """Analysiert ein Bild mit der Vision API von LM Studio."""
    import base64

    try:
        # Lese Bild und konvertiere zu Base64
        with open(image_path, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')

        # Bestimme MIME-Type
        mime_type = "image/png" if file_ext.lower() == ".png" else "image/jpeg"

        # Hole dateityp-spezifischen Prompt
        user_prompt = get_prompt_for_filetype(file_ext)

        payload = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{img_data}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.3,
            "max_tokens": 250,
        }

        resp = requests.post(LMSTUDIO_API_URL, json=payload, timeout=300)
        resp.raise_for_status()

        data = resp.json()
        summary = data["choices"][0]["message"]["content"]

        # Keine Kürzung - lasse vollständige Antwort zu
        return summary

    except Exception as e:
        print(f"Fehler bei Bildanalyse: {e}")
        # Fallback: Gebe einen Platzhalter zurück
        return f"Bilddatei ({file_ext}). Vision-Analyse fehlgeschlagen: {str(e)[:100]}"

def summarize_with_lmstudio(text, file_path=None, file_ext=None, max_chars=30000):
    # Adaptive Textkürzung mit automatischem Retry bei Context-Overflow
    # ministral-3-14b-reasoning hat größeres Context-Fenster
    # Start mit ~30000 Zeichen (~7500 Tokens), bei Fehler schrittweise reduzieren

    # Stelle sicher, dass file_ext ein String ist
    if file_ext and not isinstance(file_ext, str):
        raise TypeError(f"file_ext muss ein String sein, nicht {type(file_ext)}")

    # Prüfe ob es sich um eine Bilddatei handelt
    is_image = file_ext and file_ext.lower() in {".png", ".jpg", ".jpeg"}

    if is_image and file_path:
        # Für Bilder: Verwende Vision API
        return summarize_image_with_lmstudio(file_path, file_ext)

    # Entferne problematische Zeichen und normalisiere Whitespace
    text = text.strip()
    if not text:
        raise ValueError("Text ist leer nach Bereinigung")

    # Versuche mit verschiedenen Textlängen, falls Context zu groß ist
    # Reasoning-Modelle können mehr Text verarbeiten
    retry_lengths = [30000, 20000, 14000, 10000, 6000, 3000]

    # Hole dateityp-spezifischen Prompt
    user_prompt = get_prompt_for_filetype(file_ext) if file_ext else "Erstelle eine präzise Zusammenfassung in maximal 650 Zeichen. Bevorzuge die Nennung von Personennamen mit ihrem Kontext."

    for attempt, current_max_chars in enumerate(retry_lengths, 1):
        truncated_text = text[:current_max_chars]

        payload = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "system",
                    "content": "Du bist ein präziser Assistent, der kompakte Zusammenfassungen von Dokumenten erstellt. Achte besonders auf Personennamen und deren Kontext. Gib NIEMALS Markdown-Formatierung aus. Schreibe ausschließlich in reinem Fließtext ohne Aufzählungszeichen, Sternchen, Hashtags oder andere Formatierungszeichen."
                },
                {
                    "role": "user",
                    "content": f"{user_prompt}\n\nDokument:\n{truncated_text}"
                },
            ],
            "temperature": 0.3,
            "max_tokens": 250,
        }

        try:
            resp = requests.post(LMSTUDIO_API_URL, json=payload, timeout=300)
            resp.raise_for_status()

            # Erfolg! Gib die Zusammenfassung zurück
            data = resp.json()
            summary = data["choices"][0]["message"]["content"]

            # Keine Kürzung - lasse vollständige Antwort vom Modell zu
            # Das Modell wurde instruiert, max 650 Zeichen zu verwenden

            if attempt > 1:
                print(f"  → Erfolgreich mit {current_max_chars} Zeichen (Versuch {attempt})")

            return summary

        except requests.exceptions.HTTPError as e:
            # Prüfe ob es ein Context-Overflow-Fehler ist
            try:
                error_data = resp.json()
                error_msg = str(error_data.get("error", ""))

                # Context-Overflow erkannt? Prüfe auf verschiedene Fehlermeldungen
                is_context_error = (
                    "context" in error_msg.lower() or
                    "token" in error_msg.lower() or
                    "length" in error_msg.lower()
                )

                if is_context_error:
                    if attempt < len(retry_lengths):
                        print(f"  → Context/Token-Fehler ({current_max_chars} Zeichen), versuche mit weniger...")
                        continue  # Nächster Versuch mit weniger Text
                    else:
                        print(f"  → Alle Retry-Versuche fehlgeschlagen")
                        raise ValueError(f"Text zu lang selbst nach {len(retry_lengths)} Versuchen: {error_msg}")
                else:
                    # Anderer HTTP-Fehler
                    print(f"HTTP-Fehler {resp.status_code}:")
                    print(f"Response-Text: {resp.text}")
                    raise
            except (ValueError, KeyError, json.JSONDecodeError):
                # Kein JSON oder kein error-Feld - könnte trotzdem Context-Fehler sein
                if resp.status_code == 400 and attempt < len(retry_lengths):
                    print(f"  → HTTP 400 Fehler ({current_max_chars} Zeichen), versuche mit weniger...")
                    continue
                else:
                    print(f"HTTP-Fehler {resp.status_code}:")
                    print(f"Response-Text: {resp.text}")
                    raise

    # Falls alle Versuche fehlschlagen
    raise ValueError("Zusammenfassung fehlgeschlagen nach allen Retry-Versuchen")

def process_file(src_file):
    rel_path = os.path.relpath(src_file, SRC_ROOT)
    dst_dir = os.path.join(DST_ROOT, os.path.dirname(rel_path))
    os.makedirs(dst_dir, exist_ok=True)

    # Summary-Datei neben die Quelle legen, aber unter D:\LLM
    dst_file = os.path.join(dst_dir, os.path.basename(src_file) + ".json")

    # Prüfe ob Datei existiert und valide ist
    if os.path.exists(dst_file):
        if validate_json_file(dst_file):
            print("Überspringe (valide Summary existiert):", dst_file)
            return
        else:
            print("Lösche fehlerhafte JSON-Datei:", dst_file)
            try:
                os.remove(dst_file)
            except Exception as e:
                print(f"Fehler beim Löschen von {dst_file}: {e}")
                return

    path_obj = pathlib.Path(src_file)
    print("Verarbeite:", src_file)

    # Prüfe ob Datei zugänglich ist
    if not is_file_accessible(src_file):
        print(f"Überspringe Datei, da nicht zugänglich: {src_file}")
        return

    # Für Bilddateien: Prüfe Mindestgröße (ignoriere kleine Icons)
    file_ext = path_obj.suffix.lower()
    if file_ext in {".png", ".jpg", ".jpeg"}:
        try:
            file_size = os.path.getsize(src_file)
            if file_size < MIN_IMAGE_SIZE:
                print(f"Überspringe kleine Bilddatei ({file_size} Bytes < {MIN_IMAGE_SIZE} Bytes): {src_file}")
                return
        except OSError as e:
            print(f"Fehler beim Prüfen der Dateigröße: {e}")
            return

    try:
        text = extract_text(path_obj)
    except Exception as e:
        print(f"Fehler beim Extrahieren von Text aus {src_file}: {e}")
        return

    # file_ext wurde bereits oben definiert (Zeile 425)
    is_image = file_ext in {".png", ".jpg", ".jpeg"}

    if not is_image and not text.strip():
        print("Kein Text extrahiert, überspringe:", src_file)
        return

    if not is_image:
        print(f"Text extrahiert: {len(text)} Zeichen")

    try:
        # Debug: Prüfe file_ext Typ
        if not isinstance(file_ext, str):
            print(f"FEHLER: file_ext hat falschen Typ: {type(file_ext)}, Wert: {file_ext}")
            return

        # Übergebe file_path und file_ext für dateityp-spezifische Verarbeitung
        summary = summarize_with_lmstudio(text, file_path=src_file, file_ext=file_ext)
    except ValueError as e:
        print(f"Validierungsfehler: {e}")
        return
    except TypeError as e:
        print(f"Typfehler: {e}")
        return
    except requests.exceptions.RequestException as e:
        print(f"Netzwerkfehler bei der Zusammenfassung: {e}")
        return

    # Sammle Datei-Metadaten
    stat = os.stat(src_file)

    metadata = {
        "name": os.path.basename(src_file),
        "path": rel_path,
        "ext": path_obj.suffix.lower(),
        "size": stat.st_size,
        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "chars": len(text),
        "summary": summary
    }

    with open(dst_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"Summary erfolgreich erstellt: {dst_file}")

def validate_json_file(json_path):
    """
    Validiert eine JSON-Ausgabedatei auf Korrektheit und sinnvollen Inhalt.

    Returns:
        True: Datei ist valide und kann übersprungen werden
        False: Datei ist fehlerhaft und muss neu erstellt werden
    """
    if not os.path.exists(json_path):
        return False

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Prüfe erforderliche Felder
        required_fields = ['name', 'path', 'ext', 'size', 'created', 'modified', 'chars', 'summary']
        for field in required_fields:
            if field not in data:
                print(f"Fehlende Struktur in {json_path}: Feld '{field}' fehlt")
                return False

        # Prüfe ob Summary sinnvoll ist (nicht leer, nicht nur Leerzeichen)
        summary = data.get('summary', '').strip()
        if not summary:
            print(f"Leere Summary in {json_path}")
            return False

        # Prüfe auf typische Fehlermarker
        error_indicators = [
            'error', 'fehler', 'failed', 'exception',
            'cannot', 'kann nicht', 'konnte nicht'
        ]
        summary_lower = summary.lower()
        if any(indicator in summary_lower for indicator in error_indicators):
            # Nur als Fehler werten, wenn die Summary sehr kurz ist (wahrscheinlich Fehlermeldung)
            if len(summary) < 50:
                print(f"Verdächtige Summary in {json_path}: {summary[:100]}")
                return False

        # Prüfe Mindestlänge der Summary
        if len(summary) < 20:
            print(f"Summary zu kurz in {json_path}: {summary}")
            return False

        # Datei scheint valide zu sein
        return True

    except json.JSONDecodeError as e:
        print(f"JSON-Fehler in {json_path}: {e}")
        return False
    except Exception as e:
        print(f"Fehler beim Validieren von {json_path}: {e}")
        return False

def check_user_input():
    """
    Prüft ob eine Taste gedrückt wurde (nicht-blockierend) - macOS Version.
    Returns True wenn eine Taste gedrückt wurde.
    """
    try:
        # Verwende select() für nicht-blockierende Eingabe auf macOS/Unix
        rlist, _, _ = select.select([sys.stdin], [], [], 0)
        if rlist:
            # Lese und verwerfe die Eingabe
            sys.stdin.readline()
            return True
        return False
    except Exception:
        # Falls select nicht funktioniert, gebe False zurück
        return False

def ask_continue():
    """
    Fragt den Benutzer höflich, ob er fortfahren möchte.
    Returns True wenn fortgesetzt werden soll, False zum Abbrechen.
    """
    print("\n" + "!" * 70)
    print("PAUSE - Eine Taste wurde gedrückt")
    print("!" * 70)
    print("\nMöchten Sie die Verarbeitung fortsetzen?")
    print("  [J] Ja, fortfahren")
    print("  [N] Nein, abbrechen und beenden")
    print("\nBitte wählen Sie (J/N): ", end="", flush=True)

    while True:
        choice = input().strip().lower()

        if choice == 'j':
            print("\nVerarbeitung wird fortgesetzt...\n")
            return True
        elif choice == 'n':
            print("\nVerarbeitung wird abgebrochen. Vielen Dank!\n")
            return False
        else:
            print("Ungültige Eingabe. Bitte J oder N eingeben: ", end="", flush=True)

def check_lmstudio_connection():
    """
    Prüft ob LM Studio läuft und erreichbar ist.
    Returns True wenn verbunden, False sonst.
    """
    try:
        # Versuche eine einfache Anfrage an den Health-Endpoint
        health_url = LMSTUDIO_API_URL.replace('/v1/chat/completions', '/v1/models')
        response = requests.get(health_url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def format_time(seconds):
    """Formatiert Sekunden in h:mm:ss Format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours}h {minutes:02d}m {secs:02d}s"
    elif minutes > 0:
        return f"{minutes}m {secs:02d}s"
    else:
        return f"{secs}s"

def walk_and_process():
    # Zeige Version und Startinformationen
    print("=" * 70)
    print(f"{SCRIPT_NAME}")
    print(f"Version {VERSION} vom {VERSION_DATE}")
    print("=" * 70)
    print(f"Quellverzeichnis: {SRC_ROOT}")
    print(f"Zielverzeichnis:  {DST_ROOT}")
    print(f"Dateitypen:       {', '.join(EXTENSIONS)}")
    print("=" * 70)

    # Prüfe LM Studio Verbindung
    print("\nPrüfe LM Studio Verbindung...")
    if not check_lmstudio_connection():
        print("\n" + "!" * 70)
        print("FEHLER: LM Studio ist nicht erreichbar!")
        print("!" * 70)
        print(f"\nBitte stellen Sie sicher, dass:")
        print(f"  1. LM Studio gestartet ist")
        print(f"  2. Ein Modell geladen ist")
        print(f"  3. Der Local Server läuft")
        print(f"  4. Die URL korrekt ist: {LMSTUDIO_API_URL}")
        print("\nProgramm wird beendet.")
        print("=" * 70)
        return
    print("✓ LM Studio verbunden")

    # Zähle zunächst alle zu verarbeitenden Dateien mit Fortschrittsanzeige
    print("\nScanne Verzeichnis...")
    all_files = []
    dir_count = 0
    file_count = 0
    last_line_length = 0  # Tracke die Länge der letzten Zeile
    file_stats = {}  # Statistik: {extension: {'count': n, 'size': bytes, 'files': [paths]}}

    # Nutze os.walk und zeige Fortschritt mit \r (carriage return)
    for root, dirs, files in os.walk(SRC_ROOT):
        dir_count += 1

        # Zähle relevante Dateien in diesem Verzeichnis
        relevant_files = 0
        for name in files:
            file_count += 1
            ext = os.path.splitext(name)[1].lower()
            full_path = os.path.join(root, name)

            # Sammle Statistiken für alle Dateien
            try:
                file_size = os.path.getsize(full_path)
                if ext not in file_stats:
                    file_stats[ext] = {'count': 0, 'size': 0, 'files': []}
                file_stats[ext]['count'] += 1
                file_stats[ext]['size'] += file_size
                file_stats[ext]['files'].append(full_path)
            except (OSError, PermissionError):
                # Überspringe Dateien, auf die nicht zugegriffen werden kann
                pass

            if ext in EXTENSIONS:
                all_files.append(full_path)
                relevant_files += 1

        # Zeige Fortschritt (überschreibe vorherige Zeile mit \r)
        if dir_count % 10 == 0 or relevant_files > 0:
            rel_path = os.path.relpath(root, SRC_ROOT)
            if len(rel_path) > 50:
                rel_path = "..." + rel_path[-47:]

            # Erstelle die Ausgabezeile
            line = f"  Verzeichnisse: {dir_count:,} | Dateien gescannt: {file_count:,} | Relevante Dateien: {len(all_files):,} | {rel_path}"

            # Füge Leerzeichen hinzu, um alte längere Zeilen vollständig zu überschreiben
            if len(line) < last_line_length:
                line = line + " " * (last_line_length - len(line))

            # Merke die aktuelle Zeilenlänge für das nächste Update
            last_line_length = len(line)

            # Schreibe mit \r am Anfang (Cursor an Zeilenanfang) ohne Zeilenumbruch
            sys.stdout.write(f"\r{line}")
            sys.stdout.flush()

    # Finaler Status mit Zeilenumbruch
    final_line = f"  Verzeichnisse: {dir_count:,} | Dateien gescannt: {file_count:,} | Relevante Dateien: {len(all_files):,}"
    if len(final_line) < last_line_length:
        final_line = final_line + " " * (last_line_length - len(final_line))
    sys.stdout.write(f"\r{final_line}\n")
    sys.stdout.flush()

    # Zeige Statistik nach Dateiendungen
    print("\n" + "=" * 70)
    print("STATISTIK DER DATEIENDUNGEN")
    print("=" * 70)
    print(f"{'Endung':<10} {'Anzahl':>8} {'Größe (MB)':>12} {'Ø Größe (KB)':>14}  {'Status':<15}")
    print("-" * 70)

    # Sortiere nach Anzahl der Dateien (absteigend)
    sorted_stats = sorted(file_stats.items(), key=lambda x: x[1]['count'], reverse=True)

    for ext, stats in sorted_stats:
        count = stats['count']
        total_size_mb = stats['size'] / (1024 * 1024)
        avg_size_kb = (stats['size'] / count) / 1024 if count > 0 else 0

        # Markiere ob dieser Typ analysiert wird
        ext_display = ext if ext else "(keine)"
        will_analyze = "→ WIRD ANALYSIERT" if ext in EXTENSIONS else ""

        print(f"{ext_display:<10} {count:>8,} {total_size_mb:>12.2f} {avg_size_kb:>14.2f}  {will_analyze:<15}")

    print("=" * 70)

    total_files = len(all_files)
    print(f"\nGefunden: {total_files} Dateien zum Verarbeiten")
    print("\nHinweis: Drücken Sie Enter während der Verarbeitung,")
    print("         um anzuhalten und zu wählen, ob Sie fortfahren möchten.")
    print("=" * 70)

    if total_files == 0:
        print("Keine Dateien gefunden.")
        return

    # Verarbeite Dateien mit Fortschrittsanzeige
    processed = 0
    skipped = 0
    errors = 0
    recreated = 0
    start_time = time.time()

    for idx, full_path in enumerate(all_files, 1):
        # Prüfe auf Tasteneingabe
        if check_user_input():
            if not ask_continue():
                print("\n" + "=" * 70)
                print("VERARBEITUNG VOM BENUTZER ABGEBROCHEN")
                print("=" * 70)
                print(f"Verarbeitet bis Datei {idx}/{total_files}")
                print(f"Neu verarbeitet: {processed}")
                print(f"Neu erstellt (vorher fehlerhaft): {recreated}")
                print(f"Übersprungen (valide): {skipped}")
                print(f"Fehler: {errors}")
                elapsed = time.time() - start_time
                print(f"Laufzeit bis Abbruch: {format_time(elapsed)}")
                print("=" * 70)
                return

        try:
            # Prüfe ob bereits existiert und valide ist
            rel_path = os.path.relpath(full_path, SRC_ROOT)
            dst_dir = os.path.join(DST_ROOT, os.path.dirname(rel_path))
            dst_file = os.path.join(dst_dir, os.path.basename(full_path) + ".json")

            if os.path.exists(dst_file):
                if validate_json_file(dst_file):
                    skipped += 1
                else:
                    # Fehlerhafte Datei wird in process_file gelöscht und neu erstellt
                    process_file(full_path)
                    recreated += 1
            else:
                process_file(full_path)
                processed += 1

            # Berechne Zeitschätzung
            elapsed = time.time() - start_time
            if idx > 0:
                avg_time_per_file = elapsed / idx
                remaining_files = total_files - idx
                estimated_remaining = avg_time_per_file * remaining_files

                print(f"\n[{idx}/{total_files}] Fortschritt: {(idx/total_files)*100:.1f}%")
                print(f"Neu: {processed} | Neu erstellt: {recreated} | Übersprungen: {skipped} | Fehler: {errors}")
                print(f"Verstrichene Zeit: {format_time(elapsed)}")
                print(f"Geschätzte Restzeit: {format_time(estimated_remaining)}")
                print(f"Geschätzte Gesamtzeit: {format_time(elapsed + estimated_remaining)}")
                print(f"Durchschnitt: {avg_time_per_file:.2f}s pro Datei")
                print("=" * 70)

        except Exception as e:
            errors += 1
            print("Fehler bei", full_path, "->", e)

    # Abschlussbericht
    total_time = time.time() - start_time
    print("\n" + "=" * 70)
    print("VERARBEITUNG ABGESCHLOSSEN")
    print("=" * 70)
    print(f"Gesamt: {total_files} Dateien")
    print(f"Neu verarbeitet: {processed}")
    print(f"Neu erstellt (vorher fehlerhaft): {recreated}")
    print(f"Übersprungen (valide): {skipped}")
    print(f"Fehler: {errors}")
    print(f"Gesamtzeit: {format_time(total_time)}")
    if processed > 0:
        print(f"Durchschnitt: {total_time/total_files:.2f}s pro Datei")
    print("=" * 70)

if __name__ == "__main__":
    walk_and_process()
