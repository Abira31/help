from rest_framework.pagination import PageNumberPagination

class SubjectPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'

class StudentPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
