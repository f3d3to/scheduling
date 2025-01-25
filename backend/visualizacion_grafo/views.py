# Third Party
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Django
from django.db.models import Q
# Proyecto
from .models import VisualizacionGrafo
from .serializers import VisualizacionGrafoSerializer
from .models import VisualizacionGrafo, Materia, MateriaEstudiante, NodoGrafo, EnlaceGrafo


class VisualizacionGrafoListCreateView(ListCreateAPIView):
    """
    Vista para listar y crear visualizaciones de grafos.
    """
    queryset = VisualizacionGrafo.objects.all()
    serializer_class = VisualizacionGrafoSerializer

class VisualizacionGrafoRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Vista para obtener, actualizar y eliminar una visualización de grafo específica.
    """
    queryset = VisualizacionGrafo.objects.all()
    serializer_class = VisualizacionGrafoSerializer
    lookup_field = 'plan_de_estudio_id'

class GrafoFiltradoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, plan_de_estudio_id):
        try:
            # Obtener la visualización de grafo
            visualizacion = VisualizacionGrafo.objects.get(plan_de_estudio_id__id=plan_de_estudio_id)
        except VisualizacionGrafo.DoesNotExist:
            return Response({'error': 'Visualización no encontrada'}, status=404)

        # Obtener parámetros de filtro
        filters = request.query_params.dict()
        promocionadas = filters.pop('promocionadas', None)
        disponibles = filters.pop('disponibles', None)

        # Identificar filtros activos
        filtros_activos = {
            'promocionadas': promocionadas,
            'disponibles': disponibles,
        }

        # Base queryset de materias del plan
        materias = Materia.objects.filter(plan_de_estudio=visualizacion.plan_de_estudio)

        # Aplicar filtros dinámicos para Materia
        allowed_filters = {
            'materia': 'codigo',
            'nombre__icontains': 'nombre__icontains',
            'ciclo': 'ciclo',
            'creditos': 'creditos',
            'anio': 'anio',
            'formato_didactico': 'formato_didactico',
            'condicion': 'condicion',
        }

        # Filtro de correlativas (por código de materia)
        if 'correlativas__in' in filters:
            codigos_correlativas = filters['correlativas__in'].split(',')
            # Obtener IDs de las materias correlativas
            materias_correlativas = Materia.objects.filter(
                codigo__in=codigos_correlativas
            ).values_list('id', flat=True)
            # Filtrar materias que tengan estas correlativas
            materias = materias.filter(correlativas__in=materias_correlativas)

        if 'estado' in filters:
            materias = materias.filter(estudiantes__estado=filters['estado'], estudiantes__estudiante=request.user)

        for param, field in allowed_filters.items():
            if param in filters:
                value = filters[param]
                if '__in' in param:
                    materias = materias.filter(**{field + '__in': value.split(',')})
                else:
                    materias = materias.filter(**{field: value})


        # Obtener nodos y enlaces filtrados
        nodos_filtrados = NodoGrafo.objects.filter(
            grafo=visualizacion,
            materia__in=materias
        )
        nodos_ids = nodos_filtrados.values_list('id', flat=True)

        enlaces_filtrados = EnlaceGrafo.objects.filter(
            grafo=visualizacion,
            fuente__in=nodos_ids,
            destino__in=nodos_ids
        )
        # Serializar datos con colores computados
        data = {
            'nodos': [
                nodo.to_dict(request.user, filtros_activos)
                for nodo in nodos_filtrados
            ],
            'enlaces': [
                enlace.to_dict(request.user, filtros_activos)
                for enlace in enlaces_filtrados
            ],
        }

        return Response(data)