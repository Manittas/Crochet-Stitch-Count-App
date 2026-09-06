#!/bin/bash

echo "=========================================="
echo "      Crochet Stitch Count Builder"
echo "=========================================="
echo

cd "$(dirname "$0")/.."

echo "[1/7] Checking Python..."
echo

if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 was not found."
    echo
    echo "Please install Python 3.12 or newer from:"
    echo "https://www.python.org/downloads/"
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')

echo "Python version: $PYTHON_VERSION"

PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')

if [ "$PYTHON_MAJOR" -lt 3 ] || \
   { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 12 ]; }; then

    echo
    echo "ERROR: Python 3.12 or newer is required."
    echo "Current version: $PYTHON_VERSION"
    echo
    echo "Please update Python and try again."
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Python version is supported."

echo
echo "[2/7] Checking Vosk..."
echo

if ! python3 -m pip show vosk >/dev/null 2>&1; then
    echo "Vosk was not found."
    echo "Installing Vosk..."
    echo

    python3 -m pip install vosk

    if [ $? -ne 0 ]; then
        echo
        echo "ERROR: Failed to install Vosk."
        echo
        read -p "Press Enter to exit..."
        exit 1
    fi

    echo
    echo "Vosk installed successfully."
fi

echo "Vosk version:"
python3 -m pip show vosk

echo
echo "[3/7] Checking sounddevice..."
echo

if ! python3 -m pip show sounddevice >/dev/null 2>&1; then
    echo "sounddevice was not found."
    echo "Installing sounddevice..."
    echo

    python3 -m pip install sounddevice

    if [ $? -ne 0 ]; then
        echo
        echo "ERROR: Failed to install sounddevice."
        echo
        read -p "Press Enter to exit..."
        exit 1
    fi

    echo
    echo "sounddevice installed successfully."
fi

echo "sounddevice version:"
python3 -m pip show sounddevice

echo
echo "[4/7] Checking PyInstaller..."
echo

if ! python3 -m PyInstaller --version &> /dev/null; then
    echo "PyInstaller was not found."
    echo "Installing PyInstaller..."
    echo

    python3 -m pip install pyinstaller

    if [ $? -ne 0 ]; then
        echo
        echo "ERROR: Failed to install PyInstaller."
        read -p "Press Enter to exit..."
        exit 1
    fi

    echo
    echo "PyInstaller installed successfully."
fi

echo "PyInstaller version:"
python3 -m PyInstaller --version

echo
echo "[5/7] Validating project..."
echo

REQUIRED_FILES=(
    "StitchCount.py"
    "assets/Crochet.icns"
    "models/Row.py"
    "services/AppManager.py"
    "services/LogService.py"
    "services/StorageService.py"
    "services/SpeechService.py"
    "ui/CanvasRenderer.py"
    "ui/PopupDialog.py"
    "utils/Helpers.py
    speech\vosk-model-small-en-us-0.15"
)

for file in "${REQUIRED_FILES[@]}"; do
    echo "Checking $file..."

    if [ ! -f "$file" ]; then
        echo "ERROR: Required file or folder not found: $file"
        echo
        read -p "Press Enter to exit..."
        exit 1
    fi
done

echo
echo "All required files were found."

echo
echo "[6/7] Removing previous build..."
echo

rm -rf build
rm -rf dist
rm -f StitchCount.spec

echo "Previous build removed."

echo
echo "[7/7] Building application..."
echo

python3 -m PyInstaller \
    --clean \
    --onefile \
    --windowed \
    --icon "assets/Crochet.icns" \
    --add-data "speech/vosk-model-small-en-us-0.15:speech/vosk-model-small-en-us-0.15" \
    "StitchCount.py"

if [ $? -ne 0 ]; then
    echo
    echo "=========================================="
    echo "BUILD FAILED"
    echo "=========================================="
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

echo
echo "=========================================="
echo "BUILD SUCCESSFUL"
echo "=========================================="
echo
echo "Application created at:"
echo "dist/StitchCount"
echo

read -p "Press Enter to exit..."