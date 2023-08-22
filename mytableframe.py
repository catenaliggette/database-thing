from tkinter import ttk


class MyTableFrame(ttk.Frame):
    def __init__(self, parent, file_column_index, *args, **kwargs):
        self.file_column_index = file_column_index
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
            widgets_in_row = [child for child in self.grid_slaves() if child.grid_info()["row"] == row]
            for i, child in enumerate(widgets_in_row[1:]):  # Exclude the last widget
                child.configure(background='#247F4C', foreground="white")

    def clean_row_selection(self):
        for child in self.grid_slaves():
            if child.grid_info()["row"] != 0:
                if child.grid_info()['column'] not in self.file_column_index:
                    child.configure(bg="white", fg="black")
                else:
                    child.configure(bg="white", fg="blue")
