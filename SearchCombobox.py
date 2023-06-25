from tkinter import ttk
import tkinter as tk
from myscrollableframe import *
import re
from smh import *
from Helper_entry import *
import unicodedata
import re


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

        self.scroll_frame = ScrollableFrame(self.dropdown_window)
        self.scroll_frame.pack(fill='both', expand=True, side='left')
        self.scroll_frame.interior.columnconfigure(0, weight=1)

        self.dropdown_window.withdraw()

        self.bind("<FocusIn>", self.open_dropdown_window)
        self.bind("<FocusOut>", lambda event: self.close_dropdown_window())

        self.put_helper_text()

    def put_helper_text(self):
        self.textvariable.set(self.helper_text)
        self.configure(foreground=self.helper_text_color)
        self.current_color = self.helper_text_color

    def open_dropdown_window(self, event):

        if self.current_color == self.helper_text_color:
            self.textvariable.set("")
            self.current_color = self.default_color
            self.configure(foreground=self.default_color)

        self.select_search_values(self.textvariable.get(), None)

        #self.change_selection_window_size()

        self.dropdown_window.deiconify()

    def close_dropdown_window(self):
        if not self.get():
            self.put_helper_text()
        self.dropdown_window.withdraw()

    def change_selection_window_size(self):
        self.scroll_frame.update_idletasks()
        x = self.winfo_rootx()
        y = self.winfo_rooty()

        if not self.scroll_frame.interior.winfo_children():
            self.dropdown_window.geometry(f"{self.winfo_width()}x{0}+{x}+{0 + 35}")
        elif self.scroll_frame.interior.winfo_reqheight() <= 120:
            self.dropdown_window.geometry(
                f"{self.winfo_width()}x{self.scroll_frame.interior.winfo_reqheight() + 12}+{x}+{y + 35}")
        else:
            self.dropdown_window.geometry(f"{self.winfo_width()}x{120}+{x}+{y + 35}")

    def fill_values_frame(self):
        for widget in self.scroll_frame.interior.winfo_children():
            widget.destroy()

        for i, value in enumerate(self.search_values):
            label = ttk.Label(self.scroll_frame.interior, text=value)
            label.bind("<Button-1>", self.select_value)
            label.grid(column=0, row=i, sticky='ew')

        self.change_selection_window_size()

    def select_value(self, event):
        self.textvariable.set(event.widget.cget("text"))
        self.configure(foreground=self.default_color)
        self.current_color = self.default_color
        self.parent.focus_set()

    def select_search_values(self, search_entry, S):
        self.search_values = []
        normalized_search_entry = unicodedata.normalize('NFC', str(search_entry).casefold())
        for value in self.values:
            normalized_value = unicodedata.normalize('NFC',str(value).casefold())
            if normalized_search_entry in normalized_value:
                self.search_values.append(value)

        self.fill_values_frame()
        return True

    def values_update(self, new_values):
        self.values = new_values
        self.fill_values_frame()
