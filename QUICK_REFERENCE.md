# ⚡ Quick Reference Card

> **Quick commands and procedures for Budget Calculator development**

## 🚀 **Quick Start Commands**

### **Development**
```bash
# Run application
python main_qt.py

# Run tests
python test_app.py

# Test imports
python -c "from main_qt import BudgetApp; print('OK')"
```

### **Building**
```bash
# Full build (recommended)
python build.py

# Quick build
pyinstaller --onefile --windowed main_qt.py

# Create installer (requires NSIS)
makensis installer.nsi
```

## 🔧 **Adding New Features - Quick Steps**

### **1. Plan Feature**
- [ ] What UI components needed?
- [ ] What data structures required?
- [ ] How to integrate with existing code?
- [ ] What settings/preferences needed?

### **2. Implement Feature**
```python
# Add to main_qt.py
def _build_ui(self):
    # Add new widgets
    self.new_widget = QWidget()
    layout.addWidget(self.new_widget)

def _wire_events(self):
    # Connect events
    self.new_widget.clicked.connect(self._handle_new_feature)

def _handle_new_feature(self):
    # Implement functionality
    pass
```

### **3. Update Build Configuration**
```python
# Add to build.py - hidden imports
"--hidden-import=new_module",
"--hidden-import=PyQt5.QtWidgets.QNewWidget",

# Add to build.py - data files
"--add-data=new_file.txt;.",
```

```nsi
# Add to installer.nsi
File "new_file.txt"
Delete "$INSTDIR\new_file.txt"
```

### **4. Test and Build**
```bash
# Test feature
python main_qt.py

# Build executable
python build.py

# Test executable
cd dist && ./BudgetCalculator.exe
```

## 📋 **Common Build Issues & Solutions**

### **Import Errors**
```bash
# Error: ModuleNotFoundError
# Solution: Add to hidden-imports
"--hidden-import=missing_module",
```

### **Missing Files**
```bash
# Error: File not found in executable
# Solution: Add to --add-data
"--add-data=missing_file.txt;.",
```

### **PyQt5 Widget Errors**
```bash
# Error: Widget not found
# Solution: Add specific widget import
"--hidden-import=PyQt5.QtWidgets.QSpecificWidget",
```

## 🎯 **Feature Implementation Templates**

### **New Menu Item**
```python
# Add to _create_menu_bar()
new_action = QAction('&New Feature', self)
new_action.setShortcut('Ctrl+N')
new_action.triggered.connect(self._handle_new_feature)
menu.addAction(new_action)
```

### **New Settings Option**
```python
# Add to SettingsManager.load_defaults()
if not self.settings.contains('new_setting'):
    self.settings.setValue('new_setting', 'default_value')

# Add to SettingsDialog
self.new_setting = QCheckBox("New Setting")
layout.addWidget(self.new_setting)
```

### **New Database Field**
```python
# Add to ensure_schema()
cur.execute("ALTER TABLE expenses ADD COLUMN new_field TEXT")

# Update UI
self.new_field = QLineEdit()
layout.addWidget(self.new_field)

# Update data handling
self.cur.execute(
    "INSERT INTO expenses(..., new_field) VALUES(..., ?)",
    (..., self.new_field.text())
)
```

### **New Theme**
```python
# Add to ThemeManager
def _apply_custom_theme(self, app):
    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(100, 100, 100))
    app.setPalette(palette)

# Add to SettingsDialog
self.theme_custom = QRadioButton("Custom")
theme_layout.addWidget(self.theme_custom)
```

## 🔨 **Build Configuration Updates**

### **When Adding New Features, Always Update:**

#### **1. `build.py` - Hidden Imports**
```python
# Add new PyQt5 widgets
"--hidden-import=PyQt5.QtWidgets.QNewWidget",

# Add new Python modules
"--hidden-import=new_module",
```

#### **2. `build.py` - Data Files**
```python
# Add new files to include
"--add-data=new_file.txt;.",
"--add-data=resources/new_icon.ico;.",
```

#### **3. `installer.nsi` - Files**
```nsi
; Add to installer
File "new_file.txt"
File "resources/new_icon.ico"

; Add to uninstaller cleanup
Delete "$INSTDIR\new_file.txt"
Delete "$INSTDIR\resources\new_icon.ico"
```

#### **4. `requirements.txt` - Dependencies**
```txt
# Add new Python packages
new_dependency>=1.0.0
```

## 🧪 **Testing Checklist**

### **Before Building**
- [ ] Application runs without errors
- [ ] All new features work
- [ ] Settings save/load correctly
- [ ] Theme switching works
- [ ] All menus functional
- [ ] Database operations work
- [ ] Export functions work

### **After Building**
- [ ] Executable runs
- [ ] All features work in EXE
- [ ] Settings persist
- [ ] Theme switching works
- [ ] Installer works
- [ ] Uninstaller works
- [ ] All files included

## 📁 **File Structure Reference**

```
budget-calculator/
├── main_qt.py                 # Main application
├── analyze_expenses.py        # Analysis module
├── analyze_expenses_002.py    # Export module
├── config.py                  # Configuration
├── requirements.txt           # Dependencies
├── build.py                   # Build script
├── installer.nsi              # Installer script
├── test_app.py                # Test script
├── app.ico                    # App icon
├── app.png                    # App image
├── README.md                  # GitHub docs
├── USER_GUIDE.md              # User guide
├── DEVELOPER.md               # Developer docs
├── DEVELOPMENT_GUIDE.md       # This guide
├── FEATURE_SUGGESTIONS.md     # Feature ideas
├── ABOUT_INFO.md              # About template
└── QUICK_REFERENCE.md         # This file
```

## 🎯 **Common Tasks**

### **Add New Widget**
1. Create widget in `_build_ui()`
2. Add to layout
3. Wire events in `_wire_events()`
4. Implement handler method

### **Add New Menu**
1. Add to `_create_menu_bar()`
2. Create action with shortcut
3. Connect to handler method
4. Implement handler method

### **Add New Setting**
1. Add default to `SettingsManager.load_defaults()`
2. Add UI control to `SettingsDialog`
3. Load/save in dialog methods
4. Use setting in application

### **Add New Database Field**
1. Update `ensure_schema()`
2. Add UI control
3. Update insert/update queries
4. Update display logic

### **Add New Theme**
1. Add method to `ThemeManager`
2. Add option to `SettingsDialog`
3. Update theme switching logic
4. Test all UI elements

## 🚨 **Emergency Fixes**

### **Build Fails**
```bash
# Check for missing imports
pyinstaller --debug=imports main_qt.py

# Check for missing files
pyinstaller --debug=all main_qt.py

# Test individual modules
python -c "import main_qt"
```

### **Runtime Errors**
```bash
# Run with error output
python main_qt.py 2>&1 | tee error.log

# Check database
sqlite3 budget.db ".schema"

# Check settings
python -c "from PyQt5.QtCore import QSettings; s=QSettings('BudgetCalculator','Settings'); print(s.allKeys())"
```

### **UI Issues**
```python
# Check widget hierarchy
print(self.centralWidget().children())

# Check event connections
print(self.sender())

# Check settings
print(self.settings_manager.get('theme'))
```

---

## 📞 **Support**

- **Documentation**: See DEVELOPMENT_GUIDE.md
- **Issues**: Check error messages carefully
- **Testing**: Use test_app.py
- **Debugging**: Use verbose build output

---

<div align="center">
  <strong>⚡ Quick Reference - Keep This Handy! ⚡</strong>
</div>
