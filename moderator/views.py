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
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action

from distutils import errors
# url="http://127.0.0.1:8000/media/"
url="http://singelsajten.se:8000/media/"

# class GirlList(generics.ListCreateAPIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.AllowAny]
#     allowed_methods = ('GET', 'POST')
#     serializer_class = CreateModelSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     filterset_fields = ['county', 'city']
#     search_fields = ['username']

#     def get_queryset(self):
#         start_age = self.request.GET.get('start_age', '18')
#         end_age = self.request.GET.get('end_age', '99')
#         if start_age == '':
#             start_age = 18
#         if end_age == '':
#             end_age = 99
#         start_date = datetime.now() - relativedelta(years=int(start_age))
#         end_date = datetime.now() - relativedelta(years=(int(end_age) + 1))
#         # print(Girl.objects.filter(birthday__gte=end_date, birthday__lte=start_date).all())
#         return Girl.objects.filter(birthday__gte=end_date, birthday__lte=start_date).all()

from rest_framework.views import APIView
from datetime import date
class GirlList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    @action(detail=False, methods=['post','get'])
    def post(self, request, format=None):
        serializer=GirlSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            

            user = UserAccount.objects.get(id= serializer.data['creator'])
            user.user = user

            # girlId = Girl.objects.get(id= serializer.data['id'])
            # girlId.girlId = girlId

            # girl_like_data=GirlLike.objects.create(user=user,girl=girlId)
            # girl_like_object= GirlLike.objects.filter(girl=serializer.data['id']).values("user_like")
            # print(girl_like_object) 
            # user_like=girl_like_object[0]['user_like']
            # print(user_like)
            dict_data={"id":serializer.data['id'],"username":serializer.data['username'],"email":serializer.data['email'],"first_name":serializer.data['first_name'],
                       "last_name":serializer.data['last_name'],"birthday":serializer.data['birthday'],"gender":serializer.data['gender'],"seeking":serializer.data['seeking'],
                       "status":serializer.data['status'],"county":serializer.data['county'],"city":serializer.data['city'],"hair_color":serializer.data['hair_color'],
                       "eye_color":serializer.data['eye_color'],"smoking_habit":serializer.data['smoking_habit'],"drinking_habit":serializer.data['drinking_habit'],"sexual_position":serializer.data['sexual_position'],
                       "ethnicity":serializer.data['ethnicity'],"children":serializer.data['children'],"body_type":serializer.data['body_type'],"height":serializer.data['height'],"about_me": serializer.data['about_me'],"online":serializer.data['online'],
                       "timestamp":serializer.data['timestamp'],"creator":serializer.data['creator']}#,"liked":user_like}
            print(dict_data)
            return Response(dict_data)
        
        return Response({errors:serializer.errors})
        

    @action(detail=False, methods=['Get'])
    def get(self, request, format=None):
        snippets = Girl.objects.all()
        serializer = GirlSerializer(snippets, many=True)
        array=[]
        for x in serializer.data:
           
            id=x['id']
            username=x['username']
            email=x['email']
            first_name=x['first_name']
            last_name=x['last_name']
            birthday=(x['birthday'])
            gender=x['gender']
            seeking=x['seeking']
            status=x['status']
            county=x['county']
            city=x['city']
            hair_color=x['hair_color']
            eye_color=x['eye_color']
            smoking_habit=x['smoking_habit']
            drinking_habit=x['drinking_habit']
            sexual_position=x['sexual_position']
            ethnicity=x['ethnicity']
            children=x['children']
            body_type=x['body_type']
            height=x['height']
            about_me=x['about_me']
            online=x['online']
            timestamp=x['timestamp']
            creator=x['creator']


            # girl_like_object= GirlLike.objects.filter(user=creator,girl=id).values("user_like")
            # user_like=girl_like_object[0]['user_like']
           
            if GirlPhoto.objects.filter(girl=id).exists():
             
             girl_photo_detail=GirlPhoto.objects.filter(girl=id).values('photo')
             girl_photo=girl_photo_detail[0]['photo']
             girl_photo_data=url+girl_photo
            else:
                girl_photo_data=None

            dict_data={"id":id,"username":username,"email":email,"first_name":first_name,
                       "last_name":last_name,"birthday":birthday,"gender":gender,"seeking": seeking,
                       "status":status,"county":county,"city":city,"hair_color":hair_color,
                       "eye_color":eye_color,"smoking_habit":smoking_habit,"drinking_habit":drinking_habit,"sexual_position":sexual_position,
                       "ethnicity":ethnicity,"children": children,"body_type": body_type,"height":height,"about_me": about_me,"online":online,
                       "timestamp":timestamp,"creator":creator,"photo":girl_photo_data}#"liked":user_like,
            array.append(dict_data)
        return Response(array)
    
    
   

class GetGirlDetailView(APIView):
   authentication_classes = [authentication.TokenAuthentication]
   permission_classes = [permissions.AllowAny]
   @action(detail=False, methods=['Get'])
   def get(self,request,pk ,format=None):

        if not Girl.objects.filter(id=pk).exists():
                return JsonResponse({"message":"Not Found"})
        else:
            snippets = Girl.objects.all()
            serializer = GirlSerializer(snippets, many=True)
            array=[]
            for x in serializer.data:
                id=x['id']
                username=x['username']
                email=x['email']
                first_name=x['first_name']
                last_name=x['last_name']
                birthday=x['birthday']
                gender=x['gender']
                seeking=x['seeking']
                status=x['status']
                county=x['county']
                city=x['city']
                hair_color=x['hair_color']
                eye_color=x['eye_color']
                smoking_habit=x['smoking_habit']
                drinking_habit=x['drinking_habit']
                sexual_position=x['sexual_position']
                ethnicity=x['ethnicity']
                children=x['children']
                body_type=x['body_type']
                height=x['height']
                about_me=x['about_me']
                online=x['online']
                timestamp=x['timestamp']
                creator=x['creator']
                girl_photo_detail=GirlPhoto.objects.filter(girl=id).values('photo')
                if GirlPhoto.objects.filter(girl=id).exists():
             
                    girl_photo_detail=GirlPhoto.objects.filter(girl=id).values('photo')
                    girl_photo=girl_photo_detail[0]['photo']
                    girl_photo_data=url+girl_photo
                else:
                    girl_photo_data=None
                if id==pk:
                    dict_data={"id":id,"username":username,"email":email,"first_name":first_name,
                            "last_name":last_name,"birthday":birthday,"gender":gender,"seeking": seeking,
                            "status":status,"county":county,"city":city,"hair_color":hair_color,
                            "eye_color":eye_color,"smoking_habit":smoking_habit,"drinking_habit":drinking_habit,"sexual_position":sexual_position,
                            "ethnicity":ethnicity,"children": children,"body_type": body_type,"height":height,"about_me": about_me,"online":online,
                            "timestamp":timestamp,"creator":creator,"photo":girl_photo_data}
                  
            return Response(dict_data)



class GirlDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    allowed_methods = ( 'POST', 'DELETE', 'PUT')
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
        print(moderator)
        if moderator:
            user = UserAccount.objects.filter(role=moderator).first()
            print(user)
        else:
            user = request.user

        print(user.role)    
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
            print("user" , user)
        affiliated_customers = []

        if not year:
            today = datetime.now()
            year = today.year
            month = today.month
        for item in user.affiliate_customer.all():
            affiliated_customers.append(item.customer)
        transactions = Transactions.objects.filter(
            customer__in=affiliated_customers,
            paid_at__year=year,
            paid_at__month=month
        ).all()
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
    def create(self, request):
        user = request.user
        request_data = json.loads(request.body) 
        girl = Girl.objects.filter(id=request_data['girl']).first()
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
    serializer_class = GirlSerializer2
    def get_queryset(self):
        user = self.request.user
        print(user)
        liked_girls_query = GirlLike.objects.filter(user_like=True).all()
        liked_girls = []
        for item in liked_girls_query:
            print(item)
            girl_photo_detail=GirlPhoto.objects.filter(girl=item.girl).values('photo')
            girl_photo=girl_photo_detail[0]['photo']
            girl_photo_data = {'girl': item.girl,'photo': url+girl_photo}
            # girl_like_object= GirlLike.objects.filter(girl=item.id).values("user_like")
            # user_like=girl_like_object[0]['user_like']
            # # print(girl_photo_data , user_like)
            liked_girls.append(item.girl)
            print(liked_girls)
        return liked_girls


class RandomGirl(APIView):
   authentication_classes = [authentication.TokenAuthentication]
   permission_classes = [permissions.AllowAny]
   @action(detail=False, methods=['Get'])
   def get(self,request ,format=None):
        one_week_ago = timezone.now() - timedelta(days=7)
        random_girls = Girl.objects.exclude(username='admin',timestamp__lt=one_week_ago).order_by('timestamp')[:3].all()
        serializer = GirlSerializer(random_girls, many=True)
        array = []
        for x in serializer.data:
            id=x['id']
            username=x['username']
            email=x['email']
            first_name=x['first_name']
            last_name=x['last_name']
            birthday=x['birthday']
            gender=x['gender']
            seeking=x['seeking']
            status=x['status']
            county=x['county']
            city=x['city']
            hair_color=x['hair_color']
            eye_color=x['eye_color']
            smoking_habit=x['smoking_habit']
            drinking_habit=x['drinking_habit']
            sexual_position=x['sexual_position']
            ethnicity=x['ethnicity']
            children=x['children']
            body_type=x['body_type']
            height=x['height']
            about_me=x['about_me']
            online=x['online']
            timestamp=x['timestamp']
            creator=x['creator']
            girl_like_object= GirlLike.objects.filter(user=creator,girl=id).values("user_like")
            user_like=girl_like_object[0]['user_like']

            girl_photo_detail=GirlPhoto.objects.filter(girl=id).values('photo')
            girl_photo=girl_photo_detail[0]['photo']
            girl_photo_data=url+girl_photo

            dict_data2={"id":id,"username":username,"email":email,"first_name":first_name,
                    "last_name":last_name,"birthday":birthday,"gender":gender,"seeking": seeking,
                    "status":status,"county":county,"city":city,"hair_color":hair_color,
                    "eye_color":eye_color,"smoking_habit":smoking_habit,"drinking_habit":drinking_habit,"sexual_position":sexual_position,
                    "ethnicity":ethnicity,"children": children,"body_type": body_type,"height":height,"about_me": about_me,"online":online,
                    "timestamp":timestamp,"creator":creator,"liked":user_like,"avatar":girl_photo_data}
            array.append(dict_data2)
        return Response(array)