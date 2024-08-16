import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk, filedialog
import asyncio
import csv
from neura import TelegramBot

class TelegramBotGUI:
    def __init__(self, config):
        self.config = config
        self.loop = asyncio.get_event_loop()
        self.root = tk.Tk()
        self.root.title("Telegram Bot Configuration")
        self.root.geometry("900x750")  # Set the window size to 750px height

        self.user_batch_size = tk.IntVar(value=20)
        self.interval = tk.IntVar(value=5)
        self.interval_type = tk.StringVar(value="minutes")

        self.selected_users = self.config.get('selected_users', [])  # Load selected user IDs

        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True)

        config_frame = ttk.Frame(notebook)
        users_frame = ttk.Frame(notebook)

        notebook.add(config_frame, text="Configuration")
        notebook.add(users_frame, text="Group Members")

        self.create_config_tab(config_frame)
        self.create_users_tab(users_frame)

    def create_config_tab(self, frame):
        # Aligning the widgets for better UI
        padding = {'padx': 10, 'pady': 5}

        tk.Label(frame, text="API ID:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="e", **padding)
        self.api_id_entry = tk.Entry(frame)
        self.api_id_entry.insert(0, self.config.get('api_id', ""))
        self.api_id_entry.grid(row=0, column=1, **padding, sticky="ew")

        tk.Label(frame, text="API Hash:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="e", **padding)
        self.api_hash_entry = tk.Entry(frame)
        self.api_hash_entry.insert(0, self.config.get('api_hash', ""))
        self.api_hash_entry.grid(row=1, column=1, **padding, sticky="ew")

        tk.Label(frame, text="Phone:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="e", **padding)
        self.phone_entry = tk.Entry(frame)
        self.phone_entry.insert(0, self.config.get('phone', ""))
        self.phone_entry.grid(row=2, column=1, **padding, sticky="ew")

        tk.Label(frame, text="Group ID:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="e", **padding)
        self.group_id_entry = tk.Entry(frame)
        self.group_id_entry.insert(0, self.config.get('group_id', ""))
        self.group_id_entry.grid(row=3, column=1, **padding, sticky="ew")

        tk.Label(frame, text="Message:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="ne", **padding)
        self.message_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=40, height=10)
        self.message_text.insert(tk.INSERT, self.config.get('message_template', "This is the default message."))
        self.message_text.grid(row=4, column=1, **padding, sticky="ew")

        tk.Label(frame, text="Users per Batch:", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky="e", **padding)
        self.user_batch_entry = tk.Entry(frame, textvariable=self.user_batch_size)
        self.user_batch_entry.grid(row=5, column=1, **padding, sticky="ew")

        tk.Label(frame, text="Interval:", font=("Arial", 10, "bold")).grid(row=6, column=0, sticky="e", **padding)
        self.interval_entry = tk.Entry(frame, textvariable=self.interval)
        self.interval_entry.grid(row=6, column=1, **padding, sticky="ew")

        tk.Label(frame, text="Interval Type:", font=("Arial", 10, "bold")).grid(row=7, column=0, sticky="e", **padding)
        interval_type_menu = tk.OptionMenu(frame, self.interval_type, "seconds", "minutes", "hours")
        interval_type_menu.grid(row=7, column=1, **padding, sticky="ew")

        # Move Save and Start Bot buttons to the bottom
        save_button = tk.Button(frame, text="Save", command=self.save_config)
        save_button.grid(row=8, column=0, columnspan=2, pady=10)

        start_button = tk.Button(frame, text="Send Messages", command=self.start_bot)
        start_button.grid(row=9, column=0, columnspan=2, pady=10)

        # Make the text boxes fill the width
        frame.grid_columnconfigure(1, weight=1)

    def create_users_tab(self, frame):
        self.user_checkboxes = {}
        self.check_vars = {}

        # Adding padding for buttons
        button_padding = {'padx': 5, 'pady': 5}

        select_all_button = tk.Button(frame, text="Select All", command=self.select_all)
        select_all_button.grid(row=0, column=0, sticky="ew", **button_padding)

        clear_all_button = tk.Button(frame, text="Clear All", command=self.clear_all)
        clear_all_button.grid(row=0, column=1, sticky="ew", **button_padding)

        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=1, column=0, columnspan=2, sticky="nsew", **button_padding)
        scrollbar.grid(row=1, column=2, sticky="ns")

        self.users_frame = scrollable_frame

        self.refresh_button = tk.Button(frame, text="Refresh Users", command=self.refresh_users)
        self.refresh_button.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

        save_csv_button = tk.Button(frame, text="Save Selected Users to CSV", command=self.save_to_csv)
        save_csv_button.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

        # Adding padding around the list of users
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(1, weight=1)

    def validate_and_highlight(self, entry, key):
        if not entry.get():
            entry.config(bg="red")
            return False
        else:
            entry.config(bg="white")
            self.config.set(key, entry.get())
            return True

    def save_config(self):
        self.update_selected_users()  # Ensure selected_users list is updated
        valid = True
        valid &= self.validate_and_highlight(self.api_id_entry, 'api_id')
        valid &= self.validate_and_highlight(self.api_hash_entry, 'api_hash')
        valid &= self.validate_and_highlight(self.phone_entry, 'phone')
        valid &= self.validate_and_highlight(self.group_id_entry, 'group_id')

        if valid:
            self.config.set('message_template', self.message_text.get("1.0", tk.END).strip())
            self.config.set('selected_users', self.selected_users)
            messagebox.showinfo("Info", "Configuration saved successfully!")
        else:
            messagebox.showerror("Error", "Please fill in all the required fields highlighted in red.")

    def start_bot(self):
        self.update_selected_users()  # Ensure selected_users list is updated
        self.save_config()
        if all([self.api_id_entry.get(), self.api_hash_entry.get(), self.phone_entry.get(), self.group_id_entry.get()]):
            if not self.selected_users:
                messagebox.showwarning("Warning", "No users selected for messaging.")
                return
            bot = TelegramBot(
                config=self.config,
                user_batch_size=self.user_batch_size.get(),
                interval=self.interval.get(),
                interval_type=self.interval_type.get(),
                selected_users=self.selected_users
            )
            self.run_async(bot.send_reminders())
        else:
            messagebox.showerror("Error", "Cannot start bot. Please fill in all the required fields.")

    def run_async(self, coro):
        self.loop.run_until_complete(coro)

    def refresh_users(self):
        self.run_async(self.fetch_and_display_users())

    async def fetch_and_display_users(self):
        bot = TelegramBot(
            config=self.config,
            user_batch_size=self.user_batch_size.get(),
            interval=self.interval.get(),
            interval_type=self.interval_type.get(),
            selected_users=[]
        )
        members = await bot.get_group_members()
        for widget in self.users_frame.winfo_children():  # Clear previous checkboxes
            widget.destroy()
        self.user_checkboxes = {}
        self.check_vars = {}

        row = 0
        for user_id, username in members.items():
            var = tk.BooleanVar(value=(user_id in self.selected_users))
            chk = tk.Checkbutton(self.users_frame, text=f"{username} ({user_id})", variable=var, bg="white")
            chk.grid(row=row, column=0, sticky="w", padx=10, pady=2)
            self.user_checkboxes[user_id] = chk
            self.check_vars[user_id] = var
            row += 1

    def select_all(self):
        for var in self.check_vars.values():
            var.set(True)
        self.update_selected_users()

    def clear_all(self):
        for var in self.check_vars.values():
            var.set(False)
        self.update_selected_users()

    def update_selected_users(self):
        self.selected_users = [user_id for user_id, var in self.check_vars.items() if var.get()]

    def send_to_selected(self):
        self.update_selected_users()
        messagebox.showinfo("Info", f"Selected {len(self.selected_users)} users for messaging.")

    def save_to_csv(self):
        self.update_selected_users()  # Ensure the list of selected users is updated

        # Get the list of selected users' IDs and usernames
        selected_users_data = [{"user_id": user_id, "username": self.user_checkboxes[user_id].cget("text")} for user_id in self.selected_users]

        if not selected_users_data:
            messagebox.showwarning("Warning", "No users selected to save.")
            return

        # Prompt the user to select a save location and filename
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:  # User cancelled the save dialog
            return

        # Save to the chosen CSV file
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['user_id', 'username']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(selected_users_data)

        messagebox.showinfo("Info", f"Selected users have been saved to {file_path}")

