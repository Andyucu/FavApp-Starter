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
from core.config import ConfigManager
from gui import MainWindow, StyleManager


def main():
    """Application entry point."""
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("FavApp Starter")
    app.setOrganizationName("Alexandru Teodorovici")

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
