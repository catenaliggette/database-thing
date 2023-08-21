import tkinter
from tkinter import ttk
from tkcalendar import Calendar
from calendar_entry import *
from smh import event_window_loss_focus
from datetime import datetime


class SelectionDateWindow(tkinter.Toplevel):

    def __init__(self, root, callback):
        super().__init__(root)
        self.root = root
        self.callback = callback
        self.unselected_date_value = 'дд.мм.гггг'
        self.list_date_entry = []
        self.list_clear_label = []
        self.create_selection_window()

    def create_selection_window(self):
        self.overrideredirect(True)
        #self.bind("<FocusOut>", lambda focus_event: event_window_loss_focus(focus_event, self, self.hide_window))

        selection_frame = ttk.LabelFrame(self, labelwidget=ttk.Frame(self))
        selection_frame.pack(fill='both', expand=True)

        self.withdraw()

        for i in range(2):
            selection_frame.columnconfigure(i, weight=1)
            date_entry = CalendarEntry(selection_frame, width=11,
                                       unselected_foreground_color='#c6c6c6', callback=self.selected_date_change,
                                       unselected_date_value=self.unselected_date_value)
            date_entry.grid(column=i, row=2)
            self.list_date_entry.append(date_entry)

        start_label = ttk.Label(selection_frame, text='Start')
        start_label.grid(column=0, row=0, pady=(10, 0))
        end_label = ttk.Label(selection_frame, text='End')
        end_label.grid(column=1, row=0, pady=(10, 0))

        for i in range(2):
            clear_label = ttk.Label(selection_frame, text="")
            clear_label.grid(column=i, row=1, sticky='e')
            clear_label.bind("<Button-1>", self.clear_data_entry)
            self.list_clear_label.append(clear_label)

    def hide_window(self):
        self.withdraw()

    def show_window(self, event):
        x = event.widget.winfo_rootx()
        y = event.widget.winfo_rooty()

        self.focus_set()
        self.geometry(f"{200}x{87}+{x + 12}+{y + 28}")
        self.deiconify()

    def check_selected_variable(self, target_date):
        start_date = self.list_date_entry[0].date_label.cget("text")
        end_date = self.list_date_entry[1].date_label.cget("text")
        if start_date == self.unselected_date_value and end_date == self.unselected_date_value:
            return True
        if start_date != self.unselected_date_value and target_date < datetime.strptime(start_date, '%d.%m.%Y').date():
            return False
        if end_date != self.unselected_date_value and target_date > datetime.strptime(end_date, '%d.%m.%Y').date():
            return False
        return True

    def selected_date_change(self):
        for i in range(2):
            if self.list_date_entry[i].date_label.cget("text") != self.unselected_date_value:
                self.list_clear_label[i].config(text='🗑')
        self.callback()

    def clear_data_entry(self, event):
        event.widget.config(text='')
        self.list_date_entry[event.widget.grid_info()['column']].clear_date()
        self.callback()