from django.contrib import admin
from .models import *
from auths.models import ModeratorSetting


class GirlPhotoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'girl', 'photo', 'private')
    list_display_links = ('pk', )


class GirlLikeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'girl', 'user', 'user_like', 'girl_like')
    list_display_links = ('pk', )


class ModeratorSettingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'moderator', 'message', 'affiliate')
    list_display_links = ('pk', )


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('pk',  'receiver', 'type', 'title', 'text', 'link', 'created_at', 'checked')
    list_display_links = ('pk', )


admin.site.register(Notification, NotificationAdmin)
admin.site.register(Girl)
admin.site.register(GirlPhoto, GirlPhotoAdmin)
admin.site.register(GirlLike, GirlLikeAdmin)
admin.site.register(ModeratorSetting, ModeratorSettingAdmin)
