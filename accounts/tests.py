from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from accounts.models import Car, Warcraft, Dossier


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

class TestDossierMethods(APITestCase):
    def setUp(self):
        self.url = reverse('dossier')
        self.client = APIClient()
        self.user = User.objects.create_user(username='maksim',password='123456')
        self.dossier = Dossier.objects.create(user=self.user,full_name='maksim',date_birth='2021-05-09',
                                              gender='M',
                                              )
        Car.objects.create(dossier=self.dossier,mark='lala')
    def test_dossier_put_ok(self):
        self.client.login(username='maksim',password='123456')
        data = {
                "id": 23,
                "full_name": "maks312312312",
                "date_birth": "1998-07-26",
                "gender": "M",
                "cars": [
                        {
                            "mark": "toyota camry"
                        }
                    ]
                }
        self.response = self.client.put(self.url,data=data)
        print(self.response.json())
        self.assertEqual(self.response.status_code,status.HTTP_200_OK)

    def test_delete(self):
        self.client.login(username='maksim', password='123456')
        self.response = self.client.delete(self.url)
        print(self.response.json())
        self.assertEqual(self.response.status_code,status.HTTP_200_OK)







