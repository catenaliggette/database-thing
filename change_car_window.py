import tkinter
from tkinter import ttk
from smh import db_select
from smh import db_commit
from tkinter import messagebox
from Helper_entry import HelperEntry


class ChangeCarWindow(tkinter.Toplevel):
    def __init__(self, parent, car_number, callback, *args, **kwargs):
        self.car_entry = None
        self.callback = callback
        self.current_car_number = car_number
        super().__init__(parent, *args, **kwargs)
        self.create_change_window()

    def create_change_window(self):
        self.grab_set()
        self.focus_set()
        self.title('Редактирование Номера Автомобиля')
        self.geometry("300x110")
        self.bind('<Button-1>', lambda event: self.set_focus(event))

        self.car_entry = HelperEntry(self, helper_text='Номер Автомобиля')
        self.car_entry.set_text(self.current_car_number)
        self.car_entry.grid(column=0, row=0, padx=(15, 5), pady=(10, 0), sticky='ew')

        cancel_button = ttk.Button(self, text='Отмена', command=self.destroy)
        cancel_button.grid(column=0, columnspan=2, row=2, sticky='e', padx=(0, 105), pady=(20, 0))

        save_button = ttk.Button(self, text='Сохранить', command=self.change_car, style='Accent.TButton')
        save_button.grid(column=1, row=2, sticky='e', pady=(20, 0), padx=5)

        delete_button = ttk.Button(self, text='Удалить', command=self.delete_car, width=0)
        delete_button.grid(column=0, row=2, sticky='w', padx=15, pady=(20, 0))

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def change_car(self):
        if self.varify_new_changes():
            self.change_data()
            self.callback()
            self.destroy()

    def set_focus(self, event):
        if event.widget == self:
            self.focus_set()

    def varify_new_changes(self):
        if self.car_entry.get() == self.car_entry.helper_text:
            messagebox.showerror("Пустое поле", "Пожалуйста, выберите Номер Автомобиля")
            return False
        return True

    def change_data(self):
        car = self.car_entry.textvariable.get()
        db_commit('''update cars set car_number = %s where car_number = %s''',
                  (car, self.current_car_number))

    def delete_car(self):
        cars, _ = db_select('''select car_number
from cars
inner join transport_applications ta on cars.car_id = ta.Car_id
where car_number = %s''', (self.current_car_number,))
        if cars:
            question_window = tkinter.messagebox.askquestion('Удаление Номера Автомобиля',
                                                             "Все Заявки с данных Номером Автомобиля будут удалены из базы данных.\nПродолжить?",
                                                             icon='warning')
            if question_window == 'yes':
                db_commit('''delete cc
                            from transport_applications as cc
                            inner join cars c on cc.car_id = c.Car_id
                            where car_number = %s''', (self.current_car_number,))
                db_commit('''delete from cars where car_number = %s''', (self.current_car_number,))
                self.callback()
                self.destroy()
        else:
            question_window = tkinter.messagebox.askquestion('Удаление Номера Автомобиля',
                                                             "Вы уверены?",
                                                             icon='question')
            if question_window == 'yes':
                db_commit('''delete from cars where car_number = %s''', (self.current_car_number,))
