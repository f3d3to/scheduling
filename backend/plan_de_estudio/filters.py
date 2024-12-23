
from django_filters import rest_framework as filters
from .models import PlanDeEstudio, Materia

class PlanDeEstudioFilter(filters.FilterSet):
    class Meta:
        model = PlanDeEstudio
        fields = ['nombre', 'año_creacion', 'id', 'planificador']

class MateriaFilter(filters.FilterSet):
    ciclo = filters.CharFilter(field_name='ciclo', lookup_expr='iexact')
    anio = filters.NumberFilter(field_name='anio')
    correlativas = filters.ModelChoiceFilter(
        field_name='correlativas',
        queryset=Materia.objects.all(),
        method='filtrar_correlativas'
    )

    class Meta:
        model = Materia
        fields = ['ciclo', 'anio', 'correlativas', 'codigo']

    def filtrar_correlativas(self, queryset, name, value):
        return queryset.filter(correlativas=value)

