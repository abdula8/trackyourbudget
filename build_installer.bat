@echo off
echo Building NSIS Installer for Budget Calculator
echo =============================================

REM Check if NSIS is available
where makensis >nul 2>&1
if %errorlevel% neq 0 (
    echo NSIS not found in PATH. Trying common locations...
    
    REM Try common NSIS installation paths
    if exist "C:\Program Files (x86)\NSIS\makensis.exe" (
        set NSIS_PATH="C:\Program Files (x86)\NSIS\makensis.exe"
        echo Found NSIS at: C:\Program Files (x86)\NSIS\
        goto :build
    )
    
    if exist "C:\Program Files\NSIS\makensis.exe" (
        set NSIS_PATH="C:\Program Files\NSIS\makensis.exe"
        echo Found NSIS at: C:\Program Files\NSIS\
        goto :build
    )
    
    if exist "C:\NSIS\makensis.exe" (
        set NSIS_PATH="C:\NSIS\makensis.exe"
        echo Found NSIS at: C:\NSIS\
        goto :build
    )
    
    echo ERROR: NSIS not found!
    echo.
    echo Please install NSIS from: https://nsis.sourceforge.io/
    echo Or add NSIS to your PATH environment variable
    echo.
    echo Common installation paths:
    echo - C:\Program Files (x86)\NSIS\
    echo - C:\Program Files\NSIS\
    echo - C:\NSIS\
    echo.
    pause
    exit /b 1
) else (
    set NSIS_PATH=makensis
    echo Found NSIS in PATH
)

:build
echo.
echo Building installer with NSIS...
echo Command: %NSIS_PATH% installer.nsi
echo.

REM Check if installer.nsi exists
if not exist "installer.nsi" (
    echo ERROR: installer.nsi not found!
    echo Make sure you're running this from the project directory.
    pause
    exit /b 1
)

REM Run NSIS
%NSIS_PATH% installer.nsi

if %errorlevel% equ 0 (
    echo.
    echo =============================================
    echo Installer created successfully!
    echo Output: BudgetCalculatorSetup.exe
    echo =============================================
) else (
    echo.
    echo =============================================
    echo ERROR: Installer creation failed!
    echo Check the error messages above.
    echo =============================================
    pause
    exit /b 1
)

echo.
echo Installer is ready for distribution!
pause
