from django.urls import path
from . import views

app_name = 'chat'


urlpatterns = [
    path('', views.ChatList.as_view(), name='chat-list'),
    path('logs/', views.ChatLogCreateView.as_view(), name='chat-logs'),
    path('logs/<int:pk>/', views.ChatLogsDetailView.as_view(), name='chat-logs'),
    path('detail/<int:pk>/', views.ChatDetailView.as_view(), name='chat-list'),
    path('message/', views.MessageList.as_view(), name='message-list'),
    path('check_chat/', views.check_chat, name='chat-check'),
    path('check_chat_assign/', views.check_chat_assign, name='chat-check-assign'),
    path('check_chat_push/', views.check_chat_push, name='chat-check-push'),
    path('upload-photo/', views.UploadPhotoView.as_view(), name='chat-photo'),
    path('push-chat/', views.PushChatView.as_view(), name='push-chat'),
    path('assign/', views.AssignChatView.as_view(), name='assign'),
    path('update-coin/', views.UpdateCoin.as_view(), name='update-coin'),
    path('inactive/', views.InactiveChatView.as_view(), name='inactive'),
]