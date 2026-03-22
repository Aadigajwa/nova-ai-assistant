@echo off
set "PROJECT_DIR=c:\Users\aadig\OneDrive\Documents\python\Full Stack Practise\nova_assistant_pro"

echo Launching Nova Assistant Pro in PowerShell...

powershell.exe -NoExit -Command "& { cd '%PROJECT_DIR%'; if (Test-Path '.venv') { .\.venv\Scripts\Activate.ps1; python main.py } else { Write-Error 'Virtual environment not found'; pause } }"
