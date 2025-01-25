
import django_filters
from .models import Usuario

class UsuarioFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains', label="Buscar por nombre de usuario")
    email = django_filters.CharFilter(lookup_expr='icontains', label="Buscar por email")

    class Meta:
        model = Usuario
        fields = ['id','username', 'email']
