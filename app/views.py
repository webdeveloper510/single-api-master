from django.shortcuts import render
from rest_framework import generics
# Create your views here.
import json

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
from moderator.models import Girl

User = get_user_model()


class UserDetailView(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'POST', 'PUT')
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserLike(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'POST', 'PUT')

    def create(self, request, *args, **kwargs):
        user = request.user
        request_data = json.loads(request.body)
        girl = Girl.objects.filter(id=request_data['girl'])
        liked_users = girl.likedUser.all()
        if user in liked_users:
            girl.likedUser.remove(user)
            liked = False
        else:
            girl.likedUser.add(user)
            liked = True
        return Response({"liked": liked})


