import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add("notifications", self.channel_name)
            await self.accept()

    async def disconnect(self, code):
        try:
            await self.channel_layer.group_discard('notiifcations', self.channel_name)
        except Exception as e:
            pass

    async def receive(self, text_data=None, bytes_data=None):
        await self.send(text_data=json.dumps(text_data))
