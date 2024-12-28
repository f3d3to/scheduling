from django.urls import path
from .views import (
    EstadoListCreateView, EstadoRetrieveUpdateDestroyView,
    PlanificadorListCreateView, PlanificadorRetrieveUpdateDestroyView,
    EstructuraPlanificadorListCreateView, EstructuraPlanificadorRetrieveUpdateDestroyView,
    CeldaListCreateView, CeldaRetrieveUpdateDestroyView,
    ElementoListCreateView, ElementoRetrieveUpdateDestroyView,
    MensajeListCreateView, MensajeRetrieveUpdateDestroyView,
    ActividadListCreateView, ActividadRetrieveUpdateDestroyView,
    TareaListCreateView, TareaRetrieveUpdateDestroyView,
    RegistroProgresoListCreateView, RegistroProgresoRetrieveUpdateDestroyView,
    ObjetivoListCreateView, ObjetivoRetrieveUpdateDestroyView,
    EtiquetaListCreateView, EtiquetaRetrieveUpdateDestroyView,
    ComentarioListCreateView, ComentarioRetrieveUpdateDestroyView,
    RecurrenteListCreateView, RecurrenteRetrieveUpdateDestroyView,
    EventoListCreateView, EventoRetrieveUpdateDestroyView,
    EventoAsociadoListCreateView, EventoAsociadoRetrieveUpdateDestroyView,
    PlanificadorDetailView,
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

    # Mensaje
    path('mensajes/', MensajeListCreateView.as_view(), name='mensaje-list-create'),
    path('mensajes/<int:pk>/', MensajeRetrieveUpdateDestroyView.as_view(), name='mensaje-detail'),

    # Actividad
    path('actividades/', ActividadListCreateView.as_view(), name='actividad-list-create'),
    path('actividades/<int:pk>/', ActividadRetrieveUpdateDestroyView.as_view(), name='actividad-detail'),

    # Tarea
    path('tareas/', TareaListCreateView.as_view(), name='tarea-list-create'),
    path('tareas/<int:pk>/', TareaRetrieveUpdateDestroyView.as_view(), name='tarea-detail'),

    # Registro de Progreso
    path('registros-progreso/', RegistroProgresoListCreateView.as_view(), name='registro-progreso-list-create'),
    path('registros-progreso/<int:pk>/', RegistroProgresoRetrieveUpdateDestroyView.as_view(), name='registro-progreso-detail'),

    # Objetivo
    path('objetivos/', ObjetivoListCreateView.as_view(), name='objetivo-list-create'),
    path('objetivos/<int:pk>/', ObjetivoRetrieveUpdateDestroyView.as_view(), name='objetivo-detail'),

    # Etiqueta
    path('etiquetas/', EtiquetaListCreateView.as_view(), name='etiqueta-list-create'),
    path('etiquetas/<int:pk>/', EtiquetaRetrieveUpdateDestroyView.as_view(), name='etiqueta-detail'),

    # Comentario
    path('comentarios/', ComentarioListCreateView.as_view(), name='comentario-list-create'),
    path('comentarios/<int:pk>/', ComentarioRetrieveUpdateDestroyView.as_view(), name='comentario-detail'),

    # Recurrente
    path('recurrentes/', RecurrenteListCreateView.as_view(), name='recurrente-list-create'),
    path('recurrentes/<int:pk>/', RecurrenteRetrieveUpdateDestroyView.as_view(), name='recurrente-detail'),

    # Evento
    path('eventos/', EventoListCreateView.as_view(), name='evento-list-create'),
    path('eventos/<int:pk>/', EventoRetrieveUpdateDestroyView.as_view(), name='evento-detail'),

    # Evento Asociado
    path('eventos-asociados/', EventoAsociadoListCreateView.as_view(), name='evento-asociado-list-create'),
    path('eventos-asociados/<int:pk>/', EventoAsociadoRetrieveUpdateDestroyView.as_view(), name='evento-asociado-detail'),

    path('planificadores/<int:pk>/', PlanificadorDetailView.as_view(), name='planificador-detail'),
]
