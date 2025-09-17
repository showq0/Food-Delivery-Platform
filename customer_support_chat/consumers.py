import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message


class MessagesConsumer(AsyncWebsocketConsumer):
    chat_id = None

    async def save_message(self, sender_id, content, chat_id):
        await Message.objects.acreate(
            sender_id=sender_id,
            content=content,
            chat_id=chat_id
        )

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_room = f'chat_id{self.chat_id}'

        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data['event_type']
        sender_name = data['sender_name']
        sender_id = data['sender_id']
        if event_type == 'typing':
            typing_status = data['typing_status']

            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'typing_indicator',
                    'event_type': 'typing',
                    'sender_name': sender_name,
                    'sender_id': sender_id,
                    'typing_status': typing_status
                }
            )
        elif event_type == 'message':
            message = data['message']

            await self.save_message(sender_id, message, self.chat_id)
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'chat_message',
                    'event_type': 'message',
                    'sender_name': sender_name,
                    'sender_id': sender_id,
                    'message': message,
                }
            )

    async def chat_message(self, event):
        event_type = event['event_type']
        message = event['message']
        sender_name = event['sender_name']
        sender_id = event['sender_id']


        await self.send(text_data=json.dumps({
            'event_type': event_type,
            'message': message,
            'sender_name': sender_name,
            'sender_id': sender_id

        }))

    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'event_type': 'typing',
            'sender_name': event['sender_name'],
            'sender_id': event['sender_id'],
            'typing_status': event['typing_status'],

        }))
