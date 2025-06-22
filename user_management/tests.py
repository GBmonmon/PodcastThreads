from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

"""
NOTE: How to run this test: python manage.py test user_management.tests
"""

class AuthFlowTest(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
        self.protected_url = '/api/podcasts/test/'

        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }

        # Create user via Django ORM to skip testing /register here
        self.user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password']
        )

    def test_access_protected_without_login(self):
        # Attempt to access protected URL without any auth token
        response = self.client.get(self.protected_url)
        # Should be 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_jwt_auth_flow(self):
        # Step 1: Login
        response = self.client.post(self.login_url, {
            "username": self.user_data['username'],
            "password": self.user_data['password']
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        access_token = response.data['access']
        refresh_token = response.data['refresh']

        # Step 2: Use access token to hit protected endpoint
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        protected_response = client.get(self.protected_url)
        self.assertEqual(protected_response.status_code, status.HTTP_200_OK)

        # Step 3: Refresh token
        refresh_response = self.client.post(self.refresh_url, {
            "refresh": refresh_token
        }, format='json')

        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh_response.data)

