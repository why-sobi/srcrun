@echo off
setlocal enabledelayedexpansion

:: 1. Dynamically get the directory containing this batch file (with trailing backslash)
set "SCRIPTS_DIR=%~dp0"

:: 2. Target the local .venv relative to this file
set "VENV_DIR=%SCRIPTS_DIR%.venv"
set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"

:: 3. Ensure virtual environment exists
if not exist "%VENV_PYTHON%" (
    echo [.venv not found in %SCRIPTS_DIR%. Creating virtual environment...]
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo [Error: Failed to create virtual environment.]
        exit /b 1
    )
    echo [.venv created successfully.]
)

:: 4. Handle arguments
set SCRIPT_NAME=%1

if "%SCRIPT_NAME%"=="" (
    echo Usage: srcrun ^<script_name^> [args...]
    exit /b 1
)

:: Capture all arguments and strip the script name
set "ARGS=%*"
call set "ARGS=%%ARGS:*%1=%%"

:: 5. Run the Python script using the dynamic path and isolated venv executable
"%VENV_PYTHON%" "%SCRIPTS_DIR%%SCRIPT_NAME%.py" %ARGS%