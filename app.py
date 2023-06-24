from applications_frame import *
from companies_frame import *
from tkinterdnd2 import *

class App():
    root = TkinterDnD.Tk()
    style = ttk.Style(root)
    root.tk.call('source', '..\\aplications_DB\\Forest-ttk-theme-master\\forest-light.tcl')
    style.theme_use("forest-light")

    root.state('zoomed')

    def __init__(self):
        self.root.title('AAAAAAAAAAAAAAAAAAAAAAAAAAA')
        self.root.geometry("1000x500")

    def main_window(self):
        self.root.rowconfigure(0)
        tabs = ttk.Notebook(self.root, height=0)
        tabs.pack(expand=True, fill='both', pady=(10, 10), padx=(10, 10))

        applications_frame = ApplicationFrame(tabs)
        companies_frame = CompaniesFrame(tabs)

        applications_frame.pack(fill='both', expand=True)
        companies_frame.pack(fill='both', expand=True)

        tabs.add(applications_frame, text='Applications')
        tabs.add(companies_frame, text='Companies')

        applications_frame.fill_frame(self.root)

        tabs.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        self.root.mainloop()

    def on_tab_changed(self, event):
        selected_tab = event.widget.tab(event.widget.select(), "text")
        selected_index = event.widget.index(event.widget.select())
        print("Selected Tab:", selected_tab)
        print("Selected Index:", selected_index)
        # Access the tab object
        tab_object = event.widget.nametowidget(event.widget.select())
        print("Selected Tab Object:", tab_object)