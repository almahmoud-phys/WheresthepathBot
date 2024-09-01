import asyncio
import json
import os
import tkinter as tk
from tkinter import simpledialog

from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import  InputPeerEmpty, ChannelParticipantCreator, \
    ChannelParticipantAdmin

import neura.Constants as Constants
from neura.utils import SingleChoiceDialog
from telethon import utils

class TelegramBotConfig:
    CONFIG_FILE = Constants.CONFIG_FILE

    def __init__(self, root):
        # ceate defuat directory if not exist
        if not os.path.exists(Constants.DEFAULT_DIRICTORY):
            os.makedirs(Constants.DEFAULT_DIRICTORY)


        self.root = root

        self.loop = asyncio.get_event_loop()

        self.config = {}
        self.load_config()
        if Constants.DEBUG:
            print("Config loaded:", self.config)

        self.admin = TelegramClient(
            "session_name",
            self.config.get("api_id"),
            self.config.get("api_hash"),
            loop=self.loop,
        )
        self.loop.run_until_complete(self.start_client())
        self.group = self.loop.run_until_complete(self.get_group())
        print(f"the group is {self.group.title}")
        if Constants.DEBUG:
            print(f"the group is {self.group.title}")
        self.users = self.loop.run_until_complete(self.get_users_list())
        if Constants.DEBUG:
            # print(self.users)
            print(f"there are {len(self.users)} users ")

    def load_config(self):
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, "r") as f:
                self.config = json.load(f)
            # check if all the required keys are present
            if not all(key in self.config for key in ["api_id", "api_hash", "phone"]):
                self.setup()
        else:
            # first time to run the bot
            # show the setup window
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
        print("Setting up the bot...")
        # start a window to ask for the api_id, api_hash, and phone
        self.splash = tk.Toplevel()
        self.splash.overrideredirect(
            True
        )  # Remove window decorations (title bar, etc.)

        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        splash_width = 600
        splash_height = 200
        x = (screen_width // 2) - (splash_width // 2)
        y = (screen_height // 2) - (splash_height // 2)
        self.splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")

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
        if Constants.DEBUG:
            api_id_entry.insert(0, Constants.API_ID)
            api_hash_entry.insert(0, Constants.API_HASH)
            phone_entry.insert(0, Constants.PHONE)
        else:
            api_id_entry.insert(0, "")
            api_hash_entry.insert(0, "")
            phone_entry.insert(0, "")

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
                print("API Info saved successfully!", self.config),
                self.splash.destroy(),
                # self.to_main(),
            ),
        )
        submit_button.grid(row=3, column=0, columnspan=2, pady=20)

        self.root.wait_window(self.splash)
        # Center the window on the screen
        # self.splash.eval("tk::PlaceWindow . center")

    def to_main(self):
        self.splash.destroy()
        self.root.deiconify()  # Show the main window

    async def start_client(self):
        await self.admin.connect()
        if not await self.admin.is_user_authorized():
            await self.admin.send_code_request(self.config.get("phone"))

            self.root.withdraw()  # Hide the main window

            verification_code = simpledialog.askstring(
                "Verification Code", "Please enter the verification code:"
            )
            if verification_code:
                print(f"Verification code entered: {verification_code}")
            else:
                print("No code entered.")

            await self.admin.sign_in(self.config.get("phone"), verification_code)

    async def get_group(self):
        chats = []
        last_date = None
        chunk_size = 200
        groups = []

        result = await self.admin(
            GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash=0,
            )
        )
        chats.extend(result.chats)
        ## ATTENTION : group must be public
        for chat in chats:
            try:
                if chat.megagroup:
                    groups.append(chat)
            except:
                continue
        # Another method that work with all groups
        # but the problem is private group doesn't work well with this script
        # dialogs = await self.admin.get_dialogs()
        # for i in dialogs:
        #    try:
        #        i.entity.status
        #    except:
        #        groups.append(i)
        #        continue
        if Constants.DEBUG:
            print("groups:", groups)
            for g in groups:
                if utils.get_peer_id(g) == Constants.GROUP_ID:
                    return  g
        titles = []
        for g in groups:
            titles.append(g.title)
        selected = SingleChoiceDialog(self.root, "Choose a group ", titles).choice
        print("selected:", selected)
        for g in groups:
            if g.title == selected:
                return g

    async def get_users_list(self):
        print(self.group.title)
        users = {}
        all_participants = await self.admin.get_participants(
            self.group, aggressive=True
        )
        for participant in all_participants:
            # Get the entity (user) using the user ID
            if Constants.DEBUG:
                is_admin = False
                safe_to_send = True
            else:
                # this part only work in production mode because it's very slow
                if isinstance( participant.participant , ChannelParticipantCreator) or isinstance( participant.participant , ChannelParticipantAdmin):
                    is_admin = True
                else:
                    is_admin = False
                user = await self.admin.get_entity(participant.id)

                #TODO: we need an algorithm to check if the user is safe to send message without being blocked
                messages = await self.admin.get_messages(user, limit=1)
                if messages.total > 0:
                    safe_to_send = True
                else:
                    safe_to_send = False

            # since telegram client work with user id not with username
            # se use the user id as key in the dictionary to store the user info
            users[participant.id] = {
                    "id": participant.id,
                    "username": participant.username,
                    "first_name": participant.first_name if participant.first_name is not None else "",
                    "last_name": participant.last_name if participant.last_name is not None else "",
                    "is_admin": is_admin,
                    "safe_to_send": safe_to_send,
                # "user_interaction": 0,
                # it's better to not store the user_interaction in the dictionary because it's not necessary and it's very slow to update it
                # same thing for sace_to_send
                }
        return users

