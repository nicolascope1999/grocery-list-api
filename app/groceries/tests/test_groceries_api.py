"""
Tests for the Groceries API
"""

from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient




GROCERIES_URL = reverse("groceries:groceries")
class PublicGroceriesApiTests(TestCase):
    """
    Test the publicly available groceries API
    """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """
        Test that login is required to access the endpoint
        """
        res = self.client.get(GROCERIES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
