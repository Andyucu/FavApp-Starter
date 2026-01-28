#!/usr/bin/env python3
"""
FavApp Starter - Launch your favorite apps with one click.

PyQt6 version - Modern Windows application for managing application profiles
and launching them simultaneously.

Version: 26.02.01 (PyQt6)
"""

import sys
import os

# Add the project root to the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from core.config import ConfigManager
from gui import MainWindow, StyleManager


def main():
    """Application entry point."""
    # Set Windows AppUserModelID for proper taskbar icon (Windows only)
    if sys.platform == 'win32':
        try:
            import ctypes
            myappid = 'andyucu.favappstarter.26.02.01'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except:
            pass  # Silently fail on non-Windows or if it doesn't work

    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("FavApp Starter")
    app.setOrganizationName("Alexandru Teodorovici")

    # Set application icon for taskbar
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'icon.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Load configuration
    config = ConfigManager()

    # Apply theme
    theme = config.get_theme()
    stylesheet = StyleManager.get_stylesheet(theme)
    app.setStyleSheet(stylesheet)

    # Create and show main window
    window = MainWindow(config)
    window.show()

    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
