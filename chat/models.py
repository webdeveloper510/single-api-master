from django.contrib.auth import get_user_model
from django.db import models
from auths.models import UserAccount
from django.shortcuts import render, get_object_or_404
# from django.contrib.contenttypes.models import ContentType
from moderator.models import Girl

User = get_user_model()


def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-timestamp').all()[:10]


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)


def get_user_contact(username):
    user = User.objects.get(username=username)
    return user


def get_sender(id):
    return User.objects.get(pk=id)



def get_sender_model(type, id):
    if type == 'model':
        return Chat.objects.get(id=id).girl
    else:
        return None


SENDER_TYPE_CHOICES = [
    ('user', 'user'),
    ('model', 'model')
]

MESSAGE_TYPE_CHOICES = [
    ('normal', 'normal'),
    ('remind', 'remind')
]


class Message(models.Model):
    senderType = models.CharField(choices=SENDER_TYPE_CHOICES, default='user', verbose_name='type of sender', max_length=20)
    sender = models.ForeignKey(
        UserAccount, related_name='messages', on_delete=models.CASCADE, null=True, blank=True)
    senderModel = models.ForeignKey(
        Girl, related_name='messages', on_delete=models.CASCADE, null=True, blank=True)
    tag = models.TextField(default='text')
    file_name = models.TextField(default='', blank=True)
    file_url = models.TextField(default='', blank=True)
    file_size = models.TextField(default='', blank=True)
    content = models.TextField(default='', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default='normal')

    def __str__(self):
        return self.content


class Logs(models.Model):
    user_type = models.CharField(choices=SENDER_TYPE_CHOICES, max_length=20, default='model')
    about_me = models.TextField(null=True, blank=True)
    log = models.TextField(null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=100)
    family = models.CharField(null=True, blank=True, max_length=100)
    work = models.CharField(null=True, blank=True, max_length=100)
    pets = models.CharField(null=True, blank=True, max_length=100)
    hobbies = models.CharField(null=True, blank=True, max_length=100)
    civil_status = models.CharField(null=True, blank=True, max_length=100)
    cars = models.CharField(null=True, blank=True, max_length=100)
    living_condition = models.CharField(null=True, blank=True, max_length=100)
    personalities = models.CharField(null=True, blank=True, max_length=100)
    sexual_interests = models.CharField(null=True, blank=True, max_length=100)
    foods_drinks = models.CharField(null=True, blank=True, max_length=100)


CHAT_STATUS_CHOICES = [
    ('active', 'active'),
    ('inactive', 'inactive'),
    ('assign', 'assign'),
    ('push', 'push'),
    ('remind', 'remind')
]

# chat status: 1. customer send message, -- active status
# 2. moderator send message -- inactive status
# 3. opened status
# 4. assigned status
# 5. pushed status
# 6. remindered status

CHAT_PUSH_TIME_CHOICES = [
    (5, '5min'),
    (10, '10min'),
    (30, '30min'),
    (45, '45min'),
    (60, '1h'),
    (75, '1h 15min'),
    (90, '1h 30min'),
    (105, '1h 45min'),
    (120, '2h'),
    (180, '3h'),
    (240, '4h'),
    (300, '5h')
]


class Chat(models.Model):
    customer = models.ForeignKey(UserAccount, related_name='chats', on_delete=models.CASCADE, blank=True, null=True)
    girl = models.ForeignKey(Girl, related_name='chats', on_delete=models.CASCADE,blank=True, null=True)
    messages = models.ManyToManyField(Message, related_name='messages', blank=True)
    girl_log = models.OneToOneField(Logs, on_delete=models.CASCADE, related_name='girl_log', null=True, blank=True)
    customer_log = models.OneToOneField(Logs, on_delete=models.CASCADE, related_name='customer_log', null=True, blank=True)
    status = models.CharField(choices=CHAT_STATUS_CHOICES, default='inactive', max_length=30)

    # status property
    assigned_moderator = models.ForeignKey(UserAccount, related_name='active_chats', on_delete=models.CASCADE, null=True, blank=True)
    push_time = models.IntegerField(choices=CHAT_PUSH_TIME_CHOICES, blank=True, null=True)
    assigned_timestamp = models.DateTimeField(blank=True, null=True)
    pushed_timestamp = models.DateTimeField(blank=True, null=True)
    reminded_timestamp = models.DateTimeField(blank=True, null=True)
    reminded_counts = models.IntegerField(blank=True, null=True, default=0)

    long_log = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.pk)


class ChatPhoto(models.Model):
    file = models.FileField(upload_to='chat')