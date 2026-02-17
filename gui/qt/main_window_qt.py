"""PyQt6 main window for FavApp Starter."""

import os
import sys
import threading
from datetime import datetime
from typing import Optional
from PIL import Image
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QLineEdit, QScrollArea, QCheckBox, QFrame, QMenuBar, QMenu,
    QSystemTrayIcon
)
from PyQt6.QtGui import QIcon, QPixmap, QImage, QAction, QShortcut, QKeySequence, QPainter, QColor, QPen
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QEvent, QSize

from core.config import ConfigManager
from core.launcher import AppLauncher, IconExtractor
from .dialogs_qt import (
    ConfirmDialog, AddProfileDialog, AboutDialog, LicenseDialog,
    EditAppDialog, OptionsDialog, SearchAppsDialog, AddAppDialog
)
from .styles import StyleManager


class MainWindow(QMainWindow):
    """Main application window using PyQt6."""

    APP_VERSION = "26.2.2"
    APP_AUTHOR = "Alexandru Teodorovici"

    def __init__(self, config: ConfigManager):
        """
        Initialize the main window.

        Args:
            config: ConfigManager instance
        """
        super().__init__()

        self.config = config
        self.icon_cache = {}
        self.app_items = []
        self.tray_icon = None

        # Setup window
        self._setup_window()
        self._set_icon()

        # Create menu bar
        self._create_menu()

        # Create main UI
        self._create_main_ui()

        # Bind shortcuts
        self._bind_shortcuts()

        # Load initial data
        self._refresh_profile_list()
        self._refresh_app_list()

        # Restore window geometry
        self._restore_geometry()

        # Create system tray icon immediately
        QTimer.singleShot(100, self._init_tray_icon)

        # Start minimized if configured
        if self.config.get_setting("start_minimized", False):
            QTimer.singleShot(200, self._minimize_to_tray)

    @staticmethod
    def _create_button_icon(icon_type: str, size: int = 24) -> QIcon:
        """
        Create a simple icon with proper aspect ratio.

        Args:
            icon_type: Type of icon ('add', 'save', 'duplicate', 'delete', 'edit')
            size: Icon size in pixels (will be square)

        Returns:
            QIcon with proper aspect ratio
        """
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set color based on icon type
        # Save and delete use black icons (buttons have colored backgrounds)
        if icon_type in ['save', 'delete']:
            color = QColor(0, 0, 0)  # Black for visibility on colored buttons
        else:
            color = QColor(255, 255, 255)  # White for other buttons

        pen = QPen(color)
        pen.setWidth(3)  # Increased from 2 to 3 for better visibility
        painter.setPen(pen)
        painter.setBrush(color)  # Fill shapes for better visibility

        center = size // 2
        margin = 4

        if icon_type == 'add':
            # Plus sign - bold lines
            pen.setWidth(4)
            painter.setPen(pen)
            painter.drawLine(center, margin + 2, center, size - margin - 2)
            painter.drawLine(margin + 2, center, size - margin - 2, center)
        elif icon_type == 'save':
            # Checkmark - simple and highly visible
            pen.setWidth(4)
            painter.setPen(pen)
            painter.setBrush(Qt.GlobalColor.transparent)
            # Draw checkmark
            painter.drawLine(margin + 2, center, center - 1, size - margin - 3)
            painter.drawLine(center - 1, size - margin - 3, size - margin - 2, margin + 3)
        elif icon_type == 'duplicate':
            # Two overlapping rectangles - bold
            pen.setWidth(3)
            painter.setPen(pen)
            painter.setBrush(Qt.GlobalColor.transparent)
            painter.drawRect(margin, margin + 4, size - margin * 2 - 4, size - margin * 2 - 4)
            painter.drawRect(margin + 4, margin, size - margin * 2 - 4, size - margin * 2 - 4)
        elif icon_type == 'delete':
            # X mark - simple and highly visible
            pen.setWidth(4)
            painter.setPen(pen)
            painter.setBrush(Qt.GlobalColor.transparent)
            # Draw X
            painter.drawLine(margin + 3, margin + 3, size - margin - 3, size - margin - 3)
            painter.drawLine(size - margin - 3, margin + 3, margin + 3, size - margin - 3)
        elif icon_type == 'edit':
            # Pencil shape - bold diagonal line
            pen.setWidth(4)
            painter.setPen(pen)
            painter.drawLine(size - margin - 3, margin + 3, margin + 3, size - margin - 3)
            # Pencil tip
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawLine(size - margin - 6, margin + 3, size - margin - 3, margin + 6)
            painter.drawLine(margin + 3, size - margin - 3, margin + 6, size - margin - 6)

        painter.end()
        return QIcon(pixmap)

    def _setup_window(self):
        """Set up window properties."""
        self.setWindowTitle(f"FavApp Starter v{self.APP_VERSION}")
        self.setMinimumSize(450, 500)
        self.resize(550, 600)

    def _set_icon(self):
        """Set the application icon."""
        # Handle both running from source and from .exe
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        icon_paths = [
            os.path.join(base_dir, "assets", "icon.ico"),
            os.path.join(base_dir, "icon.ico"),
        ]

        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
                break

    def _create_menu(self):
        """Create the application menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        options_action = QAction("Options", self)
        options_action.setShortcut("Ctrl+,")
        options_action.triggered.connect(self._show_options)
        file_menu.addAction(options_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Profile menu
        profile_menu = menubar.addMenu("Profile")

        new_profile_action = QAction("New Profile", self)
        new_profile_action.setShortcut("Ctrl+N")
        new_profile_action.triggered.connect(self._show_add_profile_dialog)
        profile_menu.addAction(new_profile_action)

        duplicate_action = QAction("Duplicate Profile", self)
        duplicate_action.setShortcut("Ctrl+D")
        duplicate_action.triggered.connect(self._duplicate_profile)
        profile_menu.addAction(duplicate_action)

        rename_action = QAction("Rename Profile", self)
        rename_action.triggered.connect(self._rename_profile)
        profile_menu.addAction(rename_action)

        profile_menu.addSeparator()

        export_action = QAction("Export Profile...", self)
        export_action.triggered.connect(self._export_profile)
        profile_menu.addAction(export_action)

        export_all_action = QAction("Export All Profiles...", self)
        export_all_action.triggered.connect(self._export_all_profiles)
        profile_menu.addAction(export_all_action)

        import_action = QAction("Import Profiles...", self)
        import_action.triggered.connect(self._import_profiles)
        profile_menu.addAction(import_action)

        # About menu
        about_menu = menubar.addMenu("About")

        about_action = QAction("App Info", self)
        about_action.triggered.connect(self._show_about)
        about_menu.addAction(about_action)

    def _create_main_ui(self):
        """Create main UI."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 0)
        main_layout.setSpacing(15)

        # Header
        self._create_header(main_layout)

        # Profile section
        self._create_profile_section(main_layout)

        # Search bar
        self._create_search_bar(main_layout)

        # App list section
        self._create_app_list_section(main_layout)

        # Bottom section
        self._create_bottom_section(main_layout)

        # Status bar
        self._create_status_bar()

    def _create_header(self, layout):
        """Create header with title."""
        header_label = QLabel("FavApp Starter")
        header_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(header_label)

    def _create_profile_section(self, layout):
        """Create profile selection section."""
        profile_layout = QHBoxLayout()

        # Label
        profile_label = QLabel("Profile:")
        profile_label.setFixedWidth(60)
        profile_layout.addWidget(profile_label)

        # Profile dropdown
        self.profile_combo = QComboBox()
        self.profile_combo.setFixedWidth(200)
        self.profile_combo.currentTextChanged.connect(self._on_profile_change)
        profile_layout.addWidget(self.profile_combo)

        profile_layout.addSpacing(10)

        # Add profile button
        add_profile_btn = QPushButton()
        add_profile_btn.setIcon(self._create_button_icon('add', 24))
        add_profile_btn.setIconSize(QSize(24, 24))
        add_profile_btn.setFixedSize(40, 40)
        add_profile_btn.setToolTip("New Profile (Ctrl+N)")
        add_profile_btn.clicked.connect(self._show_add_profile_dialog)
        profile_layout.addWidget(add_profile_btn)

        # Save profile button
        save_profile_btn = QPushButton()
        save_profile_btn.setObjectName("launchButton")
        save_profile_btn.setIcon(self._create_button_icon('save', 24))
        save_profile_btn.setIconSize(QSize(24, 24))
        save_profile_btn.setFixedSize(40, 40)
        save_profile_btn.setToolTip("Save Profile")
        save_profile_btn.clicked.connect(self._save_profile)
        profile_layout.addWidget(save_profile_btn)

        # Duplicate profile button
        duplicate_profile_btn = QPushButton()
        duplicate_profile_btn.setIcon(self._create_button_icon('duplicate', 24))
        duplicate_profile_btn.setIconSize(QSize(24, 24))
        duplicate_profile_btn.setFixedSize(40, 40)
        duplicate_profile_btn.setToolTip("Duplicate Profile (Ctrl+D)")
        duplicate_profile_btn.clicked.connect(self._duplicate_profile)
        profile_layout.addWidget(duplicate_profile_btn)

        # Delete profile button
        delete_profile_btn = QPushButton()
        delete_profile_btn.setObjectName("deleteButton")
        delete_profile_btn.setIcon(self._create_button_icon('delete', 24))
        delete_profile_btn.setIconSize(QSize(24, 24))
        delete_profile_btn.setFixedSize(40, 40)
        delete_profile_btn.setToolTip("Delete Profile")
        delete_profile_btn.clicked.connect(self._delete_profile)
        profile_layout.addWidget(delete_profile_btn)

        profile_layout.addStretch()

        layout.addLayout(profile_layout)

    def _create_search_bar(self, layout):
        """Create search/filter bar."""
        search_layout = QHBoxLayout()

        # Search icon
        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("font-size: 24px;")
        search_icon.setFixedWidth(30)
        search_layout.addWidget(search_icon)

        # Search entry
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Search apps...")
        self.search_entry.textChanged.connect(self._on_search_change)
        search_layout.addWidget(self.search_entry)

        layout.addLayout(search_layout)

    def _create_app_list_section(self, layout):
        """Create the application list section."""
        # Frame for the list
        list_frame = QFrame()
        list_frame.setFrameShape(QFrame.Shape.StyledPanel)
        list_layout = QVBoxLayout(list_frame)
        list_layout.setContentsMargins(10, 10, 10, 10)
        list_layout.setSpacing(5)

        # Label
        apps_label = QLabel("Applications:")
        apps_label.setStyleSheet("font-weight: bold;")
        list_layout.addWidget(apps_label)

        # Scrollable frame for apps
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.app_list_widget = QWidget()
        self.app_list_layout = QVBoxLayout(self.app_list_widget)
        self.app_list_layout.setContentsMargins(0, 0, 0, 0)
        self.app_list_layout.setSpacing(2)

        scroll.setWidget(self.app_list_widget)
        list_layout.addWidget(scroll)

        layout.addWidget(list_frame)

    def _create_bottom_section(self, layout):
        """Create bottom section with buttons."""
        # App management buttons
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        add_app_btn = QPushButton("Add App")
        add_app_btn.setFixedSize(130, 32)
        add_app_btn.setToolTip("Add Application (Ctrl+A)")
        add_app_btn.clicked.connect(self._show_add_app_dialog)
        button_layout.addWidget(add_app_btn)

        button_layout.addSpacing(10)

        self.remove_btn = QPushButton("Remove Selected")
        self.remove_btn.setObjectName("grayButton")
        self.remove_btn.setFixedSize(130, 32)
        self.remove_btn.setEnabled(False)
        self.remove_btn.setToolTip("Remove Selected Apps (Del)")
        self.remove_btn.clicked.connect(self._remove_selected_app)
        button_layout.addWidget(self.remove_btn)

        layout.addLayout(button_layout)

        layout.addSpacing(10)

        # Launch button
        launch_layout = QHBoxLayout()
        launch_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.launch_btn = QPushButton("▶  LAUNCH ALL")
        self.launch_btn.setObjectName("launchButton")
        self.launch_btn.setFixedSize(220, 45)
        self.launch_btn.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.launch_btn.setToolTip("Launch All Apps (Ctrl+L)")
        self.launch_btn.clicked.connect(self._launch_all)
        launch_layout.addWidget(self.launch_btn)

        layout.addLayout(launch_layout)

    def _create_status_bar(self):
        """Create status bar at bottom."""
        status_bar = self.statusBar()

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: gray; font-size: 10px; font-weight: bold;")
        status_bar.addWidget(self.status_label)

        # Show last launch time if available
        last_launch = self.config.get_setting("last_launch")
        if last_launch:
            try:
                dt = datetime.fromisoformat(last_launch)
                self.status_label.setText(f"Last launch: {dt.strftime('%Y-%m-%d %H:%M')}")
            except:
                pass

    def _refresh_profile_list(self):
        """Refresh the profile dropdown."""
        profiles = self.config.get_profiles()
        active_profile = self.config.get_active_profile()

        self.profile_combo.blockSignals(True)
        self.profile_combo.clear()
        self.profile_combo.addItems(profiles)
        self.profile_combo.setCurrentText(active_profile)
        self.profile_combo.blockSignals(False)

    def _refresh_app_list(self):
        """Refresh the application list."""
        # Clear existing items
        for item in self.app_items:
            item.deleteLater()
        self.app_items.clear()

        # Get apps for current profile
        apps = self.config.get_apps()

        # Apply search filter
        search_query = self.search_entry.text().lower()
        if search_query:
            apps = [app for app in apps if search_query in app.get("name", "").lower() or
                    search_query in app.get("path", "").lower()]

        if not apps:
            # Show empty state
            empty_text = "No matching apps found." if search_query else "No apps added yet.\nClick 'Add App' to get started."
            empty_label = QLabel(empty_text)
            empty_label.setStyleSheet("color: gray;")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.app_list_layout.addWidget(empty_label)
            self.app_items.append(empty_label)
            self.remove_btn.setEnabled(False)
            return

        # Create app items
        for i, app in enumerate(apps):
            item = self._create_app_item(i, app)
            self.app_items.append(item)
            self.app_list_layout.addWidget(item)

        self.app_list_layout.addStretch()

    def _create_app_item(self, index: int, app: dict) -> QFrame:
        """Create a single app item widget."""
        name = app.get("name", "Unknown")
        path = app.get("path", "")

        item_frame = QFrame()
        item_frame.setFrameShape(QFrame.Shape.StyledPanel)
        item_layout = QHBoxLayout(item_frame)
        item_layout.setContentsMargins(10, 8, 10, 8)
        item_layout.setSpacing(5)

        # Checkbox for selection
        checkbox = QCheckBox()
        checkbox.stateChanged.connect(self._update_remove_button)
        item_layout.addWidget(checkbox)

        # Store data on frame
        item_frame.checkbox = checkbox
        item_frame.app_index = index
        item_frame.app_data = app

        # App icon
        if self.config.get_setting("show_app_icons", True):
            icon_label = self._create_app_icon(path)
            item_layout.addWidget(icon_label)

        # App info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        name_label = QLabel(name)
        name_label.setStyleSheet("font-weight: bold;")
        name_label.setCursor(Qt.CursorShape.PointingHandCursor)
        name_label.setToolTip("Double-click to launch")
        name_label.mouseDoubleClickEvent = lambda e: self._launch_single_app(app)
        info_layout.addWidget(name_label)

        path_text = path
        if app.get("arguments"):
            path_text += f" {app['arguments']}"

        path_label = QLabel(path_text)
        path_label.setStyleSheet("color: gray; font-size: 11px;")
        info_layout.addWidget(path_label)

        item_layout.addLayout(info_layout, stretch=1)

        # Edit button
        edit_btn = QPushButton()
        edit_btn.setIcon(self._create_button_icon('edit', 24))
        edit_btn.setIconSize(QSize(24, 24))
        edit_btn.setFixedSize(35, 35)
        edit_btn.setToolTip("Edit App")
        edit_btn.clicked.connect(lambda: self._edit_app(index, app))
        item_layout.addWidget(edit_btn)

        return item_frame

    def _create_app_icon(self, path: str) -> QLabel:
        """Create app icon widget."""
        # Check cache
        cache_key = f"{path}_40x40"
        if cache_key in self.icon_cache:
            pixmap = self.icon_cache[cache_key]
        else:
            pil_image = None

            # Try to extract icon from the file
            try:
                # Extract icon
                pil_image = IconExtractor.get_icon(path, size=48)

                # Verify the image is valid
                if pil_image and pil_image.size[0] > 0 and pil_image.size[1] > 0:
                    pass  # Valid image
                else:
                    pil_image = None
            except:
                pil_image = None

            # If extraction failed, create a fallback icon
            if not pil_image:
                pil_image = Image.new('RGBA', (48, 48), (100, 149, 237, 255))
                from PIL import ImageDraw, ImageFont
                draw = ImageDraw.Draw(pil_image)
                try:
                    app_name = os.path.basename(path).split('.')[0]
                    letter = app_name[0].upper() if app_name else "?"
                    try:
                        font = ImageFont.truetype("arial.ttf", 32)
                    except:
                        font = ImageFont.load_default()
                    draw.text((24, 24), letter, fill=(255, 255, 255, 255), font=font, anchor="mm")
                except:
                    pass

            # Make the image square by cropping/padding to prevent compression
            width, height = pil_image.size
            if width != height:
                # Create a square canvas with the larger dimension
                size = max(width, height)
                square_image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
                # Paste the original image centered on the canvas
                x = (size - width) // 2
                y = (size - height) // 2
                square_image.paste(pil_image, (x, y))
                pil_image = square_image

            # Convert PIL Image to QPixmap
            # Calculate bytes per line for proper stride
            bytes_per_line = 4 * pil_image.width
            qimage = QImage(
                pil_image.tobytes(),
                pil_image.width,
                pil_image.height,
                bytes_per_line,
                QImage.Format.Format_RGBA8888
            )
            pixmap = QPixmap.fromImage(qimage)
            # Scale to exact size with smooth transformation
            pixmap = pixmap.scaled(
                40, 40,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.icon_cache[cache_key] = pixmap

        icon_label = QLabel()
        icon_label.setPixmap(pixmap)
        icon_label.setFixedSize(40, 40)
        return icon_label

    def _update_remove_button(self):
        """Update remove button state based on selection."""
        has_selection = any(
            hasattr(item, 'checkbox') and item.checkbox.isChecked()
            for item in self.app_items
        )
        self.remove_btn.setEnabled(has_selection)

    def _on_profile_change(self, profile_name: str):
        """Handle profile selection change."""
        if profile_name:
            self.config.set_active_profile(profile_name)
            self._refresh_app_list()

    def _on_search_change(self):
        """Handle search text change."""
        self._refresh_app_list()

    def _show_options(self):
        """Show the options dialog."""
        def on_theme_change(theme):
            # Apply theme
            from PyQt6.QtWidgets import QApplication
            app = QApplication.instance()
            stylesheet = StyleManager.get_stylesheet(theme)
            app.setStyleSheet(stylesheet)

        dialog = OptionsDialog(self, self.config, on_theme_change)
        dialog.exec()

    def _show_about(self):
        """Show the about dialog."""
        dialog = AboutDialog(self, self.APP_VERSION, self.APP_AUTHOR)
        dialog.exec()

    def _show_add_profile_dialog(self):
        """Show dialog to add a new profile."""
        dialog = AddProfileDialog(self, self.config.get_profiles())
        if dialog.exec() and dialog.profile_name:
            self._add_profile(dialog.profile_name)

    def _add_profile(self, name: str):
        """Add a new profile."""
        if self.config.add_profile(name):
            self.config.set_active_profile(name)
            self._refresh_profile_list()
            self._refresh_app_list()
            self._refresh_tray_menu()

    def _save_profile(self):
        """Manually save the current profile configuration."""
        try:
            self.config.save()
            self.status_label.setText("✓ Profile saved successfully")
            QTimer.singleShot(2000, lambda: self.status_label.setText(f"FavApp Starter v{self.APP_VERSION}"))
        except Exception as e:
            self._show_message("Save Error", f"Failed to save profile: {str(e)}")

    def _delete_profile(self):
        """Delete the current profile."""
        profile = self.config.get_active_profile()

        if len(self.config.get_profiles()) <= 1:
            self._show_message("Cannot Delete", "You cannot delete the last profile.")
            return

        dialog = ConfirmDialog(
            self,
            "Delete Profile",
            f"Are you sure you want to delete the profile '{profile}'?\nAll apps in this profile will be removed."
        )
        if dialog.exec() and dialog.confirmed:
            if self.config.delete_profile(profile):
                self._refresh_profile_list()
                self._refresh_app_list()
                self._refresh_tray_menu()

    def _duplicate_profile(self):
        """Duplicate the current profile."""
        current_profile = self.config.get_active_profile()
        new_name = f"{current_profile} (Copy)"

        # Find unique name
        counter = 2
        while new_name in self.config.get_profiles():
            new_name = f"{current_profile} (Copy {counter})"
            counter += 1

        if self.config.duplicate_profile(current_profile, new_name):
            self.config.set_active_profile(new_name)
            self._refresh_profile_list()
            self._refresh_app_list()
            self._refresh_tray_menu()

    def _rename_profile(self):
        """Rename the current profile."""
        # Placeholder - would use InputDialog
        pass

    def _export_profile(self):
        """Export current profile as .favapp file."""
        from PyQt6.QtWidgets import QFileDialog

        profile_name = self.config.get_active_profile()
        default_filename = f"{profile_name}.favapp"

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Profile",
            default_filename,
            "FavApp Profile Files (*.favapp);;All Files (*)"
        )

        if filename:
            if not filename.lower().endswith('.favapp'):
                filename += '.favapp'

            if self.config.export_profile(profile_name, filename):
                self.status_label.setText(f"Exported: {profile_name}")
            else:
                self.status_label.setText(f"Failed to export: {profile_name}")

    def _export_all_profiles(self):
        """Export all profiles to a single file."""
        from PyQt6.QtWidgets import QFileDialog

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export All Profiles",
            "FavApp_Profiles.json",
            "JSON Files (*.json);;All Files (*)"
        )

        if filename:
            if self.config.export_all_profiles(filename):
                count = len(self.config.get_profiles())
                self.status_label.setText(f"Exported {count} profile(s)")
            else:
                self.status_label.setText("Failed to export profiles")

    def _import_profiles(self):
        """Import profiles from file (.favapp or .json)."""
        from PyQt6.QtWidgets import QFileDialog

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Import Profile(s)",
            "",
            "FavApp Files (*.favapp *.json);;All Files (*)"
        )

        if filename:
            success = False
            if filename.lower().endswith('.favapp'):
                # Import single profile
                success = self.config.import_profile_from_file(filename)
                if success:
                    self._refresh_profile_list()
                    self.status_label.setText("Profile imported successfully")
                else:
                    self.status_label.setText("Failed to import profile")
            elif filename.lower().endswith('.json'):
                # Import multiple profiles
                try:
                    import json
                    with open(filename, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    count = self.config.import_all_profiles(data, replace=False)
                    if count > 0:
                        self._refresh_profile_list()
                        self.status_label.setText(f"Imported {count} profile(s)")
                        success = True
                    else:
                        self.status_label.setText("No profiles imported")
                except Exception:
                    self.status_label.setText("Failed to import profiles")
            else:
                self.status_label.setText("Unsupported file format")

    def _show_add_app_dialog(self):
        """Show dialog to add a new app."""
        def on_add(name, path, arguments, working_dir):
            self._add_app(name, path, arguments, working_dir)

        dialog = AddAppDialog(self, on_add)
        dialog.exec()

    def _add_app(self, name: str, path: str, arguments: str = "", working_dir: str = ""):
        """Add a new app to the current profile."""
        if self.config.add_app(name, path, arguments, working_dir):
            self._refresh_app_list()
            self.status_label.setText(f"Added: {name}")

    def _remove_selected_app(self):
        """Remove selected apps from the current profile."""
        # Get selected indices in reverse order
        selected_indices = sorted(
            [item.app_index for item in self.app_items if hasattr(item, 'checkbox') and item.checkbox.isChecked()],
            reverse=True
        )

        if not selected_indices:
            return

        # Confirm deletion
        count = len(selected_indices)
        message = f"Are you sure you want to remove {count} app(s)?"

        dialog = ConfirmDialog(self, "Remove Apps", message)
        if dialog.exec() and dialog.confirmed:
            for index in selected_indices:
                self.config.remove_app(index)

            self._refresh_app_list()
            self.status_label.setText(f"Removed {count} app(s)")

    def _edit_app(self, index: int, app_data: dict):
        """Show edit dialog for an app."""
        def on_save(name: str, path: str, arguments: str, working_dir: str):
            if self.config.update_app(index, name, path, arguments, working_dir):
                self._refresh_app_list()
                self.status_label.setText(f"Updated: {name}")

        dialog = EditAppDialog(self, app_data, on_save)
        dialog.exec()

    def _launch_single_app(self, app: dict):
        """Launch a single application."""
        name = app.get("name", "Unknown")
        path = app.get("path", "")
        arguments = app.get("arguments", "")
        working_dir = app.get("working_dir", "")

        self.status_label.setText(f"Launching {name}...")

        success, error = AppLauncher.launch_app(path, arguments, working_dir)

        if success:
            self.status_label.setText(f"Launched: {name}")
        else:
            self.status_label.setText(f"Failed to launch: {name}")
            self._show_message("Launch Error", f"Failed to launch {name}:\n\n{error}")

    def _launch_all(self):
        """Launch all apps in the current profile."""
        apps = self.config.get_apps()

        if not apps:
            self._show_message("No Apps", "There are no apps to launch in the current profile.")
            return

        self.launch_btn.setText("Launching...")
        self.launch_btn.setEnabled(False)
        self.status_label.setText(f"Launching {len(apps)} apps...")

        def launch_thread():
            launch_delay = self.config.get_setting("launch_delay", 0)
            failed = []

            for i, app in enumerate(apps):
                name = app.get("name", "Unknown")
                path = app.get("path", "")
                arguments = app.get("arguments", "")
                working_dir = app.get("working_dir", "")

                success, error = AppLauncher.launch_app(path, arguments, working_dir)

                if not success:
                    failed.append(f"{name}: {error}")

                # Delay between launches
                if i < len(apps) - 1 and launch_delay > 0:
                    import time
                    time.sleep(launch_delay / 1000.0)

            # Save last launch time
            self.config.set_setting("last_launch", datetime.now().isoformat())

            # Update UI on main thread
            def update_ui():
                self.launch_btn.setEnabled(True)

                if failed:
                    self.launch_btn.setText("▶  LAUNCH ALL")
                    self.status_label.setText(f"Failed to launch {len(failed)} app(s)")
                    self._show_message("Launch Errors", "\n".join(failed))
                else:
                    self.launch_btn.setText("✓ Launched!")
                    self.launch_btn.setStyleSheet("background-color: #1e7a4f; font-size: 14px; font-weight: bold;")
                    last_launch_time = datetime.now().strftime('%Y-%m-%d %H:%M')
                    self.status_label.setText(f"Last launch: {last_launch_time}")

                    QTimer.singleShot(1500, lambda: self.launch_btn.setText("▶  LAUNCH ALL"))
                    QTimer.singleShot(1500, lambda: self.launch_btn.setStyleSheet("font-size: 14px; font-weight: bold;"))

            QTimer.singleShot(0, update_ui)

        # Run in thread to avoid blocking UI
        threading.Thread(target=launch_thread, daemon=True).start()

    def _show_message(self, title: str, message: str):
        """Show a message dialog."""
        from PyQt6.QtWidgets import QMessageBox
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.exec()

    def _bind_shortcuts(self):
        """Bind keyboard shortcuts."""
        QShortcut(QKeySequence("Ctrl+Q"), self).activated.connect(self.close)
        QShortcut(QKeySequence("Ctrl+A"), self).activated.connect(self._show_add_app_dialog)
        QShortcut(QKeySequence("Ctrl+N"), self).activated.connect(self._show_add_profile_dialog)
        QShortcut(QKeySequence("Ctrl+D"), self).activated.connect(self._duplicate_profile)
        QShortcut(QKeySequence("Ctrl+L"), self).activated.connect(self._launch_all)
        QShortcut(QKeySequence("Ctrl+,"), self).activated.connect(self._show_options)
        QShortcut(QKeySequence("Delete"), self).activated.connect(self._remove_selected_app)

    def _restore_geometry(self):
        """Restore window position and size from config."""
        window_config = self.config.get_setting("window", {})

        x = window_config.get("x")
        y = window_config.get("y")
        width = window_config.get("width", 550)
        height = window_config.get("height", 600)

        if x is not None and y is not None:
            self.move(x, y)

        self.resize(width, height)

    def _init_tray_icon(self):
        """Initialize system tray icon at startup."""
        try:
            self._create_tray_icon()
        except Exception as e:
            print(f"ERROR: Failed to create tray icon: {e}")

    def _create_tray_icon(self):
        """Create system tray icon."""
        if self.tray_icon:
            return

        # Load icon
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        icon_path = os.path.join(base_dir, "assets", "icon.ico")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(base_dir, "icon.ico")

        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
        else:
            # Fallback icon
            icon = QIcon()

        # Create tray icon
        self.tray_icon = QSystemTrayIcon(icon, self)
        self.tray_icon.setToolTip("FavApp Starter")

        # Create tray menu
        self._create_tray_menu()

        # Connect signals
        self.tray_icon.activated.connect(self._on_tray_activated)

        # Show tray icon
        self.tray_icon.show()

    def _create_tray_menu(self):
        """Create or update the tray icon menu."""
        if not self.tray_icon:
            return

        menu = QMenu()

        # Show action
        show_action = QAction("Show", self)
        show_action.triggered.connect(self._show_from_tray)
        menu.addAction(show_action)

        menu.addSeparator()

        # Profile submenu
        profiles = self.config.get_profiles()
        if profiles:
            profile_menu = menu.addMenu("Launch Profiles")
            for profile_name in sorted(profiles):
                action = QAction(profile_name, self)
                action.triggered.connect(lambda checked, p=profile_name: self._launch_profile_from_tray(p))
                profile_menu.addAction(action)

            menu.addSeparator()

        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self._exit_from_tray)
        menu.addAction(exit_action)

        self.tray_icon.setContextMenu(menu)

    def _refresh_tray_menu(self):
        """Refresh the tray icon menu with updated profiles."""
        if self.tray_icon:
            self._create_tray_menu()

    def _on_tray_activated(self, reason):
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self._show_from_tray()

    def _show_from_tray(self):
        """Show window from tray."""
        self.show()
        self.activateWindow()
        self.raise_()

    def _minimize_to_tray(self):
        """Minimize window to system tray."""
        if self.config.get_setting("minimize_to_tray", True) and self.tray_icon:
            self.hide()
        else:
            self.showMinimized()

    def _launch_profile_from_tray(self, profile_name: str):
        """Launch all apps in a profile from the tray."""
        # Temporarily switch to the profile
        original_profile = self.config.get_active_profile()
        self.config.set_active_profile(profile_name)

        # Get apps for this profile
        apps = self.config.get_apps()

        # Switch back to original profile
        self.config.set_active_profile(original_profile)

        if not apps:
            return

        # Show notification
        if self.tray_icon:
            self.tray_icon.showMessage(
                "FavApp Starter",
                f"Launching {len(apps)} app(s) from profile '{profile_name}'...",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )

        # Launch apps in background
        def launch_thread():
            launch_delay = self.config.get_setting("launch_delay", 0)

            for i, app in enumerate(apps):
                path = app.get("path", "")
                arguments = app.get("arguments", "")
                working_dir = app.get("working_dir", "")

                AppLauncher.launch_app(path, arguments, working_dir)

                # Delay between launches
                if i < len(apps) - 1 and launch_delay > 0:
                    import time
                    time.sleep(launch_delay / 1000.0)

        threading.Thread(target=launch_thread, daemon=True).start()

    def _exit_from_tray(self):
        """Exit application from tray."""
        if self.tray_icon:
            self.tray_icon.hide()
        self.close()

    def changeEvent(self, event):
        """Handle window state changes."""
        if event.type() == QEvent.Type.WindowStateChange:
            if self.isMinimized():
                # Window was minimized
                if self.config.get_setting("minimize_to_tray", True):
                    QTimer.singleShot(0, self._minimize_to_tray)
        super().changeEvent(event)

    def closeEvent(self, event):
        """Handle window close event."""
        # Save window geometry
        pos = self.pos()
        size = self.size()

        self.config.set_setting("window", {
            "x": pos.x(),
            "y": pos.y(),
            "width": size.width(),
            "height": size.height()
        })

        event.accept()
