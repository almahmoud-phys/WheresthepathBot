from telethon import TelegramClient
import asyncio

class TelegramBot:
    def __init__(self, config, user_batch_size, interval, interval_type, selected_users):
        self.loop = asyncio.get_event_loop()
        # this is bad , we only need one client for all the instances
        # so I create a client class
        # use
        # self.client =  client
        # TODO : fix this
        self.client = TelegramClient('session_name', config.get('api_id'), config.get('api_hash'), loop=self.loop)
        self.phone = config.get('phone')
        self.message_template = config.get('message_template', "This is the default message.")
        self.user_batch_size = user_batch_size
        self.interval = interval
        self.interval_type = interval_type
        self.contacted_users = set()
        self.failed_users = {}
        self.success_users = {}
        self.failure_count = 0
        self.selected_users = selected_users  # List of user IDs to send messages to


    async def send_reminders(self):
        await self.start_client()
        group = await self.client.get_entity(self.group_id)
        participants = await self.client.get_participants(group)

        selected_participants = [p for p in participants if p.id in self.selected_users]

        if not selected_participants:
            print("No users selected or available for messaging.")
            return

        print(f"Sending messages to {len(selected_participants)} users...")

        if self.user_batch_size > len(selected_participants):
            self.user_batch_size = len(selected_participants)

        counter = 0
        for user in selected_participants:
            if user.id in self.contacted_users:
                continue

            if counter >= self.user_batch_size:
                break

            try:
                await self.client.send_message(user.id, self.message_template)
                print(f"Reminder sent to {user.username or user.id}")
                self.contacted_users.add(user.id)
                self.success_users[user.id] = {
                    'user_id': user.id,
                    'username': user.username or 'N/A',
                }
                counter += 1
            except Exception as e:
                print(f"Failed to send message to {user.username or user.id}: {e}")
                if user.id in self.failed_users:
                    self.failed_users[user.id]['attempts'] += 1
                else:
                    self.failed_users[user.id] = {
                        'user_id': user.id,
                        'username': user.username or 'N/A',
                        'error': str(e),
                        'attempts': 1
                    }

        if counter > 0:
            print(f"Successfully sent messages to {counter} users.")

    async def get_group_members(self):
        await self.start_client()
        group = await self.client.get_entity(self.group_id)
        participants = await self.client.get_participants(group)
        return {user.id: user.username or user.id for user in participants}

