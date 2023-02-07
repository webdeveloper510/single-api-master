from django.urls import path
from app import views

# from .views import


app_name = 'authentication'

urlpatterns = [
    path('profile/', views.UserDetailView.as_view(), name='user-profile'),
    path('user-like/', views.UserLike.as_view(), name='user-like')
]
