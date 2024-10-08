import tkinter as tk
from tkinter import messagebox, simpledialog

import arabic_reshaper
from bidi.algorithm import get_display


class SingleChoiceDialog(simpledialog.Dialog):
    def __init__(self, parent, title, options):
        self.options = options
        self.choice = None
        super().__init__(parent, title=title)

    def body(self, master):
        tk.Label(master, text="Please choose an option:").grid(
            row=0, column=0, columnspan=2
        )

        self.var = tk.StringVar(value=self.options[0])
        for idx, option in enumerate(self.options):
            tk.Radiobutton(master, text=option, variable=self.var, value=option).grid(
                row=idx + 1, column=0, sticky="w"
            )

        return None  # No initial focus

    def apply(self):
        self.choice = self.var.get()


class Arabic:
    def display_arabic_text(text):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text


def show_info(msg : str):
    messagebox.showinfo("Information", msg)


def show_warning():
    messagebox.showwarning("Warning", "This is a warning message.")


def show_error():
    messagebox.showerror("Error", "This is an error message.")


def confirm_action():
    result = messagebox.askyesno("Confirm", "Are you sure you want to proceed?")
    if result:
        messagebox.showinfo("Confirmed", "You selected Yes.")
    else:
        messagebox.showinfo("Cancelled", "You selected No.")
