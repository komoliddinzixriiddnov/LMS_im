# from rest_framework.pagination import PageNumberPagination
# from django.conf import settings

# class Pagination(PageNumberPagination):
#     # Asosiy sahifa hajmi
#     page_size = getattr(settings, 'PAGINATION_PAGE_SIZE', 20)
#
#     # Sahifa hajmini so'rov orqali o'zgartirish parametri
#     page_size_query_param = getattr(settings, 'PAGINATION_PAGE_SIZE_QUERY_PARAM', 'page_size')
#
#     # Maksimal sahifa hajmi
#     max_page_size = getattr(settings, 'PAGINATION_MAX_PAGE_SIZE', 50)
#


from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound
from django.conf import settings

class Pagination(PageNumberPagination):
    page_size = getattr(settings, 'PAGINATION_PAGE_SIZE', 20)
    page_size_query_param = getattr(settings, 'PAGINATION_PAGE_SIZE_QUERY_PARAM', 'page_size')
    max_page_size = getattr(settings, 'PAGINATION_MAX_PAGE_SIZE', 50)

    def get_page_size(self, request):
        page_size = super().get_page_size(request)
        if page_size > self.max_page_size:
            return self.max_page_size
        return page_size

    def get_paginated_response(self, data):
        return {
            'total_items': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'page_number': self.page.number,
            'page_size': self.get_page_size(self.request),
            'next_page': self.get_next_link(),
            'previous_page': self.get_previous_link(),
            'results': data,
        }

    def paginate_queryset(self, queryset, request, view=None):
        try:
            return super().paginate_queryset(queryset, request, view)
        except NotFound:
            raise NotFound("Sahifa topilmadi. Iltimos, to'g'ri sahifa raqamini kiriting.")