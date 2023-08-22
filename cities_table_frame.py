import copy

from database import *
import tkinter
from tkinter import ttk
from selection_option_window import *
from smh import *
from selection_date_window import *
from myscrollableframe import *


class CityTableFrame(ttk.Frame):
    def __init__(self, parent, root, country_city_dict, city_change_window, country_change_window, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.root = root
        self.country_city_dict = country_city_dict
        self.city_change_window = city_change_window
        self.country_change_window = country_change_window
        self.cities_in_row = 3
        self.fill_table_frame()

    def fill_table_frame(self):
        row_index = 0
        for country, cities in self.country_city_dict.items():
            country_frame = tkinter.Frame(self, bg='#CCCCCC')
            country_label = tkinter.Label(country_frame, background='#CCCCCC', anchor='center', text=country)
            country_label.grid(column=0, row=0, sticky='w', pady=5)
            label = tkinter.Label(country_frame, text='⫶', font=('TkDefaultFont', 14), cursor='hand2',
                                  background='#CCCCCC')
            label.bind('<Button-1>', self.country_editing_window)
            label.grid(column=1, row=0)
            country_frame.columnconfigure(0, weight=1)
            country_frame.grid(row=row_index, column=0, columnspan=self.cities_in_row, sticky='ew')

            col_index = 0
            for city in cities:
                if col_index == 0:
                    row_index += 1

                city_frame = ttk.Frame(self)
                city_frame.grid(row=row_index, column=col_index, sticky='ew')
                city_label = ttk.Label(city_frame, text=city)
                label = ttk.Label(city_frame, text='⫶', font=('TkDefaultFont', 14), cursor='hand2')
                label.bind('<Button-1>', self.city_editing_window)
                city_label.grid(column=0, row=0, sticky='ew')
                label.grid(column=1, row=0)
                if col_index != self.cities_in_row - 1:
                    sep = ttk.Separator(city_frame, orient='vertical')
                    sep.grid(column=2, row=0, sticky='ns', padx=20)
                city_frame.columnconfigure(0, weight=1)
                city_frame.columnconfigure(1, weight=0)

                col_index = (col_index + 1) % self.cities_in_row
            row_index += 1

        for i in range(self.cities_in_row):
            self.columnconfigure(i, weight=1)

    def update_table_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.fill_table_frame()

    def update_data(self, new_dict):
        self.country_city_dict = new_dict
        self.update_table_frame()

    def city_editing_window(self, event):
        city_name = event.widget.master.grid_slaves(row=0, column=0)[0].cget("text")
        self.city_change_window(city_name)

    def country_editing_window(self, event):
        country_name = event.widget.master.grid_slaves(row=0, column=0)[0].cget("text")
        self.country_change_window(country_name)