import asyncio
import tkinter as tk
from tkinter import  simpledialog

from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

class SingleChoiceDialog(simpledialog.Dialog):
    def __init__(self, parent, title, options):
        self.options = options
        self.choice = None
        super().__init__(parent, title=title)

    def body(self, master):
        tk.Label(master, text="Please choose an option:").grid(row=0, column=0, columnspan=2)

        self.var = tk.StringVar(value=self.options[0])
        for idx, option in enumerate(self.options):
            tk.Radiobutton(master, text=option, variable=self.var, value=option).grid(row=idx+1, column=0, sticky='w')

        return None  # No initial focus

    def apply(self):
        self.choice = self.var.get()

class TeClient:
    def __init__(self, root, config):
        self.root = tk.Tk()
        self.loop = asyncio.get_event_loop()
        self.client = TelegramClient(
            "session_name", config.get("api_id"), config.get("api_hash"), loop=self.loop
        )
        self.phone = config.get("phone")
        self.loop.run_until_complete(self.start_client())
        config.set("group_id", self.loop.run_until_complete(self.get_group_id()))

    async def start_client(self):
        await self.client.connect()
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone)

            self.root.withdraw()  # Hide the main window

            verification_code = simpledialog.askstring(
                "Verification Code", "Please enter the verification code:"
            )
            if verification_code:
                print(f"Verification code entered: {verification_code}")
            else:
                print("No code entered.")

            await self.client.sign_in(self.phone, verification_code)

    async def get_group_id(self):
        chats = []
        last_date = None
        chunk_size = 200
        groups = []

        result = await self.client(
            GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash=0,
            )
        )
        chats.extend(result.chats)

        for chat in chats:
            try:
                if chat.megagroup == True:
                    groups.append(chat)
            except:
                continue
        titles = []
        for i, g in enumerate(groups):
            titles.append(str(i) + ";; " + g.title)

        selected = SingleChoiceDialog(self.root, "Choose a group ", titles)
        index = int(selected.choice.split(";;")[0])
        return groups[index].id
