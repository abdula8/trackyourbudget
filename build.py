#!/usr/bin/env python3
"""
Build script for Budget Calculator Application
Compiles Python to EXE and creates installer package
"""

import os
import sys
import subprocess
import shutil
import glob
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print("SUCCESS!")
        if result.stdout:
            print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {description} failed!")
        print(f"Return code: {e.returncode}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def check_dependencies():
    """Check if required tools are installed"""
    print("Checking dependencies...")
    
    # Check Python
    if sys.version_info < (3, 7):
        print("ERROR: Python 3.7 or higher is required")
        return False
    
    # Check PyInstaller
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("ERROR: PyInstaller not found. Install with: pip install pyinstaller")
        return False
    # Check if NSIS is available (optional)
    nsis_paths = [
        "makensis",  # In PATH
        "C:\\Program Files (x86)\\NSIS\\makensis.exe",  # Default x86 install
        "C:\\Program Files\\NSIS\\makensis.exe",  # Default x64 install
        "C:\\NSIS\\makensis.exe",  # Custom install
    ]
    nsis_found = False
    for path in nsis_paths:
        try:
            subprocess.run(f'"{path}" /VERSION', shell=True, check=True, capture_output=True, text=True)
            print(f"✓ NSIS found at: {path}")
            nsis_found = True
            break
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    if not nsis_found:
        print("NSIS not found in common locations. Trying to find it in PATH...")
        try:
            result = subprocess.run("where makensis", shell=True, capture_output=True, text=True, check=True)
            if result.returncode == 0:
                print(f"✓ NSIS found in PATH: {result.stdout.strip()}")
                nsis_found = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    
    if not nsis_found:
        print("WARNING: NSIS not found. Installer creation will be skipped.")
        print("Download NSIS from: https://nsis.sourceforge.io/")
        return False
    
    return True

# def clean_build_dirs():
#     """Clean previous build artifacts"""
#     print("\nCleaning build directories...")
    
#     dirs_to_clean = ['build', 'dist', '__pycache__']
#     files_to_clean = ['*.spec']
    
#     for dir_name in dirs_to_clean:
#         if os.path.exists(dir_name):
#             shutil.rmtree(dir_name)
#             print(f"Removed {dir_name}/")
    
#     for pattern in files_to_clean:
#         for file in glob.glob(pattern):
#             os.remove(file)
#             print(f"Removed {file}")
def clean_build_dirs():
    """Clean previous build artifacts"""
    print("\nCleaning build directories...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name, ignore_errors=False)
                print(f"Removed {dir_name}/")
            except PermissionError as e:
                print(f"WARNING: Could not remove {dir_name}/ due to permission error: {e}")
                print(f"Continuing build without deleting {dir_name}/")
            except Exception as e:
                print(f"ERROR: Failed to remove {dir_name}/: {e}")
                return False
    
    for pattern in files_to_clean:
        for file in glob.glob(pattern):
            try:
                os.remove(file)
                print(f"Removed {file}")
            except PermissionError as e:
                print(f"WARNING: Could not remove {file} due to permission error: {e}")
                print(f"Continuing build without deleting {file}")
            except Exception as e:
                print(f"ERROR: Failed to remove {file}: {e}")
                return False
    
    return True
def create_exe():
    """Create executable using PyInstaller"""
    print("\nCreating executable...")
    
    # PyInstaller command with optimizations
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window
        "--name=BudgetCalculator",
        "--icon=app.ico",
        "--add-data=app.ico;.",
        "--add-data=app.png;.",
        "--add-data=LICENSE.txt;.",
        "--add-data=README.txt;.",
        "--add-data=USER_GUIDE.md;.",
        "--add-data=DEVELOPER.md;.",
        "--add-data=FEATURE_SUGGESTIONS.md;.",
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui", 
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=PyQt5.QtWidgets.QButtonGroup",
        "--hidden-import=PyQt5.QtWidgets.QActionGroup",
        "--hidden-import=PyQt5.QtWidgets.QMenuBar",
        "--hidden-import=PyQt5.QtWidgets.QMenu",
        "--hidden-import=PyQt5.QtWidgets.QAction",
        "--hidden-import=PyQt5.QtWidgets.QFileDialog",
        "--hidden-import=PyQt5.QtWidgets.QTabWidget",
        "--hidden-import=PyQt5.QtWidgets.QGroupBox",
        "--hidden-import=PyQt5.QtWidgets.QRadioButton",
        "--hidden-import=PyQt5.QtWidgets.QTextBrowser",
        "--hidden-import=PyQt5.QtWidgets.QFormLayout",
        "--hidden-import=PyQt5.QtCore.QSettings",
        "--hidden-import=PyQt5.QtGui.QPalette",
        "--hidden-import=PyQt5.QtGui.QColor",
        "--hidden-import=sqlite3",
        "--hidden-import=matplotlib",
        "--hidden-import=analyze_expenses",
        "--hidden-import=analyze_expenses_002",
        "--optimize=2",  # Python optimization level
        "--strip",  # Strip debug symbols
        "main_qt.py"
    ]
    
    return run_command(" ".join(cmd), "PyInstaller compilation")

def create_installer():
    """Create NSIS installer"""
    print("\nCreating installer...")
    
    # Check if NSIS is available with multiple methods
    nsis_paths = [
        "makensis",  # In PATH
        "C:\\Program Files (x86)\\NSIS\\makensis.exe",  # Default x86 install
        "C:\\Program Files\\NSIS\\makensis.exe",  # Default x64 install
        "C:\\NSIS\\makensis.exe",  # Custom install
    ]
    
    nsis_found = False
    nsis_cmd = None
    
    for path in nsis_paths:
        try:
            subprocess.run(f'"{path}" /VERSION', shell=True, check=True, capture_output=True)
            nsis_cmd = f'"{path}"'
            nsis_found = True
            print(f"Found NSIS at: {path}")
            break
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    if not nsis_found:
        print("NSIS not found in common locations. Trying to find it...")
        # Try to find NSIS in PATH
        try:
            result = subprocess.run("where makensis", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                nsis_cmd = "makensis"
                nsis_found = True
                print(f"Found NSIS in PATH: {result.stdout.strip()}")
        except:
            pass
    
    if not nsis_found:
        print("NSIS not available, skipping installer creation")
        print("To install NSIS:")
        print("1. Download from: https://nsis.sourceforge.io/")
        print("2. Install to default location")
        print("3. Add to PATH or run build script from NSIS directory")
        return True
    
    # Copy AnyDesk.exe to current directory if it exists
    anydesk_src = "AnyDesk.exe"
    if os.path.exists(anydesk_src):
        print(f"Found {anydesk_src}, including in installer")
    else:
        print(f"WARNING: {anydesk_src} not found, AnyDesk installation will be skipped")
    
    # Run NSIS
    return run_command(f"{nsis_cmd} installer.nsi", "NSIS installer creation")

def copy_additional_files():
    """Copy additional files to dist directory"""
    print("\nCopying additional files...")
    
    dist_dir = "dist"
    if not os.path.exists(dist_dir):
        print("ERROR: dist directory not found")
        return False
    
    # Files to copy
    files_to_copy = [
        "LICENSE.txt",
        "README.txt", 
        "app.ico",
        "app.png"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, dist_dir)
            print(f"Copied {file}")
        else:
            print(f"WARNING: {file} not found")
    
    return True

def create_portable_version():
    """Create portable version with all dependencies"""
    print("\nCreating portable version...")
    
    dist_dir = "dist"
    portable_dir = "dist/BudgetCalculator_Portable"
    
    if not os.path.exists(dist_dir):
        print("ERROR: dist directory not found")
        return False
    
    # Create portable directory
    os.makedirs(portable_dir, exist_ok=True)
    
    # Copy main executable
    exe_src = os.path.join(dist_dir, "BudgetCalculator.exe")
    exe_dst = os.path.join(portable_dir, "BudgetCalculator.exe")
    
    if os.path.exists(exe_src):
        shutil.copy2(exe_src, exe_dst)
        print(f"Copied executable to portable version")
    
    # Copy additional files
    files_to_copy = ["LICENSE.txt", "README.txt", "app.ico", "app.png"]
    for file in files_to_copy:
        src = os.path.join(dist_dir, file)
        dst = os.path.join(portable_dir, file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {file} to portable version")
    
    # Create portable README
    portable_readme = os.path.join(portable_dir, "PORTABLE_README.txt")
    with open(portable_readme, 'w') as f:
        f.write("""BUDGET CALCULATOR - PORTABLE VERSION

This is a portable version of Budget Calculator that can run without installation.

To use:
1. Double-click BudgetCalculator.exe
2. The application will create necessary data files in the same directory
3. No installation required - just run the executable

Note: This version includes all dependencies and may be larger than the installer version.
""")
    
    print(f"Portable version created in: {portable_dir}")
    return True

def main():
    """Main build process"""
    print("Budget Calculator Build Script")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\nBuild failed due to missing dependencies")
        return False
    
    # Clean previous builds
    clean_build_dirs()
    
    # Create executable
    if not create_exe():
        print("\nBuild failed at executable creation")
        return False
    
    # Copy additional files
    if not copy_additional_files():
        print("\nBuild failed at file copying")
        return False
    
    # Create portable version
    if not create_portable_version():
        print("\nWarning: Portable version creation failed")
    
    # Create installer
    if not create_installer():
        print("\nWarning: Installer creation failed")
    
    print("\n" + "=" * 50)
    print("BUILD COMPLETED!")
    print("=" * 50)
    print("\nOutput files:")
    
    # List output files
    dist_dir = "dist"
    if os.path.exists(dist_dir):
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = os.path.join(root, file)
                size = os.path.getsize(file_path)
                print(f"  {file_path} ({size:,} bytes)")
    
    print(f"\nExecutable location: {os.path.join(dist_dir, 'BudgetCalculator.exe')}")
    print(f"Installer location: BudgetCalculatorSetup.exe")
    print(f"Portable version: {os.path.join(dist_dir, 'BudgetCalculator_Portable')}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
