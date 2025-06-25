@echo off
echo Initializing Git repository for Python Text Editor...
echo.

REM Check if git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo Git is not installed or not in PATH.
    echo Please use GitHub Desktop to publish this repository.
    pause
    exit /b 1
)

REM Initialize git repository
git init

REM Add all files
git add .

REM Make initial commit
git commit -m "Initial commit: Python text editor with GUI

- Complete text editor with tkinter GUI
- File operations (new, open, save, save as)  
- Edit operations (undo, redo, cut, copy, paste)
- Search functionality with highlighting
- Font customization and word wrap
- Professional project structure with README and license"

echo.
echo Repository initialized successfully!
echo.
echo Next steps:
echo 1. Create a new repository on GitHub.com
echo 2. Copy the repository URL
echo 3. Run: git remote add origin [YOUR_REPO_URL]
echo 4. Run: git branch -M main
echo 5. Run: git push -u origin main
echo.
pause
