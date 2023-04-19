from rest_framework.pagination import PageNumberPagination
class MyPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "limit"