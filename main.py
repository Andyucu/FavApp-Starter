#!/usr/bin/env python3
"""
FavApp Starter - Launch your favorite apps with one click.

A Windows application that allows you to organize applications into profiles
and launch them all simultaneously.

Version: 26.01.08
"""

import sys
import os

# Add the project root to the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow


def main():
    """Application entry point."""
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
