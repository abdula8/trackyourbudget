@echo off
REM Build & package pipeline for BudgetApp -> portable exe + NSIS installer
REM Usage: run as administrator if you want to create installers that write to Program Files

REM -------------------------
REM CONFIG
REM -------------------------
set PYTHON=python
set VENV_DIR=.venv_build
set DIST_DIR=dist
set BUILD_DIR=build
set INSTALLER_STAGED=installer_staged
set OUTPUT_INSTALLER=BudgetApp-Setup.exe
set APP_NAME=BudgetApp
set MAIN_SCRIPT=main_qt.py
set SPEC_FILE=BudgetApp.spec
set PREPARE_SCRIPT=prepare_installer.py

REM Optional: replace with path to makensis if not in PATH
set MAKENSIS=makensis

REM -------------------------
REM Create virtual environment and install requirements
REM -------------------------
REM if not exist "%VENV_DIR%" (
REM    %PYTHON% -m venv "%VENV_DIR%"
REM )

REM call "%VENV_DIR%\Scripts\activate.bat"

echo Installing requirements...
if exist requirements.txt (
    pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo No requirements.txt found - ensure PyQt5, matplotlib, sqlite3 available.
)

REM -------------------------
REM Clean previous builds
REM -------------------------
rmdir /s /q "%DIST_DIR%" 2>nul
rmdir /s /q "%BUILD_DIR%" 2>nul
rmdir /s /q "%INSTALLER_STAGED%" 2>nul
del "%OUTPUT_INSTALLER%" 2>nul

REM -------------------------
REM Run PyInstaller
REM -------------------------
echo Running PyInstaller...
pyinstaller --clean --noconfirm "%SPEC_FILE%"
if %ERRORLEVEL% neq 0 (
    echo PyInstaller failed.
    pause
    exit /b 1
)

REM -------------------------
REM Prepare installer staging folder
REM -------------------------
echo Preparing installer files...
python "%PREPARE_SCRIPT%" --dist "%DIST_DIR%" --out "%INSTALLER_STAGED%" --appname "%APP_NAME%" --main-exe "%DIST_DIR%\%APP_NAME%.exe"

if %ERRORLEVEL% neq 0 (
    echo prepare_installer.py failed.
    pause
    exit /b 1
)

REM -------------------------
REM Build NSIS installer
REM -------------------------
echo Building NSIS installer...
"%MAKENSIS%" /V4 /X"SetOutPath %CD%" installer.nsi
if %ERRORLEVEL% neq 0 (
    echo NSIS build failed.
    pause
    exit /b 1
)

echo Done. Installer created: %OUTPUT_INSTALLER%
pause
