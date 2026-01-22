# FavApp Starter - Documentation

## Overview
FavApp Starter is a Windows application that allows you to launch multiple applications simultaneously with a single click. Organize your apps into profiles for different contexts like Work, Gaming, or Creative tasks.

## Table of Contents
1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Features](#features)
4. [User Guide](#user-guide)
5. [Configuration](#configuration)
6. [Troubleshooting](#troubleshooting)

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows operating system

### Setup
1. Clone or download the repository
2. Open a terminal in the project directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```

---

## Getting Started

### First Launch
When you first launch FavApp Starter, a "Default" profile is automatically created. You can start adding applications right away.

### Quick Start
1. Click **"Add App"** to add your first application
2. Browse to the `.exe` file you want to add
3. Enter a friendly name for the app
4. Repeat for all apps you want in this profile
5. Click **"Launch All"** to open all apps at once

---

## Features

### Profiles
Profiles let you organize apps by context. For example:
- **Work** - VS Code, Slack, Chrome, Outlook
- **Gaming** - Steam, Discord, Game Launcher
- **Creative** - Photoshop, Premiere Pro, Spotify

### Theme Support
Toggle between dark and light themes using the theme button in the top-right corner.

### Persistent Settings
All your profiles and apps are automatically saved and restored when you reopen the application.

---

## User Guide

### Managing Profiles

#### Create a New Profile
1. Click the **"+"** button next to the profile dropdown
2. Enter a name for your new profile
3. Click **"Create"**

#### Switch Profiles
- Use the dropdown menu at the top to select a different profile
- The app list updates automatically

#### Delete a Profile
1. Select the profile you want to delete
2. Click the **"Delete"** button
3. Confirm the deletion

> Note: You cannot delete the last remaining profile.

### Managing Applications

#### Add an Application
1. Click **"Add App"**
2. A file picker opens - navigate to the `.exe` file
3. Enter a display name for the application
4. Click **"Add"**

#### Remove an Application
1. Select the app in the list
2. Click **"Remove"**

#### Launch Applications
- **Launch All**: Click the big "Launch All" button to open all apps in the current profile
- Apps launch simultaneously in the background

---

## Configuration

### Config File Location
Settings are stored in `config.json` in the application directory.

### Config Structure
```json
{
  "active_profile": "Work",
  "theme": "dark",
  "profiles": {
    "Work": {
      "apps": [
        {
          "name": "VS Code",
          "path": "C:\\Program Files\\Microsoft VS Code\\Code.exe"
        },
        {
          "name": "Chrome",
          "path": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        }
      ]
    }
  }
}
```

### Manual Editing
You can manually edit `config.json` if needed. The application will load changes on next startup.

---

## Troubleshooting

### Application Won't Launch
- **Check the path**: Ensure the `.exe` path is correct
- **File moved**: If you moved the application, remove and re-add it
- **Permissions**: Some apps may require administrator privileges

### Config File Errors
If the application fails to start due to config errors:
1. Delete `config.json`
2. Restart the application (a new default config will be created)

### Theme Not Changing
- The theme change applies immediately
- If it doesn't, restart the application

### Common Issues

| Issue | Solution |
|-------|----------|
| App not in list after adding | Check if the file path was valid |
| Launch All does nothing | Ensure apps are added to the current profile |
| Profile not saving | Check write permissions in the app directory |

---

## Technical Details

### Dependencies
- `customtkinter` - Modern tkinter-based GUI framework

### Supported File Types
- `.exe` - Windows executables
- `.bat` - Batch files
- `.cmd` - Command files
- `.lnk` - Shortcuts (Windows)

### System Requirements
- Windows 10 or later (recommended)
- Python 3.8+
- 50 MB disk space

---

## Support
For issues and feature requests, please visit the GitHub repository.
