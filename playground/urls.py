"""playground URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from werewolf import consumers as wolfs
from hotel_manager import consumers as tourists
from hotel_manager import views as hotel_views

urlpatterns = [
    path('', hotel_views.entrance),
    path('admin/', admin.site.urls),
    path('hotel/', include('hotel_manager.urls')),
    path('werewolf/', include('werewolf.urls'))
]


websocket_urlpatterns = [
    path('room/<room_nr>', tourists.RoomConsumer.as_asgi()),
    path('werewolf/forest/<room_nr>', wolfs.ForestConsumer.as_asgi())
]
