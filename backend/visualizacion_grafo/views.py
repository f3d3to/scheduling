from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from .models import VisualizacionGrafo
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import VisualizacionGrafoSerializer

# Vista para listar y crear grafos
class VisualizacionGrafoListCreateView(ListCreateAPIView):
    """
    Vista para listar y crear visualizaciones de grafos.
    """
    queryset = VisualizacionGrafo.objects.all()
    serializer_class = VisualizacionGrafoSerializer
    # Considera agregar filter_backends y filterset_class si necesitas filtrar la lista de grafos

class VisualizacionGrafoRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Vista para obtener, actualizar y eliminar una visualización de grafo específica.
    """
    queryset = VisualizacionGrafo.objects.all()
    serializer_class = VisualizacionGrafoSerializer
    lookup_field = 'plan_id'

class GrafoFiltradoView(RetrieveAPIView):
    """
    Vista para obtener un grafo filtrado basado en el ID del plan y los parámetros de consulta.

    Utiliza RetrieveAPIView para obtener una instancia específica (el grafo).
    """
    queryset = VisualizacionGrafo.objects.all()
    lookup_field = 'plan_id'  # Usamos 'plan_id' como campo de búsqueda

    def get(self, request, *args, **kwargs):
        """
        Devuelve la representación JSON del grafo filtrado.
        """
        instance = self.get_object()
        usuario = request.user
        filtros = request.GET.dict()

        data = instance.generar_json_visualizacion(usuario if usuario.is_authenticated else None)

        # Aplicar filtros dinámicos
        data['nodos'] = self._aplicar_filtros(data['nodos'], filtros)
        data['enlaces'] = self._filtrar_enlaces(data['enlaces'], data['nodos'])

        return Response(data)

    def _aplicar_filtros(self, nodos, filtros):
        """
        Aplica filtros a la lista de nodos.
        """
        if 'aprobadas' in filtros:
            nodos = [n for n in nodos if n['metadata'].get('estado') == 'aprobada']
        if 'optativas' in filtros:
            nodos = [n for n in nodos if n['metadata'].get('es_optativa')]
        return nodos

    def _filtrar_enlaces(self, enlaces, nodos_filtrados):
        """
        Filtra los enlaces basándose en los nodos filtrados.
        """
        ids_nodos = {n['id'] for n in nodos_filtrados}
        return [e for e in enlaces if e['fuente'] in ids_nodos and e['destino'] in ids_nodos]