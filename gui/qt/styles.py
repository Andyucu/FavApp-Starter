"""Theme and stylesheet management for PyQt6 FavApp Starter."""


class StyleManager:
    """Centralized theme and stylesheet management."""

    @staticmethod
    def get_stylesheet(theme: str) -> str:
        """
        Get complete application stylesheet for the specified theme.

        Args:
            theme: "dark", "light", or "system"

        Returns:
            Complete QSS stylesheet string
        """
        if theme == "system":
            theme = StyleManager._detect_system_theme()

        return StyleManager._dark_theme() if theme == "dark" else StyleManager._light_theme()

    @staticmethod
    def _detect_system_theme() -> str:
        """
        Detect Windows system theme preference.

        Returns:
            "dark" or "light" based on Windows settings
        """
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return "light" if value == 1 else "dark"
        except Exception:
            return "dark"  # Default to dark if detection fails

    @staticmethod
    def _dark_theme() -> str:
        """Dark theme stylesheet matching CustomTkinter appearance."""
        return """
        /* Global Styles */
        QMainWindow, QDialog, QWidget {
            background-color: #1a1a1a;
            color: #dcdcdc;
            font-family: 'Roboto', 'Segoe UI', sans-serif;
            font-size: 13px;
        }

        /* Buttons */
        QPushButton {
            background-color: #1f538d;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 15px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #2563a8;
        }

        QPushButton:pressed {
            background-color: #144e7a;
        }

        QPushButton:disabled {
            background-color: #3a3a3a;
            color: #6a6a6a;
        }

        /* Green buttons (Save, Launch) */
        QPushButton#saveButton, QPushButton#launchButton {
            background-color: #2fa572;
        }

        QPushButton#saveButton:hover, QPushButton#launchButton:hover {
            background-color: #28a164;
        }

        QPushButton#saveButton:pressed, QPushButton#launchButton:pressed {
            background-color: #1e7a4f;
        }

        /* Red buttons (Delete) */
        QPushButton#deleteButton {
            background-color: #d9534f;
        }

        QPushButton#deleteButton:hover {
            background-color: #c9302c;
        }

        QPushButton#deleteButton:pressed {
            background-color: #b52b27;
        }

        /* Gray buttons (Cancel, Remove) */
        QPushButton#grayButton {
            background-color: #4a4a4a;
        }

        QPushButton#grayButton:hover {
            background-color: #5a5a5a;
        }

        /* Text Input */
        QLineEdit {
            background-color: #2a2a2a;
            color: #dcdcdc;
            border: 2px solid #3a3a3a;
            border-radius: 6px;
            padding: 8px;
            selection-background-color: #1f538d;
        }

        QLineEdit:focus {
            border-color: #1f538d;
        }

        QLineEdit:disabled {
            background-color: #1a1a1a;
            color: #6a6a6a;
        }

        /* Text Edit (Multi-line) */
        QTextEdit, QPlainTextEdit {
            background-color: #2a2a2a;
            color: #dcdcdc;
            border: 2px solid #3a3a3a;
            border-radius: 6px;
            padding: 8px;
            selection-background-color: #1f538d;
        }

        QTextEdit:focus, QPlainTextEdit:focus {
            border-color: #1f538d;
        }

        /* Combo Box (Dropdown) */
        QComboBox {
            background-color: #2a2a2a;
            color: #dcdcdc;
            border: 2px solid #3a3a3a;
            border-radius: 6px;
            padding: 8px;
            padding-right: 30px;
        }

        QComboBox:hover {
            border-color: #4a4a4a;
        }

        QComboBox:focus {
            border-color: #1f538d;
        }

        QComboBox::drop-down {
            border: none;
            width: 30px;
        }

        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #dcdcdc;
            margin-right: 10px;
        }

        QComboBox QAbstractItemView {
            background-color: #2a2a2a;
            color: #dcdcdc;
            border: 2px solid #3a3a3a;
            selection-background-color: #1f538d;
            selection-color: white;
            outline: none;
        }

        /* Checkboxes */
        QCheckBox {
            color: #dcdcdc;
            spacing: 8px;
        }

        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 2px solid #3a3a3a;
            background-color: #2a2a2a;
        }

        QCheckBox::indicator:hover {
            border-color: #4a4a4a;
        }

        QCheckBox::indicator:checked {
            background-color: #1f538d;
            border-color: #1f538d;
        }

        QCheckBox::indicator:checked:hover {
            background-color: #2563a8;
            border-color: #2563a8;
        }

        QCheckBox::indicator:disabled {
            background-color: #1a1a1a;
            border-color: #2a2a2a;
        }

        /* Scrollbars */
        QScrollArea {
            border: none;
            background-color: transparent;
        }

        QScrollBar:vertical {
            background-color: #2a2a2a;
            width: 14px;
            border-radius: 7px;
            margin: 0px;
        }

        QScrollBar::handle:vertical {
            background-color: #4a4a4a;
            border-radius: 7px;
            min-height: 30px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: #5a5a5a;
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }

        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }

        QScrollBar:horizontal {
            background-color: #2a2a2a;
            height: 14px;
            border-radius: 7px;
            margin: 0px;
        }

        QScrollBar::handle:horizontal {
            background-color: #4a4a4a;
            border-radius: 7px;
            min-width: 30px;
        }

        QScrollBar::handle:horizontal:hover {
            background-color: #5a5a5a;
        }

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }

        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }

        /* Labels */
        QLabel {
            color: #dcdcdc;
            background-color: transparent;
        }

        QLabel#statusLabel {
            color: #8a8a8a;
            font-size: 10px;
            font-weight: bold;
        }

        QLabel#grayLabel {
            color: #8a8a8a;
        }

        QLabel#headerLabel {
            font-size: 20px;
            font-weight: bold;
        }

        /* Spin Box */
        QSpinBox {
            background-color: #2a2a2a;
            color: #dcdcdc;
            border: 2px solid #3a3a3a;
            border-radius: 6px;
            padding: 8px;
        }

        QSpinBox:focus {
            border-color: #1f538d;
        }

        QSpinBox::up-button, QSpinBox::down-button {
            background-color: #3a3a3a;
            border: none;
            width: 20px;
        }

        QSpinBox::up-button:hover, QSpinBox::down-button:hover {
            background-color: #4a4a4a;
        }

        /* Menu Bar */
        QMenuBar {
            background-color: #1a1a1a;
            color: #dcdcdc;
            border-bottom: 1px solid #2a2a2a;
        }

        QMenuBar::item {
            padding: 8px 12px;
            background-color: transparent;
        }

        QMenuBar::item:selected {
            background-color: #2a2a2a;
        }

        QMenuBar::item:pressed {
            background-color: #1f538d;
        }

        /* Menus */
        QMenu {
            background-color: #2a2a2a;
            color: #dcdcdc;
            border: 1px solid #3a3a3a;
            padding: 4px;
        }

        QMenu::item {
            padding: 8px 30px 8px 10px;
            border-radius: 4px;
        }

        QMenu::item:selected {
            background-color: #1f538d;
        }

        QMenu::separator {
            height: 1px;
            background-color: #3a3a3a;
            margin: 4px 0px;
        }

        /* Frames */
        QFrame {
            border: none;
            background-color: transparent;
        }

        QFrame#borderFrame {
            border: 2px solid #3a3a3a;
            border-radius: 6px;
        }

        /* Status Bar */
        QStatusBar {
            background-color: #1a1a1a;
            color: #8a8a8a;
            border-top: 1px solid #2a2a2a;
        }

        /* Tool Tips */
        QToolTip {
            background-color: #2a2a2a;
            color: #dcdcdc;
            border: 1px solid #3a3a3a;
            padding: 6px;
            border-radius: 4px;
        }
        """

    @staticmethod
    def _light_theme() -> str:
        """Light theme stylesheet."""
        return """
        /* Global Styles */
        QMainWindow, QDialog, QWidget {
            background-color: #f0f0f0;
            color: #2a2a2a;
            font-family: 'Roboto', 'Segoe UI', sans-serif;
            font-size: 13px;
        }

        /* Buttons */
        QPushButton {
            background-color: #1f538d;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 15px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #2563a8;
        }

        QPushButton:pressed {
            background-color: #144e7a;
        }

        QPushButton:disabled {
            background-color: #d0d0d0;
            color: #8a8a8a;
        }

        /* Green buttons */
        QPushButton#saveButton, QPushButton#launchButton {
            background-color: #2fa572;
        }

        QPushButton#saveButton:hover, QPushButton#launchButton:hover {
            background-color: #28a164;
        }

        /* Red buttons */
        QPushButton#deleteButton {
            background-color: #d9534f;
        }

        QPushButton#deleteButton:hover {
            background-color: #c9302c;
        }

        /* Gray buttons */
        QPushButton#grayButton {
            background-color: #b0b0b0;
        }

        QPushButton#grayButton:hover {
            background-color: #a0a0a0;
        }

        /* Text Input */
        QLineEdit {
            background-color: white;
            color: #2a2a2a;
            border: 2px solid #d0d0d0;
            border-radius: 6px;
            padding: 8px;
            selection-background-color: #1f538d;
        }

        QLineEdit:focus {
            border-color: #1f538d;
        }

        /* Text Edit */
        QTextEdit, QPlainTextEdit {
            background-color: white;
            color: #2a2a2a;
            border: 2px solid #d0d0d0;
            border-radius: 6px;
            padding: 8px;
        }

        /* Combo Box */
        QComboBox {
            background-color: white;
            color: #2a2a2a;
            border: 2px solid #d0d0d0;
            border-radius: 6px;
            padding: 8px;
            padding-right: 30px;
        }

        QComboBox::down-arrow {
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #2a2a2a;
            margin-right: 10px;
        }

        QComboBox QAbstractItemView {
            background-color: white;
            color: #2a2a2a;
            border: 2px solid #d0d0d0;
            selection-background-color: #1f538d;
            selection-color: white;
        }

        /* Checkboxes */
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 2px solid #d0d0d0;
            background-color: white;
        }

        QCheckBox::indicator:checked {
            background-color: #1f538d;
            border-color: #1f538d;
        }

        /* Scrollbars */
        QScrollBar:vertical {
            background-color: #e0e0e0;
            width: 14px;
            border-radius: 7px;
        }

        QScrollBar::handle:vertical {
            background-color: #b0b0b0;
            border-radius: 7px;
            min-height: 30px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: #a0a0a0;
        }

        /* Labels */
        QLabel#statusLabel {
            color: #6a6a6a;
            font-size: 10px;
            font-weight: bold;
        }

        QLabel#grayLabel {
            color: #6a6a6a;
        }

        /* Menu Bar */
        QMenuBar {
            background-color: #f0f0f0;
            color: #2a2a2a;
            border-bottom: 1px solid #d0d0d0;
        }

        QMenuBar::item:selected {
            background-color: #e0e0e0;
        }

        /* Menus */
        QMenu {
            background-color: white;
            color: #2a2a2a;
            border: 1px solid #d0d0d0;
        }

        QMenu::item:selected {
            background-color: #1f538d;
            color: white;
        }

        /* Status Bar */
        QStatusBar {
            background-color: #f0f0f0;
            color: #6a6a6a;
            border-top: 1px solid #d0d0d0;
        }
        """
