#!/usr/bin/env python3
"""
FileInventory GUI - Moderne grafische Oberfläche
================================================

Plattform: macOS (primär), Windows 11 (kompatibel)
Framework: CustomTkinter für modernes Design
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import threading
import queue
from datetime import datetime
from pathlib import Path

# Importiere FileInventory-Funktionen
from FileInventory import (
    VERSION, VERSION_DATE, SRC_ROOT, DST_ROOT,
    process_file, update_all_jsons_with_dsgvo,
    EXTENSIONS, EXCLUDE_PATTERNS
)

# CustomTkinter Konfiguration
ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"


class FileInventoryApp(ctk.CTk):
    """Hauptanwendung für FileInventory GUI"""

    def __init__(self):
        super().__init__()

        # Fenster-Konfiguration
        self.title(f"FileInventory v{VERSION} - Dokumenten-Analyse")
        self.geometry("1200x800")

        # macOS-spezifische Einstellungen
        if sys.platform == "darwin":
            # Setze macOS App-Icon (optional)
            # self.iconbitmap("app_icon.icns")
            pass

        # Queue für Thread-Kommunikation
        self.message_queue = queue.Queue()
        self.processing = False

        # Pfade
        self.src_path = ctk.StringVar(value=SRC_ROOT)
        self.dst_path = ctk.StringVar(value=DST_ROOT)

        # Statistiken
        self.stats = {
            'total_files': 0,
            'processed': 0,
            'skipped': 0,
            'errors': 0,
            'current_file': ''
        }

        # UI erstellen
        self._create_ui()

        # Queue-Überwachung starten
        self.after(100, self._check_queue)

    def _create_ui(self):
        """Erstellt die Benutzeroberfläche"""

        # Grid-Layout konfigurieren
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ========== HEADER ==========
        self._create_header()

        # ========== MAIN CONTENT ==========
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Pfad-Konfiguration
        self._create_path_section()

        # Optionen
        self._create_options_section()

        # Log-Bereich
        self._create_log_section()

        # ========== FOOTER (Buttons & Progress) ==========
        self._create_footer()

    def _create_header(self):
        """Erstellt den Header-Bereich"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1)

        # Icon/Logo (placeholder)
        icon_label = ctk.CTkLabel(
            header_frame,
            text="📁",
            font=ctk.CTkFont(size=40)
        )
        icon_label.grid(row=0, column=0, padx=(0, 15))

        # Titel und Info
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=1, sticky="w")

        title = ctk.CTkLabel(
            title_frame,
            text="FileInventory - Dokumenten-Analyse",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            title_frame,
            text=f"Version {VERSION} ({VERSION_DATE}) - KI-gestützte Dokumenten-Zusammenfassung",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle.pack(anchor="w")

    def _create_path_section(self):
        """Erstellt die Pfad-Konfiguration"""
        path_frame = ctk.CTkFrame(self.main_frame)
        path_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        path_frame.grid_columnconfigure(1, weight=1)

        # Quellpfad
        ctk.CTkLabel(
            path_frame,
            text="Quellverzeichnis:",
            font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        src_entry = ctk.CTkEntry(
            path_frame,
            textvariable=self.src_path,
            height=35
        )
        src_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkButton(
            path_frame,
            text="Durchsuchen",
            width=120,
            command=lambda: self._browse_folder(self.src_path)
        ).grid(row=0, column=2, padx=10, pady=10)

        # Zielpfad
        ctk.CTkLabel(
            path_frame,
            text="Ausgabeverzeichnis:",
            font=ctk.CTkFont(weight="bold")
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")

        dst_entry = ctk.CTkEntry(
            path_frame,
            textvariable=self.dst_path,
            height=35
        )
        dst_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkButton(
            path_frame,
            text="Durchsuchen",
            width=120,
            command=lambda: self._browse_folder(self.dst_path)
        ).grid(row=1, column=2, padx=10, pady=10)

    def _create_options_section(self):
        """Erstellt den Optionen-Bereich"""
        options_frame = ctk.CTkFrame(self.main_frame)
        options_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

        ctk.CTkLabel(
            options_frame,
            text="Optionen",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 5), sticky="w")

        # Checkboxes
        self.update_dsgvo = ctk.BooleanVar(value=True)
        self.skip_existing = ctk.BooleanVar(value=True)
        self.create_database = ctk.BooleanVar(value=False)

        ctk.CTkCheckBox(
            options_frame,
            text="DSGVO-Klassifizierung durchführen",
            variable=self.update_dsgvo
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")

        ctk.CTkCheckBox(
            options_frame,
            text="Existierende Dateien überspringen",
            variable=self.skip_existing
        ).grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkCheckBox(
            options_frame,
            text="Kombinierte Datenbank erstellen",
            variable=self.create_database
        ).grid(row=1, column=2, padx=10, pady=5, sticky="w")

    def _create_log_section(self):
        """Erstellt den Log-Bereich"""
        log_frame = ctk.CTkFrame(self.main_frame)
        log_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        log_frame.grid_rowconfigure(1, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(log_frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            header,
            text="Verarbeitungslog",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            header,
            text="Log löschen",
            width=100,
            command=self._clear_log
        ).grid(row=0, column=1, sticky="e")

        # Textbereich mit Scrollbar
        self.log_text = ctk.CTkTextbox(
            log_frame,
            wrap="word",
            font=ctk.CTkFont(family="Monaco, Courier New", size=11)
        )
        self.log_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

    def _create_footer(self):
        """Erstellt den Footer mit Buttons und Progress"""
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        footer_frame.grid_columnconfigure(1, weight=1)

        # Buttons
        button_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        button_frame.grid(row=0, column=0, sticky="w")

        self.start_button = ctk.CTkButton(
            button_frame,
            text="▶ Verarbeitung starten",
            width=180,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="green",
            hover_color="darkgreen",
            command=self._start_processing
        )
        self.start_button.pack(side="left", padx=(0, 10))

        self.stop_button = ctk.CTkButton(
            button_frame,
            text="■ Stoppen",
            width=120,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="red",
            hover_color="darkred",
            state="disabled",
            command=self._stop_processing
        )
        self.stop_button.pack(side="left", padx=(0, 10))

        # Statistik
        self.stats_label = ctk.CTkLabel(
            footer_frame,
            text="Bereit",
            font=ctk.CTkFont(size=12)
        )
        self.stats_label.grid(row=0, column=1, padx=20, sticky="e")

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(footer_frame)
        self.progress_bar.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="ew")
        self.progress_bar.set(0)

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
        color_map = {
            "INFO": "white",
            "SUCCESS": "green",
            "WARNING": "orange",
            "ERROR": "red"
        }

        # Füge zum Textfeld hinzu
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")

        # Optional: Färbe letzte Zeile
        # (CustomTkinter Textbox unterstützt tags)

    def _update_stats(self):
        """Aktualisiert die Statistik-Anzeige"""
        stats_text = (
            f"Gesamt: {self.stats['total_files']} | "
            f"Verarbeitet: {self.stats['processed']} | "
            f"Übersprungen: {self.stats['skipped']} | "
            f"Fehler: {self.stats['errors']}"
        )
        self.stats_label.configure(text=stats_text)

        if self.stats['total_files'] > 0:
            progress = self.stats['processed'] / self.stats['total_files']
            self.progress_bar.set(progress)

    def _start_processing(self):
        """Startet die Verarbeitung in einem Thread"""
        # Validiere Pfade
        src = self.src_path.get()
        dst = self.dst_path.get()

        if not os.path.exists(src):
            messagebox.showerror("Fehler", f"Quellverzeichnis existiert nicht:\n{src}")
            return

        if not dst:
            messagebox.showerror("Fehler", "Bitte Ausgabeverzeichnis angeben")
            return

        # UI aktualisieren
        self.processing = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.progress_bar.set(0)

        # Stats zurücksetzen
        self.stats = {
            'total_files': 0,
            'processed': 0,
            'skipped': 0,
            'errors': 0,
            'current_file': ''
        }

        self._log("=== Verarbeitung gestartet ===", "INFO")
        self._log(f"Quelle: {src}", "INFO")
        self._log(f"Ziel: {dst}", "INFO")

        # Starte Worker-Thread
        worker = threading.Thread(target=self._processing_worker, daemon=True)
        worker.start()

    def _stop_processing(self):
        """Stoppt die Verarbeitung"""
        self.processing = False
        self._log("Verarbeitung wird gestoppt...", "WARNING")

    def _processing_worker(self):
        """Worker-Thread für die Verarbeitung"""
        try:
            src = self.src_path.get()
            dst = self.dst_path.get()

            # Sammle alle Dateien
            self.message_queue.put(("log", "Sammle Dateien...", "INFO"))

            all_files = []
            for root, dirs, files in os.walk(src):
                # Prüfe Exclude-Patterns
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

            total = len(all_files)
            self.stats['total_files'] = total
            self.message_queue.put(("stats", None, None))
            self.message_queue.put(("log", f"Gefunden: {total} Dateien", "SUCCESS"))

            # Verarbeite Dateien
            for idx, file_path in enumerate(all_files, 1):
                if not self.processing:
                    break

                try:
                    self.stats['current_file'] = os.path.basename(file_path)
                    self.message_queue.put(("log", f"[{idx}/{total}] {self.stats['current_file']}", "INFO"))

                    # Hier würde die eigentliche Verarbeitung stattfinden
                    # process_file(file_path) - muss angepasst werden für Queue-Kommunikation

                    self.stats['processed'] += 1

                except Exception as e:
                    self.stats['errors'] += 1
                    self.message_queue.put(("log", f"Fehler: {str(e)}", "ERROR"))

                finally:
                    self.message_queue.put(("stats", None, None))

            # DSGVO-Update (optional)
            if self.update_dsgvo.get() and self.processing:
                self.message_queue.put(("log", "Führe DSGVO-Klassifizierung durch...", "INFO"))
                # update_all_jsons_with_dsgvo() - muss angepasst werden

            self.message_queue.put(("log", "=== Verarbeitung abgeschlossen ===", "SUCCESS"))

        except Exception as e:
            self.message_queue.put(("log", f"Kritischer Fehler: {str(e)}", "ERROR"))

        finally:
            self.message_queue.put(("done", None, None))

    def _check_queue(self):
        """Prüft die Message-Queue und aktualisiert UI"""
        try:
            while True:
                msg_type, msg, level = self.message_queue.get_nowait()

                if msg_type == "log":
                    self._log(msg, level)
                elif msg_type == "stats":
                    self._update_stats()
                elif msg_type == "done":
                    self._processing_complete()

        except queue.Empty:
            pass

        # Schedule nächste Prüfung
        if self.processing:
            self.after(100, self._check_queue)
        else:
            self.after(500, self._check_queue)

    def _processing_complete(self):
        """Wird aufgerufen wenn Verarbeitung beendet ist"""
        self.processing = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.progress_bar.set(1.0)


def main():
    """Haupteinstiegspunkt"""
    app = FileInventoryApp()
    app.mainloop()


if __name__ == "__main__":
    main()
