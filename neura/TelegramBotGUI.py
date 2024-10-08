#!/usr/bin/env python

import asyncio
import tkinter as tk
from tkinter import ttk

from tkinter import messagebox

# to test the gui without the full runing of the script , just run this file and it will work
# python TelegramBotGUI.py
##
if __name__ == "__main__":
    import sys
    sys.path.append("../")

import neura.Constants as Constants
from neura.TelegramBot import TelegramBot
from neura.utils import Arabic as ar
from async_tkinter_loop import async_handler


class TelegramBotGUI:
    def __init__(self, root, bot):
        """
        Initializes the TelegramBotGUI instance.

        :param root: The root Tkinter window.
        :param bot: An instance of the TelegramBotConfig class or None.
        """
        self.loop = asyncio.get_event_loop()
        # self.root = root

        if bot is not None:
            self.root = tk.Toplevel()
            self.config = bot.config
            self.group = bot.group
            self.admin = bot.admin
            self.users = bot.users
            self.bot = TelegramBot(self.admin, self.group, self.users)
        else:
            self.root = root
        title = ar.display_arabic_text("بوت برنامج أين الطريق")
        self.root.title(title)

        self.styles()
        self.create_widgets()

    def styles(self):
        """
        Initializes the styles for the application, including window size, grid configuration,
        and various color and font settings for widgets.
        """
        #TODO: we need a good lock and feel for the app
        # Set a minsize for the window, and place it in the middle
        self.root.update()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
        self.root.resizable(True, True)

        # Configure grid for responsiveness
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)

        self.primary_color = "#6200EE"  # Deep Purple 500
        self.primary_variant_color = "#3700B3"  # Deep Purple 700
        self.secondary_color = "#03DAC6"  # Teal 200
        self.background_color = "#ECEFF1"  # Grey 200 (New Background)
        self.text_primary_color = "#212121"  # Grey 900
        self.text_secondary_color = "#ECEFF1"  # Grey 600
        self.divider_color = "#BDBDBD"  # Grey 400

        # Apply general styles
        self.style = ttk.Style()
        self.style.configure(
            "TLabel",
            font=("Roboto", 14, "bold"),
            # foreground=self.text_primary_color,
            # background=self.background_color,
        )
        self.style.configure(
            "TButton",
            font=("Roboto", 12, "bold"),
            # foreground="#FFFFFF",
            background=self.primary_color,
            padding=10,
        )
        # self.style.map(
        #     "TButton",
        #     foreground=[("active", "#FFFFFF")],
        #     background=[("active", self.primary_variant_color)],
        # )

        self.style.configure("TCheckbutton",
                font=('Arial', 12),
                padding=6)
        self.style.configure("TSeparator", background=self.divider_color)

        # self.root.configure(bg=self.background_color)

    def create_widgets(self):
        """
        Initializes and arranges the main application widgets in the window.
        This includes labels, buttons, and separators.
        """
        #TODO : switch to tabs
        #TODO : add a menu bar
        #TODO : translate the text to arabic

        """
        Initializes the main application  widgets.
        """

        # Initialize row index
        self.row_index = 0

        # Top information widget
        self.create_info_label(
            # f"Group Name: {self.group.title} with {len(self.users)} users"
            "بوت برنامج أين الطريق"
        )

        # Separator between top info and first section
        self.create_separator()

        # First row: Users Management
        self.create_title("Users Management")

        self.create_button("معلومات المجموعة و أعضاء المجموعة", self.export_users, 0)

        self.row_index += 1
        # Separator between first and second section
        self.create_separator()

        # Second row: Send Bulk Messages
        self.create_title("Send Messages")
        self.create_button("إرسال رسائل للأعضاء", self.send_message, 0)

        self.row_index += 1
        # Separator between second and third section
        self.create_separator()

        # Third row: Group Call Attendance
        text = "تسجيل حضور المدارسة"
        self.create_title(text)
        self.create_button("تسجيل حضور المدارسة", self.take_presence, 0)

        self.row_index += 1

        # Separator before bottom buttons
        self.create_separator()

    # Button click handlers
    def export_users(self):
        """
        Handles exporting user information to an Excel file.
        Opens a new window to manage the export process.
        """
        #TODO: Create a new window for the task

        # reset the row index
        self.row_index = 0

        new_window = tk.Toplevel(self.root)

        # Content for the new window
        self.create_title("إستخراج معلومات الأعضاء" , new_window)

        # update the information label
        def on_update(result):
            information.config(text=ar.display_arabic_text(f"{result}"))
        # function to start the process
        def start():
            # update the information label
            information.config(text=ar.display_arabic_text("جاري العملية"))

            # start the process of taking the presence using the bot object and  async_handler to not block the main thread
            async_handler(self.bot.export_users(on_update ))

        self.row_index += 1
        self.create_button("Start", start, 0 , new_window)
        self.row_index += 1
        information = self.create_info_label("", new_window)
        pass

    def take_presence(self):
        """
        Handles recording the presence of users in a group call.
        Opens a new window to manage the presence-taking process.
        """
        # new windows
        new_window = tk.Toplevel(self.root)
        for i in range(2):
            new_window.grid_columnconfigure(i, weight=1)
        # Content for the new window
        self.create_title("تسجيل حضور المدارسة" , new_window)
        self.create_info_label("عدد الحاضرين للمدارسة", new_window)
        information = self.create_info_label("", new_window)

        # function to update the information label
        def on_update(result):
            information.config(text=ar.display_arabic_text(f"{result}"))

        # function to start the process
        def start():
            step = combobox.get()
            # start the process of taking the presence using the bot object and  async_handler to not block the main thread
            async_handler(self.bot.take_presence(step , on_update ))

        self.row_index += 6
        # Create the drop-down menu to choose the step number رقم المدارسة
        combobox = ttk.Combobox(new_window, values=[x for x in range(-1, 14)])
        combobox.set(ar.display_arabic_text("إختر رقم الخطوة"))  # Set default text
        combobox.grid(row=self.row_index, column=0, padx=10, pady=5,  sticky="ew")

        self.row_index += 1

        self.create_button("بدأ تسجيل الحضور", start, 0 , new_window)
        self.create_button("Stop",new_window.destroy, 1,new_window)

    def send_message(self):
        """
        Handles sending messages to multiple users.
        Opens a new window to input recipients and message content.
        """
        # Create a new window for the task
        new_window = tk.Toplevel(self.root)
        self.row_index = 0

        # Content for the new window
        for i in range(2):
            new_window.grid_columnconfigure(i, weight=1)
        self.create_title("إرسال رسالة" , new_window)
        self.create_label("Recipients (one per line):",1, 0, new_window)
        self.create_label("نص الرسالة",1, 1, new_window)

        send_to_all = tk.BooleanVar()
        send_to_mutual_contact = tk.BooleanVar()


        #function to update  recipients of the message when the checkbutton is clicked
        def update_list():
            if send_to_all.get():
                print(self.users)
                print(type(self.users))
                users_id = [f"@{self.users[id]["username"]}" for  id in self.users]
                recipient_text.delete("1.0", tk.END)
                recipient_text.insert(tk.END, "\n".join(users_id))
            elif send_to_mutual_contact.get():
                recipient_text.delete("1.0", tk.END)
                recipient_text.insert(tk.END, "\n".join(self.users))
        self.create_checkbutton("Send to All users",update_list, send_to_all,2,0, new_window)
        self.create_checkbutton("Send to safe users (safe from ban)",update_list,  send_to_mutual_contact,3,0, new_window)

        recipient_text = self.create_text(40, 10,4,  0, new_window)
        message_text = self.create_text(40, 10,4,  1, new_window)

        # callback function to update the information label
        def on_update(result):
            information.config(text=ar.display_arabic_text(f"{result}"))

        # function to start the process
        def start():
            # get the recipients and the message
            recipients = recipient_text.get("1.0", tk.END).strip().split('\n')
            # get the message
            message = message_text.get("1.0", tk.END)

            if not recipients  or not message.strip():
                messagebox.showwarning("Input Error", "All fields must be filled out")
                return
            # start the process of sending the message using the bot object and  async_handler to not block the main thread
            async_handler(self.bot.send_message(recipients, message.strip(), on_update))

        self.row_index += 12
        self.create_button("Send", start, 0 , new_window)
        self.row_index += 1
        information = self.create_info_label("", new_window)
        pass


    # Widget creation functions
    #NOTE: All widgets use the grid layout manager
    # it's easyto use and it's the best for this kind of app

    def create_checkbutton(self, text, command,variable ,row , column,  root=None):
        text = ar.display_arabic_text(text)
        checkbutton = ttk.Checkbutton(root, text=text, variable=variable, command=command, style="TCheckbutton")
        checkbutton.grid(row=row, column=column, padx=10, pady=5,  sticky="ew")
        return checkbutton

    def create_text(self, width, height, row , column, root=None):
        text_widget = tk.Text(root, width=width, height=height)
        text_widget.grid(row=row, column=column, padx=10, pady=5, sticky="nsew")
        return text_widget

    def create_info_label(self, text="" , root=None):
        """
        Creates an information label at the top of the window.

        Parameters:
        text (str): The text to display in the information label.
        """
        if root is None:
            root = self.root
        text = ar.display_arabic_text(text)
        info_label = ttk.Label(root, text=text, style="TLabel", anchor="center")
        info_label.grid(
            row=self.row_index,
            column=0,
            columnspan=3,
            pady=(10, 0),
            padx=5,
            sticky="ew",
        )
        self.row_index += 1
        return info_label

    def create_label(self, text,row, column, root=None):
        """
        Creates a label with specified text.

        Parameters:
        text (str): The text to display in the label.
        column (int): The column in which to place the label in the grid layout.
        """
        if root is None:
            root = self.root
        text = ar.display_arabic_text(text)
        label = ttk.Label(root, text=text, style="TLabel")
        label.grid(row=row, column=column, padx=10, pady=5, sticky="ew")
        return label

    def create_separator(self, root=None):
        """
        Creates a separator line between sections.
        """
        if root is None:
            root = self.root
        separator = ttk.Separator(root, orient="horizontal")
        separator.grid(
            row=self.row_index, column=0, columnspan=3, sticky="ew", pady=(10, 10)
        )
        self.row_index += 1

    def create_title(self, text , root=None):
        """
        Creates a title label spanning across multiple columns.

        Parameters:
        text (str): The text to display in the title label.
        """
        if root is None:
            root = self.root
        text = ar.display_arabic_text(text)
        title = ttk.Label(root, text=text, style="TLabel", anchor="center")
        title.grid(
            row=self.row_index, column=0, columnspan=3, pady=(10, 0), sticky="ew"
        )
        self.row_index += 1

    def create_button(self, text, command, column , root=None ):
        """
        Creates a button with specified text and action.

        Parameters:
        text (str): The text to display on the button.
        command (function): The function to call when the button is clicked.
        column (int): The column in which to place the button in the grid layout.
        """
        if root is None:
            root = self.root
        text = ar.display_arabic_text(text)
        button = ttk.Button(root, text=text, command=command, style="TButton")
        button.grid(row=self.row_index, column=column, padx=10, pady=10, sticky="ew")


# Run the GUI if the script is run directly
if __name__ == "__main__":
    root = tk.Tk()
    bot = TelegramBotGUI(root, None)
    root.mainloop()
