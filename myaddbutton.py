from tkinter import ttk


class MyAddButton(ttk.Button):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def add_window_set_focus(self, event, add_window):
        if event.widget == add_window:
            add_window.focus_set()