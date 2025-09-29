# 🛠️ Budget Calculator - Complete Development Guide

> **Comprehensive guide for adding new features and building EXE distributions**

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Development Environment Setup](#development-environment-setup)
3. [Project Architecture](#project-architecture)
4. [Adding New Features](#adding-new-features)
5. [Building and Distribution](#building-and-distribution)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)
8. [Advanced Topics](#advanced-topics)

## 🎯 Project Overview

### **Application Structure**
```
budget-calculator/
├── main_qt.py                 # Main application (PyQt5)
├── analyze_expenses.py        # Expense analysis module
├── analyze_expenses_002.py    # Excel export module
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── build.py                   # Build automation script
├── build.bat                  # Windows build script
├── installer.nsi              # NSIS installer script
├── test_app.py                # Application testing
├── app.ico                    # Application icon
├── app.png                    # Application image
└── docs/                      # Documentation files
```

### **Key Technologies**
- **Python 3.7+** - Core programming language
- **PyQt5** - GUI framework
- **SQLite** - Database
- **PyInstaller** - EXE conversion
- **NSIS** - Installer creation

## 🚀 Development Environment Setup

### **Prerequisites**
1. **Python 3.7+** - [Download](https://python.org/downloads/)
2. **Git** - [Download](https://git-scm.com/downloads)
3. **NSIS** - [Download](https://nsis.sourceforge.io/) (for installer)
4. **IDE** - VS Code, PyCharm, or your preferred editor

### **Setup Steps**

#### 1. **Clone and Setup Environment**
```bash
# Clone repository (if using Git)
git clone <repository-url>
cd budget-calculator

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. **Verify Installation**
```bash
# Test the application
python main_qt.py

# Run tests
python test_app.py

# Test build process
python build.py
```

## 🏗️ Project Architecture

### **Core Components**

#### **1. Main Application (`main_qt.py`)**
```python
# Key Classes:
- BudgetApp: Main window and application logic
- SettingsManager: Application settings management
- ThemeManager: Theme switching functionality
- SettingsDialog: Settings configuration dialog
- AboutDialog: About information dialog
- CustomCategoriesDialog: Category management dialog
```

#### **2. Data Layer**
```python
# Database Schema:
- expenses: id, description, amount, category, date
- budgets: month, amount

# Configuration:
- custom_categories.json: Custom categories storage
- QSettings: Application preferences
```

#### **3. Analysis Modules**
```python
# analyze_expenses.py: Core analysis functions
# analyze_expenses_002.py: Excel export functionality
```

### **Code Organization**

#### **File Structure Pattern**
```python
# Each file follows this pattern:
1. Imports
2. Constants and Configuration
3. Helper Functions
4. Dialog Classes
5. Main Application Class
6. Main Execution Block
```

#### **Class Structure Pattern**
```python
class ClassName:
    def __init__(self):
        # Initialization
        self.setup_ui()
        self.wire_events()
    
    def setup_ui(self):
        # UI creation
    
    def wire_events(self):
        # Event connections
    
    def _private_method(self):
        # Internal methods (prefixed with _)
```

## 🆕 Adding New Features

### **Step-by-Step Process**

#### **1. Planning the Feature**
```markdown
Before coding, plan:
- What UI components are needed?
- What data structures are required?
- How will it integrate with existing code?
- What settings/preferences are needed?
- How will it be tested?
```

#### **2. Database Changes (if needed)**
```python
# If adding new data storage:
# 1. Update ensure_schema() function in main_qt.py
def ensure_schema(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    # Add new table or column
    cur.execute("""
        CREATE TABLE IF NOT EXISTS new_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field1 TEXT,
            field2 REAL
        )
    """)
    conn.commit()
```

#### **3. UI Components**
```python
# Adding new UI elements:
def _build_ui(self) -> None:
    # Add new widgets
    self.new_widget = QWidget()
    self.new_button = QPushButton("New Feature")
    
    # Add to layout
    layout.addWidget(self.new_widget)
    
    # Wire events
    self.new_button.clicked.connect(self._handle_new_feature)
```

#### **4. Settings Integration**
```python
# If feature needs settings:
# 1. Add to SettingsManager.load_defaults()
def load_defaults(self):
    if not self.settings.contains('new_feature_setting'):
        self.settings.setValue('new_feature_setting', 'default_value')

# 2. Add to SettingsDialog if needed
def create_general_tab(self):
    # Add new setting controls
    self.new_setting = QCheckBox("Enable New Feature")
```

#### **5. Menu Integration**
```python
# Adding menu items:
def _create_menu_bar(self):
    # Add to existing menu
    new_action = QAction('&New Feature', self)
    new_action.setShortcut('Ctrl+N')
    new_action.triggered.connect(self._handle_new_feature)
    menu.addAction(new_action)
```

### **Feature Examples**

#### **Example 1: Adding a New Report Type**
```python
# 1. Add to analyze_expenses.py
def generate_monthly_report(expenses_data):
    """Generate monthly expense report."""
    # Implementation here
    pass

# 2. Add to main_qt.py
def _create_menu_bar(self):
    # Add menu item
    report_action = QAction('&Monthly Report', self)
    report_action.triggered.connect(self._generate_monthly_report)
    tools_menu.addAction(report_action)

def _generate_monthly_report(self):
    """Generate monthly report."""
    from analyze_expenses import generate_monthly_report
    # Get data and call function
    generate_monthly_report(data)
```

#### **Example 2: Adding a New Theme**
```python
# 1. Add to ThemeManager
def _apply_custom_theme(self, app):
    """Apply custom theme."""
    app.setStyle('Fusion')
    palette = QPalette()
    # Custom color scheme
    palette.setColor(QPalette.Window, QColor(100, 100, 100))
    app.setPalette(palette)

# 2. Add to SettingsDialog
def create_appearance_tab(self):
    # Add new theme option
    self.theme_custom = QRadioButton("Custom")
    theme_layout.addWidget(self.theme_custom)
```

#### **Example 3: Adding a New Data Field**
```python
# 1. Update database schema
def ensure_schema(conn: sqlite3.Connection) -> None:
    # Add new column
    cur.execute("ALTER TABLE expenses ADD COLUMN notes TEXT")

# 2. Update UI
def _build_ui(self):
    # Add notes field
    self.txt_notes = QTextEdit()
    self.txt_notes.setPlaceholderText("Additional notes...")
    layout.addWidget(self.txt_notes)

# 3. Update data handling
def _add_expense(self):
    notes = self.txt_notes.toPlainText().strip()
    # Include notes in database insert
    self.cur.execute(
        "INSERT INTO expenses(description, amount, category, date, notes) VALUES(?,?,?,?,?)",
        (desc, amount, category, date_str, notes)
    )
```

## 🔨 Building and Distribution

### **Build Process Overview**

#### **1. Pre-Build Checklist**
```bash
# Before building, ensure:
1. All features work correctly
2. No syntax errors
3. All imports are available
4. Dependencies are installed
5. Test script passes
```

#### **2. Testing Before Build**
```bash
# Run comprehensive tests
python test_app.py

# Test specific functionality
python -c "from main_qt import BudgetApp; print('Import successful')"

# Test all modules
python -c "import analyze_expenses; import analyze_expenses_002; print('All modules OK')"
```

### **Building Executable**

#### **Method 1: Automated Build (Recommended)**
```bash
# Use the build script
python build.py

# This will:
# 1. Clean previous builds
# 2. Create executable
# 3. Copy additional files
# 4. Create portable version
# 5. Create installer (if NSIS available)
```

#### **Method 2: Manual Build**
```bash
# Create executable manually
pyinstaller --onefile --windowed --name=BudgetCalculator --icon=app.ico main_qt.py

# With all dependencies
pyinstaller --onefile --windowed \
    --name=BudgetCalculator \
    --icon=app.ico \
    --add-data="app.ico;." \
    --add-data="app.png;." \
    --add-data="LICENSE.txt;." \
    --add-data="README.txt;." \
    --hidden-import=PyQt5.QtCore \
    --hidden-import=PyQt5.QtGui \
    --hidden-import=PyQt5.QtWidgets \
    --hidden-import=sqlite3 \
    --hidden-import=matplotlib \
    --hidden-import=analyze_expenses \
    --hidden-import=analyze_expenses_002 \
    main_qt.py
```

### **Updating Build Configuration**

#### **When Adding New Features, Update:**

#### **1. `build.py` - Hidden Imports**
```python
# Add new imports to the cmd list
"--hidden-import=PyQt5.QtWidgets.QNewWidget",
"--hidden-import=new_module_name",
```

#### **2. `build.py` - Data Files**
```python
# Add new files to be included
"--add-data=new_file.txt;.",
"--add-data=resources/new_icon.ico;.",
```

#### **3. `installer.nsi` - Installer Files**
```nsi
; Add new files to installer
File "new_file.txt"
File "resources/new_icon.ico"
```

#### **4. `installer.nsi` - Uninstaller**
```nsi
; Add new files to uninstaller cleanup
Delete "$INSTDIR\new_file.txt"
Delete "$INSTDIR\resources\new_icon.ico"
```

### **Complete Build Configuration Update Process**

#### **Step 1: Identify New Dependencies**
```python
# When adding new features, check for:
1. New PyQt5 widgets used
2. New Python modules imported
3. New data files needed
4. New external dependencies
```

#### **Step 2: Update `build.py`**
```python
def create_exe():
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=BudgetCalculator",
        "--icon=app.ico",
        # Add new data files
        "--add-data=new_file.txt;.",
        # Add new hidden imports
        "--hidden-import=new_module",
        "--hidden-import=PyQt5.QtWidgets.QNewWidget",
        # ... existing imports
        "main_qt.py"
    ]
```

#### **Step 3: Update `installer.nsi`**
```nsi
Section "!${APP_NAME}" SecMain
  ; Add new files
  File "new_file.txt"
  File "resources/new_icon.ico"
  ; ... existing files
SectionEnd

Section Uninstall
  ; Add new files to cleanup
  Delete "$INSTDIR\new_file.txt"
  Delete "$INSTDIR\resources\new_icon.ico"
  ; ... existing cleanup
SectionEnd
```

#### **Step 4: Update `requirements.txt`**
```txt
# Add new dependencies
matplotlib>=3.5.0
PyQt5>=5.15.0
pyinstaller>=5.0.0
openpyxl>=3.0.0
new_dependency>=1.0.0
```

### **Testing the Build**

#### **1. Test Executable**
```bash
# After building, test the executable
cd dist
./BudgetCalculator.exe

# Test all features:
# - Settings dialog
# - Theme switching
# - All menus
# - Data operations
# - Export functions
```

#### **2. Test Installer**
```bash
# Test the installer
./BudgetCalculatorSetup.exe

# Verify:
# - Installation process
# - All files installed
# - Shortcuts created
# - Uninstaller works
```

## 🐛 Troubleshooting

### **Common Build Issues**

#### **1. Import Errors**
```bash
# Error: ModuleNotFoundError
# Solution: Add to hidden-imports in build.py
"--hidden-import=missing_module",
```

#### **2. Missing Files**
```bash
# Error: File not found in executable
# Solution: Add to --add-data in build.py
"--add-data=missing_file.txt;.",
```

#### **3. PyQt5 Widget Errors**
```bash
# Error: Widget not found
# Solution: Add specific widget import
"--hidden-import=PyQt5.QtWidgets.QSpecificWidget",
```

#### **4. Database Errors**
```bash
# Error: Database locked
# Solution: Ensure proper connection handling
with sqlite3.connect(DB_PATH) as conn:
    # Database operations
    pass
```

### **Debugging Build Issues**

#### **1. Verbose PyInstaller Output**
```bash
# Run with verbose output
pyinstaller --onefile --windowed --debug=all main_qt.py
```

#### **2. Check Dependencies**
```bash
# Check what PyInstaller finds
pyinstaller --onefile --windowed --debug=imports main_qt.py
```

#### **3. Test Individual Modules**
```bash
# Test each module separately
python -c "import main_qt"
python -c "import analyze_expenses"
python -c "import analyze_expenses_002"
```

### **Common Runtime Issues**

#### **1. Settings Not Saving**
```python
# Check QSettings initialization
self.settings = QSettings('BudgetCalculator', 'Settings')
self.settings.sync()  # Ensure settings are saved
```

#### **2. Theme Not Applying**
```python
# Ensure theme is applied to QApplication
self.theme_manager.apply_theme(QApplication.instance())
```

#### **3. Database Connection Issues**
```python
# Use proper connection handling
try:
    self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    # ... operations
except sqlite3.Error as e:
    logging.error(f"Database error: {e}")
```

## 📚 Best Practices

### **Code Organization**

#### **1. File Structure**
```python
# Keep related functionality together
# Use clear, descriptive names
# Separate UI from business logic
# Use helper functions for complex operations
```

#### **2. Error Handling**
```python
# Always use try-catch for database operations
try:
    self.cur.execute(query, params)
    self.conn.commit()
except sqlite3.Error as e:
    logging.error(f"Database error: {e}")
    QMessageBox.critical(self, "Error", str(e))
```

#### **3. UI Guidelines**
```python
# Use consistent naming
self.btn_action = QPushButton("Action")
self.txt_input = QLineEdit()
self.cmb_selection = QComboBox()

# Wire events in dedicated method
def _wire_events(self):
    self.btn_action.clicked.connect(self._handle_action)
```

### **Adding New Features Guidelines**

#### **1. Planning Phase**
```markdown
1. Define the feature clearly
2. Identify required UI components
3. Plan data structures needed
4. Consider integration points
5. Plan testing approach
```

#### **2. Implementation Phase**
```python
# 1. Start with data layer (if needed)
# 2. Add UI components
# 3. Implement business logic
# 4. Wire events
# 5. Add to menus/settings (if needed)
# 6. Test thoroughly
```

#### **3. Integration Phase**
```python
# 1. Update build configuration
# 2. Update installer
# 3. Update documentation
# 4. Test complete build
# 5. Verify all features work
```

### **Testing Guidelines**

#### **1. Unit Testing**
```python
# Test individual functions
def test_add_expense():
    app = BudgetApp()
    result = app.add_expense("Test", 10.0, "Test")
    assert result == True
```

#### **2. Integration Testing**
```python
# Test complete workflows
def test_expense_workflow():
    app = BudgetApp()
    # Add expense
    app.add_expense("Test", 10.0, "Test")
    # Verify in database
    expenses = app.get_expenses()
    assert len(expenses) > 0
```

#### **3. UI Testing**
```python
# Test UI interactions
def test_settings_dialog():
    app = BudgetApp()
    dialog = SettingsDialog(app)
    assert dialog.isVisible() == False
    dialog.show()
    assert dialog.isVisible() == True
```

## 🔧 Advanced Topics

### **Custom PyInstaller Spec File**

#### **Creating a Spec File**
```python
# budget_calculator.spec
a = Analysis(
    ['main_qt.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app.ico', '.'),
        ('app.png', '.'),
        ('LICENSE.txt', '.'),
        ('README.txt', '.'),
        ('USER_GUIDE.md', '.'),
        ('DEVELOPER.md', '.'),
        ('FEATURE_SUGGESTIONS.md', '.'),
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PyQt5.QtWidgets.QButtonGroup',
        'PyQt5.QtWidgets.QActionGroup',
        'PyQt5.QtWidgets.QMenuBar',
        'PyQt5.QtWidgets.QMenu',
        'PyQt5.QtWidgets.QAction',
        'PyQt5.QtWidgets.QFileDialog',
        'PyQt5.QtWidgets.QTabWidget',
        'PyQt5.QtWidgets.QGroupBox',
        'PyQt5.QtWidgets.QRadioButton',
        'PyQt5.QtWidgets.QTextBrowser',
        'PyQt5.QtWidgets.QFormLayout',
        'PyQt5.QtCore.QSettings',
        'PyQt5.QtGui.QPalette',
        'PyQt5.QtGui.QColor',
        'sqlite3',
        'matplotlib',
        'analyze_expenses',
        'analyze_expenses_002',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BudgetCalculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app.ico'
)
```

#### **Using Spec File**
```bash
# Build using spec file
pyinstaller budget_calculator.spec
```

### **Advanced NSIS Installer**

#### **Custom Installer Features**
```nsi
; Add custom installer features
!define MUI_CUSTOMFUNCTION_GUIINIT onGUIInit
!define MUI_CUSTOMFUNCTION_UNGUIINIT un.onGUIInit

Function onGUIInit
    ; Custom initialization
    SetBrandingImage /RESIZETOFIT "$PLUGINSDIR\installer_banner.bmp"
FunctionEnd

Function un.onGUIInit
    ; Custom uninstaller initialization
FunctionEnd
```

### **Automated Testing**

#### **Continuous Integration Setup**
```yaml
# .github/workflows/build.yml
name: Build and Test
on: [push, pull_request]
jobs:
  test:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: python test_app.py
    - name: Build executable
      run: python build.py
```

## 📋 Quick Reference

### **Common Commands**
```bash
# Development
python main_qt.py                    # Run application
python test_app.py                   # Run tests
python -c "from main_qt import *"    # Test imports

# Building
python build.py                      # Full build process
pyinstaller main_qt.py               # Quick build
makensis installer.nsi               # Create installer

# Testing
cd dist && ./BudgetCalculator.exe    # Test executable
./BudgetCalculatorSetup.exe          # Test installer
```

### **File Locations**
```
main_qt.py          # Main application
build.py            # Build automation
installer.nsi       # Installer script
requirements.txt    # Dependencies
test_app.py         # Testing script
```

### **Key Functions**
```python
# Main application
BudgetApp.__init__()           # Initialize app
BudgetApp._build_ui()          # Create UI
BudgetApp._wire_events()       # Connect events

# Settings
SettingsManager.get()          # Get setting
SettingsManager.set()          # Set setting
ThemeManager.apply_theme()     # Apply theme

# Building
create_exe()                   # Create executable
create_installer()             # Create installer
```

---

## 🎯 **Summary**

This guide provides everything needed to:
1. **Add new features** to the Budget Calculator
2. **Update build configuration** for new features
3. **Create EXE distributions** with all features
4. **Troubleshoot common issues**
5. **Follow best practices** for development

**Key Points:**
- Always test before building
- Update build configuration when adding features
- Use proper error handling
- Follow consistent coding patterns
- Document new features

**For questions or issues:**
- Check this guide first
- Review error messages carefully
- Test individual components
- Use verbose build output for debugging

---

<div align="center">
  <strong>Happy Coding! 🚀</strong>
</div>
