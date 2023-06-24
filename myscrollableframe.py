import tkinter
from tkinter import ttk
from smh import *


class ScrollableFrame(ttk.LabelFrame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.scrollbar = ttk.Scrollbar(self)
        self.scrollbar.pack(side='right', fill='y', expand=False)

        self.canvas = tkinter.Canvas(self, highlightthickness=0)
        self.canvas.pack(side='right', fill='both', expand=True)

        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.canvas_frame = ttk.Frame(self.canvas)
        self.window = self.canvas.create_window((0, 0), window=self.canvas_frame, anchor='nw')

        self.canvas_frame.bind("<Configure>", lambda event: self.event_frame_configure())
        self.canvas.bind("<Configure>", lambda event: self.event_canvas_configure())

        self.canvas.bind("<Enter>", lambda event: self.canvas.bind_all("<MouseWheel>", lambda event: scroll_canvas(event, self.canvas)))
        self.canvas.bind("<Leave>", lambda event: self.canvas.unbind_all("<MouseWheel>"))

    def event_frame_configure(self):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def event_canvas_configure(self):
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self.canvas_frame.update_idletasks()
        min_height = self.canvas_frame.winfo_reqheight()

        if self.winfo_height() >= min_height:
            new_height = self.winfo_height()
            self.scrollbar.config(command="")
        else:
            new_height = min_height
            self.scrollbar.config(command=self.canvas.yview)
        self.canvas.itemconfig(self.window, height=new_height, width=self.canvas.winfo_width())
