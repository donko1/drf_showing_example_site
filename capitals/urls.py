from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import CapitalViewSetWithPaginator

# Создаем router и регистрируем наши ViewSet'ы
router = DefaultRouter()
router.register(r'capitals', views.CapitalViewSet, basename='capital')
router.register(r'capitals-custom', views.CapitalViewSetNotModel, basename='capital-custom')
router.register(r'capitals-only-admin', views.CapitalViewSetModel, basename='capital-admin')
router.register(r'capitals-paginated', CapitalViewSetWithPaginator, basename='capital-paginated')

urlpatterns = [
    path('', views.home, name='home'),
    path('serialize/', views.serialize_data, name='serialize'),
    path('demonstrate/', views.demonstrate_serializer, name='demonstrate'),
    path('partial-update/', views.partial_update_demo, name='partial-update'),
    path('nested/', views.nested_serializer_demo, name='nested_serializer_demo'),
    path('depth/', views.depth_demo, name='depth_demo'),
    # Добавляем все URL'ы из router с префиксом 'api/'
    path('api/', include(router.urls)),
]
