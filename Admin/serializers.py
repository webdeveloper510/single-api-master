from rest_framework import serializers
from django.contrib.auth import get_user_model
from auths.models import Transactions
from auths.serializers import UserInformationSerializer
from datetime import datetime
from chat.models import Message
from auths.models import ModeratorSetting, Affiliate
from moderator.models import GirlLike, Girl
from moderator.serializers import GirlSimpleSerializer
User = get_user_model()


class ModeratorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class ModeratorSettingSerializer(serializers.ModelSerializer):
    moderator = UserInformationSerializer(required=False, read_only=True)
    revenue = serializers.SerializerMethodField()
    customers = serializers.SerializerMethodField()

    class Meta:
        model = ModeratorSetting
        fields = ('pk', 'moderator', 'message', 'affiliate', 'revenue', 'customers')

    def get_customers(self, moderator_setting):
        affiliates = Affiliate.objects.filter(moderator=moderator_setting.moderator).all()
        return len(affiliates)


    def get_message_today(self, moderator_setting):
        moderator = moderator_setting.moderator
        today = datetime.now()
        messages = len(Message.objects.filter(senderType='model', sender=moderator, timestamp__year=today.year,
                                              timestamp__month=today.month).all())
        return messages

    def get_revenue(self, moderator_setting):
        moderator = moderator_setting.moderator
        user = moderator
        today = datetime.now()
        # messages you sent in this month
        messages = len(Message.objects.filter(senderType='model', sender=user, timestamp__year=today.year,
                                              timestamp__month=today.month).all())
        messages_today = len(Message.objects.filter(senderType='model', sender=user, timestamp__year=today.year,
                                                    timestamp__month=today.month, timestamp__day=today.day).all())
        remind_messages = len(
            Message.objects.filter(senderType='model', sender=user, type='remind', timestamp__year=today.year,
                                   timestamp__month=today.month).all())

        moderator_setting = ModeratorSetting.objects.filter(moderator=user).first()
        total_revenue = messages * moderator_setting.message

        affiliated_customers = []
        for item in user.affiliate_customer.all():
            affiliated_customers.append(item.customer)

        transactions = Transactions.objects.filter(customer__in=affiliated_customers, paid_at__year=today.year,
                                                   paid_at__month=today.month).all()
        for item in transactions:
            total_revenue = float(total_revenue) + (float(moderator_setting.affiliate) * float(item.price) / 100)

        return round(total_revenue, 2)


class GirlLikeSerializer(serializers.ModelSerializer):
    user = UserInformationSerializer()
    girl = GirlSimpleSerializer()
    class Meta:
        model = GirlLike
        fields = ('id', 'user', 'girl', 'user_like', 'girl_like')
        depth = 1
