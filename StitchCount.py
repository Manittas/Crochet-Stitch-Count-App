# Only necessary to delete .spec file before pyinstaller command
# pyinstaller --clean --onefile --noconsole --icon icon.ico your_script.py
# ------------------------------------------------------------------------

# from pathlib import Path
from tkinter import Tk, Canvas, Button, font, Entry, END
from models.Row import Row

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

# Objects and variables
# ---------------------

class AppVariables:
    def __init__(self):
        self.inputVisible = False  # toggles the input field to be visible
        self.inputWindow = None    # default store value for canvas window ID

row = Row()
variables = AppVariables()

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
            case _:
                return

def increment_button_click():
    row.increment()
    update_count()
    
def decrement_button_click():
    # prevent from going to negative values
    if row.count > 0:
        row.decrement()
        update_count()

def input_set_count():
    newCount = inputField.get()
    # verification so it only changes when input is visible and with value
    if variables.inputVisible and not(newCount == ""):
        row.count = int(newCount)
        inputField.delete(0, END)
        update_count()

def reset_count():
    row.count = 0
    update_count()
    
def update_count():
    canvas.itemconfig(rowLabel, text=f"Count: {row.count}")
    
    # toggles/untoggles decrement button depending on count value update
    if row.count == 0:
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

rowLabel = canvas.create_text(150,
                              120,
                              text=f"Count: {row.count}",
                              fill="white",
                              font=("Arial", 16, "bold"))

# buttons & Inputs
# ----------------

btn_font = font.Font(family="Arial", size=10, weight="bold")
validate_cmd = window.register(is_number)

incrementBtn = Button(window, text="Add", font=btn_font, width=4, height=1, command=increment_button_click)
decrementBtn = Button(window, text="Sub", state="disabled", font=btn_font, width=4, height=1, command=decrement_button_click)
manualSetBtn = Button(window, text="Set", font=btn_font, width=4, height=1, command=toggle_input_field)

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

# App bindings and main loop
# --------------------------

window.bind("<KeyPress>", on_key_press)
window.bind("<Return>", lambda e=None: input_set_count())
window.mainloop()