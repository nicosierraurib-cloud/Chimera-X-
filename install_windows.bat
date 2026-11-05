@echo off
cd /d "%~dp0"
if exist "C:\Program Files\ChimeraX 1.12\bin\python.exe" (
    "C:\Program Files\ChimeraX 1.12\bin\python.exe" install.py
) else (
    python install.py
)
pause
