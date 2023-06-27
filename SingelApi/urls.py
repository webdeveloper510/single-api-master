"""SingelApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from moderator.routers import router
from django.conf import settings
from django.conf.urls.static import static
from datetime import date
from auths.views import *

urlpatterns = [
    path('api/moderator/', include('moderator.urls', namespace='moderator')),
    path('api/admin/', include('Admin.urls', namespace='my-admin')),
    path('admin/', admin.site.urls),
    path('api/chat/', include('chat.urls', namespace='chat')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('app/', include('app.urls')),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    # path('token', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
] 
from django.urls import re_path, path
from chat import consumers

websocket_urlpatterns = [
    re_path(r'ws/notification/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/lobby/$', consumers.LobbyConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]   
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)