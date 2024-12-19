from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .models import Capital
from .serializers import CapitalSerializer, CapitalNestedSerializer, CapitalFlatSerializer, CapitalDepthSerializer, CapitalDepth2Serializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from .paginators import CapitalsPaginator
from .forms import JSONInputForm

class CapitalViewSet(viewsets.ModelViewSet): 
    queryset = Capital.objects.all()
    serializer_class = CapitalSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer): # Этот метод аналогичен нижнему, но для работы необходимо определять поле автор в сериализаторе(чекай код)
        serializer.save(author=self.request.user)

    # def create(self, request):
    #     data = request.data
    #     data["author"] = request.user.pk
    #     serializer = CapitalSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CapitalViewSetModel(viewsets.ModelViewSet): # Или viewsets.ReadOnlyModelViewSet только для чтения
    permission_classes = [permissions.IsAdminUser]
    queryset = Capital.objects.all()
    serializer_class = CapitalSerializer

class CapitalViewSetNotModel(viewsets.ViewSet):
    """
    ViewSet для работы со столицами без использования ModelViewSet.
    Реализует все CRUD операции вручную.
    """
    def list(self, request):
        """
        Получение списка всех столиц
        GET /api/capitals-custom/
        
        Returns:
            Response: Список всех столиц в формате JSON
        """
        queryset = Capital.objects.all()
        serializer = CapitalSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """
        Создание новой столицы
        POST /api/capitals-custom/
        
        Args:
            request.data: Данные новой столицы в формате JSON
        
        Returns:
            Response: 
            - 201: Созданная столица в формате JSON
            - 400: Ошибки валидации
        """
        serializer = CapitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """
        Получение информации о конкретной столице
        GET /api/capitals-custom/{id}/
        
        Args:
            pk: ID столицы
        
        Returns:
            Response:
            - 200: Данные столицы в формате JSON
            - 404: Столица не найдена
        """
        try:
            capital = Capital.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = CapitalSerializer(capital)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        """
        Полное обновление информации о столице
        PUT /api/capitals-custom/{id}/
        
        Args:
            pk: ID столицы
            request.data: Новые данные столицы (требуются ВСЕ поля)
        
        Returns:
            Response:
            - 200: Обновленные данные столицы
            - 400: Ошибки валидации
            - 404: Столица не найдена
        """
        try:
            capital = Capital.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = CapitalSerializer(capital, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        """
        Частичное обновление информации о столице
        PATCH /api/capitals-custom/{id}/
        
        Args:
            pk: ID столицы
            request.data: Новые данные столицы (можно указать ТОЛЬКО измененные поля)
        
        Returns:
            Response:
            - 200: Обновленные данные столицы
            - 400: Ошибки валидации
            - 404: Столица не найдена
        """
        try:
            capital = Capital.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = CapitalSerializer(capital, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """
        Удаление столицы
        DELETE /api/capitals-custom/{id}/
        
        Args:
            pk: ID столицы для удаления
        
        Returns:
            Response:
            - 204: Столица успешно удалена
            - 404: Столица не найдена
        """
        try:
            capital = Capital.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        capital.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def make_primary(self, request, pk=None):
        """
        Кастомное действие для установки столицы как основной.
        POST /api/capitals-custom/{id}/make_primary/
        
        Args:
            pk: ID столицы
        
        Returns:
            Response:
            - 200: Столица успешно помечена как основная
            - 404: Столица не найдена
        """
        try:
            capital = Capital.objects.get(pk=pk)
            # Сбрасываем флаг у всех столиц
            Capital.objects.all().update(is_primary=False)
            # Устанавливаем флаг у текущей столицы
            capital.is_primary = True
            capital.save()
            return Response({'status': 'Столица установлена как основная'})
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def primary(self, request):
        """
        Получить информацию об основной столице.
        GET /api/capitals-custom/primary/
        
        Returns:
            Response:
            - 200: Данные основной столицы
            - 404: Основная столица не найдена
        """
        try:
            capital = Capital.objects.get(is_primary=True)
            serializer = CapitalSerializer(capital)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(
                {'error': 'Основная столица не найдена'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'], url_path='set-population')
    def set_population(self, request, pk=None):
        """
        Установить население для столицы
        
        Args:
            request: Запрос с population в теле
            pk: ID столицы
            
        Returns:
            Response: Обновленные данные столицы
        """
        try:
            capital = Capital.objects.get(pk=pk)
        except Capital.DoesNotExist:  # type: ignore
            return Response({'error': 'Capital not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Получаем новое значение населения из тела запроса
        new_population = request.data.get('population')
        if new_population is None:
            return Response(
                {'error': 'Population value is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Преобразуем в целое число и сохраняем
            capital.capital_population = int(new_population)
            capital.save()
            return Response({'message': 'Population updated successfully'})
        except ValueError:
            return Response(
                {'error': 'Invalid population value'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, url_path='by-population')
    def by_population(self, request):
        """
        Получить список столиц, отсортированный по населению
        Опционально можно указать минимальное население через query parameter min_population
        
        Args:
            request: Запрос с опциональным параметром min_population
            
        Returns:
            Response: Отсортированный список столиц
        """
        queryset = Capital.objects.all().order_by('-capital_population')
        
        # Получаем минимальное население из query parameters
        min_population = request.query_params.get('min_population')
        if min_population:
            try:
                min_population = int(min_population)
                queryset = queryset.filter(capital_population__gte=min_population)
            except ValueError:
                return Response(
                    {'error': 'Invalid min_population value'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = CapitalSerializer(queryset, many=True)
        return Response(serializer.data)

class CapitalViewSetWithPaginator(viewsets.ModelViewSet):
    """
    ViewSet для демонстрации пагинации.
    Возвращает по 3 объекта на страницу.
    """
    queryset = Capital.objects.all()
    serializer_class = CapitalDepthSerializer
    pagination_class = CapitalsPaginator

def serialize_data(request):
    form = JSONInputForm()
    if request.method == "POST":
        form = JSONInputForm(request.POST)
        if form.is_valid():
            try:
                json_data = form.cleaned_data['json_data']
                if isinstance(json_data, str):
                    data = json.loads(json_data)
                else:
                    data = json_data
                serializer = CapitalSerializer(data=data, context={'request': request})
                if serializer.is_valid(raise_exception=False): # raise_exception=True позволяет 
                    # при нарушении валидации выбросить исключение
                    serializer.save()
                    return JsonResponse(serializer.data, status=201)
                else:
                    return JsonResponse(serializer.errors, status=400)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON format'}, status=400)
            
    return render(request, 'capitals/serialize_data.html', {'form': form})

def home(request):
    capitals = Capital.objects.all()
    return render(request, 'capitals/home.html', {'capitals': capitals})

def demonstrate_serializer(request):
    # Создаем или получаем тестовый объект Capital
    test_capital = Capital.objects.first()
    if not test_capital:
        user = User.objects.first()
        test_capital = Capital.objects.create(
            capital_city="Oslo",
            capital_population=693494,
            country="Norway",
            author=user
        )
    
    # Демонстрация instance - существующий объект
    serializer_with_instance = CapitalSerializer(instance=test_capital, context={'request': request})
    instance_explanation = """
    Instance Data - это данные, которые уже существуют в базе данных.
    Мы получаем их, передавая существующий объект в параметр instance сериализатора.
    Эти данные доступны через serializer.data
    """
    
    # Демонстрация initial_data - новые данные для создания объекта
    initial_data = {
        "capital_city": "Stockholm",
        "capital_population": 975551,
        "country": "Sweden",
        "author": test_capital.author.id  # Используем тот же author.id для примера
    }
    serializer_with_initial = CapitalSerializer(data=initial_data, context={'request': request})
    initial_explanation = """
    Initial Data - это новые данные, которые мы хотим сохранить в базу данных.
    Мы передаем их в параметр data сериализатора.
    Эти данные доступны через serializer.initial_data
    """
    
    is_valid = serializer_with_initial.is_valid()
    
    context = {
        'instance_data': json.dumps(serializer_with_instance.data, indent=2),
        'instance_explanation': instance_explanation,
        'initial_data': json.dumps(initial_data, indent=2),
        'initial_explanation': initial_explanation,
        'is_valid': is_valid,
        'validation_errors': json.dumps(serializer_with_initial.errors, indent=2) if not is_valid else None
    }
    
    return render(request, 'capitals/demonstrate.html', context)

def partial_update_demo(request):
    # Получаем или создаем тестовый объект
    test_capital = Capital.objects.first()
    if not test_capital:
        user = User.objects.first()
        test_capital = Capital.objects.create(
            capital_city="Oslo",
            capital_population=693494,
            country="Norway",
            author=user
        )

    if request.method == "POST":
        # Получаем данные для частичного обновления
        partial_data = {
            'capital_population': request.POST.get('capital_population', None)
        }
        # Удаляем None значения
        partial_data = {k: v for k, v in partial_data.items() if v is not None}
        
        # Создаем сериализатор с partial=True, позволяет сделать частичное обновление
        # Затрагивает только часть полей, а остальные оставляет в норме
        serializer = CapitalSerializer(test_capital, data=partial_data, partial=True)
        
        # Сначала проверяем валидность
        is_valid = serializer.is_valid()
        
        if is_valid:
            serializer.save()
            update_success = True
            errors = None
        else:
            update_success = False
            errors = serializer.errors
    else:
        serializer = CapitalSerializer(test_capital)
        update_success = None
        errors = None

    context = {
        'capital': test_capital,
        'original_data': CapitalSerializer(test_capital).data,
        'update_success': update_success,
        'errors': errors,
    }
    return render(request, 'capitals/partial_update.html', context)

def nested_serializer_demo(request):
    # Получаем все столицы с их авторами
    capitals = Capital.objects.select_related('author').all()
    
    # Используем вложенный сериализатор
    serializer = CapitalNestedSerializer(capitals, many=True)
    
    # Подготовим примеры для демонстрации
    example_data = {
        'simple_serializer': CapitalSerializer(capitals.first()).data,
        'nested_serializer': serializer.data[0] if serializer.data else None,
    }
    
    explanation = """
    Вложенные сериализаторы позволяют включать связанные данные в ответ API.
    В этом примере мы видим разницу между простым и вложенным сериализатором:
    
    1. Простой сериализатор показывает только ID автора
    2. Вложенный сериализатор показывает полную информацию об авторе
    """
    
    context = {
        'capitals': serializer.data,
        'example_data': example_data,
        'explanation': explanation
    }
    
    return render(request, 'capitals/nested_serializer.html', context)

def depth_demo(request):
    # Получаем столицу для демонстрации
    capital = Capital.objects.select_related('author').first()
    
    if not capital:
        # Если нет данных, создаем тестовый объект
        user = User.objects.first()
        capital = Capital.objects.create(
            capital_city="Oslo",
            capital_population=693494,
            country="Norway",
            author=user
        )
    
    # Сериализуем один и тот же объект с разными уровнями depth
    flat_serializer = CapitalFlatSerializer(capital)
    depth1_serializer = CapitalDepthSerializer(capital)
    depth2_serializer = CapitalDepth2Serializer(capital)
    
    explanation = """
    Параметр depth в сериализаторах Django REST Framework определяет глубину сериализации связанных полей:
    
    - depth = 0 (или не указан): Возвращает только ID связанных объектов
    - depth = 1: Сериализует первый уровень связанных объектов
    - depth = 2: Сериализует два уровня связанных объектов
    
    Это особенно полезно когда:
    1. У вас есть сложные вложенные отношения
    2. Вы хотите автоматически сериализовать связанные объекты
    3. Вам нужно контролировать глубину сериализации
    """
    
    context = {
        'flat_data': flat_serializer.data,
        'depth1_data': depth1_serializer.data,
        'depth2_data': depth2_serializer.data,
        'explanation': explanation
    }
    
    return render(request, 'capitals/depth_demo.html', context)

class GetCapitalInfoView(APIView):
    def get(self, request):
        queryset = Capital.objects.all()
        serializer_for_queryset = CapitalSerializer(
            instance=queryset, 
            many=True 
        )
        return Response(serializer_for_queryset.data)