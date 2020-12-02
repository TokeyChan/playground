#consumers.py

#from channels.db import database_sync_to_async
#from channels.generic.websocket import AsyncWebsocketConsumer
from playground.consumer import PlaygroundConsumer


from .models import *
from hotel_manager.models import *


class ForestConsumer(PlaygroundConsumer):
    async def connect(self):
        self.room_nr = self.scope['url_route']['kwargs']['room_nr']
        self.room_group_name = 'forest_room_' + self.room_nr
        self.room = await self.get_room(self.room_nr)
        self.player = await self.get_player()

        if await self.player_in_room():
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            await self.send(text_data=json.dumps({
                'type':'current_players',
                'players': await self.room_members()
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['type'] == 'message':
            message = text_data_json['message']
            player_name = self.player.name

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'chat_message',
                    'message':message,
                    'player_name':player_name
                })
