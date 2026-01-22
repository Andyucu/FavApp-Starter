"""Application launcher for FavApp Starter."""

import os
import subprocess
from typing import Optional


class AppLauncher:
    """Handles launching Windows applications."""

    @staticmethod
    def launch_app(path: str) -> tuple[bool, Optional[str]]:
        """
        Launch a single application.

        Args:
            path: Path to the executable

        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        if not path:
            return False, "Empty path provided"

        if not os.path.exists(path):
            return False, f"File not found: {path}"

        try:
            # Use subprocess.Popen for non-blocking launch
            # shell=True helps with paths containing spaces and launching shortcuts
            subprocess.Popen(path, shell=True)
            return True, None
        except PermissionError:
            return False, f"Permission denied: {path}"
        except OSError as e:
            return False, f"Failed to launch: {e}"
        except Exception as e:
            return False, f"Unexpected error: {e}"

    @staticmethod
    def launch_multiple(apps: list[dict]) -> list[dict]:
        """
        Launch multiple applications.

        Args:
            apps: List of app dictionaries with 'name' and 'path' keys

        Returns:
            List of results with 'name', 'success', and 'error' keys
        """
        results = []

        for app in apps:
            name = app.get("name", "Unknown")
            path = app.get("path", "")

            success, error = AppLauncher.launch_app(path)
            results.append({
                "name": name,
                "success": success,
                "error": error
            })

        return results

    @staticmethod
    def validate_path(path: str) -> tuple[bool, Optional[str]]:
        """
        Validate if a path exists and is executable.

        Args:
            path: Path to validate

        Returns:
            Tuple of (valid: bool, error_message: Optional[str])
        """
        if not path:
            return False, "Empty path"

        if not os.path.exists(path):
            return False, "File does not exist"

        if not os.path.isfile(path):
            return False, "Path is not a file"

        # Check for common executable extensions on Windows
        valid_extensions = {".exe", ".bat", ".cmd", ".lnk", ".msc"}
        _, ext = os.path.splitext(path.lower())

        if ext not in valid_extensions:
            return False, f"Unsupported file type: {ext}"

        return True, None
