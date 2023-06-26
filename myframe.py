from tkinter import ttk


class MyFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def refresh(self):
        pass

    def fill_frame(self, window):
        pass