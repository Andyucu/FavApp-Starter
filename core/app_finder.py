"""Find installed applications on Windows."""

import os
import winreg
from typing import List, Dict


class AppFinder:
    """Find installed applications on Windows system."""

    @staticmethod
    def find_installed_apps() -> List[Dict[str, str]]:
        """
        Find installed applications by scanning registry and common locations.

        Returns:
            List of dicts with 'name' and 'path' keys
        """
        apps = []
        seen_paths = set()

        # Scan registry
        apps.extend(AppFinder._scan_registry())

        # Scan common installation directories
        common_dirs = [
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "*"),
            os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "*"),
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "*"),
        ]

        for dir_pattern in common_dirs:
            apps.extend(AppFinder._scan_directory(os.path.dirname(dir_pattern)))

        # Remove duplicates based on path
        unique_apps = []
        for app in apps:
            path_lower = app["path"].lower()
            if path_lower not in seen_paths and os.path.exists(app["path"]):
                seen_paths.add(path_lower)
                unique_apps.append(app)

        # Sort by name
        unique_apps.sort(key=lambda x: x["name"].lower())

        return unique_apps

    @staticmethod
    def _scan_registry() -> List[Dict[str, str]]:
        """Scan Windows registry for installed applications."""
        apps = []

        # Registry paths to check
        reg_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        ]

        for hkey, subkey_path in reg_paths:
            try:
                key = winreg.OpenKey(hkey, subkey_path)
                num_subkeys = winreg.QueryInfoKey(key)[0]

                for i in range(num_subkeys):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)

                        try:
                            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]

                            # Try to get the executable path
                            exe_path = None
                            try:
                                exe_path = winreg.QueryValueEx(subkey, "DisplayIcon")[0]
                                # DisplayIcon might have format "path,index"
                                if "," in exe_path:
                                    exe_path = exe_path.split(",")[0].strip('"')
                            except:
                                pass

                            if not exe_path or not exe_path.endswith(".exe"):
                                try:
                                    install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                    if install_location and os.path.isdir(install_location):
                                        # Look for exe in install location
                                        for root, dirs, files in os.walk(install_location):
                                            for file in files:
                                                if file.endswith(".exe") and not file.startswith("unins"):
                                                    exe_path = os.path.join(root, file)
                                                    break
                                            if exe_path:
                                                break
                                except:
                                    pass

                            if exe_path and os.path.exists(exe_path) and exe_path.endswith(".exe"):
                                apps.append({"name": display_name, "path": exe_path})

                        except:
                            pass

                        winreg.CloseKey(subkey)

                    except:
                        continue

                winreg.CloseKey(key)

            except:
                continue

        return apps

    @staticmethod
    def _scan_directory(directory: str, max_depth: int = 2) -> List[Dict[str, str]]:
        """Scan a directory for .exe files."""
        apps = []

        if not os.path.exists(directory):
            return apps

        try:
            for root, dirs, files in os.walk(directory):
                # Limit depth
                depth = root[len(directory):].count(os.sep)
                if depth > max_depth:
                    dirs[:] = []
                    continue

                for file in files:
                    if file.endswith(".exe") and not file.lower().startswith("unins"):
                        full_path = os.path.join(root, file)
                        name = os.path.splitext(file)[0]
                        apps.append({"name": name, "path": full_path})

        except:
            pass

        return apps
