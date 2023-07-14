"""
tests for the user api
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create")


def create_user(**params):
    """
    create a user
    """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """
    test the users api (public)
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
        test creating user with valid payload is successful
        """
        payload = {
            "email": "test@example.com",
            "password": "testpass",
            "name": "Test Name"
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error(self):
        """
        test creating a user that already exists
        """
        payload = {
            "email": "test@example.com",
            "password": "testpass",
            "name": "Test Name"
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """
        test that password is more than 5 characters
        """
        payload = {
            "email": "test@example.com",
            "password": "pw",
            "name": "Test Name"
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """
        test that a token is created for the user
        """
        payload = {
            "email": "test@example.com",
            "password": "testpass",
            "name": "Test Name",
        }
        create_user(**payload)
        res = self.client.post(reverse("user:token"), payload)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """
        test that token is not created if invalid credentials are given
        """
        create_user(email="test@example.com", password="testpass")
        payload = {
            "email": "wrongemail@example.com",
            "password": "wrongpass",
        }
        res = self.client.post(reverse("user:token"), payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """
        test that token is not created if user doesn't exist
        """
        payload = {
            "email": "testing@example.com",
            "password": "testingpass",
        }
        res = self.client.post(reverse("user:token"), payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """
        test that email and password are required
        """
        res = self.client.post(reverse("user:token"), {
            "email": "one",
            "password": "",
        })
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """
        test that authentication is required for users
        """
        res = self.client.get(reverse("user:me"))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTest(TestCase):
    """
    test api requests that require authentication
    """

    def setUp(self):
        self.user = create_user(
            email="test@example.com",
            password="testpass",
            name="Test Name",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """
        test retrieving profile for logged in user
        """
        res = self.client.get(reverse("user:me"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            "name": self.user.name,
            "email": self.user.email,
        })

    def test_post_me_not_allowed(self):
        """
        test that POST is not allowed on the me url
        """
        res = self.client.post(reverse("user:me"), {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_username(self):
        """
        test updating the user profile for authenticated user
        """
        payload = {
            "name": "New Name",
            "password": "newpass",
        }
        res = self.client.patch(reverse("user:me"), payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
