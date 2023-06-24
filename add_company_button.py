from myaddbutton import *
from smh import *
from tkinter import messagebox
from Helper_entry import *


class AddCompanyButton(MyAddButton):
    def __init__(self, parent, callback, *args, **kwargs):
        self.callback = callback
        self.company_entry = None
        self.bin_entry = None
        self.email_entry = None
        self.phone_entry = None
        super().__init__(parent, *args, **kwargs, command=lambda: self.create_add_window(parent))

    def create_add_window(self, parent):
        add_window = tkinter.Toplevel(parent.winfo_toplevel())
        add_window.grab_set()
        add_window.focus_set()
        add_window.title('Add New Company')
        add_window.geometry("430x170")
        add_window.bind('<Button-1>', lambda event: self.add_window_set_focus(event, add_window))

        company_label = ttk.Label(add_window, text="Company:")
        company_label.grid(column=0, row=0, padx=(10, 5), pady=(10, 0), sticky='e')

        self.company_entry = HelperEntry(add_window, helper_text='Name')
        self.company_entry.grid(column=1, row=0, padx=(5, 5), pady=(10, 0), sticky='w')

        self.bin_entry = HelperEntry(add_window, helper_text='BIN')
        self.bin_entry.grid(column=2, row=0, padx=(0, 5), pady=(10, 0), sticky='w')

        contacts_label = ttk.Label(add_window, text='Contacts:')
        contacts_label.grid(column=0, row=1, padx=(10, 5), pady=(10, 35), sticky='e')

        self.email_entry = HelperEntry(add_window, helper_text='Email')
        self.email_entry.grid(column=1, row=1, padx=(5, 0), pady=(10, 35), sticky='w')

        self.phone_entry = HelperEntry(add_window, helper_text='Phone number')
        self.phone_entry.grid(column=2, row=1, padx=(0, 5), pady=(10, 35), sticky='w')

        cancel_button = ttk.Button(add_window, text='Cancel', command=add_window.destroy)
        cancel_button.grid(column=1, columnspan=2, row=2, sticky='e', padx=(0, 105))

        add_button = ttk.Button(add_window, text='Add', command=lambda: self.add_company(add_window),
                                style='Accent.TButton')
        add_button.grid(column=2, row=2, sticky='e', padx=5)

    def add_company(self, add_window):
        if self.varify_new_company():
            self.commit_new_data()
            self.callback()
            add_window.destroy()

    def varify_new_company(self):
        if self.company_entry.get() == self.company_entry.helper_text:
            messagebox.showerror("Empty entry", "Please, type Company name")
            return False

        if self.bin_entry.get() == self.bin_entry.helper_text:
            messagebox.showerror("Empty entry", "Please, type Company's BIN")
            return False

        if self.email_entry.get() == self.email_entry.helper_text:
            messagebox.showerror("Empty entry", "Please, type Email")
            return False

        if self.phone_entry.get() == self.phone_entry.helper_text:
            messagebox.showerror("Empty entry", "Please, type Phone number")
            return False

        try:
            int(self.bin_entry.get())
        except ValueError:
            messagebox.showerror("Invalid value", "Company's BIN must be a number")
            return False

        return True

    def commit_new_data(self):
        db_commit('''insert into company (Company_name, Company_BIN, email, Phone_number) values (%s, %s, %s, %s)''',
                  (self.company_entry.get(), self.bin_entry.get(), self.email_entry.get(), self.phone_entry.get()))
