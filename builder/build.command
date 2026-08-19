#!/bin/bash

echo "=========================================="
echo "      Crochet Stitch Count Builder"
echo "=========================================="
echo

cd "$(dirname "$0")/.."

echo "[1/5] Checking Python..."
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
echo "[2/5] Checking PyInstaller..."
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
fi

echo "PyInstaller version:"
python3 -m PyInstaller --version

echo
echo "[3/5] Validating project..."
echo

REQUIRED_FILES=(
    "StitchCount.py"
    "assets/Crochet.icns"
    "models/Row.py"
    "services/AppManager.py"
    "services/LogService.py"
    "services/StorageService.py"
    "ui/CanvasRenderer.py"
    "ui/PopupDialog.py"
    "utils/Helpers.py"
)

for file in "${REQUIRED_FILES[@]}"; do
    echo "Checking $file..."

    if [ ! -f "$file" ]; then
        echo "ERROR: Required file not found: $file"
        echo
        read -p "Press Enter to exit..."
        exit 1
    fi
done

echo
echo "All required files were found."

echo
echo "[4/5] Removing previous build..."
echo

rm -rf build
rm -rf dist
rm -f StitchCount.spec

echo "Previous build removed."

echo
echo "[5/5] Building application..."
echo

python3 -m PyInstaller \
    --clean \
    --onefile \
    --windowed \
    --icon "assets/Crochet.icns" \
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