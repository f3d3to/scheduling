from django.urls import path
from .views import VisualizacionGrafoListCreateView, VisualizacionGrafoRetrieveUpdateDestroyView, GrafoFiltradoView

app = "visualizacion_grafo"

urlpatterns = [
    path('grafos/', VisualizacionGrafoListCreateView.as_view(), name='visualizaciongrafo-list-create'),
    path('grafos/<int:plan_de_estudio_id>/', VisualizacionGrafoRetrieveUpdateDestroyView.as_view(), name='visualizaciongrafo-detail'),
    path('grafos/filtrado/<int:plan_de_estudio_id>/', GrafoFiltradoView.as_view(), name='grafo_filtrado'),
]