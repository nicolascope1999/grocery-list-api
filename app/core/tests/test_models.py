"""
Tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        # Arrange
        email = "test@example.com"
        password = "Testpass123"
        name = "Test User"

        # Act
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name=name
        )

        # Assert
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        # Arrange
        emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
        ]
        for email, expected in emails:
            # Act
            user = get_user_model().objects.create_user(
                email=email,
                password="test123",
                name="Test Name"
            )

            # Assert
            self.assertEqual(user.email, expected)
