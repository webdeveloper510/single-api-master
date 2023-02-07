from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from auths.models import UserAccount
from django.http import JsonResponse
from chat.models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import json

from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from chat import celery_module
from .consumers import message_to_json
from django.utils import timezone
from chat import helpers
from auths.serializers import UserInformationSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class ChatList(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'POST')
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    def get_queryset(self):
        user = self.request.user
        status = self.request.GET.get('status', '')
        if status == 'assign':
            return Chat.objects.filter(status__in=['assign', ], assigned_moderator=user).all()
        if user.role == 'user':
            return Chat.objects.filter(customer=user).all()
        else:
            return Chat.objects.filter(status__in=['active', 'remind']).exclude(girl__username__exact='admin').all()

    def create(self, request, *args, **kwargs):
        girl_id = json.loads(request.body)['girl']
        customer_id = json.loads(request.body)['customer']
        girl = Girl.objects.filter(pk=girl_id).first()
        customer = UserAccount.objects.filter(id=customer_id).first()

        chat = Chat.objects.filter(girl=girl, customer=customer).first()

        if chat is None:
            chat = Chat()
            chat.girl = girl
            chat.customer = customer
            chat.save()

            if request.user.role != 'user':
                message_text = json.loads(request.body)['message']

                message = Message.objects.create(
                    senderModel=girl,
                    tag='text',
                    file_name='',
                    file_url='',
                    file_size='',
                    content=message_text)
                chat.messages.add(message)
                chat.save()

        serializer = ChatSerializer(chat, context={"request": request})
        return Response(serializer.data)


class MessageList(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'POST')
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]


class ChatDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'POST')
    serializer_class = ChatDetailSerializer
    queryset = Chat.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, **self.kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class ChatLogCreateView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'POST')
    serializer_class = LogSerializer
    queryset = Logs.objects.all()

    def create(self, request, *args, **kwargs):
        chat_id = json.loads(request.body)['chatId']
        log_data = json.loads(request.body)['logData']

        serializer = LogSerializer(data=log_data)
        if serializer.is_valid():
            obj = serializer.save()
            chat = Chat.objects.filter(id=chat_id).first()
            if log_data['user_type'] == 'model':
                chat.girl_log = obj
            else:
                chat.customer_log = obj
            chat.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatLogsDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'POST', 'PUT')
    serializer_class = LogSerializer
    queryset = Logs.objects.all()


def check_chat(request):
    data = {
        'result': "success",
        'data': celery_module.check_chat_reminder()
    }
    return JsonResponse(data, safe=False)


def check_chat_assign(request):
    data = {
        'result': "success",
        'data': celery_module.check_chat_active()
    }
    return JsonResponse(data, safe=False)


def check_chat_push(request):
    data = {
        'result': "success",
        'data': celery_module.check_chat_push()
    }
    return JsonResponse(data, safe=False)


class UploadPhotoView(generics.ListCreateAPIView):
    permission_classes = [AllowAny, ]
    queryset = ChatPhoto.objects.all()
    serializer_class = PhotoSerializer
    allowed_methods = ('GET', 'POST')


# send push message to customer, back to lobby after set time
class PushChatView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        chatId = json.loads(request.body)['chatId']
        pushTime = json.loads(request.body)['pushTime']

        chat_obj = Chat.objects.filter(id=chatId).first()
        # chat Inactive
        chat_obj.status = 'push'
        chat_obj.push_time = pushTime
        chat_obj.pushed_timestamp = timezone.now()
        chat_obj.save()

        channel_layer = get_channel_layer()

        group_name = 'chat_'+str(chatId)

        reminder_message = Message.objects.create(
            sender=request.user,
            senderModel=chat_obj.girl,
            tag='text',
            content="I will be back in " + chat_obj.get_push_time_display(),
            senderType='model')

        reminder_message_json = message_to_json(reminder_message)
        chat_obj.messages.add(reminder_message)
        chat_obj.save()

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'chat_message',
                'message': {
                    'command': 'new_message',
                    'message': reminder_message_json
                }
            }
        )
        async_to_sync(channel_layer.group_send)(
            'lobby',
            {
                'type': 'chat_message',
                'message': {
                    'command': 'send_notification',
                    'content': "remove-lobby"
                }
            }
        )

        return Response({"result": "ok"}, status=status.HTTP_201_CREATED)


class AssignChatView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        chatId = json.loads(request.body)['chatId']
        moderator_username = json.loads(request.body)['moderator']
        chat_obj = Chat.objects.filter(id=chatId).first()
        moderator_obj = UserAccount.objects.filter(username=moderator_username).first()
        if not chat_obj.status in ['active', 'remind']:
            response_data = {
                'result': 'Permission Denied',
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        chat_obj.status = 'assign'
        chat_obj.assigned_moderator = moderator_obj
        chat_obj.assigned_timestamp = timezone.now()
        chat_obj.save()

        helpers.send_notification()

        response_data = {
            'result': 'Success',
        }

        return Response(response_data, status=status.HTTP_200_OK)


class UpdateCoin(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        user = request.user
        user = UserAccount.objects.filter(id=user.id).first()
        user.coins = user.coins - 10
        user.save()
        serializer = UserInformationSerializer(user, many=False, context={"request": request})
        return Response(serializer.data)


class InactiveChatView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        chatId = json.loads(request.body)['chatId']
        chat_obj = Chat.objects.filter(id=chatId).first()
        chat_obj.status = 'inactive'
        chat_obj.save()

        helpers.send_notification()

        response_data = {
            'result': 'Success',
        }

        return Response(response_data, status=status.HTTP_200_OK)


