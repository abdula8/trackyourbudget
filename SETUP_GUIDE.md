# Budget Calculator - Setup and Build Guide

## Overview
This guide will help you convert the Python Budget Calculator application into a professional Windows installer with all the requested features.

## Features Implemented

### ✅ Application Improvements
- **Removed "My Soul" category** from default categories
- **Added custom categories management** - Users can now add, edit, and delete custom expense categories with keywords
- **Performance optimizations** - Improved database queries, UI updates, and memory usage
- **Enhanced UI** - Added "Manage Categories" button with intuitive dialog

### ✅ Installer Features
- **Professional NSIS installer** with modern UI
- **Welcome screen** with application description
- **License agreement** with proper EULA
- **Checkboxes for installation options** (all checked by default):
  - Desktop shortcut
  - Start Menu shortcuts
  - AnyDesk installation
- **AnyDesk integration** - Uses existing AnyDesk.exe in directory
- **Uninstaller** with proper cleanup

## File Structure
```
project/
├── main_qt.py                 # Main application (enhanced)
├── analyze_expenses.py        # Analysis module
├── analyze_expenses_002.py    # Excel export module
├── config.py                  # Configuration (updated)
├── requirements.txt           # Dependencies (updated)
├── LICENSE.txt               # License agreement
├── README.txt                # User documentation
├── installer.nsi             # NSIS installer script
├── build.py                  # Python build script
├── build.bat                 # Windows batch build script
├── test_app.py               # Application test script
├── app.ico                   # Application icon
├── app.png                   # Application image
└── AnyDesk.exe              # AnyDesk remote desktop (if available)
```

## Prerequisites

### Required Software
1. **Python 3.7+** - Download from [python.org](https://python.org)
2. **NSIS (Nullsoft Scriptable Install System)** - Download from [nsis.sourceforge.io](https://nsis.sourceforge.io)
3. **Git** (optional) - For version control

### Python Dependencies
Install required packages:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install PyQt5>=5.15.0
pip install matplotlib>=3.5.0
pip install pyinstaller>=5.0.0
pip install openpyxl>=3.0.0
```

## Build Process

### Method 1: Automated Build (Recommended)
1. **Run the test script first**:
   ```bash
   python test_app.py
   ```

2. **Run the build script**:
   ```bash
   python build.py
   ```
   Or on Windows:
   ```cmd
   build.bat
   ```

### Method 2: Manual Build
1. **Test the application**:
   ```bash
   python test_app.py
   ```

2. **Create executable**:
   ```bash
   pyinstaller --onefile --windowed --name=BudgetCalculator --icon=app.ico main_qt.py
   ```

3. **Create installer** (if NSIS is installed):
   ```bash
   makensis installer.nsi
   ```

## Build Output

After successful build, you'll find:

### Executable Files
- `dist/BudgetCalculator.exe` - Main application executable
- `BudgetCalculatorSetup.exe` - Windows installer (if NSIS available)

### Portable Version
- `dist/BudgetCalculator_Portable/` - Portable version with all dependencies

### Installer Features
- **Welcome screen** with application description
- **License agreement** with proper terms
- **Component selection** with checkboxes:
  - ✅ Budget Calculator (required)
  - ✅ Desktop Shortcut (checked by default)
  - ✅ Start Menu Shortcut (checked by default)
  - ✅ Install AnyDesk (checked by default)
- **Directory selection** for installation
- **Progress indicator** during installation
- **Finish screen** with options to run application

## Installation Process

### For End Users
1. **Download** `BudgetCalculatorSetup.exe`
2. **Run** the installer as Administrator
3. **Follow** the installation wizard:
   - Read and accept the license agreement
   - Choose installation options (all recommended)
   - Select installation directory
   - Wait for installation to complete
4. **Launch** the application from desktop or Start Menu

### Installation Options
- **Desktop Shortcut**: Creates `Budget Calculator.lnk` on desktop
- **Start Menu**: Creates program group with shortcuts
- **AnyDesk**: Installs remote desktop software for support
- **Uninstaller**: Properly removes all components

## Application Features

### New Custom Categories Management
1. **Click "Manage Categories"** button
2. **Add new category**:
   - Enter category name
   - Enter keywords (comma-separated)
   - Click "Add Category"
3. **Edit existing category**:
   - Double-click category in list
   - Modify name or keywords
4. **Delete category**:
   - Select category and click "Delete"

### Performance Improvements
- **Optimized database queries** - Single query for totals calculation
- **Improved table rendering** - Pre-allocated rows, disabled sorting during updates
- **Better memory usage** - Optimized SQLite connection settings
- **Faster category detection** - Cached category lookups

## Troubleshooting

### Common Issues

#### Build Fails
- **Check Python version**: Must be 3.7 or higher
- **Install dependencies**: Run `pip install -r requirements.txt`
- **Check file paths**: Ensure all files are in correct locations

#### NSIS Installer Fails
- **Install NSIS**: Download from official website
- **Check AnyDesk.exe**: Ensure file exists in project directory
- **Run as Administrator**: NSIS may need elevated privileges

#### Application Won't Start
- **Check dependencies**: Ensure all required files are present
- **Run test script**: `python test_app.py`
- **Check logs**: Look for error messages in console

### File Requirements
- `main_qt.py` - Main application
- `analyze_expenses.py` - Analysis functions
- `analyze_expenses_002.py` - Excel export
- `config.py` - Configuration
- `app.ico` - Application icon
- `AnyDesk.exe` - For installer (optional)

## Development Notes

### Code Changes Made
1. **Removed "My Soul" category** from `CATEGORY_KEYWORDS`
2. **Added custom categories system**:
   - `load_custom_categories()` - Load from JSON
   - `save_custom_categories()` - Save to JSON
   - `get_all_categories()` - Combine default and custom
   - `CustomCategoriesDialog` - Management UI
3. **Performance optimizations**:
   - Optimized database queries
   - Improved table rendering
   - Better SQLite configuration
4. **Enhanced UI**:
   - Added "Manage Categories" button
   - Dynamic category loading
   - Better error handling

### Database Schema
- **expenses table**: id, description, amount, category, date
- **budgets table**: month, amount
- **Indexes**: date, category for performance

## Support

For technical support or questions:
- Check the README.txt file
- Review the LICENSE.txt for terms
- Run the test script for diagnostics

## Version Information
- **Application Version**: 1.0.0
- **Build Date**: 2024
- **Python Requirements**: 3.7+
- **Platform**: Windows 7+

---

**Note**: This setup creates a professional Windows installer with all requested features. The application is optimized for performance and includes comprehensive custom category management capabilities.
