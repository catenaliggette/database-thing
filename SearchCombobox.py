from tkinter import ttk
import tkinter as tk
from myscrollableframe import *
import re
from smh import *
from Helper_entry import *


class SearchCombobox(ttk.Entry):
    def __init__(self, parent, values, helper_text="", helper_text_color='#c6c6c6', *args, **kwargs):
        self.textvariable = tk.StringVar(value="")
        vcmd = (parent.register(self.select_search_values), '%P', '%S')
        super().__init__(parent, textvariable=self.textvariable, validate='key',
                         validatecommand=vcmd, *args, **kwargs)
        self.values = values
        self.search_values = values
        self.parent = parent

        self.helper_text = helper_text
        self.helper_text_color = helper_text_color
        self.current_color = helper_text_color
        self.default_color = self.cget('foreground')

        self.dropdown_window = tkinter.Toplevel(self.winfo_toplevel())
        self.dropdown_window.overrideredirect(True)

        self.scroll_frame = ScrollableFrame(self.dropdown_window, labelwidget=ttk.Frame(self.dropdown_window))
        self.scroll_frame.pack(fill='both', expand=True, side='left')
        self.scroll_frame.canvas_frame.columnconfigure(0, weight=1)

        self.dropdown_window.withdraw()

        self.bind("<FocusIn>", self.open_dropdown_window)
        self.bind("<FocusOut>", lambda event: self.close_dropdown_window())

        self.put_helper_text()

    def put_helper_text(self):
        self.textvariable.set(self.helper_text)
        self.configure(foreground=self.helper_text_color)
        self.current_color = self.helper_text_color

    def open_dropdown_window(self, event):
        x = event.widget.winfo_rootx()
        y = event.widget.winfo_rooty()

        if self.current_color == self.helper_text_color:
            self.textvariable.set("")
            self.current_color = self.default_color
            self.configure(foreground=self.default_color)

        self.select_search_values(self.textvariable.get(), None)

        self.dropdown_window.geometry(f"{self.winfo_width()}x{120}+{x}+{y + 35}")
        self.dropdown_window.deiconify()

    def close_dropdown_window(self):
        if not self.get():
            self.put_helper_text()
        self.dropdown_window.withdraw()

    def fill_values_frame(self):
        for widget in self.scroll_frame.canvas_frame.winfo_children():
            widget.destroy()

        for i, value in enumerate(self.search_values):
            label = ttk.Label(self.scroll_frame.canvas_frame, text=value)
            label.bind("<Button-1>", self.select_value)
            label.grid(column=0, row=i, sticky='ew')

        self.scroll_frame.event_canvas_configure()

    def select_value(self, event):
        self.textvariable.set(event.widget.cget("text"))
        self.configure(foreground=self.default_color)
        self.current_color = self.default_color
        self.parent.focus_set()

    def select_search_values(self, search_entry, S):
        self.search_values = []
        for value in self.values:
            if str(search_entry).lower() in str(value).lower():
                self.search_values.append(value)

        self.fill_values_frame()
        return True

    def values_update(self, new_values):
        self.values = new_values
        self.fill_values_frame()

