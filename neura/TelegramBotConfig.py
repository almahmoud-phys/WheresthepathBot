import json
import os


class TelegramBotConfig:
    CONFIG_FILE = 'config.json'

    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {}

    def save_config(self):
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=4)

    def get(self, key, default_value=None):
        return self.config.get(key, default_value)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()
