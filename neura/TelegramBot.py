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

    # all the methods that are going to be called from the main thread should be decorated with @async_handler
    # so they don't block the main thread

    @async_handler
    async def send_message(self, user_ids: list, message: str, callback):
        print("Sending message")
        for user_id in user_ids:
            try:
                # Check if '@' is in user_id, then split
                if '@' in user_id:
                    recipient_id = user_id.split("@")[1]
                else:
                    recipient_id = user_id

                print(f"Sending message to {recipient_id}")

                # Send the message to the recipient
                await self.client.send_message(recipient_id, message)

                # Introduce a random delay between sending messages
                await asyncio.sleep(random.uniform(30, 60))
            except Exception as e:
                print(f"Failed to send message to {user_id}: {str(e)}")

        # Update the UI and invoke the callback function on finish
        callback("Messages sent")
        ut.show_info("Messages sent")

    async def group_info(self):
        pass

    @async_handler
    async def take_presence(self, callback):
    #TODO: save attendence to csv file
        print("Taking presence in bot")
        chat_id = utils.get_peer_id(self.group)

        call_py = PyTgCalls(self.client)
        await call_py.start()
        global running
        running = True
        while running:
            participants = await call_py.get_participants(chat_id)
            callback(len(participants))
            print(f"Participants: {len(participants)}")
            if len(participants) == 0:
                running = False
            await asyncio.sleep(4)
        ut.show_info("Presence taking done")
        print("Presence taking done")

    @async_handler
    async def export_users(self, count):
        participants = await self.client.get_participants(self.group)
        return {user.id: user.username or user.id for user in participants}
