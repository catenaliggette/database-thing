from smh import *
from tkinter import messagebox
from Helper_entry import *


class ChangeCompanyWindow(tkinter.Toplevel):
    def __init__(self, parent, values, callback, *args, **kwargs):
        self.callback = callback
        self.company_entry = None
        self.bin_entry = None
        self.email_entry = None
        self.phone_entry = None
        self.current_values = values
        super().__init__(parent, *args, **kwargs)
        self.create_change_window()

    def create_change_window(self):
        self.grab_set()
        self.focus_set()
        self.title('Редактирование Компании')
        self.geometry("430x170")
        self.bind('<Button-1>', lambda event: self.set_focus(event))

        company_label = ttk.Label(self, text="Компания:")
        company_label.grid(column=0, row=0, padx=(10, 5), pady=(10, 0), sticky='e')

        self.company_entry = HelperEntry(self, helper_text='Название')
        self.company_entry.set_text(self.current_values[0])
        self.company_entry.grid(column=1, row=0, padx=(5, 5), pady=(10, 0), sticky='w')

        self.bin_entry = HelperEntry(self, helper_text='БИН')
        self.bin_entry.set_text(self.current_values[1])
        self.bin_entry.grid(column=2, row=0, padx=(0, 5), pady=(10, 0), sticky='w')

        contacts_label = ttk.Label(self, text='Контакты:')
        contacts_label.grid(column=0, row=1, padx=(10, 5), pady=(10, 35), sticky='e')

        self.email_entry = HelperEntry(self, helper_text='Email')
        self.email_entry.set_text(self.current_values[2])
        self.email_entry.grid(column=1, row=1, padx=(5, 0), pady=(10, 35), sticky='w')

        self.phone_entry = HelperEntry(self, helper_text='Номер телефона')
        self.phone_entry.set_text(self.current_values[3])
        self.phone_entry.grid(column=2, row=1, padx=(0, 5), pady=(10, 35), sticky='w')

        cancel_button = ttk.Button(self, text='Отмена', command=self.destroy)
        cancel_button.grid(column=1, columnspan=2, row=2, sticky='e', padx=(0, 105))

        save_button = ttk.Button(self, text='Сохранить', command=lambda: self.change_company(), style='Accent.TButton')
        save_button.grid(column=2, row=2, sticky='e', padx=5)

        delete_button = ttk.Button(self, text='Удалить', command=self.delete_company, width=0)
        delete_button.grid(column=0, row=2, sticky='w', padx=15)

    def change_company(self):
        if self.varify_new_changes():
            self.change_data()
            self.callback()
            self.destroy()

    def set_focus(self, event):
        if event.widget == self:
            self.focus_set()

    def varify_new_changes(self):
        if self.company_entry.get() == self.company_entry.helper_text:
            messagebox.showerror("Пустое поле", "Пожалуйста, введите название Компании")
            return False

        if self.bin_entry.get() == self.bin_entry.helper_text:
            messagebox.showerror("Пустое поле", "Пожалуйста, введите БИН компании")
            return False

        if self.email_entry.get() == self.email_entry.helper_text:
            messagebox.showerror("Пустое поле", "Пожалуйста, введите Email")
            return False

        if self.phone_entry.get() == self.phone_entry.helper_text:
            messagebox.showerror("Пустое поле", "Пожалуйста, введите Номер Телефона")
            return False

        try:
            int(self.bin_entry.get())
        except ValueError:
            messagebox.showerror("Недопустимое значение", "БИН компании должен быть числом")
            return False

        return True

    def change_data(self):
        db_commit('''update company
set Company_name = %s, Company_BIN = %s, email = %s, Phone_number = %s
where Company_name = %s and  Company_BIN = %s and email = %s and  Phone_number = %s''',
                  (self.company_entry.get(), self.bin_entry.get(), self.email_entry.get(), self.phone_entry.get(),
                   self.current_values[0], self.current_values[1], self.current_values[2], self.current_values[3]))

    def delete_company(self):
        company_applications, _ = db_select('''select ta.Company_id
from transport_applications as ta
inner join company c on ta.Company_id = c.Company_id
where Company_BIN = %s''', (self.current_values[1],))
        if company_applications:
            warnings_window = tkinter.messagebox.askquestion('Удаление Заявки', "Все Заявки от этой компании будут удалены из базы данных.\nПродолжить?", icon='warning')
            if warnings_window == 'yes':
                db_commit('''delete ta
from transport_applications as ta
inner join company c on ta.Company_id = c.Company_id
where Company_BIN = %s''', (self.current_values[1],))
                db_commit('''delete from company
where Company_BIN = %s''', (self.current_values[1],))
                self.callback()
                self.destroy()
        else:
            question_window = tkinter.messagebox.askquestion('Удаление Компании',
                                                             "Вы уверены?",
                                                             icon='question')
            if question_window == 'yes':
                db_commit('''delete from company
            where Company_BIN = %s''', (self.current_values[1],))
                self.callback()
                self.destroy()
