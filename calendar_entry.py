import tkinter
from tkinter import ttk
from tkcalendar import Calendar
from smh import event_window_loss_focus
from datetime import datetime


class CalendarEntry(ttk.Frame):
    def __init__(self, parent_widget, unselected_date_value, callback=None, unselected_foreground_color='#c6c6c6', *args, **kwargs):
        super().__init__(parent_widget, *args, **kwargs)
        self.configure(style='Card', padding=7, cursor="xterm")
        self.parent_widget = parent_widget
        self.textvariable = tkinter.StringVar(value=unselected_date_value)
        self.unselected_foreground_color = unselected_foreground_color
        self.helper_text = unselected_date_value
        self.callback = callback
        self.calendar_window = None
        self.calendar = None

        self.date_label = ttk.Label(self, textvariable=self.textvariable, foreground=unselected_foreground_color, width=11, anchor='center')
        self.date_label.grid(column=0, row=0)

        self.create_calendar()
        self.bind("<Button-1>", self.open_calendar)
        self.date_label.bind("<Button-1>", self.open_calendar)

    def create_calendar(self):
        self.calendar_window = tkinter.Toplevel(self.parent_widget.winfo_toplevel())
        self.calendar_window.overrideredirect(True)
        self.calendar_window.withdraw()

        self.calendar = Calendar(self.calendar_window, selectmode="day", date_pattern="dd.mm.yyyy", daynameswidth=0,
                                 month=datetime.now().month)
        self.calendar.pack()

        if self.date_label.cget("text") != self.helper_text:
            self.calendar.selection_set(datetime.strptime(self.date_label.cget("text"), "%d.%m.%Y"))

        self.calendar.bind("<<CalendarSelected>>", lambda select_event: self.select_date())
        self.calendar_window.bind("<FocusOut>", lambda focus_event: event_window_loss_focus(focus_event, self.hide_selection_window))

    def open_calendar(self, event):
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_y()
        self.calendar_window.geometry(f"+{x}+{y}")
        self.calendar_window.deiconify()
        self.calendar_window.focus_set()

    def hide_selection_window(self):
        self.parent_widget.winfo_toplevel().focus_set()
        self.calendar_window.withdraw()

    def select_date(self):
        selected_date = self.calendar.selection_get().strftime("%d.%m.%Y")
        self.date_label.config(foreground='#000000')
        self.textvariable.set(selected_date)
        self.hide_selection_window()
        if self.callback is not None:
            self.callback()

    def clear_date(self):
        self.date_label.config(foreground=self.unselected_foreground_color)
        self.textvariable.set(self.helper_text)
        self.calendar.selection_clear()
