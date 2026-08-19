@echo off
setlocal

title Stitch Counter Builder

echo ==========================================
echo       Crochet Stitch Count Builder
echo ==========================================
echo.

cd /d "%~dp0\.."

echo [1/5] Checking Python...

where python >nul 2>&1

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python was not found.
    echo.
    echo Please install Python 3.12 or newer from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

python --version

REM Check Python version
for /f "tokens=2" %%V in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%V"

for /f "tokens=1,2 delims=." %%A in ("%PYTHON_VERSION%") do (
    set "PYTHON_MAJOR=%%A"
    set "PYTHON_MINOR=%%B"
)

if %PYTHON_MAJOR% LSS 3 (
    goto PYTHON_TOO_OLD
)

if %PYTHON_MAJOR% EQU 3 if %PYTHON_MINOR% LSS 12 (
    goto PYTHON_TOO_OLD
)

echo Python version is supported.
goto PYTHON_OK

:PYTHON_TOO_OLD
echo.
echo ERROR: Python 3.12 or newer is required.
echo Current version: %PYTHON_VERSION%
echo.
echo Please update Python and try again.
pause
exit /b 1

:PYTHON_OK

echo.
echo [2/5] Checking PyInstaller...

python -m PyInstaller --version >nul 2>&1

if %errorlevel% neq 0 (
    echo PyInstaller was not found.
    echo Installing PyInstaller...
    echo.

    python -m pip install pyinstaller

    if %errorlevel% neq 0 (
        echo.
        echo ERROR: Failed to install PyInstaller.
        echo.
        pause
        exit /b 1
    )
)

python -m PyInstaller --version

echo.
echo [3/5] Validating project...

set "REQUIRED_FILES=StitchCount.py assets\Crochet.ico models\Row.py services\AppManager.py services\LogService.py services\StorageService.py ui\CanvasRenderer.py ui\PopupDialog.py utils\Helpers.py"

for %%F in (%REQUIRED_FILES%) do (
    echo Checking %%F...

    if not exist "%%F" (
        echo ERROR: Required file not found: %%F
        echo.
        pause
        exit /b 1
    )
)

echo.
echo All required files were found.

echo.
echo [4/5] Removing previous build if any exists...

if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "StitchCount.spec" del /q "StitchCount.spec"

echo.
echo [5/5] Building application...
echo.

python -m PyInstaller ^
    --clean ^
    --onefile ^
    --noconsole ^
    --icon "assets\Crochet.ico" ^
    "StitchCount.py"

if %errorlevel% neq 0 (
    echo.
    echo ==========================================
    echo BUILD FAILED
    echo ==========================================
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo BUILD SUCCESSFUL
echo ==========================================
echo.
echo Application created at:
echo dist\StitchCount.exe
echo.

pause