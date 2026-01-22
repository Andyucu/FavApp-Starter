"""Configuration management for FavApp Starter."""

import json
import os
from typing import Optional


class ConfigManager:
    """Manages application configuration including profiles and apps."""

    DEFAULT_CONFIG = {
        "active_profile": "Default",
        "theme": "dark",
        "profiles": {
            "Default": {
                "apps": []
            }
        }
    }

    def __init__(self, config_path: Optional[str] = None):
        """Initialize ConfigManager with optional config file path."""
        if config_path is None:
            # Default to config.json in the same directory as this file's parent
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
                # Validate and merge with defaults
                return self._validate_config(config)
            except (json.JSONDecodeError, IOError):
                return self.DEFAULT_CONFIG.copy()
        return self.DEFAULT_CONFIG.copy()

    def _validate_config(self, config: dict) -> dict:
        """Validate and ensure config has all required fields."""
        validated = self.DEFAULT_CONFIG.copy()

        if "active_profile" in config:
            validated["active_profile"] = config["active_profile"]
        if "theme" in config:
            validated["theme"] = config["theme"]
        if "profiles" in config and isinstance(config["profiles"], dict):
            validated["profiles"] = config["profiles"]

        # Ensure active profile exists
        if validated["active_profile"] not in validated["profiles"]:
            if validated["profiles"]:
                validated["active_profile"] = list(validated["profiles"].keys())[0]
            else:
                validated["profiles"]["Default"] = {"apps": []}
                validated["active_profile"] = "Default"

        return validated

    def save(self) -> None:
        """Save current configuration to file."""
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

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
        # Don't delete if it's the only profile
        if len(self.config["profiles"]) <= 1:
            return False

        if profile_name in self.config["profiles"]:
            del self.config["profiles"][profile_name]
            # Switch to another profile if we deleted the active one
            if self.config["active_profile"] == profile_name:
                self.config["active_profile"] = list(self.config["profiles"].keys())[0]
            self.save()
            return True
        return False

    # App management
    def get_apps(self, profile_name: Optional[str] = None) -> list[dict]:
        """Get apps for a profile. Uses active profile if none specified."""
        if profile_name is None:
            profile_name = self.config["active_profile"]

        if profile_name in self.config["profiles"]:
            return self.config["profiles"][profile_name].get("apps", [])
        return []

    def add_app(self, name: str, path: str, profile_name: Optional[str] = None) -> bool:
        """Add an app to a profile. Uses active profile if none specified."""
        if profile_name is None:
            profile_name = self.config["active_profile"]

        if profile_name in self.config["profiles"]:
            apps = self.config["profiles"][profile_name].get("apps", [])
            # Check for duplicates
            for app in apps:
                if app["path"] == path:
                    return False
            apps.append({"name": name, "path": path})
            self.config["profiles"][profile_name]["apps"] = apps
            self.save()
            return True
        return False

    def remove_app(self, index: int, profile_name: Optional[str] = None) -> bool:
        """Remove an app by index from a profile. Uses active profile if none specified."""
        if profile_name is None:
            profile_name = self.config["active_profile"]

        if profile_name in self.config["profiles"]:
            apps = self.config["profiles"][profile_name].get("apps", [])
            if 0 <= index < len(apps):
                apps.pop(index)
                self.save()
                return True
        return False

    # Theme management
    def get_theme(self) -> str:
        """Get current theme (dark or light)."""
        return self.config.get("theme", "dark")

    def set_theme(self, theme: str) -> None:
        """Set theme (dark or light)."""
        if theme in ("dark", "light"):
            self.config["theme"] = theme
            self.save()

    def toggle_theme(self) -> str:
        """Toggle between dark and light theme. Returns new theme."""
        new_theme = "light" if self.get_theme() == "dark" else "dark"
        self.set_theme(new_theme)
        return new_theme
