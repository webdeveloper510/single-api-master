from django.urls import path
from . import views

app_name = 'Admin'


urlpatterns = [
    path('moderator/', views.ModeratorListView.as_view(), name='admin-moderator'),
    path('mass-trigger/', views.MassTriggerView.as_view(), name='admin-moderator'),
    path('moderator-setting/', views.ModeratorSettingListView.as_view(), name='admin-moderator-setting'),
    path('moderator-setting/<int:pk>/', views.ModeratorSettingDetailView.as_view(), name='admin-moderator-setting-detail'),
    path('customer/add-coin/', views.CustomerAddCoin.as_view(), name='customer-add-coin'),
    path('customer/delete/', views.CustomerDeleteView.as_view(), name='customer-delete'),
    path('girl-like/', views.GirlLikeListView.as_view(), name='girl-like-list'),
    path('girl-match/', views.GirlMatchListView.as_view(), name='girl-match'),
]