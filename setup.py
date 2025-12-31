"""
setup.py für FileInventory GUI - macOS App Bundle
==================================================

Erstellt ein macOS .app Bundle mit py2app

Usage:
    python3 setup.py py2app

Output:
    dist/FileInventory.app
"""

from setuptools import setup

APP = ['FileInventoryGUI.py']
APP_NAME = 'FileInventory'
VERSION = '1.19.0'

DATA_FILES = [
    # Füge zusätzliche Daten hinzu wenn nötig
]

OPTIONS = {
    'argv_emulation': False,
    'iconfile': None,  # TODO: Icon hinzufügen wenn vorhanden
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': 'FileInventory - Dokumenten-Analyse',
        'CFBundleGetInfoString': f'FileInventory v{VERSION}',
        'CFBundleIdentifier': 'com.marckonig.fileinventory',
        'CFBundleVersion': VERSION,
        'CFBundleShortVersionString': VERSION,
        'NSHumanReadableCopyright': '© 2025 [Your Company Name]',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13.0',  # High Sierra+
        'NSRequiresAquaSystemAppearance': False,  # Dark Mode Support
    },
    'packages': [
        'customtkinter',
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
    ],
    'resources': [],
    'optimize': 2,
}

setup(
    name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    version=VERSION,
    description='KI-gestützte Dokumenten-Analyse mit DSGVO-Klassifizierung',
    author='[Your Company Name]',
)
