from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from .models import Document
from .factory import populate_test_db_users, populate_test_db_docs


class TestDocumentRulesGet(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('documents-list')
        # create user and group
        populate_test_db_users(User, Group)
        # create docs for users
        populate_test_db_docs(Document)

    def test_sergeant_permissions(self):
        self.client.login(username='sergeant', password='123456')
        self.response = self.client.get(self.url)
        print(self.response.json())
        self.assertContains(self.response, text='public document', status_code=200)

    def test_sergeant_no_permissions(self):
        self.client.login(username='sergeant', password='123456')
        self.response = self.client.get(self.url)
        # print(self.response.json())
        self.assertNotContains(self.response, text='secret document', status_code=200)

    def test_document_create(self):
        self.client.login(username='sergeant', password='123456')
        data = {
            'title': 'kn;vd',
            'status': 'active',
            'text': '1234',
            'date_expired': '2020-06-06',
            'document_root': 'public'
        }
        self.response = self.client.post(self.url, data)
        print(self.response.json())
        self.assertNotEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_general_error(self):
        self.client.login(username='general', password='123456')
        data = {
            'title': 'asdf',
            'status': 'active',
            'text': '1234',
            'date_expired': '2020-06-06',
            'document_root': 'top-secret'
        }
        self.response = self.client.post(self.url, data)
        self.assertContains(self.response,text='you have nit permision',status_code=400)


    def test_president_create(self):
        self.client.login(username='president', password='123456')
        data = {
            'title': 'asdf',
            'status': 'active',
            'text': '1234',
            'date_expired': '2020-06-06',
            'document_root': 'top-secret'
        }
        self.response = self.client.post(self.url, data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


class TestDocumentRulesPost(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('documents-list')
        populate_test_db_users(User, Group)

    def test_no_permission_common(self):
        data = {
            "title": "bdlbf",
            "text": "123",
            'status': 'active',
            'date_expired': '2020-08-09',
            'document_root': 'public'
        }
        self.client.login(username='common', password='123456')
        self.response = self.client.post(self.url, data)

        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_permission_sergeant(self):
        data = {
            "title": "Test",
            "text": "123",
            'status': 'active',
            'date_expired': '2020-08-09',
            'document_root': 'public'
        }
        self.client.login(username='sergeant', password='123456')
        self.response = self.client.post(self.url, data)
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_general(self):
        data = {
            "title": "doc for general",
            "text": "secret doc",
            'status': 'active',
            'date_expired': '2020-08-09',
            'document_root': 'public'
        }
        self.client.login(username='general', password='123456')
        self.response = self.client.post(self.url, data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_permission_president(self):
        data = {
            "title": "Document for president",
            "text": "secret document",
            'status': 'active',
            'date_expired': '2020-08-09',
            'document_root': 'public'
        }
        self.client.login(username='president', password='123456')
        self.response = self.client.post(self.url, data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_no_permission_president_private(self):
        data = {
            "title": "Document for president",
            "text": "secret document",
            'status': 'active',
            'date_expired': '2020-08-09',
            'document_root': 'private'
        }
        self.client.login(username='president', password='123456')
        self.response = self.client.post(self.url, data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)




