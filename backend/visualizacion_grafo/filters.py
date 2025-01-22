import django_filters as df
from .models import NodoGrafo, EnlaceGrafo
from users.models import MateriaEstudiante

class NodoFilter(df.FilterSet):
    estado = df.ChoiceFilter(
        method='filter_by_estado',
        choices=MateriaEstudiante.ESTADO_CHOICES,
        label="Estado de la materia"
    )

    class Meta:
        model = NodoGrafo
        fields = {
            'materia__nombre': ['icontains'],
            'materia__anio': ['exact'],
            'materia__es_optativa': ['exact']
        }

    def filter_by_estado(self, queryset, name, value):
        user = self.request.user
        return queryset.filter(
            materia__materiaestudiante__estudiante=user,
            materia__materiaestudiante__estado=value
        )

class EnlaceFilter(df.FilterSet):
    tipo_correlativa = df.CharFilter(
        field_name='materia__correlativas__tipo',
        lookup_expr='exact'
    )

    class Meta:
        model = EnlaceGrafo
        fields = {
            'fuente__materia__nombre': ['icontains'],
            'destino__materia__nombre': ['icontains']
        }