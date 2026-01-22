"""Windows auto-start functionality."""

import os
import sys
import winreg


class AutoStart:
    """Manage Windows auto-start for the application."""

    APP_NAME = "FavApp Starter"
    REG_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

    @staticmethod
    def is_enabled() -> bool:
        """Check if auto-start is enabled."""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, AutoStart.REG_PATH, 0, winreg.KEY_READ)
            try:
                winreg.QueryValueEx(key, AutoStart.APP_NAME)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except:
            return False

    @staticmethod
    def enable() -> bool:
        """Enable auto-start on Windows startup."""
        try:
            # Get the executable path
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                exe_path = sys.executable
            else:
                # Running as script - get pythonw.exe path and script
                python_exe = sys.executable.replace("python.exe", "pythonw.exe")
                script_path = os.path.abspath(sys.argv[0])
                exe_path = f'"{python_exe}" "{script_path}"'

            # Add to registry
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, AutoStart.REG_PATH, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, AutoStart.APP_NAME, 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)

            return True
        except Exception as e:
            print(f"Failed to enable auto-start: {e}")
            return False

    @staticmethod
    def disable() -> bool:
        """Disable auto-start."""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, AutoStart.REG_PATH, 0, winreg.KEY_WRITE)
            try:
                winreg.DeleteValue(key, AutoStart.APP_NAME)
            except FileNotFoundError:
                pass
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Failed to disable auto-start: {e}")
            return False
