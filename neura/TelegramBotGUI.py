import asyncio
import queue
import tkinter as tk
from threading import Thread
from tkinter import messagebox, ttk

from neura.TelegramBot import TelegramBot
import neura.Constants as Constants

# FIXME ; this class for gui only all method and logic should be in the Bot class


class TelegramBotGUI:
    def __init__(self, root, bot):

        self.updates = None
        self.q = queue.Queue()
        self.updated_widget = None

        self.loop = asyncio.get_event_loop()
        self.root = tk.Toplevel()
        # self.root = root

        self.root.title("Bot tools")
        self.config = bot.config
        self.group = bot.group
        self.admin = bot.admin
        self.users = bot.users
        self.bot = TelegramBot(self.admin, self.group , self.users)

        self.styles()
        self.create_widgets()
        self.check_queue()

    def styles(self):
        """
        Initializes the styles for the application.
        """
        # Set a minsize for the window, and place it in the middle
        self.root.update()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
        x_cordinate = int(
            (self.root.winfo_screenwidth() / 2) - (self.root.winfo_width() / 2)
        )
        y_cordinate = int(
            (self.root.winfo_screenheight() / 2) - (self.root.winfo_height() / 2)
        )
        self.root.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))

        # self.root.geometry("500x500")
        self.root.resizable(True, True)
        # Configure grid for responsiveness
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
        # for i in range(9):  # Increased to 7 to accommodate the new top widget
        #     self.root.grid_rowconfigure(i, weight=1)

    def create_widgets(self):
        """
        Initializes the main application  widgets.
        """

        # Initialize row index
        self.row_index = 0

        # Top information widget
        self.create_info_label(f"Group Name: {self.group.title} with {len(self.users)} users")

        # Separator between top info and first section
        self.create_separator()

        # First row: Users Management
        self.create_title("Users Management")

        self.create_button("Get All Users to Excel", self.export_users, 0)
        self.create_button(
            "Get Users without Telegram ID", lambda: self.export_users("no_id"), 1
        )
        self.create_button("Update Users List", lambda: self.export_users("new"), 2)

        self.row_index += 1
        # Separator between first and second section
        self.create_separator()

        # Second row: Send Bulk Messages
        self.create_title("Send Bulk Messages")
        self.create_button("Send to All Users", lambda: self.send_message("all"), 0)
        self.create_button("Send to Selected Users", lambda: self.send_message(), 1)

        self.row_index += 1
        # Separator between second and third section
        self.create_separator()

        # Third row: Group Call Attendance
        self.create_title("Group Call Attendance")
        self.create_button("get group call presence", self.take_presence, 0)

        self.row_index += 1

        self.create_title("Group Statistics")
        self.create_button("get group Statistics", self.group_info, 0)

        self.row_index += 1
        # Separator before bottom buttons
        self.create_separator()

        # Bottom buttons: Close, Help, About
        self.create_bottom_buttons()

    # Button click handlers
    def export_users(self, condition=None):
        self.bot.export_users(condition)
        pass

    def take_presence(self):
        new_window = tk.Toplevel(self.root)

        new_window.title("New Window")
        new_window.geometry("300x200")

        # Content for the new window
        label = ttk.Label(new_window, text="This is a new window", font=("Arial", 14))
        label.pack(pady=10)

        description = ttk.Label(
            new_window,
            text=f"""
            if you click start the bot will start to take presence for all users in the group for the ongoing call , if there is no call the bot will  start a call
            the presence will be saved in csv file in the { Constants.DEFAULT_DIRICTORY} directory
            """,
            wraplength=250,
            justify="left",
        )
        description.pack(pady=10)


        thread = Thread(target=self.bot.take_presence, args=(self.q,))

        close_button = ttk.Button(
            new_window, text="Start", command=thread.start
        )
        close_button.pack(pady=10)

        close_button = ttk.Button(new_window, text="Close", command=new_window.destroy)
        close_button.pack(pady=10)

        information = ttk.Label(
            new_window,
            text="number of users is .....",
            wraplength=250,
            justify="left",
        )
        information.pack(pady=10)
        self.updated_widget = information


    def check_queue(self):
        try:
            self.updates = self.q.get_nowait()
            self.updated_widget.config(text=self.updates)
        except queue.Empty:
            pass
        self.root.after(10000, self.check_queue)  # Check the queue again after 100 ms


    def group_info(self):
        self.bot.group_info()
        pass

    def send_message(self, users=None, mesaage=""):
        # if users ==  "all":
        #     users = group.users
        self.bot.send_message(users, mesaage)
        pass

    def create_info_label(self, text):
        """
        Creates an information label at the top of the window.

        Parameters:
        text (str): The text to display in the information label.
        """
        info_label = tk.Label(self.root, text=text)
        info_label.grid(
            row=self.row_index,
            column=0,
            columnspan=3,
            pady=(10, 0),
            padx=5,
            sticky="ew",
        )
        self.row_index += 1

    def create_separator(self):
        """
        Creates a separator line between sections.
        """
        separator = ttk.Separator(self.root, orient="horizontal")
        separator.grid(
            row=self.row_index, column=0, columnspan=3, sticky="ew", pady=(10, 10)
        )
        self.row_index += 1

    def create_title(self, text):
        """
        Creates a title label spanning across multiple columns.

        Parameters:
        text (str): The text to display in the title label.
        """
        title = tk.Label(self.root, text=text)
        title.grid(
            row=self.row_index, column=0, columnspan=3, pady=(10, 0), sticky="ew"
        )
        self.row_index += 1

    def create_button(self, text, command, column):
        """
        Creates a button with specified text and action.

        Parameters:
        text (str): The text to display on the button.
        command (function): The function to call when the button is clicked.
        column (int): The column in which to place the button in the grid layout.
        """
        button = tk.Button(self.root, text=text, command=command)
        button.grid(row=self.row_index, column=column, padx=10, pady=10, sticky="ew")

    def create_bottom_buttons(self):
        """
        Creates a row of buttons at the bottom of the window, including Close, Help, and About.
        """
        self.row_index += 1  # Move to the next row for bottom buttons

        close_button = tk.Button(self.root, text="Close", command=self.root.quit)
        close_button.grid(row=self.row_index, column=0, padx=10, pady=10, sticky="ew")

        help_button = tk.Button(self.root, text="Help", command=self.on_help_click)
        help_button.grid(row=self.row_index, column=1, padx=10, pady=10, sticky="ew")

        about_button = tk.Button(self.root, text="About", command=self.on_about_click)
        about_button.grid(row=self.row_index, column=2, padx=10, pady=10, sticky="ew")

    def on_help_click(self):
        """
        Displays a help message when the Help button is clicked.
        """
        messagebox.showinfo("Help", "This is where you would provide help information.")

    def on_about_click(self):
        """
        Displays an about message when the About button is clicked.
        """
        messagebox.showinfo("About", "My Tkinter App v1.0\nCreated by [Your Name]")
