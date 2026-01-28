"""Dialog windows for FavApp Starter (PyQt6 implementation)."""

import os
import sys
import threading
from typing import Callable, Optional
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QWidget, QScrollArea, QCheckBox,
    QComboBox, QSpinBox, QFileDialog, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon

from core.autostart import AutoStart
from core.app_finder import AppFinder


class ConfirmDialog(QDialog):
    """Confirmation dialog with Yes/No options."""

    def __init__(self, parent, title: str, message: str):
        """
        Initialize the confirmation dialog.

        Args:
            parent: Parent window
            title: Dialog title
            message: Message to display
        """
        super().__init__(parent)

        self.confirmed = False

        # Window setup
        self.setWindowTitle(title)
        self.setFixedSize(350, 130)
        self.setModal(True)
        self._set_icon()

        # Center on parent
        if parent:
            parent_geo = parent.geometry()
            self.move(
                parent_geo.x() + (parent_geo.width() - 350) // 2,
                parent_geo.y() + (parent_geo.height() - 130) // 2
            )

        self._create_widgets(message)

    def _set_icon(self):
        """Set dialog icon."""
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        icon_path = os.path.join(base_dir, "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def _create_widgets(self, message: str):
        """Create dialog widgets."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Message label
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(message_label)

        # Button frame
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # No button (gray)
        no_button = QPushButton("No")
        no_button.setObjectName("grayButton")
        no_button.setFixedWidth(100)
        no_button.clicked.connect(self.reject)
        button_layout.addWidget(no_button)

        button_layout.addStretch()

        # Yes button (red/danger)
        yes_button = QPushButton("Yes")
        yes_button.setObjectName("deleteButton")
        yes_button.setFixedWidth(100)
        yes_button.clicked.connect(self._on_confirm)
        button_layout.addWidget(yes_button)

        layout.addLayout(button_layout)

    def _on_confirm(self):
        """Handle confirm button click."""
        self.confirmed = True
        self.accept()


class AddProfileDialog(QDialog):
    """Dialog for creating a new profile."""

    def __init__(self, parent, existing_profiles: list[str]):
        """
        Initialize the Add Profile dialog.

        Args:
            parent: Parent window
            existing_profiles: List of existing profile names (for validation)
        """
        super().__init__(parent)

        self.existing_profiles = [p.lower() for p in existing_profiles]
        self.profile_name = None

        # Window setup
        self.setWindowTitle("New Profile")
        self.setFixedSize(450, 150)
        self.setModal(True)
        self._set_icon()

        # Center on parent
        if parent:
            parent_geo = parent.geometry()
            self.move(
                parent_geo.x() + (parent_geo.width() - 450) // 2,
                parent_geo.y() + (parent_geo.height() - 150) // 2
            )

        self._create_widgets()

    def _set_icon(self):
        """Set dialog icon."""
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        icon_path = os.path.join(base_dir, "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def _create_widgets(self):
        """Create dialog widgets."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Name input section
        name_label = QLabel("Profile Name:")
        layout.addWidget(name_label)

        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("e.g., Work, Gaming, Creative")
        self.name_entry.setMinimumHeight(32)
        self.name_entry.returnPressed.connect(self._on_create_click)
        layout.addWidget(self.name_entry)

        # Focus on entry
        self.name_entry.setFocus()

        # Button frame
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.setObjectName("grayButton")
        cancel_button.setFixedWidth(100)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        button_layout.addStretch()

        # Create button
        create_button = QPushButton("Create")
        create_button.setFixedWidth(100)
        create_button.clicked.connect(self._on_create_click)
        button_layout.addWidget(create_button)

        layout.addLayout(button_layout)

    def _on_create_click(self):
        """Handle create button click."""
        name = self.name_entry.text().strip()

        # Validation
        if not name:
            self._show_error("Please enter a profile name.")
            return

        if name.lower() in self.existing_profiles:
            self._show_error("A profile with this name already exists.")
            return

        self.profile_name = name
        self.accept()

    def _show_error(self, message: str):
        """Show error message dialog."""
        error_dialog = QDialog(self)
        error_dialog.setWindowTitle("Error")
        error_dialog.setFixedSize(300, 100)
        error_dialog.setModal(True)

        layout = QVBoxLayout(error_dialog)
        layout.setContentsMargins(20, 20, 20, 20)

        label = QLabel(message)
        label.setWordWrap(True)
        layout.addWidget(label)

        ok_button = QPushButton("OK")
        ok_button.setFixedWidth(80)
        ok_button.clicked.connect(error_dialog.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

        error_dialog.exec()


class AboutDialog(QDialog):
    """About/App Info dialog."""

    def __init__(self, parent, version: str, author: str):
        """
        Initialize the About dialog.

        Args:
            parent: Parent window
            version: App version string
            author: App author name
        """
        super().__init__(parent)

        self.version = version
        self.author = author

        # Window setup
        self.setWindowTitle("About FavApp Starter")
        self.setFixedSize(500, 550)
        self.setModal(True)
        self._set_icon()

        # Center on parent
        if parent:
            parent_geo = parent.geometry()
            self.move(
                parent_geo.x() + (parent_geo.width() - 500) // 2,
                parent_geo.y() + (parent_geo.height() - 550) // 2
            )

        self._create_widgets()

    def _set_icon(self):
        """Set dialog icon."""
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        icon_path = os.path.join(base_dir, "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def _create_widgets(self):
        """Create dialog widgets."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # App name
        app_name = QLabel("FavApp Starter")
        app_name.setStyleSheet("font-size: 24px; font-weight: bold;")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(app_name)

        # Version
        version_label = QLabel(f"Version {self.version}")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        # Author
        author_label = QLabel(f"By {self.author}")
        author_label.setObjectName("grayLabel")
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(author_label)

        layout.addSpacing(10)

        # Description
        description = QLabel(
            "Launch your favorite applications with one click.\n\n"
            "FavApp Starter allows you to organize applications into profiles "
            "and launch them all simultaneously. Perfect for setting up your "
            "work environment, gaming setup, or any collection of apps you "
            "frequently use together."
        )
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)

        layout.addSpacing(10)

        # License section
        license_label = QLabel("License")
        license_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(license_label)

        # License text (scrollable)
        license_text = QTextEdit()
        license_text.setReadOnly(True)
        license_text.setPlainText(
            "This program is free software: you can redistribute it and/or modify "
            "it under the terms of the GNU General Public License as published by "
            "the Free Software Foundation, either version 3 of the License, or "
            "(at your option) any later version.\n\n"
            "This program is distributed in the hope that it will be useful, "
            "but WITHOUT ANY WARRANTY; without even the implied warranty of "
            "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the "
            "GNU General Public License for more details."
        )
        layout.addWidget(license_text)

        # Close button
        close_button = QPushButton("Close")
        close_button.setFixedWidth(100)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)


class LicenseDialog(QDialog):
    """License information dialog."""

    MIT_LICENSE = """MIT License

Copyright (c) 2025 {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

    def __init__(self, parent, author: str):
        """
        Initialize the License dialog.

        Args:
            parent: Parent window
            author: Author name for the license
        """
        super().__init__(parent)

        self.author = author

        # Window setup
        self.setWindowTitle("License")
        self.setFixedSize(550, 450)
        self.setModal(True)
        self._set_icon()

        # Center on parent
        if parent:
            parent_geo = parent.geometry()
            self.move(
                parent_geo.x() + (parent_geo.width() - 550) // 2,
                parent_geo.y() + (parent_geo.height() - 450) // 2
            )

        self._create_widgets()

    def _set_icon(self):
        """Set dialog icon."""
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        icon_path = os.path.join(base_dir, "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def _create_widgets(self):
        """Create dialog widgets."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("MIT License")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # License text (scrollable)
        license_text_widget = QTextEdit()
        license_text_widget.setReadOnly(True)
        license_text_widget.setStyleSheet("font-family: 'Consolas', 'Courier New', monospace; font-size: 11px;")
        license_text_widget.setPlainText(self.MIT_LICENSE.format(author=self.author))
        layout.addWidget(license_text_widget)

        # Close button
        close_button = QPushButton("Close")
        close_button.setFixedWidth(100)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)


class EditAppDialog(QDialog):
    """Dialog for editing an existing application."""

    def __init__(self, parent, app_data: dict, on_save: Callable[[str, str, str, str], None]):
        """
        Initialize the Edit App dialog.

        Args:
            parent: Parent window
            app_data: Dict with 'name', 'path', 'arguments', 'working_dir' keys
            on_save: Callback function(name, path, arguments, working_dir) called when saved
        """
        super().__init__(parent)

        self.on_save = on_save
        self.app_data = app_data

        # Window setup
        self.setWindowTitle("Edit Application")
        self.setFixedSize(500, 300)
        self.setModal(True)
        self._set_icon()

        # Center on parent
        if parent:
            parent_geo = parent.geometry()
            self.move(
                parent_geo.x() + (parent_geo.width() - 500) // 2,
                parent_geo.y() + (parent_geo.height() - 300) // 2
            )

        self._create_widgets()

    def _set_icon(self):
        """Set dialog icon."""
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        icon_path = os.path.join(base_dir, "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def _create_widgets(self):
        """Create dialog widgets."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Path display (readonly)
        path_layout = QHBoxLayout()
        path_label = QLabel("Application:")
        path_label.setFixedWidth(80)
        path_layout.addWidget(path_label)

        self.path_entry = QLineEdit()
        self.path_entry.setReadOnly(True)
        self.path_entry.setText(self.app_data.get("path", ""))
        self.path_entry.setFixedWidth(370)
        path_layout.addWidget(self.path_entry)

        layout.addLayout(path_layout)

        # Name input
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_label.setFixedWidth(80)
        name_layout.addWidget(name_label)

        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("Enter a display name")
        self.name_entry.setText(self.app_data.get("name", ""))
        self.name_entry.setFixedWidth(370)
        name_layout.addWidget(self.name_entry)

        layout.addLayout(name_layout)

        # Arguments input
        args_layout = QHBoxLayout()
        args_label = QLabel("Arguments:")
        args_label.setFixedWidth(80)
        args_layout.addWidget(args_label)

        self.args_entry = QLineEdit()
        self.args_entry.setPlaceholderText("Command-line arguments (optional)")
        self.args_entry.setText(self.app_data.get("arguments", ""))
        self.args_entry.setFixedWidth(370)
        args_layout.addWidget(self.args_entry)

        layout.addLayout(args_layout)

        # Working directory input
        workdir_layout = QHBoxLayout()
        workdir_label = QLabel("Working Dir:")
        workdir_label.setFixedWidth(80)
        workdir_layout.addWidget(workdir_label)

        self.workdir_entry = QLineEdit()
        self.workdir_entry.setPlaceholderText("Working directory (optional)")
        self.workdir_entry.setText(self.app_data.get("working_dir", ""))
        self.workdir_entry.setFixedWidth(370)
        workdir_layout.addWidget(self.workdir_entry)

        layout.addLayout(workdir_layout)

        layout.addSpacing(20)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        save_button = QPushButton("Save")
        save_button.setFixedWidth(100)
        save_button.clicked.connect(self._on_save_click)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.setObjectName("grayButton")
        cancel_button.setFixedWidth(100)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

    def _on_save_click(self):
        """Handle Save button click."""
        name = self.name_entry.text().strip()
        path = self.app_data.get("path", "")
        arguments = self.args_entry.text().strip()
        working_dir = self.workdir_entry.text().strip()

        if not name:
            self._show_error("Please enter a name for the application.")
            return

        self.on_save(name, path, arguments, working_dir)
        self.accept()

    def _show_error(self, message: str):
        """Show error message dialog."""
        error_dialog = QDialog(self)
        error_dialog.setWindowTitle("Error")
        error_dialog.setFixedSize(300, 100)
        error_dialog.setModal(True)

        layout = QVBoxLayout(error_dialog)
        layout.setContentsMargins(20, 20, 20, 20)

        label = QLabel(message)
        label.setWordWrap(True)
        layout.addWidget(label)

        ok_button = QPushButton("OK")
        ok_button.setFixedWidth(80)
        ok_button.clicked.connect(error_dialog.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

        error_dialog.exec()


class OptionsDialog(QDialog):
    """Options/Settings dialog."""

    def __init__(self, parent, config, on_theme_change: Callable[[str], None]):
        """
        Initialize the Options dialog.

        Args:
            parent: Parent window
            config: ConfigManager instance
            on_theme_change: Callback when theme changes
        """
        super().__init__(parent)

        self.config = config
        self.on_theme_change = on_theme_change
        self.initial_theme = config.get_theme()
        self.selected_theme = self.initial_theme

        # Window setup
        self.setWindowTitle("Options")
        self.setFixedSize(450, 450)
        self.setModal(True)
        self._set_icon()

        # Center on parent
        if parent:
            parent_geo = parent.geometry()
            self.move(
                parent_geo.x() + (parent_geo.width() - 450) // 2,
                parent_geo.y() + (parent_geo.height() - 450) // 2
            )

        self._create_widgets()

    def _set_icon(self):
        """Set dialog icon."""
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        icon_path = os.path.join(base_dir, "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def _create_widgets(self):
        """Create dialog widgets."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Title
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(title)

        # Scrollable area for settings
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        settings_layout.setContentsMargins(0, 0, 0, 0)
        settings_layout.setSpacing(10)

        # Appearance Section
        appearance_label = QLabel("Appearance")
        appearance_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        settings_layout.addWidget(appearance_label)

        # Theme setting
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        theme_label.setFixedWidth(130)
        theme_layout.addWidget(theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "System"])
        self.theme_combo.setCurrentText(self.config.get_theme().capitalize())
        self.theme_combo.setFixedWidth(150)
        self.theme_combo.currentTextChanged.connect(self._on_theme_select)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()

        settings_layout.addLayout(theme_layout)

        # Show icons setting
        self.show_icons_check = QCheckBox("Show application icons")
        self.show_icons_check.setChecked(self.config.get_setting("show_app_icons", True))
        self.show_icons_check.stateChanged.connect(self._on_icons_toggle)
        settings_layout.addWidget(self.show_icons_check)

        settings_layout.addSpacing(5)

        # Behavior Section
        behavior_label = QLabel("Behavior")
        behavior_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        settings_layout.addWidget(behavior_label)

        # Launch delay setting
        delay_layout = QHBoxLayout()
        delay_label = QLabel("Launch delay (ms):")
        delay_label.setFixedWidth(130)
        delay_layout.addWidget(delay_label)

        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(0, 10000)
        self.delay_spin.setValue(self.config.get_setting("launch_delay", 0))
        self.delay_spin.setFixedWidth(100)
        self.delay_spin.valueChanged.connect(self._on_delay_change)
        delay_layout.addWidget(self.delay_spin)
        delay_layout.addStretch()

        settings_layout.addLayout(delay_layout)

        # Minimize to tray
        self.minimize_tray_check = QCheckBox("Minimize to system tray")
        self.minimize_tray_check.setChecked(self.config.get_setting("minimize_to_tray", True))
        self.minimize_tray_check.stateChanged.connect(self._on_minimize_tray_toggle)
        settings_layout.addWidget(self.minimize_tray_check)

        # Start minimized
        self.start_min_check = QCheckBox("Start minimized")
        self.start_min_check.setChecked(self.config.get_setting("start_minimized", False))
        self.start_min_check.stateChanged.connect(self._on_start_min_toggle)
        settings_layout.addWidget(self.start_min_check)

        # Auto-start with Windows
        self.autostart_check = QCheckBox("Start with Windows")
        self.autostart_check.setChecked(AutoStart.is_enabled())
        self.autostart_check.stateChanged.connect(self._on_autostart_toggle)
        settings_layout.addWidget(self.autostart_check)

        # Confirm on exit
        self.confirm_exit_check = QCheckBox("Confirm before exit")
        self.confirm_exit_check.setChecked(self.config.get_setting("confirm_on_exit", False))
        self.confirm_exit_check.stateChanged.connect(self._on_confirm_exit_toggle)
        settings_layout.addWidget(self.confirm_exit_check)

        settings_layout.addStretch()

        scroll.setWidget(settings_widget)
        main_layout.addWidget(scroll)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        close_button = QPushButton("Close")
        close_button.setFixedWidth(100)
        close_button.setFixedHeight(32)
        close_button.clicked.connect(self._on_cancel)
        button_layout.addWidget(close_button)

        save_button = QPushButton("Save")
        save_button.setObjectName("launchButton")
        save_button.setFixedWidth(100)
        save_button.setFixedHeight(32)
        save_button.clicked.connect(self._on_save)
        button_layout.addWidget(save_button)

        main_layout.addLayout(button_layout)

    def _on_theme_select(self, value: str):
        """Handle theme selection."""
        self.selected_theme = value.lower()

    def _on_icons_toggle(self):
        """Handle show icons toggle."""
        self.config.set_setting("show_app_icons", self.show_icons_check.isChecked())

    def _on_delay_change(self):
        """Handle launch delay change."""
        self.config.set_setting("launch_delay", self.delay_spin.value())

    def _on_minimize_tray_toggle(self):
        """Handle minimize to tray toggle."""
        self.config.set_setting("minimize_to_tray", self.minimize_tray_check.isChecked())

    def _on_start_min_toggle(self):
        """Handle start minimized toggle."""
        self.config.set_setting("start_minimized", self.start_min_check.isChecked())

    def _on_confirm_exit_toggle(self):
        """Handle confirm on exit toggle."""
        self.config.set_setting("confirm_on_exit", self.confirm_exit_check.isChecked())

    def _on_autostart_toggle(self):
        """Handle auto-start toggle."""
        if self.autostart_check.isChecked():
            if not AutoStart.enable():
                self.autostart_check.setChecked(False)
                self._show_error("Failed to enable auto-start. Make sure you have proper permissions.")
        else:
            if not AutoStart.disable():
                self.autostart_check.setChecked(True)
                self._show_error("Failed to disable auto-start.")

    def _show_error(self, message: str):
        """Show error message."""
        error_dialog = QDialog(self)
        error_dialog.setWindowTitle("Error")
        error_dialog.setFixedSize(350, 120)
        error_dialog.setModal(True)

        # Center on parent
        parent_geo = self.geometry()
        error_dialog.move(
            parent_geo.x() + (parent_geo.width() - 350) // 2,
            parent_geo.y() + (parent_geo.height() - 120) // 2
        )

        layout = QVBoxLayout(error_dialog)
        layout.setContentsMargins(20, 20, 20, 20)

        label = QLabel(message)
        label.setWordWrap(True)
        layout.addWidget(label)

        ok_button = QPushButton("OK")
        ok_button.setFixedWidth(80)
        ok_button.clicked.connect(error_dialog.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

        error_dialog.exec()

    def _on_save(self):
        """Handle Save button - apply all settings and close."""
        # Save theme
        self.config.set_theme(self.selected_theme)

        # Apply theme change if changed
        if self.selected_theme != self.initial_theme:
            parent = self.parent()
            theme = self.selected_theme
            # Close dialog first, then apply theme
            self.accept()
            QTimer.singleShot(10, lambda: self.on_theme_change(theme))
        else:
            # No theme change, just close
            self.accept()

    def _on_cancel(self):
        """Handle Close/Cancel button - close without applying theme."""
        # Revert theme to initial
        self.config.set_theme(self.initial_theme)
        self.reject()


class SearchAppsDialog(QDialog):
    """Dialog for searching installed applications."""

    def __init__(self, parent, on_select: Callable[[str, str], None]):
        """
        Initialize the Search Apps dialog.

        Args:
            parent: Parent window
            on_select: Callback function(path, name) called when app is selected
        """
        super().__init__(parent)

        self.on_select = on_select
        self.apps = []
        self.filtered_apps = []

        # Window setup
        self.setWindowTitle("Search Installed Applications")
        self.resize(600, 500)
        self.setModal(True)
        self._set_icon()

        # Center on parent
        if parent:
            parent_geo = parent.geometry()
            self.move(
                parent_geo.x() + (parent_geo.width() - 600) // 2,
                parent_geo.y() + (parent_geo.height() - 500) // 2
            )

        self._create_widgets()
        self._load_apps()

    def _set_icon(self):
        """Set dialog icon."""
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        icon_path = os.path.join(base_dir, "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def _create_widgets(self):
        """Create dialog widgets."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Title and status
        header_layout = QHBoxLayout()

        title = QLabel("Installed Applications")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        self.status_label = QLabel("Loading...")
        self.status_label.setStyleSheet("color: gray; font-size: 11px;")
        header_layout.addWidget(self.status_label)

        layout.addLayout(header_layout)

        # Search box
        search_layout = QHBoxLayout()

        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("font-size: 22px;")
        search_icon.setFixedWidth(30)
        search_layout.addWidget(search_icon)

        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Search applications...")
        self.search_entry.textChanged.connect(self._filter_apps)
        search_layout.addWidget(self.search_entry)

        layout.addLayout(search_layout)

        # App list in scrollable area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.StyledPanel)

        self.app_list_widget = QWidget()
        self.app_list_layout = QVBoxLayout(self.app_list_widget)
        self.app_list_layout.setContentsMargins(0, 0, 0, 0)
        self.app_list_layout.setSpacing(2)

        scroll.setWidget(self.app_list_widget)
        layout.addWidget(scroll)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_button = QPushButton("Cancel")
        cancel_button.setObjectName("grayButton")
        cancel_button.setFixedWidth(100)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

    def _load_apps(self):
        """Load installed applications in background."""
        def load_thread():
            self.apps = AppFinder.find_installed_apps()
            self.filtered_apps = self.apps.copy()

            # Schedule UI update on main thread
            QTimer.singleShot(0, self._populate_list)

        threading.Thread(target=load_thread, daemon=True).start()

    def _populate_list(self):
        """Populate the app list with filtered results."""
        # Clear existing
        for i in reversed(range(self.app_list_layout.count())):
            widget = self.app_list_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Update status
        self.status_label.setText(f"{len(self.filtered_apps)} apps found")

        if not self.filtered_apps:
            no_apps_label = QLabel("No applications found" if not self.apps else "No matching applications")
            no_apps_label.setStyleSheet("color: gray;")
            no_apps_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.app_list_layout.addWidget(no_apps_label)
            self.app_list_layout.addStretch()
            return

        # Create app items (limit to 100 for performance)
        for app in self.filtered_apps[:100]:
            self._create_app_item(app)

        self.app_list_layout.addStretch()

    def _create_app_item(self, app: dict):
        """Create a single app list item."""
        item_frame = QFrame()
        item_frame.setFrameShape(QFrame.Shape.StyledPanel)
        item_layout = QHBoxLayout(item_frame)
        item_layout.setContentsMargins(10, 5, 10, 5)

        # App info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        name_label = QLabel(app["name"])
        name_label.setStyleSheet("font-weight: bold;")
        info_layout.addWidget(name_label)

        path_label = QLabel(app["path"])
        path_label.setStyleSheet("color: gray; font-size: 10px;")
        info_layout.addWidget(path_label)

        item_layout.addLayout(info_layout, stretch=1)

        # Select button
        select_button = QPushButton("Select")
        select_button.setFixedWidth(80)
        select_button.setFixedHeight(28)
        select_button.clicked.connect(lambda: self._select_app(app))
        item_layout.addWidget(select_button)

        self.app_list_layout.addWidget(item_frame)

    def _filter_apps(self):
        """Filter apps based on search query."""
        query = self.search_entry.text().lower()

        if not query:
            self.filtered_apps = self.apps.copy()
        else:
            self.filtered_apps = [
                app for app in self.apps
                if query in app["name"].lower() or query in app["path"].lower()
            ]

        self._populate_list()

    def _select_app(self, app: dict):
        """Handle app selection."""
        self.on_select(app["path"], app["name"])
        self.accept()


class AddAppDialog(QDialog):
    """Dialog for adding a new application."""

    def __init__(self, parent, on_add: Callable[[str, str, str, str], None]):
        """
        Initialize the Add App dialog.

        Args:
            parent: Parent window
            on_add: Callback function(name, path, arguments, working_dir) called when app is added
        """
        super().__init__(parent)

        self.on_add = on_add
        self.selected_path: Optional[str] = None

        # Window setup
        self.setWindowTitle("Add Application")
        self.setFixedSize(600, 300)
        self.setModal(True)
        self._set_icon()

        # Center on parent
        if parent:
            parent_geo = parent.geometry()
            self.move(
                parent_geo.x() + (parent_geo.width() - 600) // 2,
                parent_geo.y() + (parent_geo.height() - 300) // 2
            )

        self._create_widgets()

    def _set_icon(self):
        """Set dialog icon."""
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        icon_path = os.path.join(base_dir, "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def _create_widgets(self):
        """Create dialog widgets."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Path selection
        path_layout = QHBoxLayout()
        path_label = QLabel("Application:")
        path_label.setFixedWidth(80)
        path_layout.addWidget(path_label)

        self.path_entry = QLineEdit()
        self.path_entry.setReadOnly(True)
        self.path_entry.setMinimumWidth(200)
        path_layout.addWidget(self.path_entry, stretch=1)

        browse_button = QPushButton("Browse...")
        browse_button.setFixedWidth(85)
        browse_button.clicked.connect(self._browse_file)
        path_layout.addWidget(browse_button)

        search_button = QPushButton("Search...")
        search_button.setObjectName("launchButton")
        search_button.setFixedWidth(85)
        search_button.clicked.connect(self._search_installed_apps)
        path_layout.addWidget(search_button)

        layout.addLayout(path_layout)

        # Name input
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_label.setFixedWidth(80)
        name_layout.addWidget(name_label)

        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("Enter a display name")
        self.name_entry.setMinimumWidth(200)
        name_layout.addWidget(self.name_entry, stretch=1)

        layout.addLayout(name_layout)

        # Arguments input
        args_layout = QHBoxLayout()
        args_label = QLabel("Arguments:")
        args_label.setFixedWidth(80)
        args_layout.addWidget(args_label)

        self.args_entry = QLineEdit()
        self.args_entry.setPlaceholderText("Command-line arguments (optional)")
        self.args_entry.setMinimumWidth(200)
        args_layout.addWidget(self.args_entry, stretch=1)

        layout.addLayout(args_layout)

        # Working directory input
        workdir_layout = QHBoxLayout()
        workdir_label = QLabel("Working Dir:")
        workdir_label.setFixedWidth(80)
        workdir_layout.addWidget(workdir_label)

        self.workdir_entry = QLineEdit()
        self.workdir_entry.setPlaceholderText("Working directory (optional)")
        self.workdir_entry.setMinimumWidth(200)
        workdir_layout.addWidget(self.workdir_entry, stretch=1)

        layout.addLayout(workdir_layout)

        layout.addSpacing(20)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        add_button = QPushButton("Add")
        add_button.setFixedWidth(100)
        add_button.clicked.connect(self._on_add_click)
        button_layout.addWidget(add_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.setObjectName("grayButton")
        cancel_button.setFixedWidth(100)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

    def _browse_file(self):
        """Open file browser to select an application."""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Application",
            "",
            "Executables (*.exe);;Batch files (*.bat *.cmd);;Shortcuts (*.lnk);;All files (*.*)"
        )

        if path:
            self._set_selected_app(path)

    def _search_installed_apps(self):
        """Show dialog to search for installed applications."""
        dialog = SearchAppsDialog(self, on_select=self._set_selected_app)
        dialog.exec()

    def _set_selected_app(self, path: str, name: str = ""):
        """Set the selected application path and name."""
        self.selected_path = path
        self.path_entry.setText(path)

        # Auto-fill name from filename if empty or use provided name
        if not self.name_entry.text():
            if name:
                self.name_entry.setText(name)
            else:
                filename = os.path.splitext(os.path.basename(path))[0]
                self.name_entry.setText(filename)

    def _on_add_click(self):
        """Handle Add button click."""
        name = self.name_entry.text().strip()
        path = self.selected_path
        arguments = self.args_entry.text().strip()
        working_dir = self.workdir_entry.text().strip()

        if not path:
            self._show_error("Please select an application file.")
            return

        if not name:
            self._show_error("Please enter a name for the application.")
            return

        self.on_add(name, path, arguments, working_dir)
        self.accept()

    def _show_error(self, message: str):
        """Show error message dialog."""
        error_dialog = QDialog(self)
        error_dialog.setWindowTitle("Error")
        error_dialog.setFixedSize(300, 100)
        error_dialog.setModal(True)

        layout = QVBoxLayout(error_dialog)
        layout.setContentsMargins(20, 20, 20, 20)

        label = QLabel(message)
        label.setWordWrap(True)
        layout.addWidget(label)

        ok_button = QPushButton("OK")
        ok_button.setFixedWidth(80)
        ok_button.clicked.connect(error_dialog.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

        error_dialog.exec()
