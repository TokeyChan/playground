#consumers.py

#from channels.db import database_sync_to_async
#from channels.generic.websocket import AsyncWebsocketConsumer
from playground.consumer import PlaygroundConsumer

from .models import *
from hotel_manager.models import *

import json

class ForestConsumer(PlaygroundConsumer):
    async def connect(self):
        self.room_nr = self.scope['url_route']['kwargs']['room_nr']
        self.room_group_name = 'forest_room_' + self.room_nr
        self.room = await self.get_room(self.room_nr)
        self.room_owner = await self.get_owner(self.room_nr)
        self.player = await self.get_player()

        if await self.player_in_room():
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            await self.send(text_data=json.dumps({
                'type':'players',
                'players': await self.room_members()
            }))
        else:
            print("not in room")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['type'] == 'set_setting':
            name = text_data_json['name']
            value = text_data_json['value']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'setting_changed',
                    'name':name,
                    'value':value
                })
            #HIER AUCH SETTING ÄNDERN
        elif text_data_json['type'] == 'start_game':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'start_game'
                }
            )

    async def setting_changed(self, event):
        if self.player != self.room_owner:
            await self.send(json.dumps({
                'type':'setting_changed',
                'name':event['name'],
                'value':event['value']
            }))

    async def start_game(self, event):
        await self.send(json.dumps({
            'type':'start_game'
        }))
