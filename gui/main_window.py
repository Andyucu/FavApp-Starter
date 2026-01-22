"""Main application window for FavApp Starter."""

import customtkinter as ctk
from tkinter import Menu
from typing import Optional
import os

from core.config import ConfigManager
from core.launcher import AppLauncher
from .dialogs import AddAppDialog, AddProfileDialog, ConfirmDialog, OptionsDialog, AboutDialog, LicenseDialog


class MainWindow(ctk.CTk):
    """Main application window."""

    APP_VERSION = "26.01.03"
    APP_AUTHOR = "Alexandru Teodorovici"

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
        self.geometry("500x500")
        self.minsize(400, 400)

        # Set icon if available
        self._set_icon()

        # Create menu bar
        self._create_menu()

        # Create widgets
        self._create_widgets()

        # Load initial data
        self._refresh_profile_list()
        self._refresh_app_list()

    def _set_icon(self):
        """Set the application icon."""
        # Try to find icon in various locations
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_paths = [
            os.path.join(base_dir, "assets", "icon.ico"),
            os.path.join(base_dir, "icon.ico"),
        ]

        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                try:
                    self.iconbitmap(icon_path)
                    break
                except Exception:
                    pass

    def _create_menu(self):
        """Create the application menu bar."""
        self.menubar = Menu(self)
        self.configure(menu=self.menubar)

        # File menu
        file_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Options", command=self._show_options)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        # About menu
        about_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="App Info", command=self._show_about)
        about_menu.add_command(label="License", command=self._show_license)

    def _create_widgets(self):
        """Create all window widgets."""
        # Main container with padding
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Header with title
        self._create_header()

        # Profile section
        self._create_profile_section()

        # App list section
        self._create_app_list_section()

        # Bottom section with fixed-size buttons
        self._create_bottom_section()

    def _create_header(self):
        """Create header with title."""
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))

        # Title
        ctk.CTkLabel(
            header_frame,
            text="FavApp Starter",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left")

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

        # Add profile button - fixed size
        self.add_profile_btn = ctk.CTkButton(
            profile_frame,
            text="+",
            width=35,
            height=35,
            command=self._show_add_profile_dialog
        )
        self.add_profile_btn.pack(side="left", padx=(0, 5))

        # Delete profile button - fixed size
        self.delete_profile_btn = ctk.CTkButton(
            profile_frame,
            text="🗑",
            width=35,
            height=35,
            fg_color="#d9534f",
            hover_color="#c9302c",
            command=self._delete_profile
        )
        self.delete_profile_btn.pack(side="left")

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

    def _create_bottom_section(self):
        """Create bottom section with fixed-size buttons."""
        # Container for bottom buttons
        bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        bottom_frame.pack(fill="x")

        # App management buttons - fixed sizes
        button_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        button_frame.pack(pady=(0, 10))

        self.add_app_btn = ctk.CTkButton(
            button_frame,
            text="Add App",
            width=120,
            height=32,
            command=self._show_add_app_dialog
        )
        self.add_app_btn.pack(side="left", padx=(0, 10))

        self.remove_btn = ctk.CTkButton(
            button_frame,
            text="Remove Selected",
            width=140,
            height=32,
            fg_color="gray",
            hover_color="darkgray",
            command=self._remove_selected_app,
            state="disabled"
        )
        self.remove_btn.pack(side="left")

        # Launch button - fixed size, centered
        launch_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        launch_frame.pack()

        self.launch_btn = ctk.CTkButton(
            launch_frame,
            text="🚀 LAUNCH ALL",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=280,
            height=50,
            command=self._launch_all
        )
        self.launch_btn.pack()

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

    def _show_options(self):
        """Show the options dialog."""
        OptionsDialog(self, self.config, on_theme_change=self._apply_theme)

    def _apply_theme(self, theme: str):
        """Apply theme change."""
        ctk.set_appearance_mode(theme)

    def _show_about(self):
        """Show the about dialog."""
        AboutDialog(self, self.APP_VERSION, self.APP_AUTHOR)

    def _show_license(self):
        """Show the license dialog."""
        LicenseDialog(self, self.APP_AUTHOR)

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
        ctk.CTkButton(dialog, text="OK", width=80, height=32, command=dialog.destroy).pack(pady=(0, 20))
