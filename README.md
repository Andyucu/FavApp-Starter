# FavApp Starter

A Windows application that allows you to launch multiple applications simultaneously with a single click. Organize your favorite apps into profiles for different contexts like Work, Gaming, or Creative tasks.

![FavApp Starter](assets/icon.png)

## Features

- **One-Click Launch** - Launch all your favorite applications in a profile with a single button click
- **Profile System** - Organize apps into different profiles (Work, Gaming, Creative, etc.)
- **Modern UI** - Clean, modern interface with dark and light theme support
- **Easy Configuration** - Add applications via file picker, no manual path editing required
- **Persistent Settings** - Your profiles and apps are automatically saved and restored
- **Portable** - Standalone executable, no installation required

## Screenshots

The application features a clean, intuitive interface:

- Profile selector dropdown for quick switching between app groups
- Application list showing all apps in the current profile
- Add/Remove buttons for easy app management
- Large "Launch All" button for one-click launching

## Installation

### Option 1: Standalone Executable (Recommended)

1. Download `FavApp Starter.exe` from the [Releases](https://github.com/Andyucu/FavApp-Starter/releases) page
2. Run the executable - no installation required
3. The configuration file will be created automatically in the same directory

### Option 2: Run from Source

#### Prerequisites

- Python 3.8 or higher
- Windows operating system

#### Setup

```bash
# Clone the repository
git clone https://github.com/Andyucu/FavApp-Starter.git
cd FavApp-Starter

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Building from Source

To build the standalone executable yourself:

```bash
pip install -r requirements.txt
python -m PyInstaller FavApp.spec --noconfirm
```

The executable will be created at `dist/FavApp Starter.exe`

## Usage

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

- **Add App**: Click "Add App", browse for an executable, and enter a name
- **Remove App**: Check the apps you want to remove and click "Remove Selected"

### Settings

Access settings via **File > Options**:

- **Theme**: Choose between Dark, Light, or System theme

### About & License

- **About**: View app information via **About > App Info**
- **License**: View the MIT license via **About > License**

## Configuration

Settings are stored in `config.json` in the application directory:

```json
{
  "active_profile": "Work",
  "theme": "dark",
  "profiles": {
    "Work": {
      "apps": [
        {"name": "VS Code", "path": "C:\\Program Files\\Microsoft VS Code\\Code.exe"},
        {"name": "Chrome", "path": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"}
      ]
    }
  }
}
```

## Supported File Types

- `.exe` - Windows executables
- `.bat` - Batch files
- `.cmd` - Command files
- `.lnk` - Windows shortcuts

## System Requirements

- Windows 10 or later
- Python 3.8+ (for running from source)

## Project Structure

```text
FavApp Starter/
├── main.py              # Application entry point
├── core/
│   ├── config.py        # Configuration management
│   └── launcher.py      # App launching logic
├── gui/
│   ├── main_window.py   # Main application window
│   └── dialogs.py       # Dialog windows
├── assets/
│   └── icon.ico         # Application icon
├── FavApp.spec          # PyInstaller build configuration
├── requirements.txt     # Python dependencies
└── config.json          # User configuration (created at runtime)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Created by Alexandru Teodorovici

## Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern UI
- Packaged with [PyInstaller](https://pyinstaller.org/) for standalone distribution
