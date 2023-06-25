import tkinter
from tkinter import ttk


class MyTableFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MyTableFrame, self).__init__(parent, *args, **kwargs)

    def refresh(self):
        pass

    def fill_frame(self, window):
        pass

    def on_click_row_selection(self, event):
        # Get the widget that was clicked
        widget = event.widget
        self.clean_row_selection()
        # Get the row and column of the clicked widget
        row = widget.grid_info()["row"]
        # Highlight all widgets in the clicked row
        if row != 0:
            for child in self.grid_slaves():
                if child.grid_info()["row"] == row:
                    child.configure(background='#247F4C', foreground="white")

    def clean_row_selection(self):
        for child in self.grid_slaves():
            if child.grid_info()["row"] != 0:
                child.configure(bg="white", fg="black")
