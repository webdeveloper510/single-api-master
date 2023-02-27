from .models import *
from rest_framework import serializers
from auths.serializers import UserInformationSerializer
from django.contrib.auth import get_user

class CreateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Girl
        fields = '__all__'
        # exclude = ('creator', 'email')


class CreateModelPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GirlPhoto
        fields = '__all__'


class GirlSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Girl
        fields = '__all__'

    def get_avatar(self, girl):
        request = self.context.get('request')
        girl_photo = girl.photo()
        if girl_photo:
            avatar = girl_photo.photo.url
            return request.build_absolute_uri(avatar)
        else:
            default = '/media/model/default_model.png'
            return request.build_absolute_uri(default)

    def get_age(self, girl):
        print("girl" , girl)
        return girl.age()

    def get_liked(self, girl):
        print("girl", girl)
        request = self.context.get('request')
        user = request.user
        print("request" , user)
        
        girl_like_obj = GirlLike.objects.filter(girl=girl).first()
        print("girl_like_obj" , girl_like_obj)
        if girl_like_obj.user_like:
            return True
        else:
            return False


class GirlSimpleSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    matches = serializers.SerializerMethodField()

    class Meta:
        model = Girl
        fields = ('username', 'avatar', 'age', 'id', 'online', 'city', 'county', 'about_me', 'matches')

    def get_avatar(self, girl):
        request = self.context.get('request')
        girl_photo = girl.photo()
        if girl_photo:
            avatar = girl_photo.photo.url
            return request.build_absolute_uri(avatar)
        else:
            default = '/media/model/default_model.png'
            return request.build_absolute_uri(default)

    def get_age(self, girl):
        return girl.age()

    def get_matches(self, girl):
        return girl.matches()


class GirlDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Girl
        fields = '__all__'


class CustomerListSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = UserAccount
        exclude = ['password', 'groups', 'is_active', 'is_staff', 'is_superuser', 'user_permissions']
        read_only_fields = ['avatar', ]

    def get_age(self, user):
        return user.age()


class CustomerPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = ['avatar',]


class AffiliateSerializer(serializers.ModelSerializer):
    customer = UserInformationSerializer()
    moderator = UserInformationSerializer()

    class Meta:
        model = Affiliate
        fields = ('id', 'customer', 'moderator')


class TransactionSerializer(serializers.ModelSerializer):
    customer = UserInformationSerializer(read_only=True, required=False)

    class Meta:
        model = Transactions
        fields = ('id', 'customer', 'price', 'paid_at')
