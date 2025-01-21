
from django_filters import rest_framework as filters
from .models import PlanDeEstudio, Materia

class PlanDeEstudioFilter(filters.FilterSet):
    class Meta:
        model = PlanDeEstudio
        fields = ['nombre', 'año_creacion', 'id']

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


class GrafoFilter(filters.FilterSet):
    plan_de_estudio__id = filters.NumberFilter(field_name='plan_de_estudio__id', lookup_expr='exact')
    estudiante_id = filters.NumberFilter(field_name='estudiante_id', lookup_expr='exact') #Este filtro se aplica a nivel de serializador

    class Meta:
        model = Materia
        fields = ['plan_de_estudio__id']