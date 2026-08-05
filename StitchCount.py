# Only necessary to delete .spec file before pyinstaller command
# pyinstaller --clean --onefile --noconsole --icon icon.ico your_script.py
# ------------------------------------------------------------------------

from tkinter import Tk, Canvas, Button, Entry, Toplevel, font, END
from services.AppManager import AppManager
from services.LogService import LogService
from services.StorageService import StorageService

import sys

# exception handling
# ------------------

def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
    logger.log_exception(exc_info=(exc_type, exc_value, exc_traceback))

logger = LogService()
sys.excepthook = handle_unhandled_exception

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

# functionality methods
# ---------------------

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
                open_new_row_popup()
            case "s" | "S":
                save()
            case _:
                return

def increment_button_click():
    manager.rowsList[manager.currentIndex].increment()
    update_count()
    
def decrement_button_click():
    # prevent from going to negative values
    if manager.rowsList[manager.currentIndex].count > 0:
        manager.rowsList[manager.currentIndex].decrement()
        update_count()

def input_set_count():
    newCount = inputField.get()
    # verification so it only changes when input is visible and with value
    if manager.inputVisible and not(newCount == ""):
        manager.rowsList[manager.currentIndex].count = int(newCount)
        inputField.delete(0, END)
        update_count()

def reset_count():
    manager.rowsList[manager.currentIndex].count = 0
    update_count()

def new_row(inputEntry, popup):
    name = inputEntry.get()
    manager.new_row(name = name if name else "row")
    # update visible objects
    update_row_name()
    update_count()
    # make New! tag visible after updating canva and set new name
    canvas.itemconfig(newLabel, state="normal")
    # destroy popup and input
    popup.grab_release()
    popup.destroy()
    
def update_count():
    if not manager.has_rows():
        return
    row = manager.rowsList[manager.currentIndex]
    canvas.itemconfig(rowLabel, text=f"Stitch Count: {row.count}")
    # always make New! and Saved! tag invisible at any update
    canvas.itemconfig(newLabel, state="hidden")
    canvas.itemconfig(saveLabel, state="hidden")
    # toggles/untoggles decrement button depending on count value update
    if decrementBtn is not None:
        decrementBtn.config(state="normal" if row.count > 0 else "disabled")

def update_row_name():
    if not manager.has_rows():
        return
    row = manager.rowsList[manager.currentIndex]
    canvas.itemconfig(rowName, text=row.name)

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

def save():
    statusOK = storageService.save_rows(manager.rowsList)
    if statusOK:
        # show saved label
        canvas.itemconfig(saveLabel, state="normal")

# Popup methods
# -------------

def open_new_row_popup(is_startup = False):
    popup = Toplevel(window)
    popup.title("New Row Name")
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
    # put it on top always
    popup.attributes("-topmost", True)
    popup.lift()
    popup.focus_force()
    # input
    nameInput = Entry(popup, width=30)
    nameInput.pack()
    # build ok button
    Button(
        popup,
        text="OK",
        command=lambda: new_row(nameInput, popup)
    ).pack(pady=15)
    # Allow pressing Enter
    nameInput.bind("<Return>", lambda e: new_row(nameInput, popup))
    # Put the cursor in the input immediately
    nameInput.focus_set()
    # Wait until popup is closed
    window.wait_window(popup)
    # Popup closed and no row added on open if no save file closes app
    if is_startup and not manager.has_rows():
        window.destroy()

# labels
# ------

canvas.create_text(150,
                   20,
                   text="Row",
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

# labels dependent on variables
# -----------------------------

rowName = canvas.create_text(150,
                              45,
                              text="",
                              fill="white",
                              font=("Arial", 12))

rowLabel = canvas.create_text(150,
                              120,
                              text="",
                              fill="white",
                              font=("Arial", 16, "bold"))

btn_font = None
initial_decrement_state = None
validate_cmd = None
incrementBtn = None
decrementBtn = None
manualSetBtn = None
saveBtn = None
newBtn = None
inputField = None

# Initialize variables and services
# ---------------------------------

storageService = StorageService(logger, window)
manager = AppManager(storageService)

if not manager.has_rows():
    # to run after mainloop of the window is created, prevents first popup not closing
    window.after(0, lambda: open_new_row_popup(True))
else:
    update_row_name()
    update_count()

# buttons & Inputs
# ----------------

btn_font = font.Font(family="Arial", size=10, weight="bold")
if manager.has_rows():
    initial_decrement_state = ("normal" if manager.rowsList[manager.currentIndex].count > 0 else "disabled")
else:
    initial_decrement_state = "disabled"
validate_cmd = window.register(is_number)

incrementBtn = Button(window, text="Add", font=btn_font, width=4, height=1, command=increment_button_click)
decrementBtn = Button(window, text="Sub", state=initial_decrement_state, font=btn_font, width=4, height=1, command=decrement_button_click)
manualSetBtn = Button(window, text="Set", font=btn_font, width=4, height=1, command=toggle_input_field)
saveBtn = Button(window, text="Save", font=btn_font, width=4, height=1, command=save)
newBtn = Button(window, text="New", font=btn_font, width=4, height=1, command=open_new_row_popup)

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
