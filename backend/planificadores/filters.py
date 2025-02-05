import django_filters

from .models import (
    Estado, Planificador, Celda, Elemento, Actividad, Tarea,
    Objetivo,
)

class EstadoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    color = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Estado
        fields = ['nombre', 'color']

class PlanificadorFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    tipo = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Planificador
        fields = ['nombre', 'tipo']

class CeldaFilter(django_filters.FilterSet):
    contenido = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Celda
        fields = ['planificador', 'contenido']

class ElementoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    content_type = django_filters.CharFilter(field_name='content_type__model', lookup_expr='iexact')

    class Meta:
        model = Elemento
        fields = ['nombre', 'celda', 'content_type']

class ActividadFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    fecha_inicio = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Actividad
        fields = ['planificador', 'nombre', 'fecha_inicio', 'estado']

class TareaFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    fecha_limite = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Tarea
        fields = ['actividad', 'nombre', 'fecha_limite', 'estado', 'esta_realizada']

class ObjetivoFilter(django_filters.FilterSet):
    descripcion = django_filters.CharFilter(lookup_expr='icontains')
    fecha_objetivo = django_filters.DateFromToRangeFilter()
    completado = django_filters.BooleanFilter()

    class Meta:
        model = Objetivo
        fields = ['descripcion', 'fecha_objetivo', 'completado']
