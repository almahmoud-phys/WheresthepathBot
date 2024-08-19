import tkinter as tk
from tkinter import simpledialog

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
