"""
Serializers for the groceries app
"""

from rest_framework import serializers
from core.models import Groceries


class GroceriesSerializer(serializers.ModelSerializer):
    """Serializer for the groceries object"""

    class Meta:
        model = Groceries
        fields = ['id', 'name']
        read_only_fields = ['id']
