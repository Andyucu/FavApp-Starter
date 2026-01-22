"""Main application window for FavApp Starter."""

import customtkinter as ctk
from typing import Optional

from core.config import ConfigManager
from core.launcher import AppLauncher
from .dialogs import AddAppDialog, AddProfileDialog, ConfirmDialog


class MainWindow(ctk.CTk):
    """Main application window."""

    APP_VERSION = "26.01.02"

    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """
        Initialize the main window.

        Args:
            config_manager: Optional ConfigManager instance. Creates new one if not provided.
        """
        super().__init__()

        # Initialize config
        self.config = config_manager or ConfigManager()

        # Set theme from config
        ctk.set_appearance_mode(self.config.get_theme())
        ctk.set_default_color_theme("blue")

        # Window setup
        self.title(f"FavApp Starter v{self.APP_VERSION}")
        self.geometry("500x450")
        self.minsize(400, 350)

        # Create widgets
        self._create_widgets()

        # Load initial data
        self._refresh_profile_list()
        self._refresh_app_list()

    def _create_widgets(self):
        """Create all window widgets."""
        # Main container with padding
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Header with title and theme toggle
        self._create_header()

        # Profile section
        self._create_profile_section()

        # App list section
        self._create_app_list_section()

        # App buttons section
        self._create_app_buttons()

        # Launch button
        self._create_launch_button()

    def _create_header(self):
        """Create header with title and theme toggle."""
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))

        # Title
        ctk.CTkLabel(
            header_frame,
            text="FavApp Starter",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left")

        # Theme toggle button
        self.theme_btn = ctk.CTkButton(
            header_frame,
            text="🌙" if self.config.get_theme() == "dark" else "☀️",
            width=35,
            height=35,
            command=self._toggle_theme
        )
        self.theme_btn.pack(side="right")

    def _create_profile_section(self):
        """Create profile selection section."""
        profile_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        profile_frame.pack(fill="x", pady=(0, 10))

        # Label
        ctk.CTkLabel(profile_frame, text="Profile:", width=60, anchor="w").pack(side="left")

        # Profile dropdown
        self.profile_var = ctk.StringVar(value=self.config.get_active_profile())
        self.profile_dropdown = ctk.CTkOptionMenu(
            profile_frame,
            variable=self.profile_var,
            values=self.config.get_profiles(),
            width=200,
            command=self._on_profile_change
        )
        self.profile_dropdown.pack(side="left", padx=(0, 10))

        # Add profile button
        ctk.CTkButton(
            profile_frame,
            text="+",
            width=35,
            height=35,
            command=self._show_add_profile_dialog
        ).pack(side="left", padx=(0, 5))

        # Delete profile button
        ctk.CTkButton(
            profile_frame,
            text="🗑",
            width=35,
            height=35,
            fg_color="#d9534f",
            hover_color="#c9302c",
            command=self._delete_profile
        ).pack(side="left")

    def _create_app_list_section(self):
        """Create the application list section."""
        # Frame for the list
        list_frame = ctk.CTkFrame(self.main_frame)
        list_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Label
        ctk.CTkLabel(
            list_frame,
            text="Applications:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        # Scrollable frame for apps
        self.app_list_frame = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        self.app_list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Store app item widgets
        self.app_items: list[ctk.CTkFrame] = []

    def _create_app_buttons(self):
        """Create app management buttons."""
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkButton(
            button_frame,
            text="Add App",
            width=120,
            command=self._show_add_app_dialog
        ).pack(side="left", padx=(0, 10))

        self.remove_btn = ctk.CTkButton(
            button_frame,
            text="Remove Selected",
            width=120,
            fg_color="gray",
            hover_color="darkgray",
            command=self._remove_selected_app,
            state="disabled"
        )
        self.remove_btn.pack(side="left")

    def _create_launch_button(self):
        """Create the main launch button."""
        self.launch_btn = ctk.CTkButton(
            self.main_frame,
            text="🚀 LAUNCH ALL",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            command=self._launch_all
        )
        self.launch_btn.pack(fill="x")

    def _refresh_profile_list(self):
        """Refresh the profile dropdown."""
        profiles = self.config.get_profiles()
        self.profile_dropdown.configure(values=profiles)
        self.profile_var.set(self.config.get_active_profile())

    def _refresh_app_list(self):
        """Refresh the application list."""
        # Clear existing items
        for item in self.app_items:
            item.destroy()
        self.app_items.clear()

        # Get apps for current profile
        apps = self.config.get_apps()

        if not apps:
            # Show empty state
            empty_label = ctk.CTkLabel(
                self.app_list_frame,
                text="No apps added yet.\nClick 'Add App' to get started.",
                text_color="gray"
            )
            empty_label.pack(pady=20)
            self.app_items.append(empty_label)
            self.remove_btn.configure(state="disabled")
            return

        # Create app items
        for i, app in enumerate(apps):
            item = self._create_app_item(i, app["name"], app["path"])
            self.app_items.append(item)

    def _create_app_item(self, index: int, name: str, path: str) -> ctk.CTkFrame:
        """Create a single app item widget."""
        item_frame = ctk.CTkFrame(self.app_list_frame)
        item_frame.pack(fill="x", pady=2)

        # Selection variable
        selected_var = ctk.BooleanVar(value=False)

        # Checkbox for selection
        checkbox = ctk.CTkCheckBox(
            item_frame,
            text="",
            variable=selected_var,
            width=20,
            command=self._update_remove_button
        )
        checkbox.pack(side="left", padx=(10, 5), pady=8)

        # Store selection var on frame
        item_frame.selected_var = selected_var
        item_frame.app_index = index

        # App info
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, pady=5)

        ctk.CTkLabel(
            info_frame,
            text=name,
            font=ctk.CTkFont(weight="bold"),
            anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            info_frame,
            text=path,
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w"
        ).pack(fill="x")

        return item_frame

    def _update_remove_button(self):
        """Update remove button state based on selection."""
        has_selection = any(
            hasattr(item, 'selected_var') and item.selected_var.get()
            for item in self.app_items
        )
        self.remove_btn.configure(state="normal" if has_selection else "disabled")

    def _on_profile_change(self, profile_name: str):
        """Handle profile selection change."""
        self.config.set_active_profile(profile_name)
        self._refresh_app_list()

    def _toggle_theme(self):
        """Toggle between dark and light theme."""
        new_theme = self.config.toggle_theme()
        ctk.set_appearance_mode(new_theme)
        self.theme_btn.configure(text="🌙" if new_theme == "dark" else "☀️")

    def _show_add_profile_dialog(self):
        """Show dialog to add a new profile."""
        AddProfileDialog(
            self,
            on_create=self._add_profile,
            existing_profiles=self.config.get_profiles()
        )

    def _add_profile(self, name: str):
        """Add a new profile."""
        if self.config.add_profile(name):
            self.config.set_active_profile(name)
            self._refresh_profile_list()
            self._refresh_app_list()

    def _delete_profile(self):
        """Delete the current profile."""
        profile = self.config.get_active_profile()

        if len(self.config.get_profiles()) <= 1:
            self._show_message("Cannot Delete", "You cannot delete the last profile.")
            return

        ConfirmDialog(
            self,
            title="Delete Profile",
            message=f"Are you sure you want to delete the profile '{profile}'?\nAll apps in this profile will be removed.",
            on_confirm=self._confirm_delete_profile
        )

    def _confirm_delete_profile(self):
        """Confirm profile deletion."""
        if self.config.delete_profile(self.config.get_active_profile()):
            self._refresh_profile_list()
            self._refresh_app_list()

    def _show_add_app_dialog(self):
        """Show dialog to add a new app."""
        AddAppDialog(self, on_add=self._add_app)

    def _add_app(self, name: str, path: str):
        """Add a new app to the current profile."""
        if self.config.add_app(name, path):
            self._refresh_app_list()

    def _remove_selected_app(self):
        """Remove selected apps from the current profile."""
        # Get selected indices in reverse order (to remove from end first)
        selected_indices = sorted(
            [item.app_index for item in self.app_items
             if hasattr(item, 'selected_var') and item.selected_var.get()],
            reverse=True
        )

        for index in selected_indices:
            self.config.remove_app(index)

        self._refresh_app_list()

    def _launch_all(self):
        """Launch all apps in the current profile."""
        apps = self.config.get_apps()

        if not apps:
            self._show_message("No Apps", "There are no apps to launch in this profile.")
            return

        # Launch apps
        results = AppLauncher.launch_multiple(apps)

        # Check for errors
        errors = [r for r in results if not r["success"]]

        if errors:
            error_msg = "\n".join([f"• {r['name']}: {r['error']}" for r in errors])
            self._show_message(
                "Launch Errors",
                f"Some apps failed to launch:\n\n{error_msg}"
            )
        else:
            # Brief success indicator
            self.launch_btn.configure(text="✓ Launched!", fg_color="green")
            self.after(1500, lambda: self.launch_btn.configure(
                text="🚀 LAUNCH ALL",
                fg_color=["#3B8ED0", "#1F6AA5"]
            ))

    def _show_message(self, title: str, message: str):
        """Show a message dialog."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("350x150")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        # Center on parent
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - 350) // 2
        y = self.winfo_y() + (self.winfo_height() - 150) // 2
        dialog.geometry(f"+{x}+{y}")

        ctk.CTkLabel(dialog, text=message, wraplength=300).pack(pady=20, padx=20)
        ctk.CTkButton(dialog, text="OK", width=80, command=dialog.destroy).pack(pady=(0, 20))
