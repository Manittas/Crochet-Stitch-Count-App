from tkinter import Toplevel

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
    
    def choose_row_popup(self, manager):
        popup = Toplevel(self.window)
        popup.title(f"Choose Row: {len(manager.rowsList)}")
        popup_width = 200
        popup_height = 100
        self.set_popup_properties(popup, popup_width, popup_height)
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