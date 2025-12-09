import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.group_name = f"user_{self.scope['user'].id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        # Typically clients don't send; we push from server.
        pass

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'created_at': event['created_at'],
        }))
