from rest_framework.pagination import BasePagination
from rest_framework.response import Response

class NoLimitPagination(BasePagination):
    def paginate_queryset(self, queryset, request, view=None):
        # Devuelve todos los objetos sin paginación
        self.total = queryset.count()
        return list(queryset)

    def get_paginated_response(self, data):
        # Mantén la estructura de respuesta de paginación, pero sin límites
        return Response({
            'count': self.total,
            'results': data,
        })