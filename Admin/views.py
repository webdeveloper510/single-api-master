from rest_framework import viewsets
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
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
from rest_framework import status

# models
from chat.models import *
from moderator.models import *
from django.contrib.auth import get_user_model
from chat.helpers import send_notification_chat
from moderator.serializers import GirlSimpleSerializer

User = get_user_model()


class ModeratorListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ModeratorCreateSerializer
    allowed_method = ('GET', 'POST')

    def get_queryset(self):
        user = self.request.user
        # return User.objects.filter(role__in=['moderator', 'admin']).exclude(username=user.username)
        return User.objects.filter(role__in=['moderator', 'admin']).all()

    def create(self, request, *args, **kwargs):
        password = json.loads(request.body)['password']

        serializer = ModeratorCreateSerializer(data=json.loads(request.body))
        if serializer.is_valid():
            obj = serializer.save()
            obj.set_password(password)
            obj.role = 'moderator'
            obj.save()

            moderator_setting = ModeratorSetting()
            moderator_setting.moderator = obj
            moderator_setting.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.core import serializers
class MassTriggerView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    allowed_method = 'POST'

    def create(self, request, *args, **kwargs):
        fake_admin = Girl.objects.filter(username='admin').first()
        if not fake_admin:
            fake_admin = Girl()
            fake_admin.creator = request.user
            fake_admin.username = 'admin'
            fake_admin.save()

        customers = UserAccount.objects.all()
        for customer in customers:
            chat = Chat.objects.filter(girl=fake_admin, customer=customer).first()

            if chat is None:
                chat = Chat()
                chat.girl = fake_admin
                chat.customer = customer
                chat.save()

            if request.user.role == 'admin':
                message_text = json.loads(request.body)['message']

                message = Message.objects.create(
                    senderModel=fake_admin,
                    tag='text',
                    file_name='',
                    file_url='',
                    file_size='',
                    content=message_text)
                chat.messages.add(message)
                aa = send_notification_chat(chat.id, 'model')

                chat.save()

        return Response({'result': "ok", 'channel':aa })


class ModeratorSettingListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ModeratorSettingSerializer
    allowed_method = ('GET', 'POST')
    queryset = ModeratorSetting.objects.all()

    def list(self, request, *args, **kwargs):
        moderator = request.GET.get('moderator', False)
        if moderator:
            user = UserAccount.objects.filter(username=moderator).first()
        else:
            user = request.user
        type = request.GET.get('type', False)
        if type == 'all':
            queryset = ModeratorSetting.objects.all()
        elif user.role in ['moderator', 'admin']:
            queryset = ModeratorSetting.objects.filter(moderator=user).all()
        else:
            queryset = []
        serializer = ModeratorSettingSerializer(queryset, many=True)
        return Response(serializer.data)


class ModeratorSettingDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ModeratorSettingSerializer
    allowed_method = ('GET', 'PUT')
    queryset = ModeratorSetting.objects.all()


class CustomerAddCoin(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    allowed_method = ('GET', 'POST')

    def create(self, request, *args, **kwargs):
        request_data = json.loads(request.body)
        user = request.user
        if user.role != 'admin':
            return Response("Permission error", 403)
        customer_id = request_data['customer']
        coin = request_data['coin']

        customer = UserAccount.objects.filter(id=customer_id).first()
        customer.coins = customer.coins + int(coin)
        customer.save()

        return Response({'result': 'success'}, 200)


class CustomerDeleteView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    allowed_method = ('GET', 'POST')

    def create(self, request, *args, **kwargs):
        request_data = json.loads(request.body)
        user = request.user
        if user.role != 'admin':
            return Response("Permission error", 403)
        customer_id = request_data['customer']

        customer = UserAccount.objects.filter(id=customer_id).first()
        customer.delete()

        return Response({'result': 'success'}, 200)


class GirlLikeListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = GirlLikeSerializer
    allowed_method = ('GET', 'POST')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user_like', 'girl_like', 'girl']
    queryset = GirlLike.objects.order_by('user').all()

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body)
        item_id = data['item_id']
        obj = GirlLike.objects.filter(id=item_id).first()
        obj.girl_like = True
        obj.save()
        return Response({'result': 'success'}, 200)


class GirlMatchListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = GirlLikeSerializer
    allowed_method = ('GET', 'POST')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    def create(self, request, *args, **kwargs):
        girls_query = Girl.objects.exclude(username='admin').all()

        girls_query = [obj for obj in girls_query if obj.matches()]

        serializer = GirlSimpleSerializer(girls_query, many=True, context={'request': request})
        return Response(serializer.data)


