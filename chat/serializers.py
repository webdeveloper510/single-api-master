from .models import *
from rest_framework import serializers
from moderator.models import Girl
from moderator.serializers import GirlSimpleSerializer
from auths.serializers import UserInformationSerializer


class ChatSerializer(serializers.ModelSerializer):
    girl = GirlSimpleSerializer()
    lastMessage = serializers.SerializerMethodField()
    unseenMsgs = serializers.SerializerMethodField()
    customer = UserInformationSerializer()
    lobbyTime = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ('girl', 'id', 'lastMessage', 'unseenMsgs', 'customer', 'status', 'lobbyTime')
        depth = 1

    def get_lastMessage(self, chat):
        if chat.messages.last():
            return chat.messages.last().content
        else:
            return ''

    def get_unseenMsgs(self, chat):
        messages = chat.messages
        user_last_message = messages.filter(senderType='user').last()
        if user_last_message:
            user_unseenMsgs = messages.filter(id__gt=user_last_message.id).all()
            return len(user_unseenMsgs)
        else:
            return 0

    def get_lobbyTime(self, chat):
        if chat.status == 'active':
            return chat.messages.last().timestamp
        elif chat.status == 'assign':
            return chat.assigned_timestamp
        elif chat.status == 'remind':
            if chat.reminded_timestamp:
                return chat.reminded_timestamp

        return ''


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = '__all__'

    def get_sender_username(self, message):
        if message.sender:
            return message.sender.username
        else:
            return ''


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = '__all__'


class ChatDetailSerializer(serializers.ModelSerializer):
    girl = GirlSimpleSerializer(required=False)
    customer = UserInformationSerializer(required=False)
    lastMessage = serializers.SerializerMethodField()
    unseenMsgs = serializers.SerializerMethodField()
    girl_log = LogSerializer(required=False)
    customer_log = LogSerializer(required=False)
    assigned_moderator = UserInformationSerializer(required=False)
    messages = MessageSerializer(required=False, many=True)


    class Meta:
        model = Chat
        fields = ('girl', 'id', 'lastMessage', 'unseenMsgs', 'messages', 'customer', 'girl_log', 'customer_log', 'status', 'assigned_moderator', 'long_log')
        depth = 1

    def get_lastMessage(self, chat):
        if chat.messages.last():
            return chat.messages.last().content
        else:
            return ''

    def get_unseenMsgs(self, chat):
        return '2'


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatPhoto
        fields = '__all__'

