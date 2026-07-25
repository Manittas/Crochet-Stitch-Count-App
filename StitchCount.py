# Only necessary to delete .spec file before pyinstaller command
# pyinstaller --clean --onefile --noconsole --icon icon.ico your_script.py
# ------------------------------------------------------------------------

from tkinter import Tk, Canvas, Button, Entry, Toplevel, font, END
from utils.AppManager import AppManager

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
    if not manager.inputVisible:
        match event.keysym:
            case "q" | "Q":
                decrement_button_click()
            case "e" | "E":
                increment_button_click()
            case "r" | "R":
                reset_count()
            case "n" | "N":
                open_new_piece_popup()
            case "s" | "S":
                manager.save_file()
            case _:
                return

def increment_button_click():
    manager.piecesList[manager.currentIndex].increment()
    update_count()
    
def decrement_button_click():
    # prevent from going to negative values
    if manager.piecesList[manager.currentIndex].count > 0:
        manager.piecesList[manager.currentIndex].decrement()
        update_count()

def input_set_count():
    newCount = inputField.get()
    # verification so it only changes when input is visible and with value
    if manager.inputVisible and not(newCount == ""):
        manager.piecesList[manager.currentIndex].count = int(newCount)
        inputField.delete(0, END)
        update_count()

def reset_count():
    manager.piecesList[manager.currentIndex].count = 0
    update_count()
    
def open_new_piece_popup():
    popup = Toplevel(window)
    popup.title("New Piece Name")
    popup_width = 200
    popup_height = 100
    # get relative positioning of the main window
    window.update_idletasks()
    main_x = window.winfo_x()
    main_y = window.winfo_y()
    main_width = window.winfo_width()
    main_height = window.winfo_height()
    # Center the popup over the main window
    x = main_x + (main_width - popup_width) // 2
    y = main_y + (main_height - popup_height) // 2
    popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
    popup.resizable(False, False)
    # Make it modal
    popup.transient(window)
    popup.grab_set()
    # input
    nameInput = Entry(popup, width=30)
    nameInput.pack()
    # build ok button
    Button(
        popup,
        text="OK",
        command=lambda: new_piece(nameInput, popup)
    ).pack(pady=15)
    # Allow pressing Enter
    nameInput.bind("<Return>", lambda e: new_piece(nameInput, popup))
    # Put the cursor in the input immediately
    nameInput.focus_set()
    # Wait until popup is closed
    window.wait_window(popup)

def new_piece(inputEntry, popup):
    name = inputEntry.get()
    newPiece = manager.newPiece(name = name if name else "piece")
    manager.piecesList[manager.currentIndex].isCurrent = False
    manager.piecesList.append(newPiece)
    manager.currentIndex = next((i for i, piece in enumerate(manager.piecesList) if piece.isCurrent), 0)
    update_count()
    # make New! tag visible after updating canva and set new name
    canvas.itemconfig(newLabel, state="normal")
    canvas.itemconfig(pieceName, text=f"{manager.piecesList[manager.currentIndex].name}")
    # destroy popup and input
    popup.destroy()
    
def update_count():
    canvas.itemconfig(pieceLabel, text=f"Row Count: {manager.piecesList[manager.currentIndex].count}")
    # always make New! and Saved! tag invisible at any update
    canvas.itemconfig(newLabel, state="hidden")
    canvas.itemconfig(saveLabel, state="hidden")
    # toggles/untoggles decrement button depending on count value update
    if manager.piecesList[manager.currentIndex].count == 0:
        decrementBtn.config(state="disabled")
    else:
        decrementBtn.config(state="normal")

def toggle_input_field():
    # deletes any value in the field, visibe or not
    inputField.delete(0, END)
    # creates / destroys the input field to be visible
    if manager.inputVisible:
        manager.inputVisible = False
        canvas.delete(manager.inputWindow)
        manager.inputWindow = None
    else:
        manager.inputVisible = True
        manager.inputWindow = canvas.create_window(150, 210, window=inputField)
        
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

manager = AppManager(window, canvas, saveLabel)

# labels dependent on variables
# -----------------------------

pieceName = canvas.create_text(150,
                              45,
                              text=f"{manager.piecesList[manager.currentIndex].name}",
                              fill="white",
                              font=("Arial", 12))

pieceLabel = canvas.create_text(150,
                              120,
                              text=f"Row Count: {manager.piecesList[manager.currentIndex].count}",
                              fill="white",
                              font=("Arial", 16, "bold"))

# buttons & Inputs
# ----------------

btn_font = font.Font(family="Arial", size=10, weight="bold")
initial_decrement_state = "normal" if manager.piecesList[manager.currentIndex].count > 0 else "disabled"
validate_cmd = window.register(is_number)

incrementBtn = Button(window, text="Add", font=btn_font, width=4, height=1, command=increment_button_click)
decrementBtn = Button(window, text="Sub", state=initial_decrement_state, font=btn_font, width=4, height=1, command=decrement_button_click)
manualSetBtn = Button(window, text="Set", font=btn_font, width=4, height=1, command=toggle_input_field)
saveBtn = Button(window, text="Save", font=btn_font, width=4, height=1, command=manager.save_file)
newBtn = Button(window, text="New", font=btn_font, width=4, height=1, command=open_new_piece_popup)

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