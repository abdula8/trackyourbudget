import sqlite3
import logging
import json
import os
from datetime import date, datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox, QDateEdit,
    QTableWidget, QTableWidgetItem, QMessageBox, QFrame, QProgressBar,
    QDialog, QDialogButtonBox, QCheckBox, QListWidget, QListWidgetItem,
    QInputDialog, QSplitter, QMenuBar, QMenu, QAction, QActionGroup,
    QSystemTrayIcon, QStyle, QFileDialog, QMessageBox, QVBoxLayout,
    QHBoxLayout, QGroupBox, QRadioButton, QSlider, QSpinBox, QCheckBox,
    QTextBrowser, QScrollArea, QTabWidget, QFormLayout, QButtonGroup
)
from PyQt5.QtCore import Qt, QDate, QSettings, QTimer, pyqtSignal
from PyQt5.QtGui import QDoubleValidator, QFont, QIcon, QPixmap, QPalette, QColor

from analyze_expenses import analyze_expenses
import analyze_expenses_002


logging.basicConfig(
    filename='budget_app.log', level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)


# --- DB helpers -------------------------------------------------------------
DB_PATH = 'budget.db'
CUSTOM_CATEGORIES_FILE = 'custom_categories.json'


def ensure_schema(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            category TEXT,
            date TEXT
        )
        """
    )
    # Add category column if older DB
    cur.execute("PRAGMA table_info(expenses)")
    cols = [r[1] for r in cur.fetchall()]
    if 'category' not in cols:
        cur.execute("ALTER TABLE expenses ADD COLUMN category TEXT")

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS budgets (
            month TEXT PRIMARY KEY,
            amount REAL NOT NULL
        )
        """
    )
    cur.execute("CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_expenses_category ON expenses(category)")
    conn.commit()


CATEGORY_KEYWORDS = {
    'Food': ['food', 'restaurant', 'groceries', 'meal', 'طعام', 'أكل', 'غذاء', 'فطار'],
    'Drinks': ['drink', 'water', 'coffee', 'beverage', 'juice', 'شرب', 'مشروب', 'قهوة', 'مياه', 'عصير'],
    'Trans.': ['transport', 'trans', 'bus', 'taxi', 'uber', 'gas', 'car', 'مواصلات', 'توصيلة', 'سيارة', 'عربية'],
    'Clothes': ['cloth', 'shopping', 'apparel', 'هدوم', 'ملابس', 'تيشيرت', 'كسوة'],
    'Family': ['family', 'kids', 'school', 'عائلة', 'أسرة', 'اسرة', 'بيت'],
    'Hygiene': ['hygiene', 'صحة', 'نظافة', 'تنظيف', 'برفيوم', 'عطر'],
    'Home': ['house', 'buildings', 'home', 'جمعية', 'جمعيه', 'الأثاث', 'الاثاث', 'المنزل', 'العزال'],
    'Charity': ['handout', 'charity', 'صدقة', 'صدقه'],
    'Courses': ['course', 'درس', 'كورس'],
    'New Flat': ['الشقة', 'ايجار', 'إيجار'],
    'Others': []
}


def load_custom_categories() -> dict:
    """Load custom categories from JSON file."""
    if os.path.exists(CUSTOM_CATEGORIES_FILE):
        try:
            with open(CUSTOM_CATEGORIES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logging.error('Failed to load custom categories: %s', e)
    return {}

def save_custom_categories(custom_categories: dict) -> None:
    """Save custom categories to JSON file."""
    try:
        with open(CUSTOM_CATEGORIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(custom_categories, f, ensure_ascii=False, indent=2)
    except IOError as e:
        logging.error('Failed to save custom categories: %s', e)

def get_all_categories() -> dict:
    """Get combined default and custom categories."""
    custom_categories = load_custom_categories()
    all_categories = CATEGORY_KEYWORDS.copy()
    all_categories.update(custom_categories)
    return all_categories

def detect_category(description: str) -> str:
    text = (description or '').lower()
    all_categories = get_all_categories()
    for cat, keywords in all_categories.items():
        if any(k.lower() in text for k in keywords):
            return cat
    return 'Others'


# --- Settings and Theme Management ----------------------------------------
class SettingsManager:
    """Manages application settings and preferences."""
    
    def __init__(self):
        self.settings = QSettings('BudgetCalculator', 'Settings')
        self.load_defaults()
    
    def load_defaults(self):
        """Load default settings if not set."""
        if not self.settings.contains('theme'):
            self.settings.setValue('theme', 'system')
        if not self.settings.contains('auto_backup'):
            self.settings.setValue('auto_backup', True)
        if not self.settings.contains('backup_interval'):
            self.settings.setValue('backup_interval', 7)  # days
        if not self.settings.contains('show_tooltips'):
            self.settings.setValue('show_tooltips', True)
        if not self.settings.contains('currency_symbol'):
            self.settings.setValue('currency_symbol', '$')
        if not self.settings.contains('date_format'):
            self.settings.setValue('date_format', 'yyyy-MM-dd')
        if not self.settings.contains('window_geometry'):
            self.settings.setValue('window_geometry', None)
    
    def get(self, key, default=None):
        """Get setting value."""
        return self.settings.value(key, default)
    
    def set(self, key, value):
        """Set setting value."""
        self.settings.setValue(key, value)
    
    def save(self):
        """Save settings to disk."""
        self.settings.sync()

class ThemeManager:
    """Manages application themes."""
    
    def __init__(self, settings_manager):
        self.settings = settings_manager
        self.current_theme = self.settings.get('theme', 'system')
    
    def apply_theme(self, app, theme=None):
        """Apply theme to application."""
        if theme:
            self.current_theme = theme
            self.settings.set('theme', theme)
        
        if self.current_theme == 'dark':
            self._apply_dark_theme(app)
        elif self.current_theme == 'light':
            self._apply_light_theme(app)
        else:  # system
            self._apply_system_theme(app)
    
    def _apply_dark_theme(self, app):
        """Apply dark theme."""
        app.setStyle('Fusion')
        palette = QPalette()
        
        # Dark color scheme
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        
        app.setPalette(palette)
    
    def _apply_light_theme(self, app):
        """Apply light theme."""
        app.setStyle('Fusion')
        palette = QPalette()
        
        # Light color scheme
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
        palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(0, 0, 238))
        palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        app.setPalette(palette)
    
    def _apply_system_theme(self, app):
        """Apply system theme."""
        app.setStyle('')
        app.setPalette(QApplication.style().standardPalette())

# --- Settings Dialog ------------------------------------------------------
class SettingsDialog(QDialog):
    """Settings dialog for application preferences."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Settings')
        self.setModal(True)
        self.resize(500, 400)
        
        self.settings = SettingsManager()
        self.theme_manager = ThemeManager(self.settings)
        
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Create tab widget
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # Appearance tab
        appearance_tab = self.create_appearance_tab()
        tab_widget.addTab(appearance_tab, "Appearance")
        
        # General tab
        general_tab = self.create_general_tab()
        tab_widget.addTab(general_tab, "General")
        
        # Data tab
        data_tab = self.create_data_tab()
        tab_widget.addTab(data_tab, "Data")
        
        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def create_appearance_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Theme selection
        theme_group = QGroupBox("Theme")
        theme_layout = QVBoxLayout(theme_group)
        
        self.theme_system = QRadioButton("System Default")
        self.theme_light = QRadioButton("Light")
        self.theme_dark = QRadioButton("Dark")
        
        # Create button group for radio buttons
        self.theme_button_group = QButtonGroup(self)
        self.theme_button_group.addButton(self.theme_system, 0)
        self.theme_button_group.addButton(self.theme_light, 1)
        self.theme_button_group.addButton(self.theme_dark, 2)
        
        theme_layout.addWidget(self.theme_system)
        theme_layout.addWidget(self.theme_light)
        theme_layout.addWidget(self.theme_dark)
        
        layout.addWidget(theme_group)
        
        # Currency settings
        currency_group = QGroupBox("Currency")
        currency_layout = QFormLayout(currency_group)
        
        self.currency_symbol = QLineEdit()
        currency_layout.addRow("Currency Symbol:", self.currency_symbol)
        
        layout.addWidget(currency_group)
        
        # Other appearance settings
        other_group = QGroupBox("Other")
        other_layout = QVBoxLayout(other_group)
        
        self.show_tooltips = QCheckBox("Show tooltips")
        other_layout.addWidget(self.show_tooltips)
        
        layout.addWidget(other_group)
        layout.addStretch()
        
        return tab
    
    def create_general_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Date format
        date_group = QGroupBox("Date Format")
        date_layout = QFormLayout(date_group)
        
        self.date_format = QComboBox()
        self.date_format.addItems(['yyyy-MM-dd', 'MM/dd/yyyy', 'dd/MM/yyyy', 'dd-MM-yyyy'])
        date_layout.addRow("Format:", self.date_format)
        
        layout.addWidget(date_group)
        
        # Window behavior
        window_group = QGroupBox("Window")
        window_layout = QVBoxLayout(window_group)
        
        self.remember_geometry = QCheckBox("Remember window size and position")
        window_layout.addWidget(self.remember_geometry)
        
        layout.addWidget(window_group)
        layout.addStretch()
        
        return tab
    
    def create_data_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Backup settings
        backup_group = QGroupBox("Backup")
        backup_layout = QVBoxLayout(backup_group)
        
        self.auto_backup = QCheckBox("Enable automatic backup")
        backup_layout.addWidget(self.auto_backup)
        
        backup_interval_layout = QHBoxLayout()
        backup_interval_layout.addWidget(QLabel("Backup interval:"))
        self.backup_interval = QSpinBox()
        self.backup_interval.setRange(1, 30)
        self.backup_interval.setSuffix(" days")
        backup_interval_layout.addWidget(self.backup_interval)
        backup_interval_layout.addStretch()
        backup_layout.addLayout(backup_interval_layout)
        
        # Backup buttons
        backup_buttons_layout = QHBoxLayout()
        self.backup_now_btn = QPushButton("Backup Now")
        self.restore_btn = QPushButton("Restore from Backup")
        backup_buttons_layout.addWidget(self.backup_now_btn)
        backup_buttons_layout.addWidget(self.restore_btn)
        backup_buttons_layout.addStretch()
        backup_layout.addLayout(backup_buttons_layout)
        
        layout.addWidget(backup_group)
        layout.addStretch()
        
        return tab
    
    def load_settings(self):
        """Load current settings into dialog."""
        # Theme
        theme = self.settings.get('theme', 'system')
        if theme == 'system':
            self.theme_system.setChecked(True)
        elif theme == 'light':
            self.theme_light.setChecked(True)
        elif theme == 'dark':
            self.theme_dark.setChecked(True)
        
        # Currency
        self.currency_symbol.setText(self.settings.get('currency_symbol', '$'))
        
        # Other settings
        self.show_tooltips.setChecked(self.settings.get('show_tooltips', True))
        self.date_format.setCurrentText(self.settings.get('date_format', 'yyyy-MM-dd'))
        self.remember_geometry.setChecked(self.settings.get('remember_geometry', True))
        self.auto_backup.setChecked(self.settings.get('auto_backup', True))
        self.backup_interval.setValue(self.settings.get('backup_interval', 7))
    
    def accept(self):
        """Save settings and close dialog."""
        # Save theme
        if self.theme_system.isChecked():
            self.settings.set('theme', 'system')
        elif self.theme_light.isChecked():
            self.settings.set('theme', 'light')
        elif self.theme_dark.isChecked():
            self.settings.set('theme', 'dark')
        
        # Save other settings
        self.settings.set('currency_symbol', self.currency_symbol.text())
        self.settings.set('show_tooltips', self.show_tooltips.isChecked())
        self.settings.set('date_format', self.date_format.currentText())
        self.settings.set('remember_geometry', self.remember_geometry.isChecked())
        self.settings.set('auto_backup', self.auto_backup.isChecked())
        self.settings.set('backup_interval', self.backup_interval.value())
        
        self.settings.save()
        super().accept()

# --- About Dialog ---------------------------------------------------------
class AboutDialog(QDialog):
    """About dialog with application information."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('About Budget Calculator')
        self.setModal(True)
        self.resize(400, 300)
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Application icon and title
        title_layout = QHBoxLayout()
        
        # Icon (if available)
        if os.path.exists('app.ico'):
            icon_label = QLabel()
            icon_pixmap = QPixmap('app.ico')
            icon_label.setPixmap(icon_pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            title_layout.addWidget(icon_label)
        
        # Title and version
        title_text = QLabel()
        title_text.setText("""
        <h2>Budget Calculator</h2>
        <p><b>Version 1.0.0</b></p>
        <p>Personal Finance Management Tool</p>
        """)
        title_text.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_text)
        
        layout.addLayout(title_layout)
        
        # Description
        description = QTextBrowser()
        description.setHtml("""
        <p>Budget Calculator is a powerful desktop application designed to help you manage your personal finances effectively.</p>
        
        <h3>Features:</h3>
        <ul>
        <li>Expense tracking and categorization</li>
        <li>Monthly budget management</li>
        <li>Custom categories with keyword detection</li>
        <li>Advanced filtering and search</li>
        <li>Data export to Excel</li>
        <li>Comprehensive analytics and reporting</li>
        <li>Multiple themes (Light, Dark, System)</li>
        <li>Automatic data backup</li>
        </ul>
        
        <h3>Technical Information:</h3>
        <ul>
        <li>Built with Python and PyQt5</li>
        <li>SQLite database for data storage</li>
        <li>Cross-platform compatibility</li>
        <li>Open source and free to use</li>
        </ul>
        """)
        description.setMaximumHeight(200)
        layout.addWidget(description)
        
        # Contact information
        contact_layout = QHBoxLayout()
        contact_layout.addWidget(QLabel("Contact: aabdallah.atef.0x@gmail.com"))
        contact_layout.addStretch()
        layout.addLayout(contact_layout)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

# --- Custom Categories Dialog -----------------------------------------------
class CustomCategoriesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Manage Custom Categories')
        self.setModal(True)
        self.resize(600, 400)
        
        self.custom_categories = load_custom_categories()
        self.setup_ui()
        self.load_categories()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Add new category section
        add_frame = QFrame()
        add_frame.setFrameStyle(QFrame.StyledPanel)
        add_layout = QVBoxLayout(add_frame)
        
        add_layout.addWidget(QLabel('Add New Category:'))
        
        # Category name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel('Category Name:'))
        self.category_name_input = QLineEdit()
        self.category_name_input.setPlaceholderText('Enter category name...')
        name_layout.addWidget(self.category_name_input)
        add_layout.addLayout(name_layout)
        
        # Keywords input
        keywords_layout = QHBoxLayout()
        keywords_layout.addWidget(QLabel('Keywords:'))
        self.keywords_input = QLineEdit()
        self.keywords_input.setPlaceholderText('Enter keywords separated by commas...')
        keywords_layout.addWidget(self.keywords_input)
        add_layout.addLayout(keywords_layout)
        
        # Add button
        self.add_button = QPushButton('Add Category')
        self.add_button.setStyleSheet('background:#4CAF50;color:white;font-weight:bold')
        self.add_button.clicked.connect(self.add_category)
        add_layout.addWidget(self.add_button)
        
        layout.addWidget(add_frame)
        
        # Categories list
        list_frame = QFrame()
        list_frame.setFrameStyle(QFrame.StyledPanel)
        list_layout = QVBoxLayout(list_frame)
        
        list_layout.addWidget(QLabel('Existing Custom Categories:'))
        
        self.categories_list = QListWidget()
        self.categories_list.itemDoubleClicked.connect(self.edit_category)
        list_layout.addWidget(self.categories_list)
        
        # List buttons
        list_buttons = QHBoxLayout()
        self.edit_button = QPushButton('Edit Selected')
        self.edit_button.clicked.connect(self.edit_category)
        self.delete_button = QPushButton('Delete Selected')
        self.delete_button.setStyleSheet('background:red;color:white;font-weight:bold')
        self.delete_button.clicked.connect(self.delete_category)
        
        list_buttons.addWidget(self.edit_button)
        list_buttons.addWidget(self.delete_button)
        list_buttons.addStretch()
        list_layout.addLayout(list_buttons)
        
        layout.addWidget(list_frame)
        
        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def load_categories(self):
        self.categories_list.clear()
        for category, keywords in self.custom_categories.items():
            item_text = f"{category}: {', '.join(keywords)}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, category)
            self.categories_list.addItem(item)
    
    def add_category(self):
        name = self.category_name_input.text().strip()
        keywords_text = self.keywords_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, 'Warning', 'Please enter a category name.')
            return
        
        if name in self.custom_categories:
            QMessageBox.warning(self, 'Warning', 'Category already exists.')
            return
        
        keywords = [k.strip() for k in keywords_text.split(',') if k.strip()]
        
        self.custom_categories[name] = keywords
        self.category_name_input.clear()
        self.keywords_input.clear()
        self.load_categories()
    
    def edit_category(self):
        current_item = self.categories_list.currentItem()
        if not current_item:
            QMessageBox.information(self, 'Info', 'Please select a category to edit.')
            return
        
        category = current_item.data(Qt.UserRole)
        current_keywords = self.custom_categories[category]
        
        # Get new name
        new_name, ok = QInputDialog.getText(self, 'Edit Category', 'Category Name:', text=category)
        if not ok or not new_name.strip():
            return
        
        # Get new keywords
        keywords_text, ok = QInputDialog.getText(self, 'Edit Keywords', 'Keywords (comma-separated):', 
                                                text=', '.join(current_keywords))
        if not ok:
            return
        
        new_keywords = [k.strip() for k in keywords_text.split(',') if k.strip()]
        
        # Update category
        if new_name != category:
            del self.custom_categories[category]
        
        self.custom_categories[new_name] = new_keywords
        self.load_categories()
    
    def delete_category(self):
        current_item = self.categories_list.currentItem()
        if not current_item:
            QMessageBox.information(self, 'Info', 'Please select a category to delete.')
            return
        
        category = current_item.data(Qt.UserRole)
        reply = QMessageBox.question(self, 'Confirm Delete', 
                                   f'Are you sure you want to delete the category "{category}"?')
        if reply == QMessageBox.Yes:
            del self.custom_categories[category]
            self.load_categories()
    
    def accept(self):
        save_custom_categories(self.custom_categories)
        super().accept()


# --- Main Window ------------------------------------------------------------
class BudgetApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Monthly Budget Calculator')
        self.resize(1100, 750)

        # Initialize settings and theme managers
        self.settings_manager = SettingsManager()
        self.theme_manager = ThemeManager(self.settings_manager)

        # Optimize database connection
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL")  # Better concurrency
        self.conn.execute("PRAGMA synchronous=NORMAL")  # Faster writes
        self.conn.execute("PRAGMA cache_size=10000")  # Larger cache
        self.conn.execute("PRAGMA temp_store=MEMORY")  # Use memory for temp tables
        ensure_schema(self.conn)
        self.cur = self.conn.cursor()

        self._build_ui()
        self._create_menu_bar()
        self._wire_events()

        # Backfill categories for legacy rows once
        self._backfill_missing_categories()

        self._refresh_totals()
        self._apply_filters()
        self._load_month_budget()
        
        # Apply saved theme
        self.theme_manager.apply_theme(QApplication.instance())

    def _create_menu_bar(self):
        """Create the application menu bar."""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu('&File')
        
        # New Database
        new_action = QAction('&New Database', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('Create a new database')
        new_action.triggered.connect(self._new_database)
        file_menu.addAction(new_action)
        
        # Open Database
        open_action = QAction('&Open Database...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open an existing database')
        open_action.triggered.connect(self._open_database)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        # Export
        export_action = QAction('&Export to Excel...', self)
        export_action.setShortcut('Ctrl+E')
        export_action.setStatusTip('Export data to Excel')
        export_action.triggered.connect(analyze_expenses_002.export_to_excel)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        # Exit
        exit_action = QAction('E&xit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit the application')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit Menu
        edit_menu = menubar.addMenu('&Edit')
        
        # Manage Categories
        categories_action = QAction('&Manage Categories...', self)
        categories_action.setShortcut('Ctrl+M')
        categories_action.setStatusTip('Manage custom expense categories')
        categories_action.triggered.connect(self._manage_categories)
        edit_menu.addAction(categories_action)
        
        edit_menu.addSeparator()
        
        # Clear Database
        clear_action = QAction('&Clear Database', self)
        clear_action.setStatusTip('Clear all expense data')
        clear_action.triggered.connect(self._clear_database)
        edit_menu.addAction(clear_action)
        
        # View Menu
        view_menu = menubar.addMenu('&View')
        
        # Theme submenu
        theme_menu = view_menu.addMenu('&Theme')
        
        # System theme
        system_theme_action = QAction('&System Default', self)
        system_theme_action.setCheckable(True)
        system_theme_action.triggered.connect(lambda: self._change_theme('system'))
        theme_menu.addAction(system_theme_action)
        
        # Light theme
        light_theme_action = QAction('&Light', self)
        light_theme_action.setCheckable(True)
        light_theme_action.triggered.connect(lambda: self._change_theme('light'))
        theme_menu.addAction(light_theme_action)
        
        # Dark theme
        dark_theme_action = QAction('&Dark', self)
        dark_theme_action.setCheckable(True)
        dark_theme_action.triggered.connect(lambda: self._change_theme('dark'))
        theme_menu.addAction(dark_theme_action)
        
        # Theme action group
        self.theme_action_group = QActionGroup(self)
        self.theme_action_group.addAction(system_theme_action)
        self.theme_action_group.addAction(light_theme_action)
        self.theme_action_group.addAction(dark_theme_action)
        
        # Set current theme
        current_theme = self.settings_manager.get('theme', 'system')
        if current_theme == 'system':
            system_theme_action.setChecked(True)
        elif current_theme == 'light':
            light_theme_action.setChecked(True)
        elif current_theme == 'dark':
            dark_theme_action.setChecked(True)
        
        view_menu.addSeparator()
        
        # Refresh
        refresh_action = QAction('&Refresh', self)
        refresh_action.setShortcut('F5')
        refresh_action.setStatusTip('Refresh the current view')
        refresh_action.triggered.connect(self._refresh_view)
        view_menu.addAction(refresh_action)
        
        # Tools Menu
        tools_menu = menubar.addMenu('&Tools')
        
        # Analyze Expenses
        analyze_action = QAction('&Analyze Expenses', self)
        analyze_action.setShortcut('Ctrl+A')
        analyze_action.setStatusTip('Analyze expense patterns')
        analyze_action.triggered.connect(analyze_expenses)
        tools_menu.addAction(analyze_action)
        
        tools_menu.addSeparator()
        
        # Settings
        settings_action = QAction('&Settings...', self)
        settings_action.setShortcut('Ctrl+,')
        settings_action.setStatusTip('Open application settings')
        settings_action.triggered.connect(self._open_settings)
        tools_menu.addAction(settings_action)
        
        # Help Menu
        help_menu = menubar.addMenu('&Help')
        
        # User Guide
        guide_action = QAction('&User Guide', self)
        guide_action.setShortcut('F1')
        guide_action.setStatusTip('Open user guide')
        guide_action.triggered.connect(self._open_user_guide)
        help_menu.addAction(guide_action)
        
        # Keyboard Shortcuts
        shortcuts_action = QAction('&Keyboard Shortcuts', self)
        shortcuts_action.setStatusTip('View keyboard shortcuts')
        shortcuts_action.triggered.connect(self._show_shortcuts)
        help_menu.addAction(shortcuts_action)
        
        help_menu.addSeparator()
        
        # Feedback
        feedback_action = QAction('&Send Feedback', self)
        feedback_action.setStatusTip('Send feedback to developer')
        feedback_action.triggered.connect(self._send_feedback)
        help_menu.addAction(feedback_action)
        
        help_menu.addSeparator()
        
        # About
        about_action = QAction('&About', self)
        about_action.setStatusTip('About Budget Calculator')
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    # --- Menu Action Methods ----------------------------------------------
    def _new_database(self):
        """Create a new database."""
        reply = QMessageBox.question(
            self, 'New Database', 
            'This will create a new database and clear all current data. Continue?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                # Close current connection
                self.conn.close()
                
                # Remove existing database
                if os.path.exists(DB_PATH):
                    os.remove(DB_PATH)
                
                # Create new database
                self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
                ensure_schema(self.conn)
                self.cur = self.conn.cursor()
                
                # Refresh UI
                self._refresh_totals()
                self._apply_filters()
                self._load_month_budget()
                
                QMessageBox.information(self, 'Success', 'New database created successfully!')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to create new database: {str(e)}')
    
    def _open_database(self):
        """Open an existing database."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Open Database', '', 'SQLite Database (*.db);;All Files (*)'
        )
        if file_path:
            try:
                # Close current connection
                self.conn.close()
                
                # Open new database
                self.conn = sqlite3.connect(file_path, check_same_thread=False)
                ensure_schema(self.conn)
                self.cur = self.conn.cursor()
                
                # Refresh UI
                self._refresh_totals()
                self._apply_filters()
                self._load_month_budget()
                
                QMessageBox.information(self, 'Success', f'Database opened: {file_path}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to open database: {str(e)}')
    
    def _change_theme(self, theme):
        """Change application theme."""
        self.theme_manager.apply_theme(QApplication.instance(), theme)
        self.settings_manager.set('theme', theme)
        self.settings_manager.save()
    
    def _refresh_view(self):
        """Refresh the current view."""
        self._refresh_totals()
        self._apply_filters()
    
    def _open_settings(self):
        """Open settings dialog."""
        dialog = SettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Apply theme changes if needed
            current_theme = self.settings_manager.get('theme', 'system')
            self.theme_manager.apply_theme(QApplication.instance(), current_theme)
            
            # Update theme menu
            for action in self.theme_action_group.actions():
                action.setChecked(False)
            
            if current_theme == 'system':
                self.theme_action_group.actions()[0].setChecked(True)
            elif current_theme == 'light':
                self.theme_action_group.actions()[1].setChecked(True)
            elif current_theme == 'dark':
                self.theme_action_group.actions()[2].setChecked(True)
    
    def _open_user_guide(self):
        """Open user guide."""
        QMessageBox.information(
            self, 'User Guide',
            'User guide is available in the documentation files.\n\n'
            'For detailed help, please refer to:\n'
            '- README.md (GitHub)\n'
            '- USER_GUIDE.md (User documentation)\n'
            '- DEVELOPER.md (Developer documentation)'
        )
    
    def _show_shortcuts(self):
        """Show keyboard shortcuts."""
        shortcuts_text = """
        <h3>Keyboard Shortcuts</h3>
        <table>
        <tr><td><b>Ctrl+N</b></td><td>New Database</td></tr>
        <tr><td><b>Ctrl+O</b></td><td>Open Database</td></tr>
        <tr><td><b>Ctrl+E</b></td><td>Export to Excel</td></tr>
        <tr><td><b>Ctrl+Q</b></td><td>Exit Application</td></tr>
        <tr><td><b>Ctrl+M</b></td><td>Manage Categories</td></tr>
        <tr><td><b>Ctrl+A</b></td><td>Analyze Expenses</td></tr>
        <tr><td><b>Ctrl+,</b></td><td>Settings</td></tr>
        <tr><td><b>F1</b></td><td>User Guide</td></tr>
        <tr><td><b>F5</b></td><td>Refresh View</td></tr>
        </table>
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle('Keyboard Shortcuts')
        msg.setText(shortcuts_text)
        msg.setTextFormat(Qt.RichText)
        msg.exec_()
    
    def _send_feedback(self):
        """Send feedback to developer."""
        QMessageBox.information(
            self, 'Send Feedback',
            'Thank you for your interest in providing feedback!\n\n'
            'Please send your feedback to:\n'
            'Email: aabdallah.atef.0x@gmail.com\n\n'
            'Include:\n'
            '- Description of the issue or suggestion\n'
            '- Steps to reproduce (if applicable)\n'
            '- Your system information\n'
            '- Any error messages you encountered'
        )
    
    def _show_about(self):
        """Show about dialog."""
        dialog = AboutDialog(self)
        dialog.exec_()

    def refresh_category_combo(self):
        """Refresh the category combo box with current categories."""
        self.cmb_category.clear()
        all_categories = get_all_categories()
        self.cmb_category.addItems(['Auto'] + list(all_categories.keys()))
        self.cmb_category.setCurrentText('Auto')

    def refresh_filter_category_combo(self):
        """Refresh the filter category combo box with current categories."""
        self.cmb_filter_category.clear()
        all_categories = get_all_categories()
        self.cmb_filter_category.addItems(['All'] + list(all_categories.keys()))
        self.cmb_filter_category.setCurrentText('All')

    def _manage_categories(self):
        """Open the custom categories management dialog."""
        dialog = CustomCategoriesDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Refresh category combos after changes
            self.refresh_category_combo()
            self.refresh_filter_category_combo()
            # Re-apply filters to update the display
            self._apply_filters()

    # --- UI -----------------------------------------------------------------
    def _build_ui(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)
        main = QVBoxLayout()
        root.setLayout(main)

        # Description
        desc_frame = QFrame()
        desc_layout = QVBoxLayout()
        desc_frame.setLayout(desc_layout)
        main.addWidget(desc_frame)

        desc_layout.addWidget(QLabel('Description'))
        self.txt_description = QTextEdit()
        self.txt_description.setFixedHeight(48)
        desc_layout.addWidget(self.txt_description)

        # Row: Amount | Category | Date | Add Expense
        row1 = QHBoxLayout()
        desc_layout.addLayout(row1)

        row1.addWidget(QLabel('Amount'))
        self.inp_amount = QLineEdit('0.0')
        self.inp_amount.setValidator(QDoubleValidator(0.0, 1e12, 2))
        self.inp_amount.setFixedWidth(120)
        row1.addWidget(self.inp_amount)

        row1.addWidget(QLabel('Category'))
        self.cmb_category = QComboBox()
        self.refresh_category_combo()
        self.cmb_category.setFixedWidth(140)
        row1.addWidget(self.cmb_category)

        row1.addWidget(QLabel('Date'))
        self.dt_add = QDateEdit()
        self.dt_add.setCalendarPopup(True)
        self.dt_add.setDate(QDate.currentDate())
        self.dt_add.setFixedWidth(140)
        row1.addWidget(self.dt_add)

        self.btn_add = QPushButton('Add Expense')
        self.btn_add.setStyleSheet('background:#4CAF50;color:white;font-weight:bold')
        row1.addStretch(1)
        row1.addWidget(self.btn_add)

        # Filters row: From | To | Category | Search | Apply | Range Total
        filters = QHBoxLayout()
        main.addLayout(filters)

        filters.addWidget(QLabel('Filter: From'))
        self.dt_from = QDateEdit()
        self.dt_from.setCalendarPopup(True)
        self.dt_from.setDate(QDate.currentDate().addDays(-30))
        filters.addWidget(self.dt_from)

        filters.addWidget(QLabel('To'))
        self.dt_to = QDateEdit()
        self.dt_to.setCalendarPopup(True)
        self.dt_to.setDate(QDate.currentDate())
        filters.addWidget(self.dt_to)

        filters.addWidget(QLabel('Category'))
        self.cmb_filter_category = QComboBox()
        self.refresh_filter_category_combo()
        self.cmb_filter_category.setFixedWidth(160)
        filters.addWidget(self.cmb_filter_category)

        filters.addWidget(QLabel('Search'))
        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText('text contains...')
        filters.addWidget(self.inp_search)

        self.btn_apply = QPushButton('Apply')
        self.btn_apply.setStyleSheet('background:#2196F3;color:white;font-weight:bold')
        filters.addWidget(self.btn_apply)

        self.lbl_range_total = QLabel('Range Total: $0.00')
        self.lbl_range_total.setFont(QFont('Arial', 10, QFont.Bold))
        self.lbl_range_total.setStyleSheet('color:#E91E63')
        filters.addWidget(self.lbl_range_total)

        # Table
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(['ID', 'Date', 'Description', 'Category', 'Amount'])
        self.table.horizontalHeader().setStretchLastSection(True)
        main.addWidget(self.table)

        # Row: Edit | Delete
        row_actions = QHBoxLayout()
        main.addLayout(row_actions)
        self.btn_edit = QPushButton('Edit Selected')
        self.btn_delete = QPushButton('Delete Selected')
        row_actions.addWidget(self.btn_edit)
        row_actions.addWidget(self.btn_delete)
        row_actions.addStretch(1)

        # Totals
        totals = QHBoxLayout()
        main.addLayout(totals)
        self.lbl_total = QLabel('Total Spent: $0.00')
        self.lbl_total.setFont(QFont('Arial', 12))
        totals.addWidget(self.lbl_total)
        self.lbl_month = QLabel('This Month: $0.00')
        self.lbl_month.setFont(QFont('Arial', 12))
        totals.addWidget(self.lbl_month)
        totals.addStretch(1)

        # Budget row
        budget = QHBoxLayout()
        main.addLayout(budget)
        budget.addWidget(QLabel('Monthly Budget'))
        self.inp_budget = QLineEdit('0.0')
        self.inp_budget.setValidator(QDoubleValidator(0.0, 1e12, 2))
        self.inp_budget.setFixedWidth(100)
        budget.addWidget(self.inp_budget)
        self.btn_save_budget = QPushButton('Save')
        self.btn_save_budget.setStyleSheet('background:#009688;color:white;font-weight:bold')
        budget.addWidget(self.btn_save_budget)
        self.progress = QProgressBar()
        self.progress.setFixedWidth(260)
        budget.addWidget(self.progress)
        self.lbl_remaining = QLabel('Remaining: $0.00')
        budget.addWidget(self.lbl_remaining)
        budget.addStretch(1)

        # Bottom actions
        bottom = QHBoxLayout()
        main.addLayout(bottom)
        self.btn_analyze = QPushButton('Analyze Expenses')
        self.btn_analyze.setStyleSheet('background:#FFC107;font-weight:bold')
        self.btn_export = QPushButton('Export to Excel')
        self.btn_export.setStyleSheet('background:#607D8B;color:white;font-weight:bold')
        self.btn_manage_categories = QPushButton('Manage Categories')
        self.btn_manage_categories.setStyleSheet('background:#9C27B0;color:white;font-weight:bold')
        self.btn_clear = QPushButton('Clear Database')
        self.btn_clear.setStyleSheet('background:red;color:white;font-weight:bold')
        bottom.addWidget(self.btn_analyze)
        bottom.addWidget(self.btn_export)
        bottom.addWidget(self.btn_manage_categories)
        bottom.addWidget(self.btn_clear)

    def _wire_events(self) -> None:
        self.btn_add.clicked.connect(self._add_expense)
        self.btn_apply.clicked.connect(self._apply_filters)
        self.dt_from.dateChanged.connect(self._apply_filters)
        self.dt_to.dateChanged.connect(self._apply_filters)
        self.cmb_filter_category.currentTextChanged.connect(self._apply_filters)
        self.inp_search.textChanged.connect(self._apply_filters)

        self.btn_delete.clicked.connect(self._delete_selected)
        self.btn_edit.clicked.connect(self._edit_selected_info)
        self.btn_save_budget.clicked.connect(self._save_month_budget)
        self.btn_analyze.clicked.connect(analyze_expenses)
        self.btn_export.clicked.connect(analyze_expenses_002.export_to_excel)
        self.btn_manage_categories.clicked.connect(self._manage_categories)
        self.btn_clear.clicked.connect(self._clear_database)

    # --- Actions -------------------------------------------------------------
    def _add_expense(self) -> None:
        desc = self.txt_description.toPlainText().strip()
        try:
            amount = float(self.inp_amount.text() or '0')
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Enter a valid amount.')
            return

        if not desc or amount <= 0:
            QMessageBox.critical(self, 'Error', 'Enter description and positive amount.')
            return

        qd = self.dt_add.date()
        date_str = datetime(qd.year(), qd.month(), qd.day()).strftime('%Y-%m-%d %H:%M:%S')

        chosen = self.cmb_category.currentText()
        category = detect_category(desc) if chosen == 'Auto' else chosen

        try:
            self.cur.execute(
                "INSERT INTO expenses(description, amount, category, date) VALUES(?,?,?,?)",
                (desc, amount, category, date_str)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error('DB insert failed: %s', e)
            QMessageBox.critical(self, 'DB Error', str(e))
            return

        self.txt_description.clear()
        self.inp_amount.setText('0.0')
        self.cmb_category.setCurrentText('Auto')
        self._refresh_totals()
        self._apply_filters()

    def _apply_filters(self) -> None:
        # Build base query with optimized structure
        base_conditions = ["1=1"]
        params = []

        # Date range filter
        f = self.dt_from.date()
        t = self.dt_to.date()
        base_conditions.append("date(date) >= ? AND date(date) <= ?")
        params.extend([QDate(f).toString('yyyy-MM-dd'), QDate(t).toString('yyyy-MM-dd')])

        # Category filter
        cat = self.cmb_filter_category.currentText()
        if cat != 'All':
            base_conditions.append("category = ?")
            params.append(cat)

        # Search filter
        s = (self.inp_search.text() or '').strip()
        if s:
            base_conditions.append("description LIKE ?")
            params.append(f"%{s}%")

        where_clause = " AND ".join(base_conditions)
        
        # Main query for table data
        q = f"SELECT id, date, description, COALESCE(category,'Others'), amount FROM expenses WHERE {where_clause} ORDER BY date DESC, id DESC"

        try:
            self.cur.execute(q, params)
            rows = self.cur.fetchall()
        except sqlite3.Error as e:
            logging.error('DB select failed: %s', e)
            QMessageBox.critical(self, 'DB Error', str(e))
            return

        # Optimize table updates by disabling sorting during bulk insert
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        
        # Pre-allocate table rows for better performance
        if rows:
            self.table.setRowCount(len(rows))
            
        for i, (rid, dstr, desc, cat, amt) in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(rid)))
            self.table.setItem(i, 1, QTableWidgetItem(dstr))
            self.table.setItem(i, 2, QTableWidgetItem(desc))
            self.table.setItem(i, 3, QTableWidgetItem(cat))
            self.table.setItem(i, 4, QTableWidgetItem(f"{amt:.2f}"))
        
        # Re-enable sorting
        self.table.setSortingEnabled(True)

        # Range total - use same conditions but different query
        try:
            total_query = f"SELECT SUM(amount) FROM expenses WHERE {where_clause}"
            self.cur.execute(total_query, params)
            rtotal = self.cur.fetchone()[0] or 0.0
        except Exception:
            rtotal = 0.0
        self.lbl_range_total.setText(f"Range Total: ${rtotal:.2f}")

        self._refresh_totals()

    def _delete_selected(self) -> None:
        sel = self.table.currentRow()
        if sel < 0:
            QMessageBox.information(self, 'Info', 'Select a row to delete.')
            return
        rid_item = self.table.item(sel, 0)
        if not rid_item:
            return
        rid = int(rid_item.text())
        if QMessageBox.question(self, 'Confirm', f'Delete expense ID {rid}?') != QMessageBox.Yes:
            return
        try:
            self.cur.execute('DELETE FROM expenses WHERE id = ?', (rid,))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error('DB delete failed: %s', e)
            QMessageBox.critical(self, 'DB Error', str(e))
            return
        self._apply_filters()

    def _edit_selected_info(self) -> None:
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, 'Edit Expense', 'Select a row to edit.')
            return
        rid_item = self.table.item(row, 0)
        if not rid_item:
            return
        rid = int(rid_item.text())

        # Load current values
        try:
            self.cur.execute(
                "SELECT description, amount, category, date FROM expenses WHERE id = ?",
                (rid,)
            )
            row_data = self.cur.fetchone()
        except sqlite3.Error as e:
            logging.error('DB fetch for edit failed: %s', e)
            QMessageBox.critical(self, 'DB Error', str(e))
            return
        if not row_data:
            return
        cur_desc, cur_amt, cur_cat, cur_date = row_data

        # Build dialog
        dlg = QDialog(self)
        dlg.setWindowTitle('Edit Expense')
        lay = QVBoxLayout(dlg)

        lay_row1 = QVBoxLayout()
        lay.addLayout(lay_row1)
        lay_row1.addWidget(QLabel('Description'))
        ed_desc = QTextEdit()
        ed_desc.setFixedHeight(60)
        ed_desc.setPlainText(cur_desc or '')
        lay_row1.addWidget(ed_desc)

        row_inputs = QHBoxLayout()
        lay.addLayout(row_inputs)
        row_inputs.addWidget(QLabel('Amount'))
        ed_amt = QLineEdit(f"{float(cur_amt or 0):.2f}")
        ed_amt.setValidator(QDoubleValidator(0.0, 1e12, 2))
        ed_amt.setFixedWidth(120)
        row_inputs.addWidget(ed_amt)

        row_inputs.addWidget(QLabel('Category'))
        ed_cat = QComboBox()
        all_categories = get_all_categories()
        ed_cat.addItems(list(all_categories.keys()))
        if cur_cat and cur_cat in all_categories:
            ed_cat.setCurrentText(cur_cat)
        row_inputs.addWidget(ed_cat)

        row_inputs.addWidget(QLabel('Date'))
        ed_date = QDateEdit()
        ed_date.setCalendarPopup(True)
        try:
            dt = datetime.strptime(cur_date, '%Y-%m-%d %H:%M:%S')
            ed_date.setDate(QDate(dt.year, dt.month, dt.day))
        except Exception:
            ed_date.setDate(QDate.currentDate())
        row_inputs.addWidget(ed_date)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        lay.addWidget(buttons)

        def on_save():
            new_desc = ed_desc.toPlainText().strip()
            try:
                new_amt = float(ed_amt.text() or '0')
            except ValueError:
                QMessageBox.critical(dlg, 'Error', 'Enter a valid amount.')
                return
            if not new_desc or new_amt <= 0:
                QMessageBox.critical(dlg, 'Error', 'Enter description and positive amount.')
                return
            nd = ed_date.date()
            nds = datetime(nd.year(), nd.month(), nd.day()).strftime('%Y-%m-%d %H:%M:%S')
            chosen = ed_cat.currentText()
            # If user didn't explicitly choose, detect from text
            final_cat = chosen or detect_category(new_desc)
            try:
                self.cur.execute(
                    'UPDATE expenses SET description=?, amount=?, category=?, date=? WHERE id=?',
                    (new_desc, new_amt, final_cat, nds, rid)
                )
                self.conn.commit()
            except sqlite3.Error as e:
                logging.error('DB update failed: %s', e)
                QMessageBox.critical(dlg, 'DB Error', str(e))
                return
            dlg.accept()

        buttons.accepted.connect(on_save)
        buttons.rejected.connect(dlg.reject)
        if dlg.exec_() == QDialog.Accepted:
            self._apply_filters()

    def _refresh_totals(self) -> None:
        # Use a single query to get all totals at once for better performance
        month_prefix = date.today().strftime('%Y-%m')
        
        try:
            # Get total and monthly total in one query
            self.cur.execute("""
                SELECT 
                    SUM(amount) as total,
                    SUM(CASE WHEN strftime('%Y-%m', date) = ? THEN amount ELSE 0 END) as monthly_total
                FROM expenses
            """, (month_prefix,))
            
            result = self.cur.fetchone()
            total = result[0] or 0.0 if result else 0.0
            mtotal = result[1] or 0.0 if result else 0.0
            
        except sqlite3.Error:
            total = 0.0
            mtotal = 0.0
            
        self.lbl_total.setText(f'Total Spent: ${total:.2f}')
        self.lbl_month.setText(f'This Month: ${mtotal:.2f}')

        # Get budget
        try:
            mkey = date.today().strftime('%Y-%m')
            self.cur.execute('SELECT amount FROM budgets WHERE month = ?', (mkey,))
            budget = (self.cur.fetchone() or (0.0,))[0]
        except sqlite3.Error:
            budget = 0.0
            
        remaining = budget - mtotal
        self.lbl_remaining.setText(f'Remaining: ${remaining:.2f}')
        
        # Update progress bar
        progress_value = 0
        if budget > 0:
            progress_value = max(0, min(100, int((mtotal / budget) * 100)))
        self.progress.setValue(progress_value)

    def _load_month_budget(self) -> None:
        mkey = date.today().strftime('%Y-%m')
        try:
            self.cur.execute('SELECT amount FROM budgets WHERE month = ?', (mkey,))
            row = self.cur.fetchone()
            self.inp_budget.setText(f"{(row[0] if row else 0.0):.2f}")
        except sqlite3.Error:
            self.inp_budget.setText('0.0')
        self._refresh_totals()

    def _save_month_budget(self) -> None:
        mkey = date.today().strftime('%Y-%m')
        try:
            amount = float(self.inp_budget.text() or '0')
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Enter a valid budget amount.')
            return
        try:
            self.cur.execute(
                "INSERT INTO budgets(month, amount) VALUES(?, ?) ON CONFLICT(month) DO UPDATE SET amount=excluded.amount",
                (mkey, amount)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error('DB upsert budget failed: %s', e)
            QMessageBox.critical(self, 'DB Error', str(e))
            return
        self._refresh_totals()

    def _clear_database(self) -> None:
        if QMessageBox.question(self, 'Clear Database', 'Are you sure? This deletes all data.') != QMessageBox.Yes:
            return
        try:
            self.cur.execute('DELETE FROM expenses')
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error('DB clear failed: %s', e)
            QMessageBox.critical(self, 'DB Error', str(e))
            return
        self._apply_filters()

    def _backfill_missing_categories(self) -> None:
        """Auto-categorize legacy rows that have NULL/empty/unknown category.
        Run once on startup; safe to run multiple times.
        """
        try:
            self.cur.execute(
                "SELECT id, description FROM expenses WHERE category IS NULL OR category = '' OR category = 'Others'"
            )
            rows = self.cur.fetchall()
            changed = 0
            for rid, desc in rows:
                new_cat = detect_category(desc)
                if new_cat and new_cat != 'Others':
                    self.cur.execute('UPDATE expenses SET category=? WHERE id=?', (new_cat, rid))
                    changed += 1
            if changed:
                self.conn.commit()
                logging.info('Backfilled categories for %s rows', changed)
        except sqlite3.Error as e:
            logging.error('Backfill categories failed: %s', e)

    # --- lifecycle ----------------------------------------------------------
    def closeEvent(self, event) -> None:  # type: ignore[override]
        try:
            self.conn.close()
        finally:
            event.accept()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = BudgetApp()
    w.show()
    sys.exit(app.exec_())


