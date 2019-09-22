# -*- coding: utf-8 -*-
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class MessagesConsumer(AsyncWebsocketConsumer):
    """
    处理私信应用中的WebSocket请求
    """

    async def connect(self):
        """
        # 用户一登陆，channels就会在redis里面创建创建一个以用户的username为组名的组
        (如果是以redis作为channels的话),发送私信就会往这个组里面发送msg
        """
        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            group_name = self.scope['user'].username
            await self.channel_layer.group_add(group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        try:
            group_name = self.scope['user'].username
            await self.channel_layer.group_discard(group_name, self.channel_name)
        except Exception as e:
            pass

    async def receive(self, text_data=None, bytes_data=None):
        """接收私信"""
        await self.send(text_data=json.dumps(text_data))

    # async def receive(self, text_data=None, bytes_data=None):
    #     # 从WebSocket接收消息
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #
    #     # 将消息发送到聊天组
    #     await self.channel_layer.group_send(
    #         f"{self.scope['user'].username}",
    #         {
    #             'type': 'chat_message',
    #             'message': message
    #         }
    #     )
    #
    # async def chat_message(self, event):
    #     # 从聊天组接收消息
    #     message = event['message']
    #
    #     # 将消息发送给Websocket
    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))
