# backend/evento_academico/urls.py
from django.urls import path
from . import views

app = "evento_academico"

urlpatterns = [
    # MetaAcademica
    path('metas/', views.MetaAcademicaListCreateView.as_view(), name='meta-list-create'),
    path('metas/<int:pk>/', views.MetaAcademicaDetailView.as_view(), name='meta-detail'),

    # ProgresoMateria
    path('progreso/', views.ProgresoMateriaListCreateView.as_view(), name='progreso-list-create'),
    path('progreso/<int:pk>/', views.ProgresoMateriaDetailView.as_view(), name='progreso-detail'),

    # RecordatorioPersonalizado
    path('recordatorios/', views.RecordatorioPersonalizadoListCreateView.as_view(), name='recordatorio-list-create'),
    path('recordatorios/<int:pk>/', views.RecordatorioPersonalizadoDetailView.as_view(), name='recordatorio-detail'),

    # EventoAcademico
    path('eventos-academicos/', views.EventoAcademicoListCreateView.as_view(), name='evento-list-create'),
    path('eventos-academicos/<int:pk>/', views.EventoAcademicoDetailView.as_view(), name='evento-detail'),

    # PlanificacionAcademica
    path('planificaciones/', views.PlanificacionAcademicaListCreateView.as_view(), name='planificacion-list-create'),
    path('planificaciones/<int:pk>/', views.PlanificacionAcademicaDetailView.as_view(), name='planificacion-detail'),

    # ActividadPlanificada
    path('actividades-academicas/', views.ActividadPlanificadaListCreateView.as_view(), name='actividad-list-create'),
    path('actividades-academicas/<int:pk>/', views.ActividadPlanificadaDetailView.as_view(), name='actividad-detail'),
]