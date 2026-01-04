"""
Plattformspezifische Konfigurationen für FileInventory.

Unterstützt Windows 11, macOS 15+ (Sequoia und neuer), und Linux.
Automatische Erkennung der Plattform und passende Standardwerte.
"""

import os
import platform
import sys
from pathlib import Path


class PlatformConfig:
    """Plattformspezifische Konfiguration."""

    def __init__(self):
        self.system = platform.system()  # 'Windows', 'Darwin', 'Linux'
        self.release = platform.release()  # z.B. '10', '26.2.0', '5.15.0'
        self.version = platform.version()

        # Setze plattformspezifische Defaults
        self._set_defaults()

    def _set_defaults(self):
        """Setze Standardwerte basierend auf der Plattform."""

        if self.system == 'Windows':
            self._setup_windows()
        elif self.system == 'Darwin':
            self._setup_macos()
        else:  # Linux und andere Unix-Systeme
            self._setup_linux()

    def _setup_windows(self):
        """Windows 11+ Konfiguration."""
        self.platform_name = "Windows"

        # Standard-Pfade für Windows
        user_profile = os.environ.get('USERPROFILE', os.path.expanduser('~'))
        onedrive_consumer = os.environ.get('OneDrive')  # Privates OneDrive
        onedrive_business = os.environ.get('OneDriveCommercial')  # OneDrive for Business

        # Priorisierung: Business OneDrive > Consumer OneDrive > Documents
        if onedrive_business:
            self.default_src = onedrive_business
        elif onedrive_consumer:
            self.default_src = onedrive_consumer
        else:
            self.default_src = os.path.join(user_profile, 'Documents')

        self.default_dst = os.path.join(user_profile, 'LLM')

        # Tesseract OCR Pfade
        self.tesseract_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            os.path.join(user_profile, 'AppData', 'Local', 'Tesseract-OCR', 'tesseract.exe'),
        ]

        # Encoding
        self.default_encoding = 'utf-8'  # Windows 11 unterstützt UTF-8 gut
        self.fallback_encoding = 'cp1252'  # Windows-1252 als Fallback

        # Tastatureingabe-Erkennung
        self.supports_select = False  # Windows verwendet msvcrt

        # Installations-Hinweise
        self.tesseract_install_cmd = "winget install UB-Mannheim.TesseractOCR"
        self.tesseract_install_url = "https://github.com/UB-Mannheim/tesseract/wiki"

    def _setup_macos(self):
        """macOS 15+ (Sequoia) Konfiguration."""
        self.platform_name = "macOS"

        # Standard-Pfade für macOS
        home = Path.home()

        # OneDrive Pfade auf macOS
        # Privat: ~/OneDrive
        # Business: ~/OneDrive - CompanyName
        possible_onedrive_paths = [
            home / "Library" / "CloudStorage" / "OneDrive-Personal",
            home / "Library" / "CloudStorage",  # Suche nach OneDrive-* Ordnern
            home / "OneDrive - CompanyName",  # Legacy Business
            home / "OneDrive",  # Legacy Consumer
        ]

        # Finde den ersten existierenden OneDrive Pfad
        self.default_src = None
        for path in possible_onedrive_paths:
            if path.exists():
                if path.name == "CloudStorage":
                    # Suche nach OneDrive-* Unterordnern
                    onedrive_dirs = [d for d in path.iterdir() if d.is_dir() and d.name.startswith('OneDrive')]
                    if onedrive_dirs:
                        self.default_src = str(onedrive_dirs[0])
                        break
                else:
                    self.default_src = str(path)
                    break

        # Fallback auf Documents
        if not self.default_src:
            self.default_src = str(home / "Documents")

        self.default_dst = str(home / "LLM")

        # Tesseract OCR Pfade (Homebrew, MacPorts, etc.)
        self.tesseract_paths = [
            '/opt/homebrew/bin/tesseract',  # Apple Silicon (M1/M2/M3)
            '/usr/local/bin/tesseract',     # Intel Mac
            '/opt/local/bin/tesseract',     # MacPorts
        ]

        # Encoding
        self.default_encoding = 'utf-8'
        self.fallback_encoding = 'utf-8'

        # Tastatureingabe-Erkennung
        self.supports_select = True  # macOS/Unix unterstützt select()

        # Installations-Hinweise
        self.tesseract_install_cmd = "brew install tesseract tesseract-lang"
        self.tesseract_install_url = "https://brew.sh"

    def _setup_linux(self):
        """Linux Konfiguration."""
        self.platform_name = "Linux"

        # Standard-Pfade für Linux
        home = Path.home()

        # OneDrive ist auf Linux weniger verbreitet, aber möglich via rclone
        possible_paths = [
            home / "OneDrive",
            home / "Documents",
        ]

        self.default_src = str(home / "Documents")
        for path in possible_paths:
            if path.exists():
                self.default_src = str(path)
                break

        self.default_dst = str(home / "LLM")

        # Tesseract OCR Pfade
        self.tesseract_paths = [
            '/usr/bin/tesseract',
            '/usr/local/bin/tesseract',
        ]

        # Encoding
        self.default_encoding = 'utf-8'
        self.fallback_encoding = 'utf-8'

        # Tastatureingabe-Erkennung
        self.supports_select = True  # Linux/Unix unterstützt select()

        # Installations-Hinweise
        self.tesseract_install_cmd = "sudo apt-get install tesseract-ocr tesseract-ocr-deu"
        self.tesseract_install_url = "https://github.com/tesseract-ocr/tesseract"

    def find_tesseract(self):
        """
        Findet den Tesseract-Pfad automatisch.

        Returns:
            str or None: Pfad zu tesseract executable oder None
        """
        # Prüfe vorkonfigurierte Pfade
        for path in self.tesseract_paths:
            if os.path.isfile(path):
                return path

        # Prüfe ob tesseract im PATH ist
        try:
            import shutil
            tesseract_cmd = shutil.which('tesseract')
            if tesseract_cmd:
                return tesseract_cmd
        except Exception:
            pass

        return None

    def get_script_name(self):
        """Generiert plattformspezifischen Script-Namen."""
        return f"FileInventory - OneDrive Dokumenten-Zusammenfassung ({self.platform_name})"

    def print_info(self):
        """Gibt Plattform-Informationen aus."""
        print(f"Plattform: {self.platform_name}")
        print(f"System: {self.system} {self.release}")
        print(f"Python: {sys.version.split()[0]}")
        print(f"Standard Quellverzeichnis: {self.default_src}")
        print(f"Standard Zielverzeichnis: {self.default_dst}")

        tesseract = self.find_tesseract()
        if tesseract:
            print(f"Tesseract OCR: {tesseract}")
        else:
            print(f"Tesseract OCR: Nicht gefunden")
            print(f"  Installation: {self.tesseract_install_cmd}")


# Globale Instanz
PLATFORM = PlatformConfig()


# Convenience-Funktionen für Abwärtskompatibilität
def get_default_src():
    """Gibt Standard-Quellverzeichnis zurück."""
    return PLATFORM.default_src


def get_default_dst():
    """Gibt Standard-Zielverzeichnis zurück."""
    return PLATFORM.default_dst


def is_windows():
    """Prüft ob Windows."""
    return PLATFORM.system == 'Windows'


def is_macos():
    """Prüft ob macOS."""
    return PLATFORM.system == 'Darwin'


def is_linux():
    """Prüft ob Linux."""
    return PLATFORM.system == 'Linux'


if __name__ == '__main__':
    # Test-Ausgabe
    print("=== Plattform-Konfiguration ===")
    PLATFORM.print_info()
