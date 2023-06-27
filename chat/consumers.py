from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from django.db.models import F

from .models import Message, get_last_10_messages, Chat, get_sender, get_sender_model, get_current_chat
from chat import helpers

User = get_user_model()


def messages_to_json(messages):
    result = []
    for message in messages:
        result.append(message_to_json(message))
    return result


def message_to_json(message):
    if message.senderType == 'user':
        sender_model_id = ''
    else:
        sender_model_id = message.senderModel.pk

    return {
        'id': message.id,
        'senderType': message.senderType,
        'sender': message.sender.pk,
        'senderModel': sender_model_id,
        'content': message.content,
        'file_url': message.file_url,
        'tag': message.tag,
        'timestamp': str(message.timestamp)
    }


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def update_user_incr(user):
    currentUser = user
    currentUser.online = currentUser.online + 1
    if currentUser.online > 0:
        currentUser.online_s = True
    else:
        currentUser.online_s = False
    currentUser.save()


def update_user_decr(user):
    currentUser = user
    # currentUser.update(online=F('online') - 1)
    currentUser.online = currentUser.online - 1
    if currentUser.online > 0:
        currentUser.online_s = True
    else:
        currentUser.online_s = False
    currentUser.save()


def read_messages(contact, chat_id):
    chat = Chat.objects.get(pk=chat_id)
    chat.messages.exclude(contact=contact).update(read=1)


class ChatConsumer(AsyncWebsocketConsumer):

    async def fetch_messages(self, data):
        messages = get_last_10_messages(data['chatId'])
        content = {
            'command': 'messages',
            'messages': messages_to_json(messages)
        }

        await self.send_message(content)

    async def new_message(self, data):
        try:
            print("here---- NEW MESSAGE")
            message = Message.objects.create(
                sender=get_sender(data['senderId']),
                senderModel=get_sender_model(data['senderType'], data['chatId']),
                tag=data['tag'],
                file_name=data['message']['file_name'],
                file_url=data['message']['file_url'],
                file_size=data['message']['file_size'],
                content=data['message']['content'],
                senderType=data['senderType'])
            current_chat = get_current_chat(data['chatId'])

            current_chat.messages.add(message)
            if message.senderModel:
                current_chat.status = 'inactive'
            else:
                if current_chat.status == 'inactive':
                    current_chat.status = 'active'
                    current_chat.reminded_counts = 0

            current_chat.assigned_user = None
            current_chat.save()
            # helpers.send_notification_chat(current_chat.id, message.senderType)
            print("group name,", self.room_group_name)

            content = {
                'command': 'new_message',
                'message': message_to_json(message)
            }

            await self.send_chat_message(content)
        except Exception as e:
            print("error", e)

    async def reminder_message(self, event):
        message = event['message']


    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
    }

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print("Here Connect")

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("Here Disconnect")

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.commands[data['command']](self, data)

    async def send_chat_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


class NotificationConsumer(AsyncWebsocketConsumer):

    async def send_notification(self, data):
        print('send-notification', data)

        await self.send_chat_message(data)

    commands = {
        'send_notification': send_notification,
    }

    async def connect(self):
        self.room_name = 'notification'
        self.room_group_name = 'notification'
        print("notification connected user:", self.scope['user'])
        # update_user_incr(self.scope['user'])
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("disconnected user:", self.scope['user'])
        # update_user_decr(self.scope['user'])
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.commands[data['command']](self, data)

    async def send_chat_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))
        print("Here Send Message")

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
        print("Here Chat Message")


class LobbyConsumer(AsyncWebsocketConsumer):

    async def send_notification(self, data):
        print('send-notification', data)

        await self.send_chat_message(data)

    commands = {
        'send_notification': send_notification,
    }

    async def connect(self):
        self.room_name = 'lobby'
        self.room_group_name = 'lobby'
        print("lobby connected user:", self.scope['user'])
        # update_user_incr(self.scope['user'])
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("lobby disconnected user:", self.scope['user'])
        # update_user_decr(self.scope['user'])
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.commands[data['command']](self, data)

    async def send_chat_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
