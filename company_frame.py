import tkinter
from tkinter import ttk

from table_frame import *
from add_company_button import *
from myscrollableframe import *
from myscrollableframe import *
from Helper_entry import *
from change_company_window import *


class CompanyFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.query = """SELECT Company_name, Company_BIN,email, Phone_number
FROM (
    SELECT
        Company_name,
        Company_BIN,
        email,
        Phone_number,
        CONCAT(Company_name, Company_BIN, email, Phone_number) as concatenated_columns
    FROM
        company
) AS co"""
        self.search_query = self.query

        self.bind('<Button-1>', lambda event: self.focus_set())

        self.rowconfigure(1, weight=1)
        self.scrollable_frame = ScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, sticky='news', pady=(10, 10))
        table_data, column_names = db_select(self.query)
        self.table_frame = TableFrame(self.scrollable_frame.interior, parent.winfo_toplevel(),
                                      weights=[1, 1, 1, 1], change_window=lambda values, parent=parent.winfo_toplevel(), callback=self.new_data_select: ChangeCompanyWindow(parent, values, callback),
                                      checkbox_columns_index=[0, 1, 2, 3], table_data=table_data, column_names=column_names)
        self.table_frame.pack(fill='both', expand=True)

        self.rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        add_button = AddCompanyButton(parent=self, text='Добавить', style='Accent.TButton', callback=self.new_data_select)
        add_button.grid(row=0, column=0, sticky='w')

        helper_text = 'Enter company details...'
        self.search_entry = HelperEntry(self, helper_text=helper_text, width=100)
        self.search_entry.grid(column=0, row=0, sticky='e', padx=(0, 100))

        #self.search_entry.textvariable.trace('w', lambda *args: self.search_query_update())
        self.search_entry.bind('<KeyRelease>', self.search_query_update)

        clear_button = ttk.Button(self, text='Очистить', command=self.clear_search_entry)
        clear_button.grid(column=0, row=0, sticky='e')

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