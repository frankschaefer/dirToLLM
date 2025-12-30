#!/usr/bin/env python3
"""
Quick GUI Test - Minimale Version zum Testen
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class TestGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("FileInventory GUI - Test")
        self.geometry("800x600")

        # Hauptframe
        main = ttk.Frame(self, padding="20")
        main.pack(fill="both", expand=True)

        # Titel
        title = ttk.Label(
            main,
            text="📁 FileInventory GUI Test",
            font=('Helvetica', 20, 'bold')
        )
        title.pack(pady=20)

        # Info
        info_text = """
        ✅ Tkinter funktioniert!
        ✅ GUI kann gestartet werden
        ✅ macOS-Kompatibilität gegeben

        Diese Test-GUI zeigt, dass die grundlegende
        Tkinter-Funktionalität auf deinem System läuft.

        Die vollständige GUI ist verfügbar in:
        - FileInventoryGUI_Lite.py (Standard Tkinter)
        - FileInventoryGUI.py (CustomTkinter - wenn verfügbar)
        """

        info = ttk.Label(main, text=info_text, justify="left")
        info.pack(pady=20)

        # Test-Buttons
        btn_frame = ttk.Frame(main)
        btn_frame.pack(pady=20)

        ttk.Button(
            btn_frame,
            text="Test: Ordner auswählen",
            command=self.test_folder
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame,
            text="Test: MessageBox",
            command=self.test_msgbox
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame,
            text="Beenden",
            command=self.quit
        ).pack(side="left", padx=5)

        # Status
        self.status = ttk.Label(main, text="Bereit", foreground="green")
        self.status.pack(pady=20)

    def test_folder(self):
        folder = filedialog.askdirectory(title="Test: Ordner auswählen")
        if folder:
            self.status.config(text=f"✓ Ordner ausgewählt: {os.path.basename(folder)}")

    def test_msgbox(self):
        messagebox.showinfo("Test", "MessageBox funktioniert! ✓")
        self.status.config(text="✓ MessageBox-Test erfolgreich")

if __name__ == "__main__":
    app = TestGUI()
    app.mainloop()
