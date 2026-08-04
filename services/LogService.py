from pathlib import Path
from datetime import datetime

import sys
import traceback

class LogService:
    def __init__(self):
        self.logPath = self.get_base_path() / "logs"
    
    ###################################################
    
    def get_base_path(self):
        # Returns the base folder whether running as a script or a PyInstaller EXE.
        if getattr(sys, 'frozen', False):
            # Running as a PyInstaller EXE
            base_path = Path(sys.executable).resolve().parent.parent
        else:
            # Running from source
            base_path = Path(__file__).resolve().parent
        return base_path
    
    def log_exception(self, exc_info=None):
        # Create logs folder if it doesn't exist
        self.logPath.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = self.logPath / f"error_log_{timestamp}.txt"
        # handled vs unhandled error
        if exc_info is None:
            log = traceback.format_exc()
        else:
            log = "".join(traceback.format_exception(*exc_info))
        # Save the full traceback
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(log)
        return file_path
