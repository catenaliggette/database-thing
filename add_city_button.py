from myaddbutton import *
from smh import *
from tkinter import messagebox
from Helper_entry import *
from SearchCombobox import *


class AddCityButton(MyAddButton):
    def __init__(self, parent, callback, *args, **kwargs):
        self.callback = callback
        self.city_entry = None
        self.country_entry = None
        super().__init__(parent, *args, **kwargs, command=lambda: self.create_add_window(parent))

    def create_add_window(self, parent):
        add_window = tkinter.Toplevel(parent.winfo_toplevel())
        add_window.grab_set()
        add_window.focus_set()
        add_window.title('Добавление нового Города')
        add_window.geometry("330x110")
        add_window.bind('<Button-1>', lambda event: self.add_window_set_focus(event, add_window))

        self.city_entry = HelperEntry(add_window, helper_text='Город')
        self.city_entry.grid(column=0, row=0, padx=(5, 5), pady=(10, 0), sticky='w')

        country_values, _ = db_select('''select distinct country_name from countries''')
        self.country_entry = SearchCombobox(add_window, helper_text='Страна', values=country_values)
        self.country_entry.grid(column=1, row=0, padx=(0, 5), pady=(10, 0), sticky='w')

        cancel_button = ttk.Button(add_window, text='Отмена', command=add_window.destroy)
        cancel_button.grid(column=0, columnspan=2, row=2, sticky='e', padx=(0, 105), pady=(20, 0))

        add_button = ttk.Button(add_window, text='Добавить', command=lambda: self.add_city(add_window),
                                style='Accent.TButton')
        add_button.grid(column=1, row=2, sticky='e', padx=5, pady=(20, 0))

    def add_city(self, add_window):
        if self.varify_new_city():
            self.commit_new_data()
            self.callback()
            add_window.destroy()

    def varify_new_city(self):
        if self.city_entry.get() == self.city_entry.helper_text:
            messagebox.showerror("Пустое поле", "Пожалуйста, введите название Города")
            return False

        if self.country_entry.get() == self.country_entry.helper_text:
            messagebox.showerror("Пустое поле", "Пожалуйста, выберите название Страны или введите новое")
            return False

        return True

    def commit_new_data(self):
        city = self.city_entry.textvariable.get()
        country = self.country_entry.textvariable.get()

        country_values, _ = db_select('''select distinct country_name from countries where country_name=%s''',
                                      (country,))
        if not country_values:
            db_commit('''insert into countries (country_name) values (%s)''', (country,))

        db_commit('''insert into cities (city_name, country_id)
                        select %s, country_id from countries where country_name = %s''', (city, country))