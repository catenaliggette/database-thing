import tkinter
from tkinter import ttk


class HelperEntry(ttk.Entry):
    def __init__(self, parent, helper_text="", helper_text_color='#c6c6c6', *args, **kwargs):
        self.textvariable = tkinter.StringVar(value=helper_text)
        super().__init__(parent, textvariable=self.textvariable, *args, **kwargs)
        self.helper_text = helper_text
        self.current_color = helper_text_color
        self.helper_text_color = helper_text_color
        self.default_color = self.cget('foreground')

        self.bind('<FocusIn>', self.event_focus_in)
        self.bind('<FocusOut>', self.event_focus_out)
        self.put_helper_text()

    def event_focus_in(self, event):
        if self.current_color == self.helper_text_color:
            self.textvariable.set('')
            self.configure(foreground=self.default_color)
            self.current_color = self.default_color

    def event_focus_out(self, event):
        if not self.get():
            self.put_helper_text()

    def put_helper_text(self):
        self.textvariable.set(self.helper_text)
        self.configure(foreground=self.helper_text_color)
        self.current_color = self.helper_text_color
