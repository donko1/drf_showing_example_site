from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


# Создаем router и регистрируем наши ViewSet'ы
router = DefaultRouter()
router.register(r'capitals', views.CapitalViewSet, basename='capital')
router.register(r'capitals-custom', views.CapitalViewSetNotModel, basename='capital-custom')
router.register(r'capitals-only-admin', views.CapitalViewSetModel, basename='capital-admin')
router.register(r'capitals-paginated', views.CapitalViewSetWithPaginator, basename='capital-paginated')
router.register(r'capitals-paginated-offset', views.CapitalViewSetWithPaginatorOffset, basename='capital-paginated-offset')
router.register(r'capitals-paginated-cursor', views.CapitalViewSetWithCursorPaginator, basename='capital-paginated-cursor')
router.register(r'capitals-filter1', views.CapitalViewSetWithFilterByPopulation, basename='capitals-filter1')

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('serialize/', views.serialize_data, name='serialize'),
    path('demonstrate/', views.demonstrate_serializer, name='demonstrate'),
    path('partial-update/', views.partial_update_demo, name='partial-update'),
    path('nested/', views.nested_serializer_demo, name='nested_serializer_demo'),
    path('depth/', views.depth_demo, name='depth_demo'),
    path('api-docs/', views.api_docs, name='api_docs'),
]
