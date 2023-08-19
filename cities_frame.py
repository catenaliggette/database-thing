import tkinter
from tkinter import ttk

from cities_table_frame import *
from add_application_button import *
from myscrollableframe import *
from myscrollableframe import *
from Helper_entry import *
from change_application_window import *


class CitiesFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.query_country = """select country_name from countries"""
        self.query_cities = """select city_name
from cities
inner join countries c on cities.country_id = c.country_id
where country_name = %s"""
        self.search_query = self.query_country

        self.country_city_dict = {}

        self.bind('<Button-1>', lambda event: self.focus_set())

        self.rowconfigure(1, weight=1)
        self.scrollable_frame = ScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, sticky='news', pady=(10, 10))
        country_names, _ = db_select(self.query_country)
        country_names = [country[0] for country in country_names]
        self.fill_dictionary(country_names)
        self.table_frame = TableFrame(self.scrollable_frame.interior, parent.winfo_toplevel(), self.country_city_dict)
        self.table_frame.pack(fill='both', expand=True)

        self.rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        add_button = AddApplicationButton(parent=self, text='Add', style='Accent.TButton',
                                          callback=self.new_data_select)
        add_button.grid(row=0, column=0, sticky='w')

        helper_text = 'Enter application details...'
        self.search_entry = HelperEntry(self, helper_text='Enter city or country name...', width=100)
        self.search_entry.grid(column=0, row=0, sticky='e', padx=(0, 100))

        # self.search_entry.textvariable.trace('w', lambda *args: self.search_query_update())
        #self.search_entry.bind('<KeyRelease>', self.search_query_update)

        clear_button = ttk.Button(self, text='Clear', command=self.clear_search_entry)
        clear_button.grid(column=0, row=0, sticky='e')

    def new_data_select(self):
        #new_data, _ = db_select(self.search_query)
        #self.table_frame.update_data(new_data)
        pass

    def clear_search_entry(self):
        self.search_entry.put_helper_text()
        self.search_query = self.query
        self.new_data_select()

    def search_query_update(self, *args):
        self.search_query = self.query
        search_text = self.search_entry.get()
        if search_text != self.search_entry.helper_text:
            search_keywords = search_text.split()
            if search_keywords:
                self.search_query += f'\nWHERE\n'
                conditions = []
                for word in search_keywords:
                    conditions.append(f"concatenated_columns LIKE '%{word}%'")
                self.search_query += " AND ".join(conditions)
        self.new_data_select()

    def fill_dictionary(self, country_names):
        for country in country_names:
            cities, _ = db_select(self.query_cities, (country,))
            self.country_city_dict[country] = [city[0] for city in cities]


