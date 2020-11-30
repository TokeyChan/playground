from django.db import models
from django.utils import timezone
import datetime, string, random


class Room(models.Model):
    room_nr = models.IntegerField()
    room_key = models.CharField(max_length=20, unique=True)
    owner = models.ForeignKey("Player", on_delete=models.CASCADE, blank=True, null=True)
    game = models.ForeignKey("Game", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.room_nr)
    def next_roomnr():
        return max([room.room_nr for room in Room.objects.all()]) + 1

    def generate_key():
        generated_key = "".join(random.choice(letters) for i in range(5))
        while len(Room.objects.filter(room_key=generated_key)) > 0:
            letters = string.ascii_uppercase
            generated_key = "".join(random.choice(letters) for i in range(5))
        return generated_key

    def join_link(self):
        return f"http://127.0.0.1:8000/room/{self.room_nr}?room_key={self.room_key}"



class Player(models.Model):
    session_id = models.IntegerField()
    name = models.CharField(max_length=25)
    creation_date = models.DateTimeField()
    active_room = models.ForeignKey(Room, related_name="members", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    def next_sessionid():
        return max([player.session_id for player in Player.objects.all()]) + 1

    def is_active(self):
        return self.creation_date >= timezone.now() - datetime.timedelta(days=1)

    def has_permission(self, room):
        if room in self.room_permissions():
            return True
        else:
            return False

    def room_permissions(self):
        return [permission.room for permission in self.roompermission_set.all()]

class RoomPermission(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{player.name}]-{room.room_nr}"


class Game(models.Model):
    name = models.CharField(max_length=20)
    link = models.CharField(max_length=30)

    def __str__(self):
        return self.name
