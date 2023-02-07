from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group


# Register your models here
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'role', 'email', 'username', 'registered_at','last_login', 'is_active', 'coins')
    list_display_links = ('pk', )
    empty_value_display = '-empty-'
    date_hierarchy = 'registered_at'
    list_filter = ('role', )


class AffiliateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer', 'moderator')
    list_display_links = ('pk',)


class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer', 'price', 'paid_at')
    list_display_links = ('pk', )


admin.site.unregister(Group)
admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(Affiliate, AffiliateAdmin)
admin.site.register(Transactions, TransactionsAdmin)