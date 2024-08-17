import json
import os
import tkinter as tk


class TelegramBotConfig:
    CONFIG_FILE = "config.json"

    def __init__(self, root):
        self.root = root
        self.splash = tk.Toplevel()
        self.splash.overrideredirect(True)  # Remove window decorations (title bar, etc.)
        self.load_config()
        self.choose_group()

    def load_config(self):
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, "r") as f:
                self.config = json.load(f)
            self.close_splash()
        else:
            # first time to run the bot
            # show the setup window
            self.config = {}
            self.setup()

    def save_config(self):
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key, default_value=None):
        return self.config.get(key, default_value)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

    def setup(self):
        # Set the splash screen size and position
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        splash_width = 600
        splash_height = 200
        x = (screen_width // 2) - (splash_width // 2)
        y = (screen_height // 2) - (splash_height // 2)
        self.splash.geometry(f'{splash_width}x{splash_height}+{x}+{y}')

        # Create and place the labels and entries for api_id, api_hash, and phone
        tk.Label(self.splash, text="API ID", font=("Arial", 12)).grid(
            row=0, column=0, pady=10, sticky="e"
        )
        tk.Label(self.splash, text="API Hash", font=("Arial", 12)).grid(
            row=1, column=0, pady=10, sticky="e"
        )
        tk.Label(self.splash, text="Phone", font=("Arial", 12)).grid(
            row=2, column=0, pady=10, sticky="e"
        )

        api_id_entry = tk.Entry(self.splash, font=("Arial", 12), width=20)
        api_hash_entry = tk.Entry(self.splash, font=("Arial", 12), width=20)
        phone_entry = tk.Entry(self.splash, font=("Arial", 12), width=20)

        api_id_entry.grid(row=0, column=1, padx=10)
        api_hash_entry.grid(row=1, column=1, padx=10)
        phone_entry.grid(row=2, column=1, padx=10)

        # Pre-fill the entries with default values (optional)
        api_id_entry.insert(0, "11114778")
        api_hash_entry.insert(0, "eaee280ee59d45c52cbd73c31fe79f69")
        phone_entry.insert(0, "+212708070221")

        # Create and place the submit button, centered below the entries
        submit_button = tk.Button(
            self.splash,
            text="Submit",
            font=("Arial", 12),
            command=lambda: (
                self.config.update(
                    {
                        "api_id": api_id_entry.get(),
                        "api_hash": api_hash_entry.get(),
                        "phone": phone_entry.get(),
                    }
                ),
                self.save_config(),
                print("API Info saved successfully!" , self.config),

                    self.close_splash(),
            ),
        )
        submit_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Center the window on the screen
        # self.splash.eval("tk::PlaceWindow . center")

    def close_splash(self):
        self.splash.destroy()
        # self.root.deiconify()  # Show the main window

    def choose_group(self):
        group = "test_group_id"
        self.set("group_id", group)
        # self.save_config()


if __name__ == "__main__":
    root = tk.Tk()
    config = TelegramBotConfig(root)
    config.setup()
