from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

from hotel_manager.models import Room, Player

def forest(request, room_nr):
    room = Room.objects.get(room_nr=room_nr)
    template = loader.get_template('werewolf/forest.html')
    context = {
        'room':room,
        'player': Player.objects.get(session_id=request.session['session_id'])
    }
    return HttpResponse(template.render(context, request))
