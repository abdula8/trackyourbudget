# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main_qt.py'],
    pathex=[],
    binaries=[],
    datas=[('app.ico', '.'), ('app.png', '.'), ('LICENSE.txt', '.'), ('README.txt', '.'), ('USER_GUIDE.md', '.'), ('DEVELOPER.md', '.'), ('FEATURE_SUGGESTIONS.md', '.')],
    hiddenimports=['PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'PyQt5.QtWidgets.QButtonGroup', 'PyQt5.QtWidgets.QActionGroup', 'PyQt5.QtWidgets.QMenuBar', 'PyQt5.QtWidgets.QMenu', 'PyQt5.QtWidgets.QAction', 'PyQt5.QtWidgets.QFileDialog', 'PyQt5.QtWidgets.QTabWidget', 'PyQt5.QtWidgets.QGroupBox', 'PyQt5.QtWidgets.QRadioButton', 'PyQt5.QtWidgets.QTextBrowser', 'PyQt5.QtWidgets.QFormLayout', 'PyQt5.QtCore.QSettings', 'PyQt5.QtGui.QPalette', 'PyQt5.QtGui.QColor', 'sqlite3', 'matplotlib', 'analyze_expenses', 'analyze_expenses_002'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('O', None, 'OPTION'), ('O', None, 'OPTION')],
    name='BudgetCalculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app.ico'],
)
