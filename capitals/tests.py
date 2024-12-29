from django.test import TestCase
from rest_framework.test import APITestCase, APIClient, APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
from .models import Capital
from .serializers import CapitalSerializer, CapitalNestedSerializer
from rest_framework.authtoken.models import Token
from .views import CapitalViewSet

class CapitalModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.capital = Capital.objects.create(
            country='Norway',
            capital_city='Oslo',
            capital_population=693494,
            author=self.user
        )

    def test_capital_creation(self):
        """Test the creation of a Capital instance"""
        self.assertEqual(self.capital.country, 'Norway')
        self.assertEqual(self.capital.capital_city, 'Oslo')
        self.assertEqual(self.capital.capital_population, 693494)
        self.assertEqual(self.capital.author, self.user)

class CapitalAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.capital = Capital.objects.create(
            country='Norway',
            capital_city='Oslo',
            capital_population=693494,
            author=self.user
        )

    def test_get_capitals_list(self):
        """Test getting list of capitals"""
        url = reverse('capital-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['country'], 'Norway')

class CapitalSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.capital = Capital.objects.create(
            country='Sweden',
            capital_city='Stockholm',
            capital_population=975551,
            author=self.user
        )
        self.serializer = CapitalSerializer(instance=self.capital)

    def test_contains_expected_fields(self):
        """Проверяем, что сериализатор содержит ожидаемые поля"""
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set(['pk', 'country', 'capital_city', 'capital_population'])  # author is HiddenField
        )

    def test_population_field_content(self):
        """Проверяем корректность значения поля population"""
        data = self.serializer.data
        self.assertEqual(data['capital_population'], 975551)

class CapitalViewSetTests(APITestCase):
    """
    Тесты для ViewSet Capital.
    APITestCase предоставляет удобный способ тестирования REST API,
    включая аутентификацию и работу с запросами/ответами.
    """

    def setUp(self):
        """
        Подготовка данных для тестов, включая создание пользователя
        и настройку аутентификации.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.capital = Capital.objects.create(
            country='Norway',
            capital_city='Oslo',
            capital_population=693494,
            author=self.user
        )
        self.url = reverse('capital-list')

    def test_get_capitals_list(self):
        """Проверяем получение списка столиц"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_capital(self):
        """Проверяем создание новой столицы"""
        data = {
            'country': 'Finland',
            'capital_city': 'Helsinki',
            'capital_population': 631695,
            'author': self.user.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Capital.objects.count(), 2)

    def test_get_capital_detail(self):
        """Проверяем получение деталей конкретной столицы"""
        url = reverse('capital-detail', kwargs={'pk': self.capital.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['country'], 'Norway')

class CapitalViewSetWithFactoryTests(TestCase):
    """
    Тесты с использованием APIRequestFactory.
    Factory позволяет создавать запросы на низком уровне и
    дает больше контроля над процессом тестирования.
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.capital = Capital.objects.create(
            country='Denmark',
            capital_city='Copenhagen',
            capital_population=794128,
            author=self.user
        )

    def test_get_capitals_with_factory(self):
        """
        Тестирование GET запроса с использованием factory.
        Factory позволяет создавать запросы без запуска реального сервера.
        """
        from .views import CapitalViewSet
        view = CapitalViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/capitals/')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_capital_with_factory(self):
        """
        Тестирование POST запроса с использованием factory.
        Показывает, как работать с запросами, требующими аутентификации.
        """
        from .views import CapitalViewSet
        view = CapitalViewSet.as_view({'post': 'create'})
        data = {
            'country': 'Iceland',
            'capital_city': 'Reykjavik',
            'capital_population': 122853,
            'author': self.user.id
        }
        request = self.factory.post('/api/capitals/', data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Capital.objects.count(), 2)

class CapitalFilterTests(APITestCase):
    """
    Тесты для проверки фильтрации в API.
    Демонстрирует тестирование query parameters и фильтров.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # Создаем несколько столиц для тестирования фильтров
        self.capitals = [
            Capital.objects.create(
                country='Norway',
                capital_city='Oslo',
                capital_population=693494,
                author=self.user
            ),
            Capital.objects.create(
                country='Sweden',
                capital_city='Stockholm',
                capital_population=975551,
                author=self.user
            ),
            Capital.objects.create(
                country='Finland',
                capital_city='Helsinki',
                capital_population=631695,
                author=self.user
            )
        ]

    def test_filter_by_population(self):
        """Проверяем фильтрацию по населению"""
        url = reverse('capitals-filter1-list')
        response = self.client.get(f'{url}?population=700000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Только Stockholm должен пройти фильтр

    def test_search_filter(self):
        """Проверяем поиск по названию города"""
        url = reverse('capitals-filter3-list')
        response = self.client.get(f'{url}?search=helsinki')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['capital_city'], 'Helsinki')

    def test_ordering_filter(self):
        """Проверяем сортировку результатов"""
        url = reverse('capitals-filter4-list')
        response = self.client.get(f'{url}?ordering=capital_city')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['capital_city'], 'Helsinki')  # Должен быть первым по алфавиту

class CapitalPaginationTests(APITestCase):
    """
    Тесты для проверки пагинации.
    Показывает, как тестировать пагинацию в API.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # Создаем 5 столиц для тестирования пагинации
        for i in range(5):
            Capital.objects.create(
                country=f'Country{i}',
                capital_city=f'City{i}',
                capital_population=100000 + i * 10000,
                author=self.user
            )

    def test_pagination(self):
        """Проверяем работу пагинации"""
        url = reverse('capital-paginated-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)  # Проверяем, что на странице 3 элемента
        self.assertIsNotNone(response.data['next'])  # Проверяем наличие ссылки на следующую страницу
        
        # Проверяем вторую страницу
        response = self.client.get(response.data['next'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Оставшиеся 2 элемента
        self.assertIsNone(response.data['next'])  # Следующей страницы быть не должно
