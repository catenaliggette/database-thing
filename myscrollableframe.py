import tkinter
from tkinter import ttk
from smh import scroll_canvas


class ScrollableFrame(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, style='Card', padding=1, *args, **kwargs)

        self.vertical_scrollbar = ttk.Scrollbar(self)
        self.vertical_scrollbar.pack(side='right', fill='y', expand=False)

        self.horizontal_scrollbar = ttk.Scrollbar(self, orient='horizontal')
        self.horizontal_scrollbar.pack(fill='x', side='bottom', expand=False)

        self.canvas = tkinter.Canvas(self, highlightthickness=0)
        self.canvas.pack(side='right', fill='both', expand=True)

        self.vertical_scrollbar.config(command=self.canvas.yview)
        self.horizontal_scrollbar.config(command=self.canvas.xview)
        self.canvas.config(yscrollcommand=self.vertical_scrollbar.set, xscrollcommand=self.horizontal_scrollbar.set)

        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.interior = ttk.Frame(self.canvas, padding=(0, 0, 12, 0))
        self.window = self.canvas.create_window((0, 0), window=self.interior, anchor='nw')

        self.interior.bind("<Configure>", lambda event: self.event_frame_configure())
        self.canvas.bind("<Configure>", lambda event: self.event_canvas_configure())

        self.canvas.bind("<Enter>", lambda event: self.canvas.bind_all("<MouseWheel>", lambda event: scroll_canvas(event, self.canvas)))
        self.canvas.bind("<Leave>", lambda event: self.canvas.unbind_all("<MouseWheel>"))

    def event_frame_configure(self):
        #self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        a = self.canvas.bbox('all')
        self.canvas.configure(scrollregion=(0, 0, a[2]-12, a[3]))

    def event_canvas_configure(self):
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self.interior.update_idletasks()
        min_height = self.interior.winfo_reqheight()
        min_width = self.interior.winfo_reqwidth()

        if self.winfo_height() >= min_height:
            new_height = self.winfo_height()
            #self.scrollbar.config(command="")
        else:
            new_height = min_height
            #self.vertical_scrollbar.config(command=self.canvas.yview)

        if self.winfo_width() >= min_width:
            new_width = self.winfo_width()
        else:
            new_width = min_width

        self.canvas.itemconfig(self.window, height=new_height, width=new_width)
