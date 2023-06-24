import tkinter
from tkinter import ttk


class HelperEntry(ttk.Entry):
    def __init__(self, parent, helper_text="", helper_text_color='#c6c6c6', *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.helper_text = helper_text
        self.current_color = helper_text_color
        self.helper_text_color = helper_text_color
        self.default_color = self.cget('foreground')

        self.bind('<FocusIn>', self.event_focus_in)
        self.bind('<FocusOut>', self.event_focus_out)
        self.put_helper_text()

    def event_focus_in(self, event):
        if self.current_color == self.helper_text_color:
            self.delete(0, 'end')
            self.configure(foreground=self.default_color)
            self.current_color = self.default_color

    def event_focus_out(self, event):
        if not self.get():
            self.put_helper_text()

    def put_helper_text(self):
        self.insert(0, self.helper_text)
        self.configure(foreground=self.helper_text_color)
        self.current_color = self.helper_text_color
