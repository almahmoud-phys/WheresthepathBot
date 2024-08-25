import asyncio
import random

from async_tkinter_loop import async_handler
from pytgcalls import PyTgCalls
from telethon import utils

# openpyxl
import openpyxl

import neura.utils as ut
import neura.Constants as Constants

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
        list_to_save = []
        while running:
            participants = await call_py.get_participants(chat_id)
            callback(f'{len(participants)}'  + " participants in the voice chat")
            for participant in participants:
                id = participant.user_id
                list_to_save.append(id)
            if len(participants) == 0:
                running = False
            await asyncio.sleep(4)
        ut.show_info("Presence taking done")
        print("Presence taking done")
        # remove duplicates
        list_to_save = list(dict.fromkeys(list_to_save))


        # use default directory to save the file
        file_path = Constants.DEFAULT_DIRICTORY + "presence.csv"
        with open(file_path, "w") as file:
            file.write("User ID, First Name, Last Name, Username \n")
            for id in list_to_save:
                user = self.users[id]
                file.write(f"{user['id']}, {user['first_name']}, {user['last_name']}, {user['username']}  \n")

        # Update the UI and invoke the callback function on finish
        callback(f"Presence saved to {file_path}")

    @async_handler
    async def export_users(self , callback):
        #TODO: switch from csv to xlsx (excel) file

        # use default directory to save the file
        file_path = Constants.DEFAULT_DIRICTORY + "users_info.csv"
        with open(file_path, "w") as file:
            # add group info to the file
            file.write(f"Group ID: {self.group.id}\n")
            file.write(f"Group Title: {self.group.title}\n")
            file.write(f"Group Username: {self.group.username}\n")
            file.write(f"Group Members: {self.group.participants_count}\n")

            file.write("User ID, First Name, Last Name, Username , مشرف , إملانية الإرسال دون حظر , التفاعل في المجموعة\n")

            # seif.users is a dict with the user id as the key and the user info as the value
            #TODO : add the user interaction in the group
            for id in self.users:
                user = self.users[id]
                file.write(f"{user['id']}, {user['first_name']}, {user['last_name']}, {user['username']} , {user['is_admin']} , {user['safe_to_send']} ,  0  \n")

        callback(f"Users exported to {file_path}")
        ut.show_info(f"Users exported to {file_path}")
