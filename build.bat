@echo off
echo Budget Calculator Build Script
echo ==============================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if PyInstaller is available
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

REM Run the build script
echo Running build script...
python build.py

if errorlevel 1 (
    echo Build failed!
    echo.
    echo If the error is related to NSIS:
    echo 1. Check NSIS_TROUBLESHOOTING.md for solutions
    echo 2. Try running build_installer.bat separately
    echo 3. Or just use the portable version in dist/
    pause
    exit /b 1
) else (
    echo Build completed successfully!
    echo.
    echo Output files are in the 'dist' directory
    echo Executable: dist/BudgetCalculator.exe
    echo Portable: dist/BudgetCalculator_Portable/
    
    REM Check if installer was created
    if exist "BudgetCalculatorSetup.exe" (
        echo Installer: BudgetCalculatorSetup.exe
    ) else (
        echo Installer: Not created (NSIS not found)
        echo To create installer manually, run: build_installer.bat
    )
    
    echo.
    echo If you need to create the installer separately:
    echo 1. Run: build_installer.bat
    echo 2. Or see NSIS_TROUBLESHOOTING.md for help
)

pause
