# chat/routing.py
from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notification/', consumers.NotificationConsumer),
    re_path(r'ws/lobby/', consumers.LobbyConsumer),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]

