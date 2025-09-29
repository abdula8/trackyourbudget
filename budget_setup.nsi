!define APP_NAME "Budget Calculator"
!define APP_VERSION "1.0"
!define APP_EXE "BudgetCalculator.exe"
!define INSTALL_DIR "$PROGRAMFILES\${APP_NAME}"
!define UNINSTALL_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"

!include "MUI2.nsh"  ; Modern UI

; Pages
!define MUI_WELCOMEPAGE_TEXT "Welcome to the ${APP_NAME} Setup Wizard.\r\n\r\nClick Next to continue."
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "license.txt"
!insertmacro MUI_PAGE_COMPONENTS  ; For checkboxes (sections)
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

; Finish page with checkboxes
!define MUI_FINISHPAGE_SHOWREADME ""  ; We'll handle manually
!define MUI_FINISHPAGE_RUN ""  ; We'll handle manually
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Name "${APP_NAME} ${APP_VERSION}"
OutFile "setup.exe"
InstallDir "${INSTALL_DIR}"
RequestExecutionLevel admin  ; For Program Files

Section "Main Application" SecMain
  SectionIn RO  ; Required
  SetOutPath "$INSTDIR"
  File "dist\${APP_EXE}"
  File "manual.md"  ; User manual
  ; Create empty db if needed
  FileOpen $0 "$INSTDIR\budget.db" w
  FileClose $0
SectionEnd

Section "Desktop Shortcut" SecDesktop
  CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
SectionEnd

Section "Start Menu Shortcut" SecStartMenu
  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
SectionEnd

Section "Auto Start with Windows" SecAutoStart
  CreateShortcut "$APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
SectionEnd

Section "Install AnyDesk for Remote Support" SecAnyDesk
  ; Download AnyDesk portable (adjust URL if needed; use latest from anydesk.com)
  NSISdl::download "https://download.anydesk.com/AnyDesk.exe" "$TEMP\AnyDesk.exe"
  Pop $0
  StrCmp $0 "success" +2
    MessageBox MB_OK "Failed to download AnyDesk."
  ExecWait '"$TEMP\AnyDesk.exe" --install "$PROGRAMFILES\AnyDesk" --start-service --silent'  ; Silent install
SectionEnd

; Descriptions for components
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} "Create a shortcut on the desktop."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} "Add to Start Menu."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecAutoStart} "Start the app automatically on Windows login."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecAnyDesk} "Install AnyDesk for remote support access."
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; Finish page custom logic (checkboxes)
Function .onInstSuccess
  ; Launch checkbox
  MessageBox MB_YESNO "Launch ${APP_NAME} now?" IDYES launch
  Goto manual
  launch:
    Exec '"$INSTDIR\${APP_EXE}"'
  manual:
  ; Manual checkbox
  MessageBox MB_YESNO "Open user manual now?" IDYES openmanual
  Goto end
  openmanual:
    ExecShell "open" "$INSTDIR\manual.md"
  end:
FunctionEnd

; Uninstaller
Section "Uninstall"
  Delete "$INSTDIR\${APP_EXE}"
  Delete "$INSTDIR\budget.db"
  Delete "$INSTDIR\manual.md"
  RMDir "$INSTDIR"
  Delete "$DESKTOP\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
  RMDir "$SMPROGRAMS\${APP_NAME}"
  Delete "$APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\${APP_NAME}.lnk"
  ; Uninstall AnyDesk if installed (optional; assumes it's installed)
  ExecWait '"$PROGRAMFILES\AnyDesk\AnyDesk.exe" --remove --silent'
  DeleteRegKey HKLM "${UNINSTALL_KEY}"
SectionEnd

; Uninstall info for Control Panel
!define MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO "Uninstall ${APP_NAME}?" IDYES +2
  Abort
FunctionEnd

; Write uninstaller info
Section -Post
  WriteUninstaller "$INSTDIR\uninstall.exe"
  WriteRegStr HKLM "${UNINSTALL_KEY}" "DisplayName" "${APP_NAME}"
  WriteRegStr HKLM "${UNINSTALL_KEY}" "UninstallString" "$INSTDIR\uninstall.exe"
  WriteRegStr HKLM "${UNINSTALL_KEY}" "DisplayVersion" "${APP_VERSION}"
  WriteRegDWORD HKLM "${UNINSTALL_KEY}" "NoModify" 1
  WriteRegDWORD HKLM "${UNINSTALL_KEY}" "NoRepair" 1
SectionEnd