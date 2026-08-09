from tkinter import Frame, Button, Toplevel, Canvas, Scrollbar

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
        # set manager and decrementBtn for the occasion
        self.manager = manager
        self.decrementBtn = decrementBtn
        # set window popup
        popup = Toplevel(self.window)
        popup.title("Choose Row")
        popup_width = 240
        popup_height = 160
        self.set_popup_properties(popup, popup_width, popup_height)
        # render canvas area for items
        canvasPopup, rowsFrame, canvasWindow = self.scrollable_area_rows(popup)
        # Update scrollable area whenever rowsFrame changes, add mouse-wheel scroll
        rowsFrame.bind(
            "<Configure>",
            lambda event: self.update_scroll_region(event, canvasPopup)
        )
        canvasPopup.bind(
            "<Configure>",
            lambda event: self.update_frame_width(event, canvasPopup, canvasWindow)
        )
        # Mouse wheel
        canvasPopup.bind(
            "<MouseWheel>",
            lambda event: self.scroll_rows(event, canvasPopup)
        )
        rowsFrame.bind(
            "<MouseWheel>",
            lambda event: self.scroll_rows(event, canvasPopup)
        )
        # create click event
        for row in manager.rowsList:
            self.render_row_item(popup, canvasPopup, rowsFrame, row)
        # Force Tkinter to process geometry changes
        popup.update_idletasks()
        # Make sure scroll region is calculated
        canvasPopup.configure(scrollregion=canvasPopup.bbox("all"))
        # Wait until popup is closed
        self.window.wait_window(popup)
        
    # Properties methods
    # ------------------
    
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
    
    # Render methods
    # --------------
        
    def scrollable_area_rows(self, popup):
        container = Frame(popup)
        container.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )
        # Canvas
        canvas = Canvas(
            container,
            bg="white",
            highlightthickness=1,
            bd=0
        )
        canvas.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        # Scrollbar
        scrollbar = Scrollbar(
            container,
            orient="vertical",
            command=canvas.yview,
            width=15
        )
        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )
        # Allow canvas to expand
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        canvas.configure(yscrollcommand=scrollbar.set)
        # Frame containing the rows
        rowsFrame = Frame(canvas)
        canvasWindow = canvas.create_window(
            (0, 0),
            window=rowsFrame,
            anchor="nw"
        )
        return canvas, rowsFrame, canvasWindow
        
    def render_row_item(self, popup, canvas, rowsFrame, row):
        rowFrame = Frame(rowsFrame)
        rowFrame.pack(fill="x", padx=10, pady=3)
        # Row name
        rowButton = Button(
            rowFrame,
            text=row.name,
            anchor="w",
            command=lambda r=row: self.select_row(r, popup)
        )
        rowButton.pack(
            side="left",
            fill="x",
            expand=True
        )
        # Delete button
        deleteButton = Button(
            rowFrame,
            text="🗑",
            width=3,
            command=lambda r=row: self.delete_row(r, popup, canvas, rowsFrame)
        )
        deleteButton.pack(side="right")
        # Make mouse wheel work when cursor is over the row
        rowFrame.bind(
            "<MouseWheel>",
            lambda event: self.scroll_rows(event, canvas)
        )
        rowButton.bind(
            "<MouseWheel>",
            lambda event: self.scroll_rows(event, canvas)
        )
        deleteButton.bind(
            "<MouseWheel>",
            lambda event: self.scroll_rows(event, canvas)
        )
        
    # Event methods
    # -------------
    
    def update_scroll_region(self, event, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    def update_frame_width(self, event, canvas, canvasWindow):
        canvas.itemconfig(canvasWindow, width=event.width)
    
    def scroll_rows(self, event, canvas):
        canvas.yview_scroll(int(-event.delta / 120),"units")
        
    def select_row(self, row, popup):
        self.manager.set_visible_row(row.rowId, self.decrementBtn)
        popup.destroy()
            
    def delete_row(self, row, popup, canvas, rowsFrame):
        self.manager.delete_row(row.rowId, self.decrementBtn)
        self.refresh_rows(popup, canvas, rowsFrame)
    
    def refresh_rows(self, popup, canvas, rowsFrame):
        # Remove existing row widgets
        for widget in rowsFrame.winfo_children():
            widget.destroy()
        # Re-render rows
        for row in self.manager.rowsList:
            self.render_row_item(popup, canvas, rowsFrame, row)
        # Recalculate scrolling
        rowsFrame.update_idletasks()
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        # Return to the top of the list
        canvas.yview_moveto(0)
