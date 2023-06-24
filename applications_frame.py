from table_frame import *
from add_application_button import *
from myscrollableframe import *


class ApplicationFrame(ttk.Frame):

    def fill_frame(self, root):
        self.root = root
        self.rowconfigure(1, weight=1)
        self.table_frame = TableFrame(self, root, labelwidget=ttk.Frame(), weights=[3, 3, 2, 3, 2, 4, 4, 1, 1],
                                 checkbox_columns_index=[0, 1, 3, 4, 5, 6], date_column_index=[2],
                                 file_column_index=[7, 8], mysql_request='''select c.Company_name, Company_BIN, application_date, car_number, freight_cost, CONCAT(senders_country.country_name, ', ', senders_city.city_name) as senders_adress, CONCAT(recipients_country.country_name, ', ',recipients_city.city_name) as recipients_adress, SMR_path, application_path
from transport_applications as ta
inner join company c on ta.Company_id = c.Company_id
inner join cars c2 on ta.Car_id = c2.car_id
join cities senders_city on senders_city.city_id = ta.senders_city_id
join countries senders_country on senders_city.country_id = senders_country.country_id
join cities recipients_city on recipients_city.city_id = ta.recipients_city_id
join countries recipients_country on recipients_city.country_id = recipients_country.country_id''')
        self.table_frame.grid(row=1, column=0, pady=(10, 10), sticky='news')

        # Create insert ADD button on main frame
        self.rowconfigure(0, weight=0)
        add_button = AddApplicationButton(parent=self, text='Add', style='Accent.TButton', callback=self.table_frame.update_data)
        add_button.grid(row=0, column=0, sticky='w')

        self.grid_columnconfigure(0, weight=1)