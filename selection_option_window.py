import tkinter
from tkinter import ttk
from smh import *
from myscrollableframe import *


class SelectionOptionWindow(tkinter.Toplevel):

    def __init__(self, root, variables, callback, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        self.variables_text = variables
        self.variables_state = [tkinter.BooleanVar(value=True) for _ in range(len(variables))]
        self.callback = callback
        self.scroll_frame = None
        self.create_selection_window()

    def create_selection_window(self):
        self.overrideredirect(True)
        self.bind("<FocusOut>", lambda event: event_window_loss_focus(event, self.hide_window))

        selection_frame = ttk.LabelFrame(self, labelwidget=ttk.Frame(self))
        selection_frame.pack(fill='both', expand=True)

        self.withdraw()

        select_all_button = ttk.Button(selection_frame, text='Выбрать Все', command=self.select_all_button)
        select_all_button.pack(anchor='w')

        self.scroll_frame = ScrollableFrame(self)
        self.scroll_frame.pack(fill='both', expand=True)

        self.fill_selection_window()

    def fill_selection_window(self):
        for widget in self.scroll_frame.interior.winfo_children():
            widget.destroy()

        for i, var_str in enumerate(self.variables_text):
            selection_checkbox = ttk.Checkbutton(self.scroll_frame.interior, text=var_str,
                                                 variable=self.variables_state[i], command=self.checkbox_state_change)
            selection_checkbox.grid(column=0, row=i, sticky='w')
            self.scroll_frame.event_canvas_configure()

    def hide_window(self):
        self.withdraw()

    def show_window(self, event):
        x = event.widget.winfo_rootx()
        y = event.widget.winfo_rooty()

        self.focus_set()
        self.geometry(f"{200}x{200}+{x + 12}+{y + 28}")
        self.deiconify()

    def select_all_button(self):
        for variable in self.variables_state:
            variable.set(True)
        self.checkbox_state_change()

    def checkbox_state_change(self):
        self.callback()

    def check_selected_variable(self, variable):
        return variable in [s for s, b in zip(self.variables_text, [var.get() for var in self.variables_state]) if b]

    def update_values(self, new_variables_text):
        new_variables_state = []
        for item in new_variables_text:
            if item in self.variables_text:
                index = self.variables_text.index(item)
                new_variables_state.append(self.variables_state[index])
            else:
                new_variables_state.append(tkinter.BooleanVar(value=True))
        self.variables_state = new_variables_state
        self.variables_text = new_variables_text

        self.fill_selection_window()


