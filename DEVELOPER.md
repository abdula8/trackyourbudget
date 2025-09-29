# 👨‍💻 Developer Documentation

> **Comprehensive guide for developers contributing to Budget Calculator**

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Project Architecture](#project-architecture)
- [Development Setup](#development-setup)
- [Code Style Guide](#code-style-guide)
- [Testing](#testing)
- [Building & Deployment](#building--deployment)
- [Contributing Guidelines](#contributing-guidelines)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)

## 🚀 Getting Started

### Prerequisites
- **Python 3.7+** - [Download](https://python.org/downloads/)
- **Git** - [Download](https://git-scm.com/downloads)
- **IDE** - VS Code, PyCharm, or your preferred editor
- **Windows SDK** (for building) - [Download](https://developer.microsoft.com/windows/downloads/windows-sdk/)

### Quick Setup
```bash
# Clone the repository
git clone https://github.com/abdula8/trackyourbudget.git
cd budget-calculator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main_qt.py
```

## 🏗️ Project Architecture

### High-Level Overview
```
Budget Calculator
├── Presentation Layer (PyQt5 UI)
├── Business Logic Layer (Core Functions)
├── Data Access Layer (SQLite Database)
└── External Services (Export, Analysis)
```

### Core Components

#### 1. **Main Application** (`main_qt.py`)
- **Purpose**: Main application entry point and UI controller
- **Key Classes**:
  - `BudgetApp`: Main window and application logic
  - `CustomCategoriesDialog`: Category management interface
- **Responsibilities**:
  - UI event handling
  - Data validation
  - Business logic coordination

#### 2. **Data Layer** (`config.py`, Database)
- **Purpose**: Data persistence and configuration
- **Key Components**:
  - SQLite database schema
  - Configuration management
  - Custom categories storage
- **Responsibilities**:
  - Data CRUD operations
  - Schema management
  - Configuration persistence

#### 3. **Analysis Module** (`analyze_expenses.py`)
- **Purpose**: Expense analysis and reporting
- **Key Functions**:
  - `analyze_expenses()`: Main analysis function
  - Data aggregation and statistics
- **Responsibilities**:
  - Data analysis
  - Report generation
  - Statistical calculations

#### 4. **Export Module** (`analyze_expenses_002.py`)
- **Purpose**: Data export functionality
- **Key Functions**:
  - `export_to_excel()`: Excel export
  - Data formatting and conversion
- **Responsibilities**:
  - Data export
  - Format conversion
  - File generation

### Database Schema

```sql
-- Expenses table
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    amount REAL,
    category TEXT,
    date TEXT
);

-- Budgets table
CREATE TABLE budgets (
    month TEXT PRIMARY KEY,
    amount REAL NOT NULL
);

-- Indexes for performance
CREATE INDEX idx_expenses_date ON expenses(date);
CREATE INDEX idx_expenses_category ON expenses(category);
```

## 🛠️ Development Setup

### Environment Configuration

#### 1. **Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. **IDE Configuration**

**VS Code Setup**:
```json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black"
}
```

**PyCharm Setup**:
- Configure Python interpreter to use virtual environment
- Enable code inspection
- Set up code formatting (Black)

### Development Tools

#### Required Tools
```bash
# Code formatting
pip install black

# Linting
pip install pylint

# Type checking
pip install mypy

# Testing
pip install pytest

# Build tools
pip install pyinstaller
```

#### Optional Tools
```bash
# Pre-commit hooks
pip install pre-commit

# Documentation
pip install sphinx

# Profiling
pip install line_profiler
```

## 📝 Code Style Guide

### Python Style (PEP 8)

#### Naming Conventions
```python
# Classes: PascalCase
class BudgetApp(QMainWindow):
    pass

# Functions and variables: snake_case
def calculate_total_expenses():
    monthly_budget = 1000.0

# Constants: UPPER_SNAKE_CASE
DATABASE_PATH = 'budget.db'
MAX_RETRIES = 3

# Private methods: leading underscore
def _internal_helper_method(self):
    pass
```

#### Type Hints
```python
from typing import List, Dict, Optional, Union

def process_expenses(expenses: List[Dict[str, Union[str, float]]]) -> Optional[float]:
    """Process a list of expenses and return total amount."""
    return sum(expense.get('amount', 0) for expense in expenses)
```

#### Docstrings
```python
def add_expense(self, description: str, amount: float, category: str) -> bool:
    """
    Add a new expense to the database.
    
    Args:
        description: Description of the expense
        amount: Amount spent (must be positive)
        category: Expense category
        
    Returns:
        True if successful, False otherwise
        
    Raises:
        ValueError: If amount is negative
        DatabaseError: If database operation fails
    """
    pass
```

### PyQt5 Style

#### Widget Naming
```python
# Use descriptive names with widget type
self.txt_description = QTextEdit()
self.btn_add_expense = QPushButton()
self.cmb_category = QComboBox()
self.lbl_total_amount = QLabel()
```

#### Layout Management
```python
# Use appropriate layout managers
main_layout = QVBoxLayout()
form_layout = QFormLayout()
button_layout = QHBoxLayout()

# Add widgets with proper spacing
main_layout.addWidget(self.description_label)
main_layout.addSpacing(10)
main_layout.addLayout(form_layout)
```

## 🧪 Testing

### Test Structure
```
tests/
├── unit/
│   ├── test_database.py
│   ├── test_categories.py
│   └── test_analysis.py
├── integration/
│   ├── test_ui_integration.py
│   └── test_export_integration.py
└── fixtures/
    ├── sample_data.json
    └── test_database.db
```

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/unit/test_database.py

# Run with coverage
python -m pytest --cov=main_qt

# Run with verbose output
python -m pytest -v
```

### Test Examples

#### Unit Test
```python
import unittest
from unittest.mock import Mock, patch
from main_qt import BudgetApp, detect_category

class TestBudgetApp(unittest.TestCase):
    def setUp(self):
        self.app = BudgetApp()
    
    def test_detect_category_food(self):
        """Test automatic category detection for food expenses."""
        result = detect_category("bought groceries at supermarket")
        self.assertEqual(result, "Food")
    
    def test_detect_category_unknown(self):
        """Test category detection for unknown expenses."""
        result = detect_category("random expense")
        self.assertEqual(result, "Others")
```

#### Integration Test
```python
import pytest
from PyQt5.QtWidgets import QApplication
from main_qt import BudgetApp

@pytest.fixture
def app():
    """Create application instance for testing."""
    application = QApplication([])
    budget_app = BudgetApp()
    yield budget_app
    application.quit()

def test_add_expense_integration(app):
    """Test complete expense addition workflow."""
    # Test data
    description = "Test expense"
    amount = 25.50
    category = "Test"
    
    # Add expense
    result = app.add_expense(description, amount, category)
    
    # Verify
    assert result is True
    assert app.get_total_expenses() == amount
```

## 🔨 Building & Deployment

### Development Build
```bash
# Run application in development mode
python main_qt.py

# Run with debug logging
python -c "import logging; logging.basicConfig(level=logging.DEBUG); import main_qt"
```

### Production Build
```bash
# Create executable
python build.py

# Or manually with PyInstaller
pyinstaller --onefile --windowed --name=BudgetCalculator main_qt.py
```

### Build Configuration

#### PyInstaller Spec File
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
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'sqlite3',
        'matplotlib',
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

## 🤝 Contributing Guidelines

### Workflow

#### 1. **Fork & Clone**
```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/abdula8/trackyourbudget.git
cd budget-calculator

# Add upstream remote
git remote add upstream https://github.com/original/budget-calculator.git
```

#### 2. **Create Feature Branch**
```bash
# Create and switch to feature branch
git checkout -b feature/amazing-feature

# Or for bug fixes
git checkout -b fix/bug-description
```

#### 3. **Development Process**
```bash
# Make your changes
# Run tests
python -m pytest

# Format code
black main_qt.py

# Check linting
pylint main_qt.py

# Commit changes
git add .
git commit -m "Add amazing feature"
```

#### 4. **Submit Pull Request**
```bash
# Push to your fork
git push origin feature/amazing-feature

# Create pull request on GitHub
```

### Pull Request Guidelines

#### Required Information
- **Clear Title** - Describe what the PR does
- **Description** - Explain the changes and why
- **Testing** - How you tested the changes
- **Screenshots** - For UI changes
- **Breaking Changes** - If any

#### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots
(For UI changes)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 📚 API Reference

### Core Classes

#### `BudgetApp`
Main application class inheriting from `QMainWindow`.

**Methods:**
- `__init__()` - Initialize application
- `add_expense(description, amount, category)` - Add new expense
- `delete_expense(expense_id)` - Delete expense
- `update_expense(expense_id, data)` - Update expense
- `get_expenses(filters=None)` - Retrieve expenses
- `calculate_totals()` - Calculate expense totals

#### `CustomCategoriesDialog`
Dialog for managing custom expense categories.

**Methods:**
- `add_category(name, keywords)` - Add new category
- `edit_category(category_id, data)` - Edit category
- `delete_category(category_id)` - Delete category
- `load_categories()` - Load categories from storage

### Utility Functions

#### `detect_category(description)`
Automatically detect expense category from description.

**Parameters:**
- `description` (str): Expense description

**Returns:**
- `str`: Detected category name

#### `load_custom_categories()`
Load custom categories from JSON file.

**Returns:**
- `dict`: Custom categories dictionary

#### `save_custom_categories(categories)`
Save custom categories to JSON file.

**Parameters:**
- `categories` (dict): Categories to save

## 🐛 Troubleshooting

### Common Issues

#### 1. **Import Errors**
```bash
# Error: ModuleNotFoundError
# Solution: Install missing dependencies
pip install -r requirements.txt
```

#### 2. **PyQt5 Issues**
```bash
# Error: PyQt5 not found
# Solution: Install PyQt5
pip install PyQt5

# On some systems, you might need:
pip install PyQt5-tools
```

#### 3. **Database Errors**
```python
# Error: Database locked
# Solution: Ensure proper connection handling
with sqlite3.connect(DB_PATH) as conn:
    # Database operations
    pass
```

#### 4. **Build Errors**
```bash
# Error: PyInstaller not found
# Solution: Install PyInstaller
pip install pyinstaller

# Error: NSIS not found
# Solution: Install NSIS from official website
```

### Debug Mode

#### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Common Debug Commands
```bash
# Run with debug output
python -u main_qt.py

# Check database
sqlite3 budget.db ".schema"

# Verify dependencies
pip list | grep -E "(PyQt5|matplotlib|sqlite3)"
```

## 📞 Support

### Getting Help
- **GitHub Issues** - Bug reports and feature requests
- **Discussions** - General questions and community help
- **Email** - abdallah.atef.0x@gmail.com
- **Documentation** - Check this guide and inline comments

### Reporting Bugs
1. **Check existing issues** - Search for similar problems
2. **Create new issue** - Use the bug report template
3. **Provide details** - Include error messages, steps to reproduce
4. **Attach logs** - Include relevant log files

---

## 🎯 **Ready to Contribute?**

**Join our development community and help make Budget Calculator even better!**

[![Contributing](https://img.shields.io/badge/Contributing-Welcome-green.svg)](CONTRIBUTING.md)
[![Issues](https://img.shields.io/badge/Issues-Open-blue.svg)](https://github.com/abdula8/trackyourbudget/issues)
[![Discussions](https://img.shields.io/badge/Discussions-Active-orange.svg)](https://github.com/abdula8/trackyourbudget/discussions)

---

<div align="center">
  <strong>Happy Coding! 🚀</strong>
</div>
