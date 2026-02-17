"""Windows file association management for .favapp files."""

import os
import sys
import winreg
from typing import Optional


class FileAssociation:
    """Manages Windows file associations for .favapp files."""

    EXTENSION = ".favapp"
    PROG_ID = "FavAppStarter.Profile"
    FILE_TYPE_NAME = "FavApp Profile"

    @staticmethod
    def get_executable_path() -> str:
        """Get the path to the FavApp Starter executable."""
        if getattr(sys, 'frozen', False):
            # Running as .exe
            return sys.executable
        else:
            # Running from source - return path to main.py
            # This won't work for association, but useful for development
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(base_dir, "main.py")

    @classmethod
    def is_registered(cls) -> bool:
        """Check if .favapp extension is registered."""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, rf"Software\Classes\{cls.EXTENSION}", 0, winreg.KEY_READ) as key:
                prog_id, _ = winreg.QueryValueEx(key, "")
                return prog_id == cls.PROG_ID
        except WindowsError:
            return False

    @classmethod
    def register(cls, icon_path: Optional[str] = None) -> bool:
        """
        Register .favapp file extension with Windows.

        Args:
            icon_path: Optional path to icon file. If None, uses executable icon.

        Returns:
            True if successful, False otherwise
        """
        try:
            exe_path = cls.get_executable_path()

            # Use executable icon if no custom icon provided
            if icon_path is None:
                if getattr(sys, 'frozen', False):
                    icon_path = exe_path
                else:
                    # Use icon.ico from assets folder
                    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    icon_path = os.path.join(base_dir, "assets", "icon.ico")

            # Register file extension -> ProgID
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, rf"Software\Classes\{cls.EXTENSION}") as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, cls.PROG_ID)

            # Register ProgID
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, rf"Software\Classes\{cls.PROG_ID}") as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, cls.FILE_TYPE_NAME)

            # Set icon
            if os.path.exists(icon_path):
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, rf"Software\Classes\{cls.PROG_ID}\DefaultIcon") as key:
                    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{icon_path}",0')

            # Register shell open command
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, rf"Software\Classes\{cls.PROG_ID}\shell\open\command") as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{exe_path}" "%1"')

            # Notify Windows of the change
            cls._notify_shell()

            return True
        except Exception:
            return False

    @classmethod
    def unregister(cls) -> bool:
        """
        Unregister .favapp file extension.

        Returns:
            True if successful, False otherwise
        """
        try:
            # Remove extension key
            try:
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, rf"Software\Classes\{cls.EXTENSION}")
            except WindowsError:
                pass

            # Remove ProgID keys
            try:
                # Remove command
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, rf"Software\Classes\{cls.PROG_ID}\shell\open\command")
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, rf"Software\Classes\{cls.PROG_ID}\shell\open")
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, rf"Software\Classes\{cls.PROG_ID}\shell")
            except WindowsError:
                pass

            try:
                # Remove icon
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, rf"Software\Classes\{cls.PROG_ID}\DefaultIcon")
            except WindowsError:
                pass

            try:
                # Remove ProgID
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, rf"Software\Classes\{cls.PROG_ID}")
            except WindowsError:
                pass

            # Notify Windows of the change
            cls._notify_shell()

            return True
        except Exception:
            return False

    @staticmethod
    def _notify_shell():
        """Notify Windows shell of file association changes."""
        try:
            import ctypes
            # SHChangeNotify with SHCNE_ASSOCCHANGED
            ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
        except Exception:
            pass
