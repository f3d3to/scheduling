from django_filters import rest_framework as filters
from .models import TareaTimer, Sesion

class TareaTimerFilter(filters.FilterSet):
    """
    Filtro para el modelo Tarea.
    """
    cantidad_para_completar = filters.RangeFilter(help_text="Filtra tareas por rango de cantidad para completar.")
    cantidad_completadas = filters.RangeFilter(help_text="Filtra tareas por rango de cantidad completada.")

    class Meta:
        model = TareaTimer
        fields = ['tarea', 'cantidad_para_completar', 'cantidad_completadas']

class SesionFilter(filters.FilterSet):
    """
    Filtro para el modelo Sesion.
    """
    nombre = filters.CharFilter(lookup_expr='icontains', help_text="Filtra sesiones por nombre (búsqueda parcial).")
    duracion_minutos = filters.RangeFilter(help_text="Filtra sesiones por rango de duración en minutos.")
    es_obligatoria = filters.BooleanFilter(help_text="Filtra sesiones según si son obligatorias o no.")
    fecha_creacion = filters.DateFromToRangeFilter(help_text="Filtra sesiones por rango de fechas de creación.")

    class Meta:
        model = Sesion
        fields = ['nombre', 'duracion_minutos', 'es_obligatoria', 'fecha_creacion']
