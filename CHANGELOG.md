# Changelog

All notable changes to FavApp Starter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
