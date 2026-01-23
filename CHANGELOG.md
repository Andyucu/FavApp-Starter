# Changelog

All notable changes to FavApp Starter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [26.01.09] - 2026-01-23

### Added

- System tray icon now appears at application startup (always visible)
- Larger, clearer icons for all buttons using emoji fonts

### Changed

- Profile buttons (Add, Duplicate, Delete) now use clearer emoji icons (➕, 📋, 🗑️) at 40x40 size
- Edit app button icon improved to ✏️ emoji at 35x35 size
- Launch All button increased to 300x55 with larger font (size 18)
- Search button in Add App dialog now larger with improved icon
- App icons in list increased from 32x32 to 40x40 for better visibility
- README icon resized to 15% of original (153x153) for better page layout
- Rebuilt icon.ico from source for all dialog windows

### Fixed

- System tray icon not visible - now created at startup instead of only on minimize
- App icons extracted at higher resolution (48px) for better quality
- Dialog window icons properly display new app icon

---

## [26.01.08] - 2026-01-23

### Added

- System tray icon with profile selection menu - "Launch Profiles" submenu
- Application icon displayed on all dialog windows
- Modern Roboto font throughout the entire application

### Changed

- Add Application dialog width increased to 600px
- Path entry field width increased to 300px
- All dialog windows display FavApp Starter icon
- Improved UI consistency with Roboto font family

### Fixed

- Search button fully visible in Add App dialog
- All dialog windows properly sized

---

## [26.01.07] - 2026-01-22

### Changed

- Improved Search button visibility in Add App dialog with green color and search icon
- Increased button width and spacing for better UI clarity
- Reduced path entry width to accommodate more visible buttons

---

## [26.01.06] - 2026-01-22

### Fixed

- Missing AutoStart import causing Windows auto-start option to not appear in settings
- Tooltip ghost images with improved cleanup and delayed rendering
- Application icon not updating properly in executable
- Icon display in README now shows new icon

### Changed

- Tooltip now shows after 500ms delay for better UX
- Build process now creates version-specific build folders (Build_v26.01.06)

---

## [26.01.05] - 2026-01-22

### Added

- Search installed applications feature - find and add apps from your system
- Windows auto-start option in settings
- AppFinder utility to scan registry and common directories for installed apps
- "Search..." button in Add App dialog

### Changed

- Updated application icon with new design
- Improved tooltip implementation to prevent ghost images

### Fixed

- Tooltip artifacts that remained visible after mouse left widget
- Better cleanup of tooltip windows

---

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

## [26.01.03] - 2025-01-22

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

## [26.01.02] - 2025-01-22

### Added

- Standalone .exe build support using PyInstaller
- PyInstaller spec file (FavApp.spec) for reproducible builds

### Changed

- Updated requirements.txt to include PyInstaller

---

## [26.01.01] - 2025-01-22

### Added
- Initial release of FavApp Starter
- Modern GUI using customtkinter with dark/light theme support
- Profile system to organize apps by context (Work, Gaming, etc.)
- Add and remove applications via file picker
- Add and remove profiles
- One-click "Launch All" to open all apps in the selected profile
- Persistent configuration saved to JSON
- Theme toggle (dark/light mode)
- Profile switching with automatic app list update
