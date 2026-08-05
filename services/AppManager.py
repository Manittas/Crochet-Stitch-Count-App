from models.Row import Row

import re

class AppManager:
    def __init__(self, _storageService):
        self.storageService = _storageService
        # flags
        self.inputVisible = False  # toggles the input field to be visible
        self.inputWindow = None    # default store value for canvas window ID
        # objects
        self.currentIndex = 0
        self.rowsList = []
        # load data
        self.load()
    
    ###################################################
    
    def load(self):
        if self.storageService is None:
            return
        data = self.storageService.load_rows()
        if data is None:
            return
        # sets list and finds current active row, saving its list index
        self.rowsList = [Row(**item) for item in data]
        self.currentIndex = next((i for i, row in enumerate(self.rowsList) if row.isCurrent), 0)
    
    def has_rows(self):
        return len(self.rowsList) > 0
        
    def new_row(self, name):
        newRow = Row(_name = name, _isCurrent=True)
        newRow.name = self.get_unique_name(name)
        # If there is already a current row, unset it
        if self.has_rows():
            self.rowsList[self.currentIndex].isCurrent = False
        # append and update
        self.rowsList.append(newRow)
        self.currentIndex = len(self.rowsList) - 1
    
    def get_unique_name(self, name):
        # Remove any existing " (number)" suffix
        base_name = re.sub(r" \(\d+\)$", "", name)
        used_names = {row.name for row in self.rowsList}
        if base_name not in used_names:
            return base_name
        # checks which increment number to add to the name
        i = 2
        while f"{base_name} ({i})" in used_names:
            i += 1
        return f"{base_name} ({i})"
