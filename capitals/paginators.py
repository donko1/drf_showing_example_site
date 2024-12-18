
# Кастопные пагинаторы. Их можно в settings.txt

from rest_framework import pagination

class CapitalsPaginator(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 5

# class StandardResultsSetPagination(pagination.PageNumberPagination):
#     page_size = 100
#     page_size_query_param = 'page_size'
#     max_page_size = 1000
