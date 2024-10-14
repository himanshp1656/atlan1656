# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DriverLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.driver_id = self.scope['url_route']['kwargs']['driver_id']
        self.room_group_name = f'driver_{self.driver_id}'
        
        # Join driver-specific group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave driver-specific group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        latitude = data['latitude']
        longitude = data['longitude']
        
        # Send the location update to the group (which includes the customer)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_location',
                'latitude': latitude,
                'longitude': longitude
            }
        )

    async def send_location(self, event):
        latitude = event['latitude']
        longitude = event['longitude']
        
        # Send the location to WebSocket
        await self.send(text_data=json.dumps({
            'latitude': latitude,
            'longitude': longitude
        }))
