from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Создаем router и регистрируем наши ViewSet'ы
router = DefaultRouter()
router.register(r"capitals", views.CapitalViewSet, basename="capital")
router.register(
    r"capitals-custom", views.CapitalViewSetNotModel, basename="capital-custom"
)
router.register(
    r"capitals-only-admin", views.CapitalViewSetModel, basename="capital-admin"
)
router.register(
    r"capitals-paginated",
    views.CapitalViewSetWithPaginator,
    basename="capital-paginated",
)
router.register(
    r"capitals-paginated-offset",
    views.CapitalViewSetWithPaginatorOffset,
    basename="capital-paginated-offset",
)
router.register(
    r"capitals-paginated-cursor",
    views.CapitalViewSetWithCursorPaginator,
    basename="capital-paginated-cursor",
)
router.register(
    r"capitals-filter1",
    views.CapitalViewSetWithFilterByPopulation,
    basename="capitals-filter1",
)
router.register(
    r"capitals-filter2", views.CapitalViewSetGenericFilter, basename="capitals-filter2"
)
router.register(
    r"capitals-filter3", views.CapitalViewSetSearchFilter, basename="capitals-filter3"
)
router.register(
    r"capitals-filter4", views.CapitalViewSetOrderingFilter, basename="capitals-filter4"
)
router.register(
    r"capitals-throttling1",
    views.CapitalViewSetWithThrottling,
    basename="capitals-throttling1",
)
router.register(
    r"capitals-throttling2",
    views.CapitalViewSetWithThrottlingAdmin,
    basename="capitals-throttling2",
)
router.register(
    r"capitals-throttling3",
    views.CapitalViewSetWithThrottlingWithScope,
    basename="capitals-throttling3",
)

# Регистрируем версионный ViewSet
router.register(r'capitals-with-versions', views.CapitalViewSetWithVersioning, basename='capital-with-versions')

# Создаем роутеры для разных версий API
router_v1 = DefaultRouter()
router_v2 = DefaultRouter()

# Регистрируем версионный ViewSet в разных пространствах имен
router_v1.register(r'capitals-ns', views.CapitalViewSetWithNamespaceVersioning, basename='capital-ns')
router_v2.register(r'capitals-ns', views.CapitalViewSetWithNamespaceVersioning, basename='capital-ns')

urlpatterns = [
    path("", views.home, name="home"),
    path("api/", include(router.urls)),
    path('api/v1/', include((router_v1.urls, 'v1'), namespace='v1')),
    path('api/v2/', include((router_v2.urls, 'v2'), namespace='v2')),
    path("api-auth/", include("rest_framework.urls")),
    path("serialize/", views.serialize_data, name="serialize"),
    path("demonstrate/", views.demonstrate_serializer, name="demonstrate"),
    path("partial-update/", views.partial_update_demo, name="partial-update"),
    path("nested/", views.nested_serializer_demo, name="nested_serializer_demo"),
    path("depth/", views.depth_demo, name="depth_demo"),
    path("api-docs/", views.api_docs, name="api_docs"),
]
