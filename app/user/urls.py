"""
URL mappings for the user api
"""

from django.urls import path
from user import views

app_name = 'user'

url_patterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    ]