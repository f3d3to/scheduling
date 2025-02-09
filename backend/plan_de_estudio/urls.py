
from django.urls import path
from .views import (
    PlanDeEstudioList,
    MateriaList, DescargarPlanDeEstudioJSON,
    MateriaCorrelativasTreeView,
    PlanDeEstudioCiclosView,
    MateriasEstudiantesListCreateView, MateriasEstudiantesRetrieveUpdateDestroyView,
    EvaluacionesListCreateView, EvaluacionesRetrieveUpdateDestroyView,
    EstadoCarreraView,
    CrearPlanConMaterias,
)
app_name = 'plan_de_estudio'


urlpatterns = [

    # Planes de estudio
    path('planes_de_estudio/', PlanDeEstudioList.as_view(), name='plan_de_estudio-list'),
    path('planes/<int:pk>/ciclos/', PlanDeEstudioCiclosView.as_view(), name='plan-ciclos'),
    path('descargar_plan_de_estudio/<int:pk>/', DescargarPlanDeEstudioJSON.as_view(), name='descargar_plan_de_estudio'),

    # Materias
    path('materias/', MateriaList.as_view(), name='materia-list'),
    path('materias/<str:codigo>/correlativas/', MateriaCorrelativasTreeView.as_view(), name='materia-correlativas-tree'),
    path('materias/estudiantes/', MateriasEstudiantesListCreateView.as_view(), name='materia-estudiante-create'),
    path('materias/estudiantes/<int:pk>/', MateriasEstudiantesRetrieveUpdateDestroyView.as_view(), name='materias-estudiantes-retrieve-update-destroy'),

    # Evaluaciones
    path('evaluaciones/', EvaluacionesListCreateView.as_view(), name='evaluaciones-list-create'),
    path('evaluaciones/<int:pk>/', EvaluacionesRetrieveUpdateDestroyView.as_view(), name='evaluaciones-retrieve-update-destroy'),

    path('carrera/<int:carrera_id>/estado/', EstadoCarreraView.as_view(), name='estado-carrera'),

    path("planes/crear-con-materias/", CrearPlanConMaterias.as_view(), name="crear-plan-con-materias"),


]
