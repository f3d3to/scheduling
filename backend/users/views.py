# users/views.py

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Usuario
from .serializers import UsuarioSerializer
from .filters import UsuarioFilter
from django_filters.rest_framework import DjangoFilterBackend

class UsuarioListCreateView(ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UsuarioFilter
    # permission_classes = [IsAuthenticated]  # Asegura que solo los usuarios autenticados puedan acceder

    def perform_create(self, serializer):
        # Aquí puedes personalizar el comportamiento de la creación si es necesario
        serializer.save()

class UsuarioRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    # permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder
