import copy

from myframe import *
from database import *
from mytableframe import *
import tkinter
from tkinter import ttk
from selection_option_window import *
from smh import *
from selection_date_window import *
from myscrollableframe import *


class TableFrame(MyTableFrame):
    def __init__(self, parent, root, weights, checkbox_columns_index, date_column_index, file_column_index,
                 mysql_request, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.root = root
        self.weights = weights
        self.my_sql_request = mysql_request
        self.checkbox_columns_index = checkbox_columns_index
        self.date_column_index = date_column_index
        self.file_column_index = file_column_index
        self.table_data, self.column_names = db_select(mysql_request)
        self.selected_table_data, _ = db_select(mysql_request)
        self.list_column_widgets = [0] * (len(date_column_index) + len(checkbox_columns_index))
        self.list_selection_window = [0] * (len(date_column_index) + len(checkbox_columns_index))
        self.list_label_point = [0] * (len(date_column_index) + len(checkbox_columns_index))
        self.list_label_arrow = [0] * (len(date_column_index) + len(checkbox_columns_index))
        self.create_table_frame()
        self.create_selection_windows()

    def create_table_frame(self):
        # Gray row for columns
        background_frame = tkinter.Frame(self, bg='#CCCCCC')
        background_frame.grid(column=0, row=0, columnspan=9, sticky='news')

        # Add weight for TABLE Frame taking all main frame space
        self.grid_columnconfigure(0, weight=1)

        # Create and fill grid columns and cells with text of TABLE Form
        for i in self.checkbox_columns_index:
            self.columnconfigure(i, weight=self.weights[i])

            column_frame = tkinter.Frame(self, bg='#CCCCCC')
            column_frame.grid(column=i, row=0, pady=(5, 5), sticky='ew')

            label_column_name = tkinter.Label(column_frame, text=self.column_names[i], background='#CCCCCC', anchor='w')
            label_column_name.grid(column=0, row=0, sticky='w')
            label_column_name.bind("<Button-1>", lambda event, frame=self: self.event_click_column_header(event, frame))
            self.list_column_widgets[i] = label_column_name

            label_arrow = tkinter.Label(column_frame, text="○", background='#CCCCCC', font=('Arial', 12))
            label_arrow.grid(column=1, row=0, sticky='w')
            self.list_label_point[i] = label_arrow

        # Create and fill grid columns with files of TABLE Form
        for i in self.file_column_index:
            self.columnconfigure(i, weight=self.weights[i])
            label = tkinter.Label(self, text=self.column_names[i], background='#CCCCCC')
            label.grid(column=i, row=0, pady=(5, 5), sticky='ew')
            label.bind("<Button-1>", lambda event, frame=self: frame.on_click_row_selection(event))

        for i in self.date_column_index:
            self.columnconfigure(i, weight=self.weights[i])

            column_frame = tkinter.Frame(self, bg='#CCCCCC')
            column_frame.grid(column=i, row=0, pady=(5, 5), sticky='ew')

            label_column_name = tkinter.Label(column_frame, text=self.column_names[i], background='#CCCCCC', anchor='w')
            label_column_name.grid(column=0, row=0, sticky='w')
            label_column_name.bind("<Button-1>", lambda event, frame=self: self.event_click_column_header(event, frame))
            self.list_column_widgets[i] = label_column_name

            label_arrow = tkinter.Label(column_frame, text="○", background='#CCCCCC', font=('Arial', 12))
            label_arrow.grid(column=1, row=0, sticky='w')
            self.list_label_point[i] = label_arrow

            label_arrow = tkinter.Label(column_frame, text="−", background='#CCCCCC', font=('Arial', 12))
            label_arrow.grid(column=2, row=0, sticky='w')
            label_arrow.bind('<Button-1>', self.event_arrow_click)
            self.list_label_arrow[i] = label_arrow
        self.fill_table_rows()

    def fill_table_rows(self):
        sorted_select_data = self.selected_table_data[:]
        for i in self.date_column_index:
            sorted_select_data = self.sort_table_by_date(sorted_select_data, i)

        for i in self.checkbox_columns_index:
            for j in range(len(sorted_select_data)):
                label = tkinter.Label(self, text=sorted_select_data[j][i], height=1, anchor='w')
                label.grid(column=i, row=j + 1, sticky='ew')
                label.bind("<Button-1>", lambda event, frame=self: frame.on_click_row_selection(event))

        # Date column
        for i in self.date_column_index:
            for j in range(len(sorted_select_data)):
                label = tkinter.Label(self, text=sorted_select_data[j][i].strftime("%d.%m.%Y"), height=1,
                                      anchor='w')
                label.grid(column=i, row=j + 1, sticky='ew')
                label.bind("<Button-1>", lambda event, frame=self: frame.on_click_row_selection(event))

        # Create and fill cells with files, add buttons for opening files
        for i in self.file_column_index:
            for j in range(len(sorted_select_data)):
                button = tkinter.Button(self, text='📄',
                                        command=lambda file_path=sorted_select_data[j][i]: open_file(file_path),
                                        highlightthickness=0, bd=0, height=1)
                button.grid(column=i, row=j + 1, sticky='ew')

    def create_selection_windows(self):
        for i in self.checkbox_columns_index:
            variables = get_unique_val_column(self.table_data, self.list_column_widgets[i].master.grid_info()['column'])
            selection_window = SelectionOptionWindow(self.root, variables,
                                                     callback=lambda index=i: self.selection_option_window_callback(
                                                         index))
            self.list_selection_window[i] = selection_window

        # Create date selection window
        for i in self.date_column_index:
            selection_window = SelectionDateWindow(self.root,
                                                   callback=lambda index=i: self.selection_date_window_callback(index))
            self.list_selection_window[i] = selection_window

    def selection_option_window_callback(self, index):
        if all(state.get() for state in self.list_selection_window[index].variables_state):
            self.list_label_point[index].configure(text="○")
        else:
            self.list_label_point[index].configure(text="●")
        self.update_table_frame()

    def selection_date_window_callback(self, index):
        helper_text = self.list_selection_window[index].unselected_date_value
        if all(entry.textvariable.get() == helper_text for entry in self.list_selection_window[index].list_date_entry):
            self.list_label_point[index].configure(text="○")
        else:
            self.list_label_point[index].configure(text="●")
        self.update_table_frame()

    def update_table_frame(self):
        self.clear_table_rows()

        self.selected_table_data = []
        for row in self.table_data:
            if all(self.list_selection_window[column_index].check_selected_variable(row[column_index]) for column_index
                   in range(len(self.list_selection_window))):
                self.selected_table_data.append(row)

        self.fill_table_rows()

    def clear_table_rows(self):
        total_rows = self.grid_size()[1]
        for row in range(1, total_rows):
            for column, widget in enumerate(self.grid_slaves(row=row)):
                widget.destroy()
            self.grid_rowconfigure(row, weight=0)

    def update_data(self, new_data):
        self.table_data = new_data
        for i in self.checkbox_columns_index:
            variables = get_unique_val_column(self.table_data, self.list_column_widgets[i].master.grid_info()['column'])
            self.list_selection_window[i].update_values(variables)

        self.update_table_frame()

    def event_click_column_header(self, event, column_header_frame):
        column_header_frame.on_click_row_selection(event)
        self.list_selection_window[event.widget.master.grid_info()['column']].show_window(event)

    def sort_table_by_date(self, selected_date, column_index):
        arrow_value = self.list_label_arrow[column_index].cget('text')
        if arrow_value == '⋀':
            return sorted(selected_date, key=lambda x: x[column_index], reverse=True)
        elif arrow_value == '⋁':
            return sorted(selected_date, key=lambda x: x[column_index])
        return selected_date

    def event_arrow_click(self, event):
        arrow_value = event.widget.cget('text')
        if arrow_value == '−':
            event.widget.configure(text='⋀')
        elif arrow_value == '⋀':
            event.widget.configure(text='⋁')
        else:
            event.widget.configure(text='−')

        self.clear_table_rows()
        self.fill_table_rows()
