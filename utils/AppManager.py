from pathlib import Path
from tkinter import messagebox
from models.Piece import Piece

import json
import sys
import re

class AppManager:
    def __init__(self, _window, _canvas, _saveLabel):
        # flags
        self.inputVisible = False  # toggles the input field to be visible
        self.inputWindow = None    # default store value for canvas window ID
        # file
        self.saveFile = "crochetdata.json"
        self.savePath = self.get_base_path() / "data"
        # objects
        self.currentIndex = 0
        self.piecesList = self.load_file()
        # window objects
        self.window = _window
        self.canvas = _canvas
        self.saveLabel = _saveLabel
        
    def newPiece(self, name = "piece"):
        newPiece = Piece(_name = name, _isCurrent=True)
        newPiece.name = self.get_unique_name(name)
        return newPiece
    
    def get_unique_name(self, name):
        # Remove any existing " (number)" suffix
        base_name = re.sub(r" \(\d+\)$", "", name)
        used_names = {piece.name for piece in self.piecesList}
        if base_name not in used_names:
            return base_name
        # checks which increment number to add to the name
        i = 2
        while f"{base_name} ({i})" in used_names:
            i += 1
        return f"{base_name} ({i})"
    
    def get_base_path(self):
        # Returns the base folder whether running as a script or a PyInstaller EXE.
        if getattr(sys, 'frozen', False):
            # Running as a PyInstaller EXE
            base_path = Path(sys.executable).resolve().parent.parent
        else:
            # Running from source
            base_path = Path(__file__).resolve().parent
        return base_path
    
    def load_file(self):
        filePath = self.savePath / self.saveFile
        newPiecesList = list()
        if filePath.exists():
            try:
                # opens file, gets data and converts it to piece object
                with open(filePath, "r") as file:
                    data = json.load(file)
                newPiecesList = [Piece(**item) for item in data]
                # finds current active piece, saving its list index
                self.currentIndex = next((i for i, piece in enumerate(newPiecesList) if piece.isCurrent), 0)
                return newPiecesList
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self.window)
        # Default case for when file doesn't exist or exception happens
        # Create empty list with new piece set to be the current
        newPiece = Piece(_isCurrent=True)
        newPiecesList.append(newPiece)
        self.currentIndex = 0
        return newPiecesList
    
    def save_file(self):
        try:
            # creates the data folder in case it doesn't exist
            self.savePath.mkdir(exist_ok=True)
            filePath = self.savePath / self.saveFile
            with open(filePath, "w") as file:
                data = [piece.__dict__ for piece in self.piecesList]
                json.dump(data, file, indent=4)
                # show saved label
                self.canvas.itemconfig(self.saveLabel, state="normal")
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.window)