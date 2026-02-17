# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for FavApp Starter (PyQt6 version).

Build command for version-specific output folder:
    pyinstaller FavApp.spec --distpath "dist/v26.2.2" --noconfirm

Or for default dist folder:
    pyinstaller FavApp.spec --noconfirm

Note: Update version number in --distpath when releasing new versions.
"""

import os
import sys

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include app assets
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'core',
        'core.config',
        'core.launcher',
        'core.app_finder',
        'core.autostart',
        'core.debug_logger',
        'gui',
        'gui.qt',
        'gui.qt.main_window_qt',
        'gui.qt.dialogs_qt',
        'gui.qt.styles',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'customtkinter',
        'tkinter',
        'pystray',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FavApp Starter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (GUI app)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
)
