from myaddbutton import *
from SearchCombobox import *
from calendar_entry import *
from smh import *
from tkinterdnd2 import *
from tkinter import filedialog
import os
from tkinter import messagebox
from datetime import datetime
from add_company_button import *


class AddApplicationButton(MyAddButton):
    def __init__(self, parent, callback, *args, **kwargs):
        self.sender_country_searchbox = None
        self.sender_city_searchbox = None
        self.recipient_city_searchbox = None
        self.recipient_country_searchbox = None
        self.cost_entry = None
        self.car_searchbox = None
        self.date_entry = None
        self.bin_searchbox = None
        self.company_searchbox = None
        self.SMR_file_path = None
        self.application_file_path = None
        self.callback = callback
        super().__init__(parent, *args, **kwargs, command=lambda: self.create_add_window(parent))

    def create_add_window(self, parent):
        add_window = tkinter.Toplevel(parent.winfo_toplevel())
        add_window.grab_set()
        add_window.focus_set()
        add_window.title('Add New Application')
        add_window.geometry("500x450")
        add_window.bind('<Button-1>', lambda event: self.add_window_set_focus(event, add_window))

        SMR_file_name = tkinter.StringVar()
        application_file_name = tkinter.StringVar()

        company_values, _ = db_select('''select distinct Company_name from company''')
        company_label = ttk.Label(add_window, text="Company:")
        company_label.grid(column=0, row=0, padx=(10, 5), pady=(10, 0), sticky='e')
        self.company_searchbox = SearchCombobox(add_window, values=["".join(value) for value in company_values],
                                                helper_text='Name')
        self.company_searchbox.grid(column=1, row=0, padx=(5, 0), pady=(10, 0), sticky='w')

        bin_values, _ = db_select('''select distinct Company_BIN from company''')
        self.bin_searchbox = SearchCombobox(add_window, values=[value[0] for value in bin_values], helper_text='BIN')
        self.bin_searchbox.grid(column=2, row=0, padx=(0, 5), pady=(10, 0), sticky='w')

        new_company_button = AddCompanyButton(parent=add_window, width=0, text='+', style='Accent.TButton',
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

        date_label = ttk.Label(add_window, text="Application date:")
        date_label.grid(column=0, row=1, padx=(10, 5), sticky='e', pady=(5, 0))
        self.date_entry = CalendarEntry(add_window, unselected_foreground_color='#c6c6c6',
                                        unselected_date_value='dd.mm.yyyy')
        self.date_entry.grid(column=1, row=1, sticky='w', padx=5, pady=(5, 0))

        car_values, car_label_text = db_select('''select distinct car_number as "Car Number:" from cars''')
        car_label = ttk.Label(add_window, text=car_label_text[0])
        car_label.grid(column=0, row=3, padx=(10, 5), sticky='e', pady=(5, 0))
        self.car_searchbox = SearchCombobox(add_window, values=["".join(value) for value in car_values])
        self.car_searchbox.grid(column=1, row=3, sticky='w', padx=5, pady=(5, 0))

        cost_label = ttk.Label(add_window, text='Freight cost:')
        cost_label.grid(column=0, row=4, padx=(10, 5), sticky='e', pady=(5, 0))
        self.cost_entry = ttk.Entry(add_window)
        self.cost_entry.grid(column=1, row=4, sticky='w', padx=5, pady=(5, 0))

        country_values, _ = db_select('''select distinct country_name from countries''')
        city_values, _ = db_select('''select distinct city_name from cities''')

        sender_label = ttk.Label(add_window, text="Sender:")
        sender_label.grid(column=0, row=5, padx=(10, 5), sticky='e', pady=(5, 0))
        self.sender_country_searchbox = SearchCombobox(add_window, values=country_values, helper_text='Country')
        self.sender_country_searchbox.grid(column=1, row=5, padx=(5, 0), sticky='w', pady=(5, 0))
        self.sender_city_searchbox = SearchCombobox(add_window, values=city_values, helper_text='City')
        self.sender_city_searchbox.grid(column=2, row=5, sticky='w', pady=(5, 0))

        recipient_label = ttk.Label(add_window, text="Recipient:")
        recipient_label.grid(column=0, row=6, padx=(10, 5), sticky='e', pady=(5, 0))
        self.recipient_country_searchbox = SearchCombobox(add_window, values=country_values, helper_text='Country')
        self.recipient_country_searchbox.grid(column=1, row=6, padx=(5, 0), sticky='w', pady=(5, 0))
        self.recipient_city_searchbox = SearchCombobox(add_window, values=city_values, helper_text='City')
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

        SMR_file_frame = ttk.LabelFrame(add_window, text='SMR', width=200, height=100)
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

        SMR_file_name_label = ttk.Label(add_window, textvariable=SMR_file_name, wraplength=200)
        SMR_file_name_label.grid(column=0, columnspan=2, row=8, sticky='nw', padx=(50, 0), pady=(0, 20))

        SMR_file_frame.bind('<Button-1>',
                            lambda event: self.set_select_file_explorer(event, SMR_file_name, self.set_SMR_file_path))
        SMR_file_text.bind('<Button-1>',
                           lambda event: self.set_select_file_explorer(event, SMR_file_name, self.set_SMR_file_path))

        application_file_frame = ttk.LabelFrame(add_window, text='Application', width=200, height=100)
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

        application_file_name_label = ttk.Label(add_window, textvariable=application_file_name, wraplength=200)
        application_file_name_label.grid(column=2, columnspan=2, row=8, sticky='nw', padx=(10, 0), pady=(0, 20))

        application_file_frame.bind('<Button-1>',
                                    lambda event: self.set_select_file_explorer(event, application_file_name,
                                                                                self.set_application_file_path))
        application_file_text.bind('<Button-1>',
                                   lambda event: self.set_select_file_explorer(event, application_file_name,
                                                                               self.set_application_file_path))

        cancel_button = ttk.Button(add_window, text="Cansel", command=add_window.destroy)
        cancel_button.grid(column=1, columnspan=2, row=9, sticky='e', padx=70)

        add_button = ttk.Button(add_window, text="Add", command=lambda: self.add_application(add_window),
                                style='Accent.TButton')
        add_button.grid(column=2, columnspan=2, row=9, sticky='e', padx=5)

    def set_drop_file_path(self, event, textvariable, file_path_set_func):
        files = self.winfo_toplevel().tk.splitlist(event.data)
        if len(files) != 1:
            messagebox.showerror("Multiple files selected", "Please, select or drag and drop one file")

        textvariable.set(os.path.basename(files[0]))
        file_path_set_func(files[0])

    def set_select_file_explorer(self, event, textvariable, file_path_set_func):
        file_path = filedialog.askopenfilename()
        textvariable.set(os.path.basename(file_path))
        file_path_set_func(file_path)
        event.widget.winfo_toplevel().focus_set()

    def set_SMR_file_path(self, value):
        self.SMR_file_path = value

    def set_application_file_path(self, value):
        self.application_file_path = value

    def fill_if_connected(self, textvariable, mysql_request, connected_searchbox):
        connected_value, _ = db_select(mysql_request, (textvariable.get(),))
        if connected_value:
            connected_searchbox.textvariable.set(connected_value[0][0])
            connected_searchbox.configure(foreground=connected_searchbox.default_color)
            connected_searchbox.current_color = connected_searchbox.default_color

    def add_application(self, add_window):
        if self.varify_new_application():
            self.commit_new_data()
            self.callback()
            add_window.destroy()

    def varify_new_application(self):
        if self.company_searchbox.textvariable.get() == self.company_searchbox.helper_text:
            messagebox.showerror("Empty entry", "Please, select Company name")
            return False

        if self.bin_searchbox.textvariable.get() == self.bin_searchbox.helper_text:
            messagebox.showerror("Empty entry", "Please, select Company BIN")
            return False

        connected_value, _ = db_select(
            '''select Company_id from company where Company_name = %s and Company_BIN = %s''',
            (self.company_searchbox.textvariable.get(), self.bin_searchbox.textvariable.get()))
        if not connected_value:
            messagebox.showerror("Entries not found", "Combination of BIN and Company name was not found")
            return False

        if self.date_entry.textvariable.get() == self.date_entry.helper_text:
            messagebox.showerror("Empty entry", "Please, select Application's Date")
            return False

        if self.car_searchbox.textvariable.get() == self.car_searchbox.helper_text:
            messagebox.showerror("Empty entry", "Please, select Car's Number or type a new one")
            return False

        if self.cost_entry.get() == "":
            messagebox.showerror("Empty entry", "Please, type freight cost")
            return False

        if self.sender_country_searchbox.textvariable.get() == self.sender_country_searchbox.helper_text:
            messagebox.showerror("Empty entry", "Please, select Sender's Country or type a new one")
            return False

        if self.sender_city_searchbox.textvariable.get() == self.sender_city_searchbox.helper_text:
            messagebox.showerror("Empty entry", "Please, select Sender's City or type a new one")
            return False

        if self.recipient_country_searchbox.textvariable.get() == self.recipient_country_searchbox.helper_text:
            messagebox.showerror("Empty entry", "Please, select Recipient's Country or type a new one")
            return False

        if self.recipient_city_searchbox.textvariable.get() == self.recipient_city_searchbox.helper_text:
            messagebox.showerror("Empty entry", "Please, select Recipient's City or type a new one")
            return False

        if self.SMR_file_path is None or self.SMR_file_path == '':
            messagebox.showerror("No path found", "Please, select SMR file path")
            return False

        if self.application_file_path is None or self.application_file_path == '':
            messagebox.showerror("No path found", "Please, select Application file path")
            return False

        return True

    def commit_new_data(self):
        s_country = self.sender_country_searchbox.textvariable.get()
        s_city = self.sender_city_searchbox.textvariable.get()
        r_country = self.recipient_country_searchbox.textvariable.get()
        r_city = self.recipient_city_searchbox.textvariable.get()
        car = self.car_searchbox.textvariable.get()
        date = datetime.strptime(self.date_entry.textvariable.get(), "%d.%m.%Y").date()
        smr = self.SMR_file_path
        appl = self.application_file_path
        company = self.company_searchbox.textvariable.get()
        cost = self.cost_entry.get()

        connected_value, _ = db_select('''select city_id from cities
                                        inner join countries c on cities.country_id = c.country_id
                                        where country_name = %s and city_name =%s''', (s_country, s_city))
        if not connected_value:
            city_values, _ = db_select('''select distinct city_name from cities where city_name=%s''', (s_city,))
            country_values, _ = db_select('''select distinct country_name from countries where country_name=%s''',
                                          (s_country,))

            if not country_values:
                db_commit('''insert into countries (country_name) values (%s)''', (s_country,))
            db_commit('''insert into cities (city_name, country_id)
                            select %s, country_id from countries where country_name = %s''', (s_city, s_country))

        connected_value, _ = db_select('''select city_id from cities
                                        inner join countries c on cities.country_id = c.country_id
                                        where country_name = %s and city_name =%s''', (r_country, r_city))
        if not connected_value:
            city_values, _ = db_select('''select distinct city_name from cities where city_name=%s''', (r_city,))
            country_values, _ = db_select('''select distinct country_name from countries where country_name=%s''',
                                          (r_country,))

            if not country_values:
                db_commit('''insert into countries (country_name) values (%s)''',
                          (r_country,))
            db_commit('''insert into cities (city_name, country_id)
                            select %s, country_id from countries where country_name = %s''',
                      (r_city, r_country))

        connected_value, _ = db_select('''select car_number from cars where car_number = %s''', (car,))
        if not connected_value:
            db_commit('''insert into cars (car_number) values (%s)''', (car,))

        db_commit('''insert into transport_applications (Company_id, application_date, Car_id, freight_cost, senders_city_id, recipients_city_id, SMR_path, application_path)
        select (select Company_id from company where Company_name = %s), %s, (select Car_id from cars where Car_number=%s), %s,
        (select City_id from cities where city_name=%s), (select City_id from cities where city_name=%s), %s, %s''',
                  (company, date, car, cost, s_city, r_city, smr, appl))

    def add_company_callback(self):
        old_company_values = self.company_searchbox.values
        old_bin_values = self.bin_searchbox.values

        new_company_values, _ = db_select('''select distinct Company_name from company''')
        self.company_searchbox.values_update(["".join(value) for value in new_company_values])

        new_bin_valies, _ = db_select('''select distinct Company_BIN from company''')
        self.bin_searchbox.values_update([value[0] for value in new_bin_valies])

        added_company = list(set(["".join(value) for value in new_company_values]) - set(old_company_values))[0]
        added_bin = list(set([value[0] for value in new_bin_valies]) - set(old_bin_values))[0]

        self.company_searchbox.textvariable.set(added_company)
        self.company_searchbox.configure(foreground=self.company_searchbox.default_color)
        self.company_searchbox.current_color = self.company_searchbox.default_color

        self.bin_searchbox.textvariable.set(added_bin)
        self.bin_searchbox.configure(foreground=self.bin_searchbox.default_color)
        self.bin_searchbox.current_color = self.bin_searchbox.default_color
