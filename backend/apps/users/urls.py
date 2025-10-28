"""
URL routing for User authentication endpoints.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    UserProfileUpdateView,
    ChangePasswordView,
)

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # Token refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profile endpoints
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile_update'),

    # Password management
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]
