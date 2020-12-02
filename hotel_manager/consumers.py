import json
#from asgiref.sync import sync_to_async
#from channels.db import database_sync_to_async
#from channels.generic.websocket import AsyncWebsocketConsumer

#from .models import *

from playground.consumer import PlaygroundConsumer

class RoomConsumer(PlaygroundConsumer):
    async def connect(self):
        self.room_nr = self.scope['url_route']['kwargs']['room_nr']
        self.room_group_name = 'chat_room_' + self.room_nr
        self.room = await self.get_room(self.room_nr)
        self.player = await self.get_player()
        self.game_has_started = False

        if await self.player_in_room() == True:
            await self.player_joined()
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            await self.send(text_data=json.dumps({
                'type':'current_players',
                'players': await self.room_members()
            }))
            await self.send(text_data=json.dumps({
                'type':'game_set',
                'game_name': await self.active_game()
            }))
        else:
            print("NOT IN ROOM")

    async def disconnect(self, close_code):
        print(await self.player_in_room())
        print("game has started: " + str(self.game_has_started))

        if self.game_has_started != True:
            if self.player_is_owner():
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type':'owner_left',
                        'player_name':self.player.name
                    }
                )
            else:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type':'player_left',
                        'player_name':self.player.name
                    }
                )
            await self.db_leave_room()

        print(await self.player_in_room())

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

        elif text_data_json['type'] == 'start_game':
            #self.game_has_started = True
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'start_game'
                })

        elif text_data_json['type'] == 'get_games':
            games_list = await self.get_games()
            await self.send(
                text_data=json.dumps({
                    'type':'games',
                    'games':games_list
                })
            )
        elif text_data_json['type'] == 'set_game':
            await self.set_game(text_data_json['game_name'])
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'game_set',
                    'game_name': text_data_json['game_name']
                }
            )

    async def player_joined(self):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'new_player',
                'player': {
                    'name':self.player.name,
                    #'color':self.player.colour
                }
            })
    async def start_game(self, event):
        self.game_has_started = True
        await self.send(text_data=json.dumps({
            'type':'start_game'
        }))


    async def chat_message(self, event):
        message = event['message']
        player_name = event['player_name']

        await self.send(text_data=json.dumps({
            'type':'chat_message',
            'message':message,
            'player_name': player_name
        }))

    async def new_player(self, event):
        player = event['player']
        await self.send(text_data=json.dumps({
            'type': 'new_player',
            'player': player
        }))


    async def player_left(self, event):
        await self.send(text_data=json.dumps({
            'type': 'player_left',
            'player_name': event['player_name']
        }))

    async def owner_left(self, event):
        await self.send(text_data=json.dumps({
            'type':'owner_left'
        }))

    async def game_set(self, event):
        await self.send(text_data=json.dumps({
            'type':'game_set',
            'game_name':event['game_name']
        }))
