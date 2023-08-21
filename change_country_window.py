from smh import *
from tkinter import messagebox
from Helper_entry import *
from SearchCombobox import *


class ChangeCountryWindow(tkinter.Toplevel):
    def __init__(self, parent, country_name, callback, *args, **kwargs):
        self.callback = callback
        self.current_country_name = country_name
        super().__init__(parent, *args, **kwargs)
        self.create_change_window()

    def create_change_window(self):
        self.grab_set()
        self.focus_set()
        self.title('Change Country')
        self.geometry("300x110")
        self.bind('<Button-1>', lambda event: self.set_focus(event))

        self.country_entry = HelperEntry(self, helper_text='Country')
        self.country_entry.set_text(self.current_country_name)
        self.country_entry.grid(column=0, row=0, padx=(15, 5), pady=(10, 0), sticky='ew')

        cancel_button = ttk.Button(self, text='Cancel', command=self.destroy)
        cancel_button.grid(column=0, columnspan=2, row=2, sticky='e', padx=(0, 105), pady=(20, 0))

        save_button = ttk.Button(self, text='Save', command=self.change_country, style='Accent.TButton')
        save_button.grid(column=1, row=2, sticky='e', pady=(20, 0), padx=5)

        delete_button = ttk.Button(self, text='Delete', command=self.delete_country, width=0)
        delete_button.grid(column=0, row=2, sticky='w', padx=15, pady=(20, 0))

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def change_country(self):
        if self.varify_new_changes():
            self.change_data()
            self.callback()
            self.destroy()

    def set_focus(self, event):
        if event.widget == self:
            self.focus_set()

    def varify_new_changes(self):
        if self.country_entry.get() == self.country_entry.helper_text:
            messagebox.showerror("Empty entry", "Please, type Country name")
            return False
        return True

    def change_data(self):
        country = self.country_entry.textvariable.get()
        db_commit('''update countries set country_name = %s where country_name = %s''',
                  (country, self.current_country_name))

    def delete_country(self):
        cities, _ = db_select('''select city_name
from cities
inner join countries c on cities.country_id = c.country_id
where country_name = %s''', (self.current_country_name,))
        print(cities)
        if cities:
            question_window = tkinter.messagebox.askquestion('Delete Country',
                                                             "All Cities from this country will be removed from the database.\nProceed?",
                                                             icon='warning')
            if question_window == 'yes':
                db_commit('''delete cc
                            from cities as cc
                            inner join countries c on cc.country_id = c.country_id
                            where country_name = %s''', (self.current_country_name,))
                db_commit('''delete from countries where country_name = %s''', (self.current_country_name,))
                self.callback()
                self.destroy()
        else:
            question_window = tkinter.messagebox.askquestion('Delete Country',
                                                             "R U Sure?",
                                                             icon='question')
            if question_window == 'yes':
                db_commit('''delete from countries where country_name = %s''', (self.current_country_name,))