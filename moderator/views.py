import decimal
import json
import random
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from datetime import datetime
from dateutil.relativedelta import relativedelta
from chat.models import Message
from datetime import timedelta


class GirlList(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'POST')
    serializer_class = CreateModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['county', 'city']
    search_fields = ['username']

    def get_queryset(self):
        start_age = self.request.GET.get('start_age', '18')
        end_age = self.request.GET.get('end_age', '99')
        if start_age == '':
            start_age = 18
        if end_age == '':
            end_age = 99
        start_date = datetime.now() - relativedelta(years=int(start_age))
        end_date = datetime.now() - relativedelta(years=(int(end_age) + 1))
        print(Girl.objects.filter(birthday__gte=end_date, birthday__lte=start_date).all())
        return Girl.objects.filter(birthday__gte=end_date, birthday__lte=start_date).all()


class GirlDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'POST', 'DELETE', 'PUT')
    queryset = Girl.objects.all()
    serializer_class = GirlSerializer


class GirlPhotoView(generics.ListCreateAPIView):
    permission_classes = [AllowAny, ]
    queryset = GirlPhoto.objects.all()
    serializer_class = CreateModelPhotoSerializer
    allowed_methods = ('GET', 'POST')

    def list(self, request, *args, **kwargs):
        model_id = request.GET.get('model_id', 1)
        private = request.GET.get('private', 0)
        queryset = GirlPhoto.objects.filter(girl=model_id, private=private)
        serializer = CreateModelPhotoSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)


class GirlPhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny, ]
    queryset = GirlPhoto.objects.all()
    serializer_class = CreateModelPhotoSerializer
    allowed_methods = ('GET', 'POST', 'DELETE', 'PUT')


class CustomersListView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = CustomerListSerializer
    allowed_method = ('GET', 'POST')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['county', 'city']

    def get_queryset(self):
        start_age = self.request.GET.get('start_age', '18')
        end_age = self.request.GET.get('end_age', '99')
        if start_age == '':
            start_age = 18
        if end_age == '':
            end_age = 99
        start_date = datetime.now() - relativedelta(years=int(start_age))
        end_date = datetime.now() - relativedelta(years=(int(end_age) + 1))
        list_data = UserAccount.objects.filter(birthday__gte=end_date, birthday__lte=start_date, role='user',
                                               is_active=True).all()

        new = self.request.GET.get('new', False)
        print("new",new)
        if new == '1':

            list_data = UserAccount.objects.filter(affiliate_moderator__customer__isnull=True, role='user',
                                                   is_active=True).all()
        return list_data


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'PUT')
    queryset = UserAccount.objects.all()
    serializer_class = CustomerListSerializer


class CustomerPhotoView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'PUT')
    queryset = UserAccount.objects.all()
    serializer_class = CustomerPhotoSerializer


class AffiliateListView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'POST')
    queryset = Affiliate.objects.all()
    serializer_class = AffiliateSerializer

    def list(self, request, *args, **kwargs):

        type = request.GET.get('type', '')

        moderator = request.GET.get('moderator', False)
        if moderator:
            user = UserAccount.objects.filter(username=moderator).first()
        else:
            user = request.user


        if type == 'all':
            affiliate_query = Affiliate.objects.all()
        elif user.role in ['moderator', 'admin']:
            affiliate_query = Affiliate.objects.filter(moderator=user).all()
        else:
            affiliate_query = []
        serializer = AffiliateSerializer(affiliate_query, many=True, context={"request": request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request_data = json.loads(request.body)
        customer = request_data['customer']
        moderator_username = request_data['moderator']
        customer = UserAccount.objects.filter(id=customer).first()
        moderator_obj = UserAccount.objects.filter(username=moderator_username).first()
        affiliate_obj = Affiliate()
        affiliate_obj.customer = customer
        affiliate_obj.moderator = moderator_obj
        affiliate_obj.save()
        serializer = AffiliateSerializer(affiliate_obj, many=False)
        return Response(serializer.data)


class AffiliateDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'PUT', 'DELETE')
    queryset = Affiliate.objects.all()
    serializer_class = AffiliateSerializer


class TransactionsListView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'POST')
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer

    def list(self, request, *args, **kwargs):
        moderator = request.GET.get('moderator', False)
        year = request.GET.get('year', False)
        month = request.GET.get('month', False)
        if moderator:
            user = UserAccount.objects.filter(username=moderator).first()
        else:
            user = request.user
        affiliated_customers = []

        if not year:
            today = datetime.now()
            year = today.year
            month = today.month

        for item in user.affiliate_customer.all():
            affiliated_customers.append(item.customer)

        transactions = Transactions.objects.filter(customer__in=affiliated_customers, paid_at__year=year,
                                                   paid_at__month=month).all()
        serializer = TransactionSerializer(transactions, many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body)
        customer = request.user
        transaction = Transactions()
        transaction.customer = customer
        transaction.price = data['price']
        transaction.save()
        customer.coins = customer.coins + int(data['coin'])
        customer.save()
        serializer = UserInformationSerializer(customer, many=False)
        return Response(serializer.data)


class RevenueView(generics.CreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'POST')

    def create(self, request, *args, **kwargs):
        if request.body:
            data = json.loads(request.body)
            moderator = UserAccount.objects.filter(username=data['moderator']).first()
            user = moderator
        else:
            user = request.user
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

        response_data = {
            'revenue': round(total_revenue, 2),
            'messageMonth': messages,
            'messageToday': messages_today,
            'affiliateCustomers': len(affiliated_customers),
            'messageCommission': moderator_setting.message,
            'messageIncomeMonth': messages * moderator_setting.message,
            'messageIncomeToday': messages_today * moderator_setting.message,
        }
        return Response(response_data)


from django.db.models.functions import TruncDate, TruncDay
from django.db.models import Count
from django.core import serializers
from django.http import JsonResponse
import calendar


class MessageStatisticView(generics.CreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'POST')

    def create(self, request, *args, **kwargs):
        if request.body:
            data = json.loads(request.body)
            moderator = UserAccount.objects.filter(username=data['moderator']).first()
            user = moderator
            month = data['month']
            year = data['year']
        else:
            user = request.user
            month = year = None
        if month and year:
            month = int(month)
            year = int(year)
        else:
            today = datetime.now()
            month = today.month
            year = today.year

        # get full dates for this month
        obj = calendar.Calendar()
        days = []
        messages = []
        incomes = []
        moderator_setting = ModeratorSetting.objects.filter(moderator=user).first()

        for day in obj.itermonthdates(year, month):
            if day.month == month:
                days.append(day)
                message_count = Message.objects.filter(sender=user, timestamp__month=day.month, timestamp__day=day.day, timestamp__year=day.year).count()
                message_revenue = message_count * moderator_setting.message
                messages.append(message_count)
                incomes.append(message_revenue)

        response_data = {
            'days': days,
            'messages': messages,
            'messages_revenue': incomes,
        }

        return JsonResponse(response_data, safe=False)

class UserLike(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'POST', 'PUT')
    serializer_class = GirlSerializer
    queryset = GirlLike.objects.all()
    print(queryset)
    def create(self, request):
        print("""=====""")
        user = request.user
        request_data = json.loads(request.body) 
        print('----------->' , request_data)
        girl = Girl.objects.filter(id=request_data['girl']).first()
        print('girl', girl)
        girl_like_obj = GirlLike.objects.filter(girl=girl, user=user).first()
        if girl_like_obj:
            if girl_like_obj.user_like:
                girl_like_obj.user_like = False
            else:
                girl_like_obj.user_like = True
        else:
            girl_like_obj = GirlLike()
            girl_like_obj.girl = girl
            girl_like_obj.user = user
            girl_like_obj.user_like = False

        girl_like_obj.save()
        return Response({"liked": girl_like_obj.user_like})




class LikedGirlListView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'POST', 'PUT')
    serializer_class = GirlSerializer
    def get_queryset(self):
        user = self.request.user
        print(user)
        liked_girls_query = GirlLike.objects.filter(user_like=True).all()
        liked_girls = []
        for item in liked_girls_query:
            liked_girls.append(item.girl)
        return liked_girls


class RandomGirl(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', )
    serializer_class = GirlSerializer

    def get_queryset(self):
        one_week_ago = timezone.now() - timedelta(days=7)
        print( timezone.now())
        print(one_week_ago)
        # Get up to 2 random girls added in the last week
        random_girls = Girl.objects.exclude(
            username='admin',
            timestamp__lt=one_week_ago
        ).order_by('timestamp')[:3]
        print(random_girls)
        return random_girls


