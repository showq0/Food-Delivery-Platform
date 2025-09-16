import json
from channels.generic.websocket import AsyncWebsocketConsumer


class TrackConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f'chat_{self.room_name}'
        user = self.scope["user"]
        self.is_driver = (user.role == "driver")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        if not self.is_driver:
            return  # ignore if customer tries to send
        data = json.loads(text_data)
        lon = data['lon']
        lat = data['lat']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'lon': lon,
                'lat': lat,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        lon = event['lon']
        lat = event['lat']

        await self.send(text_data=json.dumps({
            'lon': lon,
            'lat': lat
        }))

# {
#   lon: longitude,
#   lat: latitude
# }
