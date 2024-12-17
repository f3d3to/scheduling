
from django.urls import path
from .views import PlanDeEstudioList, \
    MateriaList, DescargarPlanDeEstudioJSON, \
    MateriaCorrelativasTreeView, PlanDeEstudioCiclosView, \
    PlanDeEstudioGraphView

app_name = 'plan_de_estudio'


urlpatterns = [
    path('planes_de_estudio/', PlanDeEstudioList.as_view(), name='plan_de_estudio-list'),
    path('materias/', MateriaList.as_view(), name='materia-list'),
    path('materias/<str:codigo>/correlativas/', MateriaCorrelativasTreeView.as_view(), name='materia-correlativas-tree'),
    path('planes/<int:pk>/ciclos/', PlanDeEstudioCiclosView.as_view(), name='plan-ciclos'),
    path('descargar_plan_de_estudio/<int:pk>/', DescargarPlanDeEstudioJSON.as_view(), name='descargar_plan_de_estudio'),
    path('planes/<int:pk>/grafo/', PlanDeEstudioGraphView.as_view(), name='plan-de-estudio-grafo'),

]
