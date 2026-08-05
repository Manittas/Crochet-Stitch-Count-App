from tkinter import messagebox
from utils.Helpers import GetBasePath

import json

class StorageService:
    def __init__(self, _logger, _window):
        # file
        self.saveFile = "crochetdata.json"
        self.savePath = GetBasePath() / "data"
        # logger
        self.logger = _logger
        # window objects
        self.window = _window
    
    ###################################################
    
    def load_rows(self):
        filePath = self.savePath / self.saveFile
        data = None
        if filePath.exists():
            try:
                # opens file, gets data and converts it to row object
                with open(filePath, "r") as file:
                    data = json.load(file)
            except Exception:
                self.logger.log_exception()
                messagebox.showerror("Error", "Error loading data.", parent=self.window)
        # Default case for when file doesn't exist or exception happens
        # Create empty list with new row set to be the current
        return data
    
    def save_rows(self, rowsList):
        try:
            # creates the data folder in case it doesn't exist
            self.savePath.mkdir(exist_ok=True)
            filePath = self.savePath / self.saveFile
            with open(filePath, "w") as file:
                data = [row.__dict__ for row in rowsList]
                json.dump(data, file, indent=4)
            return True
        except Exception:
            self.logger.log_exception()
            messagebox.showerror("Error", "Error saving data.", parent=self.window)
            return False