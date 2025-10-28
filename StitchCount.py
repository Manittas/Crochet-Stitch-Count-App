# Only necessary to delete .spec file before pyinstaller command
# pyinstaller --clean --onefile --noconsole --icon icon.ico your_script.py
# ------------------------------------------------------------------------

from pathlib import Path
from tkinter import Tk, Canvas, Button, Entry, messagebox, font, END
from models.Row import Row

import json
import sys

# Window properties
# -----------------

window = Tk()
window.geometry("300x300")
window.resizable(False, False)
window.attributes("-topmost", True)

canvas = Canvas(
    window,
    bg = "#121212",
    width = 300,
    height = 300,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.pack()

# Variables class
# ---------------

class AppVariables:
    def __init__(self):
        # flags
        self.inputVisible = False  # toggles the input field to be visible
        self.inputWindow = None    # default store value for canvas window ID
        # file
        self.saveFile = "crochetdata.json"
        self.savePath = self.get_base_path() / "data"
        # objects
        self.currentIndex = 0
        self.rowsList = self.load_file()
    
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
        newRowsList = list()
        if filePath.exists():
            try:
                # opens file, gets data and converts it to row object
                with open(filePath, "r") as file:
                    data = json.load(file)
                newRowsList = [Row(**item) for item in data]
                # finds current active row, saving its list index
                self.currentIndex = next((i for i, row in enumerate(newRowsList) if row.isCurrent), 0)
                return newRowsList
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=window)
        # Default case for when file doesn't exist or exception happens
        # Create empty list with new row set to be the current
        newRow = Row(_isCurrent=True)
        newRowsList.append(newRow)
        self.currentIndex = 0
        return newRowsList
    
    def save_file(self):
        try:
            # creates the data folder in case it doesn't exist
            self.savePath.mkdir(exist_ok=True)
            filePath = self.savePath / self.saveFile
            with open(filePath, "w") as file:
                data = [row.__dict__ for row in self.rowsList]
                json.dump(data, file, indent=4)
                # show saved label
                canvas.itemconfig(saveLabel, state="normal")
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=window)

# functions
# ----------

def on_key_press(event):
    # keyboard event system for the functionalities, input can't be visible
    if not variables.inputVisible:
        match event.keysym:
            case "q" | "Q":
                decrement_button_click()
            case "e" | "E":
                increment_button_click()
            case "r" | "R":
                reset_count()
            case "n" | "N":
                new_row()
            case "s" | "S":
                variables.save_file()
            case _:
                return

def increment_button_click():
    variables.rowsList[variables.currentIndex].increment()
    update_count()
    
def decrement_button_click():
    # prevent from going to negative values
    if variables.rowsList[variables.currentIndex].count > 0:
        variables.rowsList[variables.currentIndex].decrement()
        update_count()

def input_set_count():
    newCount = inputField.get()
    # verification so it only changes when input is visible and with value
    if variables.inputVisible and not(newCount == ""):
        variables.rowsList[variables.currentIndex].count = int(newCount)
        inputField.delete(0, END)
        update_count()

def reset_count():
    variables.rowsList[variables.currentIndex].count = 0
    update_count()

def new_row():
    newRow = Row(_isCurrent=True)
    variables.rowsList[variables.currentIndex].isCurrent = False
    variables.rowsList.append(newRow)
    variables.currentIndex = next((i for i, row in enumerate(variables.rowsList) if row.isCurrent), 0)
    update_count()
    # make New! tag visible after updating canva
    canvas.itemconfig(newLabel, state="normal")
    
def update_count():
    canvas.itemconfig(rowLabel, text=f"Count: {variables.rowsList[variables.currentIndex].count}")
    # always make New! and Saved! tag invisible at any update
    canvas.itemconfig(newLabel, state="hidden")
    canvas.itemconfig(saveLabel, state="hidden")
    # toggles/untoggles decrement button depending on count value update
    if variables.rowsList[variables.currentIndex].count == 0:
        decrementBtn.config(state="disabled")
    else:
        decrementBtn.config(state="normal")

def toggle_input_field():
    # deletes any value in the field, visibe or not
    inputField.delete(0, END)
    # creates / destroys the input field to be visible
    if variables.inputVisible:
        variables.inputVisible = False
        canvas.delete(variables.inputWindow)
        variables.inputWindow = None
    else:
        variables.inputVisible = True
        variables.inputWindow = canvas.create_window(150, 210, window=inputField)
        
def is_number(char):
    return char.isdigit() or char == ""

# Initialize variables and row
# ----------------------------

variables = AppVariables()

# labels
# ------

canvas.create_text(150,
                   20,
                   text="Stich Counting App",
                   fill="white",
                   font=("Arial", 12))

canvas.create_text(150,
                   50,
                   text="Row",
                   fill="white",
                   font=("Arial", 12, "bold"))

saveLabel = canvas.create_text(150,
                              95,
                              text="Saved!",
                              fill="Green",
                              font=("Arial", 12, "bold", "italic"),
                              state="hidden")

newLabel = canvas.create_text(105,
                              50,
                              text="NEW!",
                              fill="Yellow",
                              font=("Arial", 12, "bold"),
                              state="hidden")

rowLabel = canvas.create_text(150,
                              120,
                              text=f"Count: {variables.rowsList[variables.currentIndex].count}",
                              fill="white",
                              font=("Arial", 16, "bold"))

# buttons & Inputs
# ----------------

btn_font = font.Font(family="Arial", size=10, weight="bold")
initial_decrement_state = "normal" if variables.rowsList[variables.currentIndex].count > 0 else "disabled"
validate_cmd = window.register(is_number)

incrementBtn = Button(window, text="Add", font=btn_font, width=4, height=1, command=increment_button_click)
decrementBtn = Button(window, text="Sub", state=initial_decrement_state, font=btn_font, width=4, height=1, command=decrement_button_click)
manualSetBtn = Button(window, text="Set", font=btn_font, width=4, height=1, command=toggle_input_field)
saveBtn = Button(window, text="Save", font=btn_font, width=4, height=1, command=variables.save_file)
newBtn = Button(window, text="New", font=btn_font, width=4, height=1, command=new_row)

inputField = Entry(window, validate="key", validatecommand=(validate_cmd, "%P"))

canvas.create_window(200,
                     175,
                     window=incrementBtn)
canvas.create_window(150,
                     175,
                     window=manualSetBtn)
canvas.create_window(100,
                     175,
                     window=decrementBtn)
canvas.create_window(30,
                     275,
                     window=saveBtn)
canvas.create_window(270,
                     275,
                     window=newBtn)

# App bindings and main loop
# --------------------------

window.bind("<KeyPress>", on_key_press)
window.bind("<Return>", lambda e=None: input_set_count())
window.mainloop()