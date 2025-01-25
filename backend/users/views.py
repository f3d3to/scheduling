# users/views.py

# Third Party
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.views import APIView
from rest_framework.response import Response
# Django
from core.settings import config
from django_filters.rest_framework import DjangoFilterBackend
# Proyecto
from .models import Usuario
from .serializers import UsuarioSerializer
from .filters import UsuarioFilter


# API JWT

class CustomTokenRefreshView(TokenRefreshView):
    pass

class CustomTokenVerifyView(TokenVerifyView):
    pass


class CustomTokenObtainPairView(TokenObtainPairView):
    pass

class UsuarioListCreateView(ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UsuarioFilter

    def get_permissions(self):
        """
        Sobrescribe el método para asignar diferentes permisos según la acción.
        """
        if self.request.method == 'POST':
            return [AllowAny()]  # Permite la creación sin autenticación
        return [IsAuthenticated()]  # Requiere autenticación para otras acciones (GET, etc.)


    def perform_create(self, serializer):
        # Aquí puedes personalizar el comportamiento de la creación si es necesario
        serializer.save()

class UsuarioRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
