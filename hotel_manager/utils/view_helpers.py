from hotel_manager.models import *

def get_active_player(request):
    if not 'session_id' in request.session.keys():
        return None
    player = Player.objects.get(session_id=request.session['session_id'])
    if not player.is_active():
        player.delete()
        del request.session['session_id']
        return None
    else:
        return player
