"""GUI module for FavApp Starter."""

from .main_window import MainWindow
from .dialogs import (
    AddAppDialog,
    EditAppDialog,
    AddProfileDialog,
    ConfirmDialog,
    OptionsDialog,
    AboutDialog,
    LicenseDialog
)

__all__ = [
    "MainWindow",
    "AddAppDialog",
    "EditAppDialog",
    "AddProfileDialog",
    "ConfirmDialog",
    "OptionsDialog",
    "AboutDialog",
    "LicenseDialog"
]
