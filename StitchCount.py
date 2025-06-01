# pyinstaller --clean --onefile --noconsole --icon icon.ico your_script.py

# from pathlib import Path
from tkinter import Tk, Canvas, Button, font
from models.Row import Row

window = Tk()

# Set window properties

window.geometry("300x300")
window.resizable(False, False)

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

# row object and related

row = Row()

# functions

def increment_button_click():
    row.increment()
    canvas.itemconfig(rowLabel, text=f"Count: {row.count}")
    toggle_decrement_button()
    
def decrement_button_click():
    # prevent from going to negative values
    if row.count > 0:
        row.decrement()
        canvas.itemconfig(rowLabel, text=f"Count: {row.count}")
        toggle_decrement_button()
    
def toggle_decrement_button():
    if row.count == 0:
        decrementBtn.config(state="disabled")
    else:
        decrementBtn.config(state="normal")

# labels

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

# buttons
btn_font = font.Font(family="Arial", size=10, weight="bold")

incrementBtn = Button(window, text="Add", font=btn_font, width=4, height=1, command=increment_button_click)
decrementBtn = Button(window, text="Sub", state="disabled", font=btn_font, width=4, height=1, command=decrement_button_click)

canvas.create_window(200,
                     175,
                     window=incrementBtn)
canvas.create_window(100,
                     175,
                     window=decrementBtn)

# start app main loop
window.mainloop()