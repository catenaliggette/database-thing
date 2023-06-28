import tkinter

from myaddbutton import *
from SearchCombobox import *
from calendar_entry import *
from smh import *
from tkinterdnd2 import *
from tkinter import filedialog
import os
from tkinter import messagebox
from datetime import datetime

class ChangeApplicationWindow(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_change_window()

    def create_change_window(self):
        self.grab_set()
        self.focus_set()
        self.title('Change Application')
        self.geometry("500x450")
        self.bind('<Button-1>', lambda event: self.add_window_set_focus(event, self))

        SMR_file_name = tkinter.StringVar()
        application_file_name = tkinter.StringVar()

        company_values, company_label_text = db_select('''select distinct Company_name as "Company:" from company''')
        company_label = ttk.Label(self, text="Company:")
        company_label.grid(column=0, row=0, padx=(10, 5), pady=(10, 0), sticky='e')
        self.company_searchbox = SearchCombobox(self, values=["".join(value) for value in company_values],
                                                helper_text='Name')
        self.company_searchbox.grid(column=1, row=0, padx=(5, 0), pady=(10, 0), sticky='w')

        bin_values, _ = db_select('''select distinct Company_BIN from company''')
        self.bin_searchbox = SearchCombobox(self, values=[value[0] for value in bin_values], helper_text='BIN')
        self.bin_searchbox.grid(column=2, row=0, padx=(0, 5), pady=(10, 0), sticky='w')

        new_company_button = AddCompanyButton(parent=self, width=0, text='+', style='Accent.TButton',
                                              callback=self.add_company_callback)
        new_company_button.grid(row=0, column=3, sticky='w', pady=(10, 0))

        self.company_searchbox.textvariable.trace('w', lambda name, index, mode,
                                                              sv=self.company_searchbox.textvariable: self.fill_if_connected(
            sv,
            '''select Company_BIN from company where Company_name = %s''',
            self.bin_searchbox))
        self.bin_searchbox.textvariable.trace('w', lambda name, index, mode,
                                                          sv=self.bin_searchbox.textvariable: self.fill_if_connected(sv,
                                                                                                                     '''select Company_name from company where Company_BIN = %s''',
                                                                                                                     self.company_searchbox))

        date_label = ttk.Label(self, text="Application date:")
        date_label.grid(column=0, row=1, padx=(10, 5), sticky='e', pady=(5, 0))
        self.date_entry = CalendarEntry(self, unselected_foreground_color='#c6c6c6',
                                        unselected_date_value='dd.mm.yyyy')
        self.date_entry.grid(column=1, row=1, sticky='w', padx=5, pady=(5, 0))

        car_values, car_label_text = db_select('''select distinct car_number as "Car Number:" from cars''')
        car_label = ttk.Label(self, text=car_label_text[0])
        car_label.grid(column=0, row=3, padx=(10, 5), sticky='e', pady=(5, 0))
        self.car_searchbox = SearchCombobox(self, values=["".join(value) for value in car_values])
        self.car_searchbox.grid(column=1, row=3, sticky='w', padx=5, pady=(5, 0))

        cost_label = ttk.Label(self, text='Freight cost:')
        cost_label.grid(column=0, row=4, padx=(10, 5), sticky='e', pady=(5, 0))
        self.cost_entry = ttk.Entry(self)
        self.cost_entry.grid(column=1, row=4, sticky='w', padx=5, pady=(5, 0))

        country_values, _ = db_select('''select distinct country_name from countries''')
        city_values, _ = db_select('''select distinct city_name from cities''')

        sender_label = ttk.Label(self, text="Sender:")
        sender_label.grid(column=0, row=5, padx=(10, 5), sticky='e', pady=(5, 0))
        self.sender_country_searchbox = SearchCombobox(self, values=country_values, helper_text='Country')
        self.sender_country_searchbox.grid(column=1, row=5, padx=(5, 0), sticky='w', pady=(5, 0))
        self.sender_city_searchbox = SearchCombobox(self, values=city_values, helper_text='City')
        self.sender_city_searchbox.grid(column=2, row=5, sticky='w', pady=(5, 0))

        recipient_label = ttk.Label(self, text="Recipient:")
        recipient_label.grid(column=0, row=6, padx=(10, 5), sticky='e', pady=(5, 0))
        self.recipient_country_searchbox = SearchCombobox(self, values=country_values, helper_text='Country')
        self.recipient_country_searchbox.grid(column=1, row=6, padx=(5, 0), sticky='w', pady=(5, 0))
        self.recipient_city_searchbox = SearchCombobox(self, values=city_values, helper_text='City')
        self.recipient_city_searchbox.grid(column=2, row=6, sticky='w', pady=(5, 0))

        self.sender_city_searchbox.textvariable.trace('w', lambda name, index, mode,
                                                                  sv=self.sender_city_searchbox.textvariable: self.fill_if_connected(
            sv, '''select country_name
        from countries
        inner join cities c on countries.country_id = c.country_id
        where city_name = %s''', self.sender_country_searchbox))
        self.recipient_city_searchbox.textvariable.trace('w', lambda name, index, mode,
                                                                     sv=self.recipient_city_searchbox.textvariable: self.fill_if_connected(
            sv, '''select country_name
                from countries
                inner join cities c on countries.country_id = c.country_id
                where city_name = %s''', self.recipient_country_searchbox))

        SMR_file_frame = ttk.LabelFrame(self, text='SMR', width=200, height=100)
        SMR_file_frame.grid_propagate(False)
        SMR_file_frame.grid(column=0, columnspan=2, row=7, pady=(20, 0))
        SMR_file_frame.drop_target_register(DND_ALL)
        SMR_file_frame.dnd_bind("<<Drop>>",
                                lambda event: self.set_drop_file_path(event, SMR_file_name, self.set_SMR_file_path))
        SMR_file_frame.columnconfigure(0, weight=1)
        SMR_file_frame.rowconfigure(0, weight=1)
        SMR_file_text = ttk.Label(SMR_file_frame, text=f'Press to Select file\n or drag and drop it here',
                                  foreground='#c6c6c6', anchor='center')
        SMR_file_text.grid(sticky='news', column=0, row=0, pady=5, padx=5)

        SMR_file_name_label = ttk.Label(self, textvariable=SMR_file_name, wraplength=200)
        SMR_file_name_label.grid(column=0, columnspan=2, row=8, sticky='nw', padx=(50, 0), pady=(0, 20))

        SMR_file_frame.bind('<Button-1>',
                            lambda event: self.set_select_file_explorer(event, SMR_file_name, self.set_SMR_file_path))
        SMR_file_text.bind('<Button-1>',
                           lambda event: self.set_select_file_explorer(event, SMR_file_name, self.set_SMR_file_path))

        application_file_frame = ttk.LabelFrame(self, text='Application', width=200, height=100)
        application_file_frame.grid_propagate(False)
        application_file_frame.grid(column=2, columnspan=2, row=7, pady=(20, 0))
        application_file_frame.drop_target_register(DND_ALL)
        application_file_frame.dnd_bind("<<Drop>>", lambda event: self.set_drop_file_path(event, application_file_name,
                                                                                          self.set_application_file_path))
        application_file_frame.columnconfigure(0, weight=1)
        application_file_frame.rowconfigure(0, weight=1)
        application_file_text = ttk.Label(application_file_frame,
                                          text=f'Press to Select file\n or drag and drop it here', foreground='#c6c6c6',
                                          anchor='center')
        application_file_text.grid(sticky='news', column=0, row=0, pady=5, padx=5)

        application_file_name_label = ttk.Label(self, textvariable=application_file_name, wraplength=200)
        application_file_name_label.grid(column=2, columnspan=2, row=8, sticky='nw', padx=(10, 0), pady=(0, 20))

        application_file_frame.bind('<Button-1>',
                                    lambda event: self.set_select_file_explorer(event, application_file_name,
                                                                                self.set_application_file_path))
        application_file_text.bind('<Button-1>',
                                   lambda event: self.set_select_file_explorer(event, application_file_name,
                                                                               self.set_application_file_path))

        cancel_button = ttk.Button(self, text="Cansel", command=self.destroy)
        cancel_button.grid(column=1, columnspan=2, row=9, sticky='e', padx=70)