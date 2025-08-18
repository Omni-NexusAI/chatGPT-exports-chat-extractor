@echo off
setlocal

REM Change to this script's directory so relative paths work anywhere
cd /d "%~dp0"

REM Optional: allow drag-and-drop of chat.html onto this .bat
set "INPUT_FILE=%~1"

REM Prefer Windows Python launcher if available
where py >nul 2>nul
if %ERRORLEVEL%==0 (
    if defined INPUT_FILE (
        py -3 chat_extractor_gui.py "%INPUT_FILE%"
    ) else (
        py -3 chat_extractor_gui.py
    )
) else (
    if defined INPUT_FILE (
        python chat_extractor_gui.py "%INPUT_FILE%"
    ) else (
        python chat_extractor_gui.py
    )
)

echo.
echo If the window closed unexpectedly, ensure Python 3.8+ is installed and on PATH.
pause