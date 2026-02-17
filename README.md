# FavApp Starter

A modern Windows application that allows you to launch multiple applications simultaneously with a single click. Organize your favorite apps into profiles for different contexts like Work, Gaming, or Creative tasks.

<a href="https://www.buymeacoffee.com/anditeodorovici" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

![FavApp Starter](assets/icon_readme.png)


## Features

- **One-Click Launch** 
  - Launch all your favorite applications in a profile with a single button click
- **Profile System** 
  - Organize apps into different profiles (Work, Gaming, etc.)
- **Modern UI** 
  - Native PyQt6 interface with hardware-accelerated rendering
  - Clean, modern design with dark and light theme support
- **Search Installed Apps** 
  - Find and add applications from your system with built-in search
- **Easy Configuration** 
  - Add applications via file picker or search, no manual path editing required
- **Advanced App Settings** 
  - Set command-line arguments and working directories for each app
- **System Tray** 
  - Launch any profile directly from tray
  - Minimize to tray functionality
  - Auto-refreshing menu on profile changes
- **Keyboard Shortcuts** 
  - Comprehensive keyboard shortcuts for faster workflow
- **Auto-Start** - Option to launch with Windows startup
- **Profile Management** - Duplicate, rename, import/export profiles easily
- **Persistent Settings** - Your profiles and apps are automatically saved and restored
- **Portable** - Standalone executable (45MB), no installation required


## Installation

### For Users

1. Download `FavApp Starter.exe` from the [Releases](https://github.com/Andyucu/FavApp-Starter/releases) page
2. Run the executable - no installation required
3. The configuration file will be created automatically in the same directory


### Getting Started

1. Launch FavApp Starter
2. A "Default" profile is created automatically
3. Click **"Add App"** to add your first application
4. Browse to the `.exe` file you want to add
5. Enter a friendly name for the app
6. Click **"Launch All"** to open all apps at once

### Managing Profiles

- **Create Profile**: Click the **"+"** button next to the profile dropdown
- **Switch Profile**: Use the dropdown to select a different profile
- **Delete Profile**: Click the trash button (cannot delete the last profile)

### Managing Applications

- **Add App**: Click "Add App", then either:
  - Browse for an executable manually
  - Click "Search..." to find installed applications on your system
- **Edit App**: Click the edit button (✎) on any app to modify its settings
- **Launch Single App**: Double-click an app name to launch it individually
- **Remove App**: Check the apps you want to remove and click "Remove Selected"
- **Search Apps**: Use the search bar to filter apps by name or path

### Settings

Access settings via **File > Options**:

- **Theme**: Choose between Dark, Light, or System theme
- **Show Application Icons**: Toggle icon display in app list
- **Launch Delay**: Set delay (in milliseconds) between launching apps
- **Minimize to System Tray**: Enable system tray integration
- **Start Minimized**: Launch minimized to tray on startup
- **Start with Windows**: Automatically launch when Windows starts
- **Confirm Before Exit**: Show confirmation dialog when closing

### About & License

- **About**: View app information and GPLv3 license via **About > App Info**

### Keyboard Shortcuts

- **Ctrl+A**: Add new application
- **Ctrl+N**: Create new profile
- **Ctrl+D**: Duplicate current profile
- **Ctrl+L**: Launch all apps in current profile
- **Ctrl+,**: Open options/settings
- **Ctrl+Q**: Exit application
- **Del**: Remove selected apps


## Supported File Types

- `.exe` - Windows executables
- `.bat` - Batch files
- `.cmd` - Command files
- `.lnk` - Windows shortcuts
- `.msc` - Microsoft Management Console snap-ins
- `.msi` - Windows Installer packages

## System Requirements

- Windows 10 or later

## Technology Stack

- **PyQt6** - Modern GUI framework with native Qt widgets
- **Python 3.x** - Core language

## Project Structure

```text
FavApp Starter/
├── main.py              # Application entry point (PyQt6)
├── main_ctk.py          # Legacy CustomTkinter version (backup)
├── core/
│   ├── config.py        # Configuration management
│   ├── launcher.py      # App launching logic
│   ├── app_finder.py    # Installed app discovery
│   ├── autostart.py     # Windows startup integration
│   └── debug_logger.py  # Logging utilities (disabled by default)
├── gui/
│   ├── qt/              # PyQt6 implementation
│   │   ├── main_window_qt.py  # Main window (QMainWindow)
│   │   ├── dialogs_qt.py      # All 8 dialog classes
│   │   └── styles.py          # QSS stylesheet manager
│   └── __init__.py      # Package exports
├── assets/
│   ├── icon.ico         # Application icon
│   └── icon_readme.png  # README icon
├── dist/
│   └── v26.2.2/         # Version-specific build output
│       └── FavApp Starter.exe  # Standalone executable (45MB)
├── FavApp.spec          # PyInstaller build configuration
├── requirements.txt     # Python dependencies (PyQt6, Pillow)
└── config.json          # User configuration (created at runtime)
```


## License

This project is licensed under the GNU General Public License v3.0 (GPLv3) - see the [LICENSE](LICENSE) file for details.

## Author

Created by Alexandru Teodorovici

