from tkinter import Canvas

class CanvasRenderer:
    def __init__(self, _window):
        # window objects
        self.window = _window
        self.create_canvas()
    
    ###################################################
    
    def create_canvas(self):
        self.canvas = Canvas(
            self.window,
            bg = "#121212",
            width = 300,
            height = 300,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.pack()
    
    # -------------------------------------------------
    
    def first_render_labels(self):
        self.canvas.create_text(150,
                           20,
                           text="Row",
                           fill="white",
                           font=("Arial", 12, "bold"))
        saveLabel = self.canvas.create_text(150,
                                      95,
                                      text="Saved!",
                                      fill="Green",
                                      font=("Arial", 12, "bold", "italic"),
                                      state="hidden")
        newLabel = self.canvas.create_text(102,
                                      20,
                                      text="NEW!",
                                      fill="Yellow",
                                      font=("Arial", 12, "bold"),
                                      state="hidden")
        rowName = self.canvas.create_text(150,
                                      45,
                                      text="",
                                      fill="white",
                                      font=("Arial", 12))
        rowLabel = self.canvas.create_text(150,
                                      120,
                                      text="",
                                      fill="white",
                                      font=("Arial", 16, "bold"))
        return saveLabel, newLabel, rowName, rowLabel
    
    # -------------------------------------------------
    
    def first_render_buttons(self, incrementBtn, manualSetBtn, decrementBtn, saveBtn, newBtn, menuBtn):
        self.canvas.create_window(200,
                             175,
                             window=incrementBtn)
        self.canvas.create_window(150,
                             175,
                             window=manualSetBtn)
        self.canvas.create_window(100,
                             175,
                             window=decrementBtn)
        self.canvas.create_window(30,
                             275,
                             window=saveBtn)
        self.canvas.create_window(270,
                             275,
                             window=newBtn)
        self.canvas.create_window(275,
                             25,
                             window=menuBtn)
        
    # -------------------------------------------------
    
    def create_input_window(self, inputWindow):
        createdWindow = self.canvas.create_window(150, 210, window=inputWindow)
        return createdWindow
    
    # -------------------------------------------------
    
    def delete_input_window(self, inputWindow):
        self.canvas.delete(inputWindow)
        
    # -------------------------------------------------
    
    def set_label_state_normal(self, label):
        self.canvas.itemconfig(label, state="normal")
    
    # -------------------------------------------------
    
    def set_label_state_hidden(self, label):
        self.canvas.itemconfig(label, state="hidden")
    
    # -------------------------------------------------
    
    def set_label_text(self, label, text):
        self.canvas.itemconfig(label, text=text)
    
    # -------------------------------------------------
    
    def update_row_name(self, manager, rowName):
        if not manager.has_rows():
            return
        row = manager.rowsList[manager.currentIndex]
        self.set_label_text(label=rowName, text=row.name)