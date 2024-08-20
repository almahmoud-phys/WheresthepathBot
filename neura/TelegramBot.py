import asyncio
import random

from async_tkinter_loop import async_handler
from pytgcalls import PyTgCalls
from telethon import utils

import neura.utils as ut


class TelegramBot:
    def __init__(self, client, group, users):
        self.loop = asyncio.get_event_loop()
        self.client = client
        self.group = group
        self.users = users

    @async_handler
    async def send_message(self, user_ids: list, message: str, callback):
        print("Sending message")
        for user_id in user_ids:
            user_id = user_id.split("@")[1]
            print(f"Sending message to {user_id}")
            await self.client.send_message(user_id, message)
            await asyncio.sleep(random.uniform(30, 60))  # Random delay
        pass
        callback("Message sent")
        ut.show_info("message sent")

    async def group_info(self):
        pass

    @async_handler
    async def take_presence(self, callback):
        print("Taking presence in bot")
        chat_id = utils.get_peer_id(self.group)

        call_py = PyTgCalls(self.client)
        await call_py.start()
        # await call_py.play(
        #     chat_id,
        #     config= GroupCallConfig(auto_start=False)
        # )
        global running
        running = True
        while running:
            participants = await call_py.get_participants(chat_id)
            callback(len(participants))
            print(f"Participants: {len(participants)}")
            # calls = await call_py.group_calls
            # print(calls)
            if len(participants) == 0:
                # await call_py.leave_call(chat_id)
                running = False
            #           for participant in participants:
            #                print(f"Participant {self.users[participant.user_id]} joined ")
            await asyncio.sleep(4)
        ut.show_info("Presence taking done")
        print("Presence taking done")

    async def export_users(self, count):
        participants = await self.client.get_participants(self.group)
        return {user.id: user.username or user.id for user in participants}
