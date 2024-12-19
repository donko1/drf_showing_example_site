# Кастопные пагинаторы. Их можно в settings.txt

from rest_framework import pagination

class CapitalsPaginator(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10
    page_query_param = 'page'

class CapitalsPaginatorLimitOffset(pagination.LimitOffsetPagination):
    default_limit = 3
    page_size_query_param = 'page_size'
    max_page_size = 5

class CapitalsCursorPagination(pagination.CursorPagination):
    page_size = 3
    ordering = '-capital_population'  # Сортировка по населению (по убыванию)
    cursor_query_param = 'cursor'     # Параметр для курсора в URL