from database import *
import os
import subprocess
from tkinter import messagebox


def get_unique_val_column(data, i):
    set_val = set()
    for row in data:
        set_val.add(row[i])
    return list(reversed(list(set_val)))


def scroll_canvas(event, canvas):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def db_select(mysql_request, values=None):
    cursor = applications_db.cursor()
    if values is None:
        cursor.execute(mysql_request)
    else:
        cursor.execute(mysql_request, values)
    data = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    return data, columns


def db_commit(mysql_request, values):
    cursor = applications_db.cursor()
    cursor.execute(mysql_request, values)
    applications_db.commit()

def open_file(file_path):
    if os.path.isfile(file_path):
        try:
            os.startfile(file_path)
        except subprocess.CalledProcessError:
            messagebox.showinfo("Failed to open the file.")
    else:
        messagebox.showerror("File Not Found", f"The file '{file_path}' doesn't exist!")


def event_window_loss_focus(event, loss_focus_True_callback):
    print(f'Focused widget: {event.widget.focus_get()}')
    print(f'Widget that lost focus: {event.widget}')
    if event.widget.winfo_toplevel().focus_get() is None:
        loss_focus_True_callback()

