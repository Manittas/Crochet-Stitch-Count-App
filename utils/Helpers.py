from pathlib import Path

import sys

def GetBasePath():
    # Returns the base folder whether running as a script or a PyInstaller EXE.
    if getattr(sys, 'frozen', False):
        # Running as a PyInstaller EXE
        base_path = Path(sys.executable).resolve().parent.parent
    else:
        # Running from source
        base_path = Path(__file__).resolve().parent
    return base_path

def IsNumber(char):
    return char.isdigit() or char == ""