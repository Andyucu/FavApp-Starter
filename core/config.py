"""Configuration management for FavApp Starter."""

import json
import os
from typing import Optional
from datetime import datetime


class ConfigManager:
    """Manages application configuration including profiles and apps."""

    DEFAULT_CONFIG = {
        "active_profile": "Default",
        "theme": "dark",
        "launch_delay": 0,  # Delay in ms between launching apps
        "minimize_to_tray": True,
        "start_minimized": False,
        "confirm_on_exit": False,
        "show_app_icons": True,
        "window": {
            "x": None,
            "y": None,
            "width": 550,
            "height": 550
        },
        "last_launch": None,
        "profiles": {
            "Default": {
                "apps": []
            }
        }
    }

    def __init__(self, config_path: Optional[str] = None):
        """Initialize ConfigManager with optional config file path."""
        if config_path is None:
            import sys
            # Determine config location based on whether we're frozen or not
            if getattr(sys, 'frozen', False):
                # Running as .exe - save config next to executable
                base_dir = os.path.dirname(sys.executable)
            else:
                # Running from source - save in project root
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            config_path = os.path.join(base_dir, "config.json")

        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load configuration from file or create default."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                return self._validate_config(config)
            except (json.JSONDecodeError, IOError):
                return self._deep_copy(self.DEFAULT_CONFIG)
        return self._deep_copy(self.DEFAULT_CONFIG)

    def _deep_copy(self, d: dict) -> dict:
        """Deep copy a dictionary."""
        return json.loads(json.dumps(d))

    def _validate_config(self, config: dict) -> dict:
        """Validate and ensure config has all required fields."""
        validated = self._deep_copy(self.DEFAULT_CONFIG)

        # Merge existing config with defaults
        for key in self.DEFAULT_CONFIG:
            if key in config:
                if isinstance(self.DEFAULT_CONFIG[key], dict) and key != "profiles":
                    # Merge nested dicts
                    if isinstance(config[key], dict):
                        validated[key].update(config[key])
                else:
                    validated[key] = config[key]

        # Ensure active profile exists
        if validated["active_profile"] not in validated["profiles"]:
            if validated["profiles"]:
                validated["active_profile"] = list(validated["profiles"].keys())[0]
            else:
                validated["profiles"]["Default"] = {"apps": []}
                validated["active_profile"] = "Default"

        # Migrate old app format to new format with arguments
        for profile_name, profile_data in validated["profiles"].items():
            apps = profile_data.get("apps", [])
            for app in apps:
                if "arguments" not in app:
                    app["arguments"] = ""
                if "working_dir" not in app:
                    app["working_dir"] = ""

        return validated

    def save(self) -> None:
        """Save current configuration to file."""
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def get_setting(self, key: str, default=None):
        """Get a configuration setting value."""
        return self.config.get(key, default)

    def set_setting(self, key: str, value) -> None:
        """Set a configuration setting value."""
        self.config[key] = value
        self.save()

    # Profile management
    def get_profiles(self) -> list[str]:
        """Get list of all profile names."""
        return list(self.config["profiles"].keys())

    def get_active_profile(self) -> str:
        """Get the currently active profile name."""
        return self.config["active_profile"]

    def set_active_profile(self, profile_name: str) -> bool:
        """Set the active profile. Returns True if successful."""
        if profile_name in self.config["profiles"]:
            self.config["active_profile"] = profile_name
            self.save()
            return True
        return False

    def add_profile(self, profile_name: str) -> bool:
        """Add a new profile. Returns True if successful."""
        if profile_name and profile_name not in self.config["profiles"]:
            self.config["profiles"][profile_name] = {"apps": []}
            self.save()
            return True
        return False

    def delete_profile(self, profile_name: str) -> bool:
        """Delete a profile. Returns True if successful."""
        if len(self.config["profiles"]) <= 1:
            return False

        if profile_name in self.config["profiles"]:
            del self.config["profiles"][profile_name]
            if self.config["active_profile"] == profile_name:
                self.config["active_profile"] = list(self.config["profiles"].keys())[0]
            self.save()
            return True
        return False

    def duplicate_profile(self, source_name: str, new_name: str) -> bool:
        """Duplicate a profile with a new name."""
        if source_name not in self.config["profiles"]:
            return False
        if new_name in self.config["profiles"] or not new_name:
            return False

        # Deep copy the profile
        source_profile = self.config["profiles"][source_name]
        self.config["profiles"][new_name] = self._deep_copy(source_profile)
        self.save()
        return True

    def rename_profile(self, old_name: str, new_name: str) -> bool:
        """Rename a profile."""
        if old_name not in self.config["profiles"]:
            return False
        if new_name in self.config["profiles"] or not new_name:
            return False

        self.config["profiles"][new_name] = self.config["profiles"].pop(old_name)
        if self.config["active_profile"] == old_name:
            self.config["active_profile"] = new_name
        self.save()
        return True

    # App management
    def get_apps(self, profile_name: Optional[str] = None) -> list[dict]:
        """Get apps for a profile. Uses active profile if none specified."""
        if profile_name is None:
            profile_name = self.config["active_profile"]

        if profile_name in self.config["profiles"]:
            return self.config["profiles"][profile_name].get("apps", [])
        return []

    def add_app(self, name: str, path: str, arguments: str = "",
                working_dir: str = "", profile_name: Optional[str] = None) -> bool:
        """Add an app to a profile. Uses active profile if none specified."""
        if profile_name is None:
            profile_name = self.config["active_profile"]

        if profile_name in self.config["profiles"]:
            apps = self.config["profiles"][profile_name].get("apps", [])
            # Check for duplicates
            for app in apps:
                if app["path"] == path:
                    return False
            apps.append({
                "name": name,
                "path": path,
                "arguments": arguments,
                "working_dir": working_dir
            })
            self.config["profiles"][profile_name]["apps"] = apps
            self.save()
            return True
        return False

    def update_app(self, index: int, name: str, path: str, arguments: str = "",
                   working_dir: str = "", profile_name: Optional[str] = None) -> bool:
        """Update an existing app."""
        if profile_name is None:
            profile_name = self.config["active_profile"]

        if profile_name in self.config["profiles"]:
            apps = self.config["profiles"][profile_name].get("apps", [])
            if 0 <= index < len(apps):
                apps[index] = {
                    "name": name,
                    "path": path,
                    "arguments": arguments,
                    "working_dir": working_dir
                }
                self.save()
                return True
        return False

    def remove_app(self, index: int, profile_name: Optional[str] = None) -> bool:
        """Remove an app by index from a profile."""
        if profile_name is None:
            profile_name = self.config["active_profile"]

        if profile_name in self.config["profiles"]:
            apps = self.config["profiles"][profile_name].get("apps", [])
            if 0 <= index < len(apps):
                apps.pop(index)
                self.save()
                return True
        return False

    def move_app(self, from_index: int, to_index: int, profile_name: Optional[str] = None) -> bool:
        """Move an app to a different position."""
        if profile_name is None:
            profile_name = self.config["active_profile"]

        if profile_name in self.config["profiles"]:
            apps = self.config["profiles"][profile_name].get("apps", [])
            if 0 <= from_index < len(apps) and 0 <= to_index < len(apps):
                app = apps.pop(from_index)
                apps.insert(to_index, app)
                self.save()
                return True
        return False

    # Theme management
    def get_theme(self) -> str:
        """Get current theme."""
        return self.config.get("theme", "dark")

    def set_theme(self, theme: str) -> None:
        """Set theme."""
        if theme in ("dark", "light", "system"):
            self.config["theme"] = theme
            self.save()

    # Settings management
    def get_launch_delay(self) -> int:
        """Get launch delay in milliseconds."""
        return self.config.get("launch_delay", 0)

    def set_launch_delay(self, delay_ms: int) -> None:
        """Set launch delay in milliseconds."""
        self.config["launch_delay"] = max(0, delay_ms)
        self.save()

    def get_minimize_to_tray(self) -> bool:
        """Get minimize to tray setting."""
        return self.config.get("minimize_to_tray", True)

    def set_minimize_to_tray(self, value: bool) -> None:
        """Set minimize to tray setting."""
        self.config["minimize_to_tray"] = value
        self.save()

    def get_start_minimized(self) -> bool:
        """Get start minimized setting."""
        return self.config.get("start_minimized", False)

    def set_start_minimized(self, value: bool) -> None:
        """Set start minimized setting."""
        self.config["start_minimized"] = value
        self.save()

    def get_confirm_on_exit(self) -> bool:
        """Get confirm on exit setting."""
        return self.config.get("confirm_on_exit", False)

    def set_confirm_on_exit(self, value: bool) -> None:
        """Set confirm on exit setting."""
        self.config["confirm_on_exit"] = value
        self.save()

    def get_show_app_icons(self) -> bool:
        """Get show app icons setting."""
        return self.config.get("show_app_icons", True)

    def set_show_app_icons(self, value: bool) -> None:
        """Set show app icons setting."""
        self.config["show_app_icons"] = value
        self.save()

    # Window management
    def get_window_geometry(self) -> dict:
        """Get saved window geometry."""
        return self.config.get("window", self.DEFAULT_CONFIG["window"])

    def set_window_geometry(self, x: int, y: int, width: int, height: int) -> None:
        """Save window geometry."""
        self.config["window"] = {"x": x, "y": y, "width": width, "height": height}
        self.save()

    # Last launch tracking
    def get_last_launch(self) -> Optional[str]:
        """Get last launch timestamp."""
        return self.config.get("last_launch")

    def set_last_launch(self) -> None:
        """Set last launch to now."""
        self.config["last_launch"] = datetime.now().isoformat()
        self.save()

    # Import/Export
    def export_profile(self, profile_name: str) -> Optional[dict]:
        """Export a profile as a dictionary."""
        if profile_name in self.config["profiles"]:
            return {
                "name": profile_name,
                "data": self._deep_copy(self.config["profiles"][profile_name])
            }
        return None

    def import_profile(self, profile_data: dict, new_name: Optional[str] = None) -> bool:
        """Import a profile from a dictionary."""
        try:
            name = new_name or profile_data.get("name", "Imported")
            data = profile_data.get("data", {"apps": []})

            # Ensure unique name
            base_name = name
            counter = 1
            while name in self.config["profiles"]:
                name = f"{base_name} ({counter})"
                counter += 1

            self.config["profiles"][name] = data
            self.save()
            return True
        except Exception:
            return False

    def export_all_profiles(self) -> dict:
        """Export all profiles."""
        return {
            "version": "1.0",
            "profiles": self._deep_copy(self.config["profiles"])
        }

    def import_all_profiles(self, data: dict, replace: bool = False) -> int:
        """Import multiple profiles. Returns count of imported profiles."""
        try:
            profiles = data.get("profiles", {})
            count = 0

            if replace:
                self.config["profiles"] = {}

            for name, profile_data in profiles.items():
                base_name = name
                counter = 1
                while name in self.config["profiles"]:
                    name = f"{base_name} ({counter})"
                    counter += 1

                self.config["profiles"][name] = profile_data
                count += 1

            if not self.config["profiles"]:
                self.config["profiles"]["Default"] = {"apps": []}

            if self.config["active_profile"] not in self.config["profiles"]:
                self.config["active_profile"] = list(self.config["profiles"].keys())[0]

            self.save()
            return count
        except Exception:
            return 0
