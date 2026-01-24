# Changelog

All notable changes to FavApp Starter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [26.01.24] - 2026-01-24

### Changed

- **Search button styling** - Add Application dialog Search button now matches Browse button size
  - Width changed from 120 to 85 pixels
  - Font size changed from 16 to 13
  - Maintains green background color for better visibility
  - Improved UI consistency between similar buttons

---

## [26.01.23] - 2026-01-24

### Fixed

- **About dialog icon** - Fixed AboutDialog window icon not displaying correctly
  - Removed delayed icon setting (.after) and default= parameter
  - Now uses direct iconbitmap() call like other dialogs
  - All dialog windows now display the correct FavApp icon in the title bar

---

## [26.01.22] - 2026-01-24

### Fixed

- **CRITICAL**: Fixed 64-bit handle overflow in icon extraction
  - Icon extraction was failing with "int too long to convert" error on 64-bit Windows
  - Added explicit ctypes argument type definitions for all Windows API functions
  - GetIconInfo, GetObjectW, GetDC, CreateCompatibleDC, GetDIBits now properly handle 64-bit handles
  - All cleanup functions (DeleteDC, ReleaseDC, DeleteObject) also updated for 64-bit compatibility
  - Icons should now extract successfully on all Windows systems

---

## [26.01.21] - 2026-01-24

### Fixed

- **CRITICAL**: App icon extraction now works correctly
  - Fixed path format issue - paths were using forward slashes (C:/...) instead of Windows backslashes (C:\...)
  - Added os.path.normpath() to normalize paths before calling SHGetFileInfoW API
  - Debug log revealed all icon extraction attempts were failing with result: 0 due to path format
  - App icons should now display correctly for all applications

---

## [26.01.20] - 2026-01-24

### Added

- **Debug logging system** - Comprehensive logging to debug.log file
  - Log file created in application directory (next to .exe or in project root)
  - All icon extraction attempts logged with detailed diagnostic information
  - FavApp Starter icon loading process fully logged
  - App icon extraction pipeline logged at every step
  - Helps diagnose icon display issues with complete trace information

### Changed

- Search icon in main window enlarged 2x (emoji font size 24)
- All print statements replaced with debug logger throughout icon extraction code
- Better visibility for search functionality in main window

---

## [26.01.19] - 2026-01-24

### Fixed

- **CRITICAL**: Theme changes now apply immediately without requiring app restart
  - Save button now applies theme on parent window after closing dialog
  - Fixed modal dialog blocking issue by scheduling theme change on parent after dialog destroyed
  - Theme is correctly applied to main window while dialog is being destroyed
- **CRITICAL**: All dialog window icons now display correctly (About, Options, Add App, etc.)
  - Removed unnecessary delays and simplified icon setting
  - Direct iconbitmap() call without default parameter
  - Fixed icon display in all 6 dialogs

### Changed

- Search icon significantly enlarged in Add App dialog (font size 14 → 16)
- Search icon significantly enlarged in Search Apps dialog (emoji size 18 → 22)
- README icon resized from 51x51 to 56x56 pixels (10% larger)
- Enhanced icon extraction debugging with comprehensive logging throughout pipeline
- Improved fallback icon rendering with larger, more visible font (32pt Arial)

### Documentation

- Updated README.md with GPLv3 license information
- Added .msc and .msi to supported file types documentation
- Consolidated license information - now shown in About dialog only

---

## [26.01.18] - 2026-01-23

### Added

- **Save button in Options dialog** - Settings now require explicit Save to apply
  - Green Save button applies all changes and closes dialog
  - Close button cancels changes and reverts theme to original
  - Theme changes only applied when Save is clicked
  - Better user control over settings changes

### Fixed

- **CRITICAL**: App icon extraction now has extensive debug logging
  - Added detailed console output for every icon extraction attempt
  - Shows success/failure status for each app's icon
  - Logs .lnk resolution process
  - Fallback icon now uses larger, more visible font
  - Stack traces printed for all icon extraction errors

### Changed

- Options dialog now uses Save/Close pattern instead of auto-save
- Theme selection stored temporarily until Save is clicked
- X button (close) now acts as Cancel and reverts changes

---

## [26.01.17] - 2026-01-23

### Fixed

- **CRITICAL**: Theme changes now work correctly - REAL FIX
  - Root cause identified: OptionsDialog is modal (grab_set) which blocks parent window
  - Theme is now applied AFTER dialog closes, not while it's open
  - Prevents UI freezing and application becoming unresponsive
  - Added _on_close() handler to apply theme changes on dialog close
  - Theme selection stored and applied with 100ms delay after dialog destruction
- **CRITICAL**: Tray icon profile launching now actually launches apps
  - Fixed missing AppLauncher implementation in tray menu
  - Apps from selected profile now launch correctly from system tray
  - Uses launch_multiple() with proper threading to avoid blocking
  - Added debug logging for tray profile launches

### Changed

- Theme application now uses full update() instead of update_idletasks() for complete refresh
- Tray profile launcher runs in background thread for better responsiveness

---

## [26.01.16] - 2026-01-23

### Fixed

- **CRITICAL**: Theme changes now work properly without freezing or breaking the UI
  - Added update_idletasks() call to force UI refresh after theme change
  - Theme change now refreshes app list to apply theme to all widgets
  - OptionsDialog theme handler improved with proper update sequence
  - Application remains responsive during and after theme changes

---

## [26.01.15] - 2026-01-23

### Fixed

- **CRITICAL**: System tray icon now appears and functions correctly
  - Complete rewrite of tray icon initialization with better error handling
  - Fixed icon loading priority (ICO before PNG) for Windows compatibility
  - Improved lambda functions in menu to prevent closure issues
  - Added extensive debug logging to track icon creation process
  - Tray icon now properly converts to RGBA mode if needed
- App icon extraction significantly improved with debug logging
  - Icons now extract correctly from executables
  - Better fallback handling when extraction fails
  - Added logging to track extraction success/failure

### Changed

- **LICENSE CHANGE**: Changed from MIT License to GNU General Public License v3.0
- About dialog now includes full GPLv3 license text (no separate license window)
- About dialog expanded to 500x550 to accommodate license information
- Removed separate "License" menu item and LicenseDialog class
- Add App and Remove Selected buttons now same size (130px width)
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

---

## [26.01.13] - 2026-01-23

### Fixed

- **CRITICAL**: System tray icon now appears correctly (fixed profile iteration bug in _create_tray_icon)
  - Bug was calling .keys() on a list returned by get_profiles()
  - Tray icon thread was crashing silently on startup
- Tray icon profile menu now populates properly with all profiles
- Theme changes remain non-blocking (from v26.01.12)

### Changed

- Build output now organized in versioned folders (dist/v26.01.XX/) for easier release management
- Each release now has its own dedicated build folder

---

## [26.01.12] - 2026-01-23

### Fixed

- **CRITICAL**: Theme changes no longer freeze the application (async theme application)
- **CRITICAL**: Export Profile functionality now correctly saves files to disk
- **CRITICAL**: Export All Profiles functionality now correctly saves files to disk
- All dialog window icons now display correctly (AboutDialog, LicenseDialog, EditAppDialog)
- Enhanced system tray icon debug logging for troubleshooting

### Changed

- Theme changes applied asynchronously (10ms delay) to prevent UI freezing
- All dialogs now have standardized _set_icon() method implementation
- Improved error handling in export functions

---

## [26.01.11] - 2026-01-23

### Added

- Save Profile button (💾) next to New Profile button for manual saves
- Fallback icon rendering when exe icon extraction fails (shows first letter of app name)
- Debug logging for tray icon creation
- Better error handling for icon extraction and tray icon creation

### Fixed

- **CRITICAL**: Config now saves to executable directory (not temp dir) when running as .exe
- **CRITICAL**: Profiles now persist correctly across app restarts
- **CRITICAL**: Last used profile loads on startup
- App icons no longer show as blank squares - added fallback rendering
- Tray icon initialization improved with better error handling
- Launch button now shows play icon (▶) instead of rocket (🚀)
- Icon cache now uses unique keys to prevent conflicts

### Changed

- Tray icon creation happens immediately at startup (100ms delay)
- Config.json location: next to .exe when frozen, project root when running from source
- App icon fallback: colored square with app's first letter when extraction fails
- Better exception handling throughout icon-related code

---

## [26.01.10] - 2026-01-23

### Fixed

- System tray icon now properly appears when running from .exe (fixed path resolution with sys._MEIPASS)
- Dialog window icons now display correctly in .exe builds
- Tray icon now supports both PNG and ICO formats for better compatibility
- Launch All button reduced to more appropriate size (220x45 from 300x55)

### Changed

- README icon further reduced to 51x51 pixels (5% of original, from 15%)
- Improved icon path resolution for both source and .exe execution
- Enhanced tray icon loading with fallback options

---

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
