# CLAUDE.md - Project Context for Claude Code

## Project Overview
**FavApp Starter** is a Windows application that launches multiple applications simultaneously with one click. It features profiles to organize apps by context (Work, Gaming, Creative, etc.).

## Technology Stack
- **Python 3.x** - Core language
- **customtkinter** - Modern GUI framework with dark/light theme support
- **subprocess** - For launching Windows applications
- **JSON** - Configuration storage

## Project Structure
```
FavApp Starter/
├── main.py                 # Application entry point
├── gui/
│   ├── __init__.py
│   ├── main_window.py      # Main window with profile selector
│   └── dialogs.py          # Dialogs for adding apps and profiles
├── core/
│   ├── __init__.py
│   ├── launcher.py         # App launching logic
│   └── config.py           # Configuration management (profiles + apps)
├── config.json             # User configuration (created at runtime)
├── requirements.txt        # Python dependencies
├── PLAN.md                 # Development plan
├── CHANGELOG.md            # Release notes
├── DOCUMENTATION.md        # User and developer documentation
└── CLAUDE.md               # This file - project context
```

## Key Components

### core/config.py
- `ConfigManager` class handles loading/saving config to JSON
- Manages profiles and apps within profiles
- Config file location: `config.json` in project root

### core/launcher.py
- `AppLauncher` class handles launching Windows executables
- Uses `subprocess.Popen()` for non-blocking app launches
- Validates paths before launching

### gui/main_window.py
- `MainWindow` class - the main application window
- Features: profile dropdown, app list, add/remove buttons, launch all button
- Uses customtkinter for modern appearance

### gui/dialogs.py
- `AddAppDialog` - dialog for adding new apps (with file picker)
- `AddProfileDialog` - dialog for creating new profiles

## Configuration Format
```json
{
  "active_profile": "Default",
  "theme": "dark",
  "profiles": {
    "ProfileName": {
      "apps": [
        {"name": "App Name", "path": "C:\\path\\to\\app.exe"}
      ]
    }
  }
}
```

## Development Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py

# Run from any directory
python "e:\Projects\FavApp Starter\main.py"
```

## Git Workflow
- Repository: https://github.com/Andyucu/FavApp-Starter (private)
- Main branch: `main`
- Commit style: Descriptive messages with scope

## Versioning
- Format: `YY.MM.XX` (Year.Month.Increment)
- **Increment version in CHANGELOG.md and here on every update**
- Example: 26.01.01 → 26.01.02 → 26.02.01

## Current Status

- Version: 26.01.01
- Status: Initial development
