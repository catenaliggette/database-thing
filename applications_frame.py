import tkinter
from tkinter import ttk

from table_frame import *
from add_application_button import *
from myscrollableframe import *
from myscrollableframe import *
from Helper_entry import *
from change_application_window import *


class ApplicationFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.query = """
SELECT Company_name as "Имя Компании", Company_BIN as "БИН", application_date as "Дата заявки", car_number as "Транспорт", freight_cost as "Стоимость", senders_address as "Адрес отправителя", recipients_address as "Адрес получателя", SMR_path as "СМР", application_path as "Заявка"
FROM (
    SELECT
        c.Company_name,
        Company_BIN,
        application_date,
        car_number,
        freight_cost,
        CONCAT(senders_country.country_name, ', ', senders_city.city_name) AS senders_address,
        CONCAT(recipients_country.country_name, ', ', recipients_city.city_name) AS recipients_address,
        SMR_path,
        application_path,
        CONCAT(c.Company_name, Company_BIN, application_date, car_number, freight_cost, senders_country.country_name, senders_city.city_name, recipients_country.country_name, recipients_city.city_name) as concatenated_columns
    FROM
        transport_applications AS ta
        INNER JOIN company c ON ta.Company_id = c.Company_id
        INNER JOIN cars c2 ON ta.Car_id = c2.car_id
        JOIN cities senders_city ON senders_city.city_id = ta.senders_city_id
        JOIN countries senders_country ON senders_city.country_id = senders_country.country_id
        JOIN cities recipients_city ON recipients_city.city_id = ta.recipients_city_id
        JOIN countries recipients_country ON recipients_city.country_id = recipients_country.country_id
) AS table_alias
    """
        self.search_query = self.query

        self.bind('<Button-1>', lambda event: self.focus_set())

        self.rowconfigure(2, weight=1)
        self.scrollable_frame = ScrollableFrame(self)
        self.scrollable_frame.grid(row=2, column=0, sticky='news', pady=(10, 10))
        table_data, column_names = db_select(self.query)
        self.table_frame = TableFrame(self.scrollable_frame.interior, parent.winfo_toplevel(),
                                      weights=[3, 3, 2, 3, 2, 4, 4, 1, 1],
                                      change_window=lambda values, parent=parent.winfo_toplevel(),
                                                           callback=self.new_data_select: ChangeApplicationWindow(
                                          parent, values, callback),
                                      checkbox_columns_index=[0, 1, 3, 4, 5, 6], date_column_index=[2],
                                      file_column_index=[7, 8], table_data=table_data, column_names=column_names)
        self.table_frame.pack(fill='both', expand=True)

        self.rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        add_button = AddApplicationButton(parent=self, text='Добавить', style='Accent.TButton',
                                          callback=self.new_data_select)
        add_button.grid(row=0, column=0, sticky='w')

        helper_text = 'Введите информацию о Заявке...'
        self.search_entry = HelperEntry(self, helper_text='Введите информацию о Заявке...', width=100)
        self.search_entry.grid(column=0, row=0, sticky='e', padx=(0, 100))

        # self.search_entry.textvariable.trace('w', lambda *args: self.search_query_update())
        self.search_entry.bind('<KeyRelease>', self.search_query_update)

        clear_button = ttk.Button(self, text='Очистить', command=self.clear_search_entry)
        clear_button.grid(column=0, row=0, sticky='e')

        clear_all_button = ttk.Button(self, text='Очистить Все', command=self.clear_all_selections)
        clear_all_button.grid(column=0, row=1, sticky='e', pady=(10, 0))

    def new_data_select(self):
        new_data, _ = db_select(self.search_query)
        self.table_frame.update_data(new_data)

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

    def clear_all_selections(self):
        self.clear_search_entry()
        self.table_frame.clear_all_selections()