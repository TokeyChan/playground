from django.db import models

# Create your models here.

from hotel_manager.models import Room


class GameSetting(models.Model):
    setting = models.ForeignKey("Setting", on_delete=models.CASCADE)
    game = models.ForeignKey("WerewolfGame", on_delete=models.CASCADE)
    value = models.CharField(max_length=25)


class Setting(models.Model):
    name = models.CharField(max_length=25)
    type = models.CharField(max_length=15)
    default_value = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return self.name

class WerewolfGame(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
