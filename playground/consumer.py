#basic_consumer.py

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from hotel_manager.models import *

class PlaygroundConsumer(AsyncWebsocketConsumer):

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

    @database_sync_to_async
    def get_owner(self, room_nr):
        return self.room.owner

    @database_sync_to_async
    def active_game(self):
        return self.room.game.name
