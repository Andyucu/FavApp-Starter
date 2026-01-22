# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for FavApp Starter.
Build command: pyinstaller FavApp.spec
"""

import os
import sys

# Get customtkinter path for bundling assets
import customtkinter
ctk_path = os.path.dirname(customtkinter.__file__)

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include customtkinter assets (themes, etc.)
        (ctk_path, 'customtkinter'),
    ],
    hiddenimports=[
        'customtkinter',
        'darkdetect',
        'PIL',
        'PIL._tkinter_finder',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    icon=None,  # Add icon path here if you have one
)
