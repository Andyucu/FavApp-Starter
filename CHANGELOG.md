# Changelog

All notable changes to FavApp Starter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [26.2.2] - 2026-02-02

### Added

- **`.favapp` File Extension Support** - Double-click profiles to launch apps
  - Export profiles as standalone `.favapp` files via Profile menu
  - Import profiles from `.favapp` files
  - Windows registry integration for file association
  - Double-click `.favapp` files to launch all apps in that profile
  - "Register .favapp file extension" option in Options dialog
  - Command-line argument support for opening `.favapp` files
  - Share profiles with others as portable files

- **Profile Export/Import UI**
  - Profile Menu → Export Profile... (saves as `.favapp`)
  - Profile Menu → Import Profiles... (supports `.favapp` and `.json`)
  - File dialogs with proper extension filtering

- **Programmatic Button Icons**
  - All icons now 24x24px with perfect 1:1 aspect ratio
  - Add Profile: Plus sign icon
  - Save Profile: Checkmark icon (black on green background)
  - Duplicate Profile: Overlapping rectangles icon
  - Delete Profile: X mark icon (black on red background)
  - Edit App: Pencil icon
  - Icons drawn with QPainter for consistent, crisp rendering

### Fixed

- **System tray reliability** - QSystemTrayIcon eliminates threading complexity
  - No more separate thread for tray icon (pystray requirement)
  - Thread-safe menu updates
  - Built-in Qt integration with event loop

- **Taskbar icon** - Application now displays correct icon in Windows taskbar
  - Added Windows AppUserModelID for proper taskbar icon grouping
  - Set application icon via `app.setWindowIcon()`

- **UI Layout Issues**
  - Fixed Browse button overlapping Application field in Add Application dialog
  - Changed text fields to use stretch layout instead of fixed widths
  - Increased profile name text field height to 32px in New Profile dialog


## [26.01.30] - 2026-01-25 

### Changed

- **Font styling** - Made fonts bolder throughout the application for better readability
  - Search button now uses bold font
  - Status labels use bold font

### Fixed

- **Dialog icons removed with delay** - Added delayed iconbitmap clearing to all dialogs
  - Using `self.after(10, lambda: self.iconbitmap(bitmap=''))` to remove icon after window loads
  - Applied to all 8 dialog classes (AddApp, EditApp, AddProfile, Confirm, Options, About, License, SearchApps)
  - Should eliminate the blue Tkinter icon from all secondary windows
- **Tray icon menu** - Profile menu now updates automatically when profiles are added, deleted, duplicated, or renamed
  - New profiles immediately appear in the tray icon menu
  - Deleted profiles are removed from the tray icon menu
  - Profile names update correctly when renamed
  - Tray menu refreshes automatically after any profile modification
  - Fixed path format issue - paths were using forward slashes (C:/...) instead of Windows backslashes (C:\...)
  -Theme changes now apply immediately without requiring app restart
  - Save button now applies theme on parent window after closing dialog
  - Icons now extract correctly from executables
  - Improved tray icon visibility with green fallback color (#2ea572)

---

## [26.01.14] - 2026-01-23

### Fixed

- **CRITICAL**: Dialog window icons (Options, About, License, etc.) now display correctly in .exe builds
  - All dialogs use absolute paths and delayed iconbitmap setting for better compatibility
  - Fixed icon loading for customtkinter Toplevel windows
- App icons now properly extracted from .lnk shortcut files
  - Added win32com.client support to resolve shortcut targets
  - Icons extracted from target executable instead of shortcut file

### Changed

- Launch All button color changed to green (#2fa572) for better visibility
- Search button in Add App dialog increased to size 14 font and width 120
- Search icon in Search Apps dialog increased to size 18 font
- All dialog _set_icon methods now use consistent implementation with absolute paths


## [26.01.12] - 2026-01-22

### Fixed

- **CRITICAL**: Theme changes no longer freeze the application (async theme application)
- **CRITICAL**: Export Profile functionality now correctly saves files to disk
- **CRITICAL**: Export All Profiles functionality now correctly saves files to disk
- All dialog window icons now display correctly (AboutDialog, LicenseDialog, EditAppDialog)
- Enhanced system tray icon debug logging for troubleshooting


### Changed

- Tray icon creation happens immediately at startup (100ms delay)
- Config.json location: next to .exe when frozen, project root when running from source
- App icon fallback: colored square with app's first letter when extraction fails
- Better exception handling throughout icon-related code


## [26.01.07] - 2026-01-22

### Added

- Search installed applications feature - find and add apps from your system
- Windows auto-start option in settings
- AppFinder utility to scan registry and common directories for installed apps
- "Search..." button in Add App dialog

### Changed

- Improved Search button visibility in Add App dialog with green color and search icon
- Increased button width and spacing for better UI clarity
- Reduced path entry width to accommodate more visible buttons


### Fixed

- Missing AutoStart import causing Windows auto-start option to not appear in settings
- Tooltip ghost images with improved cleanup and delayed rendering
- Application icon not updating properly in executable
- Icon display in README now shows new icon

## [26.01.04] - 2026-01-22

### Added

- App icon extraction and display in application list
- System tray support with minimize to tray option (requires pystray)
- Edit app functionality with dedicated dialog
- Search/filter bar to quickly find apps
- Double-click on app name to launch individual applications
- Tooltips on all buttons showing keyboard shortcuts
- Status bar at bottom showing last launch time and current status
- Window position and size memory (restored on startup)
- Launch delay option (configurable in Options)
- Import/export profiles feature (single or all profiles)
- Duplicate profile feature
- Rename profile feature
- App arguments and working directory support
- Comprehensive keyboard shortcuts (Ctrl+A, Ctrl+L, Ctrl+N, Ctrl+D, Ctrl+Q, Del, etc.)
- Visual polish with hover effects
- Expanded Options dialog with all new settings
- Profile menu in menu bar

### Changed

- App list items now show icons (when enabled), edit buttons, and support double-click to launch
- AddAppDialog now includes arguments and working directory fields
- Launch process runs in background thread with progress updates
- Enhanced app management with full CRUD operations

### Fixed

- Window geometry now properly saved and restored between sessions

---

## [26.01.03] - 2025-01-21

### Added

- Menu bar with File (Options, Exit) and About (App Info, License) menus
- Options dialog for theme settings (Dark, Light, System)
- About dialog showing app info and version
- License dialog displaying MIT License
- Custom application icon (blue/teal gradient bookmark with plus sign)

### Changed

- Buttons now have fixed sizes and don't stretch with window resize
- Moved theme toggle from header to Options dialog
- Updated LICENSE to Alexandru Teodorovici
- Improved README.md with detailed documentation

### Fixed

- Button layout consistency across different window sizes

---

## [26.01.02] - 2025-01-20

### Added

- Standalone .exe build support using PyInstaller
- PyInstaller spec file (FavApp.spec) for reproducible builds

### Changed

- Updated requirements.txt to include PyInstaller

---

## [26.01.01] - 2025-01-18

### Added
- Initial release of FavApp Starter
- Modern GUI using with dark/light theme support
- Profile system to organize apps by context (Work, Gaming, etc.)
- Add and remove applications via file picker
- Add and remove profiles
- One-click "Launch All" to open all apps in the selected profile
- Persistent configuration saved to JSON
- Theme toggle (dark/light mode)
- Profile switching with automatic app list update
