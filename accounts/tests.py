import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_auth.tests.mixins import APIClient
from rest_auth.views import LoginView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework import status
from accounts.models import Profile
from accounts.serializers import ProfileSerializer
from accounts.views import MyProfileView


class RegistrationTestCase(APITestCase):

    def test_registration_successfull(self):
        data = {"username": "testcase", "email": "testcase@test.com", "password1": "qwerty", "password2": "qwerty"}
        response = self.client.post("/rest-auth/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unsuccessfull_registration(self):
        data = {"email": "testcase@test.com", "password1": "qwerty", "password2": "qwerty"}
        response = self.client.post("/rest-auth/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProfileViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="davinci", password="qwerty")
        self.profile = Profile.objects.create(user=self.user)
        self.token = Token.objects.create(user=self.user)
        self.factory = APIRequestFactory()
        self.view = MyProfileView.as_view({'get': 'retrieve', 'put': 'update'})
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_profile_detail_retrieve(self):
        request = self.factory.get('/profile/1')
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = self.view(request, pk='1')
        response.render()
        self.assertEqual(response.data, {"id": 1, "description": None, "user": 1})
        print(status.HTTP_200_OK)

    def test_profile_update_put(self):
        data = {"id": 1, "description": "test", "user": 1}
        request = self.factory.put('/profile/', data)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=1)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)
        print(status.HTTP_200_OK)

    def test_invalid_profile_update_put(self):
        invalid_data = {"id": self.profile.description, "description": 'test', "user": self.user.username}
        request = self.factory.put('/profile/', invalid_data)
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = self.view(request, pk=1)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.data, invalid_data)
        print(status.HTTP_400_BAD_REQUEST)