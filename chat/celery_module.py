from .models import Chat
from Admin.models import Setting
from django.utils import timezone

from chat import helpers

def check_chat_reminder():
    chats = Chat.objects.filter(status__in=['inactive', ], reminded_counts__lt=3)
    current_time = timezone.now()
    admin_setting = Setting.objects.first()
    reminded_chat = []
    if admin_setting:
        reminder_hours = admin_setting.reminder_hours
    else:
        reminder_hours = 6
    for chat in chats:
        last_message = chat.messages.last()
        if last_message:
            last_time = last_message.timestamp
            delta = current_time - last_time
            if delta.seconds > (reminder_hours * 3600):
                chat.status = 'remind'
                chat.reminded_timestamp = timezone.now()

                chat.reminded_counts = chat.reminded_counts + 1
                chat.save()
                reminded_chat.append(chat.id)
                helpers.send_notification()
    return reminded_chat


def check_chat_active():
    chats = Chat.objects.filter(status='assign')
    current_time = timezone.now()
    actived_chat = []
    for chat in chats:
        active_time = chat.assigned_timestamp
        last_message = chat.messages.last()
        if last_message:
            if not last_message.senderModel:  # it means that last message is from user. so moderator didn't send message yet.
                delta = current_time - active_time
                if delta.seconds > (10 * 60):
                    chat.status = 'active'
                    chat.assigned_moderator = None
                    chat.save()
                    actived_chat.append(chat.id)
                    helpers.send_notification()
    return actived_chat


def check_chat_push():
    chats = Chat.objects.filter(status='push')
    current_time = timezone.now()
    actived_chat = []
    for chat in chats:
        active_time = chat.pushed_timestamp
        delta = current_time - active_time
        push_time = chat.push_time * 60

        if delta.seconds > push_time:
            chat.status = 'active'
            chat.save()
            actived_chat.append(chat.id)
            helpers.send_notification()
    return actived_chat
