"""
Tests for User authentication and profile management.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserModelTests(TestCase):
    """Test the custom User model"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'TestPass123!'
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name='Test',
            last_name='User'
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@EXAMPLE.COM'
        user = User.objects.create_user(
            email=email,
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            User.objects.create_user(None, 'TestPass123!')

    def test_create_superuser(self):
        """Test creating a new superuser"""
        user = User.objects.create_superuser(
            email='admin@example.com',
            password='TestPass123!',
            first_name='Admin',
            last_name='User'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class UserRegistrationTests(TestCase):
    """Test user registration endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/register/'

    def test_register_user_success(self):
        """Test registering a user is successful"""
        payload = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'TestPass123!',
            'password2': 'TestPass123!',
        }

        res = self.client.post(self.register_url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', res.data)
        self.assertIn('tokens', res.data)

        user = User.objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_register_user_password_mismatch(self):
        """Test registration fails when passwords don't match"""
        payload = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'TestPass123!',
            'password2': 'DifferentPass123!',
        }

        res = self.client.post(self.register_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTests(TestCase):
    """Test user login endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.login_url = '/api/auth/login/'
        self.user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )

    def test_login_user_success(self):
        """Test logging in a user is successful"""
        payload = {
            'email': 'test@example.com',
            'password': 'TestPass123!',
        }

        res = self.client.post(self.login_url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('user', res.data)
        self.assertIn('tokens', res.data)

    def test_login_user_invalid_credentials(self):
        """Test login fails with invalid credentials"""
        payload = {
            'email': 'test@example.com',
            'password': 'WrongPassword',
        }

        res = self.client.post(self.login_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
