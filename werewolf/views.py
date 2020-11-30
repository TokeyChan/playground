from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

from hotel_manager.models import Room, Player

def forest(request, room_nr):
    room = Room.objects.get(room_nr=room_nr)
    
    return HttpResponse("There are a lot of trees here")
