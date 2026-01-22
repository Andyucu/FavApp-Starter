"""Application launcher for FavApp Starter."""

import os
import subprocess
import time
from typing import Optional, Callable
from PIL import Image
import ctypes
from ctypes import wintypes
import io


class IconExtractor:
    """Extract icons from Windows executables."""

    # Windows API constants
    SHGFI_ICON = 0x000000100
    SHGFI_LARGEICON = 0x000000000
    SHGFI_SMALLICON = 0x000000001
    SHIL_EXTRALARGE = 0x02
    SHIL_JUMBO = 0x04

    class SHFILEINFO(ctypes.Structure):
        _fields_ = [
            ("hIcon", wintypes.HANDLE),
            ("iIcon", ctypes.c_int),
            ("dwAttributes", wintypes.DWORD),
            ("szDisplayName", wintypes.WCHAR * 260),
            ("szTypeName", wintypes.WCHAR * 80),
        ]

    @staticmethod
    def get_icon(path: str, size: int = 32) -> Optional[Image.Image]:
        """
        Extract icon from an executable file.

        Args:
            path: Path to the executable
            size: Desired icon size (16, 32, 48, or 256)

        Returns:
            PIL Image of the icon, or None if extraction fails
        """
        if not os.path.exists(path):
            return None

        try:
            # Load shell32
            shell32 = ctypes.windll.shell32

            # Get file info with icon
            shinfo = IconExtractor.SHFILEINFO()
            flags = IconExtractor.SHGFI_ICON

            if size <= 16:
                flags |= IconExtractor.SHGFI_SMALLICON
            else:
                flags |= IconExtractor.SHGFI_LARGEICON

            result = shell32.SHGetFileInfoW(
                path, 0, ctypes.byref(shinfo),
                ctypes.sizeof(shinfo), flags
            )

            if result and shinfo.hIcon:
                # Convert HICON to PIL Image
                icon_image = IconExtractor._hicon_to_image(shinfo.hIcon, size)

                # Destroy the icon handle
                ctypes.windll.user32.DestroyIcon(shinfo.hIcon)

                return icon_image

        except Exception:
            pass

        return None

    @staticmethod
    def _hicon_to_image(hicon, size: int = 32) -> Optional[Image.Image]:
        """Convert a Windows HICON to a PIL Image."""
        try:
            # Get icon info
            class ICONINFO(ctypes.Structure):
                _fields_ = [
                    ("fIcon", wintypes.BOOL),
                    ("xHotspot", wintypes.DWORD),
                    ("yHotspot", wintypes.DWORD),
                    ("hbmMask", wintypes.HBITMAP),
                    ("hbmColor", wintypes.HBITMAP),
                ]

            icon_info = ICONINFO()
            if not ctypes.windll.user32.GetIconInfo(hicon, ctypes.byref(icon_info)):
                return None

            # Get bitmap info
            class BITMAP(ctypes.Structure):
                _fields_ = [
                    ("bmType", wintypes.LONG),
                    ("bmWidth", wintypes.LONG),
                    ("bmHeight", wintypes.LONG),
                    ("bmWidthBytes", wintypes.LONG),
                    ("bmPlanes", wintypes.WORD),
                    ("bmBitsPixel", wintypes.WORD),
                    ("bmBits", ctypes.c_void_p),
                ]

            bmp = BITMAP()
            if icon_info.hbmColor:
                ctypes.windll.gdi32.GetObjectW(
                    icon_info.hbmColor, ctypes.sizeof(BITMAP), ctypes.byref(bmp)
                )

                width = bmp.bmWidth
                height = bmp.bmHeight

                # Create device context
                hdc = ctypes.windll.user32.GetDC(0)
                hdc_mem = ctypes.windll.gdi32.CreateCompatibleDC(hdc)

                # Create bitmap info header
                class BITMAPINFOHEADER(ctypes.Structure):
                    _fields_ = [
                        ("biSize", wintypes.DWORD),
                        ("biWidth", wintypes.LONG),
                        ("biHeight", wintypes.LONG),
                        ("biPlanes", wintypes.WORD),
                        ("biBitCount", wintypes.WORD),
                        ("biCompression", wintypes.DWORD),
                        ("biSizeImage", wintypes.DWORD),
                        ("biXPelsPerMeter", wintypes.LONG),
                        ("biYPelsPerMeter", wintypes.LONG),
                        ("biClrUsed", wintypes.DWORD),
                        ("biClrImportant", wintypes.DWORD),
                    ]

                bmi = BITMAPINFOHEADER()
                bmi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
                bmi.biWidth = width
                bmi.biHeight = -height  # Top-down
                bmi.biPlanes = 1
                bmi.biBitCount = 32
                bmi.biCompression = 0  # BI_RGB

                # Get bits
                buffer_size = width * height * 4
                buffer = ctypes.create_string_buffer(buffer_size)

                ctypes.windll.gdi32.GetDIBits(
                    hdc_mem, icon_info.hbmColor, 0, height,
                    buffer, ctypes.byref(bmi), 0
                )

                # Create image from buffer
                img = Image.frombuffer('RGBA', (width, height), buffer, 'raw', 'BGRA', 0, 1)

                # Cleanup
                ctypes.windll.gdi32.DeleteDC(hdc_mem)
                ctypes.windll.user32.ReleaseDC(0, hdc)

                if icon_info.hbmColor:
                    ctypes.windll.gdi32.DeleteObject(icon_info.hbmColor)
                if icon_info.hbmMask:
                    ctypes.windll.gdi32.DeleteObject(icon_info.hbmMask)

                # Resize if needed
                if img.size != (size, size):
                    img = img.resize((size, size), Image.Resampling.LANCZOS)

                return img

        except Exception:
            pass

        return None

    @staticmethod
    def get_default_icon(size: int = 32) -> Image.Image:
        """Create a default application icon."""
        img = Image.new('RGBA', (size, size), (100, 100, 100, 255))
        return img


class AppLauncher:
    """Handles launching Windows applications."""

    @staticmethod
    def launch_app(path: str, arguments: str = "", working_dir: str = "") -> tuple[bool, Optional[str]]:
        """
        Launch a single application.

        Args:
            path: Path to the executable
            arguments: Command-line arguments
            working_dir: Working directory for the app

        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        if not path:
            return False, "Empty path provided"

        if not os.path.exists(path):
            return False, f"File not found: {path}"

        try:
            # Build command
            if arguments:
                cmd = f'"{path}" {arguments}'
            else:
                cmd = f'"{path}"'

            # Set working directory
            cwd = working_dir if working_dir and os.path.isdir(working_dir) else os.path.dirname(path)

            # Launch with subprocess
            subprocess.Popen(
                cmd,
                shell=True,
                cwd=cwd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True, None

        except PermissionError:
            return False, f"Permission denied: {path}"
        except OSError as e:
            return False, f"Failed to launch: {e}"
        except Exception as e:
            return False, f"Unexpected error: {e}"

    @staticmethod
    def launch_multiple(apps: list[dict], delay_ms: int = 0,
                        progress_callback: Optional[Callable[[int, int, str], None]] = None) -> list[dict]:
        """
        Launch multiple applications with optional delay between them.

        Args:
            apps: List of app dictionaries with 'name', 'path', 'arguments', 'working_dir' keys
            delay_ms: Delay in milliseconds between launching apps
            progress_callback: Optional callback(current, total, app_name) for progress updates

        Returns:
            List of results with 'name', 'success', and 'error' keys
        """
        results = []
        total = len(apps)

        for i, app in enumerate(apps):
            name = app.get("name", "Unknown")
            path = app.get("path", "")
            arguments = app.get("arguments", "")
            working_dir = app.get("working_dir", "")

            # Call progress callback
            if progress_callback:
                progress_callback(i + 1, total, name)

            success, error = AppLauncher.launch_app(path, arguments, working_dir)
            results.append({
                "name": name,
                "success": success,
                "error": error
            })

            # Apply delay between apps (except for the last one)
            if delay_ms > 0 and i < total - 1:
                time.sleep(delay_ms / 1000.0)

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
        valid_extensions = {".exe", ".bat", ".cmd", ".lnk", ".msc", ".msi"}
        _, ext = os.path.splitext(path.lower())

        if ext not in valid_extensions:
            return False, f"Unsupported file type: {ext}"

        return True, None

    @staticmethod
    def is_running(path: str) -> bool:
        """Check if an application is already running."""
        try:
            # Get the executable name
            exe_name = os.path.basename(path).lower()

            # Use tasklist to check
            result = subprocess.run(
                ['tasklist', '/FI', f'IMAGENAME eq {exe_name}'],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            return exe_name in result.stdout.lower()
        except Exception:
            return False
