; Budget Calculator Installer Script
; NSIS (Nullsoft Scriptable Install System) installer

!define APP_NAME "Budget Calculator"
!define APP_VERSION "1.0.0"
!define APP_PUBLISHER "Budget Calculator Team"
!define APP_WEB_SITE "https://example.com"
!define APP_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
!define APP_UNINST_ROOT_KEY "HKLM"

; Modern UI
!include "MUI2.nsh"

; General
Name "${APP_NAME} ${APP_VERSION}"
OutFile "BudgetCalculatorSetup.exe"
InstallDir "$PROGRAMFILES\${APP_NAME}"
InstallDirRegKey HKLM "Software\${APP_NAME}" ""
RequestExecutionLevel admin

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "app.ico"
!define MUI_UNICON "app.ico"

; Welcome page
!define MUI_WELCOMEPAGE_TITLE "Welcome to ${APP_NAME} Setup"
!define MUI_WELCOMEPAGE_TEXT "This wizard will guide you through the installation of ${APP_NAME} ${APP_VERSION}.$\r$\n$\r$\n${APP_NAME} is a powerful tool for managing your monthly budget and tracking expenses.$\r$\n$\r$\nClick Next to continue."
!insertmacro MUI_PAGE_WELCOME

; License page
!define MUI_LICENSEPAGE_TEXT_TOP "Please review the license terms before installing ${APP_NAME}."
!define MUI_LICENSEPAGE_TEXT_BOTTOM "If you accept the terms of the agreement, click I Agree to continue. You must accept the agreement to install ${APP_NAME}."
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"

; Components page
!define MUI_COMPONENTSPAGE_TEXT_TOP "Select the components you want to install. Click Next to continue."
!insertmacro MUI_PAGE_COMPONENTS

; Directory page
!define MUI_DIRECTORYPAGE_TEXT_TOP "Setup will install ${APP_NAME} in the following folder. To install in a different folder, click Browse and select another folder. Click Next to continue."
!insertmacro MUI_PAGE_DIRECTORY

; Instfiles page
!insertmacro MUI_PAGE_INSTFILES

; Finish page
!define MUI_FINISHPAGE_TITLE "Completing the ${APP_NAME} Setup Wizard"
!define MUI_FINISHPAGE_TEXT "${APP_NAME} has been installed on your computer.$\r$\n$\r$\nClick Finish to close this wizard."
!define MUI_FINISHPAGE_RUN "$INSTDIR\BudgetCalculator.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Run ${APP_NAME} now"
!define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\README.txt"
!define MUI_FINISHPAGE_SHOWREADME_TEXT "Show README"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Language
!insertmacro MUI_LANGUAGE "English"

; Set default component selections
InstType "Full"  ; Defines a "Full" installation type that includes all components

; Installer sections
Section "!${APP_NAME}" SecMain
  SectionIn RO  ; Required component
  SetOutPath "$INSTDIR"
  
  ; Main application files
  File "dist\BudgetCalculator.exe"  ; Adjusted to match build.py output
  File "dist\app.ico"
  File "dist\app.png"
  File "dist\LICENSE.txt"
  File "dist\README.txt"
  File "dist\USER_GUIDE.md"
  File "dist\DEVELOPER.md"
  File "dist\FEATURE_SUGGESTIONS.md"
  
  ; Create directories
  CreateDirectory "$INSTDIR\data"
  CreateDirectory "$INSTDIR\logs"
  
  ; Store installation folder
  WriteRegStr HKLM "Software\${APP_NAME}" "" $INSTDIR
  
  ; Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  ; Add to Add/Remove Programs
  WriteRegStr ${APP_UNINST_ROOT_KEY} "${APP_UNINST_KEY}" "DisplayName" "${APP_NAME}"
  WriteRegStr ${APP_UNINST_ROOT_KEY} "${APP_UNINST_KEY}" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr ${APP_UNINST_ROOT_KEY} "${APP_UNINST_KEY}" "DisplayIcon" "$INSTDIR\app.ico"
  WriteRegStr ${APP_UNINST_ROOT_KEY} "${APP_UNINST_KEY}" "DisplayVersion" "${APP_VERSION}"
  WriteRegStr ${APP_UNINST_ROOT_KEY} "${APP_UNINST_KEY}" "Publisher" "${APP_PUBLISHER}"
  WriteRegStr ${APP_UNINST_ROOT_KEY} "${APP_UNINST_KEY}" "URLInfoAbout" "${APP_WEB_SITE}"
  WriteRegDWORD ${APP_UNINST_ROOT_KEY} "${APP_UNINST_KEY}" "NoModify" 1
  WriteRegDWORD ${APP_UNINST_ROOT_KEY} "${APP_UNINST_KEY}" "NoRepair" 1
SectionEnd

Section "Desktop Shortcut" SecDesktop
  SectionIn 1  ; Component 1 (Full install)
  CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\BudgetCalculator.exe" "" "$INSTDIR\app.ico"
SectionEnd

Section "Start Menu Shortcut" SecStartMenu
  SectionIn 1  ; Component 1 (Full install)
  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\BudgetCalculator.exe" "" "$INSTDIR\app.ico"
  CreateShortCut "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Install AnyDesk" SecAnyDesk
  SectionIn 1  ; Component 1 (Full install)
  SetOutPath "$INSTDIR\AnyDesk"
  File "AnyDesk.exe"
  CreateShortCut "$SMPROGRAMS\${APP_NAME}\AnyDesk.lnk" "$INSTDIR\AnyDesk\AnyDesk.exe" "" "$INSTDIR\AnyDesk\AnyDesk.exe"
SectionEnd

; Section descriptions
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} "The main application files. This component is required."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} "Create a desktop shortcut for easy access."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} "Create Start Menu shortcuts and program group."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecAnyDesk} "Install AnyDesk remote desktop software for support purposes."
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; Uninstaller section
Section "Uninstall"
  ; Remove files and directories
  Delete "$INSTDIR\BudgetCalculator.exe"
  Delete "$INSTDIR\app.ico"
  Delete "$INSTDIR\app.png"
  Delete "$INSTDIR\LICENSE.txt"
  Delete "$INSTDIR\README.txt"
  Delete "$INSTDIR\USER_GUIDE.md"
  Delete "$INSTDIR\DEVELOPER.md"
  Delete "$INSTDIR\FEATURE_SUGGESTIONS.md"
  Delete "$INSTDIR\Uninstall.exe"
  
  ; Remove AnyDesk
  Delete "$INSTDIR\AnyDesk\AnyDesk.exe"
  RMDir "$INSTDIR\AnyDesk"
  
  ; Remove directories (only if empty)
  RMDir "$INSTDIR\data"
  RMDir "$INSTDIR\logs"
  RMDir "$INSTDIR"
  
  ; Remove shortcuts
  Delete "$DESKTOP\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\AnyDesk.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
  RMDir "$SMPROGRAMS\${APP_NAME}"
  
  ; Remove registry entries
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
  DeleteRegKey HKLM "Software\${APP_NAME}"
SectionEnd