from models.Row import Row

import re

class AppManager:
    def __init__(self, _storageService, _renderer, _speechService):
        self.storageService = _storageService
        self.renderer = _renderer
        self.speechService = _speechService
        # flags
        self.inputVisible = False  # toggles the input field to be visible
        self.micOn = False
        # default store value for canvas window ID
        self.inputWindow = None
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
    
    def get_index_by_id(self, rowId):
        return next(i for i, row in enumerate(self.rowsList) if row.rowId == rowId)
    
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
    
    def update_row_renderers(self, index, decrementBtn):
        self.renderer.update_row_name(manager=self)
        count = self.rowsList[self.currentIndex].count
        self.renderer.set_count_label_text(f"Stitch Count: {count}")
        self.renderer.hide_poping_labels()
        # toggles/untoggles decrement button depending on count value update
        if decrementBtn is not None:
            decrementBtn.config(state="normal" if self.rowsList[index].count > 0 else "disabled")
        
    def set_visible_row(self, rowId, decrementBtn):
        index = self.get_index_by_id(rowId)
        self.rowsList[self.currentIndex].isCurrent = False
        self.rowsList[index].isCurrent = True
        self.currentIndex = index
        self.update_row_renderers(self.currentIndex, decrementBtn)
            
    def new_row(self, name):
        newRow = Row(_name = name, _isCurrent=True)
        newRow.name = self.get_unique_name(name)
        # If there is already a current row, unset it
        if self.has_rows():
            self.rowsList[self.currentIndex].isCurrent = False
        # append and update
        self.rowsList.append(newRow)
        self.currentIndex = len(self.rowsList) - 1
            
    def delete_row(self, rowId, decrementBtn):
        # Prevent deleting the last row
        if len(self.rowsList) <= 1:
            return True
        index = self.get_index_by_id(rowId)
        was_current = index == self.currentIndex
        del self.rowsList[index]
        # If only one row remains, make it current
        if len(self.rowsList) == 1:
            self.currentIndex = 0
            self.rowsList[0].isCurrent = True
            self.update_row_renderers(self.currentIndex, decrementBtn)
            return True
        # Deleted a row before the current row
        if index < self.currentIndex:
            self.currentIndex -= 1
        # Deleted the current row
        elif was_current:
            self.currentIndex = min(self.currentIndex, len(self.rowsList) - 1)
            self.rowsList[self.currentIndex].isCurrent = True
            self.update_row_renderers(self.currentIndex, decrementBtn)
        return False
 
    def toggle_microphone(self, voiceBtn, update_count):
        self.micOn = not self.micOn
        if self.micOn:
            self.renderer.renderVoiceButton(voiceBtn, "red")
            self.speechService.start(lambda number: self.handle_voice_input(number, update_count))
        else:
            self.renderer.renderVoiceButton(voiceBtn, "black")
            self.speechService.stop()

    def handle_voice_input(self, number, update_count):
        # verification so it only changes if recognizable value
        if number >= 0:
            self.rowsList[self.currentIndex].count = int(number)
            update_count()