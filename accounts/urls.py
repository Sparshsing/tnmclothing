from django.urls import path, include
from rest_framework import routers
from .views import ChangePasswordView, ListUsers, UpdateProfileView, ViewProfileView

urlpatterns = [
    path('', ListUsers.as_view()),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='accounts_change_password'),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='accounts_update_profile'),
    path('<int:pk>/', ViewProfileView.as_view(), name='accounts_view_profile')
]