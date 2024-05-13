from users.models import User
from django.urls import reverse

from rest_framework.test import APITestCase


class UserRegistrationAPIViewTestCase(APITestCase):
    url = reverse("users:register")

    def test_invalid_password(self):
        """
        Test to verify that a post call with invalid passwords
        """
        user_data = {
            "email": "test@testuser.com",
            "password1": "password",
            "password2": "INVALID_PASSWORD",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_password_mismatch(self):
        """
        Test to verify that a post call with mismatched passwords
        """
        user_data = {
            "email": "test@testuser.com",
            "password1": "password",
            "password2": "mismatched_password",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_missing_password(self):
        """
        Test to verify that a post call with a missing password
        """
        user_data = {
            "email": "test@testuser.com",
            "password2": "password",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_missing_confirm_password(self):
        """
        Test to verify that a post call with a missing confirm password
        """
        user_data = {
            "email": "test@testuser.com",
            "password1": "password",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_short_password(self):
        """
        Test to verify that a post call with a short password
        """
        user_data = {
            "email": "test@testuser.com",
            "password1": "1234",
            "password2": "1234",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_duplicate_username(self):
        """
        Test to verify that a post call with a duplicate username
        """
        user_data = {
            "email": "test@testuser.com",
            "password1": "password",
            "password2": "password",
        }
        self.client.post(self.url, user_data)
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_duplicate_email(self):
        """
        Test to verify that a post call with a duplicate email
        """
        user_data = {
            "email": "test@testuser.com",
            "password1": "password",
            "password2": "password",
        }
        self.client.post(self.url, user_data)
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_valid_user_registration(self):
        """
        Test to verify that a post call with valid user data
        """
        user_data = {
            "email": "test@testuser.com",
            "password1": "password",
            "password2": "password",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(201, response.status_code)
        user = User.objects.get(email=user_data["email"])
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password(user_data["password1"]))


class UserLoginAPIViewTestCase(APITestCase):
    url = reverse("users:login")

    def setUp(self):
        self.user_email = "john@snow.com"
        self.user_password = "you_know_nothing"
        self.user = User.objects.create_user(self.user_email, self.user_password)

    def test_login_with_valid_credentials(self):
        """
        Test to verify that a post call with valid credentials returns a token
        """
        data = {
            "email": self.user_email,
            "password": self.user_password,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(200, response.status_code)
        self.assertIn("access", response.data)

    def test_login_with_invalid_password(self):
        """
        Test to verify that a post call with invalid password returns a 400 error
        """
        data = {
            "email": self.user_email,
            "password": "invalid_password",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(401, response.status_code)

    def test_login_with_invalid_email(self):
        """
        Test to verify that a post call with invalid email returns a 400 error
        """
        data = {
            "email": "invalid_email",
            "password": self.user_password,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(401, response.status_code)

    def test_login_with_missing_data(self):
        """
        Test to verify that a post call with missing data returns a 400 error
        """
        data = {
            "email": self.user_email,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)
