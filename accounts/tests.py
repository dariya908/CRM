from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient


class Avtoriz(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('login')
        User.objects.create_user(username='dari', password='dari1234')

    def test_avtoriz_succes(self):
        self.client.login(username='president', password='123456')
        data = {
            "username": "dari",
            "password": "dari1234"
        }
        self.response = self.client.post(self.url, data)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_password_succes(self):
        self.client.login(username='president', password='123456')
        data = {
            "username": "dari",
            "password": "dari.1234"
        }
        self.response = self.client.post(self.url, data)
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_succes(self):
        self.client.login(username='president', password='123456')
        data = {
            "username": "dariusha",
            "password": "dari12356"
        }
        self.response = self.client.post(self.url, data)
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)



