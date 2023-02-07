from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_notification():
    channel_layer = get_channel_layer()

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
    return channel_layer


def send_notification_chat(chatId, senderType):
    channel_layer = get_channel_layer()
    print('Hi', chatId)
    print('channel_layer', channel_layer)
    async_to_sync(channel_layer.group_send)(
        'lobby',
        {
            'type': 'chat_message',
            'message': {
                'command': 'send_notification',
                'content': {
                    'chatId': chatId,
                    'senderType': senderType
                }
            }
        }
    )
    return str(channel_layer)
