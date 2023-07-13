"""
URL mapping for the groceries app
"""
# defiens a path and includes the router.urls
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from groceries import views

# create a router
router = DefaultRouter()
# creates an endpoint for our viewset
router.register('', views.GroceriesViewSet)
# name for reverse  lookups
app_name = 'groceries'
# retrieve urls
urlpatterns = [
    path('', include(router.urls))
]