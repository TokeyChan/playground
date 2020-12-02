from django.urls import path

from . import views

app_name = "werewolf"

urlpatterns = [
    path('<int:room_nr>', views.forest, name="forest"),
    path('village/<int:room_nr>', views.village, name="village")
]
