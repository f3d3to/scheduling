from django_filters import rest_framework as filters
from .models import Planificador, Actividad, Tarea, EstructuraPlanificador

class PlanificadorFilter(filters.FilterSet):
    """
    Filtro para el modelo Planificador.
    """
    nombre = filters.CharFilter(lookup_expr='icontains', help_text="Filtra planificadores por nombre (búsqueda parcial).")
    descripcion = filters.CharFilter(lookup_expr='icontains', help_text="Filtra planificadores por descripción (búsqueda parcial).")
    estructura = filters.NumberFilter(field_name="estructura__id", help_text="Filtra planificadores por estructura asociada.")
    fecha_creacion = filters.DateFromToRangeFilter(help_text="Filtra planificadores por rango de fechas de creación.")
    usuario = filters.NumberFilter(field_name="usuario__id", help_text="Filtra planificadores por usuario.")

    class Meta:
        model = Planificador
        fields = ['nombre', 'descripcion', 'estructura', 'fecha_creacion', 'usuario']


class ActividadFilter(filters.FilterSet):
    """
    Filtro para el modelo Actividad.
    """
    nombre = filters.CharFilter(lookup_expr='icontains', help_text="Filtra actividades por nombre (búsqueda parcial).")
    descripcion = filters.CharFilter(lookup_expr='icontains', help_text="Filtra actividades por descripción.")
    estado = filters.NumberFilter(field_name="estado__id", help_text="Filtra actividades por estado asociado.")
    planificador = filters.NumberFilter(field_name="planificador__id", help_text="Filtra actividades por planificador.")
    fecha_inicio = filters.DateFromToRangeFilter(help_text="Filtra actividades por rango de fechas de inicio.")
    fecha_fin = filters.DateFromToRangeFilter(help_text="Filtra actividades por rango de fechas de finalización.")

    class Meta:
        model = Actividad
        fields = ['nombre', 'descripcion', 'estado', 'planificador', 'fecha_inicio', 'fecha_fin']


class TareaFilter(filters.FilterSet):
    """
    Filtro para el modelo Tarea.
    """
    nombre = filters.CharFilter(lookup_expr='icontains', help_text="Filtra tareas por nombre (búsqueda parcial).")
    descripcion = filters.CharFilter(lookup_expr='icontains', help_text="Filtra tareas por descripción.")
    estado = filters.NumberFilter(field_name="estado__id", help_text="Filtra tareas por estado asociado.")
    actividad = filters.NumberFilter(field_name="actividad__id", help_text="Filtra tareas por actividad asociada.")
    fecha_limite = filters.DateFromToRangeFilter(help_text="Filtra tareas por rango de fechas límite.")

    class Meta:
        model = Tarea
        fields = ['nombre', 'descripcion', 'estado', 'actividad', 'fecha_limite']


class EstructuraPlanificadorFilter(filters.FilterSet):
    """
    Filtro para el modelo EstructuraPlanificador.
    """
    nombre = filters.CharFilter(lookup_expr='icontains', help_text="Filtra estructuras por nombre (búsqueda parcial).")
    descripcion = filters.CharFilter(lookup_expr='icontains', help_text="Filtra estructuras por descripción.")
    usuario = filters.NumberFilter(field_name="usuario__id", help_text="Filtra estructuras por usuario asociado.")

    class Meta:
        model = EstructuraPlanificador
        fields = ['nombre', 'descripcion', 'usuario']
