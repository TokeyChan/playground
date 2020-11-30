from django.urls import path

from . import views

app_name = "hotel_manager"

urlpatterns = [
    path('lobby/<slug:room_key>', views.lobby, name="lobby"),
    path('lobby/', views.login, name="login"),
    path('hallway/', views.hallway, name="hallway"),
    path('', views.entrance, name="entrance"),
    path('room/<int:room_nr>', views.room, name="room"),
    path('bar/games/', views.games, name="games")
]
