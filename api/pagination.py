from rest_framework.pagination import PageNumberPagination


class RidesPagination(PageNumberPagination):
    # Page size was not specified in requirement.
    page_size = 20
    max_page_size = 40
    page_size_query_param = 'page_size'