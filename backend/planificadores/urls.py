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
]
