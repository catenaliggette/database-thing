from applications_frame import ApplicationFrame
from company_frame import CompanyFrame
from tkinterdnd2 import TkinterDnD
from tkinter import ttk
from cities_frame import CitiesFrame
from cars_frame import CarsFrame
import os


def on_tab_changed(event):
    tab_object = event.widget.nametowidget(event.widget.select())
    tab_object.new_data_select()


class App:
    root = TkinterDnD.Tk()
    style = ttk.Style(root)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    root.tk.call('source', 'forest-light.tcl')
    style.theme_use("forest-light")

    root.state('zoomed')
    root.option_add("*encoding", "utf-8")

    def __init__(self):
        self.root.title('а')
        self.root.geometry("1000x500")

    def main_window(self):
        self.root.rowconfigure(0)
        tabs = ttk.Notebook(self.root, height=0)
        tabs.pack(expand=True, fill='both', pady=(10, 10), padx=(10, 10))

        applications_frame = ApplicationFrame(tabs)
        companies_frame = CompanyFrame(tabs)
        cities_frame = CitiesFrame(tabs)
        cars_frame = CarsFrame(tabs)

        applications_frame.pack(fill='both', expand=True)
        companies_frame.pack(fill='both', expand=True)
        cities_frame.pack(fill='both', expand=True)
        cars_frame.pack(fill='both', expand=True)

        tabs.add(applications_frame, text='Заявки')
        tabs.add(companies_frame, text='Компании')
        tabs.add(cities_frame, text='Города')
        tabs.add(cars_frame, text='Автомобили')

        tabs.bind("<<NotebookTabChanged>>", on_tab_changed)

        self.root.mainloop()
