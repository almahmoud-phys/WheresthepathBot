import asyncio
from queue import Queue

from pytgcalls import PyTgCalls
from telethon import utils


class TelegramBot:
    def __init__(self, client, group, users):
        self.loop = asyncio.get_event_loop()
        self.client = client
        self.group = group
        self.users = users

    async def send_message(self, user_ids, message):
        pass

    async def group_info(self):
        pass

    def take_presence(self, q: Queue):
        self.loop.run_until_complete(self.take_presence_async(q))

    async def take_presence_async(self, q: Queue):
        print("Taking presence in bot")
        chat_id = utils.get_peer_id(self.group)

        call_py = PyTgCalls(self.client)

        await call_py.start()
        await call_py.play(
            chat_id,
        )
        global running
        running = True
        while running:
            participants = await call_py.get_participants(chat_id)
            q.put(f"number of users {len(participants)}")
            print(f"number of users {len(participants)}")
            if len(participants) == 0:
                running = False
            #           for participant in participants:
            #                print(f"Participant {self.users[participant.user_id]} joined ")
            await asyncio.sleep(10)

    async def export_users(self, count):
        participants = await self.client.get_participants(self.group)
        return {user.id: user.username or user.id for user in participants}
