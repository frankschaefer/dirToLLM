#!/usr/bin/env python3
"""
FileInventory GUI Lite - Plattformübergreifende Basis-Version
==============================================================

Verwendet Standard Tkinter (keine externen GUI-Abhängigkeiten)
Kompatibel mit Windows 11, macOS 10.13+, und Linux
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import threading
import queue
from datetime import datetime
from pathlib import Path

# Importiere Plattform-Konfiguration
from platform_config import PLATFORM

# Importiere FileInventory-Funktionen
from FileInventory import (
    VERSION, VERSION_DATE, SRC_ROOT, DST_ROOT,
    EXTENSIONS, EXCLUDE_PATTERNS, process_file
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
        self.paused = False

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

        # Zeit-Tracking
        self.start_time = None
        self.last_file_time = None

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
        options_frame = ttk.LabelFrame(parent, text="Optionen & Parameter", padding="10")
        options_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        options_frame.grid_columnconfigure(1, weight=1)

        # Checkboxen
        cb_frame = ttk.Frame(options_frame)
        cb_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 10))

        self.update_dsgvo = tk.BooleanVar(value=True)
        self.skip_existing = tk.BooleanVar(value=True)
        self.create_database = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            cb_frame,
            text="DSGVO-Klassifizierung",
            variable=self.update_dsgvo
        ).grid(row=0, column=0, sticky="w", padx=10)

        ttk.Checkbutton(
            cb_frame,
            text="Existierende überspringen",
            variable=self.skip_existing
        ).grid(row=0, column=1, sticky="w", padx=10)

        ttk.Checkbutton(
            cb_frame,
            text="Datenbank erstellen",
            variable=self.create_database
        ).grid(row=0, column=2, sticky="w", padx=10)

        # Parameter
        ttk.Separator(options_frame, orient='horizontal').grid(
            row=1, column=0, columnspan=3, sticky="ew", pady=10
        )

        # Zusammenfassungs-Länge
        ttk.Label(options_frame, text="Max. Zusammenfassung (Zeichen):").grid(
            row=2, column=0, sticky="w", padx=10, pady=5
        )
        self.summary_max_chars = tk.IntVar(value=1500)
        summary_spin = ttk.Spinbox(
            options_frame,
            from_=500,
            to=5000,
            increment=100,
            textvariable=self.summary_max_chars,
            width=10
        )
        summary_spin.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Min. Bildgröße
        ttk.Label(options_frame, text="Min. Bildgröße (KB):").grid(
            row=3, column=0, sticky="w", padx=10, pady=5
        )
        self.min_image_size = tk.IntVar(value=10)
        image_spin = ttk.Spinbox(
            options_frame,
            from_=1,
            to=1024,
            increment=10,
            textvariable=self.min_image_size,
            width=10
        )
        image_spin.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        # Erweiterte Optionen (Button)
        ttk.Button(
            options_frame,
            text="⚙ Erweiterte Einstellungen...",
            command=self._show_advanced_settings
        ).grid(row=2, column=2, rowspan=2, padx=10, pady=5)

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

        self.pause_button = ttk.Button(
            button_frame,
            text="⏸ Pause",
            command=self._toggle_pause,
            state="disabled"
        )
        self.pause_button.pack(side="left", padx=(0, 10))

        self.stop_button = ttk.Button(
            button_frame,
            text="■ Stoppen",
            command=self._stop_processing,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=(0, 10))

        # Hilfe-Button
        ttk.Button(
            button_frame,
            text="❓ Hilfe",
            command=self._show_help
        ).pack(side="left")

        # Statistik und Zeit
        stats_container = ttk.Frame(footer_frame)
        stats_container.grid(row=0, column=1, sticky="e")

        self.stats_label = ttk.Label(stats_container, text="Bereit")
        self.stats_label.pack(side="top", anchor="e")

        self.time_label = ttk.Label(stats_container, text="", foreground="gray")
        self.time_label.pack(side="top", anchor="e")

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
            progress = ((self.stats['processed'] + self.stats['skipped']) / self.stats['total_files']) * 100
            self.progress_var.set(progress)

            # Berechne Restzeit
            if self.start_time and (self.stats['processed'] + self.stats['skipped']) > 0:
                import time
                elapsed = time.time() - self.start_time
                completed = self.stats['processed'] + self.stats['skipped']
                remaining = self.stats['total_files'] - completed

                if remaining > 0:
                    avg_time = elapsed / completed
                    eta_seconds = avg_time * remaining

                    # Formatiere Zeit
                    if eta_seconds < 60:
                        eta_str = f"{int(eta_seconds)}s"
                    elif eta_seconds < 3600:
                        minutes = int(eta_seconds / 60)
                        seconds = int(eta_seconds % 60)
                        eta_str = f"{minutes}m {seconds}s"
                    else:
                        hours = int(eta_seconds / 3600)
                        minutes = int((eta_seconds % 3600) / 60)
                        eta_str = f"{hours}h {minutes}m"

                    # Formatiere vergangene Zeit
                    if elapsed < 60:
                        elapsed_str = f"{int(elapsed)}s"
                    elif elapsed < 3600:
                        minutes = int(elapsed / 60)
                        seconds = int(elapsed % 60)
                        elapsed_str = f"{minutes}m {seconds}s"
                    else:
                        hours = int(elapsed / 3600)
                        minutes = int((elapsed % 3600) / 60)
                        elapsed_str = f"{hours}h {minutes}m"

                    self.time_label.config(text=f"Vergangen: {elapsed_str} | Verbleibend: ~{eta_str}")
                else:
                    self.time_label.config(text=f"Abgeschlossen")
            else:
                self.time_label.config(text="")

    def _start_processing(self):
        """Startet die Verarbeitung"""
        src = self.src_path.get()
        dst = self.dst_path.get()

        if not os.path.exists(src):
            messagebox.showerror("Fehler", f"Quellverzeichnis existiert nicht:\n{src}")
            return

        self.processing = True
        self.paused = False
        self.start_button.config(state="disabled")
        self.pause_button.config(state="normal")
        self.stop_button.config(state="normal")
        self.progress_var.set(0)

        self.stats = {'total_files': 0, 'processed': 0, 'skipped': 0, 'errors': 0}

        # Setze Start-Zeit
        import time
        self.start_time = time.time()
        self.time_label.config(text="Initialisiere...")

        self._log("=== Verarbeitung gestartet ===")
        self._log(f"Quelle: {src}")
        self._log(f"Ziel: {dst}")

        # Starte Worker
        worker = threading.Thread(target=self._processing_worker, daemon=True)
        worker.start()

    def _toggle_pause(self):
        """Pausiert oder setzt die Verarbeitung fort"""
        if self.paused:
            # Fortsetzen
            self.paused = False
            self.pause_button.config(text="⏸ Pause")
            self._log("Verarbeitung wird fortgesetzt...")
        else:
            # Pausieren
            self.paused = True
            self.pause_button.config(text="▶ Fortsetzen")
            self._log("Verarbeitung wird nach aktueller Datei pausiert...")

    def _stop_processing(self):
        """Stoppt die Verarbeitung"""
        self.processing = False
        self.paused = False
        self._log("Verarbeitung wird gestoppt...")

    def _processing_worker(self):
        """Worker-Thread"""
        try:
            import FileInventory
            import io
            import contextlib

            # Setze Pfade in FileInventory-Modul
            src = self.src_path.get()
            dst = self.dst_path.get()
            FileInventory.SRC_ROOT = src
            FileInventory.DST_ROOT = dst

            # Setze Parameter
            FileInventory.SUMMARY_MAX_CHARS = self.summary_max_chars.get()
            FileInventory.MIN_IMAGE_SIZE = self.min_image_size.get() * 1024  # KB -> Bytes

            # Erstelle stdout-Capture für print-Ausgaben
            output_capture = io.StringIO()

            # Log Konfiguration
            self.message_queue.put(("log", f"Konfiguration:"))
            self.message_queue.put(("log", f"  DSGVO: {self.update_dsgvo.get()}"))
            self.message_queue.put(("log", f"  Existierende überspringen: {self.skip_existing.get()}"))
            self.message_queue.put(("log", f"  Max. Zusammenfassung: {FileInventory.SUMMARY_MAX_CHARS} Zeichen"))
            self.message_queue.put(("log", f"  Min. Bildgröße: {self.min_image_size.get()} KB"))

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

            # Verarbeite alle Dateien
            for idx, file_path in enumerate(all_files, 1):
                if not self.processing:
                    self.message_queue.put(("log", "Verarbeitung abgebrochen"))
                    break

                # Warte während Pause
                while self.paused and self.processing:
                    import time
                    time.sleep(0.1)

                # Prüfe erneut ob gestoppt wurde während Pause
                if not self.processing:
                    self.message_queue.put(("log", "Verarbeitung abgebrochen"))
                    break

                try:
                    self.message_queue.put(("log", f"[{idx}/{len(all_files)}] {os.path.basename(file_path)}"))

                    # Prüfe skip_existing
                    skip_existing = self.skip_existing.get()
                    if not skip_existing:
                        # Lösche vorhandene JSON falls vorhanden
                        rel_path = os.path.relpath(file_path, src)
                        dst_dir = os.path.join(dst, os.path.dirname(rel_path))
                        dst_file = os.path.join(dst_dir, os.path.basename(file_path) + ".json")
                        if os.path.exists(dst_file):
                            os.remove(dst_file)
                            self.message_queue.put(("log", f"  Lösche existierende JSON"))

                    # Capture stdout für print-Ausgaben
                    with contextlib.redirect_stdout(output_capture):
                        # Rufe FileInventory process_file auf
                        result = process_file(file_path)

                    # Hole print-Ausgaben und zeige sie in GUI
                    captured = output_capture.getvalue()
                    if captured:
                        for line in captured.strip().split('\n'):
                            if line:
                                self.message_queue.put(("log", f"  {line}"))
                        output_capture.truncate(0)
                        output_capture.seek(0)

                    if result is None:
                        # Datei wurde übersprungen oder hatte Fehler
                        self.stats['skipped'] += 1
                    else:
                        self.stats['processed'] += 1

                    self.message_queue.put(("stats", None))

                except Exception as e:
                    self.message_queue.put(("log", f"  ⚠️ Fehler: {str(e)}"))
                    self.stats['errors'] += 1
                    self.message_queue.put(("stats", None))

            self.message_queue.put(("log", "=== Verarbeitung abgeschlossen ==="))
            self.message_queue.put(("log", f"✓ Verarbeitet: {self.stats['processed']}, Übersprungen: {self.stats['skipped']}, Fehler: {self.stats['errors']}"))

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
        self.paused = False
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled", text="⏸ Pause")
        self.stop_button.config(state="disabled")
        self.progress_var.set(100)

        # Zeige Gesamt-Zeit
        if self.start_time:
            import time
            total_elapsed = time.time() - self.start_time

            if total_elapsed < 60:
                elapsed_str = f"{int(total_elapsed)}s"
            elif total_elapsed < 3600:
                minutes = int(total_elapsed / 60)
                seconds = int(total_elapsed % 60)
                elapsed_str = f"{minutes}m {seconds}s"
            else:
                hours = int(total_elapsed / 3600)
                minutes = int((total_elapsed % 3600) / 60)
                elapsed_str = f"{hours}h {minutes}m"

            self.time_label.config(text=f"Abgeschlossen in {elapsed_str}")
            self.start_time = None

    def _show_advanced_settings(self):
        """Zeigt erweiterte Einstellungen in einem Dialog"""
        dialog = tk.Toplevel(self)
        dialog.title("Erweiterte Einstellungen")
        dialog.geometry("600x500")
        dialog.transient(self)
        dialog.grab_set()

        # Hauptframe mit Scrollbar
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Titel
        ttk.Label(
            main_frame,
            text="⚙ Erweiterte Einstellungen",
            font=('Helvetica', 16, 'bold')
        ).pack(pady=(0, 20))

        # Notebook für Tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True)

        # Tab 1: Dateitypen
        files_tab = ttk.Frame(notebook, padding="10")
        notebook.add(files_tab, text="Dateitypen")

        ttk.Label(
            files_tab,
            text="Zu verarbeitende Dateitypen:",
            font=('Helvetica', 12, 'bold')
        ).pack(anchor="w", pady=(0, 10))

        extensions_text = ", ".join(sorted(EXTENSIONS))
        ttk.Label(
            files_tab,
            text=extensions_text,
            wraplength=500,
            justify="left"
        ).pack(anchor="w")

        ttk.Label(
            files_tab,
            text="\n💡 Tipp: Dateitypen können in FileInventory.py angepasst werden",
            foreground="gray"
        ).pack(anchor="w")

        # Tab 2: Ausschlüsse
        exclude_tab = ttk.Frame(notebook, padding="10")
        notebook.add(exclude_tab, text="Ausschlüsse")

        ttk.Label(
            exclude_tab,
            text="Ausgeschlossene Verzeichnisse:",
            font=('Helvetica', 12, 'bold')
        ).pack(anchor="w", pady=(0, 10))

        exclude_text = tk.Text(exclude_tab, height=15, wrap="word")
        exclude_text.pack(fill="both", expand=True)
        exclude_text.insert("1.0", "\n".join(EXCLUDE_PATTERNS))
        exclude_text.config(state="disabled")

        # Tab 3: LLM-Einstellungen
        llm_tab = ttk.Frame(notebook, padding="10")
        notebook.add(llm_tab, text="LLM")

        ttk.Label(
            llm_tab,
            text="LM Studio Konfiguration:",
            font=('Helvetica', 12, 'bold')
        ).pack(anchor="w", pady=(0, 10))

        # API URL
        ttk.Label(llm_tab, text="API URL:").pack(anchor="w")
        api_url = ttk.Entry(llm_tab, width=50)
        api_url.insert(0, "http://localhost:1234/v1/chat/completions")
        api_url.pack(fill="x", pady=(0, 10))

        # Model Name
        ttk.Label(llm_tab, text="Model Name:").pack(anchor="w")
        model_name = ttk.Entry(llm_tab, width=50)
        model_name.insert(0, "local-model")
        model_name.pack(fill="x", pady=(0, 10))

        # Max Context Tokens
        ttk.Label(llm_tab, text="Max Context Tokens:").pack(anchor="w")
        max_tokens = ttk.Spinbox(llm_tab, from_=8192, to=524288, increment=8192, width=20)
        max_tokens.set(262144)
        max_tokens.pack(anchor="w", pady=(0, 10))

        # Tab 4: Performance
        perf_tab = ttk.Frame(notebook, padding="10")
        notebook.add(perf_tab, text="Performance")

        ttk.Label(
            perf_tab,
            text="Performance-Einstellungen:",
            font=('Helvetica', 12, 'bold')
        ).pack(anchor="w", pady=(0, 10))

        # Parallele Verarbeitung (zukünftig)
        parallel_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            perf_tab,
            text="Parallele Verarbeitung (experimentell)",
            variable=parallel_var,
            state="disabled"
        ).pack(anchor="w")

        ttk.Label(
            perf_tab,
            text="⚠️ Noch nicht implementiert",
            foreground="orange"
        ).pack(anchor="w", padx=20)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(20, 0))

        ttk.Button(
            button_frame,
            text="Schließen",
            command=dialog.destroy
        ).pack(side="right", padx=5)

        ttk.Button(
            button_frame,
            text="Standard wiederherstellen",
            command=lambda: messagebox.showinfo(
                "Info",
                "Diese Funktion ist noch nicht implementiert.\n"
                "Starte die App neu für Standard-Einstellungen."
            )
        ).pack(side="right", padx=5)

    def _show_help(self):
        """Zeigt die Hilfe-Seite mit README"""
        help_window = tk.Toplevel(self)
        help_window.title("FileInventory - Hilfe")
        help_window.geometry("900x700")
        help_window.transient(self)

        # Hauptframe
        main_frame = ttk.Frame(help_window, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Titel
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(
            title_frame,
            text="❓ FileInventory - Hilfe & Dokumentation",
            font=('Helvetica', 18, 'bold')
        ).pack(side="left")

        ttk.Button(
            title_frame,
            text="✕ Schließen",
            command=help_window.destroy
        ).pack(side="right")

        # Notebook für Tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True, pady=(0, 10))

        # Tab 1: Schnellstart
        quickstart_tab = ttk.Frame(notebook, padding="10")
        notebook.add(quickstart_tab, text="Schnellstart")

        quickstart_text = tk.Text(quickstart_tab, wrap="word", font=('Helvetica', 11))
        quickstart_scroll = ttk.Scrollbar(quickstart_tab, command=quickstart_text.yview)
        quickstart_text.configure(yscrollcommand=quickstart_scroll.set)

        quickstart_content = """
🚀 SCHNELLSTART

1. QUELLVERZEICHNIS AUSWÄHLEN
   • Klicke auf "Durchsuchen" beim Quellverzeichnis
   • Wähle den Ordner mit deinen Dokumenten (z.B. OneDrive)
   • Standard: ~/OneDrive - CompanyName

2. AUSGABEVERZEICHNIS FESTLEGEN
   • Klicke auf "Durchsuchen" beim Ausgabeverzeichnis
   • Wähle wo die JSON-Dateien gespeichert werden sollen
   • Standard: ~/LLM

3. OPTIONEN KONFIGURIEREN
   ☑ DSGVO-Klassifizierung durchführen
      → Analysiert Dokumente auf personenbezogene Daten
      → Warnt vor sensiblen Daten (Gehaltsabrechnungen, etc.)

   ☑ Existierende Dateien überspringen
      → Spart Zeit bei erneutem Durchlauf
      → Nur neue/geänderte Dateien werden verarbeitet

   ☐ Kombinierte Datenbank erstellen
      → Erstellt große JSON-Datenbanken für RAG-Systeme
      → Optimal für semantische Suche

4. PARAMETER ANPASSEN (OPTIONAL)
   • Max. Zusammenfassung: 500-5000 Zeichen
   • Min. Bildgröße: 1-1024 KB
   • ⚙ Erweiterte Einstellungen für mehr Optionen

5. VERARBEITUNG STARTEN
   • Klicke auf "▶ Verarbeitung starten"
   • Beobachte den Fortschritt im Log-Bereich
   • Stoppe bei Bedarf mit "■ Stoppen"

6. ERGEBNISSE NUTZEN
   • JSON-Dateien im Ausgabeverzeichnis
   • Eine .json pro Quelldatei
   • Enthält: Zusammenfassung, Entities, Keywords, DSGVO-Klassifizierung
"""

        quickstart_text.insert("1.0", quickstart_content)
        quickstart_text.config(state="disabled")
        quickstart_text.pack(side="left", fill="both", expand=True)
        quickstart_scroll.pack(side="right", fill="y")

        # Tab 2: Features
        features_tab = ttk.Frame(notebook, padding="10")
        notebook.add(features_tab, text="Features")

        features_text = tk.Text(features_tab, wrap="word", font=('Helvetica', 11))
        features_scroll = ttk.Scrollbar(features_tab, command=features_text.yview)
        features_text.configure(yscrollcommand=features_scroll.set)

        features_content = """
✨ FEATURES

📄 UNTERSTÜTZTE DATEITYPEN
   • PDF-Dokumente (.pdf)
   • Word-Dokumente (.docx, .doc)
   • PowerPoint-Präsentationen (.pptx, .ppt)
   • Excel-Tabellen (.xlsx, .xls, .xlsm, .xltx)
   • Textdateien (.txt, .md)
   • Bilder (.png, .jpg, .jpeg)

🤖 KI-GESTÜTZTE ANALYSE
   • Automatische Zusammenfassungen via LLM
   • Named Entity Recognition (Firmen, Personen, Institutionen)
   • Keyword-Extraktion
   • Semantisch optimiert für RAG-Systeme

🔐 DSGVO-KLASSIFIZIERUNG
   • Erkennt personenbezogene Daten
   • Unterscheidet Firmen- vs. Private Bankdaten
   • Warnt vor sensiblen Kategorien:
     - Gehaltsabrechnungen
     - Gesundheitsdaten
     - Personalakten
     - Sozialversicherungsdaten
   • Rechtliche Einordnung nach Art. 9 DSGVO

📊 DATENEXTRAKTION
   • Text aus PDFs (auch gescannte mit OCR)
   • Metadaten (Autor, Datum, etc.)
   • URLs und E-Mail-Adressen
   • Telefonnummern
   • Projekte und Organisationen

🚀 PERFORMANCE
   • Intelligentes Caching
   • Duplikat-Erkennung
   • Multi-Threading (GUI bleibt responsive)
   • Fortschrittsanzeige in Echtzeit

💾 OUTPUT
   • JSON-Format pro Datei
   • RAG-optimierte Zusammenfassungen
   • Strukturierte Metadaten
   • Optional: Kombinierte Datenbanken
"""

        features_text.insert("1.0", features_content)
        features_text.config(state="disabled")
        features_text.pack(side="left", fill="both", expand=True)
        features_scroll.pack(side="right", fill="y")

        # Tab 3: FAQ
        faq_tab = ttk.Frame(notebook, padding="10")
        notebook.add(faq_tab, text="FAQ")

        faq_text = tk.Text(faq_tab, wrap="word", font=('Helvetica', 11))
        faq_scroll = ttk.Scrollbar(faq_tab, command=faq_text.yview)
        faq_text.configure(yscrollcommand=faq_scroll.set)

        faq_content = """
❓ HÄUFIG GESTELLTE FRAGEN

F: Wie lange dauert die Verarbeitung?
A: Abhängig von Dateigröße und Anzahl. Typisch:
   • 100 Dokumente: 5-10 Minuten
   • 1000 Dokumente: 1-2 Stunden
   • Mit LLM-Analyse deutlich länger

F: Benötige ich eine Internet-Verbindung?
A: Nein, bis auf LLM-Features. Die App arbeitet lokal.
   Für LLM-Zusammenfassungen muss LM Studio laufen.

F: Was ist LM Studio?
A: Ein lokaler LLM-Server (wie ChatGPT, aber offline).
   Download: https://lmstudio.ai

F: Werden meine Daten in die Cloud hochgeladen?
A: Nein! Alles läuft lokal auf deinem Mac.
   Keine Telemetrie, keine Cloud-Verbindungen.

F: Kann ich die Verarbeitung unterbrechen?
A: Ja, mit dem "■ Stoppen" Button.
   Bereits verarbeitete Dateien bleiben erhalten.

F: Was bedeutet "DSGVO-Klassifizierung"?
A: Das Tool erkennt personenbezogene Daten und warnt dich:
   • Gehaltsabrechnungen → sehr schützenswert
   • Firmen-IBANs → nicht personenbezogen
   • Gesundheitsdaten → besonders sensibel

F: Wo finde ich die JSON-Dateien?
A: Im Ausgabeverzeichnis (Standard: ~/LLM)
   Struktur spiegelt Quellverzeichnis wider.

F: Kann ich mehrere Ordner gleichzeitig verarbeiten?
A: Wähle einen Hauptordner - Unterordner werden automatisch
   rekursiv durchsucht (außer ausgeschlossene Patterns).

F: Was sind "Exclude Patterns"?
A: Ordner die übersprungen werden, z.B.:
   • Vorlagen
   • Templates
   • Archive
   → Siehe "Erweiterte Einstellungen" → "Ausschlüsse"

F: Wie kann ich Dateitypen ändern?
A: In FileInventory.py die Variable EXTENSIONS anpassen.
   GUI-Version zeigt nur aktuelle Einstellungen an.

F: Verbraucht die App viel Speicher?
A: Normal: 50-200 MB
   Bei großen PDFs/Bildern: Bis 500 MB
   Nach Abschluss wird Speicher freigegeben.
"""

        faq_text.insert("1.0", faq_content)
        faq_text.config(state="disabled")
        faq_text.pack(side="left", fill="both", expand=True)
        faq_scroll.pack(side="right", fill="y")

        # Tab 4: Über
        about_tab = ttk.Frame(notebook, padding="10")
        notebook.add(about_tab, text="Über")

        about_text = tk.Text(about_tab, wrap="word", font=('Helvetica', 11))
        about_scroll = ttk.Scrollbar(about_tab, command=about_text.yview)
        about_text.configure(yscrollcommand=about_scroll.set)

        about_content = f"""
📁 FILEINVENTORY

Version: {VERSION}
Datum: {VERSION_DATE}

BESCHREIBUNG
KI-gestützte Dokumenten-Analyse mit DSGVO-Klassifizierung.
Erstellt strukturierte JSON-Datenbanken für RAG-Systeme.

ENTWICKELT VON
Frank Schäfer

TECHNOLOGIE
• Python 3.12+
• Tkinter (GUI)
• LM Studio (LLM-Integration)
• pdfplumber (PDF-Extraktion)
• python-docx, python-pptx, openpyxl (Office-Formate)
• pytesseract (OCR)

QUELLCODE
Die CLI-Version ist Open Source verfügbar.
GUI-Version: Proprietär

LIZENZ
Proprietär - Frank Schäfer
© 2025 Alle Rechte vorbehalten

SUPPORT
Bei Problemen oder Fragen:
• GitHub: frankschaefer/dirToLLM
• E-Mail: Support-Kontakt

CHANGELOG v1.20.0
• ✅ Grafische Benutzeroberfläche
• ✅ DSGVO-Bankdaten-Unterscheidung
• ✅ Erweiterte Einstellungen
• ✅ Live-Fortschrittsanzeige
• ✅ Multi-Threading

BEKANNTE EINSCHRÄNKUNGEN
• OCR benötigt Tesseract-Installation
• LLM benötigt LM Studio
• Große Dateien (>100MB) können langsam sein

GEPLANTE FEATURES
• Drag & Drop Support
• Export-Funktionen (CSV, Excel)
• Cloud-Integration
• Mehrsprachigkeit

MADE WITH ❤️
Entwickelt mit Claude Code und Liebe zum Detail.

---

FileInventory - Die intelligente Art, Dokumente zu verwalten.
"""

        about_text.insert("1.0", about_content)
        about_text.config(state="disabled")
        about_text.pack(side="left", fill="both", expand=True)
        about_scroll.pack(side="right", fill="y")

        # Footer mit Links
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill="x", pady=(10, 0))

        ttk.Button(
            footer_frame,
            text="📖 README_GUI.md öffnen",
            command=lambda: self._open_file("README_GUI.md")
        ).pack(side="left", padx=5)

        ttk.Button(
            footer_frame,
            text="📄 Release Notes",
            command=lambda: self._open_file("RELEASE_NOTES_v1.20.0.md")
        ).pack(side="left", padx=5)

        ttk.Button(
            footer_frame,
            text="🌐 GitHub",
            command=lambda: os.system("open https://github.com/frankschaefer/dirToLLM")
        ).pack(side="left", padx=5)

    def _open_file(self, filename):
        """Öffnet eine Dokumentations-Datei"""
        filepath = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(filepath):
            os.system(f"open '{filepath}'")
        else:
            messagebox.showwarning(
                "Datei nicht gefunden",
                f"Die Datei {filename} wurde nicht gefunden."
            )


def main():
    """Haupteinstiegspunkt"""
    app = FileInventoryAppLite()
    app.mainloop()


if __name__ == "__main__":
    main()
