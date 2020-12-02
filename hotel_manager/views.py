from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.utils import timezone

from hotel_manager.utils import view_helpers as helper

from .models import *

import json

def entrance(request):
    template = loader.get_template('hotel_manager/entrance.html')
    context = {
        'player':helper.get_active_player(request)
    }
    return HttpResponse(template.render(context, request))

def lobby(request, room_key):
    template = loader.get_template('hotel_manager/lobby.html')
    return HttpResponse(template.render({'type':'unlock',
                                         'room_key':room_key,
                                         'room_nr':Room.objects.get(room_key=room_key).room_nr}, request))

def login(request):
    template = loader.get_template('hotel_manager/lobby.html')
    return HttpResponse(template.render({'type':'login'}, request))

def hallway(request):
    if request.method == "POST":
        request_data = request.POST
    else:
        request_data = request.session['hallway_data']
        del request.session['hallway_data']

    if 'session_id' in request.session:
        player = Player.objects.get(session_id=request.session['session_id'])
        if player.active_room != None:
            player.active_room = None
            player.save()
    if 'login' in request.POST.keys():
        player = Player(name=request_data['name'], session_id=Player.next_sessionid(), creation_date=timezone.now())
        player.save()
        request.session['session_id'] = player.session_id
    if 'create' in request_data.keys():
        if not 'session_id' in request.session.keys():
            return redirect('hotel_manager:login')
        elif not Player.objects.get(session_id=request.session['session_id']).is_active():
            Player.objects.get(session_id=request.session['session_id']).delete()
            del request.session['session_id']
            return redirect('hotel_manager:login')

        r = Room(room_nr=Room.next_roomnr(), room_key=Room.generate_key(), owner=Player.objects.get(session_id=request.session['session_id']))
        r.save()
        rp = RoomPermission(room=r, player=Player.objects.get(session_id=request.session['session_id']))
        rp.save()
        player.active_room = r
        player.save()
        return redirect('hotel_manager:room', room_nr=r.room_nr)

    if 'join' in request_data.keys():
        if not 'session_id' in request.session.keys():
            if 'room_key' in request_data.keys() and request_data['room_key'] != "":
                return redirect('hotel_manager:lobby', room_key=request_data['room_key'])
            if 'room_nr' in request_data.keys() and request_data['room_nr'] != "":
                #KNOCK
                return HttpResponse(f"Knock Knock at Room {request_data['room_nr']}. Please wait, until we programm this waiting and continue page!")

        else:
            if 'room_key' in request_data.keys() and request_data['room_key'] != "":
                if not player.has_permission(Room.objects.get(room_key=request_data['room_key'])):
                    rp = RoomPermission(room=Room.objects.get(room_key=request_data['room_key']), player=Player.objects.get(session_id=request.session['session_id']))
                    rp.save()
                return redirect('hotel_manager:room', room_nr=Room.objects.get(room_key=request_data['room_key']))
            if 'room_nr' in request_data.keys():
                try:
                    if player.has_permission(Room.objects.get(room_nr=request_data['room_nr'])):
                        return redirect('hotel_manager:room', room_nr=request_data['room_nr'])
                    #KNOCK
                    return HttpResponse("Knock Knock at Room " + request_data['room_nr'])
                except:
                    pass

    print(request_data.keys())
    if 'start_game' in request_data.keys():
        room = Room.objects.get(room_nr = request_data['room_nr'])
        return redirect(room.game.link, room_nr=room.room_nr)

    return HttpResponse("Welcome to the Hallway")


def room(request, room_nr):
    if 'room_key' in request.GET:
        request.session['hallway_data'] = {
            'join':'true',
            'room_key':request.GET['room_key']
        }
        return redirect('hotel_manager:hallway')

    room = Room.objects.get(room_nr=room_nr)
    if not 'session_id' in request.session.keys():
        request.session['hallway_data'] = {
            'join':'true',
            'room_nr':room_nr
        }
        if request.method == "POST":
            if 'room_key' in request.POST:
                request.session['hallway_data']['room_key'] = request.POST['room_key']
        return redirect('hotel_manager:hallway')

    player = Player.objects.get(session_id=request.session['session_id'])

    if not player.has_permission(room):
        return redirect('hotel_manager:entrance')

    player.active_room = room
    player.save()

    template = loader.get_template('hotel_manager/room.html')
    context = {
        'room': room,
        'player': player
        #'game':room.game
    }
    return HttpResponse(template.render(context, request))

def games(request):
    if request.method == "GET":
        return HttpResponse(json.dumps({'games':[game.name for game in Game.objects.all()]}))
    else:
        return HttpResponse("nah")
