from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]