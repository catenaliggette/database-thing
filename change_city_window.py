import tkinter
from tkinter import ttk
from smh import db_select
from smh import db_commit
from tkinter import messagebox
from Helper_entry import HelperEntry
from SearchCombobox import SearchCombobox


class ChangeCityWindow(tkinter.Toplevel):
    def __init__(self, parent, city_name, callback, *args, **kwargs):
        self.callback = callback
        self.current_city_name = city_name
        country_name, _ = db_select('''select country_name
        from countries
        inner join cities c on countries.country_id = c.country_id
        where city_name = %s''', (self.current_city_name,))
        self.current_country_name = country_name[0][0]
        super().__init__(parent, *args, **kwargs)
        self.create_change_window()

    def create_change_window(self):
        self.grab_set()
        self.focus_set()
        self.title('Редактирование Города')
        self.geometry("340x110")
        self.bind('<Button-1>', lambda event: self.set_focus(event))

        self.city_entry = HelperEntry(self, helper_text='Город')
        self.city_entry.set_text(self.current_city_name)
        self.city_entry.grid(column=0, row=0, padx=(15, 5), pady=(10, 0), sticky='w')

        country_values, _ = db_select('''select distinct country_name from countries''')
        self.country_entry = SearchCombobox(self, helper_text='Страна', values=country_values)
        self.country_entry.set_text(self.current_country_name)
        self.country_entry.grid(column=1, row=0, padx=(0, 5), pady=(10, 0), sticky='w')

        cancel_button = ttk.Button(self, text='Отмена', command=self.destroy)
        cancel_button.grid(column=0, columnspan=2, row=2, sticky='e', padx=(0, 105), pady=(20, 0))

        save_button = ttk.Button(self, text='Сохранить', command=self.change_city, style='Accent.TButton')
        save_button.grid(column=1, row=2, sticky='e', padx=5, pady=(20, 0))

        delete_button = ttk.Button(self, text='Удалить', command=self.delete_city, width=0)
        delete_button.grid(column=0, row=2, sticky='w', padx=15, pady=(20, 0))

    def change_city(self):
        if self.varify_new_changes():
            self.change_data()
            self.callback()
            self.destroy()

    def set_focus(self, event):
        if event.widget == self:
            self.focus_set()

    def varify_new_changes(self):
        if self.city_entry.get() == self.city_entry.helper_text:
            messagebox.showerror("Пустое поле", "Пожалуйста, введите название Города")
            return False

        if self.country_entry.get() == self.country_entry.helper_text:
            messagebox.showerror("Пустое поле", "Пожалуйста, выберите название Страны или введите новое")
            return False

        return True

    def change_data(self):
        city = self.city_entry.textvariable.get()
        country = self.country_entry.textvariable.get()
        country_values, _ = db_select('''select distinct country_name from countries where country_name=%s''',
                                      (country,))
        if country_values:
            if country_values[0][0] == self.current_country_name:
                db_commit('''update cities
inner join countries c on cities.country_id = c.country_id
set city_name = %s
where city_name = %s and country_name = %s''', (city, self.current_city_name, self.current_country_name))
            else:
                country_id, _ = db_select('''select distinct country_id from countries where country_name = %s''',
                                          (country,))
                db_commit('''update cities
inner join countries c on cities.country_id = c.country_id
set city_name = %s, cities.country_id = (select d.country_id from countries as d where d.country_name = %s)
where city_name = %s and country_name = %s''', (city, country, self.current_city_name, self.current_country_name))
        else:
            db_commit('''insert into countries (country_name) values (%s)''', (country,))
            db_commit('''update cities
inner join countries c on cities.country_id = c.country_id
set city_name = %s, cities.country_id = (select d.country_id from countries as d where d.country_name = %s)
where city_name = %s and country_name = %s''', (city, country, self.current_city_name, self.current_country_name))

    def delete_city(self):
        question_window = tkinter.messagebox.askquestion('Удаление Города',
                                                         "Вы уверены?",
                                                         icon='question')
        if question_window == 'yes':
            db_commit('''delete from cities
where city_name = %s and country_id = (select country_id from countries where countries.country_name = %s)''',
                      (self.current_city_name, self.current_country_name))
            self.callback()
            self.destroy()
