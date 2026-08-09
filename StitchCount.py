# Only necessary to delete .spec file before pyinstaller command
# windows: pyinstaller --clean --onefile --noconsole --icon assets/icon.ico your_script.py
# macOS: pyinstaller --clean --onefile --windowed --icon assets/icon.icns your_script.py
# necessary to install python ang pyinstaller: pip install pyinstaller
# -------------------------------------------------------------------------------

from tkinter import Tk, Button, Entry, font, END
from services.AppManager import AppManager
from services.LogService import LogService
from services.StorageService import StorageService
from ui.CanvasRenderer import CanvasRenderer
from ui.PopupDialog import PopupDialog
from utils.Helpers import IsNumber

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

renderer = CanvasRenderer(window)

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
            case "m" | "M":
                popupService.choose_row_popup(manager, decrementBtn)
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
    renderer.update_row_name(manager)
    update_count()
    # make New! tag visible after updating canva and set new name
    renderer.set_label_state_normal(newLabel)
    # destroy popup and input
    popup.grab_release()
    popup.destroy()
    
def update_count():
    if not manager.has_rows():
        return
    row = manager.rowsList[manager.currentIndex]
    renderer.set_count_label_text(f"Stitch Count: {row.count}")
    # always make New! and Saved! tag invisible at any update
    renderer.hide_poping_labels()
    # toggles/untoggles decrement button depending on count value update
    if decrementBtn is not None:
        decrementBtn.config(state="normal" if row.count > 0 else "disabled")

def toggle_input_field():
    # deletes any value in the field, visibe or not
    inputField.delete(0, END)
    # creates / destroys the input field to be visible
    if manager.inputVisible:
        manager.inputVisible = False
        renderer.delete_input_window(manager.inputWindow)
        manager.inputWindow = None
    else:
        manager.inputVisible = True
        manager.inputWindow = renderer.create_input_window(inputField)

def save():
    statusOK = storageService.save_rows(manager.rowsList)
    if statusOK:
        # show saved label
        renderer.set_label_state_normal(saveLabel)

# Popup methods
# -------------

def open_new_row_popup(is_startup = False):
    popup = popupService.new_row_popup()
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
        
# Render labels
# -------------

saveLabel, newLabel = renderer.first_render_labels()
        
# Declare window related objects
# ------------------------------

btn_font = None
initial_decrement_state = None
validate_cmd = None
incrementBtn = None
decrementBtn = None
manualSetBtn = None
saveBtn = None
newBtn = None
menuBtn = None
inputField = None

# Initialize variables and services
# ---------------------------------

storageService = StorageService(logger, window)
manager = AppManager(storageService, renderer)
popupService = PopupDialog(window)

if not manager.has_rows():
    # to run after mainloop of the window is created, prevents first popup not closing
    window.after(0, lambda: open_new_row_popup(True))
else:
    renderer.update_row_name(manager)
    update_count()

# buttons & Inputs
# ----------------

btn_font = font.Font(family="Arial", size=10, weight="bold")
if manager.has_rows():
    initial_decrement_state = ("normal" if manager.rowsList[manager.currentIndex].count > 0 else "disabled")
else:
    initial_decrement_state = "disabled"
validate_cmd = window.register(IsNumber)

incrementBtn = Button(window, text="Add", font=btn_font, width=4, height=1, command=increment_button_click)
decrementBtn = Button(window, text="Sub", state=initial_decrement_state, font=btn_font, width=4, height=1, command=decrement_button_click)
manualSetBtn = Button(window, text="Set", font=btn_font, width=4, height=1, command=toggle_input_field)
saveBtn = Button(window, text="Save", font=btn_font, width=4, height=1, command=save)
newBtn = Button(window, text="New", font=btn_font, width=4, height=1, command=open_new_row_popup)
menuBtn = Button(window, text="☰", font=btn_font, command=lambda: popupService.choose_row_popup(manager, decrementBtn))

inputField = Entry(window, validate="key", validatecommand=(validate_cmd, "%P"))

renderer.first_render_buttons(incrementBtn, manualSetBtn, decrementBtn, saveBtn, newBtn, menuBtn)

# App bindings and main loop
# --------------------------

window.bind("<KeyPress>", on_key_press)
window.bind("<Return>", lambda e=None: input_set_count())
window.mainloop()
