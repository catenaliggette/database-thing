import copy

from database import *
import tkinter
from tkinter import ttk
from selection_option_window import *
from smh import *
from selection_date_window import *
from myscrollableframe import *


class CarTableFrame(ttk.Frame):
    def __init__(self, parent, root, car_list, change_window, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.root = root
        self.car_list = car_list
        self.change_window = change_window
        self.cars_in_row = 3
        self.fill_table_frame()

    def fill_table_frame(self):
        row_index = 0
        col_index = 0
        for car in self.car_list:
            car_frame = ttk.Frame(self)
            car_frame.grid(row=row_index, column=col_index, sticky='ew')
            car_label = ttk.Label(car_frame, text=car)
            label = ttk.Label(car_frame, text='⫶', font=('TkDefaultFont', 14), cursor='hand2')
            label.bind('<Button-1>', self.editing_window)
            car_label.grid(column=0, row=0, sticky='ew')
            label.grid(column=1, row=0)
            if col_index != self.cars_in_row - 1:
                sep = ttk.Separator(car_frame, orient='vertical')
                sep.grid(column=2, row=0, sticky='ns', padx=20)
            car_frame.columnconfigure(0, weight=1)
            car_frame.columnconfigure(1, weight=0)

            col_index = (col_index + 1) % self.cars_in_row
            if col_index == 0:
                row_index += 1

        for i in range(self.cars_in_row):
            self.columnconfigure(i, weight=1)

    def update_table_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.fill_table_frame()

    def update_data(self, new_list):
        self.car_list = copy.copy(new_list)
        self.update_table_frame()

    def editing_window(self, event):
        car_number = event.widget.master.grid_slaves(row=0, column=0)[0].cget("text")
        self.change_window(car_number)
