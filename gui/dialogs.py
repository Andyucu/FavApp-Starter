"""Dialog windows for FavApp Starter."""

import os
import customtkinter as ctk
from tkinter import filedialog
from typing import Optional, Callable
import threading
from core.app_finder import AppFinder
from core.autostart import AutoStart


class AddAppDialog(ctk.CTkToplevel):
    """Dialog for adding a new application."""

    def __init__(self, parent, on_add: Callable[[str, str, str, str], None]):
        """
        Initialize the Add App dialog.

        Args:
            parent: Parent window
            on_add: Callback function(name, path, arguments, working_dir) called when app is added
        """
        super().__init__(parent)

        self.on_add = on_add
        self.selected_path: Optional[str] = None

        # Window setup
        self.title("Add Application")
        self.geometry("600x300")
        self.resizable(False, False)

        # Set icon
        self._set_icon()

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 600) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 300) // 2
        self.geometry(f"+{x}+{y}")

        self._create_widgets()

    def _create_widgets(self):
        """Create dialog widgets."""
        # Main frame with padding
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Path selection
        path_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        path_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(path_frame, text="Application:", width=80, anchor="w").pack(side="left")

        self.path_entry = ctk.CTkEntry(path_frame, width=300, state="readonly")
        self.path_entry.pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            path_frame,
            text="Browse...",
            width=85,
            command=self._browse_file
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            path_frame,
            text="🔍  Search...",
            width=110,
            font=ctk.CTkFont(family="Roboto", size=13),
            fg_color="#2fa572",
            hover_color="#28a164",
            command=self._search_installed_apps
        ).pack(side="left")

        # Name input
        name_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(name_frame, text="Name:", width=80, anchor="w").pack(side="left")

        self.name_entry = ctk.CTkEntry(name_frame, width=370, placeholder_text="Enter a display name")
        self.name_entry.pack(side="left")

        # Arguments input
        args_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        args_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(args_frame, text="Arguments:", width=80, anchor="w").pack(side="left")

        self.args_entry = ctk.CTkEntry(args_frame, width=370, placeholder_text="Command-line arguments (optional)")
        self.args_entry.pack(side="left")

        # Working directory input
        workdir_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        workdir_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(workdir_frame, text="Working Dir:", width=80, anchor="w").pack(side="left")

        self.workdir_entry = ctk.CTkEntry(workdir_frame, width=370, placeholder_text="Working directory (optional)")
        self.workdir_entry.pack(side="left")

        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x")

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=100,
            fg_color="gray",
            hover_color="darkgray",
            command=self.destroy
        ).pack(side="right", padx=(10, 0))

        ctk.CTkButton(
            button_frame,
            text="Add",
            width=100,
            command=self._on_add_click
        ).pack(side="right")

    def _set_icon(self):
        """Set the window icon."""
        try:
            import sys
            # Handle both running from source and from .exe
            if getattr(sys, 'frozen', False):
                # Running from .exe
                base_dir = sys._MEIPASS
            else:
                # Running from source
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            icon_path = os.path.join(base_dir, "assets", "icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            pass

    def _browse_file(self):
        """Open file browser to select an application."""
        path = filedialog.askopenfilename(
            title="Select Application",
            filetypes=[
                ("Executables", "*.exe"),
                ("Batch files", "*.bat;*.cmd"),
                ("Shortcuts", "*.lnk"),
                ("All files", "*.*")
            ]
        )

        if path:
            self._set_selected_app(path)

    def _search_installed_apps(self):
        """Show dialog to search for installed applications."""
        SearchAppsDialog(self, on_select=self._set_selected_app)

    def _set_selected_app(self, path: str, name: str = ""):
        """Set the selected application path and name."""
        self.selected_path = path
        self.path_entry.configure(state="normal")
        self.path_entry.delete(0, "end")
        self.path_entry.insert(0, path)
        self.path_entry.configure(state="readonly")

        # Auto-fill name from filename if empty or use provided name
        if not self.name_entry.get():
            import os
            if name:
                self.name_entry.insert(0, name)
            else:
                filename = os.path.splitext(os.path.basename(path))[0]
                self.name_entry.insert(0, filename)

    def _on_add_click(self):
        """Handle Add button click."""
        name = self.name_entry.get().strip()
        path = self.selected_path
        arguments = self.args_entry.get().strip()
        working_dir = self.workdir_entry.get().strip()

        if not path:
            self._show_error("Please select an application file.")
            return

        if not name:
            self._show_error("Please enter a name for the application.")
            return

        self.on_add(name, path, arguments, working_dir)
        self.destroy()

    def _show_error(self, message: str):
        """Show error message dialog."""
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("Error")
        error_dialog.geometry("300x100")
        error_dialog.resizable(False, False)
        error_dialog.transient(self)
        error_dialog.grab_set()

        ctk.CTkLabel(error_dialog, text=message, wraplength=260).pack(pady=20)
        ctk.CTkButton(error_dialog, text="OK", width=80, command=error_dialog.destroy).pack()


class EditAppDialog(ctk.CTkToplevel):
    """Dialog for editing an existing application."""

    def __init__(self, parent, app_data: dict, on_save: Callable[[str, str, str, str], None]):
        """
        Initialize the Edit App dialog.

        Args:
            parent: Parent window
            app_data: Dict with 'name', 'path', 'arguments', 'working_dir' keys
            on_save: Callback function(name, path, arguments, working_dir) called when saved
        """
        super().__init__(parent)

        self.on_save = on_save
        self.app_data = app_data

        # Window setup
        self.title("Edit Application")
        self.geometry("500x300")
        self.resizable(False, False)

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 500) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 300) // 2
        self.geometry(f"+{x}+{y}")

        self._create_widgets()

    def _create_widgets(self):
        """Create dialog widgets."""
        # Main frame with padding
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Path display (readonly)
        path_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        path_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(path_frame, text="Application:", width=80, anchor="w").pack(side="left")

        self.path_entry = ctk.CTkEntry(path_frame, width=370, state="readonly")
        self.path_entry.pack(side="left")
        self.path_entry.configure(state="normal")
        self.path_entry.insert(0, self.app_data.get("path", ""))
        self.path_entry.configure(state="readonly")

        # Name input
        name_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(name_frame, text="Name:", width=80, anchor="w").pack(side="left")

        self.name_entry = ctk.CTkEntry(name_frame, width=370, placeholder_text="Enter a display name")
        self.name_entry.pack(side="left")
        self.name_entry.insert(0, self.app_data.get("name", ""))

        # Arguments input
        args_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        args_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(args_frame, text="Arguments:", width=80, anchor="w").pack(side="left")

        self.args_entry = ctk.CTkEntry(args_frame, width=370, placeholder_text="Command-line arguments (optional)")
        self.args_entry.pack(side="left")
        self.args_entry.insert(0, self.app_data.get("arguments", ""))

        # Working directory input
        workdir_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        workdir_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(workdir_frame, text="Working Dir:", width=80, anchor="w").pack(side="left")

        self.workdir_entry = ctk.CTkEntry(workdir_frame, width=370, placeholder_text="Working directory (optional)")
        self.workdir_entry.pack(side="left")
        self.workdir_entry.insert(0, self.app_data.get("working_dir", ""))

        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x")

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=100,
            fg_color="gray",
            hover_color="darkgray",
            command=self.destroy
        ).pack(side="right", padx=(10, 0))

        ctk.CTkButton(
            button_frame,
            text="Save",
            width=100,
            command=self._on_save_click
        ).pack(side="right")

    def _on_save_click(self):
        """Handle Save button click."""
        name = self.name_entry.get().strip()
        path = self.app_data.get("path", "")
        arguments = self.args_entry.get().strip()
        working_dir = self.workdir_entry.get().strip()

        if not name:
            self._show_error("Please enter a name for the application.")
            return

        self.on_save(name, path, arguments, working_dir)
        self.destroy()

    def _show_error(self, message: str):
        """Show error message dialog."""
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("Error")
        error_dialog.geometry("300x100")
        error_dialog.resizable(False, False)
        error_dialog.transient(self)
        error_dialog.grab_set()

        ctk.CTkLabel(error_dialog, text=message, wraplength=260).pack(pady=20)
        ctk.CTkButton(error_dialog, text="OK", width=80, command=error_dialog.destroy).pack()


class AddProfileDialog(ctk.CTkToplevel):
    """Dialog for creating a new profile."""

    def __init__(self, parent, on_create: Callable[[str], None], existing_profiles: list[str]):
        """
        Initialize the Add Profile dialog.

        Args:
            parent: Parent window
            on_create: Callback function(name) called when profile is created
            existing_profiles: List of existing profile names (for validation)
        """
        super().__init__(parent)

        self.on_create = on_create
        self.existing_profiles = [p.lower() for p in existing_profiles]

        # Window setup
        self.title("New Profile")
        self.geometry("350x150")
        self.resizable(False, False)

        # Set icon
        self._set_icon()

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 350) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 150) // 2
        self.geometry(f"+{x}+{y}")

        self._create_widgets()

    def _create_widgets(self):
        """Create dialog widgets."""
        # Main frame with padding
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Name input
        name_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(name_frame, text="Profile Name:", anchor="w").pack(fill="x")

        self.name_entry = ctk.CTkEntry(name_frame, placeholder_text="e.g., Work, Gaming, Creative")
        self.name_entry.pack(fill="x", pady=(5, 0))
        self.name_entry.focus()

        # Bind Enter key
        self.name_entry.bind("<Return>", lambda e: self._on_create_click())

        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x")

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=100,
            fg_color="gray",
            hover_color="darkgray",
            command=self.destroy
        ).pack(side="right", padx=(10, 0))

        ctk.CTkButton(
            button_frame,
            text="Create",
            width=100,
            command=self._on_create_click
        ).pack(side="right")

    def _set_icon(self):
        """Set the window icon."""
        try:
            import sys
            # Handle both running from source and from .exe
            if getattr(sys, 'frozen', False):
                # Running from .exe
                base_dir = sys._MEIPASS
            else:
                # Running from source
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            icon_path = os.path.join(base_dir, "assets", "icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            pass

    def _on_create_click(self):
        """Handle Create button click."""
        name = self.name_entry.get().strip()

        if not name:
            self._show_error("Please enter a profile name.")
            return

        if name.lower() in self.existing_profiles:
            self._show_error("A profile with this name already exists.")
            return

        self.on_create(name)
        self.destroy()

    def _show_error(self, message: str):
        """Show error message dialog."""
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("Error")
        error_dialog.geometry("300x100")
        error_dialog.resizable(False, False)
        error_dialog.transient(self)
        error_dialog.grab_set()

        ctk.CTkLabel(error_dialog, text=message, wraplength=260).pack(pady=20)
        ctk.CTkButton(error_dialog, text="OK", width=80, command=error_dialog.destroy).pack()


class ConfirmDialog(ctk.CTkToplevel):
    """Confirmation dialog with Yes/No options."""

    def __init__(self, parent, title: str, message: str, on_confirm: Callable[[], None]):
        """
        Initialize the confirmation dialog.

        Args:
            parent: Parent window
            title: Dialog title
            message: Message to display
            on_confirm: Callback function called when confirmed
        """
        super().__init__(parent)

        self.on_confirm = on_confirm

        # Window setup
        self.title(title)
        self.geometry("350x130")
        self.resizable(False, False)

        # Set icon
        self._set_icon()

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 350) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 130) // 2
        self.geometry(f"+{x}+{y}")

        self._create_widgets(message)

    def _create_widgets(self, message: str):
        """Create dialog widgets."""
        # Main frame
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Message
        ctk.CTkLabel(main_frame, text=message, wraplength=300).pack(pady=(0, 20))

        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x")

        ctk.CTkButton(
            button_frame,
            text="No",
            width=100,
            fg_color="gray",
            hover_color="darkgray",
            command=self.destroy
        ).pack(side="right", padx=(10, 0))

        ctk.CTkButton(
            button_frame,
            text="Yes",
            width=100,
            fg_color="#d9534f",
            hover_color="#c9302c",
            command=self._on_confirm_click
        ).pack(side="right")

    def _set_icon(self):
        """Set the window icon."""
        try:
            import sys
            # Handle both running from source and from .exe
            if getattr(sys, 'frozen', False):
                # Running from .exe
                base_dir = sys._MEIPASS
            else:
                # Running from source
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            icon_path = os.path.join(base_dir, "assets", "icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            pass

    def _on_confirm_click(self):
        """Handle confirm button click."""
        self.on_confirm()
        self.destroy()


class OptionsDialog(ctk.CTkToplevel):
    """Options/Settings dialog."""

    def __init__(self, parent, config, on_theme_change: Callable[[str], None]):
        """
        Initialize the Options dialog.

        Args:
            parent: Parent window
            config: ConfigManager instance
            on_theme_change: Callback when theme changes
        """
        super().__init__(parent)

        self.config = config
        self.on_theme_change = on_theme_change

        # Window setup
        self.title("Options")
        self.geometry("450x450")
        self.resizable(False, False)

        # Set icon
        self._set_icon()

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 450) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 450) // 2
        self.geometry(f"+{x}+{y}")

        self._create_widgets()

    def _create_widgets(self):
        """Create dialog widgets."""
        # Main frame
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        ctk.CTkLabel(
            main_frame,
            text="Settings",
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold")
        ).pack(anchor="w", pady=(0, 15))

        # Scrollable frame for settings
        settings_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        settings_frame.pack(fill="both", expand=True, pady=(0, 15))

        # Appearance Section
        ctk.CTkLabel(
            settings_frame,
            text="Appearance",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold")
        ).pack(anchor="w", pady=(0, 10))

        # Theme setting
        theme_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        theme_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(theme_frame, text="Theme:", width=130, anchor="w").pack(side="left")

        self.theme_var = ctk.StringVar(value=self.config.get_theme().capitalize())
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            variable=self.theme_var,
            values=["Dark", "Light", "System"],
            width=150,
            command=self._on_theme_select
        )
        theme_menu.pack(side="left")

        # Show icons setting
        icons_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        icons_frame.pack(fill="x", pady=(0, 15))

        self.show_icons_var = ctk.BooleanVar(value=self.config.get_setting("show_app_icons", True))
        ctk.CTkCheckBox(
            icons_frame,
            text="Show application icons",
            variable=self.show_icons_var,
            command=self._on_icons_toggle
        ).pack(side="left")

        # Behavior Section
        ctk.CTkLabel(
            settings_frame,
            text="Behavior",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold")
        ).pack(anchor="w", pady=(5, 10))

        # Launch delay setting
        delay_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        delay_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(delay_frame, text="Launch delay (ms):", width=130, anchor="w").pack(side="left")

        self.delay_var = ctk.StringVar(value=str(self.config.get_setting("launch_delay", 0)))
        delay_entry = ctk.CTkEntry(delay_frame, textvariable=self.delay_var, width=100)
        delay_entry.pack(side="left")
        delay_entry.bind("<FocusOut>", self._on_delay_change)

        # Minimize to tray
        tray_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        tray_frame.pack(fill="x", pady=(0, 8))

        self.minimize_tray_var = ctk.BooleanVar(value=self.config.get_setting("minimize_to_tray", True))
        ctk.CTkCheckBox(
            tray_frame,
            text="Minimize to system tray",
            variable=self.minimize_tray_var,
            command=self._on_minimize_tray_toggle
        ).pack(side="left")

        # Start minimized
        start_min_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        start_min_frame.pack(fill="x", pady=(0, 8))

        self.start_min_var = ctk.BooleanVar(value=self.config.get_setting("start_minimized", False))
        ctk.CTkCheckBox(
            start_min_frame,
            text="Start minimized",
            variable=self.start_min_var,
            command=self._on_start_min_toggle
        ).pack(side="left")

        # Auto-start with Windows
        autostart_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        autostart_frame.pack(fill="x", pady=(0, 8))

        self.autostart_var = ctk.BooleanVar(value=AutoStart.is_enabled())
        ctk.CTkCheckBox(
            autostart_frame,
            text="Start with Windows",
            variable=self.autostart_var,
            command=self._on_autostart_toggle
        ).pack(side="left")

        # Confirm on exit
        confirm_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        confirm_frame.pack(fill="x", pady=(0, 10))

        self.confirm_exit_var = ctk.BooleanVar(value=self.config.get_setting("confirm_on_exit", False))
        ctk.CTkCheckBox(
            confirm_frame,
            text="Confirm before exit",
            variable=self.confirm_exit_var,
            command=self._on_confirm_exit_toggle
        ).pack(side="left")

        # Close button
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x")

        ctk.CTkButton(
            button_frame,
            text="Close",
            width=100,
            height=32,
            command=self.destroy
        ).pack(side="right")

    def _set_icon(self):
        """Set the window icon."""
        try:
            import sys
            # Handle both running from source and from .exe
            if getattr(sys, 'frozen', False):
                # Running from .exe
                base_dir = sys._MEIPASS
            else:
                # Running from source
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            icon_path = os.path.join(base_dir, "assets", "icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            pass

    def _on_theme_select(self, value: str):
        """Handle theme selection."""
        theme = value.lower()
        self.config.set_theme(theme)
        self.on_theme_change(theme)

    def _on_icons_toggle(self):
        """Handle show icons toggle."""
        self.config.set_setting("show_app_icons", self.show_icons_var.get())

    def _on_delay_change(self, event=None):
        """Handle launch delay change."""
        try:
            delay = int(self.delay_var.get())
            if delay < 0:
                delay = 0
            self.config.set_setting("launch_delay", delay)
        except ValueError:
            self.delay_var.set("0")
            self.config.set_setting("launch_delay", 0)

    def _on_minimize_tray_toggle(self):
        """Handle minimize to tray toggle."""
        self.config.set_setting("minimize_to_tray", self.minimize_tray_var.get())

    def _on_start_min_toggle(self):
        """Handle start minimized toggle."""
        self.config.set_setting("start_minimized", self.start_min_var.get())

    def _on_confirm_exit_toggle(self):
        """Handle confirm on exit toggle."""
        self.config.set_setting("confirm_on_exit", self.confirm_exit_var.get())

    def _on_autostart_toggle(self):
        """Handle auto-start toggle."""
        if self.autostart_var.get():
            if not AutoStart.enable():
                self.autostart_var.set(False)
                self._show_options_error("Failed to enable auto-start. Make sure you have proper permissions.")
        else:
            if not AutoStart.disable():
                self.autostart_var.set(True)
                self._show_options_error("Failed to disable auto-start.")

    def _show_options_error(self, message: str):
        """Show error message."""
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("Error")
        error_dialog.geometry("350x120")
        error_dialog.resizable(False, False)
        error_dialog.transient(self)
        error_dialog.grab_set()

        # Center on parent
        error_dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - 350) // 2
        y = self.winfo_y() + (self.winfo_height() - 120) // 2
        error_dialog.geometry(f"350x120+{x}+{y}")

        ctk.CTkLabel(error_dialog, text=message, wraplength=300).pack(pady=20, padx=20)
        ctk.CTkButton(error_dialog, text="OK", width=80, command=error_dialog.destroy).pack()


class AboutDialog(ctk.CTkToplevel):
    """About/App Info dialog."""

    def __init__(self, parent, version: str, author: str):
        """
        Initialize the About dialog.

        Args:
            parent: Parent window
            version: App version string
            author: App author name
        """
        super().__init__(parent)

        self.version = version
        self.author = author

        # Window setup
        self.title("About FavApp Starter")
        self.geometry("400x300")
        self.resizable(False, False)

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 400) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 300) // 2
        self.geometry(f"+{x}+{y}")

        self._create_widgets()

    def _create_widgets(self):
        """Create dialog widgets."""
        # Main frame
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # App name
        ctk.CTkLabel(
            main_frame,
            text="FavApp Starter",
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold")
        ).pack(pady=(10, 5))

        # Version
        ctk.CTkLabel(
            main_frame,
            text=f"Version {self.version}",
            font=ctk.CTkFont(family="Roboto", size=14),
            text_color="gray"
        ).pack(pady=(0, 20))

        # Description
        ctk.CTkLabel(
            main_frame,
            text="Launch your favorite applications\nwith a single click.",
            font=ctk.CTkFont(family="Roboto", size=13),
            justify="center"
        ).pack(pady=(0, 20))

        # Author
        ctk.CTkLabel(
            main_frame,
            text=f"Created by {self.author}",
            font=ctk.CTkFont(family="Roboto", size=12),
            text_color="gray"
        ).pack(pady=(0, 10))

        # Spacer
        ctk.CTkFrame(main_frame, fg_color="transparent").pack(fill="both", expand=True)

        # Close button
        ctk.CTkButton(
            main_frame,
            text="Close",
            width=100,
            height=32,
            command=self.destroy
        ).pack(pady=(10, 0))


class LicenseDialog(ctk.CTkToplevel):
    """License information dialog."""

    MIT_LICENSE = """MIT License

Copyright (c) 2025 {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

    def __init__(self, parent, author: str):
        """
        Initialize the License dialog.

        Args:
            parent: Parent window
            author: Author name for the license
        """
        super().__init__(parent)

        self.author = author

        # Window setup
        self.title("License")
        self.geometry("550x450")
        self.resizable(False, False)

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 550) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 450) // 2
        self.geometry(f"+{x}+{y}")

        self._create_widgets()

    def _create_widgets(self):
        """Create dialog widgets."""
        # Main frame
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        ctk.CTkLabel(
            main_frame,
            text="MIT License",
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold")
        ).pack(anchor="w", pady=(0, 15))

        # License text in scrollable textbox
        license_text = self.MIT_LICENSE.format(author=self.author)

        textbox = ctk.CTkTextbox(
            main_frame,
            width=500,
            height=320,
            font=ctk.CTkFont(family="Consolas", size=11),
            wrap="word"
        )
        textbox.pack(fill="both", expand=True)
        textbox.insert("1.0", license_text)
        textbox.configure(state="disabled")

        # Close button
        ctk.CTkButton(
            main_frame,
            text="Close",
            width=100,
            height=32,
            command=self.destroy
        ).pack(pady=(15, 0))


class SearchAppsDialog(ctk.CTkToplevel):
    """Dialog for searching installed applications."""

    def __init__(self, parent, on_select: Callable[[str, str], None]):
        """
        Initialize the Search Apps dialog.

        Args:
            parent: Parent window
            on_select: Callback function(path, name) called when app is selected
        """
        super().__init__(parent)

        self.on_select = on_select
        self.apps = []
        self.filtered_apps = []

        # Window setup
        self.title("Search Installed Applications")
        self.geometry("600x500")
        self.resizable(True, True)

        # Set icon
        self._set_icon()

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 600) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 500) // 2
        self.geometry(f"600x500+{x}+{y}")

        self._create_widgets()
        self._load_apps()

    def _create_widgets(self):
        """Create dialog widgets."""
        # Main frame
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title and status
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            header_frame,
            text="Installed Applications",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold")
        ).pack(side="left")

        self.status_label = ctk.CTkLabel(
            header_frame,
            text="Loading...",
            font=ctk.CTkFont(family="Roboto", size=11),
            text_color="gray"
        )
        self.status_label.pack(side="right")

        # Search box
        search_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(search_frame, text="🔍", width=30).pack(side="left")

        self.search_var = ctk.StringVar()
        self.search_var.trace("w", lambda *args: self._filter_apps())
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search applications...",
            textvariable=self.search_var
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(5, 0))

        # App list in scrollable frame
        self.app_list_frame = ctk.CTkScrollableFrame(main_frame)
        self.app_list_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x")

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=100,
            fg_color="gray",
            hover_color="darkgray",
            command=self.destroy
        ).pack(side="right")

    def _set_icon(self):
        """Set the window icon."""
        try:
            import sys
            # Handle both running from source and from .exe
            if getattr(sys, 'frozen', False):
                # Running from .exe
                base_dir = sys._MEIPASS
            else:
                # Running from source
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            icon_path = os.path.join(base_dir, "assets", "icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            pass

    def _load_apps(self):
        """Load installed applications in background."""
        def load_thread():
            self.apps = AppFinder.find_installed_apps()
            self.filtered_apps = self.apps.copy()

            self.after(0, self._populate_list)

        threading.Thread(target=load_thread, daemon=True).start()

    def _populate_list(self):
        """Populate the app list with filtered results."""
        # Clear existing
        for widget in self.app_list_frame.winfo_children():
            widget.destroy()

        # Update status
        self.status_label.configure(text=f"{len(self.filtered_apps)} apps found")

        if not self.filtered_apps:
            ctk.CTkLabel(
                self.app_list_frame,
                text="No applications found" if not self.apps else "No matching applications",
                text_color="gray"
            ).pack(pady=20)
            return

        # Create app items
        for app in self.filtered_apps[:100]:  # Limit to 100 for performance
            self._create_app_item(app)

    def _create_app_item(self, app: dict):
        """Create a single app list item."""
        item_frame = ctk.CTkFrame(self.app_list_frame)
        item_frame.pack(fill="x", pady=2, padx=5)

        # App name and path
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=5)

        ctk.CTkLabel(
            info_frame,
            text=app["name"],
            font=ctk.CTkFont(family="Roboto", weight="bold"),
            anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            info_frame,
            text=app["path"],
            font=ctk.CTkFont(family="Roboto", size=10),
            text_color="gray",
            anchor="w"
        ).pack(fill="x")

        # Select button
        ctk.CTkButton(
            item_frame,
            text="Select",
            width=80,
            height=28,
            command=lambda: self._select_app(app)
        ).pack(side="right", padx=10)

    def _filter_apps(self):
        """Filter apps based on search query."""
        query = self.search_var.get().lower()

        if not query:
            self.filtered_apps = self.apps.copy()
        else:
            self.filtered_apps = [
                app for app in self.apps
                if query in app["name"].lower() or query in app["path"].lower()
            ]

        self._populate_list()

    def _select_app(self, app: dict):
        """Handle app selection."""
        self.on_select(app["path"], app["name"])
        self.destroy()
