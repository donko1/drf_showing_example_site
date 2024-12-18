from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Capital

class CapitalModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.capital = Capital.objects.create(
            country='Norway',
            capital_city='Oslo',
            capital_population=693494,
            author=self.user
        )

    def test_capital_creation(self):
        self.assertEqual(self.capital.country, 'Norway')
        self.assertEqual(self.capital.capital_city, 'Oslo')
        self.assertEqual(self.capital.capital_population, 693494)
        self.assertEqual(self.capital.author, self.user)

    def test_capital_str_method(self):
        self.assertEqual(str(self.capital), 'Oslo - Norway')

class CapitalAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.capital1 = Capital.objects.create(
            country='Norway',
            capital_city='Oslo',
            capital_population=693494,
            author=self.user
        )
        self.capital2 = Capital.objects.create(
            country='Sweden',
            capital_city='Stockholm',
            capital_population=975551,
            author=self.user
        )
        self.url = reverse('capital-list')

    def test_get_capitals_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verify the structure and content of the response
        self.assertEqual(response.data[0]['capital_city'], 'Oslo')
        self.assertEqual(response.data[0]['capital_population'], 693494)
        self.assertEqual(response.data[0]['author'], 'testuser')
        
        self.assertEqual(response.data[1]['capital_city'], 'Stockholm')
        self.assertEqual(response.data[1]['capital_population'], 975551)
        self.assertEqual(response.data[1]['author'], 'testuser')
