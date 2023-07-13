"""
Views for the groceries app.
"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated # permission to check before user can use endpoint

from core.models import Groceries
from groceries import serializers


#
class GroceriesViewSet(viewsets.ModelViewSet):
    # This will genereate multiple endpoints for us
    """Manage groceries in the database"""
    authentication_classes = [TokenAuthentication]
    # must be authenticated to use this endpoint else error
    permission_classes = [IsAuthenticated]
    # the objects available for this viewset
    queryset = Groceries.objects.all()
    serializer_class = serializers.GroceriesSerializer

    # overide the get_queryset method. This allows only the authenticated user to view their own groceries
    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    # overide the perform_create method. This allows only the authenticated user to create their own groceries
    def perform_create(self, serializer):
        """Create a new groceries"""
        serializer.save(user=self.request.user)