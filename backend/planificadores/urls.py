from django.urls import path
from .views import (
    EstadoListCreateView, EstadoRetrieveUpdateDestroyView,
    PlanificadorListCreateView, PlanificadorRetrieveUpdateDestroyView,
    EstructuraPlanificadorListCreateView, EstructuraPlanificadorRetrieveUpdateDestroyView,
    CeldaListCreateView, CeldaRetrieveUpdateDestroyView,
    ElementoListCreateView, ElementoRetrieveUpdateDestroyView,
    ActividadListCreateView, ActividadRetrieveUpdateDestroyView,
    TareaListCreateView, TareaRetrieveUpdateDestroyView,
    ObjetivoListCreateView, ObjetivoRetrieveUpdateDestroyView,
    PlanificadorDetailView,
    CeldaContenidoUpdate,
    EstructuraPlanificadorUpdateAPIView,
    AsociarElementoAPIView,
    ModeloAPIView,
    ElementoDetailView,
)

app_name = "planificadores"

urlpatterns = [
    # Estructura Planificador
    path('estructuras-planificador/', EstructuraPlanificadorListCreateView.as_view(), name='estructura-planificador-list-create'),
    path('estructuras-planificador/<int:pk>/', EstructuraPlanificadorRetrieveUpdateDestroyView.as_view(), name='estructura-planificador-detail'),

    # Estado
    path('estados/', EstadoListCreateView.as_view(), name='estado-list-create'),
    path('estados/<int:pk>/', EstadoRetrieveUpdateDestroyView.as_view(), name='estado-detail'),

    # Planificador
    path('planificadores/', PlanificadorListCreateView.as_view(), name='planificador-list-create'),
    path('planificadores-eliminar/<int:pk>/', PlanificadorRetrieveUpdateDestroyView.as_view(), name='planificador-detail'),

    # Celda
    path('celdas/', CeldaListCreateView.as_view(), name='celda-list-create'),
    path('celdas/<int:pk>/', CeldaRetrieveUpdateDestroyView.as_view(), name='celda-detail'),

    # Elemento
    path('elementos/', ElementoListCreateView.as_view(), name='elemento-list-create'),
    path('elementos/<int:pk>/', ElementoRetrieveUpdateDestroyView.as_view(), name='elemento-detail'),

    # Actividad
    path('actividades/', ActividadListCreateView.as_view(), name='actividad-list-create'),
    path('actividades/<int:pk>/', ActividadRetrieveUpdateDestroyView.as_view(), name='actividad-detail'),

    # Tarea
    path('tareas/', TareaListCreateView.as_view(), name='tarea-list-create'),
    path('tareas/<int:pk>/', TareaRetrieveUpdateDestroyView.as_view(), name='tarea-detail'),

    # Objetivo
    path('objetivos/', ObjetivoListCreateView.as_view(), name='objetivo-list-create'),
    path('objetivos/<int:pk>/', ObjetivoRetrieveUpdateDestroyView.as_view(), name='objetivo-detail'),

    path('planificadores/<int:pk>/', PlanificadorDetailView.as_view(), name='planificador-detail'),

    path('planificadores/<int:planificador_id>/celdas/<int:celda_id>/', CeldaContenidoUpdate.as_view(), name='update_celda_content'),
    path('planificador/estructura/actualizar/<int:pk>/', EstructuraPlanificadorUpdateAPIView.as_view(), name='update-celdas-estructura'),

    path('models/', ModeloAPIView.as_view(), name='models'),
    path('celdas/<int:planificador_id>/<int:celda_id>/elementos/', AsociarElementoAPIView.as_view(), name='asociar-elemento'),

    path('elementos/detalle/<int:content_type_id>/<int:object_id>/', ElementoDetailView.as_view(), name='elemento-detail'),
]
