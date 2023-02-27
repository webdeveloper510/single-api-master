from djoser.serializers import UserCreateSerializer 
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('__all__')


class UserInformationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'birthday', 'city', 'county', 'username', 'role', 'avatar', 'age', 'about_me', 'coins')