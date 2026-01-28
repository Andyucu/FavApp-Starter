"""GUI module for FavApp Starter (PyQt6 implementation)."""

from .qt.main_window_qt import MainWindow
from .qt.styles import StyleManager
from .qt.dialogs_qt import (
    ConfirmDialog,
    AddProfileDialog,
    AboutDialog,
    LicenseDialog,
    EditAppDialog,
    OptionsDialog,
    SearchAppsDialog,
    AddAppDialog
)

__all__ = [
    "MainWindow",
    "StyleManager",
    "ConfirmDialog",
    "AddProfileDialog",
    "AboutDialog",
    "LicenseDialog",
    "EditAppDialog",
    "OptionsDialog",
    "SearchAppsDialog",
    "AddAppDialog"
]
