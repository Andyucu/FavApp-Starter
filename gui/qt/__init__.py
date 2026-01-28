"""PyQt6 GUI implementation for FavApp Starter."""

from .main_window_qt import MainWindow
from .styles import StyleManager
from .dialogs_qt import (
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
    'MainWindow',
    'StyleManager',
    'ConfirmDialog',
    'AddProfileDialog',
    'AboutDialog',
    'LicenseDialog',
    'EditAppDialog',
    'OptionsDialog',
    'SearchAppsDialog',
    'AddAppDialog'
]
