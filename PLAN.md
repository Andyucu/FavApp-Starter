# FavApp Starter - Development Plan

## Part 1: GitHub Setup & Workflow

### Step 1: Install GitHub CLI (gh)
The `gh` CLI is not currently installed. Install it:

```bash
winget install --id GitHub.cli
```

Or download from: https://cli.github.com/

After installation, **restart VS Code** to refresh the PATH.

### Step 2: Authenticate GitHub CLI
```bash
gh auth login
```
- Select `GitHub.com` → `HTTPS` → Authenticate with browser

### Step 3: Initialize & Connect to Your Existing Repo
Your repo: `https://github.com/Andyucu/FavApp-Starter` (private)

```bash
git init
git remote add origin https://github.com/Andyucu/FavApp-Starter.git
```

### Step 4: First Commit & Push
```bash
git add .
git commit -m "Initial commit: project setup"
git branch -M main
git push -u origin main
```

---

## Part 2: FavApp Application Design

### Overview
A Windows application that launches multiple apps simultaneously with one click, featuring **profiles** to organize apps by context (Work, Gaming, etc.).

### Core Features
1. **Modern GUI** - Using customtkinter for dark/light theme support
2. **App Profiles** - Create different sets of apps (Work, Gaming, Creative, etc.)
3. **One-Click Launch** - Launch all apps in the selected profile
4. **Settings Persistence** - JSON configuration storage

### Technology Stack
- **Python 3.x**
- **customtkinter** - Modern GUI framework
- **subprocess** - Launch Windows applications
- **JSON** - Configuration storage

### Project Structure
```
FavApp Starter/
├── main.py                 # Entry point
├── gui/
│   ├── __init__.py
│   ├── main_window.py      # Main window with profile selector
│   └── dialogs.py          # Add app & add profile dialogs
├── core/
│   ├── __init__.py
│   ├── launcher.py         # App launching logic
│   └── config.py           # Config management (profiles + apps)
├── config.json             # User config (created at runtime)
├── requirements.txt        # customtkinter
└── .gitignore
```

### Implementation Phases

#### Phase 1: Project Setup
- [ ] Install gh CLI and connect to GitHub
- [ ] Create project structure
- [ ] Create requirements.txt with customtkinter
- [ ] Create .gitignore

#### Phase 2: Core Logic
- [ ] `core/config.py` - Profile & app management
  - Load/save config
  - Add/remove profiles
  - Add/remove apps from profiles
- [ ] `core/launcher.py` - Launch executables

#### Phase 3: GUI Development
- [ ] `gui/main_window.py` - Main window:
  - Profile dropdown selector
  - "New Profile" / "Delete Profile" buttons
  - App list for selected profile
  - "Add App" / "Remove App" buttons
  - **"Launch All"** button (prominent)
- [ ] `gui/dialogs.py`:
  - New profile dialog (name input)
  - Add app dialog (file picker + name)

#### Phase 4: Integration & Polish
- [ ] Wire GUI to core logic
- [ ] Error handling
- [ ] Theme toggle (dark/light)

---

## Config JSON Structure
```json
{
  "active_profile": "Work",
  "profiles": {
    "Work": {
      "apps": [
        {"name": "VS Code", "path": "C:\\...\\Code.exe"},
        {"name": "Slack", "path": "C:\\...\\slack.exe"}
      ]
    },
    "Gaming": {
      "apps": [
        {"name": "Steam", "path": "C:\\...\\steam.exe"},
        {"name": "Discord", "path": "C:\\...\\Discord.exe"}
      ]
    }
  }
}
```

---

## GUI Layout (Main Window)
```
┌─────────────────────────────────────────┐
│  FavApp Starter                    [─]  │
├─────────────────────────────────────────┤
│  Profile: [Work        ▼] [+] [Delete]  │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────┐    │
│  │ VS Code                         │    │
│  │ Slack                           │    │
│  │ Chrome                          │    │
│  └─────────────────────────────────┘    │
│  [Add App]  [Remove]                    │
├─────────────────────────────────────────┤
│        [ LAUNCH ALL ]                   │
└─────────────────────────────────────────┘
```

---

## Files to Create
1. `requirements.txt` - `customtkinter`
2. `.gitignore` - `config.json`, `__pycache__/`, `*.pyc`, `.venv/`
3. `main.py` - Entry point
4. `core/__init__.py`, `core/config.py`, `core/launcher.py`
5. `gui/__init__.py`, `gui/main_window.py`, `gui/dialogs.py`

---

## Verification Plan
1. Run `python main.py` - Modern GUI opens
2. Create a profile named "Test"
3. Add 2-3 apps via file picker
4. Click "Launch All" - All apps open
5. Switch profiles - App list changes
6. Close and reopen - Settings persist
