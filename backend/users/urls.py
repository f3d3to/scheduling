# users/urls.py

from django.urls import path
from .views import UsuarioListCreateView, UsuarioRetrieveUpdateDestroyView

app_name = "users"

urlpatterns = [
    path('usuarios/', UsuarioListCreateView.as_view(), name='usuario-list-create'),
    path('usuarios/<int:pk>/', UsuarioRetrieveUpdateDestroyView.as_view(), name='usuario-retrieve-update-destroy'),
]
