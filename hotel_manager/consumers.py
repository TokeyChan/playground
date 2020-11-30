import json
#from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import *

class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_nr = self.scope['url_route']['kwargs']['room_nr']
        self.room_group_name = 'chat_room_' + self.room_nr
        self.room = await self.get_room(self.room_nr)
        self.player = await self.get_player()

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
        else:
            print("NOT IN ROOM")

    async def disconnect(self, close_code):
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
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.db_leave_room()


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

    async def start_game(self, event):
        await self.send(text_data=json.dumps({
            'type':'start_game'
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

    @database_sync_to_async
    def player_in_room(self):
        if not 'session_id' in self.scope['session'].keys():
            return False
        p = Player.objects.get(session_id=self.scope['session']['session_id'])
        room = Room.objects.get(room_nr=self.scope['url_route']['kwargs']['room_nr'])

        if p.active_room == room:
            return True
        else:
            return False

    @database_sync_to_async
    def get_room(self, room_nr):
        return Room.objects.get(room_nr=room_nr)

    @database_sync_to_async
    def get_player(self):
        if not 'session_id' in self.scope['session'].keys():
            return None
        return Player.objects.get(session_id=self.scope['session']['session_id'])


    @database_sync_to_async
    def room_members(self):
        room = Room.objects.get(room_nr=self.scope['url_route']['kwargs']['room_nr'])
        players = []
        for member in room.members.all():
            players.append({
                'name': member.name,
                #'color': member.color
                })
        return players

    @database_sync_to_async
    def db_leave_room(self):
        if not 'session_id' in self.scope['session'].keys():
            return None

        player = Player.objects.get(session_id=self.scope['session']['session_id'])
        player.active_room = None;
        player.save()

    @database_sync_to_async
    def player_is_owner(self):
        return self.room.owner == self.player

    @database_sync_to_async
    def get_games(self):
        return [game.name for game in Game.objects.all()]

    @database_sync_to_async
    def set_game(self, game_name):
        room = Room.objects.get(room_nr=self.scope['url_route']['kwargs']['room_nr'])
        room.game = Game.objects.get(name=game_name)
        room.save()
