from django.urls import path
from .views import (
    PlanificadorListCreateView,
    PlanificadorDetailView,
    EstructuraPlanificadorListCreateView,
    EstructuraPlanificadorDetailView,
    ActividadListCreateView,
    ActividadDetailView,
    TareaListCreateView,
    TareaDetailView,
    EstadoListCreateView,
    EstadoDetailView,
    TipoPlanificadorListCreateView,
    TipoPlanificadorDetailView,
    ObjetivoListCreateView,
    ObjetivoDetailView,
    RegistroProgresoListCreateView,
    RegistroProgresoDetailView,
)

app_name = 'planificadores'

urlpatterns = [
    # Planificadores
    path('planificadores/', PlanificadorListCreateView.as_view(), name='planificador-list-create'),
    path('planificadores/<int:pk>/', PlanificadorDetailView.as_view(), name='planificador-detail'),

    # Estructuras de Planificadores
    path('estructuras/', EstructuraPlanificadorListCreateView.as_view(), name='estructura-list-create'),
    path('estructuras/<int:pk>/', EstructuraPlanificadorDetailView.as_view(), name='estructura-detail'),

    # Actividades
    path('actividades/', ActividadListCreateView.as_view(), name='actividad-list-create'),
    path('actividades/<int:pk>/', ActividadDetailView.as_view(), name='actividad-detail'),

    # Tareas
    path('tareas/', TareaListCreateView.as_view(), name='tarea-list-create'),
    path('tareas/<int:pk>/', TareaDetailView.as_view(), name='tarea-detail'),

    # Estados
    path('estados/', EstadoListCreateView.as_view(), name='estado-list-create'),
    path('estados/<int:pk>/', EstadoDetailView.as_view(), name='estado-detail'),

    # Tipos de Planificador
    path('tipos-planificador/', TipoPlanificadorListCreateView.as_view(), name='tipo-planificador-list-create'),
    path('tipos-planificador/<int:pk>/', TipoPlanificadorDetailView.as_view(), name='tipo-planificador-detail'),

    # Objetivos
    path('objetivos/', ObjetivoListCreateView.as_view(), name='objetivo-list-create'),
    path('objetivos/<int:pk>/', ObjetivoDetailView.as_view(), name='objetivo-detail'),

    # Registros de Progreso
    path('registros-progreso/', RegistroProgresoListCreateView.as_view(), name='registro-progreso-list-create'),
    path('registros-progreso/<int:pk>/', RegistroProgresoDetailView.as_view(), name='registro-progreso-detail'),
]
