#!/usr/bin/env python3
"""
FavApp Starter - Launch your favorite apps with one click.

PyQt6 version - Modern Windows application for managing application profiles
and launching them simultaneously.

Version: 26.2.2 (PyQt6)
"""

import sys
import os

# Add the project root to the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer
from core.config import ConfigManager
from core.launcher import AppLauncher
from gui import MainWindow, StyleManager


def main():
    """Application entry point."""
    # Set Windows AppUserModelID for proper taskbar icon (Windows only)
    if sys.platform == 'win32':
        try:
            import ctypes
            myappid = 'andyucu.favappstarter.26.2.2'  # arbitrary string
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

    # Check if a .favapp file was passed as argument
    favapp_file = None
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.isfile(arg) and arg.lower().endswith('.favapp'):
            favapp_file = arg

    # Create and show main window
    window = MainWindow(config)

    # If a .favapp file was provided, launch its apps
    if favapp_file:
        profile_data = config.load_profile_from_file(favapp_file)
        if profile_data:
            apps = profile_data.get("data", {}).get("apps", [])
            if apps:
                launcher = AppLauncher()
                # Use QTimer to launch apps after window is shown
                QTimer.singleShot(500, lambda: launcher.launch_multiple(apps, config.get_launch_delay()))

    window.show()

    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
