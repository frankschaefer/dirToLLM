"""
setup_lite.py für FileInventory GUI Lite - macOS App Bundle
============================================================

Kompatibel mit älteren macOS-Versionen (10.13+)
Verwendet Standard Tkinter statt CustomTkinter

Usage:
    python3 setup_lite.py py2app

Output:
    dist/FileInventory.app
"""

from setuptools import setup

APP = ['FileInventoryGUI_Lite.py']
APP_NAME = 'FileInventory'
VERSION = '1.19.0'

DATA_FILES = []

OPTIONS = {
    'argv_emulation': False,
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': 'FileInventory - Dokumenten-Analyse',
        'CFBundleGetInfoString': f'FileInventory v{VERSION}',
        'CFBundleIdentifier': 'com.marckonig.fileinventory',
        'CFBundleVersion': VERSION,
        'CFBundleShortVersionString': VERSION,
        'NSHumanReadableCopyright': '© 2025 [Your Company Name]',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13.0',
        'NSRequiresAquaSystemAppearance': False,
    },
    'packages': [
        'tkinter',
        'PIL',
        'requests',
        'pdfplumber',
        'docx',
        'pptx',
        'openpyxl',
    ],
    'includes': [
        'FileInventory',
    ],
    'excludes': [
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'test',
        'unittest',
        'customtkinter',  # Nicht benötigt in Lite
    ],
    'optimize': 2,
}

setup(
    name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    version=VERSION,
    description='KI-gestützte Dokumenten-Analyse mit DSGVO-Klassifizierung (Lite)',
    author='[Your Company Name]',
)
