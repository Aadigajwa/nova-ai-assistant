@echo off
set "PROJECT_DIR=c:\Users\PATH OF YOUR DIRECTORY"

echo Launching Nova Assistant Pro in PowerShell...

powershell.exe -NoExit -Command "& { cd '%PROJECT_DIR%'; if (Test-Path '.venv') { .\.venv\Scripts\Activate.ps1; python main.py } else { Write-Error 'Virtual environment not found'; pause } }"
