from django.contrib import admin
from .models import Chat, Message, Logs
# Register your models here.


class ChatAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer', 'girl', 'status', 'assigned_moderator', 'assigned_timestamp', 'push_time', 'pushed_timestamp', 'reminded_timestamp', 'reminded_counts')
    list_display_links = ('pk', )


admin.site.register(Chat, ChatAdmin)
admin.site.register(Message)
admin.site.register(Logs)

