import tkinter

from SearchCombobox import *
from calendar_entry import *
from smh import *
from tkinterdnd2 import *
from tkinter import filedialog
import os
from tkinter import messagebox
from datetime import datetime


class ChangeApplicationWindow(tkinter.Toplevel):
    def __init__(self, parent, values, callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        query = '''SELECT Company_name, Company_BIN, application_date, car_number, freight_cost, sender_country, sender_city, recipint_country, recipint_city, SMR_path, application_path
FROM (
    SELECT
        c.Company_name,
        Company_BIN,
        application_date,
        car_number,
        freight_cost,
        senders_country.country_name as sender_country,
        senders_city.city_name as sender_city,
        recipients_country.country_name as recipint_country,
        recipients_city.city_name as recipint_city,
        CONCAT(senders_country.country_name, ', ', senders_city.city_name) AS senders_address,
        CONCAT(recipients_country.country_name, ', ', recipients_city.city_name) AS recipients_address,
        SMR_path,
        application_path
    FROM
        transport_applications AS ta
        INNER JOIN company c ON ta.Company_id = c.Company_id
        INNER JOIN cars c2 ON ta.Car_id = c2.car_id
        JOIN cities senders_city ON senders_city.city_id = ta.senders_city_id
        JOIN countries senders_country ON senders_city.country_id = senders_country.country_id
        JOIN cities recipients_city ON recipients_city.city_id = ta.recipients_city_id
        JOIN countries recipients_country ON recipients_city.country_id = recipients_country.country_id
) AS table_alias

where Company_BIN = %s and application_date = %s and car_number = %s and freight_cost = %s and senders_address = %s and recipients_address = %s and SMR_path = %s and application_path = %s '''
        self.current_values, _ = db_select(query, (
            values[1], datetime.strptime(values[2], '%d.%m.%Y'), values[3], values[4], values[5], values[6], values[7],
            values[8]))
        self.callback = callback
        self.sender_country_searchbox = None
        self.sender_city_searchbox = None
        self.recipient_city_searchbox = None
        self.recipient_country_searchbox = None
        self.cost_entry = None
        self.car_searchbox = None
        self.date_entry = None
        self.bin_searchbox = None
        self.company_searchbox = None
        self.SMR_file_path = values[7]
        self.application_file_path = values[8]
        self.create_change_window()

    def create_change_window(self):
        self.grab_set()
        self.focus_set()
        self.title('Change Application')
        self.geometry("500x500")
        self.bind('<Button-1>', lambda event: self.set_focus(event))

        SMR_file_name = tkinter.StringVar(value=os.path.basename(self.current_values[0][9]))
        application_file_name = tkinter.StringVar(value=os.path.basename(self.current_values[0][10]))

        company_values, company_label_text = db_select('''select distinct Company_name as "Company:" from company''')
        company_label = ttk.Label(self, text="Company:")
        company_label.grid(column=0, row=0, padx=(10, 5), pady=(10, 0), sticky='e')
        self.company_searchbox = SearchCombobox(self, values=["".join(value) for value in company_values],
                                                helper_text='Name')
        self.company_searchbox.set_text(self.current_values[0][0])
        self.company_searchbox.grid(column=1, row=0, padx=(5, 0), pady=(10, 0), sticky='w')

        bin_values, _ = db_select('''select distinct Company_BIN from company''')
        self.bin_searchbox = SearchCombobox(self, values=[value[0] for value in bin_values], helper_text='BIN')
        self.bin_searchbox.set_text(self.current_values[0][1])
        self.bin_searchbox.grid(column=2, row=0, padx=(0, 5), pady=(10, 0), sticky='w')

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
        self.date_entry.textvariable.set(self.current_values[0][2].strftime("%d.%m.%Y"))
        self.date_entry.date_label.configure(foreground='#000000')
        self.date_entry.grid(column=1, row=1, sticky='w', padx=5, pady=(5, 0))

        car_values, car_label_text = db_select('''select distinct car_number as "Car Number:" from cars''')
        car_label = ttk.Label(self, text=car_label_text[0])
        car_label.grid(column=0, row=3, padx=(10, 5), sticky='e', pady=(5, 0))
        self.car_searchbox = SearchCombobox(self, values=["".join(value) for value in car_values])
        self.car_searchbox.set_text(self.current_values[0][3])
        self.car_searchbox.grid(column=1, row=3, sticky='w', padx=5, pady=(5, 0))

        cost_label = ttk.Label(self, text='Freight cost:')
        cost_label.grid(column=0, row=4, padx=(10, 5), sticky='e', pady=(5, 0))
        self.cost_textvar = tkinter.StringVar(value=self.current_values[0][4])
        self.cost_entry = ttk.Entry(self, textvariable=self.cost_textvar)
        self.cost_entry.grid(column=1, row=4, sticky='w', padx=5, pady=(5, 0))

        country_values, _ = db_select('''select distinct country_name from countries''')
        city_values, _ = db_select('''select distinct city_name from cities''')

        sender_label = ttk.Label(self, text="Sender:")
        sender_label.grid(column=0, row=5, padx=(10, 5), sticky='e', pady=(5, 0))
        self.sender_country_searchbox = SearchCombobox(self, values=["".join(value) for value in country_values],
                                                       helper_text='Country')
        self.sender_country_searchbox.set_text(self.current_values[0][5])
        self.sender_country_searchbox.grid(column=1, row=5, padx=(5, 0), sticky='w', pady=(5, 0))
        self.sender_city_searchbox = SearchCombobox(self, values=["".join(value) for value in city_values],
                                                    helper_text='City')
        self.sender_city_searchbox.set_text(self.current_values[0][6])
        self.sender_city_searchbox.grid(column=2, row=5, sticky='w', pady=(5, 0))

        recipient_label = ttk.Label(self, text="Recipient:")
        recipient_label.grid(column=0, row=6, padx=(10, 5), sticky='e', pady=(5, 0))
        self.recipient_country_searchbox = SearchCombobox(self, values=["".join(value) for value in country_values],
                                                          helper_text='Country')
        self.recipient_country_searchbox.set_text(self.current_values[0][7])
        self.recipient_country_searchbox.grid(column=1, row=6, padx=(5, 0), sticky='w', pady=(5, 0))
        self.recipient_city_searchbox = SearchCombobox(self, values=["".join(value) for value in city_values],
                                                       helper_text='City')
        self.recipient_city_searchbox.set_text(self.current_values[0][8])
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
        cancel_button.grid(column=1, columnspan=2, row=9, sticky='e', padx=85)

        save_button = ttk.Button(self, text="Save", command=lambda: self.change_application(), style='Accent.TButton')
        save_button.grid(column=2, columnspan=2, row=9, sticky='e', padx=5)

        delete_button = ttk.Button(self, text='Delete', command=self.delete_application, width=0)
        delete_button.grid(column=0, row=9, sticky='w', padx=15)

    def set_focus(self, event):
        if event.widget == self:
            self.focus_set()

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

    def change_application(self):
        if self.varify_new_changes():
            self.change_data()
            self.callback()
            self.destroy()

    def delete_application(self):
        db_commit('''delete from transport_applications
where Company_id = (select Company_id from company where Company_BIN=%s) and
      Car_id = (select Car_id from cars where car_number=%s) and
      application_date = %s and freight_cost = %s and
      senders_city_id = (select city_id from cities where city_name = %s) and
      recipients_city_id = (select city_id from cities where city_name = %s) and
      SMR_path = %s and  application_path = %s''',
                  (self.current_values[0][1], self.current_values[0][3], self.current_values[0][2],
                   self.current_values[0][4], self.current_values[0][6], self.current_values[0][8],
                   self.current_values[0][9], self.current_values[0][10]))
        self.callback()
        self.destroy()

    def varify_new_changes(self):
        if self.company_searchbox.get() not in self.company_searchbox.values:
            messagebox.showerror("Invalid entry", "Please, select new Company name from list")
            return False
        try:
            if int(self.bin_searchbox.get()) not in self.bin_searchbox.values:
                messagebox.showerror("Invalid entry", "Please, select new BIN name from list")
                return False
        except ValueError:
            messagebox.showerror("Wrong data type", "BIN must be a number")

        if self.date_entry.textvariable.get() == self.date_entry.helper_text:
            messagebox.showerror("Empty entry", "Please, select new Application's Date")
            return False

        if self.car_searchbox.get() not in self.car_searchbox.values:
            messagebox.showerror("Invalid entry", "Please, select new Car's Number name from list")
            return False

        if self.cost_entry.get() == "":
            messagebox.showerror("Empty entry", "Please, type new freight cost")
            return False

        if self.sender_country_searchbox.get() not in self.sender_country_searchbox.values:
            messagebox.showerror("Invalid entry", "Please, select Sender's Country from list")
            return False

        if self.sender_city_searchbox.get() not in self.sender_city_searchbox.values:
            messagebox.showerror("Invalid entry", "Please, select Sender's City from list")
            return False

        if self.recipient_country_searchbox.get() not in self.recipient_country_searchbox.values:
            messagebox.showerror("Invalid entry", "Please, select Recipient's Country from list")
            return False

        if self.recipient_city_searchbox.get() not in self.recipient_city_searchbox.values:
            messagebox.showerror("Invalid entry", "Please, select Recipient's City from list")
            return False

        if self.SMR_file_path is None or self.SMR_file_path == '':
            messagebox.showerror("No path found", "Please, select SMR file path")
            return False

        if self.application_file_path is None or self.application_file_path == '':
            messagebox.showerror("No path found", "Please, select Application file path")
            return False

        return True

    def change_data(self):
        new_s_country = self.sender_country_searchbox.textvariable.get()
        new_s_city = self.sender_city_searchbox.textvariable.get()
        new_r_country = self.recipient_country_searchbox.textvariable.get()
        new_r_city = self.recipient_city_searchbox.textvariable.get()
        new_car = self.car_searchbox.textvariable.get()
        new_date = datetime.strptime(self.date_entry.textvariable.get(), "%d.%m.%Y").date()
        new_smr = self.SMR_file_path
        new_appl = self.application_file_path
        new_company = self.company_searchbox.textvariable.get()
        new_cost = self.cost_entry.get()

        db_commit('''update transport_applications as ta
inner join company c on ta.Company_id = c.Company_id
inner join cars c2 on ta.Car_id = c2.car_id
join cities as sender_city on senders_city_id = sender_city.city_id
join cities as recipient_city on recipients_city_id = recipient_city.city_id,
(select Company_id from company where Company_name=%s) as comp,
(select Car_id from cars where  car_number=%s) as car,
(select city_id from cities where  city_name=%s) as s_city,
(select city_id from cities where city_name=%s) as r_city
set ta.Company_id = comp.Company_id, ta.application_date = %s, ta.freight_cost = %s, ta.Car_id = car.car_id, senders_city_id = s_city.city_id,
    recipients_city_id = r_city.city_id, SMR_path = %s, application_path = %s
where Company_BIN = %s and application_date = %s and car_number = %s and freight_cost = %s and
      sender_city.city_name = %s and recipient_city.city_name = %s and SMR_path = %s and application_path = %s''',
                  (new_company, new_car, new_s_city, new_r_city, new_date, new_cost, new_smr, new_appl,
                   self.current_values[0][1], self.current_values[0][2], self.current_values[0][3],
                   self.current_values[0][4], self.current_values[0][6], self.current_values[0][8],
                   self.current_values[0][9], self.current_values[0][10]))
