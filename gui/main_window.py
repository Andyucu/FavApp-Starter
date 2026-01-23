"""Main application window for FavApp Starter."""

import customtkinter as ctk
from tkinter import Menu, filedialog
from typing import Optional
import os
import threading
from datetime import datetime
from PIL import Image, ImageTk

from core.config import ConfigManager
from core.launcher import AppLauncher, IconExtractor
from .dialogs import AddAppDialog, EditAppDialog, AddProfileDialog, ConfirmDialog, OptionsDialog, AboutDialog, LicenseDialog

# Optional pystray import for system tray
try:
    import pystray
    from pystray import MenuItem as TrayMenuItem
    PYSTRAY_AVAILABLE = True
except ImportError:
    PYSTRAY_AVAILABLE = False


class MainWindow(ctk.CTk):
    """Main application window."""

    APP_VERSION = "26.01.11"
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

        # System tray
        self.tray_icon = None
        self.tray_thread = None

        # Icon cache for apps
        self.icon_cache = {}

        # Window setup
        self.title(f"FavApp Starter v{self.APP_VERSION}")

        # Restore window position and size
        window_cfg = self.config.get_setting("window", {})
        width = window_cfg.get("width", 550)
        height = window_cfg.get("height", 600)
        x = window_cfg.get("x")
        y = window_cfg.get("y")

        if x is not None and y is not None:
            self.geometry(f"{width}x{height}+{x}+{y}")
        else:
            self.geometry(f"{width}x{height}")

        self.minsize(450, 500)

        # Set icon if available
        self._set_icon()

        # Bind window close event
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Bind keyboard shortcuts
        self._bind_shortcuts()

        # Save window position on configure
        self.bind("<Configure>", self._on_window_configure)

        # Create menu bar
        self._create_menu()

        # Create widgets
        self._create_widgets()

        # Load initial data
        self._refresh_profile_list()
        self._refresh_app_list()

        # Create system tray icon immediately
        self.after(100, self._init_tray_icon)

        # Start minimized if configured
        if self.config.get_setting("start_minimized", False):
            self.after(200, self._minimize_to_tray)

    def _set_icon(self):
        """Set the application icon."""
        import sys
        # Handle both running from source and from .exe
        if getattr(sys, 'frozen', False):
            # Running from .exe
            base_dir = sys._MEIPASS
        else:
            # Running from source
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
        file_menu.add_command(label="Options", command=self._show_options, accelerator="Ctrl+,")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_close, accelerator="Ctrl+Q")

        # Profile menu
        profile_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Profile", menu=profile_menu)
        profile_menu.add_command(label="New Profile", command=self._show_add_profile_dialog, accelerator="Ctrl+N")
        profile_menu.add_command(label="Duplicate Profile", command=self._duplicate_profile, accelerator="Ctrl+D")
        profile_menu.add_command(label="Rename Profile", command=self._rename_profile)
        profile_menu.add_separator()
        profile_menu.add_command(label="Export Profile...", command=self._export_profile)
        profile_menu.add_command(label="Export All Profiles...", command=self._export_all_profiles)
        profile_menu.add_command(label="Import Profiles...", command=self._import_profiles)

        # About menu
        about_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="App Info", command=self._show_about)
        about_menu.add_command(label="License", command=self._show_license)

    def _create_widgets(self):
        """Create all window widgets."""
        # Main container with padding
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=(15, 0))

        # Header with title
        self._create_header()

        # Profile section
        self._create_profile_section()

        # Search bar
        self._create_search_bar()

        # App list section
        self._create_app_list_section()

        # Bottom section with fixed-size buttons
        self._create_bottom_section()

        # Status bar
        self._create_status_bar()

    def _create_header(self):
        """Create header with title."""
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))

        # Title
        ctk.CTkLabel(
            header_frame,
            text="FavApp Starter",
            font=ctk.CTkFont(family="Roboto", size=20, weight="bold")
        ).pack(side="left")

    def _create_search_bar(self):
        """Create search/filter bar."""
        search_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(search_frame, text="🔍", width=30).pack(side="left", padx=(0, 5))

        self.search_var = ctk.StringVar()
        self.search_var.trace("w", lambda *args: self._on_search_change())
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search apps...",
            textvariable=self.search_var
        )
        self.search_entry.pack(side="left", fill="x", expand=True)

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
            text="➕",
            width=40,
            height=40,
            font=ctk.CTkFont(family="Segoe UI Emoji", size=18),
            command=self._show_add_profile_dialog
        )
        self.add_profile_btn.pack(side="left", padx=(0, 5))
        self._create_tooltip(self.add_profile_btn, "New Profile (Ctrl+N)")

        # Save profile button - fixed size
        self.save_profile_btn = ctk.CTkButton(
            profile_frame,
            text="💾",
            width=40,
            height=40,
            font=ctk.CTkFont(family="Segoe UI Emoji", size=18),
            fg_color="#2fa572",
            hover_color="#28a164",
            command=self._save_profile
        )
        self.save_profile_btn.pack(side="left", padx=(0, 5))
        self._create_tooltip(self.save_profile_btn, "Save Profile")

        # Duplicate profile button - fixed size
        self.duplicate_profile_btn = ctk.CTkButton(
            profile_frame,
            text="📋",
            width=40,
            height=40,
            font=ctk.CTkFont(family="Segoe UI Emoji", size=18),
            command=self._duplicate_profile
        )
        self.duplicate_profile_btn.pack(side="left", padx=(0, 5))
        self._create_tooltip(self.duplicate_profile_btn, "Duplicate Profile (Ctrl+D)")

        # Delete profile button - fixed size
        self.delete_profile_btn = ctk.CTkButton(
            profile_frame,
            text="🗑️",
            width=40,
            height=40,
            font=ctk.CTkFont(family="Segoe UI Emoji", size=18),
            fg_color="#d9534f",
            hover_color="#c9302c",
            command=self._delete_profile
        )
        self.delete_profile_btn.pack(side="left")
        self._create_tooltip(self.delete_profile_btn, "Delete Profile")

    def _create_app_list_section(self):
        """Create the application list section."""
        # Frame for the list
        list_frame = ctk.CTkFrame(self.main_frame)
        list_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Label
        ctk.CTkLabel(
            list_frame,
            text="Applications:",
            font=ctk.CTkFont(family="Roboto", weight="bold")
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
        self._create_tooltip(self.add_app_btn, "Add Application (Ctrl+A)")

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
        self._create_tooltip(self.remove_btn, "Remove Selected Apps (Del)")

        # Launch button - fixed size, centered
        launch_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        launch_frame.pack()

        self.launch_btn = ctk.CTkButton(
            launch_frame,
            text="▶  LAUNCH ALL",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=220,
            height=45,
            command=self._launch_all
        )
        self.launch_btn.pack()
        self._create_tooltip(self.launch_btn, "Launch All Apps (Ctrl+L)")

    def _create_status_bar(self):
        """Create status bar at bottom."""
        status_frame = ctk.CTkFrame(self, fg_color="transparent", height=25)
        status_frame.pack(fill="x", side="bottom", padx=15, pady=(0, 5))

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready",
            font=ctk.CTkFont(family="Roboto", size=10),
            text_color="gray",
            anchor="w"
        )
        self.status_label.pack(side="left", fill="x", expand=True)

        # Show last launch time if available
        last_launch = self.config.get_setting("last_launch")
        if last_launch:
            try:
                dt = datetime.fromisoformat(last_launch)
                self.status_label.configure(text=f"Last launch: {dt.strftime('%Y-%m-%d %H:%M')}")
            except:
                pass

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

        # Apply search filter
        search_query = self.search_var.get().lower() if hasattr(self, 'search_var') else ""
        if search_query:
            apps = [app for app in apps if search_query in app.get("name", "").lower() or
                    search_query in app.get("path", "").lower()]

        if not apps:
            # Show empty state
            empty_text = "No matching apps found." if search_query else "No apps added yet.\nClick 'Add App' to get started."
            empty_label = ctk.CTkLabel(
                self.app_list_frame,
                text=empty_text,
                text_color="gray"
            )
            empty_label.pack(pady=20)
            self.app_items.append(empty_label)
            self.remove_btn.configure(state="disabled")
            return

        # Create app items
        for i, app in enumerate(apps):
            item = self._create_app_item(i, app)
            self.app_items.append(item)

    def _create_app_item(self, index: int, app: dict) -> ctk.CTkFrame:
        """Create a single app item widget."""
        name = app.get("name", "Unknown")
        path = app.get("path", "")

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

        # Store data on frame
        item_frame.selected_var = selected_var
        item_frame.app_index = index
        item_frame.app_data = app

        # App icon
        if self.config.get_setting("show_app_icons", True):
            icon_label = self._create_app_icon(item_frame, path)
            icon_label.pack(side="left", padx=(5, 10))

        # App info
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, pady=5)

        name_label = ctk.CTkLabel(
            info_frame,
            text=name,
            font=ctk.CTkFont(family="Roboto", weight="bold"),
            anchor="w",
            cursor="hand2"
        )
        name_label.pack(fill="x")
        name_label.bind("<Double-Button-1>", lambda e: self._launch_single_app(app))
        self._create_tooltip(name_label, "Double-click to launch")

        path_text = path
        if app.get("arguments"):
            path_text += f" {app['arguments']}"

        ctk.CTkLabel(
            info_frame,
            text=path_text,
            font=ctk.CTkFont(family="Roboto", size=11),
            text_color="gray",
            anchor="w"
        ).pack(fill="x")

        # Edit button
        edit_btn = ctk.CTkButton(
            item_frame,
            text="✏️",
            width=35,
            height=35,
            font=ctk.CTkFont(family="Segoe UI Emoji", size=16),
            command=lambda: self._edit_app(index, app)
        )
        edit_btn.pack(side="right", padx=(5, 10))
        self._create_tooltip(edit_btn, "Edit App")

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

    def _save_profile(self):
        """Manually save the current profile configuration."""
        try:
            self.config.save()
            # Show brief status message
            self.status_label.configure(text="✓ Profile saved successfully")
            self.after(2000, lambda: self.status_label.configure(text=f"FavApp Starter v{self.APP_VERSION}"))
        except Exception as e:
            self._show_message("Save Error", f"Failed to save profile: {str(e)}")

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

    def _add_app(self, name: str, path: str, arguments: str = "", working_dir: str = ""):
        """Add a new app to the current profile."""
        if self.config.add_app(name, path, arguments, working_dir):
            self._refresh_app_list()
            self.status_label.configure(text=f"Added: {name}")

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

        # Get launch delay from config
        delay_ms = self.config.get_setting("launch_delay", 0)

        # Update status
        self.status_label.configure(text=f"Launching {len(apps)} apps...")
        self.launch_btn.configure(state="disabled")

        def launch_thread():
            # Launch apps with progress callback
            def progress_cb(current, total, app_name):
                self.after(0, lambda: self.status_label.configure(
                    text=f"Launching {current}/{total}: {app_name}"
                ))

            results = AppLauncher.launch_multiple(apps, delay_ms=delay_ms, progress_callback=progress_cb)

            # Update last launch time
            self.config.set_setting("last_launch", datetime.now().isoformat())

            # Check for errors
            errors = [r for r in results if not r["success"]]

            def update_ui():
                self.launch_btn.configure(state="normal")

                if errors:
                    error_msg = "\n".join([f"• {r['name']}: {r['error']}" for r in errors])
                    self.status_label.configure(text=f"Launch completed with {len(errors)} error(s)")
                    self._show_message(
                        "Launch Errors",
                        f"Some apps failed to launch:\n\n{error_msg}"
                    )
                else:
                    # Brief success indicator
                    self.launch_btn.configure(text="✓ Launched!", fg_color="green")
                    last_launch_time = datetime.now().strftime('%Y-%m-%d %H:%M')
                    self.status_label.configure(text=f"Last launch: {last_launch_time}")
                    self.after(1500, lambda: self.launch_btn.configure(
                        text="▶  LAUNCH ALL",
                        fg_color=["#3B8ED0", "#1F6AA5"]
                    ))

            self.after(0, update_ui)

        # Run in thread to avoid blocking UI
        threading.Thread(target=launch_thread, daemon=True).start()

    def _create_app_icon(self, parent, path: str) -> ctk.CTkLabel:
        """Create app icon widget."""
        # Check cache
        cache_key = f"{path}_40x40"
        if cache_key in self.icon_cache:
            icon_image = self.icon_cache[cache_key]
        else:
            try:
                # Extract icon
                pil_image = IconExtractor.get_icon(path, size=48)
                if not pil_image or pil_image.size[0] == 0:
                    # If extraction failed, create a default colored square
                    pil_image = Image.new('RGBA', (48, 48), (100, 149, 237, 255))  # Cornflower blue
                    # Draw first letter of app name if possible
                    from PIL import ImageDraw, ImageFont
                    draw = ImageDraw.Draw(pil_image)
                    try:
                        # Get app name from path
                        app_name = os.path.basename(path).split('.')[0]
                        letter = app_name[0].upper() if app_name else "?"
                        # Draw letter in center
                        draw.text((24, 24), letter, fill=(255, 255, 255, 255), anchor="mm")
                    except:
                        pass

                # Convert to CTkImage
                icon_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(40, 40))
                self.icon_cache[cache_key] = icon_image
            except Exception as e:
                # Fallback to simple default icon
                pil_image = Image.new('RGBA', (40, 40), (128, 128, 128, 255))
                icon_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(40, 40))
                self.icon_cache[cache_key] = icon_image

        icon_label = ctk.CTkLabel(parent, image=icon_image, text="")
        return icon_label

    def _create_tooltip(self, widget, text: str):
        """Create a tooltip for a widget."""
        tooltip_window = None
        after_id = None

        def destroy_tooltip():
            """Safely destroy the tooltip."""
            nonlocal tooltip_window, after_id
            if after_id:
                widget.after_cancel(after_id)
                after_id = None
            if tooltip_window:
                try:
                    tooltip_window.destroy()
                except:
                    pass
                tooltip_window = None

        def on_enter(event):
            nonlocal tooltip_window, after_id
            # Clear any existing tooltip
            destroy_tooltip()

            # Create tooltip after a small delay
            def show_tooltip():
                nonlocal tooltip_window
                try:
                    tooltip_window = ctk.CTkToplevel(widget)
                    tooltip_window.wm_overrideredirect(True)
                    tooltip_window.wm_attributes("-topmost", True)

                    # Position tooltip
                    x = event.x_root + 10
                    y = event.y_root + 10
                    tooltip_window.wm_geometry(f"+{x}+{y}")

                    # Create label
                    label = ctk.CTkLabel(
                        tooltip_window,
                        text=text,
                        fg_color=("gray75", "gray25"),
                        corner_radius=6,
                        padx=8,
                        pady=4
                    )
                    label.pack()

                    # Update to ensure proper rendering
                    tooltip_window.update_idletasks()
                except:
                    pass

            after_id = widget.after(500, show_tooltip)

        def on_leave(event):
            destroy_tooltip()

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def _bind_shortcuts(self):
        """Bind keyboard shortcuts."""
        self.bind("<Control-q>", lambda e: self._on_close())
        self.bind("<Control-a>", lambda e: self._show_add_app_dialog())
        self.bind("<Control-n>", lambda e: self._show_add_profile_dialog())
        self.bind("<Control-d>", lambda e: self._duplicate_profile())
        self.bind("<Control-l>", lambda e: self._launch_all())
        self.bind("<Control-comma>", lambda e: self._show_options())
        self.bind("<Delete>", lambda e: self._remove_selected_app())

    def _on_window_configure(self, event):
        """Save window position and size."""
        if event.widget == self and self.state() == "normal":
            # Debounce saves
            if hasattr(self, '_save_timer'):
                self.after_cancel(self._save_timer)

            def save_geometry():
                self.config.set_setting("window", {
                    "x": self.winfo_x(),
                    "y": self.winfo_y(),
                    "width": self.winfo_width(),
                    "height": self.winfo_height()
                })

            self._save_timer = self.after(500, save_geometry)

    def _on_search_change(self):
        """Handle search text change."""
        self._refresh_app_list()

    def _edit_app(self, index: int, app_data: dict):
        """Show edit dialog for an app."""
        def on_save(name: str, path: str, arguments: str, working_dir: str):
            if self.config.update_app(index, name, path, arguments, working_dir):
                self._refresh_app_list()
                self.status_label.configure(text=f"Updated: {name}")

        EditAppDialog(self, app_data, on_save=on_save)

    def _launch_single_app(self, app: dict):
        """Launch a single application."""
        name = app.get("name", "Unknown")
        path = app.get("path", "")
        arguments = app.get("arguments", "")
        working_dir = app.get("working_dir", "")

        self.status_label.configure(text=f"Launching {name}...")

        success, error = AppLauncher.launch_app(path, arguments, working_dir)

        if success:
            self.status_label.configure(text=f"Launched: {name}")
        else:
            self.status_label.configure(text=f"Failed to launch: {name}")
            self._show_message("Launch Error", f"Failed to launch {name}:\n\n{error}")

    def _duplicate_profile(self):
        """Duplicate the current profile."""
        current = self.config.get_active_profile()
        new_name = f"{current} (Copy)"

        # Find unique name
        counter = 2
        while new_name in self.config.get_profiles():
            new_name = f"{current} (Copy {counter})"
            counter += 1

        if self.config.duplicate_profile(current, new_name):
            self.config.set_active_profile(new_name)
            self._refresh_profile_list()
            self._refresh_app_list()
            self.status_label.configure(text=f"Duplicated profile: {new_name}")

    def _rename_profile(self):
        """Rename the current profile."""
        current = self.config.get_active_profile()

        # Simple input dialog
        dialog = ctk.CTkInputDialog(
            text=f"Enter new name for profile '{current}':",
            title="Rename Profile"
        )
        new_name = dialog.get_input()

        if new_name and new_name != current:
            if new_name in self.config.get_profiles():
                self._show_message("Error", "A profile with this name already exists.")
            elif self.config.rename_profile(current, new_name):
                self._refresh_profile_list()
                self.status_label.configure(text=f"Renamed profile to: {new_name}")

    def _export_profile(self):
        """Export current profile to JSON file."""
        profile = self.config.get_active_profile()
        filepath = filedialog.asksaveasfilename(
            title="Export Profile",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"{profile}.json"
        )

        if filepath:
            if self.config.export_profile(profile, filepath):
                self.status_label.configure(text=f"Exported: {profile}")
                self._show_message("Success", f"Profile '{profile}' exported successfully.")
            else:
                self._show_message("Error", "Failed to export profile.")

    def _export_all_profiles(self):
        """Export all profiles to JSON file."""
        filepath = filedialog.asksaveasfilename(
            title="Export All Profiles",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="favapp_profiles.json"
        )

        if filepath:
            if self.config.export_all_profiles(filepath):
                self.status_label.configure(text="Exported all profiles")
                self._show_message("Success", "All profiles exported successfully.")
            else:
                self._show_message("Error", "Failed to export profiles.")

    def _import_profiles(self):
        """Import profiles from JSON file."""
        filepath = filedialog.askopenfilename(
            title="Import Profiles",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filepath:
            result = self.config.import_profiles(filepath)
            if result:
                imported, skipped = result
                self._refresh_profile_list()
                self._refresh_app_list()
                msg = f"Imported {imported} profile(s)."
                if skipped:
                    msg += f"\n{skipped} profile(s) skipped (already exist)."
                self.status_label.configure(text=f"Imported {imported} profile(s)")
                self._show_message("Import Complete", msg)
            else:
                self._show_message("Error", "Failed to import profiles.")

    def _init_tray_icon(self):
        """Initialize system tray icon at startup."""
        if PYSTRAY_AVAILABLE and not self.tray_icon:
            try:
                self._create_tray_icon()
                print("Tray icon created successfully")  # Debug
            except Exception as e:
                print(f"Failed to create tray icon: {e}")  # Debug

    def _minimize_to_tray(self):
        """Minimize window to system tray."""
        if not PYSTRAY_AVAILABLE or not self.config.get_setting("minimize_to_tray", True):
            self.iconify()
            return

        # Hide window
        self.withdraw()

        # Create tray icon if not exists
        if not self.tray_icon:
            self._create_tray_icon()

    def _create_tray_icon(self):
        """Create system tray icon."""
        if not PYSTRAY_AVAILABLE:
            return

        # Load icon image
        import sys
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Try PNG first for better tray icon compatibility
        icon_path_png = os.path.join(base_dir, "assets", "icon.png")
        icon_path_ico = os.path.join(base_dir, "assets", "icon.ico")

        icon_image = None
        if os.path.exists(icon_path_png):
            try:
                icon_image = Image.open(icon_path_png)
                # Resize to reasonable tray icon size
                icon_image = icon_image.resize((64, 64), Image.Resampling.LANCZOS)
            except:
                icon_image = None

        if icon_image is None and os.path.exists(icon_path_ico):
            try:
                icon_image = Image.open(icon_path_ico)
                icon_image = icon_image.resize((64, 64), Image.Resampling.LANCZOS)
            except:
                icon_image = None

        if icon_image is None:
            try:
                icon_image = IconExtractor.get_default_icon(size=64)
            except:
                # Last resort: create a simple blue square
                icon_image = Image.new('RGBA', (64, 64), (100, 149, 237, 255))

        # Create profile menu items
        profiles = self.config.get_profiles()
        profile_items = []
        for profile_name in sorted(profiles.keys()):
            profile_items.append(
                TrayMenuItem(
                    profile_name,
                    lambda p=profile_name: self.after(0, lambda: self._launch_profile_from_tray(p))
                )
            )

        # Create menu
        if profile_items:
            menu = pystray.Menu(
                TrayMenuItem("Show", self._show_from_tray, default=True),
                pystray.Menu.SEPARATOR,
                TrayMenuItem("Launch Profiles", pystray.Menu(*profile_items)),
                pystray.Menu.SEPARATOR,
                TrayMenuItem("Exit", self._exit_from_tray)
            )
        else:
            menu = pystray.Menu(
                TrayMenuItem("Show", self._show_from_tray, default=True),
                pystray.Menu.SEPARATOR,
                TrayMenuItem("Exit", self._exit_from_tray)
            )

        # Create icon
        self.tray_icon = pystray.Icon("FavApp", icon_image, "FavApp Starter", menu)

        # Run in thread
        self.tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        self.tray_thread.start()

    def _show_from_tray(self):
        """Show window from system tray."""
        self.after(0, self.deiconify)

    def _launch_profile_from_tray(self, profile_name: str):
        """Launch all apps from a specific profile via tray icon."""
        # Get apps from the profile
        apps = self.config.get_apps(profile_name)
        if not apps:
            return

        # Launch each app
        for app_data in apps:
            try:
                self.launcher.launch(
                    app_data["path"],
                    app_data.get("arguments", ""),
                    app_data.get("working_dir", "")
                )
            except Exception as e:
                print(f"Error launching {app_data.get('name', 'Unknown')}: {e}")

    def _exit_from_tray(self):
        """Exit from system tray."""
        self.after(0, self.quit)

    def _on_close(self):
        """Handle window close event."""
        if self.config.get_setting("confirm_on_exit", False):
            ConfirmDialog(
                self,
                title="Exit FavApp Starter",
                message="Are you sure you want to exit?",
                on_confirm=self._do_close
            )
        else:
            self._do_close()

    def _do_close(self):
        """Actually close the application."""
        # Stop tray icon if running
        if self.tray_icon:
            self.tray_icon.stop()

        self.quit()

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
