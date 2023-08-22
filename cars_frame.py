from tkinter import ttk
from smh import db_select
from add_car_button import AddCarButton
from myscrollableframe import ScrollableFrame
from Helper_entry import HelperEntry
from change_car_window import ChangeCarWindow
from cars_table_frame import CarTableFrame


class CarsFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.query = """select car_number from cars"""
        self.car_list = []
        self.fill_car_list()

        self.bind('<Button-1>', lambda event: self.focus_set())

        self.rowconfigure(1, weight=1)
        self.scrollable_frame = ScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, sticky='news', pady=(10, 10))
        self.table_frame = CarTableFrame(self.scrollable_frame.interior, parent.winfo_toplevel(),
                                         self.car_list,
                                         change_window=lambda car, parent=parent.winfo_toplevel(),
                                                              callback=self.new_data_select: ChangeCarWindow(parent,
                                                                                                             car,
                                                                                                             callback))
        self.table_frame.pack(fill='both', expand=True)

        self.rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        add_button = AddCarButton(parent=self, text='Добавить', style='Accent.TButton', callback=self.new_data_select)
        add_button.grid(row=0, column=0, sticky='w')

        self.search_entry = HelperEntry(self, helper_text='Введите название города или страны...', width=100)
        self.search_entry.grid(column=0, row=0, sticky='e', padx=(0, 100))

        self.search_entry.textvariable.trace('w', lambda *args: self.new_data_select())

        clear_button = ttk.Button(self, text='Очистить', command=self.clear_search_entry)
        clear_button.grid(column=0, row=0, sticky='e')

    def new_data_select(self):
        self.fill_car_list()
        self.filter_car_list()
        self.table_frame.update_data(self.car_list)

    def clear_search_entry(self):
        self.search_entry.put_helper_text()
        self.new_data_select()

    def fill_car_list(self):
        car_numbers, _ = db_select(self.query)
        car_numbers = [country[0] for country in car_numbers]
        self.car_list = car_numbers

    def filter_car_list(self):
        search_text = self.search_entry.get()
        if search_text != self.search_entry.helper_text:
            search_keywords = search_text.split()
            if search_keywords:
                filtered_car_list = []
                for car in self.car_list:
                    if any(search_word.lower() in car.lower() for search_word in search_keywords):
                        filtered_car_list.append(car)
                self.car_list = filtered_car_list
