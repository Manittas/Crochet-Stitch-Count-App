from tkinter import Toplevel, Listbox, Scrollbar, RIGHT, Y, END

class PopupDialog:
    def __init__(self, _window):
        # window objects
        self.window = _window
    
    ###################################################
    
    def new_row_popup(self):
        popup = Toplevel(self.window)
        popup.title("New Row Name")
        popup_width = 200
        popup_height = 100
        self.set_popup_properties(popup, popup_width, popup_height)
        return popup
    
    def choose_row_popup(self, manager, decrementBtn):
        popup = Toplevel(self.window)
        popup.title("Choose Row")
        popup_width = 200
        popup_height = 100
        self.set_popup_properties(popup, popup_width, popup_height)
        # show list of rows
        listbox = Listbox(popup)
        listbox.pack(side="left", fill="both", expand=True)
        # Scrollbar
        scrollbar = Scrollbar(popup, command=listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        listbox.config(yscrollcommand=scrollbar.set)
        # create click event
        for row in manager.rowsList:
            listbox.insert(END, row.name)
        # Handle click
        def select_row(event):
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                manager.set_visible_row(index, decrementBtn)
                popup.destroy()
        # bind selection event
        listbox.bind("<<ListboxSelect>>", select_row)
        # Wait until popup is closed
        self.window.wait_window(popup)
        
    def set_popup_properties(self, popup, width, height):
        # get relative positioning of the main window
        self.window.update_idletasks()
        main_x = self.window.winfo_x()
        main_y = self.window.winfo_y()
        main_width = self.window.winfo_width()
        main_height = self.window.winfo_height()
        # Center the popup over the main window
        x = main_x + (main_width - width) // 2
        y = main_y + (main_height - height) // 2
        popup.geometry(f"{width}x{height}+{x}+{y}")
        popup.resizable(False, False)
        # Make it modal
        popup.transient(self.window)
        popup.grab_set()
        # put it on top always
        popup.attributes("-topmost", True)
        popup.lift()
        popup.focus_force()
        