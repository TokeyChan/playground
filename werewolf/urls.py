from django.urls import path

from . import views

app_name = "werewolf"

urlpatterns = [
    path('<int:room_nr>', views.forest, name="forest")
]
