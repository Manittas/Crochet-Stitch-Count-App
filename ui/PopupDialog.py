from tkinter import Toplevel

class PopupDialog:
    def __init__(self, _window):
        # window objects
        self.window = _window
    
    ###################################################
    
    def open_choose_row_popup(self, manager):
        popup = Toplevel(self.window)
        popup.title(f"Choose Row: {len(manager.rowsList)}")
        popup_width = 200
        popup_height = 100
        # get relative positioning of the main window
        self.window.update_idletasks()
        main_x = self.window.winfo_x()
        main_y = self.window.winfo_y()
        main_width = self.window.winfo_width()
        main_height = self.window.winfo_height()
        # Center the popup over the main window
        x = main_x + (main_width - popup_width) // 2
        y = main_y + (main_height - popup_height) // 2
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        popup.resizable(False, False)
        # Make it modal
        popup.transient(self.window)
        popup.grab_set()
        # put it on top always
        popup.attributes("-topmost", True)
        popup.lift()
        popup.focus_force()
        # Wait until popup is closed
        self.window.wait_window(popup)