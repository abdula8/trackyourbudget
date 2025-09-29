# 🔧 NSIS Troubleshooting Guide

> **Complete guide for fixing NSIS installation and build issues**

## 🚨 **Common NSIS Issues**

### **Issue 1: "NSIS not found" Error**

#### **Symptoms**
```
NSIS not found in common locations. Trying to find it...
NSIS not available, skipping installer creation
```

#### **Solutions**

##### **Solution 1: Check NSIS Installation**
```bash
# Check if NSIS is installed
where makensis

# If not found, check common locations:
dir "C:\Program Files (x86)\NSIS\makensis.exe"
dir "C:\Program Files\NSIS\makensis.exe"
dir "C:\NSIS\makensis.exe"
```

##### **Solution 2: Add NSIS to PATH**
1. **Find NSIS installation directory**
2. **Add to PATH environment variable**:
   - Open System Properties → Advanced → Environment Variables
   - Add NSIS directory to PATH
   - Example: `C:\Program Files (x86)\NSIS\`

##### **Solution 3: Use Full Path**
```bash
# Use full path to makensis
"C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi
```

##### **Solution 4: Reinstall NSIS**
1. **Download NSIS**: https://nsis.sourceforge.io/
2. **Install to default location**: `C:\Program Files (x86)\NSIS\`
3. **Add to PATH** during installation
4. **Restart command prompt**

### **Issue 2: "makensis: command not found"**

#### **Symptoms**
```
'makensis' is not recognized as an internal or external command
```

#### **Solutions**

##### **Solution 1: Use build_installer.bat**
```bash
# Use the standalone installer script
build_installer.bat
```

##### **Solution 2: Run from NSIS Directory**
```bash
# Navigate to NSIS directory
cd "C:\Program Files (x86)\NSIS\"

# Run makensis with full path to script
makensis.exe "D:\scripts\temp\temp\installer.nsi"
```

##### **Solution 3: Fix PATH Environment**
```bash
# Check current PATH
echo %PATH%

# Add NSIS to PATH temporarily
set PATH=%PATH%;C:\Program Files (x86)\NSIS\

# Test makensis
makensis /VERSION
```

### **Issue 3: "Installer.nsi not found"**

#### **Symptoms**
```
ERROR: installer.nsi not found!
```

#### **Solutions**

##### **Solution 1: Check Working Directory**
```bash
# Make sure you're in the project directory
cd D:\scripts\temp\temp

# Verify installer.nsi exists
dir installer.nsi
```

##### **Solution 2: Use Full Path to Script**
```bash
# Use full path to installer.nsi
makensis "D:\scripts\temp\temp\installer.nsi"
```

### **Issue 4: "Permission Denied" Error**

#### **Symptoms**
```
Access is denied
Permission denied
```

#### **Solutions**

##### **Solution 1: Run as Administrator**
```bash
# Right-click Command Prompt → Run as Administrator
# Then run build script
build.bat
```

##### **Solution 2: Check File Permissions**
```bash
# Check if installer.nsi is writable
attrib installer.nsi

# Make sure you have write permissions
```

### **Issue 5: "AnyDesk.exe not found"**

#### **Symptoms**
```
WARNING: AnyDesk.exe not found, AnyDesk installation will be skipped
```

#### **Solutions**

##### **Solution 1: Add AnyDesk.exe**
```bash
# Copy AnyDesk.exe to project directory
copy "C:\Path\To\AnyDesk.exe" "D:\scripts\temp\temp\"
```

##### **Solution 2: Modify Installer Script**
```nsi
; Comment out AnyDesk section in installer.nsi
; Section "Install AnyDesk" SecAnyDesk
;   SetOutPath "$INSTDIR\AnyDesk"
;   File "AnyDesk.exe"
; SectionEnd
```

## 🛠️ **Manual NSIS Build Process**

### **Step 1: Prepare Files**
```bash
# Ensure all required files exist
dir BudgetCalculator.exe
dir app.ico
dir app.png
dir LICENSE.txt
dir README.txt
dir installer.nsi
```

### **Step 2: Run NSIS Manually**
```bash
# Method 1: From project directory
makensis installer.nsi

# Method 2: With full path
"C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi

# Method 3: From NSIS directory
cd "C:\Program Files (x86)\NSIS\"
makensis.exe "D:\scripts\temp\temp\installer.nsi"
```

### **Step 3: Verify Output**
```bash
# Check if installer was created
dir BudgetCalculatorSetup.exe

# Test the installer
BudgetCalculatorSetup.exe
```

## 🔍 **Debugging NSIS Issues**

### **Enable Verbose Output**
```bash
# Run NSIS with verbose output
makensis /V4 installer.nsi

# This will show detailed information about the build process
```

### **Check NSIS Version**
```bash
# Check NSIS version
makensis /VERSION

# Should output something like: MakeNSIS v3.08
```

### **Test NSIS Installation**
```bash
# Create a simple test script
echo 'OutFile "test.exe"' > test.nsi
echo 'Section "Test"' >> test.nsi
echo '  DetailPrint "NSIS is working"' >> test.nsi
echo 'SectionEnd' >> test.nsi

# Test it
makensis test.nsi

# Clean up
del test.nsi
del test.exe
```

## 📋 **Complete NSIS Setup Checklist**

### **Installation Checklist**
- [ ] NSIS downloaded from official website
- [ ] NSIS installed to default location
- [ ] NSIS added to PATH environment variable
- [ ] Command prompt restarted after PATH change
- [ ] `makensis /VERSION` works from any directory

### **Build Checklist**
- [ ] All required files present in project directory
- [ ] installer.nsi script is valid
- [ ] Working directory is correct
- [ ] Sufficient disk space for build
- [ ] No file permission issues

### **Verification Checklist**
- [ ] `makensis installer.nsi` runs without errors
- [ ] BudgetCalculatorSetup.exe is created
- [ ] Installer size is reasonable (> 10MB)
- [ ] Installer runs and installs correctly
- [ ] Uninstaller works properly

## 🚀 **Alternative Solutions**

### **Solution 1: Use Portable NSIS**
```bash
# Download portable NSIS
# Extract to project directory
# Use local makensis.exe
.\nsis\makensis.exe installer.nsi
```

### **Solution 2: Use Different Installer**
```bash
# Use Inno Setup instead
# Download from: https://jrsoftware.org/isinfo.php
# Create .iss script instead of .nsi
```

### **Solution 3: Skip Installer Creation**
```bash
# Just create the executable
python build.py

# Distribute the portable version
# Located in: dist/BudgetCalculator_Portable/
```

## 📞 **Getting Help**

### **Common Error Messages and Solutions**

#### **"The system cannot find the file specified"**
- **Cause**: NSIS not in PATH or not installed
- **Solution**: Add NSIS to PATH or use full path

#### **"Access is denied"**
- **Cause**: Permission issues
- **Solution**: Run as Administrator

#### **"The filename, directory name, or volume label syntax is incorrect"**
- **Cause**: Invalid path or filename
- **Solution**: Check file paths and names

#### **"NSIS Error: Invalid command"**
- **Cause**: Invalid installer.nsi script
- **Solution**: Check script syntax

### **Useful Commands**
```bash
# Check NSIS installation
where makensis
makensis /VERSION

# Check file permissions
attrib installer.nsi

# Check disk space
dir

# Test NSIS with simple script
echo 'OutFile "test.exe"' > test.nsi && makensis test.nsi && del test.nsi test.exe
```

---

## 🎯 **Quick Fix Summary**

### **Most Common Solution**
1. **Download NSIS** from https://nsis.sourceforge.io/
2. **Install to default location** (C:\Program Files (x86)\NSIS\)
3. **Add to PATH** during installation
4. **Restart command prompt**
5. **Run build script again**

### **If Still Not Working**
1. **Use build_installer.bat** - Standalone script
2. **Run NSIS manually** - `makensis installer.nsi`
3. **Check file paths** - Ensure all files exist
4. **Run as Administrator** - Fix permission issues

---

<div align="center">
  <strong>🔧 NSIS Issues Solved! 🔧</strong>
</div>
