#!/usr/bin/env python3
"""
FileInventory GUI Lite - Kompatible Version für ältere macOS-Versionen
=======================================================================

Verwendet Standard Tkinter statt CustomTkinter
Kompatibel mit macOS 10.13+ (High Sierra)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import threading
import queue
from datetime import datetime
from pathlib import Path

# Importiere FileInventory-Funktionen
from FileInventory import (
    VERSION, VERSION_DATE, SRC_ROOT, DST_ROOT,
    EXTENSIONS, EXCLUDE_PATTERNS
)


class FileInventoryAppLite(tk.Tk):
    """Hauptanwendung für FileInventory GUI (Lite Version)"""

    def __init__(self):
        super().__init__()

        # Fenster-Konfiguration
        self.title(f"FileInventory v{VERSION} - Dokumenten-Analyse")
        self.geometry("1200x800")
        self.minsize(900, 600)

        # Setze macOS-spezifisches Aussehen
        if sys.platform == "darwin":
            # Verwende Aqua-Style
            self.tk.call('tk', 'scaling', 2.0)

        # Style konfigurieren
        self.style = ttk.Style()
        self.style.theme_use('aqua' if sys.platform == 'darwin' else 'clam')

        # Queue für Thread-Kommunikation
        self.message_queue = queue.Queue()
        self.processing = False

        # Pfade
        self.src_path = tk.StringVar(value=SRC_ROOT)
        self.dst_path = tk.StringVar(value=DST_ROOT)

        # Statistiken
        self.stats = {
            'total_files': 0,
            'processed': 0,
            'skipped': 0,
            'errors': 0
        }

        # UI erstellen
        self._create_ui()

        # Queue-Überwachung starten
        self.after(100, self._check_queue)

    def _create_ui(self):
        """Erstellt die Benutzeroberfläche"""

        # Hauptcontainer mit Padding
        main_container = ttk.Frame(self, padding="10")
        main_container.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_container.grid_rowconfigure(3, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        # Header
        self._create_header(main_container)

        # Pfad-Sektion
        self._create_path_section(main_container)

        # Optionen
        self._create_options_section(main_container)

        # Log-Bereich
        self._create_log_section(main_container)

        # Footer
        self._create_footer(main_container)

    def _create_header(self, parent):
        """Erstellt den Header"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        title = ttk.Label(
            header_frame,
            text="📁 FileInventory - Dokumenten-Analyse",
            font=('Helvetica', 20, 'bold')
        )
        title.pack(anchor="w")

        subtitle = ttk.Label(
            header_frame,
            text=f"Version {VERSION} ({VERSION_DATE}) - KI-gestützte Dokumenten-Zusammenfassung",
            foreground='gray'
        )
        subtitle.pack(anchor="w")

    def _create_path_section(self, parent):
        """Erstellt die Pfad-Konfiguration"""
        path_frame = ttk.LabelFrame(parent, text="Verzeichnisse", padding="10")
        path_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        path_frame.grid_columnconfigure(1, weight=1)

        # Quellpfad
        ttk.Label(path_frame, text="Quellverzeichnis:").grid(
            row=0, column=0, sticky="w", padx=(0, 10), pady=5
        )
        ttk.Entry(path_frame, textvariable=self.src_path).grid(
            row=0, column=1, sticky="ew", padx=(0, 10), pady=5
        )
        ttk.Button(
            path_frame,
            text="Durchsuchen",
            command=lambda: self._browse_folder(self.src_path)
        ).grid(row=0, column=2, pady=5)

        # Zielpfad
        ttk.Label(path_frame, text="Ausgabeverzeichnis:").grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=5
        )
        ttk.Entry(path_frame, textvariable=self.dst_path).grid(
            row=1, column=1, sticky="ew", padx=(0, 10), pady=5
        )
        ttk.Button(
            path_frame,
            text="Durchsuchen",
            command=lambda: self._browse_folder(self.dst_path)
        ).grid(row=1, column=2, pady=5)

    def _create_options_section(self, parent):
        """Erstellt den Optionen-Bereich"""
        options_frame = ttk.LabelFrame(parent, text="Optionen", padding="10")
        options_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        self.update_dsgvo = tk.BooleanVar(value=True)
        self.skip_existing = tk.BooleanVar(value=True)
        self.create_database = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            options_frame,
            text="DSGVO-Klassifizierung durchführen",
            variable=self.update_dsgvo
        ).grid(row=0, column=0, sticky="w", padx=10)

        ttk.Checkbutton(
            options_frame,
            text="Existierende Dateien überspringen",
            variable=self.skip_existing
        ).grid(row=0, column=1, sticky="w", padx=10)

        ttk.Checkbutton(
            options_frame,
            text="Kombinierte Datenbank erstellen",
            variable=self.create_database
        ).grid(row=0, column=2, sticky="w", padx=10)

    def _create_log_section(self, parent):
        """Erstellt den Log-Bereich"""
        log_frame = ttk.LabelFrame(parent, text="Verarbeitungslog", padding="10")
        log_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 10))
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        # Textbereich mit Scrollbar
        text_scroll = ttk.Scrollbar(log_frame)
        text_scroll.grid(row=0, column=1, sticky="ns")

        self.log_text = tk.Text(
            log_frame,
            wrap="word",
            yscrollcommand=text_scroll.set,
            font=('Monaco', 10) if sys.platform == 'darwin' else ('Courier', 10),
            bg='#1e1e1e',
            fg='#ffffff',
            insertbackground='white'
        )
        self.log_text.grid(row=0, column=0, sticky="nsew")
        text_scroll.config(command=self.log_text.yview)

        # Button-Leiste
        button_bar = ttk.Frame(log_frame)
        button_bar.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5, 0))

        ttk.Button(
            button_bar,
            text="Log löschen",
            command=self._clear_log
        ).pack(side="right")

    def _create_footer(self, parent):
        """Erstellt den Footer"""
        footer_frame = ttk.Frame(parent)
        footer_frame.grid(row=4, column=0, sticky="ew")
        footer_frame.grid_columnconfigure(1, weight=1)

        # Buttons
        button_frame = ttk.Frame(footer_frame)
        button_frame.grid(row=0, column=0, sticky="w")

        self.start_button = ttk.Button(
            button_frame,
            text="▶ Verarbeitung starten",
            command=self._start_processing
        )
        self.start_button.pack(side="left", padx=(0, 10))

        self.stop_button = ttk.Button(
            button_frame,
            text="■ Stoppen",
            command=self._stop_processing,
            state="disabled"
        )
        self.stop_button.pack(side="left")

        # Statistik
        self.stats_label = ttk.Label(footer_frame, text="Bereit")
        self.stats_label.grid(row=0, column=1, sticky="e")

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            footer_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5, 0))

    def _browse_folder(self, path_var):
        """Öffnet Folder-Browser"""
        folder = filedialog.askdirectory(
            initialdir=path_var.get(),
            title="Verzeichnis auswählen"
        )
        if folder:
            path_var.set(folder)

    def _clear_log(self):
        """Löscht den Log"""
        self.log_text.delete("1.0", "end")

    def _log(self, message, level="INFO"):
        """Fügt eine Nachricht zum Log hinzu"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {message}\n"
        self.log_text.insert("end", formatted)
        self.log_text.see("end")

    def _update_stats(self):
        """Aktualisiert die Statistik"""
        stats_text = (
            f"Gesamt: {self.stats['total_files']} | "
            f"Verarbeitet: {self.stats['processed']} | "
            f"Übersprungen: {self.stats['skipped']} | "
            f"Fehler: {self.stats['errors']}"
        )
        self.stats_label.config(text=stats_text)

        if self.stats['total_files'] > 0:
            progress = (self.stats['processed'] / self.stats['total_files']) * 100
            self.progress_var.set(progress)

    def _start_processing(self):
        """Startet die Verarbeitung"""
        src = self.src_path.get()
        dst = self.dst_path.get()

        if not os.path.exists(src):
            messagebox.showerror("Fehler", f"Quellverzeichnis existiert nicht:\n{src}")
            return

        self.processing = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.progress_var.set(0)

        self.stats = {'total_files': 0, 'processed': 0, 'skipped': 0, 'errors': 0}

        self._log("=== Verarbeitung gestartet ===")
        self._log(f"Quelle: {src}")
        self._log(f"Ziel: {dst}")

        # Starte Worker
        worker = threading.Thread(target=self._processing_worker, daemon=True)
        worker.start()

    def _stop_processing(self):
        """Stoppt die Verarbeitung"""
        self.processing = False
        self._log("Verarbeitung wird gestoppt...")

    def _processing_worker(self):
        """Worker-Thread"""
        try:
            src = self.src_path.get()

            # Sammle Dateien
            self.message_queue.put(("log", "Sammle Dateien..."))

            all_files = []
            for root, dirs, files in os.walk(src):
                skip = False
                for pattern in EXCLUDE_PATTERNS:
                    if Path(root).match(pattern):
                        skip = True
                        break
                if skip:
                    continue

                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in EXTENSIONS:
                        all_files.append(os.path.join(root, file))

            self.stats['total_files'] = len(all_files)
            self.message_queue.put(("stats", None))
            self.message_queue.put(("log", f"Gefunden: {len(all_files)} Dateien"))

            # Hinweis: Vollständige Integration folgt
            self.message_queue.put(("log", "Demo-Modus: Keine echte Verarbeitung"))

            for idx, file_path in enumerate(all_files[:10], 1):  # Demo: nur 10 Dateien
                if not self.processing:
                    break
                self.message_queue.put(("log", f"[{idx}/10] {os.path.basename(file_path)}"))
                self.stats['processed'] += 1
                self.message_queue.put(("stats", None))
                import time
                time.sleep(0.1)

            self.message_queue.put(("log", "=== Verarbeitung abgeschlossen ==="))

        except Exception as e:
            self.message_queue.put(("log", f"Fehler: {str(e)}"))
        finally:
            self.message_queue.put(("done", None))

    def _check_queue(self):
        """Prüft Message-Queue"""
        try:
            while True:
                msg_type, msg = self.message_queue.get_nowait()

                if msg_type == "log":
                    self._log(msg)
                elif msg_type == "stats":
                    self._update_stats()
                elif msg_type == "done":
                    self._processing_complete()

        except queue.Empty:
            pass

        self.after(100, self._check_queue)

    def _processing_complete(self):
        """Verarbeitung abgeschlossen"""
        self.processing = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.progress_var.set(100)


def main():
    """Haupteinstiegspunkt"""
    app = FileInventoryAppLite()
    app.mainloop()


if __name__ == "__main__":
    main()
