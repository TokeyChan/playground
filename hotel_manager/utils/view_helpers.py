from hotel_manager.models import *

def get_active_player(request):
    if not 'session_id' in request.session.keys():
        return None

    return Player.objects.get(session_id=request.session['session_id'])
