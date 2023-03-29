from django.urls import path
from moderator import views

# from .views import


app_name = 'authentication'

urlpatterns = [
    # path('', LogIn.as_view(), name='login'),  
    path('model/<int:pk>/', views.GirlDetailView.as_view(), name='girl-detail'),#change name models  from model due to confusion 
    path('model/', views.GirlList.as_view()),
    path('model/<int:pk>', views.GirlList.as_view()),
    path('model-photo/', views.GirlPhotoView.as_view()),
    path('model-photo/<int:pk>/', views.GirlPhotoDetailView.as_view()),
    path('customers/', views.CustomersListView.as_view()),
    path('customers/photo/<int:pk>/', views.CustomerPhotoView.as_view()),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view()),
    path('affiliate/', views.AffiliateListView.as_view()),
    path('affiliate/<int:pk>/', views.AffiliateDetailView.as_view()),
    path('transactions/', views.TransactionsListView.as_view(), name='send-message'),
    path('revenue/', views.RevenueView.as_view(), name='revenue'),
    path('message-statistic/', views.MessageStatisticView.as_view(), name='message-statistic'),
    path('user-like/', views.UserLike.as_view(), name='user-like'),
    path('liked-girls/', views.LikedGirlListView.as_view(), name='user-like'),
    path('random-girl/', views.RandomGirl.as_view(), name='random-girl'),
    # path('notifications/', views.NotificationListView.as_view(), name='notifications'),
]

