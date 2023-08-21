import tkinter
from tkinter import ttk

from cities_table_frame import *
from add_city_button import *
from myscrollableframe import *
from myscrollableframe import *
from Helper_entry import *
from change_city_window import *
from change_country_window import *
from change_country_window import *


class CitiesFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.query_country = """select country_name from countries"""
        self.query_cities = """select city_name
from cities
inner join countries c on cities.country_id = c.country_id
where country_name = %s"""

        self.country_city_dict = {}

        self.bind('<Button-1>', lambda event: self.focus_set())

        self.rowconfigure(1, weight=1)
        self.scrollable_frame = ScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, sticky='news', pady=(10, 10))
        self.fill_dictionary()
        self.table_frame = CityTableFrame(self.scrollable_frame.interior, parent.winfo_toplevel(),
                                          self.country_city_dict,
                                          city_change_window=lambda city_name, parent=parent.winfo_toplevel(), callback=self.new_data_select: ChangeCityWindow(parent, city_name, callback),
                                          country_change_window=lambda country_name, parent=parent.winfo_toplevel(), callback=self.new_data_select: ChangeCountryWindow(parent, country_name, callback))
        self.table_frame.pack(fill='both', expand=True)

        self.rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        add_button = AddCityButton(parent=self, text='Add', style='Accent.TButton', callback=self.new_data_select)
        add_button.grid(row=0, column=0, sticky='w')

        self.search_entry = HelperEntry(self, helper_text='Введите название города или страны...', width=100)
        self.search_entry.grid(column=0, row=0, sticky='e', padx=(0, 100))

        self.search_entry.textvariable.trace('w', lambda *args: self.new_data_select())

        clear_button = ttk.Button(self, text='Clear', command=self.clear_search_entry)
        clear_button.grid(column=0, row=0, sticky='e')

    def new_data_select(self):
        self.fill_dictionary()
        self.filter_dictionary()
        self.table_frame.update_data(self.country_city_dict)

    def clear_search_entry(self):
        self.search_entry.put_helper_text()
        self.new_data_select()

    def fill_dictionary(self):
        self.country_city_dict = {}
        country_names, _ = db_select(self.query_country)
        country_names = [country[0] for country in country_names]
        for country in country_names:
            cities, _ = db_select(self.query_cities, (country,))
            self.country_city_dict[country] = [city[0] for city in cities]

    def filter_dictionary(self):
        filtered_dict = {}
        search_text = self.search_entry.get()
        if search_text != self.search_entry.helper_text:
            search_keywords = search_text.split()
            if search_keywords:
                for country, cities in self.country_city_dict.items():
                    matching_cities = []
                    for city in cities:
                        if any(search_word.lower() in city.lower() for search_word in search_keywords):
                            matching_cities.append(city)

                    if matching_cities:
                        filtered_dict[country] = matching_cities
                self.country_city_dict = filtered_dict


