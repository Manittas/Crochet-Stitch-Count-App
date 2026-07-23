# Only necessary to delete .spec file before pyinstaller command
# pyinstaller --clean --onefile --noconsole --icon icon.ico your_script.py
# ------------------------------------------------------------------------

from tkinter import Tk, Canvas, Button, Entry, font, END
from models.Piece import Piece
from utils.AppVariables import AppVariables

# Window properties
# -----------------

window = Tk()
window.title("Stich Counter")
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
                new_piece()
            case "s" | "S":
                variables.save_file()
            case _:
                return

def increment_button_click():
    variables.piecesList[variables.currentIndex].increment()
    update_count()
    
def decrement_button_click():
    # prevent from going to negative values
    if variables.piecesList[variables.currentIndex].count > 0:
        variables.piecesList[variables.currentIndex].decrement()
        update_count()

def input_set_count():
    newCount = inputField.get()
    # verification so it only changes when input is visible and with value
    if variables.inputVisible and not(newCount == ""):
        variables.piecesList[variables.currentIndex].count = int(newCount)
        inputField.delete(0, END)
        update_count()

def reset_count():
    variables.piecesList[variables.currentIndex].count = 0
    update_count()

def new_piece():
    newPiece = Piece(_isCurrent=True)
    variables.piecesList[variables.currentIndex].isCurrent = False
    variables.piecesList.append(newPiece)
    variables.currentIndex = next((i for i, piece in enumerate(variables.piecesList) if piece.isCurrent), 0)
    update_count()
    # make New! tag visible after updating canva and set new name
    canvas.itemconfig(newLabel, state="normal")
    canvas.itemconfig(pieceName, text=f"{variables.piecesList[variables.currentIndex].name}")
    
def update_count():
    canvas.itemconfig(pieceLabel, text=f"Row Count: {variables.piecesList[variables.currentIndex].count}")
    # always make New! and Saved! tag invisible at any update
    canvas.itemconfig(newLabel, state="hidden")
    canvas.itemconfig(saveLabel, state="hidden")
    # toggles/untoggles decrement button depending on count value update
    if variables.piecesList[variables.currentIndex].count == 0:
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
                   text="Piece",
                   fill="white",
                   font=("Arial", 12, "bold"))

saveLabel = canvas.create_text(150,
                              95,
                              text="Saved!",
                              fill="Green",
                              font=("Arial", 12, "bold", "italic"),
                              state="hidden")

newLabel = canvas.create_text(102,
                              20,
                              text="NEW!",
                              fill="Yellow",
                              font=("Arial", 12, "bold"),
                              state="hidden")

# Initialize variables and piece
# ----------------------------

variables = AppVariables(window, canvas, saveLabel)

# labels dependent on variables
# -----------------------------

pieceName = canvas.create_text(150,
                              45,
                              text=f"{variables.piecesList[variables.currentIndex].name}",
                              fill="white",
                              font=("Arial", 12))

pieceLabel = canvas.create_text(150,
                              120,
                              text=f"Row Count: {variables.piecesList[variables.currentIndex].count}",
                              fill="white",
                              font=("Arial", 16, "bold"))

# buttons & Inputs
# ----------------

btn_font = font.Font(family="Arial", size=10, weight="bold")
initial_decrement_state = "normal" if variables.piecesList[variables.currentIndex].count > 0 else "disabled"
validate_cmd = window.register(is_number)

incrementBtn = Button(window, text="Add", font=btn_font, width=4, height=1, command=increment_button_click)
decrementBtn = Button(window, text="Sub", state=initial_decrement_state, font=btn_font, width=4, height=1, command=decrement_button_click)
manualSetBtn = Button(window, text="Set", font=btn_font, width=4, height=1, command=toggle_input_field)
saveBtn = Button(window, text="Save", font=btn_font, width=4, height=1, command=variables.save_file)
newBtn = Button(window, text="New", font=btn_font, width=4, height=1, command=new_piece)

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