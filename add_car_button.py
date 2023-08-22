from myaddbutton import *
from smh import *
from tkinter import messagebox
from Helper_entry import *
from SearchCombobox import *


class AddCarButton(MyAddButton):
    def __init__(self, parent, callback, *args, **kwargs):
        self.callback = callback
        self.car_entry = None
        super().__init__(parent, *args, **kwargs, command=lambda: self.create_add_window(parent))

    def create_add_window(self, parent):
        add_window = tkinter.Toplevel(parent.winfo_toplevel())
        add_window.grab_set()
        add_window.focus_set()
        add_window.title('Добавление нового Автомобиля')
        add_window.geometry("290x110")
        add_window.bind('<Button-1>', lambda event: self.add_window_set_focus(event, add_window))

        self.car_entry = HelperEntry(add_window, helper_text='Номер Автомобиля')
        self.car_entry.grid(column=0, columnspan=1, row=0, padx=(15, 5), pady=(10, 0), sticky='ew')

        cancel_button = ttk.Button(add_window, text='Отмена', command=add_window.destroy)
        cancel_button.grid(column=0, columnspan=2, row=1, sticky='e', padx=(0, 105), pady=(20, 0))

        add_button = ttk.Button(add_window, text='Добавить', command=lambda: self.add_car(add_window),
                                style='Accent.TButton')
        add_button.grid(column=1, row=1, sticky='e', pady=(20, 0), padx=5)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def add_car(self, add_window):
        if self.varify_new_car():
            self.commit_new_data()
            self.callback()
            add_window.destroy()

    def varify_new_car(self):
        if self.car_entry.get() == self.car_entry.helper_text:
            messagebox.showerror("Пустое поле", "Пожалуйста, введите Номер Автомобиля")
            return False

        return True

    def commit_new_data(self):
        car = self.car_entry.textvariable.get()
        db_commit('''insert into cars (car_number) values (%s)''', (car, ))